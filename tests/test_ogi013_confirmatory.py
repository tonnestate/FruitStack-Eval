"""Registered confirmatory analysis (exact McNemar, Clopper-Pearson, Holm). Hand-computed expectations; synthetic rows only."""
import json
import math
import subprocess
import sys
from pathlib import Path

from ogi013_confirmatory import analyse_pair, clopper_pearson, holm, mcnemar_exact


def test_mcnemar_exact_values():
    assert mcnemar_exact(7, 0) == 2 * 0.5 ** 7
    assert mcnemar_exact(5, 1) == 2 * 7 / 64
    assert mcnemar_exact(3, 3) == 1.0 and mcnemar_exact(0, 0) == 1.0


def test_clopper_pearson_known_bounds():
    lo, hi = clopper_pearson(7, 7)
    assert math.isclose(lo, 0.025 ** (1 / 7), abs_tol=1e-6) and hi == 1.0
    lo, hi = clopper_pearson(0, 10)
    assert lo == 0.0 and math.isclose(hi, 1 - 0.025 ** (1 / 10), abs_tol=1e-6)


def test_holm_step_down_is_monotone_and_capped():
    out = holm({"a": 0.01, "b": 0.02, "c": 0.04})
    assert math.isclose(out["a"], 0.03) and math.isclose(out["b"], 0.04) and math.isclose(out["c"], 0.04)
    assert holm({"x": 0.6, "y": 0.9})["y"] == 1.0


def _rows(spec):
    """spec: list of (task, a_success, b_success, b_status)"""
    rows = []
    for task, a, b, status in spec:
        rows.append({"task_id": task, "arm": "FIXED", "grade": 1.0 if a else 0.0, "grade_status": "VERIFIED"})
        rows.append({"task_id": task, "arm": "ADAPTIVE", "grade": 1.0 if b else (None if status != "VERIFIED" else 0.0), "grade_status": status})
    return rows


def test_pair_counts_and_unverified_is_nonsuccess():
    spec = [(f"t{i}", True, False, "VERIFIED") for i in range(7)] + [(f"s{i}", True, True, "VERIFIED") for i in range(3)] + [("u", True, False, "UNVERIFIED")]
    res = analyse_pair(_rows(spec))
    assert (res["pairs"], res["a_only"], res["b_only"], res["both_success"]) == (11, 8, 0, 3)     # the unverified B grade counts as a failure of B, not as a missing pair
    assert res["non_verified_as_nonsuccess"] == 1 and math.isclose(res["p_exact_mcnemar"], 2 * 0.5 ** 8)
    assert res["risk_difference"] == 8 / 11


def test_excluded_and_unpaired_rows_are_not_analysed():
    rows = _rows([("t1", True, False, "VERIFIED")]) + [{"task_id": "t2", "arm": "FIXED", "grade": 1.0, "grade_status": "VERIFIED"}]
    rows += [{"task_id": "t3", "arm": "FIXED", "grade": 1.0, "grade_status": "VERIFIED", "pair_excluded": True}, {"task_id": "t3", "arm": "ADAPTIVE", "grade": 0.0, "grade_status": "VERIFIED", "pair_excluded": True}]
    assert analyse_pair(rows)["pairs"] == 1


def test_cli_applies_holm_over_the_family(tmp_path):
    p1, p2 = tmp_path / "h1.jsonl", tmp_path / "h2.jsonl"
    p1.write_text("\n".join(json.dumps(r) for r in _rows([(f"t{i}", True, False, "VERIFIED") for i in range(7)])))
    p2.write_text("\n".join(json.dumps(r) for r in _rows([(f"t{i}", i % 2 == 0, i % 2 == 1, "VERIFIED") for i in range(6)])))
    out = tmp_path / "res.json"
    r = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "runners" / "ogi013_confirmatory.py"), "--out", str(out), f"H1={p1}", f"H2={p2}"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    res = json.loads(out.read_text())["results"]
    assert math.isclose(res["H1"]["p_holm"], 2 * 2 * 0.5 ** 7) and res["H2"]["p_holm"] == 1.0 and res["H1"]["significant_alpha_0_05_after_holm"] is True
