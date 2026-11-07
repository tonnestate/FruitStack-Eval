#!/usr/bin/env python3
"""Frozen acceptance evaluation (SWE-bench protocol, no LLM, no simulator): in a COPY of the working tree, overwrite the test files with the task's test_patch, run the Django test runner on the
modules that contain FAIL_TO_PASS / PASS_TO_PASS tests, parse per-test results. usage: evaluate.py WORKDIR OUTJSON"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
PY = str(HERE / "venv38/bin/python")
t = json.load(open(HERE / "task.json"))
f2p, p2p = json.loads(t["FAIL_TO_PASS"]), json.loads(t["PASS_TO_PASS"])
def mod(name): return re.search(r"\(([\w.]+)\.\w+\)$", name).group(1) if re.search(r"\(([\w.]+)\.\w+\)$", name) else name
modules = sorted({mod(n) for n in f2p + p2p})
work = Path(sys.argv[1])
with tempfile.TemporaryDirectory() as tmp:
    copy = Path(tmp) / "tree"
    shutil.copytree(work, copy, ignore=shutil.ignore_patterns("*.pyc", "__pycache__"))
    (Path(tmp) / "test.patch").write_text(t["test_patch"])
    a = subprocess.run(["git", "apply", "--whitespace=nowarn", str(Path(tmp) / "test.patch")], cwd=copy, capture_output=True, text=True)
    if a.returncode:                                   # the agent already touched the test file: take the task's version of the test files verbatim
        subprocess.run(["git", "checkout", "--", "tests"], cwd=copy, capture_output=True)
        a = subprocess.run(["git", "apply", "--whitespace=nowarn", str(Path(tmp) / "test.patch")], cwd=copy, capture_output=True, text=True)
    r = subprocess.run([PY, "tests/runtests.py", "--parallel", "1", "-v", "2", *modules], cwd=copy, capture_output=True, text=True, timeout=1800, env={"PYTHONWARNINGS": "ignore", "PATH": "/usr/bin:/bin"})
out = r.stdout + "\n" + r.stderr
status = {}
for line in out.splitlines():
    m = re.match(r"^(\S.*? \([\w.]+\))(?: \.\.\.|\n)?\s*(?:\n)?.*?\.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|unexpected success)\s*$", line)
    if m:
        status[m.group(1)] = m.group(2)
def passed(names): return [n for n in names if status.get(n, "").startswith("ok") or status.get(n, "").startswith("skipped")]
res = {"patch_applied": a.returncode == 0, "f2p_total": len(f2p), "f2p_passed": len(passed(f2p)), "p2p_total": len(p2p), "p2p_passed": len(passed(p2p)),
       "f2p_failed": [n for n in f2p if n not in passed(f2p)], "p2p_failed": [n for n in p2p if n not in passed(p2p)], "runner_exit": r.returncode,
       "resolved": a.returncode == 0 and len(passed(f2p)) == len(f2p) and len(passed(p2p)) == len(p2p), "tail": out[-600:]}
json.dump(res, open(sys.argv[2], "w"), indent=1)
print({k: v for k, v in res.items() if k not in ("tail", "f2p_failed", "p2p_failed")})
