"""Offline unit tests for runners/ogi013_single_e.py (SINGLE-E baseline helpers). Pure functions; no network, no provider calls."""
import pytest

from ogi013_single_e import canonical_action, majority_action, read_k

MSG_A = {"action": "message", "content": "Hello there"}
MSG_A_WS = {"action": "message", "content": "  Hello   there\n"}
MSG_B = {"action": "message", "content": "Goodbye"}
TOOL_X = {"action": "tool", "name": "get_user", "arguments": {"id": 1, "x": "y"}}
TOOL_X_REORDERED = {"action": "tool", "name": "get_user", "arguments": {"x": "y", "id": 1}}
TOOL_Y = {"action": "tool", "name": "get_user", "arguments": {"id": 2}}


def test_canonical_message_normalises_whitespace():
    assert canonical_action(MSG_A) == canonical_action(MSG_A_WS)
    assert canonical_action(MSG_A) != canonical_action(MSG_B)


def test_canonical_tool_ignores_argument_key_order():
    assert canonical_action(TOOL_X) == canonical_action(TOOL_X_REORDERED)
    assert canonical_action(TOOL_X) != canonical_action(TOOL_Y)


def test_message_never_equals_tool_call():
    assert canonical_action(MSG_A) != canonical_action({"action": "tool", "name": "Hello there", "arguments": {}})


def test_majority_picks_most_common_and_ignores_unparseable():
    winner, info = majority_action([None, MSG_B, MSG_A, None, MSG_A_WS])
    assert winner == MSG_A
    assert info["winner_index"] == 2
    assert info["ties"] is False
    assert sorted(info["counts"].values()) == [1, 2]


def test_tie_goes_to_earliest_draft_among_tied():
    winner, info = majority_action([MSG_B, MSG_A, MSG_A, MSG_B])
    assert winner == MSG_B
    assert info["winner_index"] == 0
    assert info["ties"] is True


def test_tie_with_unparseable_gap_uses_original_index():
    winner, info = majority_action([None, TOOL_Y, None, TOOL_X])
    assert winner == TOOL_Y
    assert info["winner_index"] == 1
    assert info["ties"] is True


def test_all_unparseable_returns_none():
    winner, info = majority_action([None, None])
    assert winner is None
    assert info == {"counts": {}, "winner_index": None, "ties": False}


def test_k1_equals_single_draft():
    winner, info = majority_action([TOOL_X])
    assert winner is TOOL_X
    assert info["winner_index"] == 0 and info["ties"] is False


@pytest.mark.parametrize("env", [{}, {"OGI013_SINGLE_E_K": ""}, {"OGI013_SINGLE_E_K": "0"}, {"OGI013_SINGLE_E_K": "-2"}, {"OGI013_SINGLE_E_K": "two"}])
def test_read_k_rejects_unset_or_invalid(env):
    with pytest.raises(RuntimeError, match="SINGLE_E_K_REQUIRED"):
        read_k(env)


def test_read_k_accepts_positive_integer():
    assert read_k({"OGI013_SINGLE_E_K": "3"}) == 3
    assert read_k({"OGI013_SINGLE_E_K": "1"}) == 1


def test_single_e_registered_and_never_organises():
    pytest.importorskip("tau2")
    from ogi013_tau2_agent import MODES, should_organize
    assert "single_e" in MODES
    assert should_organize("single_e", TOOL_X, {"get_user"}) is False
    assert should_organize("single_e", MSG_A, set()) is False
