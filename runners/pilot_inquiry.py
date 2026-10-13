#!/usr/bin/env python3
"""Pilot runner (FRUITSTACK-EVAL-001 phase 2): the 50 inquiry tasks on arms F1 and F3.

Harness code: imports the installed PlumMe and, for F3, CherryMe and AppleMe on the host.
It never reads task references; grading happens afterwards with `fse inquiry grade`.

Arms (protocol v0.2, §5):
  F1  best free single model: one PINNED PlumMe call per task on the offer named by
      --offer, chosen beforehand by the pre-registered rule (`best_single_offer` of
      `fse independence` on the G2 calibration, never on pilot tasks).
  F3  ledger + bootstrap ensemble rule + trajectory and claim assurance: CherryMe with
      the ACE skill, its persistent workspace, PlumMe as labor market and AppleMe as the
      assurance tier. VERDICT comes from CherryMe's claim status (SUPPORTED, REFUTED;
      UNKNOWN and CONFLICT become NOT_ENOUGH_INFO). KEY is extracted from CherryMe's own
      evidence by one composer call; a key that does not literally occur in that
      evidence is replaced by UNKNOWN (strict scoring, pre-registered as primary).
  A   paid frontier model: refused here. Arm A starts only after the owner approved its
      actual cost (FRUITSTACK-EVAL-001) and needs its own, separately approved run.

Safety: refuses to start unless PLUMME_COST_POLICY=FREE_ONLY; every call goes through
PlumMe's hard-eligibility gate under that policy. Quota units in the pilot are provider
calls (successful or not); per-provider allowance normalization is fixed later.

Output in --out: results-<ARM>.jsonl (task_id, arm, output, quota_units, cost_eur,
wall_seconds, status, diagnostics) and the arm's DecisionLog under state-<ARM>/.
"""
from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

FREE = {"ANONYMOUS_FREE", "FREE_TIER"}
VERDICT_OF_STATUS = {"SUPPORTED": "SUPPORTED", "REFUTED": "REFUTED", "UNKNOWN": "NOT_ENOUGH_INFO",
                     "CONFLICT": "NOT_ENOUGH_INFO"}
SCHEMA = "FSE-PILOT-RUN/1"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _value(x) -> str:
    return str(getattr(x, "value", x))


def load_tasks(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    out = []
    for row in rows:
        if row.get("family") != "INQUIRY":
            continue
        claim = re.search(r"^Claim: (.+)$", row["prompt"], re.M)
        question = re.search(r"^Question: (.+)$", row["prompt"], re.M)
        if not claim or not question:
            raise SystemExit(f"{row['task_id']}: prompt is not in FSE-INQUIRY/1 form")
        # The runner keeps only what the arms may see. References stay unread.
        out.append({"task_id": row["task_id"], "prompt": row["prompt"], "claim": claim.group(1),
                    "question": question.group(1)})
    if not out:
        raise SystemExit("no INQUIRY tasks found")
    return out


def isolated(base, out: Path, arm: str):
    state = out / f"state-{arm}"
    state.mkdir(parents=True, exist_ok=True)
    # Keep every decision of the run in memory so per-task quota counts stay exact.
    return dataclasses.replace(base, state_dir=state, receipt_file=state / "receipts.jsonl",
                               decision_log=state / "decisions.jsonl", decision_memory_limit=1_000_000)


def decision_count(service) -> int:
    """Provider-facing decisions so far (ACQUIRE and FALLBACK); ENSEMBLE records route nothing."""
    return sum(len(d.choices) for d in service.scheduler.decisions.decisions.values()
               if _value(d.kind) != "ENSEMBLE")


def cost_eur_from_usd(cost_usd: float | None) -> float | None:
    """FREE_ONLY proves EUR zero only when the receipt explicitly reports USD zero."""
    if cost_usd is None or cost_usd != 0:
        return None
    return 0.0


def receipts_since(path: Path, offset: int) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as stream:
        stream.seek(offset)
        return [json.loads(line) for line in stream if line.strip()]


def receipt_cost_eur(receipts: list[dict], provider_calls: int) -> float | None:
    if not receipts:
        return 0.0 if provider_calls == 0 else None
    costs = [receipt.get("usage", {}).get("cost_usd") for receipt in receipts]
    if any(cost is None or cost != 0 for cost in costs):
        return None
    return 0.0


def f3_configuration_error(args) -> str | None:
    if args.arm != "F3":
        return None
    if args.no_assurance:
        return "--no-assurance is not allowed for protocol arm F3"
    if not args.composer_offer:
        return "--composer-offer is required for protocol arm F3"
    return None


async def pinned_call(service, offer_id: str, task_text: str, *, consumer: str, max_output_tokens: int,
                      metadata: dict) -> dict:
    from plumme.models import BudgetEnvelope, NeuronExecution, NeuronRequest, SelectionMode
    budget = BudgetEnvelope(max_calls=1, max_output_tokens=max_output_tokens, max_concurrency=1)
    try:
        lease = await service.acquire_neuron(NeuronRequest(
            consumer=consumer, objective=task_text, role_id="REASONING", selection_mode=SelectionMode.PINNED,
            pinned_offer_hint=offer_id, budget=budget, metadata=metadata))
        result = await service.execute_lease(NeuronExecution(lease_id=lease.lease_id, task=task_text, budget=budget))
    except Exception as exc:
        return {"success": False, "failure_class": f"HARNESS_{type(exc).__name__}", "detail": str(exc)[:300]}
    receipt = result.receipt
    row = {"success": bool(result.success), "output": result.output, "failure_class": result.failure_class,
           "structural_state": _value(result.structural_state)}
    if receipt is not None:
        row.update(receipt_id=receipt.receipt_id, decision_id=receipt.decision_id, offer_id=receipt.offer_id,
                   input_tokens=receipt.usage.input_tokens, output_tokens=receipt.usage.output_tokens,
                   cost_usd=receipt.usage.cost_usd, model_fingerprint=(receipt.metadata or {}).get("model_fingerprint"))
    return row


def check_offer(service, offer_id: str) -> None:
    offer = service.store.offers.get(offer_id)
    if offer is None:
        raise SystemExit(f"offer {offer_id} is not in the discovered supply")
    if _value(offer.cost_class) not in FREE:
        raise SystemExit(f"offer {offer_id} is {_value(offer.cost_class)}, not free")


def supply_gate(settings, report_path: Path, minimum: int) -> str | None:
    """Refuse to start on thin supply: an evaluation on a fraction of the free market measures the outage, not the system."""
    from plumme.service import PlumMeService
    try:
        from plumme.free_supply import free_supply_report
    except ImportError:
        return "SUPPLY_GATE_UNAVAILABLE: this PlumMe has no free-supply report (needs PLUMME-FREE-SUPPLY-001); use --skip-supply-gate only for development"
    service = PlumMeService(settings)
    asyncio.run(service.store.discover())
    report = free_supply_report(service)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    executable = report["headline"]["free_models_executable"]
    if executable < minimum:
        return f"SUPPLY_NOT_READY: {executable} executable free models < {minimum}; gaps by state: {report['states']} (see {report_path})"
    return None


# ---------------------------------------------------------------- F1

async def run_f1(args, settings, tasks) -> list[dict]:
    from plumme.service import PlumMeService
    service = PlumMeService(settings)
    await service.store.discover()
    check_offer(service, args.offer)
    rows = []
    for task in tasks:
        t0, before = time.monotonic(), decision_count(service)
        call = await pinned_call(service, args.offer, task["prompt"], consumer="fse-pilot-f1",
                                 max_output_tokens=args.max_output_tokens, metadata={"fse_task_id": task["task_id"]})
        rows.append({"task_id": task["task_id"], "arm": "F1", "output": call.get("output"),
                     "status": "COMPLETED" if call["success"] else "FAILED",
                     "quota_units": max(0, decision_count(service) - before),
                     "cost_eur": cost_eur_from_usd(call.get("cost_usd")),
                     "wall_seconds": round(time.monotonic() - t0, 2), "offer_id": args.offer, "calls": [call]})
        if args.pause:
            await asyncio.sleep(args.pause)
    return rows


# ---------------------------------------------------------------- F3

def _fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").casefold()
    return re.sub(r"[^a-z0-9]+", "", text)


_DATE_SPANS = re.compile(r"\b\d{4}-\d{1,2}-\d{1,2}\b|\b\d{1,2}\.\s*\d{1,2}\.\s*\d{4}\b"
                         r"|\b\d{1,2}(?:st|nd|rd|th)?\.?\s+[A-Za-zäÄ]+\.?,?\s+\d{4}\b"
                         r"|\b[A-Za-z]+\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b")
_NUMBER_SPANS = re.compile(r"-?\d[\d,.' ]*\d|-?\d")


def key_grounded(key: str | None, evidence_texts: list[str]) -> bool:
    """True if the extracted key occurs in CherryMe's evidence: same date, same number or same text."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from fruitstack_eval import inquiry   # value normalization only; this is not grading

    if not key or key.strip().upper() == "UNKNOWN":
        return False
    text = "\n".join(evidence_texts)
    as_date = inquiry._date(key)
    if as_date:
        return any(inquiry._date(span) == as_date for span in _DATE_SPANS.findall(text))
    as_number = inquiry._number(key)
    if as_number is not None and re.fullmatch(r"[^A-Za-z]*\d[^A-Za-z]*", key.strip()):
        return any(inquiry._number(span) == as_number for span in _NUMBER_SPANS.findall(text))
    needle = _fold(key)
    return bool(needle) and needle in _fold(text)


COMPOSER = ("You extract one value from evidence. Use ONLY the evidence below, never your own knowledge.\n"
            "Claim under inquiry: {claim}\nValue requested: {question}\n\nEvidence:\n{evidence}\n\n"
            "If the evidence does not state the value, write UNKNOWN. End with exactly one line:\nKEY: <value or UNKNOWN>")


def run_f3(args, settings, tasks) -> list[dict]:
    from cherryme import CherryMeEngine
    from cherryme.models import Claim
    from cherryme.plumme_bridge import connect_plumme
    from plumme.service import PlumMeService

    service = PlumMeService(settings)
    registry, investigator = connect_plumme(service=service, refresh=True)
    if args.composer_offer:
        check_offer(service, args.composer_offer)
    rows = []
    for task in tasks:
        t0, before = time.monotonic(), decision_count(service)
        receipts_path = Path(settings.receipt_file)
        receipt_offset = receipts_path.stat().st_size if receipts_path.exists() else 0
        workspace = Path(args.out) / "cherryme" / task["task_id"]
        tier = None
        if not args.no_assurance:
            from cherryme.appleme_bridge import connect_appleme
            tier = connect_appleme(workspace_root=workspace / "appleme")
        diag: dict = {}
        try:
            engine = CherryMeEngine(workspace_root=workspace, registry=registry, investigator=investigator,
                                    orchestration_skill=args.cherryme_skill, assurance_tier=tier)
            claim = Claim(text=task["claim"], importance=1.0)
            engine.add_claim(claim)
            final = engine.run([claim.id], budget=args.budget, call_budget=args.call_budget)[0]
            status = _value(final.status)
            evidence = [f"{e.source_ref}: {e.summary}" for e in final.evidence]
            diag = {"claim_status": status, "evidence_items": len(evidence), "questions": engine.questions_asked,
                    "provider_calls": engine.provider_calls, "provider_failures": engine.provider_failures,
                    "asked_types": list(final.asked_types)}
        except Exception as exc:
            rows.append({"task_id": task["task_id"], "arm": "F3", "output": None, "status": "FAILED",
                         "quota_units": max(0, decision_count(service) - before),
                         "cost_eur": receipt_cost_eur(
                             receipts_since(receipts_path, receipt_offset),
                             max(0, decision_count(service) - before)),
                         "wall_seconds": round(time.monotonic() - t0, 2),
                         "diagnostics": {"error": f"{type(exc).__name__}: {exc}"[:400]}})
            continue
        if status == "INCOMPLETE":      # CherryMe could not finish (supply, budget, abort): a system outcome, never an answer
            diag["incomplete_cause"] = getattr(final, "incomplete_reason", None) or getattr(final, "delta_status", None)
            rows.append({"task_id": task["task_id"], "arm": "F3", "output": None, "status": "INCOMPLETE",
                         "quota_units": max(0, decision_count(service) - before),
                         "cost_eur": receipt_cost_eur(receipts_since(receipts_path, receipt_offset),
                                                      max(0, decision_count(service) - before)),
                         "wall_seconds": round(time.monotonic() - t0, 2), "diagnostics": diag})
            continue
        key, composer = "UNKNOWN", None
        if evidence and args.composer_offer:
            composer = asyncio.run(pinned_call(
                service, args.composer_offer,
                COMPOSER.format(claim=task["claim"], question=task["question"], evidence="\n".join(evidence)[:6000]),
                consumer="fse-pilot-f3-composer", max_output_tokens=256, metadata={"fse_task_id": task["task_id"]}))
            found = re.findall(r"^\W*KEY\s*[:=]\s*(.+?)\s*$", composer.get("output") or "", re.M | re.I)
            proposed = found[-1] if found else "UNKNOWN"
            diag["composer_key"] = proposed
            diag["key_grounded"] = key_grounded(proposed, evidence)
            key = proposed if diag["key_grounded"] else "UNKNOWN"
        verdict = VERDICT_OF_STATUS.get(status, "NOT_ENOUGH_INFO")
        output = f"CherryMe claim status: {status}; evidence items: {len(evidence)}\nVERDICT: {verdict}\nKEY: {key}"
        task_receipts = receipts_since(receipts_path, receipt_offset)
        rows.append({"task_id": task["task_id"], "arm": "F3", "output": output, "status": "COMPLETED",
                     "quota_units": max(0, decision_count(service) - before),
                     "cost_eur": receipt_cost_eur(
                         task_receipts, max(0, decision_count(service) - before)),
                     "wall_seconds": round(time.monotonic() - t0, 2), "diagnostics": diag,
                     "composer": composer})
        if args.pause:
            time.sleep(args.pause)
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--arm", required=True, choices=["F1", "F3", "A"])
    ap.add_argument("--offer", help="F1: the free offer chosen by the pre-registered rule")
    ap.add_argument("--composer-offer", help="F3: required free offer for KEY extraction")
    ap.add_argument("--cherryme-skill", help="F3: directory with the ACE SKILL.md and orchestration.json")
    ap.add_argument("--budget", type=int, default=8, help="F3: CherryMe question budget per task")
    ap.add_argument("--call-budget", type=int, default=24, help="F3: provider call cap per task")
    ap.add_argument("--no-assurance", action="store_true", help="disable AppleMe assurance (invalid for protocol F3)")
    ap.add_argument("--max-output-tokens", type=int, default=1024)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--shard", default="0/1", help="K/N: run every N-th task starting at K (parallel processes, own state dirs)")
    ap.add_argument("--min-free-models", type=int, default=50,
                    help="refuse to start below this many executable free models (`plumme coverage --free`)")
    ap.add_argument("--skip-supply-gate", action="store_true", help="development only: run without the free-supply gate")
    ap.add_argument("--pause", type=float, default=0.0)
    args = ap.parse_args(argv)
    if args.arm == "A":
        print("refusing: arm A needs the owner's approval of its actual cost and a separate run", file=sys.stderr)
        return 3
    if error := f3_configuration_error(args):
        ap.error(error)

    import plumme
    from plumme.config import Settings
    base = Settings.load()
    if base.cost_policy != "FREE_ONLY":
        print("refusing to run: PLUMME_COST_POLICY must be FREE_ONLY", file=sys.stderr)
        return 3
    if args.arm == "F1" and not args.offer:
        ap.error("--offer is required for F1")
    if args.arm == "F3" and not args.cherryme_skill:
        ap.error("--cherryme-skill is required for F3")
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    tasks = load_tasks(Path(args.tasks))[: args.limit or None]
    try:
        k, n = (int(x) for x in args.shard.split("/"))
        assert 0 <= k < n
    except (ValueError, AssertionError):
        ap.error("--shard must be K/N with 0 <= K < N")
    tasks = [t for i, t in enumerate(tasks) if i % n == k]
    tag = args.arm if n == 1 else f"{args.arm}-shard{k}of{n}"
    settings = isolated(base, out, tag)
    if not args.skip_supply_gate:
        gate = supply_gate(settings, out / f"supply-{tag}.json", args.min_free_models)
        if gate is not None:
            print(gate, file=sys.stderr)
            return 4
    t0 = time.time()
    rows = asyncio.run(run_f1(args, settings, tasks)) if args.arm == "F1" else run_f3(args, settings, tasks)
    path = out / f"results-{tag}.jsonl"
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True, default=str) + "\n" for r in rows),
                    encoding="utf-8")
    meta = {"schema": SCHEMA, "arm": args.arm, "finished_at": _now(), "seconds": round(time.time() - t0, 1),
            "tasks": len(tasks), "completed": sum(1 for r in rows if r["status"] == "COMPLETED"),
            "incomplete": sum(1 for r in rows if r["status"] == "INCOMPLETE"), "shard": args.shard,
            "plumme": plumme.__version__, "offer": args.offer, "composer_offer": args.composer_offer,
            "budget": args.budget, "call_budget": args.call_budget, "assurance": not args.no_assurance,
            "cost_policy": base.cost_policy, "env_keys": sorted(k for k in os.environ if k.startswith("PLUMME_")),
            "results": str(path), "decision_log": str(settings.decision_log)}
    try:
        import cherryme
        meta["cherryme"] = getattr(cherryme, "__version__", "unknown")
    except ImportError:
        pass
    (out / f"run-{tag}.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: meta[k] for k in ("arm", "tasks", "completed", "results")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
