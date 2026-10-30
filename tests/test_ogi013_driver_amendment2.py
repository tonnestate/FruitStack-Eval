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
    ct.LIMITS["author"] = 3
    ct.pomelo_call = lambda *a, **k: ("x", False)
    ct.agent_loop(ctx, "author", "h", SB(), {"list_dir"}, gated=False)
    assert [c[0] for c in calls] == [None, "m1", "m1"] and all(c[1] == 2 for c in calls)
    assert [k["to_model"] for kind, k in events if kind == "ROLE_HANDOVER"] == ["m2"]
