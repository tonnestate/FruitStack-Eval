#!/usr/bin/env python3
"""OGI-013 SINGLE-TASK acceptance evaluator, v2.1 (calibration amendment to the frozen evaluate.py; no LLM, no simulator).

Fixes defects found by calibration on 2026-10-30, before any competitor run was scored:
  D1  the frozen evaluator cleared the environment and never put the evaluated tree on sys.path, so Django was imported
      from whatever was installed in venv38 -> the agent's source code was never tested (base and gold scored identically);
  D2  12 of the 58 PASS_TO_PASS tests are named by their docstring; the frozen parser only matched "name (module.Class)",
      so they could never count as passed, and the docstrings were passed to runtests.py as bogus module labels;
  D3  "skipped" counted as passed; SWE-bench grading counts only PASSED / XFAIL;
  D4  tests with a docstring print "test_x (mod.Class)" and "Docstring ... ok" on two lines; the SWE-bench lists name
      some of them by method, some by docstring, so the result is recorded under both keys;
  D5  (v2.1) the anti-tamper reset trusted the agent's own .git and ignored failures. The evaluated tree is now built from
      an evaluator-owned pristine base checkout plus ONLY the agent's changes under django/ (excluding django/test/).
      Changes anywhere else (tests/, runtests.py, a planted sitecustomize.py, ...) are discarded and listed; changes to
      django/test/ reject the submission. Any failure of the guard fails closed (resolved = false, error recorded).

usage: evaluate_v2.py WORKDIR OUTJSON
pristine base: $FSE_BASE_TREE or <this dir>/base_tree, a clean git checkout of task.json:base_commit owned by the evaluator.
"""
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = str(HERE / "venv38/bin/python")
BASE = Path(os.environ.get("FSE_BASE_TREE", HERE / "base_tree")).resolve()
TASK = json.load(open(HERE / "task.json"))
F2P = json.loads(TASK["FAIL_TO_PASS"])
P2P = json.loads(TASK["PASS_TO_PASS"])
LABEL_RE = re.compile(r"\(([\w.]+)\.\w+\)$")
MODULES = sorted({LABEL_RE.search(n).group(1) for n in F2P + P2P if LABEL_RE.search(n)})  # D2
RESULT_RE = re.compile(r"^(.+?) \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|unexpected success)\s*$")
PASS_STATES = ("ok", "expected failure")  # D3
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
ACCEPT_PREFIX = "django/"
REJECT_PREFIX = "django/test/"


class GuardError(Exception):
    pass


def files_of(root: Path) -> set:
    out = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if not f.endswith(".pyc"):
                out.add(str((Path(dirpath) / f).relative_to(root)))
    return out


def check_base() -> None:
    if not (BASE / ".git").exists():
        raise GuardError(f"BASE_TREE_MISSING: {BASE}")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=BASE, capture_output=True, text=True)
    if head.returncode or head.stdout.strip() != TASK["base_commit"]:
        raise GuardError(f"BASE_TREE_WRONG_REVISION: {head.stdout.strip() or head.stderr.strip()}")
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=BASE, capture_output=True, text=True)
    if dirty.returncode or dirty.stdout.strip():
        raise GuardError("BASE_TREE_DIRTY")


def agent_changes(work: Path):
    """Return (accepted_changed, accepted_deleted, discarded, rejected) relative paths."""
    base_files, work_files = files_of(BASE), files_of(work)
    changed = sorted(p for p in work_files if p not in base_files or not filecmp.cmp(BASE / p, work / p, shallow=False))
    deleted = sorted(base_files - work_files)
    def bucket(p):
        if p.startswith(REJECT_PREFIX):
            return "rejected"
        return "accepted" if p.startswith(ACCEPT_PREFIX) else "discarded"
    acc_c = [p for p in changed if bucket(p) == "accepted"]
    acc_d = [p for p in deleted if bucket(p) == "accepted"]
    discarded = [p for p in changed + deleted if bucket(p) == "discarded"]
    rejected = [p for p in changed + deleted if bucket(p) == "rejected"]
    return acc_c, acc_d, discarded, rejected


def evaluate(work: Path) -> dict:
    res = {"evaluator": "evaluate_v2.1", "resolved": False, "error": None}
    try:
        check_base()
        if not work.is_dir():
            raise GuardError(f"WORKDIR_MISSING: {work}")
        acc_c, acc_d, discarded, rejected = agent_changes(work)
        res.update({"applied_agent_files": acc_c + [f"(deleted) {p}" for p in acc_d],
                    "discarded_agent_files": discarded, "rejected_agent_files": rejected})
        if rejected:
            raise GuardError("REJECTED_TEST_FRAMEWORK_CHANGE")
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "tree"
            shutil.copytree(BASE, copy, ignore=shutil.ignore_patterns(*SKIP_DIRS, "*.pyc"))
            for p in acc_c:
                (copy / p).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(work / p, copy / p)
            for p in acc_d:
                (copy / p).unlink()
            subprocess.run(["git", "init", "-q"], cwd=copy, check=True)
            patch = Path(tmp) / "test.patch"
            patch.write_text(TASK["test_patch"])
            a = subprocess.run(["git", "apply", "--whitespace=nowarn", str(patch)], cwd=copy, capture_output=True, text=True)
            if a.returncode:
                raise GuardError("TEST_PATCH_DID_NOT_APPLY_TO_PRISTINE_TESTS: " + a.stderr[-300:])
            env = {"PYTHONWARNINGS": "ignore", "PATH": "/usr/bin:/bin", "PYTHONPATH": str(copy), "LANG": "C.UTF-8"}  # D1
            r = subprocess.run([PY, "tests/runtests.py", "--parallel", "1", "-v", "2", *MODULES], cwd=copy,
                               capture_output=True, text=True, timeout=1800, env=env)
            probe = subprocess.run([PY, "-c", "import django;print(django.__file__)"], cwd=copy / "tests",
                                   capture_output=True, text=True, env=env)
            imported = probe.stdout.strip()
            if not imported.startswith(str(copy)):
                raise GuardError(f"DJANGO_NOT_FROM_EVALUATED_TREE: {imported or probe.stderr[-200:]}")
    except (GuardError, OSError, subprocess.SubprocessError) as e:
        res["error"] = f"{type(e).__name__}: {e}"
        return res

    out = r.stdout + "\n" + r.stderr
    status, header = {}, None  # D4
    for line in out.splitlines():
        m = RESULT_RE.match(line)
        if m:
            status[m.group(1)] = m.group(2)
            if header and not LABEL_RE.search(m.group(1)):
                status[header] = m.group(2)
            header = None
        elif re.match(r"^\w+ \([\w.]+\)$", line):
            header = line

    def passed(names):
        return [n for n in names if status.get(n, "") in PASS_STATES]

    f2p_ok, p2p_ok = passed(F2P), passed(P2P)
    res.update({
        "patch_applied": True,
        "django_imported_from": imported,
        "f2p_total": len(F2P), "f2p_passed": len(f2p_ok),
        "p2p_total": len(P2P), "p2p_passed": len(p2p_ok),
        "f2p_failed": [n for n in F2P if n not in f2p_ok],
        "p2p_failed": [n for n in P2P if n not in p2p_ok],
        "unparsed_required": [n for n in F2P + P2P if n not in status],
        "runner_exit": r.returncode,
        "resolved": r.returncode == 0 and len(f2p_ok) == len(F2P) and len(p2p_ok) == len(P2P),
        "tail": out[-800:],
    })
    return res


if __name__ == "__main__":
    result = evaluate(Path(sys.argv[1]).resolve())
    json.dump(result, open(sys.argv[2], "w"), indent=1)
    print({k: v for k, v in result.items() if k not in ("tail", "f2p_failed", "p2p_failed", "unparsed_required")})
