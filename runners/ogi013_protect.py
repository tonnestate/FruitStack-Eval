"""Repair order 1 section R6 measures, fixed before any new run. Hidden grades (grades.json from ogi013_grade_snapshots.py) are used HERE only, outside every agent loop.
  M-protect  every proposed revision (adopted or rolled back) is graded; prevented regression = rolled back AND graded lower than the incumbent; unprotected regression = adopted AND graded lower.
             Counts as organisational value only relative to arm N on the same task.
  M-confirm  a grounded independent approval (an EXCELLENT vote citing the candidate's sha256) of a candidate that grades resolved.
  M-cost     tokens and wall time per arm and per resolved task.
usage: ogi013_protect.py RUN_DIR [RUN_DIR ...] > M_PROTECT.md        (a run dir holds run.json, grades.json, snapshots/)"""
import json
import sys
from pathlib import Path


def key(g: dict) -> tuple:
    return (bool(g.get("resolved")), g.get("f2p_passed", 0), g.get("p2p_passed", 0))


def lower(a: dict, b: dict) -> bool:
    return (a.get("f2p_passed", 0), a.get("p2p_passed", 0)) < (b.get("f2p_passed", 0), b.get("p2p_passed", 0)) and a.get("f2p_passed", 0) <= b.get("f2p_passed", 0)


def measure(run: Path) -> dict:
    r = json.loads((run / "run.json").read_text())
    grades = json.loads((run / "grades.json").read_text()) if (run / "grades.json").exists() else {}
    prevented, unprotected, rows = 0, 0, []
    if r.get("candidates"):                                              # arm T: the candidate ledger
        last_adopted: dict = {}
        for c in r["candidates"]:
            fname = f"{c['id'].replace(':', '_')}{'_REJECTED' if c['status'] == 'REJECTED_REVISION' else ''}.diff"
            g = grades.get(fname)
            inc = last_adopted.get(c["pos"])
            if c["label"] != "first" and g is not None and inc is not None:
                if lower(g, inc[1]):
                    if c["status"] == "REJECTED_REVISION":
                        prevented += 1
                    else:
                        unprotected += 1
                rows.append({"candidate": c["id"], "status": c["status"], "reason": c.get("reason"), "vs_incumbent": inc[0], "grade": f"{g['f2p_passed']}/{g['f2p_total']}", "lower": lower(g, inc[1])})
            if c["status"] in ("ADOPTED", "SUPERSEDED") and g is not None:
                last_adopted[c["pos"]] = (c["id"], g)
    else:                                                                # arm N / S: last patch wins, every revision is adopted
        prev = None
        for name in sorted(grades):
            if name == "RELEASED.diff":
                continue
            g = grades[name]
            if "_rev" in name and prev is not None and lower(g, prev[1]):
                unprotected += 1
                rows.append({"candidate": name, "status": "ADOPTED_LAST_WINS", "vs_incumbent": prev[0], "grade": f"{g['f2p_passed']}/{g['f2p_total']}", "lower": True})
            prev = (name, g)
    confirm = []
    for v in (r.get("release") or {}).get("votes", []):
        if v.get("counts") == "EXCELLENT" and v.get("verdict") == "EXCELLENT":
            confirm.append(v.get("pos"))
    resolved = bool(grades.get("RELEASED.diff", {}).get("resolved"))
    tokens = (r.get("stats") or {}).get("tokens_in", 0) + (r.get("stats") or {}).get("tokens_out", 0)
    return {"run": run.parent.name + "/" + run.name if run.name == "run" else run.name, "status": r["status"], "prevented_regressions": prevented, "unprotected_regressions": unprotected, "revisions_graded": rows,
            "approvals_excellent": len(confirm), "resolved": resolved, "tokens": tokens, "seconds": r.get("seconds")}


if __name__ == "__main__":
    out = [measure(Path(a)) for a in sys.argv[1:]]
    print("# M-protect / M-confirm / M-cost\n\n| run | status | prevented regressions | unprotected regressions | EXCELLENT approvals | resolved | tokens | wall s |\n|---|---|---|---|---|---|---|---|")
    for m in out:
        print(f"| {m['run']} | {m['status']} | {m['prevented_regressions']} | {m['unprotected_regressions']} | {m['approvals_excellent']} | {m['resolved']} | {m['tokens']} | {m['seconds']} |")
    print("\n```json\n" + json.dumps(out, indent=1) + "\n```")
