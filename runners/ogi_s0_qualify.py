"""OGI-013 stage S0: REASONING qualification of candidate lineages (PROTOCOL §3, STAGE_BUDGET §2; owner-approved 2026-11-09).

Items: MATH-500 levels 1-4 (never level 5 = F1), the first N by sha256("OGI013-S0|"+id); the same items for every candidate, one trial each.
Candidates: PlumMe's own REASONING ranking (query_supply, no inference), one offer per distinct independence_key, the owner-allowed subscription
lineages first. Every call: PeachMe WorkerPool pinned to the candidate's model_key (fs_org_driver.peach_host().worker), graded by math-verify after
the call, then fed to PlumMe as VERIFIED decision feedback (single worker -> competence). A call served by another lineage is IDENTITY_MISMATCH:
recorded, never graded, never fed back. Resumable: rows already in rows.jsonl are not re-run. Caps: --max-calls (360), --max-tokens (1.1M), USD 0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import ogi_tasks as T
from fs_org_driver import Task, peach_host
from fs_runtime import operational_service

SUBSCRIPTION = ("gpt-6-luna", "claude-haiku-5-5")
# S0-A2 (pre-outcome): a roster lineage must be a foundation-model family with its own pre-training. PlumMe derives lineage from the model name,
# so a community fine-tune (e.g. mini-magnum = a Mistral-Nemo fine-tune) would otherwise count as an independent lineage.
FOUNDATION_LINEAGES = frozenset({"gpt", "claude", "gemini", "gemma", "mistral", "qwen", "llama", "nemotron", "deepseek", "glm", "allam", "command",
                                 "cohere", "phi", "granite", "olmo", "kimi", "minimax", "yi", "jamba", "sdaia"})


def items(n: int) -> list:
    rows = [json.loads(x) for x in T._verified("math-500").read_text().splitlines() if x.strip()]
    pool = sorted((r for r in rows if r["level"] != 5), key=lambda r: hashlib.sha256(f"OGI013-S0|{r['unique_id']}".encode()).hexdigest())
    return [T.make_task("math", r) for r in pool[:n]]


def candidates(svc, k: int) -> list[dict]:
    import asyncio
    ranked = asyncio.run(svc.query_supply({"consumer": "ogi013-s0", "role_id": "REASONING", "objective": "solve a competition math problem; final answer in \\boxed{}"}))
    from plumme.knowledge import independence_key
    for o in ranked:                                   # PlumMe's own lineage rule (the one leases and the identity guard use)
        off = svc.store.offers.get(o.get("offer_id"))
        o["independence_key"] = independence_key(off) if off is not None else None
    seen, out = set(), []
    for o in sorted(ranked, key=lambda o: 0 if any(m in str(o.get("model_key") or o.get("model")) for m in SUBSCRIPTION) else 1):   # stable: PlumMe order otherwise
        lin = o.get("independence_key")
        if lin and lin not in seen and o.get("model_key"):
            seen.add(lin)
            out.append({"model_key": o["model_key"], "independence_key": lin, "provider": o.get("provider"), "cost_class": o.get("cost_class")})
    return out[:k]


def candidates_from_reliability(svc, k: int, window_h: float = 24) -> list[dict]:
    """S0-A2 rule (fixed before any S0 accuracy was read): PlumMe's own RELIABLE models, one per vendor lineage (highest usable share, then most
    calls), the owner-allowed subscription lineages first; pinned by the route's model_key."""
    from plumme.knowledge import independence_key
    from plumme.reliability import report
    rel = report(svc.settings.receipt_file, window_h=window_h)["models"]
    by_name = {}
    for o in svc.store.offers.values():
        for name in (getattr(o, "canonical_model_id", None), o.model):
            if name and o.model_key:
                by_name.setdefault(name, o)
    ranked = sorted(((k_, v) for k_, v in rel.items() if v["status"] == "RELIABLE" and k_ in by_name),
                    key=lambda kv: (0 if any(m in kv[0] for m in SUBSCRIPTION) else 1, -kv[1]["usable_rate"], -kv[1]["calls"], kv[0]))
    seen, out = set(), []
    for name, v in ranked:
        o = by_name[name]
        lin = {"sdaia": "allam", "gemma": "gemini", "cohere": "command"}.get(v["vendor_lineage"], v["vendor_lineage"])   # one vendor, one lineage
        if lin and lin in FOUNDATION_LINEAGES and lin not in seen:
            seen.add(lin)
            out.append({"model_key": o.model_key, "independence_key": independence_key(o), "vendor_lineage": lin, "provider": o.provider,
                        "cost_class": str(getattr(o.cost_class, "value", o.cost_class)), "usable_rate": v["usable_rate"], "calls": v["calls"]})
    return out[:k]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--items", type=int, default=30)
    ap.add_argument("--candidates", type=int, default=8)
    ap.add_argument("--max-calls", type=int, default=360)
    ap.add_argument("--max-tokens", type=int, default=1_100_000)
    ap.add_argument("--candidates-from", choices=("ranking", "reliability"), default="ranking")
    ap.add_argument("--rerun-host-defect", default="", help="failure_class of rows caused by a documented host defect; such rows stay in rows.jsonl and are re-run once")
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    rows_f = a.out / "rows.jsonl"
    done = [json.loads(x) for x in rows_f.read_text().splitlines()] if rows_f.exists() else []
    redo = {(r["candidate"], r["item"]) for r in done if a.rerun_host_defect and r.get("failure_class") == a.rerun_host_defect}
    redo -= {(r["candidate"], r["item"]) for r in done if r.get("rerun_of") == a.rerun_host_defect}     # once only
    seen = {(r["candidate"], r["item"]) for r in done} - redo
    calls, tokens = len(done), sum((r.get("input_tokens") or 0) + (r.get("output_tokens") or 0) for r in done)
    svc = operational_service()
    cand_f = a.out / "candidates.json"
    cands = json.loads(cand_f.read_text()) if cand_f.exists() else (       # frozen at first start
        candidates_from_reliability(svc, a.candidates) if a.candidates_from == "reliability" else candidates(svc, a.candidates))
    cand_f.write_text(json.dumps(cands, indent=1))
    tasks = items(a.items)
    # a measurement: the pinned candidate must answer or the call fails - never another model under its name (PeachMe pin_binding, PR #41)
    host = peach_host(svc, a.out / "episodes", worker_budget={"max_calls": 2, "max_tokens": 12000, "max_cost_usd": 0.0}, max_workers=1, max_replacements=0,
                      pin_binding="PINNED")
    print(f"S0: {len(cands)} candidates x {len(tasks)} items; resume at {calls} calls", file=sys.stderr, flush=True)
    for c in cands:
        for t in tasks:
            if (c["model_key"], t.id) in seen:
                continue
            if calls >= a.max_calls or tokens >= a.max_tokens:
                print(json.dumps({"stop": "BUDGET_STOP", "calls": calls, "tokens": tokens}), file=sys.stderr)
                return 3
            work, events = host.worker(Task(t.id, t.prompt, None, None, "math-verify"))
            try:
                res = work(t.prompt, "solve", prefer=c["model_key"])
            except Exception as exc:  # noqa: BLE001 - lease/route failure: infrastructure, recorded
                res = {"success": False, "failure_class": f"{type(exc).__name__}: {str(exc)[:160]}"}
            calls += 1
            tokens += (res.get("input_tokens") or 0) + (res.get("output_tokens") or 0)
            row = {"candidate": c["model_key"], "declared_lineage": c["independence_key"], "item": t.id, "served_model": res.get("model_key"),
                   "served_lineage": res.get("independence_key"), "receipt_id": res.get("receipt_id"), "decision_id": res.get("decision_id"),
                   "input_tokens": res.get("input_tokens"), "output_tokens": res.get("output_tokens"), "failure_class": res.get("failure_class"),
                   "events": [e["type"] for e in events], **({"rerun_of": a.rerun_host_defect} if (c["model_key"], t.id) in redo else {})}
            if not res.get("success"):
                row["status"] = "INFRA"
            elif res.get("independence_key") != c["independence_key"]:
                row["status"] = "IDENTITY_MISMATCH"
            else:
                g = T.grade(t, res["output"])
                row.update(status="GRADED", correct=bool(g["correct"]), parsable=g["evidence"]["parsable"])
                fb = svc.record_decision_feedback(res["decision_id"], epistemic_state="VERIFIED", verified_utility=1.0 if g["correct"] else 0.0,
                                                  verifier="math-verify==0.9.0:MATH-500-L1-4", receipt_id=res.get("receipt_id"), note=f"OGI013-S0 {t.id}")
                row["feedback"] = fb.get("feedback_id") if isinstance(fb, dict) else str(fb)[:80]
            with rows_f.open("a") as f:
                f.write(json.dumps(row) + "\n")
            print(f"{calls} {c['model_key']} {t.id} {row['status']} {row.get('correct', '')}", file=sys.stderr, flush=True)
    comp = svc.scheduler.competence
    report = {"candidates": cands, "profiles": {c["model_key"]: comp.profile(c["model_key"], "REASONING") for c in cands},
              "calls": calls, "tokens": tokens}
    (a.out / "S0_REPORT.json").write_text(json.dumps(report, indent=1, default=str))
    print(json.dumps({"done": True, "calls": calls, "tokens": tokens}), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
