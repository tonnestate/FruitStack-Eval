"""Addenda 6 and 7: release-vote grounding and objection lifecycle decided by the host from the ledger (scripted voters, no models)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
from ogi013_vote import OPEN, PENDING, RESOLVED, WITHDRAWN, Ledger, judge_vote, next_no_shrink, tally, vote_stop  # noqa: E402

OK_NONE = "APPROVE: EXCELLENT\nRan forms_tests.test_media: 3 tests OK; reproduced the issue with run_python, now passes.\nOWN_OBJECTIONS: NONE"
CHANGE, AFTER, BEFORE = 100, 200, 50


def ledger_with(lineage="L2", n=1):
    led = Ledger()
    for _ in range(n):
        led.objection("S1", lineage, "text", grounded=True)
    for o in led.objs:
        o["raised_ns"] = 60
    return led


def vote(text, lineage, led, checks=((AFTER, "out"),), stated=True, **kw):
    return judge_vote(text, lineage, led.objs, "S1", list(checks), CHANGE, stated, **kw)


FIXED = "APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O1 fixed in revision 1, test now passes"


def test_a_no_ledger_objection_none_is_valid():
    assert vote(OK_NONE, "L2", Ledger())["verdict"] == "EXCELLENT"


def test_b_open_objection_not_listed():
    assert vote(OK_NONE.replace("NONE", "O9 fine"), "L2", ledger_with())["verdict"] == "UNGROUNDED_APPROVAL"


def test_c_listed_but_still_open():
    assert vote(FIXED, "L2", ledger_with())["verdict"] == "UNGROUNDED_APPROVAL"


def test_d_check_before_latest_change():
    assert vote(OK_NONE, "L2", Ledger(), checks=((BEFORE, "o"),))["verdict"] == "UNGROUNDED_APPROVAL"
    assert vote(OK_NONE, "L2", Ledger(), checks=())["verdict"] == "UNGROUNDED_APPROVAL"


def test_e_claims_none_but_ledger_has_objection():
    assert vote(OK_NONE, "L2", ledger_with())["verdict"] == "UNGROUNDED_APPROVAL"


def test_f_three_grounded_voters_release_unanimously():
    assert tally([vote(OK_NONE, f"L{i}", Ledger()) for i in range(3)]) == "RELEASED_UNANIMOUS_EXCELLENT"


def test_g_one_acceptable_returns_to_author():
    votes = [vote(OK_NONE, "L1", Ledger()), vote(OK_NONE, "L2", Ledger()), vote(OK_NONE.replace("EXCELLENT", "ACCEPTABLE"), "L3", Ledger())]
    assert tally(votes) == "RETURN_TO_AUTHOR"


def test_h_unchanged_code_revision_leaves_objection_open():
    led = ledger_with()
    led.revise("S1", 1, False, ["O1"], reason="I disagree")
    o = led.objs[0]
    assert o["state"] == OPEN and o["contested"] == 1 and led.open_count("S1") == 1
    assert vote(FIXED, "L2", led)["verdict"] == "UNGROUNDED_APPROVAL"


def test_i_changed_code_is_only_pending():
    led = ledger_with()
    led.revise("S1", 1, True, ["O1"])
    assert led.objs[0]["state"] == PENDING and led.open_count("S1") == 1
    assert vote(FIXED, "L2", led)["verdict"] == "UNGROUNDED_APPROVAL"


def test_j_reexamination_by_raiser_resolves():
    led = ledger_with()
    led.revise("S1", 1, True, ["O1"])
    rev_ns = led.objs[0]["revised_ns"]
    ch = led.reexamine("S1", "ISSUES: NONE\nO1: RESOLVED", "L2", ("L1",), [(rev_ns + 5, "out")])
    assert ch == [("O1", RESOLVED)] and led.open_count("S1") == 0
    assert vote(FIXED, "L2", led)["verdict"] == "EXCELLENT"


def test_reexamination_needs_check_after_revision_and_other_lineage():
    led = ledger_with()
    led.revise("S1", 1, True, ["O1"])
    rev_ns = led.objs[0]["revised_ns"]
    assert led.reexamine("S1", "O1: RESOLVED", "L2", ("L1",), [(rev_ns - 1, "o")]) == []        # check before the revision
    assert led.reexamine("S1", "O1: RESOLVED", "L1", ("L1",), [(rev_ns + 1, "o")]) == []        # the reviser's own lineage
    assert led.objs[0]["state"] == PENDING


def test_k_still_open_returns_to_open():
    led = ledger_with()
    led.revise("S1", 1, True, ["O1"])
    rev_ns = led.objs[0]["revised_ns"]
    assert led.reexamine("S1", "O1: STILL_OPEN", "L2", ("L1",), [(rev_ns + 1, "o")]) == [("O1", OPEN)]
    assert led.open_count("S1") == 1


def test_l_withdrawal_needs_evidence():
    led = ledger_with()
    w = "APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O1 WITHDRAWN because test_media_order passes with the new code"
    assert vote(w, "L2", led, checks=((CHANGE + 1, "unrelated output"),))["verdict"] == "UNGROUNDED_APPROVAL"       # check output not referred to
    assert vote(w, "L2", led, checks=((55, "test_media_order ... ok"), (AFTER, "x")))["verdict"] == "UNGROUNDED_APPROVAL"   # check before the objection was raised
    assert vote("APPROVE: EXCELLENT\nchecked forms_tests ok\nOWN_OBJECTIONS: O1 WITHDRAWN", "L2", led, checks=((AFTER, "test_media_order ... ok"),))["verdict"] == "UNGROUNDED_APPROVAL"
    r = vote(w, "L2", led, checks=((AFTER, "test_media_order ... ok"),))
    assert r["verdict"] == "EXCELLENT" and r["withdrawals"] == 1 and led.objs[0]["state"] == WITHDRAWN


def test_m_voter_lineage_fallback_is_no_vote():
    r = vote(OK_NONE, "L2", Ledger(), returned_lineage="L1", author_lineages=("L1",))
    assert r["verdict"] == "NO_VOTE" and r["counts"] == "REJECT" and r["reason"] == "VOTER_LINEAGE_FALLBACK"


def test_o_unchanged_revisions_end_with_no_shrink_3_not_cycles_8():
    led, no_shrink, prev_open, guard, cycle = ledger_with(), 0, None, None, 0
    while guard is None:
        open_now = led.open_count("S1")
        no_shrink = next_no_shrink(no_shrink, prev_open, open_now, 0, 0)
        prev_open, cycle = open_now, cycle + 1
        guard = vote_stop(no_shrink, cycle, 0, 8)
        led.revise("S1", cycle, False, ["O1"], reason="no change")
    assert guard == "VOTE_NO_SHRINK_3" and cycle < 8


def test_ledger_emit_works_with_episode_event_signature():
    """FIX: OBJECTION used kind= which clashed with Episode.event(kind, ...) (gdev1 TypeError)."""
    got = []
    led = Ledger()
    led.emit = lambda kind, **k: got.append((kind, k))
    led.objection("S1", "L1", "t")
    assert got[0][0] == "OBJECTION" and got[0][1]["okind"] == "objection"
