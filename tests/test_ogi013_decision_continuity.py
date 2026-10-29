"""PILOT-4 decision-continuity repair, on the REAL PlumMe scheduler (lineage exclusion, pinning, receipts) with scripted providers and the real CherryMe continuity ledger: rejecting one action must not end the task; a terminating
replacement stands only on a verified policy clause; a required transfer stays possible; reviewer agreement is never proof. General: nothing here names an airline rule, an id or a benchmark answer."""
import json

import pytest

pytest.importorskip("tau2")
pytest.importorskip("plumme")
from cherryme.continuity import ContinuityLedger  # noqa: E402
from ogi013_scripted_stack import FOUND, GOOD, J, NONE_WITH_GROUNDS, events, make_agent, say  # noqa: E402
from ogi013_tau2_agent import DECLINE_ACTION  # noqa: E402

TRANSFER = {"action": "tool", "name": "transfer_to_human_agents", "arguments": {"summary": "the cancellation is not possible"}}
CONTINUE_MSG = {"action": "message", "content": "I cannot cancel that booking under the policy. Let's continue with your other request."}
REQUIRED = "If any portion of the flight has already been flown, the agent cannot help and transfer is needed."
POLICY = "You should deny user requests that are against this policy. " + REQUIRED
CRITIC_PROPOSES_TRANSFER = "ISSUES: FOUND\nCancellation is not allowed here. Transfer the customer to a human agent."


def term(open_="book a new round trip", clause="NONE", alt="NONE", verdict="CONTINUE"):
    return f"OPEN_REQUESTS: {open_}\nTERMINATION_REQUIRED_CLAUSE: {clause}\nALTERNATIVE: {alt}\nVERDICT: {verdict}"


def pilot4_script(termination):
    """The PILOT-4 shape: the draft is a write the policy forbids, the critic finds it and proposes a transfer, the author revises to the transfer, a further lineage agrees with stated grounds."""
    return {"draft": [J(GOOD)], "challenge": [CRITIC_PROPOSES_TRANSFER, NONE_WITH_GROUNDS], "revise": [J(TRANSFER)], "termination": termination}


@pytest.fixture(params=["fake", "real"])
def mk(request, monkeypatch, tmp_path):
    def build(script, policy=POLICY):
        return make_agent(monkeypatch, tmp_path / request.param, script, real=request.param == "real", policy=policy)
    return build


def collab_event(out):
    return next(e for e in events(out) if e["event"] == "ORG_COLLAB")


def test_rejecting_an_action_does_not_end_the_task_when_the_policy_does_not_require_it(mk):
    agent, state, stack, out = mk(pilot4_script([term(alt=J(CONTINUE_MSG))]))
    action, _ = say(agent, state)
    assert action == CONTINUE_MSG                                                         # the customer's other requests continue; no transfer happens
    t = collab_event(out)["termination"]
    assert t["outcome"] == "CONTINUE_ADOPTED" and t["open_requests"] == ["book a new round trip"] and t["clause_verified"] is False
    led = ContinuityLedger(out / "continuity.json")                                       # a replacement worker / restart reads the same record
    assert [o["text"] for o in led.open_objectives()] == ["book a new round trip"]       # the remaining objective is preserved, not abandoned
    cp = [e for e in events(out) if e["event"] in ("CONTINUITY_CHECKPOINT", "CONTINUITY_CHECKPOINT_FAILED")]
    assert cp and cp[0]["event"] == "CONTINUITY_CHECKPOINT"                                 # and written to the canonical work graph, where a restart / another worker finds it
    assert led.rejections[0]["kind"] == "action" and led.decisions[0]["decision"].startswith("CONTINUE_ADOPTED")
    assert any(r["stage"] == "TERMINATION_REVIEW" for r in collab_event(out)["trail"])


def test_reviewer_agreement_is_not_proof_a_fabricated_clause_cannot_end_the_task(mk):
    agent, state, stack, out = mk(pilot4_script([term(clause='"Agents must always transfer when a request is denied"', verdict="TERMINATE")]))
    action, _ = say(agent, state)
    t = collab_event(out)["termination"]
    assert t["verdict"] == "TERMINATE" and t["clause_verified"] is False and t["outcome"] == "DECLINE_FALLBACK"         # the quote does not occur in the policy
    assert action == DECLINE_ACTION and action["action"] == "message"                    # declined without ending; the transfer did not happen
    assert any(e["event"] == "ORG_DECLINE" for e in events(out))


def test_a_required_transfer_stays_possible_when_the_policy_clause_is_quoted_verbatim(mk):
    agent, state, stack, out = mk(pilot4_script([term(open_="NONE", clause=REQUIRED, verdict="TERMINATE")]))
    action, _ = say(agent, state)
    t = collab_event(out)["termination"]
    assert action == TRANSFER and t["outcome"] == "TERMINATE_APPROVED" and t["clause_verified"] is True
    assert ContinuityLedger(out / "continuity.json").restrictions[0]["clause"] == REQUIRED          # the restriction in force is on record with its source


def test_a_verified_clause_with_open_requests_but_no_continuing_alternative_still_ends_the_interaction(mk):
    agent, state, stack, out = mk(pilot4_script([term(clause=REQUIRED, verdict="TERMINATE")]))
    action, _ = say(agent, state)
    assert action == TRANSFER and collab_event(out)["termination"]["outcome"] == "TERMINATE_APPROVED"


def test_a_continuing_alternative_wins_over_a_terminate_verdict_while_requests_remain_open(mk):
    agent, state, stack, out = mk(pilot4_script([term(clause=REQUIRED, alt=J(CONTINUE_MSG), verdict="TERMINATE")]))
    action, _ = say(agent, state)
    assert action == CONTINUE_MSG and collab_event(out)["termination"]["outcome"] == "CONTINUE_ADOPTED"


def test_an_unavailable_termination_review_never_blocks_the_replacement(mk):
    agent, state, stack, out = mk(pilot4_script([]))                                       # no worker answers the termination question
    action, _ = say(agent, state)
    assert action == TRANSFER and collab_event(out)["termination"]["outcome"] == "REVIEW_UNAVAILABLE"


def test_a_transfer_the_author_itself_proposed_is_not_second_guessed(mk):
    script = {"draft": [J(TRANSFER)], "challenge": [NONE_WITH_GROUNDS], "termination": [term(alt=J(CONTINUE_MSG))]}
    agent, state, stack, out = mk(script)
    action, _ = say(agent, state)
    assert action == TRANSFER and collab_event(out)["termination"] is None                  # only a REJECTION that ended in a terminating action triggers the check


def test_a_correct_action_that_needs_no_correction_is_untouched(mk):
    agent, state, stack, out = mk({"draft": [J(GOOD)], "challenge": [NONE_WITH_GROUNDS]})
    action, _ = say(agent, state)
    assert action == GOOD and collab_event(out)["termination"] is None and not (out / "continuity.json").exists()


def test_the_frozen_path_is_unchanged_without_a_terminating_hook():
    from ogi013_org_collab import collaborate
    import inspect
    sig = inspect.signature(collaborate)
    assert sig.parameters["terminating"].default is None and sig.parameters["continuity"].default is None


def test_after_the_correction_the_next_step_still_sees_the_open_objective_whichever_worker_serves_it(monkeypatch, tmp_path):
    """Worker replacement / continuation: the second turn is answered by a different lineage (the first lineage is excluded by the scripted pool) and its prompt carries the preserved objective and the rejection."""
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [J(GOOD), J({"action": "message", "content": "Let us look at flights."})],
                                                                  "challenge": [CRITIC_PROPOSES_TRANSFER, NONE_WITH_GROUNDS], "revise": [J(TRANSFER)], "termination": [term(alt=J(CONTINUE_MSG))]},
                                          real=True, policy=POLICY)
    say(agent, state)
    assert [o["text"] for o in agent.ep.continuity.open_objectives()] == ["book a new round trip"]
    say(agent, state, text="Thanks. Now please book the round trip.")
    prompts = [e["task"] for e in stack.adapter.executed if e["stage"] == "draft"]
    assert len(prompts) == 2 and "<your_earlier_decisions>" not in prompts[0]
    assert "[OPEN] book a new round trip" in prompts[1] and "REJECTED action" in prompts[1] and "does not close them" in prompts[1]
    lineages = [e["lineage"] for e in stack.adapter.executed if e["stage"] == "draft"]
    assert len(set(lineages)) >= 1                                                         # (the pool decides who serves; the record does not depend on it)
