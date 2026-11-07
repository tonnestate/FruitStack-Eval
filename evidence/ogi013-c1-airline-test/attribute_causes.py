"""Merge failure_table.json + replay_assurance.json into a per-arm primary-cause attribution (rules are explicit, no model judgement)."""
import json, sys, collections, glob, os
base = sys.argv[1]
ft = {(r["task"], r["mode"]): r for r in json.load(open("failure_table.json"))}
rp = {(r["task"], r["mode"]): r for r in json.load(open("replay_assurance.json"))}
APOL = "I'm sorry, I could not complete that step"
rows = []
for (t, m), r in sorted(ft.items(), key=lambda kv: (int(kv[0][0]), kv[0][1])):
    off = json.load(open(f"{base}/{t}-{m}/tasks/{t}/official-result.json"))
    ev = [json.loads(l) for l in open(f"{base}/{t}-{m}/tasks/{t}/fruitstack-events.jsonl") if l.strip().startswith("{")]
    apol = sum(1 for x in off["messages"] if x["role"] == "assistant" and APOL in str(x.get("content")))
    nva = sum(1 for e in ev if e["event"] == "NO_VALID_ACTION")
    real_tool_err = sum(1 for x in off["messages"] if x["role"] == "tool" and x.get("error") and "REFLEX_BLOCKED" not in str(x.get("content")))
    p = rp[(t, m)]; first = p["as_run_first_unhealthy"]; g = p["grounded_first_unhealthy"]
    if r["reward"] == 1.0: cause = "SUCCESS"
    elif r["closed"] != "REFLEX_BLOCKED": cause = "TASK_FAILED_UNBLOCKED(model/policy)"
    else:
        turns_pre = first  # assistant turns up to and including the one AppleMe flagged
        # how much of the pre-block conversation was route-failure fallback?
        if apol >= 2 and apol >= turns_pre // 2: cause = "ROUTE_OUTPUT_UNUSABLE->reflex"
        elif g is None or g > first: cause = "SENSOR_STARVED_FALSE_LOOP->reflex"
        else: cause = "REFLEX_OTHER(sensor still fires with grounded events)"
    rows.append(dict(task=t, mode=m, reward=r["reward"], cause=cause, first_unhealthy_turn=first, grounded_first_unhealthy=g, apology_turns=apol, no_valid_action=nva,
                     step_refused=r["refused"], real_tool_errors=real_tool_err, escalations=r["esc"], contributions=r["contrib"]))
json.dump(rows, open("cause_attribution.json", "w"), indent=1)
c = collections.Counter((x["mode"], x["cause"]) for x in rows); print(sorted(c.items()))
by = collections.defaultdict(dict)
for x in rows: by[x["task"]][x["mode"]] = x["cause"]
print("common failures:", [t for t, d in by.items() if all(v != "SUCCESS" for v in d.values())].__len__())
for t, d in sorted(by.items(), key=lambda kv: int(kv[0])): print(t, "F:", d["fixed"], "| A:", d["adaptive"])
