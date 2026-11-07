#!/usr/bin/env python3
"""Deterministic task selection and allocation for the prospective COLLAB study (COLLAB_STUDY_DESIGN.md). No outcome of any earlier run is read: only the official tau2 split files and the reference actions
of each task. usage: make_study_manifest.py TAU2_DATA_DIR > study_manifest.json"""
import hashlib
import json
import sys
from pathlib import Path

SEED = 4242
AIRLINE_WRITES = {"book_reservation", "cancel_reservation", "update_reservation_flights", "update_reservation_passengers", "update_reservation_baggages", "send_certificate"}
RETAIL_WRITES = {"cancel_pending_order", "exchange_delivered_order_items", "modify_pending_order_address", "modify_pending_order_items", "modify_pending_order_payment", "modify_user_address",
                 "return_delivered_order_items"}
RETAIL_WRITE_SAMPLE, AIRLINE_NOWRITE_SAMPLE = 27, 8


def rank(domain: str, tid) -> str:
    return hashlib.sha256(f"{SEED}|{domain}|{tid}".encode()).hexdigest()


def load(data: Path, domain: str):
    split = json.loads((data / "domains" / domain / "split_tasks.json").read_text())
    tasks = {str(t["id"]): t for t in json.loads((data / "domains" / domain / "tasks.json").read_text())}
    return split, tasks


def writes(task, names) -> int:
    return sum(1 for a in (task.get("evaluation_criteria") or {}).get("actions") or [] if a["name"] in names)


def build(data: Path) -> dict:
    a_split, a_tasks = load(data, "airline")
    r_split, r_tasks = load(data, "retail")
    a_train = [str(i) for i in a_split["train"]]
    r_train = [str(i) for i in r_split["train"]]
    airline_write = sorted((i for i in a_train if writes(a_tasks[i], AIRLINE_WRITES) > 0), key=int)                      # ALL of them: no sampling
    retail_write = sorted(sorted((i for i in r_train if writes(r_tasks[i], RETAIL_WRITES) > 0), key=lambda i: rank("retail", i))[:RETAIL_WRITE_SAMPLE], key=int)
    airline_none = sorted(sorted((i for i in a_train if writes(a_tasks[i], AIRLINE_WRITES) == 0), key=lambda i: rank("airline", i))[:AIRLINE_NOWRITE_SAMPLE], key=int)
    rows = []
    for stratum, domain, ids in (("write-opportunity", "airline", airline_write), ("write-opportunity", "retail", retail_write), ("no-write-control", "airline", airline_none)):
        for i in ids:
            first = "SINGLE" if int(rank(domain, i)[0], 16) % 2 == 0 else "COLLAB"                                       # arm order by hash parity, not always SINGLE first
            rows.append({"stratum": stratum, "domain": domain, "task_id": i, "task_ref": f"{domain}:{i}", "first_arm": first, "expected_write_actions": writes((a_tasks if domain == "airline" else r_tasks)[i],
                                                                                                                                                           AIRLINE_WRITES if domain == "airline" else RETAIL_WRITES)})
    return {"study": "OGI-013-COLLAB-1", "seed": SEED, "selection_rule": "airline train split: ALL tasks with >=1 expected write action; retail train split: the first 27 write tasks by sha256('4242|retail|id'); "
            "airline train split: the first 8 zero-write tasks by sha256('4242|airline|id') as the no-write control stratum. Test-split tasks (C1/C2/C3, pilots) are excluded by construction.",
            "n_tasks": len(rows), "n_write_opportunity": sum(r["stratum"] == "write-opportunity" for r in rows), "conditions": ["SINGLE", "COLLAB", "SINGLE-E"], "tasks": rows}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(build(Path(sys.argv[1])), indent=1))
