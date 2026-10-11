#!/usr/bin/env python3
"""Readiness gate G2: run calibration tasks on every free provider group through
PlumMe's real execution path and record receipts for `fse independence`.

Harness code, not part of the evaluator: it imports the installed PlumMe on the host.

Safety: it refuses to start unless PLUMME_COST_POLICY=FREE_ONLY, re-checks the cost
class of every offer before each call, and acquires every lease PINNED to an offer the
hard-eligibility gate admitted. A paid route cannot be executed by this script.

Steps:
1. Supply census: every discovered offer with adapter, provider, model, cost class,
   independence key, grounding and the gate's verdict for the REASONING role. The
   census also counts grounded free offers, which CherryMe's SCIENCE and REUSE
   questions require (arm F3).
2. Selection: eligible free offers grouped by independence key; up to --per-group
   offers per group, in PlumMe's own ranking order.
3. Calibration: every task on every selected offer, task-major so rate limits spread.
   One PINNED lease and one execution per call; nothing is retried by this script.

Output in --out: census.json, results.jsonl (one row per call), run.json, and the
run's DecisionLog in state/decisions.jsonl. The production DecisionLog is not touched.
"""
from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import os
import platform
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FREE = {"ANONYMOUS_FREE", "FREE_TIER"}
GROUNDED = {"WEB_SEARCH", "RETRIEVAL", "TOOL_GROUNDED"}
SCHEMA = "FSE-G2-RUN/1"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _value(x) -> str:
    return str(getattr(x, "value", x))


def load_tasks(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or any(not {"task_id", "prompt"} <= set(r) for r in rows):
        raise SystemExit("tasks file must hold JSON lines with task_id and prompt")
    return rows


def census(service, role: str) -> tuple[list[dict], list]:
    from plumme.models import ExecutionRequest

    eligible, rejected = service.scheduler.screen(ExecutionRequest(task="fse g2 census", role_id=role, consumer="fse-g2"))
    ranked = service.scheduler.policy.rank(ExecutionRequest(task="fse g2 census", role_id=role, consumer="fse-g2"), eligible)
    eligible_ids = {o.offer_id for o in eligible}
    rows = []
    for offer in service.store.offers.values():
        rows.append({
            "offer_id": offer.offer_id, "adapter": offer.adapter, "provider": offer.provider, "model": offer.model,
            "model_family": offer.model_family, "cost_class": _value(offer.cost_class),
            "independence_key": _independence_key(offer), "independence_basis": _independence_basis(offer),
            "grounding": _value(offer.grounding), "health": _value(getattr(offer, "health", "UNKNOWN")),
            "independence_group_declared": bool(getattr(offer, "independence_group", None)),
            "eligible_reasoning": offer.offer_id in eligible_ids, "gate_reasons": rejected.get(offer.offer_id, []),
        })
    return sorted(rows, key=lambda r: (r["adapter"], r["model"])), ranked


def _independence_key(offer) -> str:
    from plumme.knowledge import independence_key   # the helper PlumMe's scheduler and receipts use
    return independence_key(offer)


def _independence_basis(offer) -> str:
    from plumme.knowledge import independence_basis  # HEURISTIC when only the model_family string is known
    return independence_basis(offer)


async def run_call(service, offer, task: dict, role: str, max_output_tokens: int) -> dict:
    from plumme.models import BudgetEnvelope, NeuronExecution, NeuronRequest, SelectionMode

    row = {"task_id": task["task_id"], "offer_id": offer.offer_id, "group": _independence_key(offer),
           "independence_basis": _independence_basis(offer),
           "provider": offer.provider, "model": offer.model, "adapter": offer.adapter,
           "cost_class": _value(offer.cost_class), "started_at": _now()}
    if row["cost_class"] not in FREE:            # belt and braces: never execute a non-free offer
        row.update(success=False, structural_state="FAILED", failure_class="FSE_REFUSED_NON_FREE")
        return row
    budget = BudgetEnvelope(max_calls=1, max_output_tokens=max_output_tokens, max_concurrency=1)
    try:
        lease = await service.acquire_neuron(NeuronRequest(
            consumer="fse-g2", objective=task["prompt"], role_id=role, selection_mode=SelectionMode.PINNED,
            pinned_offer_hint=offer.offer_id, budget=budget, metadata={"fse_task_id": task["task_id"]}))
        result = await service.execute_lease(NeuronExecution(lease_id=lease.lease_id, task=task["prompt"], budget=budget))
    except Exception as exc:
        row.update(success=False, structural_state="FAILED", failure_class=f"HARNESS_{type(exc).__name__}",
                   failure_message=str(exc)[:300])
        return row
    receipt = result.receipt
    row.update(success=result.success, structural_state=_value(result.structural_state),
               failure_class=result.failure_class, output=(result.output or "")[:4000],
               lease_id=result.lease_id)
    if receipt is not None:
        row.update(receipt_id=receipt.receipt_id, decision_id=receipt.decision_id, latency_ms=receipt.latency_ms,
                   input_tokens=receipt.usage.input_tokens, output_tokens=receipt.usage.output_tokens,
                   cost_usd=receipt.usage.cost_usd, executed_offer_id=receipt.offer_id,
                   model_fingerprint=(receipt.metadata or {}).get("model_fingerprint"),
                   provider_reported_model=(receipt.metadata or {}).get("provider_reported_model"))
        if receipt.offer_id and receipt.offer_id != offer.offer_id:
            row["warning"] = "EXECUTED_OFFER_DIFFERS_FROM_PINNED_OFFER"
    return row


async def main_async(args) -> int:
    import plumme
    from plumme.config import Settings
    from plumme.service import PlumMeService

    base = Settings.load()
    if base.cost_policy != "FREE_ONLY":
        print("refusing to run: PLUMME_COST_POLICY must be FREE_ONLY", file=sys.stderr)
        return 3
    out = Path(args.out).resolve()
    (out / "state").mkdir(parents=True, exist_ok=True)
    settings = dataclasses.replace(base, state_dir=out / "state", receipt_file=out / "state" / "receipts.jsonl",
                                   decision_log=out / "state" / "decisions.jsonl")
    tasks = load_tasks(Path(args.tasks))[: args.limit or None]
    service = PlumMeService(settings)
    await service.store.discover()
    offers, ranked = census(service, args.role)
    free_eligible = [o for o in ranked if _value(o.cost_class) in FREE]
    by_group: dict[str, list] = defaultdict(list)
    for offer in free_eligible:
        by_group[_independence_key(offer)].append(offer)
    selected = [o for group in sorted(by_group) for o in by_group[group][: args.per_group]]
    summary = {
        "offers": len(offers),
        "free_offers": sum(1 for o in offers if o["cost_class"] in FREE),
        "free_eligible_reasoning": len(free_eligible),
        "free_groups": len(by_group),
        "grounded_free_offers": sum(1 for o in offers if o["cost_class"] in FREE and o["grounding"] in GROUNDED),
        # CherryMe treats offers without a declared independence group as one shared group
        # ("UNKNOWN"), so ACE can recruit independent workers only among declared groups.
        "free_offers_with_declared_independence_group": sum(
            1 for o in offers if o["cost_class"] in FREE and o["independence_group_declared"]),
        "declared_free_independence_groups": len({o["independence_key"] for o in offers
                                                  if o["cost_class"] in FREE and o["independence_group_declared"]}),
        "selected_offers": [{"offer_id": o.offer_id, "group": _independence_key(o), "model": o.model,
                             "provider": o.provider} for o in selected],
    }
    (out / "census.json").write_text(json.dumps({"schema": SCHEMA, "recorded_at": _now(), "summary": summary,
                                                 "offers": offers}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"census": summary}, indent=2), file=sys.stderr)
    if args.census_only or not selected:
        return 0 if selected else 1
    t0 = time.time()
    results_path = out / "results.jsonl"
    with results_path.open("a", encoding="utf-8") as handle:
        for task in tasks:
            rows = await asyncio.gather(*(run_call(service, o, task, args.role, args.max_output_tokens) for o in selected))
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            if args.pause:
                await asyncio.sleep(args.pause)
    run = {"schema": SCHEMA, "finished_at": _now(), "seconds": round(time.time() - t0, 1),
           "plumme": {"version": plumme.__version__, "module": str(Path(plumme.__file__).resolve().parent)},
           "python": sys.version.split()[0], "host": platform.node(), "tasks_file": str(Path(args.tasks).resolve()),
           "tasks": len(tasks), "selected_offers": summary["selected_offers"], "role": args.role,
           "cost_policy": base.cost_policy, "env_keys": sorted(k for k in os.environ if k.startswith("PLUMME_")),
           "results": str(results_path), "decision_log": str(out / "state" / "decisions.jsonl")}
    (out / "run.json").write_text(json.dumps(run, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tasks", required=True, help="calibration tasks from `fse calib generate`")
    ap.add_argument("--out", required=True)
    ap.add_argument("--role", default="REASONING")
    ap.add_argument("--per-group", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0, help="first N tasks only (0 = all)")
    ap.add_argument("--max-output-tokens", type=int, default=1024)
    ap.add_argument("--pause", type=float, default=0.0, help="seconds between tasks")
    ap.add_argument("--census-only", action="store_true")
    return asyncio.run(main_async(ap.parse_args(argv)))


if __name__ == "__main__":
    raise SystemExit(main())
