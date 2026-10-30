"""AMENDMENT-DRIVER-2 tests: R3 syntax guard, transcript visibility of the latest run_tests, R1 sticky author (fake episode, no models)."""
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_code_task as ct  # noqa: E402


def test_syntax_guard_reverts_and_names_error_only(tmp_path):
    (tmp_path / "django").mkdir()
    f = tmp_path / "django" / "m.py"
    f.write_text("if True:\n    x = 1\n")
    sb = ct.Sandbox(tmp_path, sys.executable)
    with pytest.raises(ValueError, match=r"EDIT_REJECTED: (IndentationError|SyntaxError) at line \d+"):
        sb.edit_file("django/m.py", "    x = 1\n", "")
    assert f.read_text() == "if True:\n    x = 1\n"
    assert "OK" in sb.edit_file("django/m.py", "x = 1", "x = 2")


def test_latest_run_tests_stays_full():
    long = "x" * 2500
    t = [{"role": "call", "text": "run_tests({})"}, {"role": "result", "text": long}]
    t += [e for _ in range(4) for e in ({"role": "call", "text": "read_file({})"}, {"role": "result", "text": "y" * 2500})]
    out = ct.render(t)
    assert long in out and "y" * 2500 not in out.split(long)[0]          # older read result cut, latest run_tests full


def test_author_prefers_its_first_model_and_handover_is_logged():
    seq = iter(["m1", "m1", "m2"])
    calls, events = [], []

    class Ep:
        def blocking(self): return None
        def event(self, kind, **k): events.append((kind, k))
        def step(self, prompt, role, *, exclude=(), prefer=None, sticky_attempts=1):
            calls.append((prefer, sticky_attempts))
            m = next(seq)
            return {"success": True, "output": '{"action": "tool", "name": "list_dir", "arguments": {}}', "model_key": m, "independence_key": m, "receipt_id": "r"}

    class SB:
        def list_dir(self, path="."): return "x"
    ctx = SimpleNamespace(ep=Ep(), deadline=time.monotonic() + 60, keys={"author": set()}, gate=None, effects=None)
    ct.pomelo_call = lambda *a, **k: ("x", False)
    ct.agent_loop(ctx, "author", "h", SB(), {"list_dir"}, gated=False, limit=3)
    assert [c[0] for c in calls] == [None, "m1", "m1"] and all(c[1] == 2 for c in calls)
    assert [k["to_model"] for kind, k in events if kind == "ROLE_HANDOVER"] == ["m2"]


def test_no_progress_guard_stops_after_eight_idle_turns():
    events = []

    class Ep:
        def blocking(self): return None
        def event(self, kind, **k): events.append(kind)
        def step(self, prompt, role, *, exclude=(), prefer=None, sticky_attempts=1):
            return {"success": True, "output": '{"action": "tool", "name": "list_dir", "arguments": {"path": "."}}', "model_key": "m", "independence_key": "m", "receipt_id": "r"}

    class SB:
        def list_dir(self, path="."): return "x"
    ctx = SimpleNamespace(ep=Ep(), deadline=time.monotonic() + 60, keys={}, gate=None, effects=None)
    ct.pomelo_call = lambda *a, **k: ("x", False)
    out, _ = ct.agent_loop(ctx, "critic", "h", SB(), {"list_dir"}, gated=False)
    assert out == "STOP:NO_PROGRESS" and "LOOP_GUARD" in events      # the same read repeated is not progress (only the first one is novel)


def _session(actions, gated, outputs=None):
    """Drives agent_loop with a scripted model and fake tools; returns (result, events)."""
    events, it = [], iter(actions)

    class Ep:
        def blocking(self): return None
        def event(self, kind, **k): events.append((kind, k))
        def step(self, prompt, role, *, exclude=(), prefer=None, sticky_attempts=1):
            return {"success": True, "output": next(it), "model_key": "m", "independence_key": "m", "receipt_id": "r"}

    class Gate:
        def record_edit(self, p): pass
        def record_test_run(self, *a): return {"tests_executed": 1}
        def check_submit(self): raise AssertionError
        def _source_diff(self): return ("", False, ())

    class SB:
        last_run = last_py = None
        def edit_file(self, **k): return "OK"
        def read_file(self, **k): return "x"
        def run_tests(self, modules):
            self.last_run = (["python", "t.py"] + modules, 1, next(outputs))
            return "r"
    ctx = SimpleNamespace(ep=Ep(), deadline=time.monotonic() + 60, keys={}, gate=Gate(), effects=None)
    ct.pomelo_call = lambda ep, sb, eff, name, args, write: (getattr(sb, name)(**args), False)
    res, _ = ct.agent_loop(ctx, "author" if gated else "critic", "h", SB(), {"edit_file", "read_file", "run_tests"}, gated=gated)
    return res, events


def _tool(name, **args):
    import json
    return json.dumps({"action": "tool", "name": name, "arguments": args})


def test_author_edits_alone_are_not_progress():
    res, ev = _session([_tool("edit_file", path="a.py", old="x", new="y")] * 8, True)
    assert res == "STOP:NO_PROGRESS" and not any(k == "PROGRESS" for k, _ in ev)


def test_author_progress_only_when_visible_tests_strictly_better():
    good = "a (m.T) ... ok\nb (m.T) ... FAIL\n"
    better = "a (m.T) ... ok\nb (m.T) ... ok\n"
    worse = "a (m.T) ... FAIL\nb (m.T) ... ok\n"
    seq = [_tool("run_tests", modules=["m"])] * 3 + [_tool("edit_file", path="a.py", old="x", new="y")] * 8
    res, ev = _session(seq, True, iter([good, better, worse]))
    assert [k["label"] for n, k in ev if n == "PROGRESS"] == ["visible_tests_better", "visible_tests_better"]   # `worse` regresses a passing test: not progress
    assert res == "STOP:NO_PROGRESS"


def test_reader_progress_limited_to_exploration_allowance():
    seq = [_tool("read_file", path=f"f{i}.py") for i in range(12 + 8)]
    res, ev = _session(seq, False)
    assert res == "STOP:NO_PROGRESS" and sum(1 for n, _ in ev if n == "PROGRESS") == ct.EXPLORATION_ALLOWANCE


def test_grounded_text():
    sess = {"cmd_keys": ["admin_views.tests"], "reads": {"django/forms/widgets.py"}}
    assert ct.grounded_text("ran admin_views.tests: 2 failures", sess)
    assert ct.grounded_text("bug at django/forms/widgets.py:120", sess)
    assert not ct.grounded_text("this looks wrong to me", sess)
    assert not ct.grounded_text("see django/forms/other.py:5", sess)


def test_tolerant_code_action_parser():
    assert ct.parse_code_action('{"action": "read_file", "name": "read_file", "arguments": {"path": "a.py"}}') == {"action": "tool", "name": "read_file", "arguments": {"path": "a.py"}}
    assert ct.parse_code_action('```json\n{"action": "edit_file", "path": "a.py", "old": "x", "new": "y"}\n```')["arguments"] == {"path": "a.py", "old": "x", "new": "y"}
    assert ct.parse_code_action('{"action": "tool", "name": "submit", "arguments": {}}')["name"] == "submit"
    assert ct.parse_code_action('{"action": "launch_missiles"}') is None
