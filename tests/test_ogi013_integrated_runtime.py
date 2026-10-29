"""Integrated runtime: the REAL FruitStackTau2Agent / Episode / FruitStackSession / SessionStore / BudgetGovernance / LineageHeart / collaborate() / Brother Mode, with scripted model providers only.
Task -> PlumMe-style model selection -> draft -> cooperation -> independent criticism -> revision -> renewed assessment -> specialist -> consolidation -> final action, and the resource controls around it.
Zero network, zero inference; synthetic customer task (proves mechanics and attribution, not benchmark outcomes)."""
import json

import pytest

pytest.importorskip("tau2")
pytest.importorskip("peachme")
pytest.importorskip("plumme")
pytest.importorskip("cherryme")
from ogi013_scripted_stack import BAD, FOUND, GOOD, J, NONE_WITH_GROUNDS, POOL, events, make_agent, route, say  # noqa: E402
from ogi013_tau2_agent import _action_digest  # noqa: E402
from peachme import PeachError  # noqa: E402

LINEAGES = {"draft": "L-alpha", "challenge": "L-beta", "specialist": "L-gamma", "rereview": "L-delta"}


def collab_event(out):
    found = [e for e in events(out) if e["event"] == "ORG_COLLAB"]
    assert len(found) == 1, [e["event"] for e in events(out)]
    return found[0]


# ---- 0. the collaboration path is the one that runs --------------------------------------------------------------------------------------------------------------

def test_the_collaboration_flag_selects_the_collaboration_path_not_the_legacy_one(monkeypatch, tmp_path):
    import ogi013_tau2_agent as mod

    def boom(*a, **k):
        raise AssertionError("legacy RG/2 FALSIFY path invoked")
    monkeypatch.setattr(mod.FruitStackTau2Agent, "_org_decide", boom)
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)], "challenge": [NONE_WITH_GROUNDS]})
    assert say(agent, state)[0] == GOOD and collab_event(out)["purpose"] == "consequential_effect"

    marker = {}
    monkeypatch.setattr(mod.FruitStackTau2Agent, "_org_decide", lambda self, ep, prompt, action, state, uncertain=False: marker.setdefault("legacy", action))
    monkeypatch.setattr(mod.FruitStackTau2Agent, "_org_collab", boom)
    agent2, state2, _, out2 = make_agent(monkeypatch, tmp_path / "b", {"draft": [J(GOOD)]}, collab=False)
    (tmp_path / "b").mkdir(exist_ok=True)
    assert say(agent2, state2)[0] == GOOD and marker["legacy"] == GOOD                    # without the flag the unchanged RG/2 path runs and the collaboration is never invoked


# ---- 1. a correct answer is independently assessed -----------------------------------------------------------------------------------------------------------------

def test_a_correct_answer_gets_a_grounded_assessment_by_another_lineage(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)], "challenge": [NONE_WITH_GROUNDS]})
    action, _ = say(agent, state)
    ex = stack.svc.executed
    assert action == GOOD and [e["stage"] for e in ex] == ["draft", "challenge"]            # one independent review, nothing else was asked
    assert ex[0]["lineage"] == "L-alpha" and ex[1]["lineage"] != ex[0]["lineage"]            # the reviewer is a different lineage than the author - at the PlumMe selection
    assert "state the specific checks" in ex[1]["task"] and J(GOOD) in ex[1]["task"] and "POLICY: refunds only within 24h." in ex[1]["task"]        # grounds are requested; the full materials are shown
    e = collab_event(out)
    assert e["validated"] and not e["improved"] and e["independent_review"] and e["final_reviewed"] and not e["ungrounded_agreement"]
    assert e["agreement"][0]["lineage"] == "L-beta" and "refund window" in e["agreement"][0]["grounds"] and e["agreement"][0]["agreed_with"] == _action_digest(GOOD)
    assert not [x for x in events(out) if x["event"] == "ORG_REVISION"]                        # an unchanged, validated answer is not a revision


def test_a_bare_agreement_is_recorded_but_does_not_count_as_validation(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": ["ISSUES: NONE"]})
    action, _ = say(agent, state)
    e = collab_event(out)
    assert action == BAD and e["ungrounded_agreement"] and not e["validated"] and e["agreement"][0]["grounds"] == "" and e["agreement"][0]["grounds_stated"] is False      # agreement on a WRONG answer is only a claim


# ---- 2/3. a wrong answer is corrected after criticism; the revision is challenged again; contributors are attributed -----------------------------------------------

def test_a_wrong_answer_is_criticised_revised_and_the_revision_examined_again(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(GOOD)]})
    action, _ = say(agent, state)
    ex = stack.svc.executed
    assert action == GOOD and [e["stage"] for e in ex] == ["draft", "challenge", "revise", "challenge"]
    assert "WRONG1" in ex[1]["task"] and "WRONG1" not in ex[3]["task"] and J(GOOD) in ex[3]["task"]        # the first review sees the draft, the second review sees the REVISION
    assert "Cancel HAT001" in ex[2]["task"]                                                    # the author is shown the criticism
    assert [e["lineage"] for e in ex] == ["L-alpha", "L-beta", "L-alpha", "L-beta"]            # reviewers never the author's lineage; the author revises with their own model
    steps = [e for e in events(out) if e["event"] == "STEP"]
    assert [s["independence_key"] for s in steps] == ["L-alpha", "L-beta", "L-alpha", "L-beta"] and steps[2]["prefer_met"] is True and all(s["model_key"] for s in steps)
    e = collab_event(out)
    assert e["improved"] and not e["validated"] and e["final_reviewed"] and e["independent_review"] and e["unresolved"] == []
    assert [t["stage"] for t in e["trail"]] == ["SOLUTION", "CRITIQUE", "REVISION", "CRITIQUE"]      # the draft, the criticism, the revision and the renewed review - in order, with their text
    assert J(BAD) in e["trail"][0]["text"] and "WRONG1" in e["trail"][1]["text"] and J(GOOD) in e["trail"][2]["text"]
    roles = {(a["role"], a["lineage"], a.get("found_issues"), a.get("materially_improved", a.get("changed_action"))) for a in e["attribution"]}
    assert ("critique", "L-beta", True, True) in roles and ("revision", "L-alpha", None, True) in roles and ("critique", "L-beta", False, False) in roles
    rev = [x for x in events(out) if x["event"] == "ORG_REVISION"]
    assert len(rev) == 1 and rev[0]["draft"] == _action_digest(BAD) and rev[0]["revised"] == _action_digest(GOOD) and e["draft"] == _action_digest(BAD) and e["final"] == _action_digest(GOOD)


# ---- 4. specialist disagreement: resolved or preserved --------------------------------------------------------------------------------------------------------------

def test_a_specialist_that_overrules_the_author_is_itself_reviewed_by_a_new_lineage(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(BAD) + " "], "specialist": [J(GOOD)]})
    action, _ = say(agent, state)
    ex = stack.svc.executed
    assert action == GOOD and [e["stage"] for e in ex] == ["draft", "challenge", "revise", "specialist", "challenge"]
    assert [e["lineage"] for e in ex] == ["L-alpha", "L-beta", "L-alpha", "L-gamma", "L-delta"]          # four distinct lineages; nobody reviews their own work
    e = collab_event(out)
    assert e["specialist"] and e["improved"] and e["final_reviewed"] and e["unresolved"] == []
    assert len(e["overruled"]) == 1 and e["overruled"][0]["author_position"] == _action_digest(BAD) and e["overruled"][0]["overruled_by"] == "gamma@x"
    assert len({t["lineage"] for t in e["trail"]}) == 4                                          # drafts, revisions, specialist and the renewed review are all attributable to a lineage


def test_disagreement_that_the_specialist_does_not_settle_stays_visible(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND], "revise": [J(BAD)], "specialist": [J(BAD)]})
    action, _ = say(agent, state)
    e = collab_event(out)
    assert action == BAD and not e["improved"] and not e["final_reviewed"] and len(e["unresolved"]) == 1 and "HAT001" in e["unresolved"][0]["objection"]      # the objection is not dropped
    assert not [x for x in events(out) if x["event"] == "ORG_REVISION"]                          # nothing improved, so nothing is reported as a revision
    pool_one_round = {"draft": [J(BAD)], "challenge": [FOUND, "ISSUES: FOUND\nHAT001 is a flight number, not a reservation id."], "revise": [J(BAD)], "specialist": [J(GOOD)]}
    agent2, state2, stack2, out2 = make_agent(monkeypatch, tmp_path / "b", pool_one_round)
    action2, _ = say(agent2, state2)
    e2 = collab_event(out2)
    assert action2 == GOOD and e2["changed"] and not e2["final_reviewed"] and any("flight number" in u["objection"] for u in e2["unresolved"])      # the re-review's objection to the specialist is kept


# ---- 5. failed models and unavailable reviewers ---------------------------------------------------------------------------------------------------------------------

def test_unavailable_reviewers_are_a_bounded_failed_review_never_agreement(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [{"fail": "RATE_LIMITED"}] * 40})
    action, _ = say(agent, state)
    e = collab_event(out)
    assert action == BAD and e["review_unavailable"] and not e["validated"] and not e["improved"] and not e["independent_review"] and e["agreement"] == []
    assert len(stack.svc.executed) <= 1 + 3 * 4 and e["failures"]                               # Brother Mode's loop guard (3 failed calls) x Episode.step's 4 attempts: bounded, no retry storm


def test_with_a_single_lineage_available_nobody_reviews_their_own_work(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [NONE_WITH_GROUNDS]}, routes=[route("alpha@x", "L-alpha")])
    action, _ = say(agent, state)
    e = collab_event(out)
    assert action == BAD and e["review_unavailable"] and [x["stage"] for x in stack.svc.executed] == ["draft"]          # no admissible reviewer lineage -> no review, not a self-review
    assert not e["independent_review"] and not e["validated"]


def test_an_uncertain_failure_stays_in_the_books_and_the_retries_are_bounded(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [{"timeout": True}] * 40}, budget=(100, 200000, 0.0))
    snap0 = stack.fs.governance.snapshot(agent.ep.sid)
    action, _ = say(agent, state)
    timeouts = [e for e in stack.svc.executed if e["stage"] == "challenge"]
    snap = stack.fs.governance.snapshot(agent.ep.sid)
    assert action == BAD and collab_event(out)["review_unavailable"] and 1 <= len(timeouts) <= 3 * 4          # Brother Mode's 3 failed calls x Episode.step's 4 attempts at most
    assert agent.ep.stats["unknown_steps"] == len(timeouts)                                                  # every possibly-billed attempt is on record as an unknown step ...
    assert snap0["tokens_remaining"] - snap["tokens_remaining"] >= 2048 * len(timeouts)                       # ... and keeps its reservation: uncertain billing never frees capacity


# ---- 9. unknown usage, failed authorization, budget exhaustion ------------------------------------------------------------------------------------------------------

def test_unknown_usage_is_charged_at_its_reservation_never_as_zero(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"nousage": J(GOOD)}], "challenge": [NONE_WITH_GROUNDS]}, budget=(50, 100000, 0.0))
    snap0 = stack.fs.governance.snapshot(agent.ep.sid)
    say(agent, state)
    snap = stack.fs.governance.snapshot(agent.ep.sid)
    known = 500                                                                                      # the challenge step reported 400+100
    used = snap0["tokens_remaining"] - snap["tokens_remaining"]
    assert used > known + 2000                                                                       # the step without usage kept its (>= 2048) reservation instead of counting as 0


def test_the_session_budget_stops_the_run_before_the_next_dispatch_and_keeps_the_evidence(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(GOOD)]}, budget=(2, 100000, 0.0))
    with pytest.raises(PeachError, match="SESSION_BUDGET_EXHAUSTED"):
        say(agent, state)
    assert [e["stage"] for e in stack.svc.executed] == ["draft", "challenge"]                        # the third dispatch (revise) was refused BEFORE it reached the provider
    kinds = [e["event"] for e in events(out)]
    assert kinds.count("STEP") == 2 and "BUDGET_STOP" in kinds and "ORG_ERROR" not in kinds and "ORG_COLLAB" not in kinds        # not swallowed as an error, no unreviewed action
    agent.stop()
    assert [e for e in events(out) if e["event"] == "EPISODE_CLOSED"][0]["reason"] == "BUDGET_STOP"      # the episode closes with its evidence and says why


def test_the_single_arm_is_governed_by_the_same_budget(monkeypatch, tmp_path):
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)] * 5}, mode="single", collab=False, budget=(2, 100000, 0.0))
    say(agent, state)
    say(agent, state)
    with pytest.raises(PeachError, match="SESSION_BUDGET_EXHAUSTED"):
        say(agent, state)
    assert len(stack.svc.executed) == 2
    free, state2, stack2, _ = make_agent(monkeypatch, tmp_path / "free", {"draft": [J(GOOD)]}, mode="single", collab=False)
    assert stack2.fs.governance.snapshot(free.ep.sid) is None                                         # outside the pilot nothing changes: the frozen single condition has no session budget


def test_a_paid_route_is_refused_before_dispatch_when_no_cash_is_authorised(monkeypatch, tmp_path):
    paid = [route("paid@x", "L-paid", cost_class="NORMAL", price=5.0)]
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, routes=paid, budget=(50, 100000, 0.0))
    with pytest.raises(PeachError, match="SESSION_BUDGET_EXHAUSTED"):
        say(agent, state)
    assert stack.svc.executed == []                                                                   # authorisation failed -> not a single provider call


def test_a_route_with_unknown_cost_class_is_refused_fail_closed(monkeypatch, tmp_path):
    unknown = route("mystery@x", "L-mystery")
    unknown.cost_class = None
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD)]}, routes=[unknown], budget=(50, 100000, 0.0))
    with pytest.raises(PeachError, match="BUDGET_RESERVATION_REQUIRED"):
        say(agent, state)
    assert stack.svc.executed == [] and "BUDGET_STOP" in [e["event"] for e in events(out)]


def test_the_pre_dispatch_gate_halts_the_collaboration_mid_way_and_preserves_everything(monkeypatch, tmp_path):
    import ogi013_pilot_gate as gate
    from ogi013_pilot_fixtures import BUDGET, PILOT, receipt, write_arm
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "budget.json").write_text(json.dumps(BUDGET))
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(BAD)], "challenge": [FOUND, NONE_WITH_GROUNDS], "revise": [J(GOOD)]})
    for k, v in {"OGI013_PILOT_BUDGET": str(runs / "budget.json"), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs),
                 "OGI013_PILOT_ARMS": "pilot-1/single,pilot-1/collab", "OGI013_PILOT_ARM": "pilot-1/collab", "OGI013_PILOT_START": "9999999999"}.items():
        monkeypatch.setenv(k, v)
    write_arm(runs, "pilot-1/collab", [receipt() for _ in range(BUDGET["arms"]["pilot-1/collab"]["max_dispatches"])])      # the provider-side ledger says this arm has used all its dispatches
    with pytest.raises(gate.PilotBudgetStop):
        say(agent, state)
    assert stack.svc.executed == [] and (runs / "PILOT_HALT").is_file() and "BUDGET_STOP" in [e["event"] for e in events(out)]


def test_the_real_stack_builds_the_lineage_heart_and_the_hooks_exist():
    import ast
    from pathlib import Path
    src = (Path(__file__).resolve().parents[1] / "runners/ogi013_tau2_agent.py").read_text()
    stack_init = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.ClassDef) and n.name == "Stack")
    assigns = [ast.unparse(n.value) for n in ast.walk(stack_init) if isinstance(n, ast.Assign) and any(ast.unparse(t) == "self.heart" for t in n.targets)]
    assert assigns == ["LineageHeart(self.svc)"]                                       # the live Stack must not fall back to the attribute-only PlumMeProvider


# ---- 10. the customer-simulator dispatch path (same pinned model, same accounting, same gate) ------------------------------------------------------------------------

def _install_sim(monkeypatch, tmp_path, script, model_key="sim@x", armed=True):
    from types import SimpleNamespace

    from ogi013_pilot_fixtures import ARMS, BUDGET, PILOT
    from ogi013_scripted_stack import ScriptedPlumMe
    from tau2.user import user_simulator

    import ogi013_sim_supply as sim
    svc = ScriptedPlumMe(script, routes=[route(model_key, "L-sim")])
    svc.store = SimpleNamespace(offers={})
    svc.scheduler = SimpleNamespace(screen=lambda req: ([], {}), availability=lambda o: {"retry_after_seconds": None, "circuit_open": False, "credential_available": True, "quota_exhausted": False})
    route_file = tmp_path / "pair.route"
    route_file.write_text(json.dumps({"model_key": model_key}))
    monkeypatch.setattr(user_simulator, "generate", user_simulator.generate)          # restored after the test
    monkeypatch.setattr(sim.time, "sleep", lambda s: None)
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "budget.json").write_text(json.dumps(BUDGET))
    if armed:
        for k, v in {"OGI013_PILOT_BUDGET": str(runs / "budget.json"), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs), "OGI013_PILOT_ARMS": ",".join(ARMS),
                     "OGI013_PILOT_ARM": ARMS[1], "OGI013_PILOT_START": "9999999999"}.items():
            monkeypatch.setenv(k, v)
    sim.install(svc, route_file, tmp_path / "out")
    return user_simulator.generate, svc, runs


def test_the_simulator_dispatches_through_the_same_pinned_model_and_is_logged(monkeypatch, tmp_path):
    from types import SimpleNamespace
    generate, svc, _ = _install_sim(monkeypatch, tmp_path, {"draft": ["I want to cancel HAT001."]})
    msg = generate("ignored", [SimpleNamespace(role="user", content="Hello, how can I help?")])
    row = json.loads((tmp_path / "out/sim-usage.jsonl").read_text().splitlines()[0])
    assert msg.content == "I want to cancel HAT001." and svc.executed[0]["model_key"] == "sim@x" and row["model_key"] == "sim@x" and row["success"] and row["receipt_id"].startswith("rcpt-")


def test_the_simulator_is_refused_before_dispatch_by_the_gate_and_is_not_retried(monkeypatch, tmp_path):
    import ogi013_pilot_gate as gate
    from types import SimpleNamespace
    from ogi013_pilot_fixtures import ARMS, BUDGET, receipt, write_arm
    generate, svc, runs = _install_sim(monkeypatch, tmp_path, {"draft": ["never sent"] * 5})
    write_arm(runs, ARMS[1], [receipt() for _ in range(BUDGET["arms"][ARMS[1]]["max_dispatches"])])
    with pytest.raises(gate.PilotBudgetStop):
        generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    assert svc.executed == [] and svc.requests == [] and (runs / "PILOT_HALT").is_file()           # not even a route was acquired; the stop was not turned into a retry loop


def test_a_rejected_simulator_route_fails_the_pair_without_a_retry_storm(monkeypatch, tmp_path):
    from types import SimpleNamespace
    generate, svc, _ = _install_sim(monkeypatch, tmp_path, {"draft": [{"fail": "RATE_LIMITED"}] * 60})
    with pytest.raises(RuntimeError, match="SIM_ROUTE_FAILED:RATE_LIMITED"):
        generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    assert len(svc.executed) == 1                                                                   # PlumMe says no recovery time is known -> the block fails now, registered, not 60 attempts
    exhausted = json.loads((tmp_path / "sim_exhausted.jsonl").read_text().splitlines()[0])         # the exhausted model is remembered (this write used to crash on a closed file)
    assert exhausted["model_key"] == "sim@x" and exhausted["cause"] == "RATE_LIMITED"


def test_the_groq_failure_sequence_never_sleeps_and_ends_the_attempt_at_once(monkeypatch, tmp_path):
    """The historical sequence: the pinned model answered once, then BILLING_OR_CREDIT_EXHAUSTED. Before: ~600 s waits. Now: the attempt ends on the spot, no sleep, no retry, evidence row without any window."""
    from types import SimpleNamespace
    generate, svc, _ = _install_sim(monkeypatch, tmp_path, {"draft": ["I want to cancel HAT001.", {"fail": "BILLING_OR_CREDIT_EXHAUSTED"}] + [{"fail": "BILLING_OR_CREDIT_EXHAUSTED"}] * 60})
    slept = []
    monkeypatch.setattr(__import__("time"), "sleep", lambda s: slept.append(s))
    generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    with pytest.raises(RuntimeError, match="SIM_ROUTE_FAILED:BILLING_OR_CREDIT_EXHAUSTED"):
        generate("ignored", [SimpleNamespace(role="user", content="And?")])
    assert slept == [] and len(svc.executed) == 2
    row = json.loads((tmp_path / "sim_exhausted.jsonl").read_text().splitlines()[0])
    assert row["cause"] == "BILLING_OR_CREDIT_EXHAUSTED" and "until" not in row


def test_in_the_pilot_the_simulator_gets_the_per_step_token_bound_and_zero_cash(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from ogi013_pilot_fixtures import ARMS, BUDGET, receipt, write_arm
    generate, svc, runs = _install_sim(monkeypatch, tmp_path, {"draft": ["I want to cancel HAT001."]})
    write_arm(runs, ARMS[1], [receipt(tin=10000, tout=0)])
    generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    assert svc.executed[0]["max_total_tokens"] == min(BUDGET["max_tokens_per_step"], BUDGET["arms"][ARMS[1]]["max_tokens"] - 10000)      # same bound as the agent steps, ledger-aware
    assert svc.requests[0].budget.max_cost_usd == 0.0                                                    # PlumMe admits no priced route for the simulator


def test_the_simulator_stops_before_dispatch_when_the_headroom_cannot_carry_a_reply(monkeypatch, tmp_path):
    import ogi013_pilot_gate as gate
    from types import SimpleNamespace
    from ogi013_pilot_fixtures import ARMS, BUDGET, receipt, write_arm
    generate, svc, runs = _install_sim(monkeypatch, tmp_path, {"draft": ["never sent"]})
    write_arm(runs, ARMS[1], [receipt(tin=BUDGET["arms"][ARMS[1]]["max_tokens"] - 4600, tout=0)])      # 4,600 left: the 4,000 reserve passes the gate, but no 512-token reply fits after a 4,100-byte prompt
    with pytest.raises(gate.PilotBudgetStop, match="cannot afford"):
        generate("ignored", [SimpleNamespace(role="user", content="x" * 4100)])
    assert svc.executed == [] and svc.requests == []


def test_outside_the_pilot_the_simulator_is_unchanged(monkeypatch, tmp_path):
    from types import SimpleNamespace
    generate, svc, _ = _install_sim(monkeypatch, tmp_path, {"draft": ["hi"]}, armed=False)
    generate("ignored", [SimpleNamespace(role="user", content="Hello")])
    assert svc.executed[0]["max_total_tokens"] is None and svc.requests[0].budget.max_cost_usd is None       # frozen conditions: no pilot limits


READ = {"action": "tool", "name": "get_reservation_details", "arguments": {"reservation_id": "HAT001"}}


def test_single_e_scope_writes_spends_the_extra_drafts_only_on_consequential_decisions(monkeypatch, tmp_path):
    monkeypatch.setenv("OGI013_SINGLE_E_K", "3")
    monkeypatch.setenv("OGI013_SINGLE_E_SCOPE", "writes")
    agent, state, stack, out = make_agent(monkeypatch, tmp_path / "a", {"draft": [J(READ)]}, mode="single_e", collab=False)
    assert say(agent, state)[0] == READ and len(stack.svc.executed) == 1                          # a read: one draft, no vote
    agent, state, stack, out = make_agent(monkeypatch, tmp_path / "b", {"draft": [J(GOOD), J(BAD), J(GOOD)]}, mode="single_e", collab=False)
    assert say(agent, state)[0] == GOOD and len(stack.svc.executed) == 3                          # a write: k independent drafts, majority
    assert [e["event"] for e in events(out)].count("SINGLE_E_VOTE") == 1
    monkeypatch.delenv("OGI013_SINGLE_E_SCOPE")
    agent, state, stack, out = make_agent(monkeypatch, tmp_path / "c", {"draft": [J(READ)] * 3}, mode="single_e", collab=False)
    say(agent, state)
    assert len(stack.svc.executed) == 3                                                           # the registered C3 behaviour (scope all) is unchanged
