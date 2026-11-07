#!/usr/bin/env python3
"""VALIDATION-1 task selection (OGI-013, prospective, written BEFORE any validation episode). Outcome-independent: uses only the frozen tau2 task definitions and the frozen COLLAB-1 manifest.
Pool: the 19 registered mechanism-sensitive tasks (>= 2 reference WRITE actions). Score = 2 x distinct reference write-tool types + number of reference write actions + number of
policy-conditional / pressure markers in the simulated user's instructions (conditionals on a policy outcome, refusal handling, insistence, change of mind). Ties and ordering: sha256 of
"OGI013-VALIDATION-1|<ref>". The top 3 are the cohort. Nothing about any episode result is read."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench/data/tau2/domains")
WRITES = {"book_reservation", "cancel_reservation", "update_reservation_flights", "update_reservation_baggages", "update_reservation_passengers", "send_certificate", "transfer_to_human_agents",
          "cancel_pending_order", "exchange_delivered_order_items", "modify_pending_order_address", "modify_pending_order_items", "modify_pending_order_payment", "modify_user_address", "return_delivered_order_items"}
MARK = re.compile(r"\bif\b[^.]*\b(not possible|can't|cannot|unable|refus|declin|deny|denies|basic economy|not allowed|doesn't|does not|isn't|is not)\b|otherwise|insist|persistent|change your mind|instead|unless|don't want|do not want|refuse", re.I)


def main() -> None:
    manifest = json.loads((HERE.parent / "ogi013-collab1/study_manifest_v2.json").read_text())
    pool = [t for t in manifest["tasks"] if t["expected_write_actions"] >= 2]
    rows = []
    for t in pool:
        tasks = {str(x["id"]): x for x in json.loads((DATA / t["domain"] / "tasks.json").read_text())}
        x = tasks[str(t["task_id"])]
        acts = [a["name"] for a in x["evaluation_criteria"].get("actions") or []]
        writes = [a for a in acts if a in WRITES]
        instr = json.dumps(x["user_scenario"]["instructions"])
        score = 2 * len(set(writes)) + len(writes) + len(MARK.findall(instr))
        rows.append({"task_ref": t["task_ref"], "domain": t["domain"], "task_id": t["task_id"], "write_actions": writes, "distinct_write_tools": len(set(writes)), "markers": len(MARK.findall(instr)),
                     "score": score, "tiebreak": hashlib.sha256(("OGI013-VALIDATION-1|" + t["task_ref"]).encode()).hexdigest()})
    rows.sort(key=lambda r: (-r["score"], r["tiebreak"]))
    cohort = [r["task_ref"] for r in rows[:3]]
    out = {"study": "OGI-013-VALIDATION-1", "rule": __doc__.strip().splitlines()[0], "pool_size": len(pool), "ranking": rows, "cohort": cohort}
    (HERE / "cohort.json").write_text(json.dumps(out, indent=1))
    for r in rows[:8]:
        print(r["task_ref"], r["score"], r["write_actions"], r["markers"])
    print("COHORT", cohort)


if __name__ == "__main__":
    main()
