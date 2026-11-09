"""BigCodeBench(-Hard) adapter: deterministic visible/hidden split of each task's unittest suite.

Split rule (fixed, data-independent): the test methods of every unittest.TestCase class are ordered by
sha256("OGI-TASKS|bcb-split|<task_id>|<Class.method>"); the first max(1, n // 3) are VISIBLE, the rest
HIDDEN. Tasks with fewer than 2 test methods are rejected (no non-empty hidden set).
Visible tests go into the prompt and into every arm's selector; hidden tests are run only by the grader.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

from . import sandbox

BOUNDARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boundary.py")
MODES = ("confirmatory", "dev")

SPLIT_SALT = "OGI-TASKS|bcb-split"
PROMPT = """{instruct}

Visible tests (a subset of the tests; further hidden tests decide correctness):
```python
{visible}
```
Return the complete solution as one ```python code block."""



def _methods(tree: ast.Module) -> list[tuple[ast.ClassDef, ast.FunctionDef]]:
    return [(c, f) for c in tree.body if isinstance(c, ast.ClassDef)
            for f in c.body if isinstance(f, ast.FunctionDef) and f.name.startswith("test")]


def split_tests(task_id: str, test_src: str) -> dict:
    """-> {visible: [names], hidden: [names], visible_src, hidden_src: {name: source}}"""
    tree = ast.parse(test_src)
    meths = _methods(tree)
    names = sorted((f"{c.name}.{f.name}" for c, f in meths),
                   key=lambda n: hashlib.sha256(f"{SPLIT_SALT}|{task_id}|{n}".encode()).hexdigest())
    if len(names) < 2:
        raise ValueError(f"{task_id}: {len(names)} test methods, need >= 2 for a visible/hidden split")
    visible = names[:max(1, len(names) // 3)]
    hidden_src = {f"{c.name}.{f.name}": ast.get_source_segment(test_src, f) for c, f in meths
                  if f"{c.name}.{f.name}" not in visible}
    for c, f in meths:                               # strip hidden methods from the visible module
        if f"{c.name}.{f.name}" not in visible:
            c.body.remove(f)
            if not c.body:
                c.body.append(ast.Pass())
    return {"visible": visible, "hidden": sorted(hidden_src), "visible_src": ast.unparse(tree),
            "hidden_src": hidden_src}


def build(row: dict) -> tuple[dict, dict]:
    """BigCodeBench row -> (public task fields, grader-only material)."""
    s = split_tests(row["task_id"], row["test"])
    public = {"id": row["task_id"], "family": "code",
              "prompt": PROMPT.format(instruct=row["instruct_prompt"].strip(), visible=s["visible_src"]),
              "visible_checks": s["visible_src"]}
    hidden = {"test": row["test"], "visible": s["visible"], "hidden": s["hidden"], "hidden_src": s["hidden_src"],
              "entry_point": row.get("entry_point", "task_func"), "canonical_solution": row.get("canonical_solution"),
              "code_prompt": row.get("code_prompt", ""), "libs": row.get("libs", "[]")}
    return public, hidden


def extract_code(answer: str, entry_point: str = "task_func") -> str:
    """Longest fenced block defining the entry point, else the longest fenced block, else the raw text."""
    blocks = re.findall(r"```(?:python|py)?[^\n]*\n(.*?)```", answer, flags=re.S)
    if not blocks:
        return answer
    with_entry = [b for b in blocks if re.search(rf"def\s+{re.escape(entry_point)}\b", b)]
    return max(with_entry or blocks, key=len)


def run_tests(code: str, test_src: str, names: list[str], *, code_prompt: str = "", entry_point: str = "task_func",
              python: str = sys.executable, timeout: float = 60, mem_mb: int = 4096, mode: str = "confirmatory") -> dict:
    """Run test `names` against `code` behind the trusted boundary (boundary.py). `timeout` is per test.

    The verdict per test comes only from the trusted evaluator's report; nothing the candidate writes is read.
    confirmatory: bwrap and its preflight are mandatory, OGI_ALLOW_UNSANDBOXED is ignored (sandbox.wrap)."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, not {mode!r}")
    confirmatory, python = mode == "confirmatory", os.path.abspath(python)
    _, isolation = sandbox.wrap([], "/", python, confirmatory=confirmatory)     # raises SANDBOX_UNAVAILABLE
    if confirmatory:
        sandbox.preflight(python)
    spec = {"code": code, "test_src": test_src, "names": names, "code_prompt": code_prompt, "entry": entry_point,
            "python": python, "timeout": timeout, "mem_mb": mem_mb, "confirmatory": confirmatory,
            "allow_unsandboxed": isolation != sandbox.ISOLATED}
    rep, err, exit_code = None, "", None
    with tempfile.TemporaryDirectory(prefix="ogi-eval-") as d:
        try:   # ponytail: wall budget = all tests timing out + slack; a per-test kill lives in the evaluator
            p = subprocess.run([python, "-I", BOUNDARY, "evaluate"], input=json.dumps(spec), capture_output=True,
                               text=True, errors="replace", cwd=d, env=sandbox.env(d),
                               timeout=timeout * (len(names) + 1) + 60)
            exit_code, err = p.returncode, p.stderr
            rep = json.loads(p.stdout)
        except (subprocess.TimeoutExpired, ValueError) as e:
            err += f"\nEVALUATOR_FAILED: {type(e).__name__}"
    if not isinstance(rep, dict) or not isinstance(rep.get("per_test"), dict):
        rep = {"per_test": {}, "evaluator_error": "EVALUATOR_FAILED"}
    per = {n: rep["per_test"].get(n) is True for n in names}
    faults = rep.get("faults") or {}
    return {"per_test": per, "passed": sum(per.values()), "load_error": rep.get("load_error"),
            "setup_error": rep.get("setup_error"), "evaluator_error": rep.get("evaluator_error"), "faults": faults,
            "timeout": any(f == "TIMEOUT" for fs in faults.values() for f in fs), "exit": exit_code,
            "isolation": rep.get("isolation") or isolation, "mode": mode,
            "stderr_tail": (err[-700:] + "\n--- candidate ---\n" + (rep.get("candidate_stderr_tail") or ""))[-1500:]}


# ---- eligibility for confirmatory grading behind the boundary (static part; the reference run is in __init__) ----
MOCK_NAMES = {"mock", "patch", "Mock", "MagicMock", "create_autospec", "PropertyMock"}
FS_NAMES = {"open", "os", "shutil", "tempfile", "pathlib", "Path", "glob", "zipfile", "tarfile"}
STREAM_NAMES = {"stdout", "stderr", "redirect_stdout", "redirect_stderr", "capsys", "capture_output"}


def _imports(tree: ast.Module) -> set[str]:
    return {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} | \
           {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}


def ineligibility(libs: list[str], test_src: str, code_prompt: str = "", dataset_libs: frozenset = frozenset(),
                  check_env: bool = True, semantics: str = "boundary") -> str | None:
    """Static reason why a task's tests need in-process access to the candidate (or cannot run here), else None.
    Conservative: a name that merely appears in the test module is enough to exclude the task.
    UNDECLARED_TEST_DEPENDENCY: the tests import a third-party module that no task of the dataset declares in
    `libs` (`dataset_libs`), i.e. outside the benchmark's own environment spec (faker in BigCodeBench-Hard)."""
    tree = ast.parse(test_src)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
            {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    mods = _imports(tree)
    tops = {m.split(".")[0] for m in mods}
    undeclared = sorted(m for m in tops if m not in sys.stdlib_module_names and m not in libs
                        and m not in dataset_libs)
    if undeclared:
        return "UNDECLARED_TEST_DEPENDENCY:" + ",".join(undeclared)
    if semantics != "official":                    # official: in-process access is the benchmark's own semantics; only env rules apply
        if names & MOCK_NAMES or "unittest.mock" in mods:
            return "IN_PROCESS_MOCK_PATCH"
        if names & FS_NAMES or tops & FS_NAMES:
            return "FILESYSTEM_SIDE_EFFECTS_INSPECTED_IN_PROCESS"
        if names & STREAM_NAMES:
            return "IN_PROCESS_STREAM_CAPTURE"
    if not check_env:
        return None
    tops |= {m.split(".")[0] for m in _imports(ast.parse(code_prompt + "    pass\n"))} if code_prompt else set()
    missing = sorted(m for m in set(libs) | tops if importlib.util.find_spec(m) is None)
    return "DEPENDENCY_UNAVAILABLE_IN_GRADER_ENV:" + ",".join(missing) if missing else None


# ---- official BigCodeBench semantics (owner decision D2, 2026-11-09) ----
# Candidate and tests share one interpreter, as the benchmark defines correctness, inside the same bwrap sandbox.
# The verdict line carries a nonce the runner reads and deletes before candidate code runs, and is written with
# output primitives captured before that; a static tamper audit rejects candidates that reach the test machinery.
# ponytail: static audit, not a proof of non-interference; a per-test process boundary is the upgrade (= semantics "boundary").
OFFICIAL_RUNNER = r'''
import json, os, signal, sys, unittest
_nonce = open("_nonce").read(); os.unlink("_nonce")
_w, _dumps, _TR, _TS = os.write, json.dumps, unittest.TestResult, unittest.TestSuite
spec = json.load(open("_spec.json")); os.unlink("_spec.json")
ns = {"__name__": "__ogi_candidate__"}
per, load_error = {}, None
try:
    exec(compile(open("candidate.py").read(), "candidate.py", "exec"), ns)
    exec(compile(open("tests.py").read(), "tests.py", "exec"), ns)
except BaseException as e:  # noqa: BLE001 - a load failure fails every test
    load_error = f"{type(e).__name__}: {str(e)[:200]}"
def _alarm(*_):
    raise TimeoutError("TEST_TIMEOUT")
for name in spec["names"]:
    ok = False
    if load_error is None:
        cls, meth = name.split(".", 1)
        try:
            signal.signal(signal.SIGALRM, _alarm); signal.alarm(int(spec["timeout"]))
            r = _TR(); _TS([ns[cls](meth)]).run(r)
            ok = r.testsRun == 1 and not r.failures and not r.errors and not r.unexpectedSuccesses and not r.skipped
        except BaseException:  # noqa: BLE001
            ok = False
        finally:
            signal.alarm(0)
    per[name] = ok
_w(1, ("\n" + _nonce + _dumps({"per_test": per, "load_error": load_error}) + "\n").encode())
'''
TAMPER_NAMES = {"unittest", "TestCase", "TestResult", "TestSuite", "modules", "_getframe", "f_back", "f_globals", "f_locals",
                "__builtins__", "builtins", "__import__", "importlib", "inspect", "gc", "ctypes", "_exit", "exit", "quit", "kill",
                "SystemExit", "signal", "alarm", "setitimer", "atexit", "faulthandler", "__subclasses__", "__globals__", "__code__",
                "settrace", "setprofile", "_nonce", "_w", "_dumps", "_TR", "_TS", "stdout", "__stdout__"}


def tamper_audit(code: str) -> list[str]:
    """Static reasons a candidate could interfere with the in-process test machinery or the verdict ([] = clean).
    Also flags assignment to an attribute of an imported module (monkeypatching, e.g. `np.testing.x = ...`)."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []                                   # does not load; graded FAIL by the run itself
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | \
            {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)} | \
            {a.asname or a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names} | \
            {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
    found = sorted(names & TAMPER_NAMES)
    mods = {a.asname or a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    for n in ast.walk(tree):
        targets = n.targets if isinstance(n, ast.Assign) else [n.target] if isinstance(n, (ast.AugAssign, ast.AnnAssign)) else []
        for t in targets:
            base = t
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(t, ast.Attribute) and isinstance(base, ast.Name) and base.id in mods:
                found.append(f"MODULE_ATTRIBUTE_ASSIGNED:{base.id}")
    return found


def run_tests_official(code: str, test_src: str, names: list[str], *, code_prompt: str = "", entry_point: str = "task_func",
                       python: str = sys.executable, timeout: float = 60, mem_mb: int = 4096, mode: str = "confirmatory") -> dict:
    """Same return shape as run_tests, official in-process semantics (see block comment)."""
    import secrets
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, not {mode!r}")
    confirmatory, python = mode == "confirmatory", os.path.abspath(python)
    if confirmatory:
        sandbox.preflight(python)
    nonce = "OGI-VERDICT-" + secrets.token_hex(16) + ":"
    r = sandbox.run_python({"_nonce": nonce, "_spec.json": json.dumps({"names": names, "timeout": timeout}), "candidate.py": code,
                            "tests.py": test_src, "runner.py": OFFICIAL_RUNNER}, ["runner.py"], python=python,
                           timeout=timeout * (len(names) + 1) + 30, mem_mb=mem_mb, confirmatory=confirmatory)
    rep = next((json.loads(line[len(nonce):]) for line in reversed(r["stdout"].splitlines()) if line.startswith(nonce)), None)
    per = {n: bool(rep and rep["per_test"].get(n) is True) for n in names}
    return {"per_test": per, "passed": sum(per.values()), "load_error": (rep or {}).get("load_error"), "setup_error": None,
            "evaluator_error": None if rep else "NO_VERDICT", "faults": {}, "timeout": r["timeout"], "exit": r["exit"],
            "isolation": r["isolation"], "mode": mode, "semantics": "official", "stderr_tail": r["stderr"][-1500:]}
