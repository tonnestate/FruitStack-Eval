"""OGI task families: visible/hidden split, sandboxed executed grader, math-verify grader, uniform selector, leak guard."""
import dataclasses
import shutil

import pytest

pytest.importorskip("math_verify")
import ogi_tasks as T  # noqa: E402
from ogi_tasks import code, sandbox  # noqa: E402

N = 6
TEST_SRC = "import unittest\nclass TestCases(unittest.TestCase):\n" + "".join(
    f"    def test_case_{k}(self):\n        self.assertEqual(task_func({k}), {k * k})\n" for k in range(N))
SOLUTION = "```python\ndef task_func(x):\n    return x * x\n```"


def suite_src(n):
    return "import unittest\nclass TestCases(unittest.TestCase):\n" + "".join(
        f"    def test_case_{k}(self):\n        self.assertEqual(task_func({k}), {k * k})\n" for k in range(n))


@pytest.fixture(autouse=True)
def fixtures_eligible(monkeypatch):
    """Fixture tasks are not in eligibility.json; mark them ELIGIBLE so confirmatory grading (the default) runs."""
    for tid in ("Fixture/1", "Fixture/2", "Fixture/raises"):
        monkeypatch.setitem(T.ELIGIBILITY, tid, {"status": "ELIGIBLE", "reason": None})


def code_row(task_id="Fixture/1", test=TEST_SRC):
    return {"task_id": task_id, "instruct_prompt": "Write task_func(x) returning the square of x.", "test": test,
            "entry_point": "task_func", "canonical_solution": "    return x * x\n", "code_prompt": "def task_func(x):\n"}


def math_row(answer="\\frac{1}{2}", uid="test/algebra/1.json"):
    return {"unique_id": uid, "problem": "What is one divided by two?", "answer": answer, "level": 5,
            "solution": "Clearly it is $\\boxed{" + answer + "}$ by the secret method XYZZY."}


def only_for(ks):
    return f"def task_func(x):\n    return x * x if x in {sorted(ks)} else -1\n"


def ks(names):
    return {int(n.rsplit("_", 1)[1]) for n in names}


# ---- split ----
def test_split_is_deterministic_disjoint_and_complete():
    a, b = code.split_tests("Fixture/1", TEST_SRC), code.split_tests("Fixture/1", TEST_SRC)
    assert a["visible"] == b["visible"] and a["hidden"] == b["hidden"]
    assert len(a["visible"]) == N // 3 and len(a["hidden"]) == N - N // 3
    assert set(a["visible"]).isdisjoint(a["hidden"])
    assert set(a["visible"]) | set(a["hidden"]) == {f"TestCases.test_case_{k}" for k in range(N)}
    # the split depends on task id and method names only, not on test bodies
    body_changed = TEST_SRC.replace(str((N - 1) ** 2), "12345")
    assert code.split_tests("Fixture/1", body_changed)["visible"] == a["visible"]


def test_split_rejects_tasks_without_hidden_tests():
    with pytest.raises(ValueError):
        code.split_tests("x", "import unittest\nclass TestCases(unittest.TestCase):\n    def test_a(self): pass\n")


# ---- leak guard ----
def test_leak_guard_prompts_never_contain_hidden_tests_or_answers():
    ct, mt = T.make_task("code", code_row()), T.make_task("math", math_row())
    assert [f.name for f in dataclasses.fields(T.Task)] == ["id", "family", "prompt", "visible_checks"]
    h = T._HIDDEN[("code", ct.id)]
    for src in h["hidden_src"].values():
        assert src not in ct.prompt and src not in ct.visible_checks
    for name in h["hidden"]:
        assert name.split(".")[1] + "(" not in ct.prompt and name.split(".")[1] not in ct.visible_checks
    assert "XYZZY" not in mt.prompt and "\\boxed{\\frac{1}{2}}" not in mt.prompt and mt.visible_checks == ""
    # grader-only inputs do not influence what an arm sees
    hidden_k = ks(h["hidden"])
    mutated = TEST_SRC
    for k in hidden_k:
        mutated = mutated.replace(f"task_func({k}), {k * k})", f"task_func({k}), -999)")
    ct2 = T.make_task("code", {**code_row(test=mutated), "canonical_solution": "    return 0\n"})
    assert (ct2.prompt, ct2.visible_checks) == (ct.prompt, ct.visible_checks)
    mt2 = T.make_task("math", math_row(answer="42"))
    assert mt2.prompt == mt.prompt


# ---- code grader ----
needs_bwrap = pytest.mark.skipif(not shutil.which("bwrap"), reason="bwrap not installed")


def test_code_grader_uses_hidden_tests():
    t = T.make_task("code", code_row())
    h = T._HIDDEN[("code", t.id)]
    good = T.grade(t, SOLUTION)
    assert good["correct"] and good["evidence"]["all_tests_pass"] and good["evidence"]["hidden_passed"] == len(h["hidden"])
    overfit = T.grade(t, only_for(ks(h["visible"])))       # passes every visible test, fails hidden
    assert not overfit["correct"] and overfit["evidence"]["visible_passed"] == len(h["visible"])
    assert not T.grade(t, "this is not python")["correct"]


def test_code_grader_times_out_and_limits_memory():
    t = T.make_task("code", code_row("Fixture/2", suite_src(2)))
    slow = T.grade(t, "def task_func(x):\n    while True: pass\n", timeout=2)
    assert slow["evidence"]["timeout"] and not slow["correct"] and slow["grade"] == "ERROR"
    t = T.make_task("code", code_row())
    hog = T.grade(t, "b = bytearray(8 << 30)\ndef task_func(x):\n    return x * x\n", mem_mb=1024)
    assert not hog["correct"] and hog["evidence"]["load_error"] == "MemoryError"


@needs_bwrap
def test_sandbox_has_no_network_and_hides_root():
    r = sandbox.run_python({"a.py": "import socket, os, json\ns = socket.socket(); s.settimeout(2)\n"
                            "json.dump({'net': s.connect_ex(('1.1.1.1', 80)), 'data': os.path.exists("
                            f"{str(T.DATA_DIR)!r}), 'root': sorted(os.listdir('/root'))}}, open('o.json', 'w'))\n"},
                           ["a.py"])
    import json
    out = json.loads(r["outputs"]["o.json"])
    assert r["isolation"] == "bwrap-unshare-all-rlimit" and out["net"] != 0 and out["data"] is False


# ---- selector ----
def test_code_selector_uses_visible_tests_only_and_ties_go_earliest():
    t = T.make_task("code", code_row())
    h = T._HIDDEN[("code", t.id)]
    vis, hid = ks(h["visible"]), ks(h["hidden"])
    # candidate 0 passes all hidden but no visible test; candidate 1 passes the visible tests only
    assert T.select_by_visible(t, [only_for(hid), only_for(vis)]) == 1
    assert T.select_by_visible(t, [SOLUTION, only_for(vis)]) == 0          # tie on visible -> earliest
    assert T.select_by_visible(t, ["junk", "junk2"]) == 0


# ---- math ----
@pytest.mark.parametrize("answer,ok", [("so the answer is $\\boxed{0.5}$", True), ("\\boxed{\\dfrac12}", True),
                                       ("\\boxed{1/2}", True), ("\\boxed{2}", False), ("no idea", False)])
def test_math_grader_symbolic_equivalence(answer, ok):
    t = T.make_task("math", math_row())
    assert T.grade(t, answer)["correct"] is ok


def test_math_grader_radicals_and_sets():
    assert T.grade(T.make_task("math", math_row("2\\sqrt{2}", "m/2")), "\\boxed{\\sqrt{8}}")["correct"]
    assert T.grade(T.make_task("math", math_row("(-\\infty, 3)", "m/3")), "\\boxed{(-\\infty,3)}")["correct"]


def test_math_selector_plurality_ties_earliest():
    t = T.make_task("math", math_row())
    assert T.select_by_visible(t, ["\\boxed{3}", "\\boxed{0.5}", "\\boxed{1/2}", "\\boxed{3}", "\\boxed{\\frac12}"]) == 1
    assert T.select_by_visible(t, ["\\boxed{3}", "\\boxed{4}"]) == 0
    assert T.select_by_visible(t, ["nothing", "\\boxed{4}"]) == 1


def test_sandbox_fails_closed_without_bwrap(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.delenv("OGI_ALLOW_UNSANDBOXED", raising=False)
    with pytest.raises(RuntimeError, match="SANDBOX_UNAVAILABLE"):
        sandbox.run_python({"a.py": "print(1)"}, ["a.py"])
    t = T.make_task("code", code_row())
    with pytest.raises(RuntimeError, match="SANDBOX_UNAVAILABLE"):
        T.grade(t, SOLUTION, mode="dev")


def test_confirmatory_ignores_allow_unsandboxed_and_dev_rows_say_so(monkeypatch):
    t = T.make_task("code", code_row())
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setenv("OGI_ALLOW_UNSANDBOXED", "1")
    with pytest.raises(RuntimeError, match="SANDBOX_UNAVAILABLE: confirmatory"):
        T.grade(t, SOLUTION)
    with pytest.raises(ValueError, match="mode"):
        T.grade(t, SOLUTION, mode="lenient")
    dev = T.grade(t, SOLUTION, mode="dev")             # allowed, and the row is marked as dev
    assert dev["mode"] == "dev" and dev["correct"]


def test_ineligible_tasks_are_excluded_from_confirmatory_not_graded(monkeypatch):
    t = T.make_task("code", code_row("Fixture/unlisted"))
    r = T.grade(t, SOLUTION)
    assert r["correct"] is None and r["grade"] == "INELIGIBLE_CONFIRMATORY" and r["evidence"]["reason"] == "NOT_CLASSIFIED"
    monkeypatch.setitem(T.ELIGIBILITY, t.id, {"status": "INELIGIBLE_CONFIRMATORY", "reason": "IN_PROCESS_MOCK_PATCH"})
    assert T.grade(t, SOLUTION)["evidence"]["reason"] == "IN_PROCESS_MOCK_PATCH"
    assert T.grade(t, SOLUTION, mode="dev")["correct"] is True


@pytest.mark.parametrize("test_src,reason", [
    ("from unittest.mock import patch\nclass T(unittest.TestCase):\n    @patch('m.f')\n    def test_a(self, f): pass", "IN_PROCESS_MOCK_PATCH"),
    ("import os\nclass T(unittest.TestCase):\n    def test_a(self): os.makedirs('x')", "FILESYSTEM_SIDE_EFFECTS_INSPECTED_IN_PROCESS"),
    ("class T(unittest.TestCase):\n    def test_a(self):\n        with open('f') as f: pass", "FILESYSTEM_SIDE_EFFECTS_INSPECTED_IN_PROCESS"),
    ("import sys\nclass T(unittest.TestCase):\n    def test_a(self): sys.stdout.getvalue()", "IN_PROCESS_STREAM_CAPTURE"),
    ("from faker import Faker\nclass T(unittest.TestCase):\n    def test_a(self): pass", "UNDECLARED_TEST_DEPENDENCY:faker"),
    ("import zzz_not_installed\nclass T(unittest.TestCase):\n    def test_a(self): pass", "DEPENDENCY_UNAVAILABLE_IN_GRADER_ENV:zzz_not_installed"),
    ("class T(unittest.TestCase):\n    def test_a(self): self.assertEqual(task_func(2), 4)", None)])
def test_static_eligibility_rules(test_src, reason):
    assert code.ineligibility([], "import unittest\n" + test_src, "", frozenset({"zzz_not_installed"})
                              if "zzz" in test_src else frozenset()) == reason
