"""The collaboration on the REAL PlumMe service and scheduler (PlumMe's own offline harness over a scripted provider adapter): lineage exclusion, author pinning and receipts are PlumMe's code.
No network, no inference."""
import json

import pytest

pytest.importorskip("tau2")
pytest.importorskip("plumme")
from ogi013_scripted_stack import FOUND, GOOD, BAD, J, NONE_WITH_GROUNDS, events, make_agent, say  # noqa: E402


def _confirm_scripted_critique(agent):
    step = agent.ep.step

    def verify(prompt, stage, **kwargs):
        answer = step(prompt, stage, **kwargs)
        if stage == "challenge" and answer.get("success") and answer.get("output") in {FOUND, NONE_WITH_GROUNDS}:
            answer.update(verification="independently_confirmed", relevance_assessed=True, independent_confirmation=True)
        return answer

    agent.ep.step = verify  # deterministic verifier fixture; model text alone cannot promote a revision


def test_the_real_scheduler_keeps_reviewers_off_the_authors_lineage_and_pins_the_author_for_the_revision(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(GOOD)]}, real=True)
    _confirm_scripted_critique(agent)
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
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"long": LONG}], "challenge": [NONE_WITH_GROUNDS]}, real=True, real_kw={"route_output_limit": 8192}, budget=(50, 100000, 0.0))
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
    _confirm_scripted_critique(agent)
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
    for env in ({"output_limit": 1_000_000, "context_window": 2_000_000}, {"output_limit": 3000}, {}):
        assert agent.ep.output_budget("short prompt", env) == (None, BUDGET["max_tokens_per_step"])      # the authorization is the reservation whatever the route claims; no fixed output cap


def test_a_long_prompt_is_admitted_by_the_token_bound(monkeypatch, tmp_path):
    from ogi013_pilot_fixtures import BUDGET
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, real=True, budget=(50, 270000, 0.0))
    long_prompt = "x" * 30000                                                  # pilot-2 refused such a step (bytes bound 30,000 + 2,048 > 24,000)
    assert agent.ep.output_budget(long_prompt, {"output_limit": 20000}) == (None, BUDGET["max_tokens_per_step"])
    assert agent.ep.input_tokens(long_prompt, {})["bound"] + agent.ep.MIN_ANSWER_TOKENS <= BUDGET["max_tokens_per_step"]


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
        assert max_out is None and reserve <= BUDGET["max_tokens_per_step"] and est["bound"] + agent.ep.MIN_ANSWER_TOKENS <= reserve


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
    assert ok == (None, 24000)
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


def test_a_continuation_the_remaining_authorization_cannot_accommodate_is_refused_before_dispatch(monkeypatch, tmp_path):
    """The long answer does not fit what the step may still use: the first response is cut at the route's limit, the continuation is refused by the step's ParentBudget BEFORE dispatch - one request only."""
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"long": "Reasoning: " + "x" * 8500 + "\n" + J(GOOD)}]}, real=True, real_kw={"route_output_limit": 8192}, budget=(50, 9000, 0.0))
    try:
        say(agent, state)
    except Exception:                                                  # the exhausted session then refuses the next step: also fine, nothing more is sent
        pass
    assert len(stack.adapter.executed) == 1
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert receipts and all(((r.get("usage") or {}).get("total_tokens") or 0) <= 9000 + 400 for r in receipts)


def test_a_cut_off_answer_continues_inside_the_step_authorization_and_is_delivered_whole(monkeypatch, tmp_path):
    """The legitimate case: the route cuts the answer at its limit, PlumMe continues, every request is pre-checked against the step's 24,000 tokens, the whole answer arrives."""
    answer = "Reasoning: " + "x" * 15000 + "\n" + J(GOOD)
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"long": answer}], "challenge": [NONE_WITH_GROUNDS]}, real=True, real_kw={"context_window": 64000, "route_output_limit": 4096}, budget=(50, 100000, 0.0))
    action, _ = say(agent, state)
    step = next(e for e in events(out) if e["event"] == "STEP" and e["tag"] == "draft")
    assert action == GOOD and step["step_requests"] >= 2 and step["step_tokens_charged"] <= 24000        # several provider requests, one step, inside the authorization
    assert sum(1 for e in stack.adapter.executed if e["stage"] == "draft") == step["step_requests"]


# ---- the owner's per-step authorization across multi-request executions (continuations, retries) ------------------------------------------------------------------

def _long_answer_world(tmp_path, chars=50000):
    import asyncio

    from ogi013_scripted_stack import real_plumme
    from peachme.plumme import PlumMeProvider
    from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
    svc, adapter = real_plumme(tmp_path, {"draft": [{"long": "z" * chars}]}, tokens=(400, 100), context_window=64000, route_output_limit=7000)      # four allowed responses exceed the step ceiling without a parent budget
    prov = PlumMeProvider(svc)

    def execute(**kw):
        lease = asyncio.run(svc.acquire_neuron(NeuronRequest(consumer="t", objective="o", role_id="REASONING", cognitive_owner=CognitiveOwner.CONSUMER, selection_mode=SelectionMode.BEST,
                                                              required_skill_ids=[],
                                                              budget=BudgetEnvelope(max_concurrency=1, max_cost_usd=0.0),
                                                              allow_route_output_limit=True)))
        return asyncio.run(prov.execute(lease_id=lease.lease_id, task="question " * 20, max_cost_usd=0.0, **kw))
    return svc, adapter, execute


def _receipts(tmp_path):
    return [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]


def test_without_a_step_budget_a_multi_request_answer_silently_exceeds_the_step_ceiling(tmp_path):
    """Characterisation: this is the gap. One execution, several provider requests, aggregate usage far beyond 24,000, one receipt."""
    svc, adapter, execute = _long_answer_world(tmp_path)
    execute()
    receipts = _receipts(tmp_path)
    assert len(receipts) == 1 and receipts[0]["metadata"]["provider_attempt_count"] == len(adapter.executed) >= 4
    assert receipts[0]["usage"]["total_tokens"] > 24000


def test_a_step_budget_bounds_the_aggregate_tokens_of_all_requests_before_each_request(tmp_path):
    from ogi013_pilot_fixtures import ARMS, BUDGET, guard, write_arm
    from ogi013_pilot_gate import step_parent_budget
    svc, adapter, execute = _long_answer_world(tmp_path)
    arm_dir = tmp_path / "runs" / ARMS[1]
    arm_dir.mkdir(parents=True)
    with step_parent_budget(svc, 24000, 50, account_to=arm_dir, who="step-1") as parent:
        result = execute()
        parent.receipted = bool(result["success"])
    snap = parent.snapshot()
    receipts = _receipts(tmp_path)
    assert len(receipts) == 1 and receipts[0]["metadata"]["provider_attempt_count"] == len(adapter.executed) >= 2          # it did continue (several requests) ...
    assert 0 < snap["charged_tokens"] <= 24000                                                                              # ... but the AGGREGATE of the step stayed inside the authorization:
    assert snap["provider_attempt_count"] == len(adapter.executed) and svc.parent_budget is None                            # every request was reserved first against it, then the budget was released
    assert not receipts[0]["success"] and receipts[0]["failure_class"] == "BUDGET_EXHAUSTED"                                # the request that would have crossed it was refused before dispatch
    # the receipt of such a step carries no usage although earlier requests consumed tokens: the parent budget's record is written beside it and the guard charges it
    rows = [json.loads(line) for line in (arm_dir / "step-accounting.jsonl").read_text().splitlines()]
    assert rows == [dict(rows[0], who="step-1", requests=len(adapter.executed), charged_tokens=snap["charged_tokens"])]
    write_arm(tmp_path / "runs", ARMS[1], receipts)
    assert guard.usage(str(tmp_path / "runs"), [ARMS[1]], BUDGET["reserve_tokens_per_dispatch"])["tokens"] >= snap["charged_tokens"]      # never under-counted


def test_a_step_budget_bounds_the_number_of_provider_requests_and_the_guard_counts_them(tmp_path):
    from ogi013_pilot_fixtures import ARMS, BUDGET, guard, write_arm
    from ogi013_pilot_gate import step_parent_budget
    svc, adapter, execute = _long_answer_world(tmp_path)
    with step_parent_budget(svc, 1_000_000, 2) as parent:
        execute()
    assert len(adapter.executed) == 2 and parent.snapshot()["provider_attempt_count"] == 2                                  # the third request was refused BEFORE dispatch
    receipts = _receipts(tmp_path)
    assert len(receipts) == 1 and receipts[0]["metadata"]["provider_attempt_count"] == 2
    write_arm(tmp_path / "runs", ARMS[1], receipts)
    u = guard.usage(str(tmp_path / "runs"), [ARMS[1]], BUDGET["reserve_tokens_per_dispatch"])
    assert u["dispatches"] == 2                                                                                              # one receipt, two provider requests: both counted against the 180


def test_the_agent_step_runs_under_a_step_budget_and_reports_its_requests_and_tokens(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)], "challenge": [NONE_WITH_GROUNDS]}, real=True, budget=(50, 100000, 0.0))
    seen = []
    original = stack.svc.set_parent_budget
    stack.svc.set_parent_budget = lambda parent: (seen.append(parent), original(parent))[1]
    say(agent, state)
    bound = [p for p in seen if p is not None]
    steps = [e for e in events(out) if e["event"] == "STEP"]
    assert bound and all(b.max_total_tokens <= 24000 and b.max_cost_usd == 0.0 for b in bound) and stack.svc.parent_budget is None
    assert all(e["step_requests"] == 1 and e["step_tokens_charged"] == e["tokens_in"] + e["tokens_out"] for e in steps)       # per step: the requests and the charged tokens are on the record


def test_the_simulator_reply_also_runs_under_a_step_budget_in_the_pilot(monkeypatch, tmp_path):
    from types import SimpleNamespace

    from ogi013_pilot_fixtures import ARMS, BUDGET, PILOT
    from ogi013_scripted_stack import real_plumme
    from tau2.user import user_simulator

    import ogi013_sim_supply as sim
    svc, adapter = real_plumme(tmp_path, {"draft": ["I want to cancel HAT001."]}, models=("free-1",))
    route_file = tmp_path / "pair.route"
    route_file.write_text(json.dumps({"model_key": "free-1@default"}))
    runs = tmp_path / "runs"
    for a in ARMS:
        (runs / a / "fruitstack/plumme-state").mkdir(parents=True)
    (runs / "budget.json").write_text(json.dumps(BUDGET))
    for k, v in {"OGI013_PILOT_BUDGET": str(runs / "budget.json"), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs), "OGI013_PILOT_ARMS": ",".join(ARMS),
                 "OGI013_PILOT_ARM": ARMS[1], "OGI013_PILOT_START": "9999999999"}.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(user_simulator, "generate", user_simulator.generate)
    seen, original = [], svc.set_parent_budget
    svc.set_parent_budget = lambda parent: (seen.append(parent), original(parent))[1]
    sim.install(svc, route_file, tmp_path / "out")
    user_simulator.generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    bound = [p for p in seen if p is not None]
    assert len(bound) == 1 and bound[0].max_total_tokens <= BUDGET["max_tokens_per_step"] and bound[0].max_provider_calls == BUDGET["arms"][ARMS[1]]["max_dispatches"] and svc.parent_budget is None


def test_a_step_budget_stop_in_the_simulator_halts_instead_of_being_retried(monkeypatch, tmp_path):
    from types import SimpleNamespace

    from ogi013_pilot_gate import PilotBudgetStop
    from ogi013_scripted_stack import real_plumme
    from tau2.user import user_simulator

    import ogi013_sim_supply as sim
    svc, adapter = real_plumme(tmp_path, {"draft": ["hi"]}, models=("free-1",))
    route_file = tmp_path / "pair.route"
    route_file.write_text(json.dumps({"model_key": "free-1@default"}))
    monkeypatch.setattr(user_simulator, "generate", user_simulator.generate)
    monkeypatch.setattr(sim, "pilot_gate", lambda: None)
    monkeypatch.setattr(sim, "token_limits", lambda: {"headroom": 50000, "per_step": 24000, "calls": 0})          # no provider request left for this reply
    sim.install(svc, route_file, tmp_path / "out")
    with pytest.raises(PilotBudgetStop, match="no room for one more provider request"):
        user_simulator.generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    assert adapter.executed == []


# ---- step accounting without double charges ---------------------------------------------------------------------------------------------------------------------

def _accounting_case(tmp_path, *, new_receipts=(), charged=0, unknown=0, receipted=False, before=2):
    """A step on a PlumMe-shaped service: `before` receipts exist when it starts, `new_receipts` are written during it, the ParentBudget ends with `charged` recorded tokens."""
    from types import SimpleNamespace

    from ogi013_pilot_gate import step_parent_budget
    path = tmp_path / "receipts.jsonl"
    path.write_text("".join(json.dumps({"receipt_id": f"old{i}", "usage": {"total_tokens": 100}}) + "\n" for i in range(before)))
    svc = SimpleNamespace(parent_budget=None, scheduler=SimpleNamespace(receipts=SimpleNamespace(path=path)))
    svc.set_parent_budget = lambda parent: setattr(svc, "parent_budget", parent)
    arm = tmp_path / "arm"
    arm.mkdir()
    with step_parent_budget(svc, 24000, 50, account_to=arm, who="s") as parent:
        with path.open("a") as f:
            f.writelines(json.dumps(r) + "\n" for r in new_receipts)
        parent.charged_tokens, parent.unknown_usage_attempts, parent.provider_attempt_count = charged, unknown, 2
        parent.receipted = receipted
    rows = [json.loads(line) for line in (arm / "step-accounting.jsonl").read_text().splitlines()] if (arm / "step-accounting.jsonl").exists() else []
    return rows


def test_step_accounting_writes_nothing_for_a_step_whose_receipt_carries_its_usage(tmp_path):
    assert _accounting_case(tmp_path, new_receipts=[{"receipt_id": "r1", "usage": {"total_tokens": 7000}}], charged=7000, receipted=True) == []          # successful


def test_a_failed_receipt_with_recorded_usage_is_not_charged_twice(tmp_path):
    rows = _accounting_case(tmp_path, new_receipts=[{"receipt_id": "r1", "success": False, "usage": {"input_tokens": 5000, "output_tokens": 2000, "total_tokens": None}}], charged=7000)
    assert rows == []                                                                                                                                 # confirmed in the receipt: the guard counts it once, from the receipt


def test_a_rejected_request_consumed_nothing_and_adds_no_accounting(tmp_path):
    assert _accounting_case(tmp_path, new_receipts=[{"receipt_id": "r1", "success": False, "failure_class": "RATE_LIMITED", "usage": None}], charged=0) == []


def test_a_partially_metered_step_charges_only_what_its_receipts_do_not_carry(tmp_path):
    rows = _accounting_case(tmp_path, new_receipts=[{"receipt_id": "r1", "success": False, "usage": {"total_tokens": 5000}}, {"receipt_id": "r2", "success": False, "usage": None}], charged=8000)
    assert len(rows) == 1 and rows[0]["charged_tokens"] == 3000 and rows[0]["in_receipts"] == 5000 and rows[0]["receipt_ids"] == ["r1", "r2"]          # failover: r1 counted from its receipt, the 3,000 behind r2 from the ParentBudget
    rows = _accounting_case(tmp_path / "b", new_receipts=[{"receipt_id": "r1", "success": False, "usage": None}], charged=18768) if (tmp_path / "b").mkdir() is None else []
    assert rows[0]["charged_tokens"] == 18768                                                                                                         # the continuation case: nothing in the receipt, all of it is charged


def test_unreported_usage_stays_conservative_and_the_guard_totals_each_source_once(tmp_path):
    from ogi013_pilot_fixtures import ARMS, BUDGET, guard, write_arm
    rows = _accounting_case(tmp_path, new_receipts=[{"receipt_id": "r1", "success": False, "usage": None}], charged=0, unknown=1)
    assert len(rows) == 1 and rows[0]["unknown_usage_attempts"] == 1
    runs = tmp_path / "runs"
    write_arm(runs, ARMS[1], [])
    (runs / ARMS[1] / "step-accounting.jsonl").write_text(json.dumps({"charged_tokens": 3000, "unknown_usage_attempts": 1}) + "\n")
    assert guard.usage(str(runs), [ARMS[1]], BUDGET["reserve_tokens_per_dispatch"])["tokens"] == 3000 + BUDGET["reserve_tokens_per_dispatch"]
