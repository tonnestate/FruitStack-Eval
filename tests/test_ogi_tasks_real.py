"""Checks against the pinned local dataset copies (runners/ogi_tasks/datasets.json); skipped where the data is absent."""
import shutil

import pytest

pytest.importorskip("math_verify")
import ogi_tasks as T  # noqa: E402

HAVE = {k: (T.DATA_DIR / T.MANIFEST[k]["file"]).exists() for k in ("bigcodebench-hard", "math-500")}


@pytest.mark.skipif(not HAVE["bigcodebench-hard"] or not HAVE["math-500"], reason="pinned datasets not present")
def test_real_tasks_split_and_never_leak():
    ct, mt = T.load_bigcodebench_hard(), T.load_math_level5()
    assert len(ct) == T.MANIFEST["bigcodebench-hard"]["rows"] and len(mt) == T.MANIFEST["math-500"]["level5_rows"]
    for t in ct:
        h = T._HIDDEN[("code", t.id)]
        assert h["visible"] and h["hidden"]
        for src in h["hidden_src"].values():
            assert src not in t.prompt
        assert h["canonical_solution"].strip() not in t.prompt
    for t in mt:
        h = T._HIDDEN[("math", t.id)]
        assert h["solution"] not in t.prompt and "\\boxed{" + h["answer"] + "}" not in t.prompt


@pytest.mark.skipif(not HAVE["math-500"], reason="MATH-500 not present")
def test_real_math_keys_and_reference_solutions_grade_correct():
    for t in T.load_math_level5():
        h = T._HIDDEN[("math", t.id)]
        assert T.grade(t, h["solution"])["correct"], t.id
        assert not T.grade(t, "\\boxed{\\text{zebra}}")["correct"], t.id


@pytest.mark.skipif(not HAVE["bigcodebench-hard"] or not shutil.which("bwrap"), reason="needs BCB-Hard and bwrap")
def test_real_code_eligible_references_pass_behind_the_boundary_and_stubs_fail():
    assert T.ELIGIBILITY_FILE.exists()
    import json
    manifest = json.loads(T.ELIGIBILITY_FILE.read_text())
    assert manifest["dataset_sha256"] == T.MANIFEST["bigcodebench-hard"]["sha256"]
    tasks = {t.id: t for t in T.load_bigcodebench_hard()}
    assert set(manifest["tasks"]) == set(tasks)
    for tid in ("BigCodeBench/287", "BigCodeBench/313", "BigCodeBench/826"):          # undeclared faker
        assert manifest["tasks"][tid]["reason"] == "UNDECLARED_TEST_DEPENDENCY:faker"
    eligible = [tasks[i] for i, v in manifest["tasks"].items() if v["status"] == "ELIGIBLE"]
    assert len(eligible) == manifest["eligible"] > 0
    for t in eligible:
        h = T._HIDDEN[("code", t.id)]
        assert T.grade(t, h["code_prompt"] + h["canonical_solution"])["grade"] == "PASS", t.id
        assert T.grade(t, "def task_func(*a, **k):\n    return None\n")["grade"] in ("FAIL", "ERROR"), t.id
    ineligible = next(t for i, t in tasks.items() if manifest["tasks"][i]["status"] != "ELIGIBLE")
    assert T.grade(ineligible, "whatever")["grade"] == "INELIGIBLE_CONFIRMATORY"
