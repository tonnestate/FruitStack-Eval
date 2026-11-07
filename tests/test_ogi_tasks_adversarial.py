"""Adversarial candidates against the trusted grading boundary (runners/ogi_tasks/boundary.py).

Every hostile candidate here must grade FAIL or ERROR, never PASS. Where a cheat would *succeed* if a leak
existed, the candidate is written to return the right answer exactly when the leak works, so a FAIL proves
the leak is closed rather than just that the candidate was wrong.
"""
import hashlib
import shutil
from pathlib import Path

import pytest

pytest.importorskip("math_verify")
import ogi_tasks as T  # noqa: E402

pytestmark = pytest.mark.skipif(not shutil.which("bwrap"), reason="confirmatory grading needs bwrap")

SECRET = "SECRET" + "-7f3a"          # appears in the hidden test source only (assembled so this file is no hit)
TESTS = ("import unittest\nclass TestCases(unittest.TestCase):\n"
         "    def test_a(self):\n        self.assertEqual(task_func(3), 9, 'SECRET-7f3a')\n"
         "    def test_b(self):\n        self.assertEqual(task_func(4), 16, 'SECRET-7f3a')\n")
RAISES = ("import unittest\nclass TestCases(unittest.TestCase):\n"
          "    def test_a(self):\n        with self.assertRaises(Exception):\n            task_func(-1)\n"
          "    def test_b(self):\n        with self.assertRaises(Exception):\n            task_func(-2)\n")
RUNNERS = Path(T.__file__).parent


@pytest.fixture(autouse=True)
def eligible(monkeypatch):
    for tid in ("Adv/1", "Adv/raises"):
        monkeypatch.setitem(T.ELIGIBILITY, tid, {"status": "ELIGIBLE", "reason": None})


def task(test=TESTS, tid="Adv/1"):
    return T.make_task("code", {"task_id": tid, "instruct_prompt": "square", "test": test, "entry_point": "task_func",
                                "canonical_solution": "    return x * x\n", "code_prompt": "def task_func(x):\n"})


def assert_not_pass(r):
    assert r["correct"] is False and r["grade"] in ("FAIL", "ERROR"), (r["grade"], r["evidence"].get("faults"))
    return r


def test_honest_candidate_still_passes():          # control: the boundary does not break correct code
    assert T.grade(task(), "def task_func(x):\n    print('noise'); return x * x\n")["grade"] == "PASS"
    assert T.grade(task(RAISES, "Adv/raises"), "def task_func(x):\n    raise ValueError('neg')\n")["grade"] == "PASS"


def test_forged_results_and_verdict_files_are_ignored():
    forge = ("import json\nV = json.dumps({'TestCases.test_a': True, 'TestCases.test_b': True, 'correct': True,"
             " 'grade': 'PASS', 'passed': 2})\n"
             "for n in ('results.json', 'verdict.json', 'result.json', '/tmp/results.json'):\n"
             "    try: open(n, 'w').write(V)\n    except OSError: pass\n"
             "def task_func(x):\n    open('results.json', 'w').write(V)\n    return -1\n")
    assert_not_pass(T.grade(task(), forge))


def test_monkeypatching_unittest_assert_and_exit_has_no_effect():
    patch = ("import unittest, sys, builtins\n"
             "unittest.TestCase.assertEqual = lambda *a, **k: None\n"
             "unittest.TestCase.run = lambda self, result=None: None\n"
             "unittest.TestResult.wasSuccessful = lambda self: True\n"
             "builtins.AssertionError = type('Nope', (Exception,), {})\n"
             "sys.exit = lambda *a: None\n"
             "def task_func(x):\n    return -1\n")
    assert_not_pass(T.grade(task(), patch))


@pytest.mark.parametrize("src", [
    "import os\nos._exit(0)\ndef task_func(x):\n    return x * x\n",            # exits before it can be called
    "import os\ndef task_func(x):\n    os._exit(0)\n",
    "import sys\ndef task_func(x):\n    sys.exit(0)\n",
    "import sys\nsys.exit(0)\n",
    "import os, signal\ndef task_func(x):\n    os.kill(os.getpid(), signal.SIGKILL)\n"])
def test_early_termination_is_error(src):
    assert_not_pass(T.grade(task(), src))


def test_sleeping_past_the_timeout_is_error_even_if_the_value_would_be_right():
    r = assert_not_pass(T.grade(task(), "import time\ndef task_func(x):\n    time.sleep(60)\n    return x * x\n",
                                timeout=2))
    assert r["grade"] == "ERROR" and r["evidence"]["timeout"]


@pytest.mark.parametrize("payload", [
    b"not json\n", b"[1, 2]\n", b'{"ok": {"$": "evil", "v": 1}}\n', b'{"ok": {"$": "set", "v": [[1]]}}\n',
    b'{"ok": 9, "extra": 1}\n', b'{"ok": 9', b'{"raise": "SystemExit", "msg": "0"}\n'])
def test_malformed_or_missing_channel_output_is_error(payload):
    # the channel is the server's dup of fd 1 (fd 3); the candidate writes raw bytes onto it, then dies
    src = f"import os\ndef task_func(x):\n    os.write(3, {payload!r})\n    os._exit(0)\n"
    assert_not_pass(T.grade(task(), src))


def test_channel_injection_before_ready_and_closed_channel():
    assert_not_pass(T.grade(task(), "import os\nos.write(3, b'{\"ok\": 9}\\n{\"ok\": 16}\\n')\n"
                                    "def task_func(x):\n    return -1\n"))
    assert_not_pass(T.grade(task(), "import os\nos.close(3)\ndef task_func(x):\n    return x * x\n"))


def test_hidden_tests_answer_registry_and_data_dir_are_unreachable():
    leak = (f"import os\nDATA, RUNNERS, SECRET = {str(T.DATA_DIR)!r}, {str(RUNNERS)!r}, ('SECRET' + '-7f3a').encode()\n"
            "def leaked():\n"
            "    if os.path.exists(DATA) or os.path.exists(RUNNERS):\n        return True\n"
            "    paths = [f'/proc/{p}/{k}' for p in os.listdir('/proc') if p.isdigit() for k in ('cmdline', 'environ')]\n"
            "    paths += [f'/proc/{p}/fd/{fd}' for p in os.listdir('/proc') if p.isdigit()\n"
            "              for fd in (os.listdir(f'/proc/{p}/fd') if os.access(f'/proc/{p}/fd', os.R_OK) else [])]\n"
            "    for root in ('/tmp', '/dev/shm', '/var/tmp'):\n"
            "        paths += [os.path.join(dp, f) for dp, dn, fn in os.walk(root) for f in fn\n"
            "                  if not dp.startswith(os.getcwd())]\n"
            "    for p in paths:\n"
            "        try:\n            if os.path.isfile(p) and SECRET in open(p, 'rb').read(1 << 20): return True\n"
            "        except OSError: pass\n"
            "    return False\n"
            "def task_func(x):\n    return x * x if leaked() else -1\n")
    assert_not_pass(T.grade(task(), leak, timeout=30))


def test_test_files_and_grader_sources_cannot_be_tampered():
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in RUNNERS.glob("*.py")}
    tamper = (f"import os\nRUNNERS, SECRET = {str(RUNNERS)!r}, ('SECRET' + '-7f3a').encode()\n"
              "for n in ('tests.py', 'selection.json', 'harness.py'):\n    open(n, 'w').write('pass')\n"
              "for p in [os.path.join(RUNNERS, f) for f in ('boundary.py', 'code.py', '__init__.py')] + ['/tmp/tests.py']:\n"
              "    try: open(p, 'w').write('raise SystemExit')\n    except OSError: pass\n"
              "for dp, dn, fn in os.walk('/tmp'):\n"
              "    for f in fn:\n"
              "        try:\n            if SECRET in open(os.path.join(dp, f), 'rb').read():\n"
              "                open(os.path.join(dp, f), 'w').write('')\n"
              "        except OSError: pass\n"
              "def task_func(x):\n    return -1\n")
    assert_not_pass(T.grade(task(), tamper))
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in RUNNERS.glob("*.py")} == before
    assert T.grade(task(), "def task_func(x):\n    return x * x\n")["grade"] == "PASS"


@pytest.mark.parametrize("src", [
    "class Always:\n    def __eq__(self, o): return True\n    def __ne__(self, o): return False\n"
    "    __hash__ = object.__hash__\ndef task_func(x):\n    return Always()\n",
    "class I(int):\n    def __eq__(self, o): return True\n    __hash__ = int.__hash__\n"
    "def task_func(x):\n    return I(0)\n",
    "class S(str):\n    def __eq__(self, o): return True\n    __hash__ = str.__hash__\n"
    "def task_func(x):\n    return [S('a')]\n",
    "import unittest\ndef task_func(x):\n    raise unittest.SkipTest('skip me')\n",
    "def task_func(x):\n    raise SystemExit(0)\n"])
def test_proxy_spoofing_objects_and_exception_names_never_pass(src):
    assert_not_pass(T.grade(task(), src))


@pytest.mark.parametrize("src", [
    "import os\ndef task_func(x):\n    if x < 0: os._exit(1)\n    return x * x\n",
    "import time\ndef task_func(x):\n    if x < 0: time.sleep(60)\n    return x * x\n"])
def test_a_crash_or_hang_never_satisfies_assertRaises(src):
    assert_not_pass(T.grade(task(RAISES, "Adv/raises"), src, timeout=2))


def test_math_grading_never_executes_the_answer(tmp_path):
    flag = tmp_path / "pwned"
    m = T.make_task("math", {"unique_id": "m/x", "problem": "1+1?", "answer": "2", "level": 5, "solution": "2"})
    for a in (f"\\boxed{{__import__('os').system('touch {flag}')}}", f"__import__('os').system('touch {flag}') 7"):
        assert T.grade(m, a)["correct"] is False
    assert not flag.exists()
