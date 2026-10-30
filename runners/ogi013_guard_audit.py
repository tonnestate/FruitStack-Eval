"""GUARD_AUDIT (Addendum 5 C): per session progress credits vs hidden-test improvements of snapshots, wasted tail, per-episode trajectory.
usage: ogi013_guard_audit.py RUN_DIR [RUN_DIR ...]  (needs grades.json from ogi013_grade_snapshots.py; hidden tests are used here only, outside every agent loop)"""
import json
import sys
from pathlib import Path


def audit(run: Path, base: dict):
    ev = [json.loads(l) for l in (run / "fruitstack-events.jsonl").read_text().splitlines() if l.startswith("{")]
    grades = json.loads((run / "grades.json").read_text())
    best = (base["f2p_passed"], base["p2p_passed"])
    traj, improved_idx = [], {}
    for i, e in enumerate(ev):
        if e["event"] != "SNAPSHOT":
            continue
        g = grades.get(f"{e['pos']}_{e['label']}.diff")
        if not g:
            continue
        cur = (g["f2p_passed"], g["p2p_passed"])
        better = cur[0] >= best[0] and cur[1] >= best[1] and cur != best
        traj.append({"i": i, "snapshot": f"{e['pos']}_{e['label']}", "f2p": cur[0], "p2p": cur[1], "improved": better})
        if better:
            improved_idx[i] = cur
            best = cur
    last_imp = max(improved_idx, default=-1)
    toks = lambda e: (e.get("tokens_in") or 0) + (e.get("tokens_out") or 0)
    total = sum(toks(e) for e in ev if e["event"] == "STEP")
    tail = sum(toks(e) for i, e in enumerate(ev) if e["event"] == "STEP" and i > last_imp)
    stack, sessions = [], []
    for i, e in enumerate(ev):
        if e["event"] == "SESSION_START":
            stack.append({"role": e["role"], "tokens": 0, "start": i, "steps": []})
        elif e["event"] == "STEP" and stack:
            stack[-1]["tokens"] += toks(e)
            stack[-1]["steps"].append(i)
        elif e["event"] == "SESSION_END" and stack:
            s = stack.pop()
            s.update(end=i, turns=e["turns"], progress_turns=e["progress_turns"], stop=e["stop"])
            nxt = next((j for j in range(i + 1, len(ev)) if ev[j]["event"] in ("SNAPSHOT", "SESSION_START")), None)
            s["snapshot_improved"] = bool(nxt is not None and ev[nxt]["event"] == "SNAPSHOT" and nxt in improved_idx)
            s["tokens_after_last_improvement"] = sum(toks(ev[j]) for j in s["steps"] if j > last_imp)
            sessions.append(s)
    return {"run": run.name, "total_tokens": total, "wasted_tail_tokens": tail, "wasted_tail_share": round(tail / total, 3) if total else None,
            "baseline": base, "trajectory": traj, "sessions": sessions}


if __name__ == "__main__":
    base = json.loads((Path(__import__("os").environ["TASK_DIR"]) / "base_grade.json").read_text())
    res = [audit(Path(a), base) for a in sys.argv[1:]]
    T, W = sum(r["total_tokens"] for r in res), sum(r["wasted_tail_tokens"] for r in res)
    out = ["# GUARD_AUDIT", f"Episodes: {len(res)}; total tokens {T}; wasted tail {W} = {round(W / T, 3) if T else None} (criterion <= 0.40, pre-registered)", ""]
    for r in res:
        out += [f"## {r['run']}", f"tokens {r['total_tokens']}, wasted tail {r['wasted_tail_tokens']} ({r['wasted_tail_share']}); baseline F2P/P2P {r['baseline']['f2p_passed']}/{r['baseline']['p2p_passed']}",
                "", "| snapshot | F2P | P2P | improved |", "|---|---|---|---|"]
        out += [f"| {t['snapshot']} | {t['f2p']} | {t['p2p']} | {t['improved']} |" for t in r["trajectory"]]
        out += ["", "| session | role | turns | progress turns | tokens | tokens after last improvement | snapshot improved | stop |", "|---|---|---|---|---|---|---|---|"]
        out += [f"| {k} | {s['role']} | {s['turns']} | {s['progress_turns']} | {s['tokens']} | {s['tokens_after_last_improvement']} | {s['snapshot_improved']} | {s['stop']} |" for k, s in enumerate(r["sessions"])]
        out.append("")
    print("\n".join(out))
