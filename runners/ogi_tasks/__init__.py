"""OGI task families with independent executed verifiers (OGI-STUDY-0 prerequisite, audit gap 7 / D7).

    Task(id, family, prompt, visible_checks)          what an arm may see
    grade(task, answer) -> {correct, evidence}       grader only; reads hidden tests / answer keys
    select_by_visible(task, candidates) -> index     the uniform selector every arm ends with (D2)

Grader-only material (hidden tests, answer keys, reference solutions) is kept in a module registry keyed by
(family, id), never on the Task object, so whatever receives a Task cannot leak it into a prompt.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

from . import code, mathkey

MANIFEST = json.loads((Path(__file__).with_name("datasets.json")).read_text())
DATA_DIR = Path(os.environ.get("OGI_TASKS_DATA", "/root/fruits/ogi-tasks/data"))


@dataclass(frozen=True)
class Task:
    id: str
    family: str          # "code" | "math"
    prompt: str
    visible_checks: str  # code: the visible unittest module; math: "" (no visible check)


_HIDDEN: dict[tuple[str, str], dict] = {}


def make_task(family: str, row: dict) -> Task:
    public, hidden = {"code": code.build, "math": mathkey.build}[family](row)
    task = Task(**public)
    _HIDDEN[(task.family, task.id)] = hidden
    return task


def _verified(name: str) -> Path:
    m = MANIFEST[name]
    p = DATA_DIR / m["file"]
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    if digest != m["sha256"]:
        raise ValueError(f"{p}: sha256 {digest} != pinned {m['sha256']}")
    return p


def load_bigcodebench_hard() -> list[Task]:
    import pyarrow.parquet as pq
    return [make_task("code", r) for r in pq.read_table(_verified("bigcodebench-hard")).to_pylist()]


def load_math_level5() -> list[Task]:
    rows = [json.loads(line) for line in _verified("math-500").read_text().splitlines() if line.strip()]
    return [make_task("math", r) for r in rows if r["level"] == 5]


def grade(task: Task, answer: str, **sandbox_kw) -> dict:
    h = _HIDDEN[(task.family, task.id)]
    if task.family == "code":
        names = h["visible"] + h["hidden"]
        r = code.run_tests(code.extract_code(answer, h["entry_point"]), h["test"], names, **sandbox_kw)
        hidden_ok = all(r["per_test"][n] for n in h["hidden"])
        return {"correct": hidden_ok and not r["timeout"], "evidence": {
            "verifier": "executed:hidden-tests", "hidden_passed": sum(r["per_test"][n] for n in h["hidden"]),
            "hidden_total": len(h["hidden"]), "visible_passed": sum(r["per_test"][n] for n in h["visible"]),
            "all_tests_pass": r["passed"] == len(names) and not r["timeout"], **{k: r[k] for k in
            ("per_test", "load_error", "timeout", "exit", "isolation", "stderr_tail")}}}
    g, p = mathkey.gold(h["answer"]), mathkey.extract(answer)
    return {"correct": mathkey.equivalent(g, p), "evidence": {
        "verifier": "dataset_key:math-verify", "parsed": [str(x) for x in p], "parsable": bool(p)}}


def select_by_visible(task: Task, candidates: list[str], **sandbox_kw) -> int:
    """Index of the selected candidate; ties go to the earliest. Uses only what arms may see.
    code: most visible tests passed. math: plurality of math-verify equivalence classes (no key)."""
    if not candidates:
        raise ValueError("no candidates")
    if task.family == "code":
        names = [f"{c.name}.{f.name}" for c, f in code._methods(ast.parse(task.visible_checks))]
        scores = [code.run_tests(code.extract_code(c), task.visible_checks, names, **sandbox_kw)["passed"]
                  for c in candidates]
        return scores.index(max(scores))
    parsed = [mathkey.extract(c) for c in candidates]
    classes: list[list[int]] = []                       # each class: candidate indices, first = representative
    for i, p in enumerate(parsed):
        if not p:
            continue
        for cl in classes:
            if mathkey.equivalent(parsed[cl[0]], p):
                cl.append(i)
                break
        else:
            classes.append([i])
    return max(classes, key=len)[0] if classes else 0    # max keeps the first maximal class = earliest
