"""BigCodeBench(-Hard) adapter: deterministic visible/hidden split of each task's unittest suite.

Split rule (fixed, data-independent): the test methods of every unittest.TestCase class are ordered by
sha256("OGI-TASKS|bcb-split|<task_id>|<Class.method>"); the first max(1, n // 3) are VISIBLE, the rest
HIDDEN. Tasks with fewer than 2 test methods are rejected (no non-empty hidden set).
Visible tests go into the prompt and into every arm's selector; hidden tests are run only by the grader.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re

from . import sandbox

SPLIT_SALT = "OGI-TASKS|bcb-split"
PROMPT = """{instruct}

Visible tests (a subset of the tests; further hidden tests decide correctness):
```python
{visible}
```
Return the complete solution as one ```python code block."""

# ponytail: candidate and tests share one interpreter (as in the official BigCodeBench harness), so a
# hostile candidate could forge results.json; move the harness to a separate process if reward hacking shows up.
HARNESS = """import json, sys, unittest
sel = json.loads(open("selection.json").read())
ns = {"__name__": "__candidate__"}
try:
    exec(compile(open("candidate.py").read(), "candidate.py", "exec"), ns)
    exec(compile(open("tests.py").read(), "tests.py", "exec"), ns)
except BaseException as e:
    res = {"load_error": type(e).__name__}
else:
    res = {}
    for name in sel:
        cls, meth = name.split(".")
        r = unittest.TestResult()
        try:
            unittest.TestSuite([ns[cls](meth)]).run(r)   # suite, so setUpClass/tearDownClass run
            res[name] = not (r.failures or r.errors)
        except BaseException:
            res[name] = False
open("results.json", "w").write(json.dumps(res))
"""


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
              "entry_point": row.get("entry_point", "task_func"), "canonical_solution": row.get("canonical_solution")}
    return public, hidden


def extract_code(answer: str, entry_point: str = "task_func") -> str:
    """Longest fenced block defining the entry point, else the longest fenced block, else the raw text."""
    blocks = re.findall(r"```(?:python|py)?[^\n]*\n(.*?)```", answer, flags=re.S)
    if not blocks:
        return answer
    with_entry = [b for b in blocks if re.search(rf"def\s+{re.escape(entry_point)}\b", b)]
    return max(with_entry or blocks, key=len)


def run_tests(code: str, test_src: str, names: list[str], **kw) -> dict:
    r = sandbox.run_python({"candidate.py": code, "tests.py": test_src, "selection.json": json.dumps(names),
                            "harness.py": HARNESS}, ["harness.py"], **kw)
    try:
        res = json.loads(r["outputs"].get("results.json", "{}"))
    except ValueError:
        res = {}
    per = {n: bool(res.get(n)) for n in names}
    return {"per_test": per, "passed": sum(per.values()), "load_error": res.get("load_error"),
            "timeout": r["timeout"], "exit": r["exit"], "isolation": r["isolation"], "stderr_tail": r["stderr"][-1500:]}
