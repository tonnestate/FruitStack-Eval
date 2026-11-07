"""OGI task families with independent executed verifiers (OGI-STUDY-0 prerequisite, audit gap 7 / D7).

    Task(id, family, prompt, visible_checks)          what an arm may see
    grade(task, answer, mode=) -> {correct, grade, mode, evidence}   grader only; reads hidden tests / answer keys
    select_by_visible(task, candidates) -> index     the uniform selector every arm ends with (D2)

Grader-only material (hidden tests, answer keys, reference solutions) is kept in a module registry keyed by
(family, id), never on the Task object, so whatever receives a Task cannot leak it into a prompt.

Code tasks are graded behind the trusted boundary in boundary.py (candidate in bwrap, tests and verdict in a
trusted evaluator). mode="confirmatory" (default) grades only tasks listed ELIGIBLE in eligibility.json and
refuses to run without bwrap; mode="dev" grades anything and may run unsandboxed with OGI_ALLOW_UNSANDBOXED=1.
Rows carry their mode. MATH grading never executes candidate output (math-verify parses the answer string).
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from . import code, mathkey

MANIFEST = json.loads((Path(__file__).with_name("datasets.json")).read_text())
ELIGIBILITY_FILE = Path(__file__).with_name("eligibility.json")
ELIGIBILITY: dict[str, dict] = (json.loads(ELIGIBILITY_FILE.read_text())["tasks"]
                                if ELIGIBILITY_FILE.exists() else {})
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


def _faulted(r: dict) -> bool:
    return bool(r["load_error"] or r["setup_error"] or r["evaluator_error"] or r["faults"])


def grade(task: Task, answer: str, *, mode: str = "confirmatory", **sandbox_kw) -> dict:
    h = _HIDDEN[(task.family, task.id)]
    if task.family == "code":
        if mode == "confirmatory":
            e = ELIGIBILITY.get(task.id, {"status": "INELIGIBLE_CONFIRMATORY", "reason": "NOT_CLASSIFIED"})
            if e["status"] != "ELIGIBLE":       # excluded from confirmatory evidence, never silently graded
                return {"correct": None, "grade": "INELIGIBLE_CONFIRMATORY", "mode": mode,
                        "evidence": {"verifier": "executed:hidden-tests", "reason": e["reason"]}}
        names = h["visible"] + h["hidden"]
        r = code.run_tests(code.extract_code(answer, h["entry_point"]), h["test"], names, code_prompt=h["code_prompt"],
                           entry_point=h["entry_point"], mode=mode, **sandbox_kw)
        ok = all(r["per_test"][n] for n in h["hidden"])
        return {"correct": ok, "grade": "PASS" if ok else "ERROR" if _faulted(r) else "FAIL", "mode": mode, "evidence": {
            "verifier": "executed:hidden-tests:trusted-boundary", "hidden_passed": sum(r["per_test"][n] for n in h["hidden"]),
            "hidden_total": len(h["hidden"]), "visible_passed": sum(r["per_test"][n] for n in h["visible"]),
            "all_tests_pass": r["passed"] == len(names), **{k: r[k] for k in
            ("per_test", "load_error", "setup_error", "evaluator_error", "faults", "timeout", "exit", "isolation",
             "stderr_tail")}}}
    g, p = mathkey.gold(h["answer"]), mathkey.extract(answer)
    ok = mathkey.equivalent(g, p)
    return {"correct": ok, "grade": "PASS" if ok else "FAIL", "mode": mode, "evidence": {
        "verifier": "dataset_key:math-verify", "parsed": [str(x) for x in p], "parsable": bool(p)}}


def dataset_libs(tasks: list[Task]) -> frozenset:
    return frozenset(m for t in tasks for m in ast.literal_eval(_HIDDEN[("code", t.id)]["libs"]))


def classify_code_task(task: Task, libs_declared: frozenset = frozenset(), **sandbox_kw) -> dict:
    """Confirmatory eligibility: static rules (code.ineligibility), then the reference solution must pass every
    test (visible + hidden) behind the boundary in confirmatory mode. Either failing -> INELIGIBLE_CONFIRMATORY."""
    h = _HIDDEN[("code", task.id)]
    reason = code.ineligibility(ast.literal_eval(h["libs"]), h["test"], h["code_prompt"], libs_declared)
    if reason is None:
        names = h["visible"] + h["hidden"]
        r = code.run_tests(h["code_prompt"] + h["canonical_solution"], h["test"], names, code_prompt=h["code_prompt"],
                           entry_point=h["entry_point"], mode="confirmatory", **sandbox_kw)
        if r["passed"] != len(names):
            first = next(iter(r["faults"].values()), [None])[0]
            reason = "REFERENCE_FAILS_UNDER_BOUNDARY:" + (
                first or r["setup_error"] or r["load_error"] or r["evaluator_error"]
                or f"{len(names) - r['passed']}/{len(names)} tests fail")[:200]
    return {"status": "INELIGIBLE_CONFIRMATORY" if reason else "ELIGIBLE", "reason": reason}


def write_eligibility(path: Path = ELIGIBILITY_FILE, **sandbox_kw) -> dict:
    """Classify all BigCodeBench-Hard tasks and write the manifest confirmatory grading reads (ids only, no task text)."""
    import importlib.metadata as md
    all_tasks = load_bigcodebench_hard()
    declared = dataset_libs(all_tasks)
    tasks = {t.id: classify_code_task(t, declared, **sandbox_kw) for t in all_tasks}
    out = {"_note": "Generated by ogi_tasks.write_eligibility(); confirmatory grading accepts only ELIGIBLE ids. "
                    "Reasons are rule codes from code.ineligibility or the reference run behind the boundary.",
           "dataset_sha256": MANIFEST["bigcodebench-hard"]["sha256"],
           "grader_env": {"python": sys.version.split()[0],
                          "packages": sorted(f"{d.metadata['Name']}=={d.version}" for d in md.distributions())},
           "eligible": sum(v["status"] == "ELIGIBLE" for v in tasks.values()), "total": len(tasks), "tasks": tasks}
    path.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    ELIGIBILITY.clear()
    ELIGIBILITY.update(tasks)
    return out


def select_by_visible(task: Task, candidates: list[str], *, mode: str = "confirmatory", **sandbox_kw) -> int:
    """Index of the selected candidate; ties go to the earliest. Uses only what arms may see.
    code: most visible tests passed. math: plurality of math-verify equivalence classes (no key)."""
    if not candidates:
        raise ValueError("no candidates")
    if task.family == "code":
        names = [f"{c.name}.{f.name}" for c, f in code._methods(ast.parse(task.visible_checks))]
        prelude = _HIDDEN[("code", task.id)]["code_prompt"]   # public: the instruct prompt already shows it
        scores = [code.run_tests(code.extract_code(c), task.visible_checks, names, code_prompt=prelude, mode=mode,
                                 **sandbox_kw)["passed"] for c in candidates]
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
