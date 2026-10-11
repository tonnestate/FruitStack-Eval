import json

import pytest

from fruitstack_eval import blind, inquiry
from fruitstack_eval.compare import score_rows

REF = json.dumps({"verdict": "REFUTED", "key_type": "date", "key": "1957-03-25", "accept": [],
                  "sources": ["https://example.org/treaty"]})


def answer(verdict, key, prefix="Some reasoning.\n"):
    return f"{prefix}VERDICT: {verdict}\nKEY: {key}"


@pytest.mark.parametrize("output, grade", [
    (answer("REFUTED", "1957-03-25"), 1.0),
    (answer("REFUTED", "25 March 1957"), 1.0),
    (answer("False", "March 25th, 1957"), 1.0),
    (answer("**REFUTED**", "25.03.1957"), 1.0),
    (answer("REFUTED", "1958-01-01"), 0.5),
    (answer("SUPPORTED", "1957-03-25"), 0.5),
    (answer("SUPPORTED", "1958"), 0.0),
    ("The claim is wrong; it was signed in 1957.", 0.0),
    (None, 0.0),
])
def test_inquiry_grades(output, grade):
    assert inquiry.grade(REF, output)["grade"] == grade


def test_statuses_and_abstention_are_reported():
    assert inquiry.grade(REF, None)["status"] == "NO_ANSWER"
    assert inquiry.grade(REF, "no block here")["status"] == "NO_STRUCTURED_ANSWER"
    abstain = inquiry.grade(REF, answer("NOT_ENOUGH_INFO", "unknown"))
    assert abstain["abstained"] and abstain["grade"] == 0.0
    last_block_wins = inquiry.grade(REF, answer("SUPPORTED", "1956-01-01") + "\n" + answer("REFUTED", "1957-03-25"))
    assert last_block_wins["grade"] == 1.0


def test_key_types():
    num = json.dumps({"verdict": "SUPPORTED", "key_type": "number", "key": "84.7 million", "tolerance": 0.01,
                      "sources": ["s"]})
    assert inquiry.grade(num, answer("SUPPORTED", "84,669,326"))["key_ok"]
    assert inquiry.grade(num, answer("SUPPORTED", "84.7 Mio"))["key_ok"]
    assert not inquiry.grade(num, answer("SUPPORTED", "83 million"))["key_ok"]
    integer = json.dumps({"verdict": "REFUTED", "key_type": "integer", "key": "8446", "sources": ["s"]})
    assert inquiry.grade(integer, answer("REFUTED", "RFC 8446"))["grade"] == 1.0
    assert inquiry.grade(integer, answer("REFUTED", "8,446"))["grade"] == 1.0
    year = json.dumps({"verdict": "SUPPORTED", "key_type": "year", "key": "1969", "sources": ["s"]})
    assert inquiry.grade(year, answer("SUPPORTED", "in 1969"))["grade"] == 1.0
    text = json.dumps({"verdict": "REFUTED", "key_type": "text", "key": "Marie Curie", "accept": ["Maria Skłodowska-Curie"],
                       "sources": ["s"]})
    assert inquiry.grade(text, answer("REFUTED", "marie curie."))["grade"] == 1.0
    assert inquiry.grade(text, answer("REFUTED", "Maria Sklodowska Curie"))["grade"] == 1.0
    assert inquiry.grade(text, answer("REFUTED", "Pierre Curie"))["grade"] == 0.5


@pytest.mark.parametrize("bad", [
    {"verdict": "MAYBE", "key_type": "date", "key": "2020-01-01", "sources": ["s"]},
    {"verdict": "REFUTED", "key_type": "colour", "key": "red", "sources": ["s"]},
    {"verdict": "REFUTED", "key_type": "date", "key": "not a date", "sources": ["s"]},
    {"verdict": "REFUTED", "key_type": "date", "key": "2020-01-01", "sources": []},
    {"verdict": "REFUTED", "key_type": "number", "key": "3", "tolerance": -1, "sources": ["s"]},
])
def test_invalid_references_are_rejected(bad):
    with pytest.raises(ValueError):
        inquiry.parse_reference(json.dumps(bad))


def test_evidence_is_an_admissible_inquiry_label():
    ev = inquiry.evidence(REF, answer("REFUTED", "1957-03-25"))
    scored, excluded = score_rows([{"task_id": "t", "arm": "F1", "family": "INQUIRY", "subfamily": "HIST",
                                    "evidence": ev, "quota_units": 1, "cost_eur": 0.0, "wall_seconds": 3}])
    assert scored[0]["utility"] == 1.0 and not any(excluded.values())


def make_results():
    tasks = [{"task_id": f"t{i}", "prompt": f"Claim {i}", "reference": REF} for i in range(4)]
    results = [{"task_id": f"t{i}", "arm": arm, "output": answer("REFUTED", "1957-03-25", prefix=f"As Claude Opus, {arm}\n")}
               for i in range(4) for arm in ("F1", "F3", "A")]
    return tasks, results


def test_blind_export_hides_arms_and_redacts_names():
    tasks, results = make_results()
    sheet, key, manifest = blind.export(results, tasks, seed=5, created_at="2026-10-11T00:00:00+00:00")
    assert len(sheet) == 12 and manifest["arms"] == ["A", "F1", "F3"]
    assert all("arm" not in row for row in sheet)
    assert all("Claude" not in row["answer"] and "Opus" not in row["answer"] for row in sheet)
    assert manifest["redactions"] == 24
    again = blind.export(results, tasks, seed=5, created_at="2026-10-11T00:00:00+00:00")
    assert again[2] == manifest                                           # reproducible from the seed


def test_blind_ingest_validates_and_voids_whole_tasks():
    tasks, results = make_results()
    sheet, key, manifest = blind.export(results, tasks, seed=5)
    graded = [dict(row, grade=1.0) for row in sheet]
    out = blind.ingest(manifest, key, graded, grader="owner")
    assert len(out["labels"]) == 12 and out["labels"][0]["evidence"]["provenance"] == "EXTERNALLY_VERIFIED"

    graded[0]["void"] = True
    voided = blind.ingest(manifest, key, graded, grader="owner")
    assert voided["voided_tasks"] == [key[0]["task_id"]] and len(voided["labels"]) == 9

    with pytest.raises(ValueError, match="key does not match"):
        blind.ingest(manifest, [dict(key[0], arm="SWAPPED")] + key[1:], graded, grader="owner")
    with pytest.raises(ValueError, match="not graded"):
        blind.ingest(manifest, key, graded[1:], grader="owner")
    bad = [dict(row, grade=0.7) for row in sheet]
    with pytest.raises(ValueError, match="grade must be one of"):
        blind.ingest(manifest, key, bad, grader="owner")
    with pytest.raises(ValueError, match="grader identity"):
        blind.ingest(manifest, key, [dict(row, grade=1.0) for row in sheet], grader=" ")


def test_blind_sample_keeps_every_arm_of_a_sampled_task():
    tasks, results = make_results()
    sheet, key, manifest = blind.export(results, tasks, seed=9, sample=0.5)
    per_task = {}
    for k in key:
        per_task.setdefault(k["task_id"], set()).add(k["arm"])
    assert len(per_task) == 2 and all(arms == {"F1", "F3", "A"} for arms in per_task.values())


def test_agreement_with_deterministic_grades():
    labels = [{"task_id": "t1", "arm": "F1", "evidence": {"grade": 1.0}},
              {"task_id": "t2", "arm": "F1", "evidence": {"grade": 0.5}}]
    stats = blind.agreement(labels, {("t1", "F1"): 1.0, ("t2", "F1"): 1.0})
    assert stats == {"items": 2, "exact_agreement": 0.5, "disagreements": 1}
