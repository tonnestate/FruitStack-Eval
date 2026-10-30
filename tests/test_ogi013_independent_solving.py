"""Addendum 8: during independent solving a solver (and its helper) must not see the other solver's position; afterwards the shared state is complete."""
import sys
import time
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_code_task as ct  # noqa: E402
import ogi013_team_code as tc  # noqa: E402

DIFF1, TAIL1 = "+    return SECRET_SOLVER_ONE_FIX", "Ran 3 tests ... SECRET_SOLVER_ONE_TAIL"


def team(tmp_path, independent):
    t = tc.TeamState("goal", tmp_path / "team_state.md")
    t.pos = {"S1": SimpleNamespace(id="S1", model="m1", status="open", rev=0, diff=DIFF1, test_tail=TAIL1),
             "S2": SimpleNamespace(id="S2", model="m2", status="open", rev=0, diff="", test_tail="")}
    t.decisions.append("S1 produced its first gate-accepted diff (abc)")
    t.objection("S1", "L9", "an objection on S1")
    t.independent = independent
    return t


def captured_prompt(t, view):
    seen = []

    class Ep:
        def blocking(self): return None
        def event(self, kind, **k): pass
        def step(self, prompt, role, **k):
            seen.append(prompt)
            return {"success": True, "output": '{"action": "message", "content": "ISSUES: NONE"}', "model_key": "m", "independence_key": "m", "receipt_id": "r"}
    ctx = SimpleNamespace(ep=Ep(), deadline=time.monotonic() + 60, keys={}, gate=None, effects=None)
    ct.agent_loop(ctx, "critic", "head", SimpleNamespace(), set(), gated=False, team=t, view=view)
    return seen[0]


def test_p_solver_two_and_its_helper_never_see_solver_one(tmp_path):
    prompt = captured_prompt(team(tmp_path, True), "S2")              # solver 2's (and a helper's, view=S2) full prompt
    for leaked in (DIFF1, "SECRET_SOLVER_ONE_FIX", "SECRET_SOLVER_ONE_TAIL", "an objection on S1", "S1 produced"):
        assert leaked not in prompt
    assert "(withheld during independent solving)" in prompt


def test_q_after_solve_phase_challenger_sees_both(tmp_path):
    prompt = captured_prompt(team(tmp_path, False), None)
    assert DIFF1 in prompt and "S2 (model m2" in prompt and "an objection on S1" in prompt


def test_r_helper_never_from_a_solver_lineage_else_unavailable():
    events, seen = [], []
    ep = SimpleNamespace(event=lambda kind, **k: events.append(kind))
    positions = {"S1": SimpleNamespace(keys={"mistral"}), "S2": SimpleNamespace(keys={"qwen"})}
    p = positions["S1"]
    p.id = "S1"
    assert tc.help_guard(ep, positions, p, True, lambda excl: seen.append(excl) or "ok") == "ok" and set(seen[0]) == {"mistral", "qwen"}

    def none_eligible(excl):
        raise RuntimeError("NO_ELIGIBLE_NEURON")
    assert tc.help_guard(ep, positions, p, True, none_eligible) is None and events == ["HELP_UNAVAILABLE_INDEPENDENCE"]


def test_solver_similarity():
    a = "--- a\n+++ b\n+x\n+y\n-z\n"
    assert tc.solver_similarity([a, a]) == 1.0
    assert tc.solver_similarity([a, "+x\n+q\n"]) == round(1 / 4, 3)
    assert tc.solver_similarity([a]) is None
