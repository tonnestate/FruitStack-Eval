#!/usr/bin/env python3
"""COLLAB-1 manifest v2 (AMENDMENT-1): the v1 task selection unchanged, plus a per-block condition ORDER assigned by cycling the six permutations of the three conditions over the tasks ranked by the seeded hash (balanced: each condition is first and last equally often, +-1), so SINGLE-E is not systematically last, and the SINGLE-E effort constants fixed from calibration data (CALIBRATION.md) before any COLLAB-1 episode.
usage: make_manifest_v2.py TAU2_DATA_DIR > study_manifest_v2.json"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ogi013-phase2"))
import make_study_manifest as v1  # noqa: E402

CONDITIONS = ["SINGLE", "COLLAB", "SINGLE-E"]
SINGLE_E_K = 3
SINGLE_E_SCOPE = "writes"


def build(data: Path) -> dict:
    m = v1.build(data)
    perms = list(itertools.permutations(CONDITIONS))                                                          # the 6 orders: balanced, so no condition is systematically first or last
    ranked = sorted(m["tasks"], key=lambda t: v1.rank(t["domain"], t["task_id"]))                              # by the seeded hash, not by anything about the task
    for i, t in enumerate(ranked):
        t["order"] = list(perms[i % len(perms)])
    for t in m["tasks"]:
        t.pop("first_arm", None)
    m.update({"study": "OGI-013-COLLAB-1", "version": 2, "amends": "evidence/ogi013-phase2/study_manifest.json (v1, unchanged)", "single_e": {"k": SINGLE_E_K, "scope": SINGLE_E_SCOPE},
              "conditions": CONDITIONS})
    return m


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    print(json.dumps(build(Path(sys.argv[1])), indent=1))
