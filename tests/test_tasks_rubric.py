import itertools

import pytest

from fruitstack_eval import tasks
from fruitstack_eval.rubric import NotALabel, utility


def task(task_id, subfamily="valuation", split="HELDOUT", family="INQUIRY", reference="42"):
    return {"task_id": task_id, "family": family, "subfamily": subfamily, "split": split,
            "prompt": f"question {task_id}", "reference": reference}


def test_validate_catches_problems():
    rows = [task("t1"), task("t1"), task("t2", split="TRAIN"), task("t3", family="ART", subfamily="x")]
    problems = tasks.validate(rows)
    assert any("duplicate" in p for p in problems)
    assert any("both TRAIN and HELDOUT" in p for p in problems)
    assert any("unknown family" in p for p in problems)
    assert tasks.validate([task("a", split="TRAIN")]) == ["no HELDOUT subfamily: generalization cannot be tested"]


def test_commit_and_verify_roundtrip():
    rows = [task("t1"), task("t2", subfamily="register", split="TRAIN", reference="HRB 1")]
    counter = itertools.count()
    manifest, salts = tasks.commit(rows, salt_factory=lambda: f"salt{next(counter)}", created_at="2026-10-11T00:00:00+00:00")
    assert "prompt" not in manifest["tasks"][0] and "reference" not in manifest["tasks"][0]
    assert tasks.verify(manifest, rows, salts) == []
    tampered = [dict(rows[0], reference="43"), rows[1]]
    assert any("reference differs" in p for p in tasks.verify(manifest, tampered, salts))
    manifest["tasks"][0]["split"] = "TRAIN"
    assert any("digest" in p for p in tasks.verify(manifest, rows, salts))


def test_commit_refuses_invalid_sets():
    with pytest.raises(ValueError):
        tasks.commit([task("a", split="TRAIN")])


def test_rubric_families():
    observed = {"provenance": "HARNESS_OBSERVED"}
    assert utility("SOFTWARE", {**observed, "tests_total": 4, "tests_passed": 3}) == 0.75
    assert utility("INQUIRY", {**observed, "blinded": True, "grade": 0.5}) == 0.5
    research = {**observed, "claims_asserted": 4, "claims_supported": 2, "key_points_total": 2, "key_points_covered": 2}
    assert utility("RESEARCH", research) == pytest.approx(2 * 0.5 * 1.0 / 1.5)
    economic = {"provenance": "EXTERNALLY_VERIFIED", "correctness_audit_passed": True, "penalty_events": 0,
                "outcome_score": 0.8}
    assert utility("ECONOMIC", economic) == 0.8
    assert utility("ECONOMIC", {**economic, "penalty_events": 1}) == 0.0
    assert utility("ECONOMIC", {**economic, "correctness_audit_passed": False}) == 0.0


def test_worker_claims_and_unblinded_grades_are_not_labels():
    with pytest.raises(NotALabel):
        utility("SOFTWARE", {"provenance": "WORKER_CLAIMED", "tests_total": 1, "tests_passed": 1})
    with pytest.raises(NotALabel):
        utility("INQUIRY", {"provenance": "HARNESS_OBSERVED", "blinded": False, "grade": 1})


@pytest.mark.parametrize("family,evidence", [
    ("SOFTWARE", {"tests_total": 0, "tests_passed": 0}),
    ("SOFTWARE", {"tests_total": 2, "tests_passed": 3}),
    ("INQUIRY", {"blinded": True, "grade": 0.7}),
    ("RESEARCH", {"claims_asserted": 1, "claims_supported": 2, "key_points_total": 1, "key_points_covered": 1}),
    ("ECONOMIC", {"correctness_audit_passed": True, "penalty_events": 0, "outcome_score": 1.2}),
    ("POETRY", {}),
])
def test_rubric_rejects_inconsistent_evidence(family, evidence):
    with pytest.raises(ValueError):
        utility(family, {"provenance": "HARNESS_OBSERVED", **evidence})
