"""Offline counterfactual: feed the recorded c1 transcripts to AppleMe with (a) the events the runner actually sent and (b) events that
also carry environment-observed information gain. No model calls. Reports the turn at which health first leaves HEALTHY."""
import json, sys, glob, os, hashlib, tempfile
from cherryme.appleme_bridge import connect_appleme
from cherryme.models import Claim
base = sys.argv[1]
def run(msgs, grounded):
    ws = tempfile.mkdtemp(prefix="replay-")
    ap = connect_appleme(workspace_root=ws)
    claim = Claim(text="Resolve the customer's request in tau2 airline task within the policy.")
    sig = ap.start_run(claims=[claim], frame={"appleme": {"root_goal": claim.text, "definition_of_done": "resolved or transferred, no repeated failing action.", "policy": {"no_progress_heartbeat_threshold": 8}}}, budget=1, call_budget=None)
    rid, seen, verified, last_err, first_bad, health = sig.target_run_id, set(), 0, None, None, []
    turn = 0
    for i, m in enumerate(msgs):
        if m["role"] == "tool":
            if m.get("error"): last_err = hashlib.sha256(str(m.get("content"))[:200].encode()).hexdigest()[:12]
            else:
                h = hashlib.sha256(str(m.get("content")).encode()).hexdigest()
                if h not in seen: seen.add(h); verified += 1
            continue
        if m["role"] != "assistant" or i == 0: continue
        turn += 1
        tools = m.get("tool_calls") or []
        name = tools[0]["name"] if tools else None
        outcome = "COUNTED_FAILURE" if last_err and tools else "PROGRESS"
        ev = {"question_type": ("ACT" if tools else "SAY"), "question_outcome": outcome, "mutation_error": {"code": last_err} if outcome == "COUNTED_FAILURE" else {}}
        if grounded:
            ev["question_type"] = f"ACT:{name}" if tools else "SAY"; ev["verified_evidence_total"] = verified
        s = ap.observe_event(target_run_id=rid, event=ev, claim=claim); last_err = None
        health.append(s.health_state[0])
        if first_bad is None and s.health_state != "HEALTHY": first_bad = turn
    return first_bad, "".join(health)
out = []
for d in sorted(glob.glob(f"{base}/*-fixed") + glob.glob(f"{base}/*-adaptive")):
    t, mode = os.path.basename(d).rsplit("-", 1)
    off = json.load(open(f"{d}/tasks/{t}/official-result.json"))
    a, b = run(off["messages"], False), run(off["messages"], True)
    out.append(dict(task=t, mode=mode, reward=off["reward_info"].get("reward"), as_run_first_unhealthy=a[0], as_run=a[1], grounded_first_unhealthy=b[0], grounded=b[1]))
    print(out[-1])
json.dump(out, open(sys.argv[2], "w"), indent=1)
