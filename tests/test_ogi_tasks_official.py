"""Official BigCodeBench semantics (owner decision D2 2026-11-09): candidate + tests in one sandboxed interpreter, verdict via a
nonce line written with primitives captured before candidate code runs, static tamper audit. Mutation targets: a forged verdict,
an import-time exit, a patched unittest, and a wrong answer must never PASS."""
import shutil

import pytest

import ogi_tasks as T  # noqa: E402
from ogi_tasks import code  # noqa: E402

pytestmark = pytest.mark.skipif(not shutil.which("bwrap"), reason="confirmatory grading requires bwrap")

TESTS = ("import unittest\nfrom unittest.mock import patch\n"
         "class TestCases(unittest.TestCase):\n"
         "    def test_a(self):\n        self.assertEqual(task_func(2), 4)\n"
         "    def test_b(self):\n        self.assertEqual(task_func(3), 6)\n"
         "    def test_c(self):\n"
         "        with patch('builtins.len', return_value=7):\n            self.assertEqual(task_func(5), 10)\n")


def task():
    return T.make_task("code", {"task_id": "Fixture/official", "instruct_prompt": "double", "test": TESTS, "entry_point": "task_func",
                                "canonical_solution": "    return x * 2\n", "code_prompt": "def task_func(x):\n", "libs": "[]"})


@pytest.mark.parametrize("answer,expected", [
    ("def task_func(x):\n    return x * 2\n", "PASS"),                                      # in-process mock.patch works (boundary could not)
    ("def task_func(x):\n    return x + 2\n", "FAIL"),
    ("print('\\nOGI-VERDICT-00:{\"per_test\": {}}')\ndef task_func(x):\n    return 0\n", "FAIL"),   # forged verdict without the nonce
    ("raise SystemExit(0)\n", "TAMPER"),                                                    # the audit catches it; the runtime guard is tested below
])
def test_official_verdicts(answer, expected):
    r = T.grade(task(), answer, mode="dev", semantics="official")
    assert r["grade"] == expected, r["evidence"]


def test_patching_the_test_machinery_is_tamper_not_pass():
    cheat = "import unittest\nunittest.TestCase.assertEqual = lambda *a, **k: None\ndef task_func(x):\n    return 0\n"
    r = T.grade(task(), cheat, mode="dev", semantics="official")
    assert r["grade"] == "TAMPER" and r["correct"] is False and "unittest" in r["evidence"]["tamper_audit"]


def test_audit_flags_module_monkeypatch_and_frame_access():
    assert "MODULE_ATTRIBUTE_ASSIGNED:json" in code.tamper_audit("import json\njson.dumps = str\n")
    assert "_getframe" in code.tamper_audit("import sys\nf = sys._getframe(1)\n")
    assert code.tamper_audit("import numpy as np\ndef task_func(x):\n    return np.array(x) * 2\n") == []


def test_runtime_guard_without_the_audit_an_import_time_exit_fails_every_test():
    names = ["TestCases.test_a", "TestCases.test_b"]
    r = code.run_tests_official("raise SystemExit(0)\n", TESTS, names, mode="dev")
    assert r["passed"] == 0 and r["load_error"].startswith("SystemExit")      # the runner survives the exit and still reports every test failed


def test_a_hanging_candidate_fails_within_the_per_test_timeout():
    import time
    t0 = time.monotonic()
    r = T.grade(task(), "def task_func(x):\n    while True: pass\n", mode="dev", semantics="official", timeout=2)
    assert r["correct"] is False and time.monotonic() - t0 < 30
