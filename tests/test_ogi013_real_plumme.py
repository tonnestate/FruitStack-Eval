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
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 2000, 0.0))
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


def test_the_simulator_executes_on_a_free_route_under_the_real_lease_budget_check(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from ogi013_pilot_fixtures import ARMS, BUDGET, PILOT
    from tau2.user import user_simulator
    import ogi013_sim_supply as sim
    from ogi013_scripted_stack import real_plumme
    svc, adapter = real_plumme(tmp_path, {"draft": ["I want to cancel HAT001."]}, **_paid(("free-1",), ()))
    route_file = tmp_path / "pair.route"
    route_file.write_text(json.dumps({"model_key": "free-1@default"}))
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "budget.json").write_text(json.dumps(BUDGET))
    for k, v in {"OGI013_PILOT_BUDGET": str(runs / "budget.json"), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs), "OGI013_PILOT_ARMS": ",".join(ARMS),
                 "OGI013_PILOT_ARM": ARMS[1], "OGI013_PILOT_START": "9999999999"}.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(user_simulator, "generate", user_simulator.generate)
    monkeypatch.setattr(sim.time, "sleep", lambda s: None)
    sim.install(svc, route_file, tmp_path / "out")
    user_simulator.generate("ignored", [SimpleNamespace(role="user", content="Hello")])      # regression: execute must not widen the lease's zero-cash budget (LEASE_BUDGET_EXPANSION in the first live pilot)
    assert len(adapter.executed) == 1


def test_no_agent_step_can_reserve_more_than_the_per_step_ceiling_whatever_the_route_claims(monkeypatch, tmp_path):
    from ogi013_pilot_fixtures import BUDGET
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    inp = agent.ep.input_tokens("short prompt", {})["bound"]
    huge = agent.ep.output_budget("short prompt", {"output_limit": 1_000_000, "context_window": 2_000_000})
    assert huge[1] == BUDGET["max_tokens_per_step"] and huge[0] == huge[1] - inp               # a route that claims a million output tokens is still bounded by the owner's ceiling; the cap IS the reserved room
    small = agent.ep.output_budget("short prompt", {"output_limit": 3000})
    assert small == (3000, inp + 3000)                                                          # a modest route limit sizes the reservation itself (input + the route's own answer limit)
    unknown_route = agent.ep.output_budget("short prompt", {})
    assert unknown_route[1] == BUDGET["max_tokens_per_step"]                                    # no published limit: still capped by budget facts, never unbounded


def test_a_long_prompt_is_admitted_by_the_token_bound(monkeypatch, tmp_path):
    from ogi013_pilot_fixtures import BUDGET
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    long_prompt = "x" * 30000                                                  # pilot-2 refused such a step (bytes bound 30,000 + 2,048 > 24,000)
    max_out, reserve = agent.ep.output_budget(long_prompt, {"output_limit": 20000})
    inp = agent.ep.input_tokens(long_prompt, {})["bound"]
    assert reserve == BUDGET["max_tokens_per_step"] and max_out == reserve - inp and max_out >= agent.ep.MIN_ANSWER_TOKENS


def test_a_step_whose_recorded_tokens_exceed_the_ceiling_stops_the_pilot(monkeypatch, tmp_path):
    from peachme import PeachError
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0), tokens_per_call=(30000, 100))     # the provider records more than the 24,000 per-step ceiling
    with pytest.raises(PeachError, match="BUDGET_STEP_CEILING_EXCEEDED"):
        say(agent, state)
    assert "BUDGET_STOP" in [e["event"] for e in events(out)]


TEXTS = {
    "english conversation": "Customer: I would like to change my flight to next Tuesday please. Agent: Certainly, let me look that up. " * 300,
    "chinese": "我想把我的航班改到下周二，请帮我查一下可用的座位和价格。" * 400,
    "arabic": "أريد تغيير رحلتي إلى يوم الثلاثاء القادم من فضلك وتأكيد السعر." * 300,
    "cyrillic": "Я хотел бы изменить свой рейс на следующий вторник, пожалуйста." * 300,
    "emoji": "✈️🧳🎫 " * 1500,
    "json": json.dumps([{"reservation_id": f"R{i:05d}", "passengers": [{"first_name": "Ethan", "dob": "1990-01-01"}], "flights": [{"origin": "JFK", "destination": "SFO", "date": "2024-05-20"}]} for i in range(250)]),
}


@pytest.mark.parametrize("name", sorted(TEXTS))
def test_the_input_bound_is_the_larger_of_plummes_estimate_and_a_real_tokenizer_and_sizes_the_reserved_output(monkeypatch, tmp_path, name):
    from ogi013_pilot_fixtures import BUDGET
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    est = agent.ep.input_tokens(TEXTS[name], {"model_id": "gemini-3.1-flash-lite"})
    assert est["counted"] is not None and est["tokenizer"]                                      # litellm's local tokenizer is available in the pilot interpreter
    assert est["bound"] == max(est["plumme"], est["counted"]) and est["bound"] >= est["plumme"]
    try:
        max_out, reserve = agent.ep.output_budget(TEXTS[name], {"model_id": "gemini-3.1-flash-lite", "output_limit": 8192})
    except Exception as exc:                                                                    # a prompt that leaves no room under the approved ceiling is the only refusal
        assert "BUDGET_HEADROOM_BELOW_MIN_ANSWER" in str(exc) and est["bound"] + agent.ep.MIN_ANSWER_TOKENS > BUDGET["max_tokens_per_step"]
    else:
        assert reserve <= BUDGET["max_tokens_per_step"] and max_out == min(8192, reserve - est["bound"]) and est["bound"] + max_out <= reserve


def test_scripts_with_many_tokens_per_character_are_counted_not_guessed(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    cjk = agent.ep.input_tokens(TEXTS["chinese"], {})
    assert cjk["counted"] > cjk["plumme"] and cjk["bound"] == cjk["counted"]                  # PlumMe's chars/3 UNDER-counts CJK; the real tokenizer governs there
    eng = agent.ep.input_tokens(TEXTS["english conversation"], {})
    assert eng["bound"] == eng["plumme"] and eng["counted"] < eng["plumme"]                    # and for English the (larger) PlumMe estimate governs: no legitimate request is refused on a loose multiplier


def test_a_long_multilingual_prompt_that_really_exceeds_the_ceiling_is_refused_and_a_shorter_one_is_not(monkeypatch, tmp_path):
    from peachme import PeachError
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    ok = agent.ep.output_budget(TEXTS["chinese"][:3000], {"output_limit": 8192})
    assert ok[0] and ok[1] <= 24000
    with pytest.raises(PeachError, match="BUDGET_HEADROOM_BELOW_MIN_ANSWER"):
        agent.ep.output_budget(TEXTS["chinese"] * 6, {"output_limit": 8192})                    # ~60k tokens of CJK: cannot fit one step under 24,000


def test_the_input_counted_is_the_provider_facing_input_including_the_system_skill_text(monkeypatch, tmp_path):
    from plumme.scheduler import SwarmScheduler
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    say(agent, state)
    sent = stack.adapter.executed[0]["task"]                                                    # what the provider adapter received: system + user message contents
    step = next(e for e in events(out) if e["event"] == "STEP" and e["tag"] == "draft")
    est = step["input_estimate"]
    assert "BASE_REASONING_SKILL" in sent and est["plumme"] > SwarmScheduler.estimate_input_tokens([{"content": sent.split("\n", 1)[1]}])     # the system text is part of it
    assert abs(est["plumme"] - SwarmScheduler.estimate_input_tokens([{"content": sent}])) <= 1  # and it is the very number PlumMe computed from the messages it sent


def test_plumme_enforces_max_total_tokens_before_dispatch_against_its_own_estimate_plus_the_stated_output_cap(tmp_path):
    """How PlumMe enforces the reservation (characterisation of the real BudgetLedger): refused BEFORE the provider when its input estimate (chars/3 of system + task) plus the caller's max_output_tokens
    exceeds max_total_tokens; the TRUE token count is not known to it, which is why the caller states the cap and counts with a real tokenizer."""
    import asyncio

    from ogi013_scripted_stack import real_plumme
    from peachme.plumme import PlumMeProvider
    from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
    from plumme.scheduler import SwarmScheduler
    svc, adapter = real_plumme(tmp_path, {"draft": ["ok", "ok"]})
    prov = PlumMeProvider(svc)

    def run(task, delta, out=None):
        lease = asyncio.run(svc.acquire_neuron(NeuronRequest(consumer="t", objective="o", role_id="REASONING", cognitive_owner=CognitiveOwner.CONSUMER, selection_mode=SelectionMode.BEST,
                                                              required_skill_ids=[], budget=BudgetEnvelope(max_concurrency=1, max_cost_usd=0.0))))
        system = svc.skills.execution_instructions_for_skills(lease.role_id, list(lease.effective_skill_ids))          # exactly what the scheduler sends
        est = SwarmScheduler.estimate_input_tokens([{"content": system}, {"content": task}])
        return asyncio.run(prov.execute(lease_id=lease.lease_id, task=task, max_total_tokens=est + delta, max_output_tokens=out, max_cost_usd=0.0))
    refused = run("y" * 3000, -1)
    assert refused["success"] is False and refused["failure_class"] == "BUDGET_EXHAUSTED" and adapter.executed == []                      # input alone over the reservation: nothing sent
    assert run("y" * 3000, 50, out=51)["failure_class"] == "BUDGET_EXHAUSTED" and adapter.executed == []                                  # input + stated output cap over it: nothing sent
    ok = run("y" * 3000, 50, out=50)
    assert ok["success"] and len(adapter.executed) == 1 and adapter.executed[0]["max_output_tokens"] == 50                              # exactly the room fits


def test_a_continuation_that_would_pass_the_reservation_is_refused_by_the_ledger_before_dispatch(monkeypatch, tmp_path):
    """The long answer does not fit the reserved room: PlumMe's ledger refuses the continuation (input so far + the stated cap > reservation) - one dispatch only, nothing beyond the reservation."""
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"long": "Reasoning: " + "x" * 8500 + "\n" + J(GOOD)}]}, real=True, budget=(50, 9000, 0.0))
    try:
        say(agent, state)
    except Exception:                                                  # the exhausted session then refuses the next step: also fine, nothing more is sent
        pass
    assert len(stack.adapter.executed) == 1
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert receipts and all(((r.get("usage") or {}).get("total_tokens") or 0) <= 9000 + 400 for r in receipts)     # (the scripted provider adds 400 input tokens per call)
