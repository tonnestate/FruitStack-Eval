"""Checks against the pinned local dataset copies (runners/ogi_tasks/datasets.json); skipped where the data is absent."""
import ast
import sys

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


@pytest.mark.skipif(not HAVE["bigcodebench-hard"], reason="BigCodeBench-Hard not present")
def test_real_code_canonical_passes_and_stub_fails():
    import pyarrow.parquet as pq
    rows = pq.read_table(T.DATA_DIR / T.MANIFEST["bigcodebench-hard"]["file"]).to_pylist()
    row = next(r for r in rows if set(ast.literal_eval(r["libs"])) <= set(sys.stdlib_module_names)
               and "faker" not in r["test"])
    t = T.make_task("code", row)
    assert T.grade(t, row["code_prompt"] + row["canonical_solution"])["correct"]
    assert not T.grade(t, "def task_func(*a, **k):\n    return None\n")["correct"]
