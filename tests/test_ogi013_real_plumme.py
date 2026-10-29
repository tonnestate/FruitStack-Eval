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


def test_characterization_an_answer_longer_than_the_step_reservation_is_refused_not_truncated(monkeypatch, tmp_path):
    """OPEN POINT (documented, not yet repaired): the agent reserves prompt bytes + 2048 tokens per step and PlumMe stops the continuation of a longer answer at that reservation.
    The answer is not silently cut: the dispatch fails BUDGET_EXHAUSTED, PeachMe holds the receipt, the step becomes UNKNOWN and is abandoned. Long reasoning answers therefore fail in both arms."""
    long_answer = "Reasoning: " + "x" * 5200 + "\n" + J(GOOD)
    agent, state, stack, out = make_agent(monkeypatch, tmp_path, {"draft": [{"long": long_answer}]}, real=True, budget=(50, 100000, 0.0))
    action, _ = say(agent, state)
    receipts = [json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()]
    assert receipts[0]["failure_class"] == "BUDGET_EXHAUSTED" and action["action"] == "message"
    assert agent.ep.stats["unknown_steps"] >= 1 and stack.fs.governance.snapshot(agent.ep.sid)["tokens_reserved"] > 0          # the possibly-billed attempt stays in the books
