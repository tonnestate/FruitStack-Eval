"""Addendum 6 section 1: release-vote grounding decided by the host from the ledger (scripted voters, no models)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
from ogi013_vote import judge_vote, tally  # noqa: E402

OK_NONE = "APPROVE: EXCELLENT\nRan forms_tests.test_media: 3 tests OK; reproduced the issue with run_python, now passes.\nOWN_OBJECTIONS: NONE"
CHANGE, CHECK_AFTER, CHECK_BEFORE = 100, 200, 50


def row(i, lineage="L2", answered=None, withdrawn=False):
    return {"id": i, "target": "S1", "lineage": lineage, "kind": "objection", "open": answered is None, "answered_by": answered, "withdrawn": withdrawn}


def vote(text, lineage, objs, checks=(CHECK_AFTER,), stated=True):
    return judge_vote(text, lineage, objs, "S1", list(checks), CHANGE, stated)


def test_a_no_ledger_objection_none_is_valid():
    assert vote(OK_NONE, "L2", [])["verdict"] == "EXCELLENT"


def test_b_open_objection_not_listed():
    assert vote(OK_NONE.replace("NONE", "O1 is fine"), "L2", [row("O1")])["verdict"] == "UNGROUNDED_APPROVAL"
    assert vote("APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O9 fixed", "L2", [row("O1", answered="rev1")])["verdict"] == "UNGROUNDED_APPROVAL"


def test_c_listed_but_still_open():
    r = vote("APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O1 I think it is fine now", "L2", [row("O1")])
    assert r["verdict"] == "UNGROUNDED_APPROVAL" and "still open" in r["reason"]


def test_d_check_before_latest_change():
    assert vote(OK_NONE, "L2", [], checks=(CHECK_BEFORE,))["verdict"] == "UNGROUNDED_APPROVAL"
    assert vote(OK_NONE, "L2", [], checks=())["verdict"] == "UNGROUNDED_APPROVAL"


def test_e_claims_none_but_ledger_has_objection():
    assert vote(OK_NONE, "L2", [row("O1", answered="rev1")])["verdict"] == "UNGROUNDED_APPROVAL"


def test_listed_and_answered_or_withdrawn_is_valid():
    t = "APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O1 fixed in revision 1, test now passes"
    assert vote(t, "L2", [row("O1", answered="revision 1")])["verdict"] == "EXCELLENT"
    w = vote("APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O1 WITHDRAWN", "L2", [row("O1")])
    assert w["verdict"] == "EXCELLENT"


def test_f_three_grounded_voters_release_unanimously():
    votes = [vote(OK_NONE, f"L{i}", []) for i in range(3)]
    assert tally(votes) == "RELEASED_UNANIMOUS_EXCELLENT"


def test_g_one_acceptable_returns_to_author():
    votes = [vote(OK_NONE, "L1", []), vote(OK_NONE, "L2", []), vote(OK_NONE.replace("EXCELLENT", "ACCEPTABLE"), "L3", [])]
    assert tally(votes) == "RETURN_TO_AUTHOR"
