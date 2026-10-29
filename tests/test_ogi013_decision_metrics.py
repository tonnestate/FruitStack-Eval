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


def test_summary_counts_executed_unexpected_actions_and_completed_objectives():
    official = {"reward_info": {"reward": 0.0}, "termination_reason": "user_stop", "messages": [{"role": "assistant", "tool_calls": [{"name": "cancel_reservation", "arguments": {"reservation_id": "R"}},
                                                                                                 {"name": "book_reservation", "arguments": BOOK["arguments"]}]}]}
    s = dm.summarize(official, [], [BOOK])
    assert s["unexpected_writes_executed"] == 1 and s["expected_actions_completed"] == ["book_reservation"] and s["reviews"] == []


RUN = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs/pilot-4")
DATA = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench/data/tau2")


@pytest.mark.skipif(not (RUN / "collab/tasks/24/official-result.json").is_file(), reason="needs the PILOT-4 evidence")
def test_pilot4_collab_decision_is_classified_as_an_error_replaced_by_a_different_error():
    expected = next((t.get("evaluation_criteria") or {}).get("actions") for t in json.loads((DATA / "domains/airline/tasks.json").read_text()) if str(t["id"]) == "24")
    arm = RUN / "collab/tasks/24"
    s = dm.summarize(json.loads((arm / "official-result.json").read_text()), [json.loads(x) for x in (arm / "fruitstack-events.jsonl").read_text().splitlines() if x.strip()], expected)
    first = s["reviews"][0]
    assert (first["draft_class"], first["final_class"], first["outcome"]) == ("UNEXPECTED_WRITE", "UNEXPECTED_TRANSFER", "ERROR_REPLACED_BY_DIFFERENT_ERROR")
    assert s["unexpected_writes_executed"] == 0 and s["unexpected_transfer_executed"] == 1 and s["expected_actions_completed"] == [] and s["reward"] == 0.0


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


def test_the_collab_study_lock_matches_the_frozen_files():
    """A change to any frozen file must be a dated amendment, not a silent edit: STUDY_LOCK.txt hashes the design, manifest, generator, metrics and the COLLAB implementation."""
    import hashlib
    rows = [line.split(None, 1) for line in (PHASE2 / "STUDY_LOCK.txt").read_text().splitlines() if line and not line.startswith("#")]
    assert len(rows) >= 10
    for digest, rel in rows:
        assert hashlib.sha256((ROOT / rel.strip()).read_bytes()).hexdigest() == digest, rel
