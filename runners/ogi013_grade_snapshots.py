"""Grade every snapshot diff of a team run (Addendum 3 B.5) with evaluate_v2.py v2.1: applies each diff to a fresh base copy, grades, writes grades.json.
usage: ogi013_grade_snapshots.py RUN_DIR   (frozen task only: evaluate_v2.py is bound to task.json of OGI013-SINGLE-TASK)"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TASK = Path("/root/fruits/research/OGI013-SINGLE-TASK")
run = Path(sys.argv[1])
out = {}
for diff in sorted((run / "snapshots").glob("*.diff")):
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp) / "ws"
        shutil.copytree(TASK / "base", ws)
        if diff.stat().st_size:
            subprocess.run(["git", "apply", "--whitespace=nowarn", str(diff.resolve())], cwd=ws, check=True)
        res = Path(tmp) / "g.json"
        subprocess.run([str(TASK / "venv38/bin/python"), str(TASK / "evaluate_v2.py"), str(ws), str(res)], capture_output=True, text=True, timeout=2400)
        g = json.loads(res.read_text())
    out[diff.name] = {k: g.get(k) for k in ("resolved", "f2p_passed", "f2p_total", "p2p_passed", "p2p_total", "runner_exit", "error")}
    print(diff.name, out[diff.name], flush=True)
(run / "grades.json").write_text(json.dumps(out, indent=1))
