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
