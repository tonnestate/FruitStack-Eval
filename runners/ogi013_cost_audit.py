#!/usr/bin/env python3
"""OGI-013 cost audit of ONE episode: reconstruct how a benchmark task generates provider calls, classify every receipt, and relate the organisational spend to its contributions.
Read-only, stdlib only, no network, no inference.

usage: ogi013_cost_audit.py EPISODE_DIR STATE_CHERRY_DIR [--out audit.json] [--md audit.md]
  EPISODE_DIR       e.g. runs/c3-phaseA/airline:2/RG2-RANDOMIZED   (fruitstack/plumme-state/receipts.jsonl, tasks/<id>/fruitstack-events.jsonl, tasks/<id>/org/verifier.log, sim-usage.jsonl)
  STATE_CHERRY_DIR  the engine workspace shared by the arm (<state>/cherry); only rows of claims decided in THIS episode are used

Receipt classes (every receipt row is placed in exactly one, in this priority): verifier_judgment (listed in verifier.log) > worker_proposal (a ledger PROPOSAL/CANDIDATE row cites it)
> agent_step:<tag> (a STEP event cites it) > unreferenced_ok / unreferenced_failed (executed but cited by nothing: nothing in the record shows it influenced a decision).
Influence is read from the record only: a worker/verifier receipt is "decision-influencing" when its claim led to an ORG_REVISION; a promoted verifier pair is a "verified contribution";
an ORG_REVISION with action_changed=true is a "changing revision". Nothing here is a success criterion.
"""
import argparse
import collections
import glob
import json
import os
import sys


def jl(path):
    if not os.path.isfile(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def tok(r):
    u = r.get("usage") or {}
    return (u.get("input_tokens") or 0, u.get("output_tokens") or 0, (r.get("metadata") or {}).get("reasoning_tokens") or 0)


def audit(ep: str, state: str) -> dict:
    receipts = {r["receipt_id"]: r for r in jl(os.path.join(ep, "fruitstack/plumme-state/receipts.jsonl"))}
    task_dirs = sorted(glob.glob(os.path.join(ep, "tasks/*/")))
    events = [e for t in task_dirs for e in jl(os.path.join(t, "fruitstack-events.jsonl"))]
    verifier = [v for t in task_dirs for v in jl(os.path.join(t, "org/verifier.log"))]
    decisions = [e for e in events if e.get("event") == "ORG_DECISION"]
    revisions = [e for e in events if e.get("event") == "ORG_REVISION"]
    claims = {d["claim"] for d in decisions} | {a["claim"] for d in decisions for a in (d.get("atoms") or []) if isinstance(a, dict)}
    ledger = [c for c in jl(os.path.join(state, "contributions.jsonl")) if c.get("claim_id") in claims]
    cherry = [c for c in jl(os.path.join(state, "events.jsonl")) if c.get("claim_id") in claims and c.get("question_type")]

    step_rc = {e.get("receipt"): e.get("tag") for e in events if e.get("event") == "STEP" and e.get("receipt")}
    ver_rc = {rid for v in verifier for rid in (v.get("receipts") or [])}
    prop_rc = {c.get("receipt") for c in ledger if c.get("kind") in ("PROPOSAL", "CANDIDATE") and c.get("receipt")}
    ver_ledger_rc = {c.get("receipt") for c in ledger if c.get("kind") == "VERIFIER" and c.get("receipt")}

    cls = {}
    for rid, r in receipts.items():
        if rid in ver_rc or rid in ver_ledger_rc:
            cls[rid] = "verifier_judgment"
        elif rid in prop_rc:
            cls[rid] = "worker_proposal"
        elif rid in step_rc:
            cls[rid] = "agent_step:" + str(step_rc[rid])
        else:
            cls[rid] = "unreferenced_ok" if r.get("success") else "unreferenced_failed"

    by_class = collections.defaultdict(lambda: {"dispatches": 0, "ok": 0, "in": 0, "out": 0, "reasoning": 0, "no_usage": 0})
    for rid, r in receipts.items():
        b = by_class[cls[rid]]
        i, o, rs = tok(r)
        b["dispatches"] += 1
        b["ok"] += 1 if r.get("success") else 0
        b["in"] += i
        b["out"] += o
        b["reasoning"] += rs
        b["no_usage"] += 0 if r.get("usage") else 1

    revised_claims = {r.get("claim") for r in revisions}
    changing = [r for r in revisions if r.get("action_changed") is True]
    promoted = [v for v in verifier if v.get("promoted")]
    verified_pairs = {(c["claim_id"], tuple(c.get("evidence_refs") or ())) for c in ledger
                      if c.get("kind") == "VERIFIER" and c.get("epistemic_status") == "VERIFIED" and c.get("disposition") == "ACCEPTED"}
    claim_of_receipt = {c.get("receipt"): c["claim_id"] for c in ledger if c.get("receipt")}
    influencing = [rid for rid in receipts if cls[rid] in ("worker_proposal", "verifier_judgment") and claim_of_receipt.get(rid) in revised_claims]

    tree = []
    for d in decisions:
        cl = d["claim"]
        qs = [c for c in cherry if c["claim_id"] == cl]
        atoms = []
        for a in (d.get("atoms") or []):
            if isinstance(a, dict):
                aq = [c for c in cherry if c["claim_id"] == a.get("claim")]
                atoms.append({"value": a.get("value"), "status": a.get("status"), "questions": len(aq), "provider_calls": sum(c.get("provider_calls") or 0 for c in aq),
                              "attempt_errors": dict(collections.Counter(at.get("error_code") or "OK" for c in aq for at in (c.get("routing") or {}).get("attempts", [])))})
        rows = [c for c in ledger if c["claim_id"] == cl]
        tree.append({"action": d.get("action"), "claim": cl[-8:], "status": d.get("status"), "questions": len(qs),
                     "question_types": dict(collections.Counter(c["question_type"] for c in qs)),
                     "attempts": sum(len((c.get("routing") or {}).get("attempts", [])) for c in qs),
                     "attempt_errors": dict(collections.Counter(at.get("error_code") or "OK" for c in qs for at in (c.get("routing") or {}).get("attempts", []))),
                     "provider_calls_primary": d.get("provider_calls"), "ledger_rows": dict(collections.Counter(r["kind"] for r in rows)),
                     "atoms": atoms, "revision": next((r.get("trigger") + (":changed" if r.get("action_changed") else ":same") for r in revisions if r.get("claim") == cl), None)})

    total = sum(b["dispatches"] for b in by_class.values())
    org_spend = sum(by_class[k]["dispatches"] for k in by_class if k in ("worker_proposal", "verifier_judgment", "unreferenced_ok", "unreferenced_failed") or k == "agent_step:revise")
    sim = [r for r in jl(os.path.join(ep, "sim-usage.jsonl")) if "success" in r]
    return {
        "episode": ep, "provider_dispatches": total, "dispatches_ok": sum(b["ok"] for b in by_class.values()),
        "tokens": {"input": sum(b["in"] for b in by_class.values()), "output": sum(b["out"] for b in by_class.values()), "reasoning": sum(b["reasoning"] for b in by_class.values()),
                   "receipts_without_usage": sum(b["no_usage"] for b in by_class.values())},
        "unique_models_executed": len({r["model"] for r in receipts.values() if r.get("success")}), "unique_models_attempted": len({r["model"] for r in receipts.values()}),
        "providers_ok": dict(collections.Counter(r["provider"] for r in receipts.values() if r.get("success"))),
        "simulator": {"calls": len(sim), "calls_ok": sum(bool(r.get("success")) for r in sim), "tokens": sum((r.get("input_tokens") or 0) + (r.get("output_tokens") or 0) for r in sim)},
        "by_class": {k: dict(v) for k, v in sorted(by_class.items())},
        "decisions": len(decisions), "tree": tree,
        "verifier": {"judgments": len(verifier), "promoted_sources": len(promoted), "verified_pairs_in_ledger": len(verified_pairs),
                     "outcomes": dict(collections.Counter(v.get("reason") for v in verifier))},
        "revisions": {"total": len(revisions), "action_changed": len(changing), "triggers": dict(collections.Counter(r.get("trigger") for r in revisions))},
        "decision_influencing_org_receipts": len(influencing),
        "org_dispatches_not_influencing_any_decision": sum(1 for rid in receipts if cls[rid] in ("worker_proposal", "verifier_judgment", "unreferenced_ok", "unreferenced_failed")) - len(influencing),
        "marginal": {"org_dispatches_total": org_spend, "per_verified_pair": (org_spend / len(verified_pairs)) if verified_pairs else None,
                     "per_changing_revision": (org_spend / len(changing)) if changing else None},
        "organisational_events": {"escalations_to_engine": len(decisions), "claims_created": len(claims)},
    }


def render(a: dict) -> str:
    L = [f"# Cost audit — {a['episode']}", "",
         f"- provider dispatches (receipt rows): {a['provider_dispatches']} (successful {a['dispatches_ok']}); unique models executed {a['unique_models_executed']} (attempted {a['unique_models_attempted']})",
         f"- tokens (recorded): in {a['tokens']['input']}, out {a['tokens']['output']}, reasoning {a['tokens']['reasoning']}; receipts without usage: {a['tokens']['receipts_without_usage']}",
         f"- simulator: {a['simulator']['calls']} calls ({a['simulator']['calls_ok']} ok), {a['simulator']['tokens']} tokens", f"- successful dispatches by provider: {a['providers_ok']}", "",
         "## Receipts by class", "", "| class | dispatches | ok | in | out | reasoning |", "|---|---|---|---|---|---|"]
    for k, v in a["by_class"].items():
        L.append(f"| {k} | {v['dispatches']} | {v['ok']} | {v['in']} | {v['out']} | {v['reasoning']} |")
    L += ["", "## Execution tree (one row per organisational decision)", "", "| action | status | questions | attempts (errors) | ledger rows | atoms | revision |", "|---|---|---|---|---|---|---|"]
    for t in a["tree"]:
        L.append(f"| {t['action']} | {t['status']} | {t['questions']} {t['question_types']} | {t['attempts']} {t['attempt_errors']} | {t['ledger_rows']} | "
                 f"{[(x['value'], x['status'], x['questions'], x['provider_calls']) for x in t['atoms']]} | {t['revision']} |")
    L += ["", f"- verifier: {a['verifier']}", f"- revisions: {a['revisions']}", f"- organisational dispatches total {a['marginal']['org_dispatches_total']}; decision-influencing {a['decision_influencing_org_receipts']}; "
          f"not influencing any decision {a['org_dispatches_not_influencing_any_decision']}", f"- marginal: {a['marginal']}"]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("episode")
    ap.add_argument("state")
    ap.add_argument("--out")
    ap.add_argument("--md")
    args = ap.parse_args()
    a = audit(args.episode, args.state)
    if args.out:
        json.dump(a, open(args.out, "w"), indent=2, default=str)
    md = render(a)
    if args.md:
        open(args.md, "w").write(md)
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
