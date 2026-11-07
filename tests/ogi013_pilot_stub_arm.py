#!/usr/bin/env python3
"""Stand-in for run_arm.sh in the launcher tests (stdlib only; no model, no tau2). usage: ogi013_pilot_stub_arm.py SCENARIO ARGS... as run_pilot.sh passes them to run_arm.sh.
It writes what a real arm writes (receipts, sim-usage, official result, events) so the launcher, the guard and the report are tested together."""
import json
import os
import sys
import time
from pathlib import Path

scenario, args = os.environ["STUB_SCENARIO"], sys.argv[1:]
base = Path(os.environ["PILOT_BASE"]) / "runs"
count = base / "stub-launches.txt"
if args and args[0] == "--verify-components":
    sys.exit(1 if scenario == "components_fail" else 0)
if args and args[0] == "--contract":
    sys.exit(1 if scenario == "contract_fail" else 0)
if args and args[0] == "--preflight":
    sys.exit(1 if scenario == "preflight_fail" else (Path(args[2]).mkdir(parents=True, exist_ok=True) or print(json.dumps({"executable": True})) or 0))
out, task, domain, mode, route, slot = args
with count.open("a") as f:
    f.write(f"{out} {mode}\n")
arm = out.split("/")[-1]
d = base / out
(d / "fruitstack/plumme-state").mkdir(parents=True)
(d / "tasks/24").mkdir(parents=True)
json.dump({k: os.environ.get(k) for k in ("OGI013_PILOT_ARM", "OGI013_ORG_COLLAB", "OGI013_ORG_POLICY_MODE", "OGI013_ORG_STATE_DIR", "PILOT_SESSION_MAX_CALLS", "PILOT_SESSION_MAX_TOKENS",
                                           "PILOT_SESSION_MAX_COST_USD", "OGI013_PILOT_BUDGET", "OGI013_PILOT_ARMS", "OGI013_PILOT_RUNS", "OGI013_PILOT_START")} | {"args": args}, (d / "stub-env.json").open("w"))
print("OGI013_SOURCE plumme=abc123", flush=True)


def receipt(i, ok=True, cls="FREE_TIER", lineage="L-a"):
    return {"receipt_id": f"{arm}-{i}", "success": ok, "cost_class": cls, "independence_key": lineage, "model": "m", "provider": "p", "failure_class": None if ok else "RATE_LIMITED",
            "usage": {"input_tokens": 500, "output_tokens": 50, "cost_usd": None} if ok else None}


n = 400 if scenario == "over_budget" and arm == "single" else 6
rows = [receipt(i, lineage="L-a" if i % 2 else "L-b") for i in range(n)]
(d / "fruitstack/plumme-state/receipts.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
(d / "sim-usage.jsonl").write_text("".join(json.dumps({"receipt_id": rows[i]["receipt_id"], "success": True, "model_key": "gemini-3.1-flash-lite@vision"}) + "\n" for i in (1, 3)))
if scenario in ("hang", "over_budget") and (arm == "single"):
    time.sleep(60)                                                           # a running arm: the guard / a signal must stop it
if scenario == "arm_fail":
    sys.exit(7)
reward = 1.0 if arm == "collab" else 0.0
(d / "tasks/24/official-result.json").write_text(json.dumps({
    "task_id": "24", "seed": 42, "policy": "POLICY TEXT", "duration": 12.5, "start_time": "t0", "end_time": "t1", "termination_reason": "user_stop",
    "reward_info": {"reward": reward, "action_checks": [{"action": {"name": "book_reservation"}, "action_match": reward == 1.0}]},
    "messages": [{"role": "assistant", "content": "", "tool_calls": [{"name": "book_reservation", "arguments": {"x": 1}}]}, {"role": "assistant", "content": "Done."}]}))
ev = [{"event": "EPISODE_OPENED"}]
if arm == "collab":
    ev += [{"event": "ORG_COLLAB", "purpose": "consequential_effect", "action": "book_reservation", "draft": "d1", "final": "d2", "changed": True, "improved": True, "validated": False, "ungrounded_agreement": False,
            "final_reviewed": True, "independent_review": True, "review_unavailable": False, "specialist": False, "calls": 3, "stop": "NO_ISSUES", "unresolved": [], "overruled": [],
            "agreement": [{"model": "m2", "lineage": "L-b", "agreed_with": "d2", "grounds": "checked policy", "grounds_stated": True}], "attribution": [],
            "trail": [{"stage": "SOLUTION", "model": "m", "lineage": "L-a", "status": "UNVERIFIED", "text": "draft"}, {"stage": "CRITIQUE", "model": "m2", "lineage": "L-b", "status": "DISSENT", "text": "wrong id"},
                      {"stage": "REVISION", "model": "m", "lineage": "L-a", "status": "UNVERIFIED", "text": "fixed"}], "failures": []},
           {"event": "ORG_REVISION", "action_changed": True}]
(d / "tasks/24/fruitstack-events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in ev))
