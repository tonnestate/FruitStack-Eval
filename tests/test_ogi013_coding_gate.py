"""Tests for the OGI-013 coding-driver submit gate (synthetic Django-shaped repository; no network, no models)."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
from ogi013_coding_gate import NO_DIFF, NO_TEST, CodingGate, GateError  # noqa: E402

RAN_OK = "test_x (forms_tests.tests.test_media.T) ... ok\n\nRan 3 tests in 0.01s\n\nOK\n"
RAN_FAIL = "test_x (forms_tests.tests.test_media.T) ... FAIL\n\nRan 3 tests in 0.01s\n\nFAILED (failures=1)\n"
RAN_ZERO = "\nRan 0 tests in 0.000s\n\nOK\n"


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture()
def repo(tmp_path):
    ws = tmp_path / "ws"
    (ws / "django/forms").mkdir(parents=True)
    (ws / "django/utils").mkdir(parents=True)
    (ws / "tests/forms_tests/tests").mkdir(parents=True)
    (ws / "tests/utils_tests").mkdir(parents=True)
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return a + b\n")
    (ws / "django/utils/text.py").write_text("X = 1\n")
    (ws / "tests/forms_tests/tests/test_media.py").write_text("from django.forms import widgets\n")
    (ws / "tests/utils_tests/test_text.py").write_text("from django.utils import text\n")
    (ws / "tests/runtests.py").write_text("")
    git(ws, "init", "-q")
    git(ws, "-c", "user.email=a@b", "-c", "user.name=t", "add", "-A")
    git(ws, "-c", "user.email=a@b", "-c", "user.name=t", "commit", "-qm", "base")
    return ws, git(ws, "rev-parse", "HEAD"), tmp_path / "out"


RUN = ["python", "tests/runtests.py", "--parallel", "1", "forms_tests.tests.test_media"]


def test_rejects_submit_without_diff(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    g.record_test_run(RUN, 0, RAN_OK)
    d = g.check_submit()
    assert not d.accepted and d.reason == NO_DIFF and d.diff_sha256 is None


def test_rejects_whitespace_only_and_test_only_changes(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return a + b\n\n\n")
    (ws / "tests/forms_tests/tests/test_media.py").write_text("from django.forms import widgets\nassert True\n")
    g.record_edit("django/forms/widgets.py")
    g.record_test_run(RUN, 0, RAN_OK)
    assert g.check_submit().reason == NO_DIFF


def test_rejects_diff_without_test_run_and_stale_test_run(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    g.record_test_run(RUN, 0, RAN_OK)                       # tested BEFORE editing: stale
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return list(dict.fromkeys(a + b))\n")
    g.record_edit("django/forms/widgets.py")
    d = g.check_submit()
    assert not d.accepted and d.reason == NO_TEST and "django/forms/widgets.py" in d.changed_source_files


def test_rejects_irrelevant_or_empty_test_run(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return b + a\n")
    g.record_edit(str(ws / "django/forms/widgets.py"))
    g.record_test_run(["python", "tests/runtests.py", "utils_tests.test_text"], 0, RAN_OK)   # does not touch django.forms
    g.record_test_run(RUN, 0, RAN_ZERO)                                                      # zero tests executed
    assert g.check_submit().reason == NO_TEST


def test_accepts_failing_but_relevant_run_and_new_files(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    (ws / "django/forms/helpers.py").write_text("def order(x):\n    return x\n")                # new, untracked file
    g.record_edit("django/forms/helpers.py")
    g.record_test_run(RUN, 1, RAN_FAIL)                    # a failing relevant run still counts as evidence
    d = g.check_submit()
    assert d.accepted and "django/forms/helpers.py" in d.diff and d.diff_sha256
    assert git(ws, "status", "--porcelain") == "?? django/forms/helpers.py"   # agent's index untouched


def test_whole_suite_run_counts(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return b + a\n")
    g.record_edit("django/forms/widgets.py")
    g.record_test_run("python tests/runtests.py --parallel 1", 0, RAN_OK)
    assert g.check_submit().accepted


def test_p0_snapshot_immutable_and_required_for_review(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    with pytest.raises(GateError):
        g.review_target()                                    # no Brother Mode review without P0
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return b + a\n")
    g.record_edit("django/forms/widgets.py")
    g.record_test_run(RUN, 1, RAN_FAIL)
    d0 = g.check_submit()
    p0 = g.snapshot("P0", d0)
    assert g.review_target() == p0.read_text() == d0.diff
    with pytest.raises(GateError):
        g.snapshot("P0", d0)                                 # immutable
    # revision after criticism -> P1, P0 unchanged
    (ws / "django/forms/widgets.py").write_text("def merge(a, b):\n    return list(dict.fromkeys(b + a))\n")
    g.record_edit("django/forms/widgets.py")
    assert not g.check_submit().accepted                     # revision must be tested again
    g.record_test_run(RUN, 0, RAN_OK)
    d1 = g.check_submit()
    g.snapshot("P1", d1)
    assert (out / "P0.diff").read_text() == d0.diff and (out / "P1.diff").read_text() == d1.diff and d0.diff != d1.diff
    with pytest.raises(GateError):
        g.snapshot("P2", g._decide(False, NO_TEST, "", ()))  # rejected submissions are never frozen


def test_no_patch_outcome_is_logged(repo):
    ws, base, out = repo
    g = CodingGate(ws, base, out)
    rec = g.outcome_without_patch("max_requests=110")
    assert rec["outcome"] == "NO_PATCH"
    assert '"NO_PATCH"' in (out / "gate.jsonl").read_text()
