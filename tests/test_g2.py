import random
from datetime import date, timedelta
from pathlib import Path

import pytest

from fruitstack_eval import calibration, independence

ROOT = Path(__file__).resolve().parent.parent


def test_generation_is_deterministic_and_covers_every_kind_and_level():
    a, b = calibration.generate(48, 7), calibration.generate(48, 7)
    assert a == b and calibration.task_set_digest(a) == calibration.task_set_digest(b)
    assert calibration.task_set_digest(calibration.generate(48, 8)) != calibration.task_set_digest(a)
    assert {t["kind"] for t in a} == set(calibration.KINDS)
    assert {t["level"] for t in a} == {0, 1, 2, 3}
    assert all(t["prompt"].endswith(calibration.FORMAT) for t in a)
    with pytest.raises(ValueError):
        calibration.generate(3, 1)


def test_reference_answers_are_correct():
    for task in calibration.generate(120, 11):
        prompt, answer = task["prompt"], task["answer"]
        if task["kind"] == "multiply":
            left, right = prompt.split("Compute ")[1].split(" exactly")[0].split(" × ")
            assert int(left) * int(right) == int(answer)
        elif task["kind"] == "count_letter":
            letter = prompt.split("letter '")[1][0]
            text = prompt.split("\n")[1]
            assert text.count(letter) == int(answer)
        elif task["kind"] == "date_shift" and task["level"] < 3:
            words = prompt.split()
            span, verb, start = int(words[3]), words[5], date.fromisoformat(words[6].rstrip("?"))
            assert (start + timedelta(days=span if verb == "after" else -span)).isoformat() == answer
        elif task["kind"] == "word_sort":
            words = prompt.split(": ")[1].split("\n")[0].split(", ")
            assert ",".join(sorted(words)) == answer


def test_extract_and_normalize():
    assert calibration.extract("x\nANSWER: 12\nANSWER: 1,234.") == "1,234."
    assert calibration.extract("no answer line") is None
    assert calibration.normalize("multiply", "1,234.") == "1234"
    assert calibration.normalize("kth_smallest", "−17") == "-17"
    assert calibration.normalize("word_sort", "Bab, cad,  dof") == "bab,cad,dof"
    assert calibration.normalize("date_shift", "Monday.") == "monday"


def test_score_separates_unexecuted_unparsed_and_wrong():
    tasks = [{"task_id": "t1", "kind": "multiply", "level": 0, "prompt": "p", "answer": "42"}]
    rows = [
        {"task_id": "t1", "group": "g", "success": True, "structural_state": "WELL_FORMED", "output": "ANSWER: 42"},
        {"task_id": "t1", "group": "g", "success": True, "structural_state": "WELL_FORMED", "output": "forty-two"},
        {"task_id": "t1", "group": "g", "success": False, "structural_state": "FAILED", "output": None},
        {"task_id": "zz", "group": "g", "success": True, "structural_state": "WELL_FORMED", "output": "ANSWER: 1"},
    ]
    scored, warnings = calibration.score(tasks, rows)
    assert [(r["executed"], r["parsed"], r["correct"]) for r in scored] == [
        (True, True, True), (True, False, False), (False, False, None)]
    assert warnings == ["result for unknown task zz"]


def thresholds(**kw):
    base = dict(version="test", min_calls=40, min_execution_rate=0.8, min_shared_tasks=30, max_phi=0.5,
                max_same_wrong_share=0.5, min_groups=3, bootstrap=200, seed=1)
    base.update(kw)
    return independence.Thresholds(**base)


def rows_for(group, errors, wrong_tag, executed=None, n=60):
    out = []
    for t in range(n):
        ok = t not in errors
        done = executed is None or t in executed
        out.append({"task_id": f"t{t}", "group": group, "offer_id": f"o-{group}", "model": f"m-{group}",
                    "receipt_id": f"r-{group}-{t}" if done else None, "model_fingerprint": "fp",
                    "executed": done, "parsed": done, "correct": ok if done else None,
                    "answer_given": ("ok" if ok else f"bad-{wrong_tag}") if done else None})
    return out


def test_phi_matches_hand_computation():
    a = [1, 1, 0, 0, 1, 0, 0, 0]
    b = [1, 0, 0, 0, 1, 0, 1, 0]
    # n11 = 2, n1. = 3, n.1 = 3, n = 8 -> (16 - 9) / sqrt(3*5*3*5) = 7/15
    assert independence._phi(a, b) == pytest.approx(7 / 15)
    assert independence._phi([0, 0, 0], [1, 0, 1]) is None


def test_independent_groups_pass_and_a_clone_is_correlated():
    errs = {"A": set(range(0, 18)), "B": set(range(12, 30)), "D": set(range(36, 54))}
    scored = (rows_for("A", errs["A"], "a") + rows_for("B", errs["B"], "b") + rows_for("D", errs["D"], "d")
              + rows_for("C", errs["A"], "a"))                       # C copies A, wrong answers included
    result = independence.analyze(scored, thresholds())
    assert result["pairs"]["A|C"]["verdict"] == "CORRELATED" and result["pairs"]["A|C"]["phi"] == pytest.approx(1.0)
    assert len(result["largest_independent_set"]) == 3 and "B" in result["largest_independent_set"]
    assert result["passed"]


def test_same_wrong_answers_count_as_correlation_even_with_low_phi():
    rng = random.Random(4)
    ea, eb = set(rng.sample(range(60), 20)), set(rng.sample(range(60), 20))
    scored = rows_for("A", ea, "same") + rows_for("B", eb, "same")
    pair = independence.analyze(scored, thresholds(min_groups=2))["pairs"]["A|B"]
    assert pair["same_wrong_share"] == 1.0 and pair["verdict"] == "CORRELATED"


def test_unreliable_and_error_free_groups_do_not_qualify_as_evidence():
    rng = random.Random(5)
    flaky = rows_for("F", set(rng.sample(range(60), 15)), "f", executed=set(range(25)))
    perfect = rows_for("P", set(), "p")
    good = rows_for("G", set(rng.sample(range(60), 15)), "g")
    result = independence.analyze(flaky + perfect + good, thresholds())
    assert result["groups"]["F"]["qualified"] is False                 # 25 of 60 executed
    assert result["pairs"]["G|P"]["verdict"] == "UNDETERMINED_NO_ERROR_VARIANCE"
    assert result["pairs"]["F|G"]["verdict"] == "INSUFFICIENT_SHARED_TASKS"
    assert result["qualified_groups"] == ["G", "P"]
    assert not result["passed"]
    assert set(result["blockers"]) == {"TOO_FEW_QUALIFIED_GROUPS", "NO_INDEPENDENT_SET_OF_REQUIRED_SIZE"}


def test_rows_without_group_block_the_gate():
    rows = rows_for("A", {1}, "a")
    rows[0]["group"] = None
    result = independence.analyze(rows, thresholds(min_groups=1))
    assert "ROWS_WITHOUT_GROUP" in result["blockers"]


def test_frozen_thresholds_load():
    t = independence.Thresholds.load(ROOT / "config" / "g2_thresholds.toml")
    assert t.version == "G2-THRESHOLDS/1" and t.min_groups == 3 and t.max_phi == 0.5
