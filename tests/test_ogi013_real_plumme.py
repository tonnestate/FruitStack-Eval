"""The collaboration on the REAL PlumMe service and scheduler (PlumMe's own offline harness over a scripted provider adapter): lineage exclusion, author pinning and receipts are PlumMe's code.
No network, no inference."""
import json

import pytest

pytest.importorskip("tau2")
pytest.importorskip("plumme")
from ogi013_scripted_stack import FOUND, GOOD, BAD, J, NONE_WITH_GROUNDS, events, make_agent, say  # noqa: E402


def test_the_real_scheduler_keeps_reviewers_off_the_authors_lineage_and_pins_the_author_for_the_revision(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(GOOD)]}, real=True)
    action, _ = say(agent, state)
    ex = stack.adapter.executed
    assert action == GOOD and [e["stage"] for e in ex] == ["draft", "challenge", "revise", "challenge"]
    author, reviewer = ex[0]["lineage"], ex[1]["lineage"]
    assert reviewer != author and ex[2]["lineage"] == author and ex[3]["lineage"] != author        # PlumMe's own EXCLUDED_INDEPENDENCE_KEY gate and PINNED_MODEL
    steps = [e for e in events(out) if e["event"] == "STEP"]
    assert [s["independence_key"] for s in steps] == [e["lineage"] for e in ex] and steps[2]["prefer_met"] is True
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert [r["independence_key"] for r in receipts] == [e["lineage"] for e in ex] and all(r["success"] for r in receipts)      # the guard's ledger agrees with the episode
    collab = next(e for e in events(out) if e["event"] == "ORG_COLLAB")
    assert collab["improved"] and collab["independent_review"] and collab["final_reviewed"]


LONG = "Reasoning: " + "x" * 5200 + "\n" + J(GOOD)       # an answer far beyond the old 2048-token response cap (1 character = 1 token in the scripted provider)


def test_in_the_pilot_a_long_answer_is_delivered_whole_with_its_real_usage(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"long": LONG}], "challenge": [NONE_WITH_GROUNDS]}, real=True, budget=(50, 100000, 0.0))
    action, _ = say(agent, state)
    draft = stack.adapter.executed[0]
    assert action == GOOD and draft["max_output_tokens"] != 2048                       # no fixed output cap: PlumMe applied the route's own limit
    step = next(e for e in events(out) if e["event"] == "STEP" and e["tag"] == "draft")
    assert step["tokens_out"] >= len(LONG) and agent.ep.stats["unknown_steps"] == 0      # the whole answer arrived and its real usage is booked


def test_outside_the_pilot_the_frozen_behaviour_is_unchanged(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)], "challenge": [NONE_WITH_GROUNDS]}, real=True)
    say(agent, state)
    assert {e["max_output_tokens"] for e in stack.adapter.executed} == {2048}            # the frozen conditions keep 2048 per response and their reservation rule
    agent2, state2, stack2, _ = make_agent(monkeypatch, tmp_path / "long", {"draft": [{"long": LONG}]}, real=True)
    say(agent2, state2)
    receipts = [json.loads(line) for line in (tmp_path / "long/receipts.jsonl").read_text().splitlines()]
    assert receipts[0]["failure_class"] == "BUDGET_EXHAUSTED"                             # (there a long answer is still refused at the reservation - unchanged on purpose)


def test_a_step_that_cannot_afford_a_normal_answer_is_a_budget_stop_before_dispatch(monkeypatch, tmp_path):
    from peachme import PeachError
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 3000, 0.0))
    with pytest.raises(PeachError, match="BUDGET_HEADROOM_BELOW_MIN_ANSWER"):
        say(agent, state)
    assert stack.adapter.executed == [] and "BUDGET_STOP" in [e["event"] for e in events(out)]


# ---- no unintended paid dispatch: the REAL scheduler in AUTO (PLUMME_COST_POLICY=ANY from env.sh is ignored by this PlumMe) ------------------------------------------------

def _paid(models, paid):
    from plumme.models import CostClass
    return {"models": models, "costs": {m: CostClass.NORMAL for m in paid}}


def test_a_paid_only_world_gets_no_dispatch_at_all(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 100000, 0.0), real_kw=_paid(("paid-1",), ("paid-1",)))
    with pytest.raises(Exception):                                  # PlumMe: PAID_BUDGET_NOT_AUTHORIZED for every offer -> no route to lease
        say(agent, state)
    assert stack.adapter.executed == []                             # not one provider call, so no charge was possible


def test_with_free_and_paid_routes_only_free_ones_ever_execute(monkeypatch, tmp_path):
    kw = _paid(("alpha-1", "beta-1", "paid-1", "gamma-1", "paid-2"), ("paid-1", "paid-2"))
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(GOOD)]}, real=True, budget=(50, 100000, 0.0), real_kw=kw)
    action, _ = say(agent, state)
    assert action == GOOD and stack.adapter.executed and not [e for e in stack.adapter.executed if e["model_key"].startswith("paid")]
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert {r["cost_class"] for r in receipts} == {"FREE_TIER"}      # and the provider ledger the guard reads says the same


def test_the_simulator_cannot_reach_a_paid_route_either(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from ogi013_pilot_fixtures import ARMS, BUDGET, PILOT
    from tau2.user import user_simulator
    import ogi013_sim_supply as sim
    from ogi013_scripted_stack import real_plumme
    svc, adapter = real_plumme(tmp_path, {"draft": ["never sent"]}, **_paid(("paid-1",), ("paid-1",)))
    route_file = tmp_path / "pair.route"
    route_file.write_text(json.dumps({"model_key": "paid-1@default"}))
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "budget.json").write_text(json.dumps(BUDGET))
    for k, v in {"OGI013_PILOT_BUDGET": str(runs / "budget.json"), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs), "OGI013_PILOT_ARMS": ",".join(ARMS),
                 "OGI013_PILOT_ARM": ARMS[1], "OGI013_PILOT_START": "9999999999"}.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(user_simulator, "generate", user_simulator.generate)
    monkeypatch.setattr(sim.time, "sleep", lambda s: None)
    sim.install(svc, route_file, tmp_path / "out")
    with pytest.raises(RuntimeError, match="SIM_ROUTE_FAILED"):
        user_simulator.generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    assert adapter.executed == []


def test_no_agent_step_can_reserve_more_than_the_per_step_ceiling_whatever_the_route_claims(monkeypatch, tmp_path):
    from ogi013_pilot_fixtures import BUDGET
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    huge = agent.ep.output_budget("short prompt", {"output_limit": 1_000_000, "context_window": 2_000_000})
    assert huge[0] is None and huge[1] == BUDGET["max_tokens_per_step"]                         # a route that claims a million output tokens is still bounded by the owner's ceiling
    small = agent.ep.output_budget("short prompt", {"output_limit": 3000})
    assert small[1] == len("short prompt") + 3000                                              # a modest route limit sizes the reservation itself (input + the route's own answer limit)
    unknown_route = agent.ep.output_budget("short prompt", {})
    assert unknown_route[1] == BUDGET["max_tokens_per_step"]                                    # no published limit: still capped by budget facts, never unbounded
