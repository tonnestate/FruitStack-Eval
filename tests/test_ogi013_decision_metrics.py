"""Decision-level metrics and the prospective COLLAB study manifest: mechanical, deterministic, no model, no network."""
import json
from pathlib import Path

import pytest

from ogi013_pilot_fixtures import ROOT, load

PHASE2 = ROOT / "evidence/ogi013-phase2"
dm = load("decision_metrics", PHASE2 / "decision_metrics.py")
mf = load("make_study_manifest", PHASE2 / "make_study_manifest.py")
BOOK = {"name": "book_reservation", "arguments": {"user_id": "u", "cabin": "basic_economy", "flights": [{"flight_number": "HAT069", "date": "2024-05-20"}]}}
T = lambda name, **args: {"action": "tool", "name": name, "arguments": args}  # noqa: E731


def test_classification_against_the_reference_actions():
    exp = [BOOK]
    assert dm.classify(T("book_reservation", user_id="u", cabin="basic_economy", flights=[{"flight_number": "HAT069", "date": "2024-05-20", "x": 1}], extra=1), exp) == "MATCH_EXPECTED"
    assert dm.classify(T("book_reservation", user_id="u", cabin="economy", flights=[]), exp) == "WRONG_ARGS"
    assert dm.classify(T("cancel_reservation", reservation_id="R"), exp) == "UNEXPECTED_WRITE"
    assert dm.classify(T("transfer_to_human_agents", summary="s"), exp) == "UNEXPECTED_TRANSFER"
    assert dm.classify(T("transfer_to_human_agents", summary="s"), [{"name": "transfer_to_human_agents", "arguments": {}}]) == "MATCH_EXPECTED"
    assert dm.classify(T("get_reservation_details", reservation_id="R"), exp) == "SAFE_NON_WRITE" and dm.classify({"action": "message", "content": "hi"}, exp) == "SAFE_NON_WRITE"


@pytest.mark.parametrize("draft,final,changed,expected", [
    ("UNEXPECTED_WRITE", "SAFE_NON_WRITE", True, "PREVENTED_WRITE_ERROR"), ("WRONG_ARGS", "MATCH_EXPECTED", True, "PREVENTED_WRITE_ERROR"),
    ("UNEXPECTED_WRITE", "UNEXPECTED_TRANSFER", True, "ERROR_REPLACED_BY_DIFFERENT_ERROR"), ("UNEXPECTED_WRITE", "UNEXPECTED_WRITE", False, "ERROR_NOT_FIXED"),
    ("MATCH_EXPECTED", "SAFE_NON_WRITE", True, "CORRECT_BLOCKED"), ("MATCH_EXPECTED", "MATCH_EXPECTED", False, "VALIDATED_CORRECT"),
    ("SAFE_NON_WRITE", "SAFE_NON_WRITE", False, "NO_CHANGE_SAFE"), ("SAFE_NON_WRITE", "SAFE_NON_WRITE", True, "UNNECESSARY_CHANGE")])
def test_review_outcomes(draft, final, changed, expected):
    assert dm.outcome(draft, final, changed) == expected


def test_summary_separates_attempted_from_executed_and_deviations_from_policy_violations():
    msgs = [{"role": "assistant", "tool_calls": [{"id": "1", "name": "cancel_reservation", "arguments": {"reservation_id": "R"}}]}, {"role": "tool", "id": "1", "content": "ok", "error": False},
            {"role": "assistant", "tool_calls": [{"id": "2", "name": "cancel_reservation", "arguments": {"reservation_id": "Q"}}]}, {"role": "tool", "id": "2", "content": "Error: x", "error": True},
            {"role": "assistant", "tool_calls": [{"id": "3", "name": "book_reservation", "arguments": BOOK["arguments"]}]}, {"role": "tool", "id": "3", "content": "ok", "error": False}]
    s = dm.summarize({"reward_info": {"reward": 0.0, "db_check": {"db_match": False}, "nl_assertions": None}, "termination_reason": "user_stop", "messages": msgs}, [], [BOOK])
    assert s["state_changing_deviations"] == ["cancel_reservation"] and s["failed_write_attempts"] == ["cancel_reservation"]          # the failed cancel changed no state
    assert s["expected_actions_completed"] == ["book_reservation"] and s["objectives_abandoned"] == [] and s["abandon_cause"] == "NONE"
    assert s["policy_evidence"] == "NOT_EVALUATED_BY_OFFICIAL_GRADER" and s["db_match"] is False and s["reviews"] == []                # a reference deviation is NOT reported as a policy violation


def test_abandonment_causes_are_mechanical():
    base = {"reward_info": {"reward": 0.0}, "termination_reason": "user_stop"}
    stop = dict(base, messages=[{"role": "assistant", "content": "Please confirm?"}, {"role": "user", "content": "Yes, go ahead. ###STOP###"}])
    assert dm.summarize(stop, [], [BOOK])["abandon_cause"] == "PREMATURE_STOP_PENDING"
    transfer = dict(base, messages=[{"role": "assistant", "content": "x"}, {"role": "user", "content": "###TRANSFER###"}])
    assert dm.summarize(transfer, [], [BOOK])["abandon_cause"] == "TRANSFER"
    wrong = dict(stop, messages=[{"role": "assistant", "tool_calls": [{"id": "1", "name": "cancel_reservation", "arguments": {}}]}, {"role": "tool", "id": "1", "content": "ok", "error": False},
                                 {"role": "assistant", "content": "Done?"}, {"role": "user", "content": "yes ###STOP###"}])
    assert dm.summarize(wrong, [], [BOOK])["abandon_cause"] == "WRONG_ACTION_EXECUTED"


RUN = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs/pilot-4")
DATA = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench/data/tau2")


@pytest.mark.skipif(not (RUN / "collab/tasks/24/official-result.json").is_file(), reason="needs the PILOT-4 evidence")
def test_pilot4_collab_decision_is_classified_as_an_error_replaced_by_a_different_error():
    expected = next((t.get("evaluation_criteria") or {}).get("actions") for t in json.loads((DATA / "domains/airline/tasks.json").read_text()) if str(t["id"]) == "24")
    arm = RUN / "collab/tasks/24"
    s = dm.summarize(json.loads((arm / "official-result.json").read_text()), [json.loads(x) for x in (arm / "fruitstack-events.jsonl").read_text().splitlines() if x.strip()], expected)
    first = s["reviews"][0]
    assert (first["draft_class"], first["final_class"], first["outcome"]) == ("UNEXPECTED_WRITE", "UNEXPECTED_TRANSFER", "ERROR_REPLACED_BY_DIFFERENT_ERROR")
    assert s["state_changing_deviations"] == [] and s["unnecessary_transfer"] is True and s["expected_actions_completed"] == [] and s["reward"] == 0.0 and s["abandon_cause"] == "TRANSFER"


@pytest.mark.skipif(not (DATA / "domains/airline/split_tasks.json").is_file(), reason="needs the tau2 data")
def test_the_study_manifest_is_deterministic_disjoint_from_the_test_splits_and_stratified():
    m = mf.build(DATA)
    assert m == mf.build(DATA) and m["n_tasks"] == 48 and m["n_write_opportunity"] == 40
    for domain in ("airline", "retail"):
        test = {str(i) for i in json.loads((DATA / f"domains/{domain}/split_tasks.json").read_text())["test"]}
        assert not test & {r["task_id"] for r in m["tasks"] if r["domain"] == domain}                    # C1/C2/C3 and the pilots live in the test splits
    assert all(r["expected_write_actions"] > 0 for r in m["tasks"] if r["stratum"] == "write-opportunity") and all(r["expected_write_actions"] == 0 for r in m["tasks"] if r["stratum"] == "no-write-control")
    assert 0 < sum(r["first_arm"] == "SINGLE" for r in m["tasks"]) < m["n_tasks"]                        # the arm order is not always SINGLE first
    assert (PHASE2 / "study_manifest.json").is_file() and json.loads((PHASE2 / "study_manifest.json").read_text()) == m      # the frozen file is the generator's output


# Documented, expected drift: these 4 frozen files were legitimately changed by QA-1/QA-1b after the 2026-10-29 freeze (c204e66). The study is archived, C3 is on HOLD and
# no PREREG_LOCK exists, so the lock is not re-issued. The lock files themselves are never edited. Any OTHER drift still fails this test.
KNOWN_POST_FREEZE_DRIFT = {
    "runners/ogi013_tau2_agent.py": "QA-1/QA-1b change after the 2026-10-29 freeze; study archived",
    "runners/ogi013_org_collab.py": "QA-1/QA-1b change after the 2026-10-29 freeze; study archived",
    "runners/ogi013_lineage_heart.py": "QA-1/QA-1b change after the 2026-10-29 freeze; study archived",
    "evidence/ogi013-pilot/sim_preflight.py": "QA-1/QA-1b change after the 2026-10-29 freeze; study archived",
}


def test_the_collab_study_lock_matches_the_frozen_files():
    """A change to any frozen file must be a dated amendment, not a silent edit: the LATEST entry per file of STUDY_LOCK.txt and AMENDMENT_LOCK.txt must match the bytes in the repository.
    The KNOWN_POST_FREEZE_DRIFT files are the only exemption; every other frozen file must still match."""
    import hashlib
    latest = {}
    for lock in (PHASE2 / "STUDY_LOCK.txt", ROOT / "evidence/ogi013-collab1/AMENDMENT_LOCK.txt"):
        for line in lock.read_text().splitlines():
            if line and not line.startswith("#"):
                digest, rel = line.split(None, 1)
                latest[rel.strip()] = digest
    assert len(latest) >= 24
    assert set(KNOWN_POST_FREEZE_DRIFT) <= set(latest), "an exempted file is no longer in the lock; remove its exemption"
    for rel, digest in latest.items():
        if rel in KNOWN_POST_FREEZE_DRIFT:
            continue
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == digest, rel


def test_reads_are_means_not_objectives():
    official = {"reward_info": {"reward": 1.0}, "termination_reason": "user_stop", "messages": [{"role": "assistant", "tool_calls": [{"id": "1", "name": "book_reservation", "arguments": BOOK["arguments"]}]},
                                                                                            {"role": "tool", "id": "1", "content": "ok", "error": False}]}
    s = dm.summarize(official, [], [{"name": "get_reservation_details", "arguments": {}}, {"name": "search_direct_flight", "arguments": {}}, BOOK])
    assert s["expected_writes"] == ["book_reservation"] and s["objectives_abandoned"] == [] and s["abandon_cause"] == "NONE"
