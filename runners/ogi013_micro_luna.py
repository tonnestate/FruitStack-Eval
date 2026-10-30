"""Micro pilot arm L: Luna (Codex headless, gpt-6-luna) on one micro task, same issue text, one run, 30 min cap.
usage: ogi013_micro_luna.py TASKDIR OUTDIR     (TASKDIR holds base/, agent_task.json, venv38/; the host python is enough: no stack, no MangoMe)"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ogi013_luna_branches import luna  # noqa: E402

task_dir, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
task = json.load(open(task_dir / "agent_task.json"))
ws = out / "ws"
out.mkdir(parents=True, exist_ok=True)
shutil.copytree(task_dir / "base", ws)
py = task_dir / "venv38/bin/python"
prompt = (f"You are working in a checkout of a Python package in the current directory. Python 3.8 interpreter: {py} ; run tests with: PYTHONPATH=. {py} tests/runtests.py <dotted.module>\n"
          f"ISSUE:\n{task['problem_statement']}\nFix the issue by changing the source code under django/, run the relevant existing tests after your last edit, and finish.")
res = luna(prompt, ws, "workspace-write", out / "luna")
subprocess.run(["git", "add", "-A", "--", "django"], cwd=ws, check=True)
diff = subprocess.run(["git", "diff", "--cached", "--no-color", task["base_commit"], "--", "django"], cwd=ws, capture_output=True, text=True, check=True).stdout
(out / "snapshots").mkdir(exist_ok=True)
(out / "snapshots" / "L_final.diff").write_text(diff)
summary = {"status": "DONE" if diff.strip() else "NO_PATCH", "usage": res["usage"], "seconds": res["seconds"], "exit": res["exit"], "final": res["final"][:500]}
(out / "run.json").write_text(json.dumps(summary, indent=1))
print(json.dumps(summary))
