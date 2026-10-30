#!/usr/bin/env python3
"""OGI-013 SINGLE-TASK acceptance evaluator, v2 (calibration amendment to the frozen evaluate.py; no LLM, no simulator).

Fixes defects found by calibration on 2026-10-30, before any competitor run was scored:
  D1  the frozen evaluator cleared the environment and never put the evaluated tree on sys.path, so Django was imported
      from whatever was installed in venv38 -> the agent's source code was never tested (base and gold scored identically);
  D2  12 of the 58 PASS_TO_PASS tests are named by their docstring; the frozen parser only matched "name (module.Class)",
      so they could never count as passed, and the docstrings were passed to runtests.py as bogus module labels;
  D3  "skipped" counted as passed; SWE-bench grading counts only PASSED / XFAIL.
  D4  tests with a docstring print "test_x (mod.Class)" and "Docstring ... ok" on two lines; the SWE-bench lists name
      some of them by method, some by docstring, so the result is recorded under both keys.

usage: evaluate_v2.py WORKDIR OUTJSON
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = str(HERE / "venv38/bin/python")
TASK = json.load(open(HERE / "task.json"))
F2P = json.loads(TASK["FAIL_TO_PASS"])
P2P = json.loads(TASK["PASS_TO_PASS"])
LABEL_RE = re.compile(r"\(([\w.]+)\.\w+\)$")
# runner modules are taken only from properly named tests (D2); docstring-named tests live in the same modules
MODULES = sorted({LABEL_RE.search(n).group(1) for n in F2P + P2P if LABEL_RE.search(n)})
# Django -v 2 prints "test_x (mod.Class) ... ok" or, for docstring tests, "test_x (mod.Class)\nDocstring ... ok"
RESULT_RE = re.compile(r"^(.+?) \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|unexpected success)\s*$")
PASS_STATES = ("ok", "expected failure")  # D3: skipped is not a pass


def evaluate(work: Path) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "tree"
        shutil.copytree(work, copy, ignore=shutil.ignore_patterns("*.pyc", "__pycache__", ".git"))
        # a .git directory is needed for git apply; recreate a minimal one from the work tree
        subprocess.run(["git", "init", "-q"], cwd=copy, check=True)
        patch = Path(tmp) / "test.patch"
        patch.write_text(TASK["test_patch"])
        # overwrite the target test files with their base versions first, so an agent cannot pre-edit them (anti-tamper)
        base_tests = re.findall(r"^diff --git a/(\S+)", TASK["test_patch"], re.M)
        for rel in base_tests:
            src = subprocess.run(["git", "show", f"{TASK['base_commit']}:{rel}"], cwd=work, capture_output=True, text=True)
            if src.returncode == 0:
                (copy / rel).write_text(src.stdout)
        a = subprocess.run(["git", "apply", "--whitespace=nowarn", str(patch)], cwd=copy, capture_output=True, text=True)
        env = {"PYTHONWARNINGS": "ignore", "PATH": "/usr/bin:/bin", "PYTHONPATH": str(copy), "LANG": "C.UTF-8"}  # D1
        r = subprocess.run([PY, "tests/runtests.py", "--parallel", "1", "-v", "2", *MODULES], cwd=copy,
                           capture_output=True, text=True, timeout=1800, env=env)
        probe = subprocess.run([PY, "-c", "import django,sys;print(django.__file__)"], cwd=copy / "tests",
                               capture_output=True, text=True, env=env)
    out = r.stdout + "\n" + r.stderr
    status = {}
    header = None  # "test_x (mod.Class)" printed alone on a line when a docstring follows
    for line in out.splitlines():
        m = RESULT_RE.match(line)
        if m:
            status[m.group(1)] = m.group(2)
            if header and not LABEL_RE.search(m.group(1)):  # docstring result line: key it under the method name too
                status[header] = m.group(2)
            header = None
        elif re.match(r"^\w+ \([\w.]+\)$", line):
            header = line

    def passed(names):
        return [n for n in names if status.get(n, "") in PASS_STATES]

    f2p_ok, p2p_ok = passed(F2P), passed(P2P)
    return {
        "evaluator": "evaluate_v2",
        "patch_applied": a.returncode == 0,
        "django_imported_from": probe.stdout.strip(),
        "f2p_total": len(F2P), "f2p_passed": len(f2p_ok),
        "p2p_total": len(P2P), "p2p_passed": len(p2p_ok),
        "f2p_failed": [n for n in F2P if n not in f2p_ok],
        "p2p_failed": [n for n in P2P if n not in p2p_ok],
        "unparsed_required": [n for n in F2P + P2P if n not in status],
        "runner_exit": r.returncode,
        "resolved": a.returncode == 0 and r.returncode == 0 and len(f2p_ok) == len(F2P) and len(p2p_ok) == len(P2P),
        "tail": out[-800:],
    }


if __name__ == "__main__":
    res = evaluate(Path(sys.argv[1]).resolve())
    json.dump(res, open(sys.argv[2], "w"), indent=1)
    print({k: v for k, v in res.items() if k not in ("tail", "f2p_failed", "p2p_failed", "unparsed_required")})
