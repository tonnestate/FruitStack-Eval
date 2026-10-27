"""Per-arm termination/cause table from immutable c1 run dirs (read-only)."""
import json, sys, glob, os, collections
base = sys.argv[1]
rows = []
for d in sorted(glob.glob(f"{base}/*-fixed") + glob.glob(f"{base}/*-adaptive")):
    t, mode = os.path.basename(d).rsplit("-", 1)
    try: off = json.load(open(f"{d}/tasks/{t}/official-result.json"))
    except Exception: rows.append(dict(task=t, mode=mode, err="no_official_result")); continue
    ev = [json.loads(l) for l in open(f"{d}/tasks/{t}/fruitstack-events.jsonl") if l.strip().startswith("{")]
    c = collections.Counter(e["event"] for e in ev)
    closed = next((e for e in ev if e["event"] == "EPISODE_CLOSED"), {})
    ass = [e for e in ev if e["event"] == "ASSURANCE"]
    st = closed.get("stats", {})
    msgs = off.get("messages", [])
    rows.append(dict(task=t, mode=mode, reward=off["reward_info"].get("reward"), term=off.get("termination_reason"),
        closed=closed.get("reason"), last_health=ass[-1]["health"] if ass else None,
        health_seq="".join(a["health"][0] for a in ass), steps=st.get("steps"), retries=st.get("step_retries"),
        esc=st.get("escalations"), chal=st.get("challenges_found"), rev=st.get("revisions"), reflex=st.get("reflex_blocks"),
        unk=st.get("unknown_steps"), refused=c["STEP_REFUSED"], abandoned=c["STEP_ABANDONED"], tool_err=c["POMELO_TOOL_ERROR"],
        contrib=len(closed.get("contributions") or []), n_msgs=len(msgs), models=st.get("models")))
json.dump(rows, open(sys.argv[2], "w"), indent=1)
for r in rows: print({k: r.get(k) for k in ("task","mode","reward","term","closed","health_seq","steps","esc","chal","rev","contrib","refused","tool_err","n_msgs")})
