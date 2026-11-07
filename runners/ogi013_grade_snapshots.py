"""Grade every snapshot diff of a team run (Addendum 3 B.5) with evaluate_v2.py v2.1: applies each diff to a fresh base copy, grades, writes grades.json.
usage: ogi013_grade_snapshots.py RUN_DIR   (evaluate_v2.py is bound to the task.json beside it; hidden tests are used here only, outside every agent loop)"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import os
TASK = Path(os.environ.get("TASK_DIR", "/root/fruits/research/OGI013-SINGLE-TASK"))   # development task: TASK_DIR=/root/fruits/research/OGI013-DEV (verbatim evaluate_v2.py copy + FSE_BASE_TREE=<dir>/base)
run = Path(sys.argv[1])
out = {}
base_cache = TASK / "base_grade.json"                       # the unmodified base, graded once: the baseline of every audit
diffs = sorted((run / "snapshots").glob("*.diff"))
for diff in ([] if base_cache.exists() else [Path("/dev/null")]) + diffs:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        shutil.copytree(TASK / "base", ws)
        if str(diff) != "/dev/null" and diff.stat().st_size:
            subprocess.run(["git", "apply", "--whitespace=nowarn", str(diff.resolve())], cwd=ws, check=True)
        res = Path(tmp) / "g.json"
        subprocess.run([str(TASK / "venv38/bin/python"), str(TASK / "evaluate_v2.py"), str(ws), str(res)], capture_output=True, text=True, timeout=2400)
        g = json.loads(res.read_text())
    rec = {k: g.get(k) for k in ("resolved", "f2p_passed", "f2p_total", "p2p_passed", "p2p_total", "runner_exit", "error")}
    if str(diff) == "/dev/null":
        base_cache.write_text(json.dumps(rec))
        continue
    out[diff.name] = rec
    print(diff.name, rec, flush=True)
(run / "grades.json").write_text(json.dumps(out, indent=1))
