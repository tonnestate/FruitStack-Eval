"""Repair order 1, R7 replay acceptance (no model calls): the stored micro-pilot T records are replayed through the NEW logic (candidate ledger with driver-run visible checks, grounded-critique rule).
Hidden grades are read only to state the result; they never influence the replay. usage: ogi013_replay.py TASK_ID  (task dir /root/fruits/research/OGI013-MICRO/<TASK_ID>, records in evidence/ogi013-micro/runs/<TASK_ID>/T)"""
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ogi013_candidates as oc  # noqa: E402

MICRO = Path("/root/fruits/research/OGI013-MICRO")
EVID = HERE.parent / "evidence/ogi013-micro/runs"


def stored_objections(team_state: str) -> dict:
    out = {}
    for m in re.finditer(r"^- (O\d+) on (\S+) from (\S+) \[([^\]]*)\]: (.*?)(?=^- O\d+ on |^DECISIONS:|\Z)", team_state, re.M | re.S):
        out[m.group(1)] = {"id": m.group(1), "target": m.group(2), "lineage": m.group(3), "flags": m.group(4), "text": m.group(5).strip()}
    return out


def replay(task_id: str) -> dict:
    task_dir, rec = MICRO / task_id, EVID / task_id / "T"
    task = json.loads((task_dir / "agent_task.json").read_text())["problem_statement"]
    python = str(task_dir / "venv38/bin/python")
    events = [json.loads(l) for l in (rec / "fruitstack-events.jsonl").read_text().splitlines() if l.startswith("{")]
    objs = stored_objections((rec / "team_state.md").read_text())
    ground = {oid: oc.classify_objection(o["text"], task, []) for oid, o in objs.items()}      # the stored records carry no check logs: only a verbatim task quote can ground
    grounded = {oid for oid, g in ground.items() if oc.is_grounded(g)}
    labels = oc.visible_labels(task_dir / "base")

    def checker(diff, repros):
        with tempfile.TemporaryDirectory() as tmp:
            tree = oc.tree_with_diff(task_dir / "base", diff, Path(tmp) / "t")
            return {**oc.run_visible(python, tree, labels), "repro": {}}
    led = oc.CandidateLedger(checker)
    decisions = []
    for e in events:
        if e["event"] == "SNAPSHOT":
            pos, label = e["pos"], e["label"]
            diff = (rec / "snapshots" / f"{pos}_{label}.diff").read_text()
            if label == "first":
                led.add(pos, label, diff)
                decisions.append((f"{pos}_{label}", "ADOPTED", "FIRST_CANDIDATE"))
        elif e["event"] == "REVISION":
            claimed = [o for o in e["responding_to"] if o in grounded]
            diff = (rec / "snapshots" / f"{e['pos']}_rev{e['rev']}.diff").read_text()
            d = led.consider_revision(e["pos"], f"rev{e['rev']}", diff, claimed)
            decisions.append((f"{e['pos']}_rev{e['rev']}", "ADOPTED" if d["adopted"] else "REJECTED_REVISION", d["reason"], {"responding_to": e["responding_to"], "grounded_claimed": claimed}))
    best = led.best()
    grades = json.loads((rec / "grades.json").read_text())
    return {"task": task_id, "grounded_objections": sorted(grounded), "ungrounded_or_suggestion": sorted(set(objs) - grounded), "decisions": decisions,
            "selected_output": best["id"] if best else None, "selected_hidden_grade": grades.get(f"{best['pos']}_{best['label']}.diff") if best else None,
            "pilot_released": "RELEASED.diff graded " + json.dumps({k: grades["RELEASED.diff"][k] for k in ("f2p_passed", "f2p_total")})}


if __name__ == "__main__":
    print(json.dumps(replay(sys.argv[1]), indent=1, default=str))
