#!/usr/bin/env python3
"""Descriptive per-block results of the COLLAB-1 campaign from the on-disk records (no inference, no exclusion): official reward, status, guard-counted requests/tokens, minutes, and the
ORGANISATIONAL ACTIVATION actually observed (reviews run, consequential reviews, revisions that changed the action) so that episodes in which the mechanism had no opportunity are visible.
usage: results_table.py [RUNS_DIR]   (host python, no other dependencies)"""
import collections
import glob
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1/runs")
C = R / "collab1"
spec = importlib.util.spec_from_file_location("g", HERE.parent / "ogi013-pilot/pilot_guard.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
budget = json.loads((HERE / "collab1_budget.json").read_text())
CONDS = ("SINGLE", "SINGLE-E", "COLLAB")


def episode(task_dir: str, cond: str) -> dict | None:
    rec = C / task_dir / f"{cond}.episode.json"
    if not rec.is_file():
        return None
    e = json.loads(rec.read_text())
    out = {"status": e["status"], "min": round(((e.get("ended_at") or e["started_at"]) - e["started_at"]) / 60, 1), "reward": None, "req": None, "tok": None, "reviews": 0, "consequential": 0, "changed": 0, "writes": 0}
    off = glob.glob(str(C / task_dir / cond / "tasks/*/official-result.json"))
    if off:
        out["reward"] = json.loads(Path(off[0]).read_text())["reward_info"]["reward"]
    u = g.usage(str(R), [f"collab1/{task_dir}/{cond}"], budget["reserve_tokens_per_dispatch"])
    out["req"], out["tok"] = u["dispatches"], u["tokens"]
    ev = glob.glob(str(C / task_dir / cond / "tasks/*/fruitstack-events.jsonl"))
    if ev:
        for x in map(json.loads, Path(ev[0]).read_text().splitlines()):
            if x["event"] == "ORG_COLLAB":
                out["reviews"] += 1
                out["consequential"] += x.get("action_kind") in ("WRITE", "TRANSFER")
                out["changed"] += bool(x.get("changed"))
            elif x["event"] == "STEP" and x.get("tag") == "draft" and False:
                pass
    return out


rows = {}
for d in sorted(p.name for p in C.iterdir() if p.is_dir() and "_" in p.name and p.name not in ("discarded",)):
    r = {c: episode(d, c) for c in CONDS}
    if any(r.values()):
        rows[d.replace("_", ":", 1)] = r
fmt = lambda e: "-" if e is None else f"{e['status'][:6]}|rw={e['reward']}|{e['req']}rq|{e['tok']}t|{e['min']}m|rev={e['reviews']}/{e['consequential']}c/{e['changed']}ch"
print(f"{'task':12s} " + " ".join(f"{c:42s}" for c in CONDS))
for t, r in rows.items():
    print(f"{t:12s} " + " ".join(f"{fmt(r[c]):42s}" for c in CONDS))
done = collections.Counter()
for r in rows.values():
    for c in CONDS:
        e = r[c]
        if e and e["reward"] is not None:
            done[c, "graded"] += 1
            done[c, "success"] += e["reward"] >= 1.0
        elif e and e["status"] in ("BUDGET_STOP", "TIMEOUT"):
            done[c, "stopped"] += 1
print("\nPER CONDITION (all blocks on disk; graded = official result exists; BUDGET_STOP/TIMEOUT are scored non-success under the registered rule):")
for c in CONDS:
    print(f"  {c:9s} graded={done[c,'graded']} success={done[c,'success']} stopped={done[c,'stopped']}")
