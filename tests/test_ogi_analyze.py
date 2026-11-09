import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import ogi_analyze as oa  # noqa: E402


def synth(n, p_t, p_e, fam="F1", seed=0, members=("S_a", "S_b"), p_s=0.5, p_g=None, bad_e=0):
    rnd = random.Random(seed)
    rows = []
    for i in range(n):
        tid = f"{fam}{i}"
        hard = rnd.random()  # shared task difficulty induces correlation
        def draw(p):
            return rnd.random() < p and hard < 0.95 or rnd.random() < p * 0.3
        mem = [draw(p_s) for _ in members]
        t_ok = draw(p_t)
        base = dict(task_id=tid, family=fam, tokens_in=500, tokens_out=500, calls=3, valid=True)
        rows.append({**base, "arm": "T", "correct": t_ok, "member_first_correct": mem})
        rows.append({**base, "arm": "E", "correct": draw(p_e), "valid": i >= bad_e})
        if p_g is not None:
            rows.append({**base, "arm": "G", "correct": draw(p_g)})
        for m, ok in zip(members, mem):
            rows.append({**base, "arm": m, "correct": ok, "tokens_out": 300})
    return rows


def test_planted_effect_detected():
    rep = oa.analyze(synth(300, 0.85, 0.5, p_g=0.5))
    t = rep["families"]["F1"]["contrasts"]["primary:T_vs_E"]
    assert t["reject"] and t["direction"] == "a"
    assert rep["families"]["F1"]["harm"]["n"] == 300


def test_null_not_detected():
    rep = oa.analyze(synth(300, 0.6, 0.6, seed=3))
    assert not rep["families"]["F1"]["contrasts"]["primary:T_vs_E"]["reject"]


def test_two_family_rule():
    rows = synth(300, 0.85, 0.5, "A", 1) + synth(300, 0.85, 0.5, "B", 2)
    assert oa.analyze(rows)["two_family_rule"]["primary:T_vs_E"]["confirmed"]
    rows = synth(300, 0.85, 0.5, "A", 1) + synth(300, 0.6, 0.6, "B", 2)
    assert not oa.analyze(rows)["two_family_rule"]["primary:T_vs_E"]["confirmed"]


def test_invalid_rows_excluded_and_reported():
    rep = oa.analyze(synth(40, 0.8, 0.5, bad_e=5))
    assert rep["excluded_invalid"]["n_excluded"] == 5
    assert rep["families"]["F1"]["contrasts"]["primary:T_vs_E"]["n_pairs"] == 35


def test_mcnemar_holm_known_values():
    assert abs(oa.mcnemar_exact(10, 0) - 2 * 0.5**10) < 1e-12
    assert oa.mcnemar_exact(0, 0) == 1.0
    assert oa.holm({"a": 0.01, "b": 0.02, "c": 0.5}) == {"a": 0.03, "b": 0.04, "c": 0.5}


def test_harm_counts_and_ci():
    rows = [dict(task_id=str(i), family="F", arm="T", correct=c, member_first_correct=m, valid=True)
            for i, (c, m) in enumerate([(True, [False]), (False, [True]), (True, [True]), (False, [False])])]
    h = oa.harm(rows, "T")
    assert (h["corrected"], h["damaged"], h["held"], h["lost_both"]) == (1, 1, 1, 1)
    assert h["corrected_ci"][0] < 0.25 < h["corrected_ci"][1]


def test_eval003_union_oracle():
    rows = []
    for i in range(30):
        for m in ("S_a", "S_b"):
            for _ in range(3):
                rows.append(dict(task_id=f"t{i}", family="F", arm=m, correct=False, valid=True))
        rows.append(dict(task_id=f"t{i}", family="F", arm="T", correct=i < 20, valid=True))
        rows.append(dict(task_id=f"t{i}", family="F", arm="E", correct=i < 2, valid=True))
    r = oa.eval003(rows, oa.ROLES)
    assert r["n_U"] == 30 and r["team"]["solved"] == 20
    assert r["tests"]["T_vs_E_on_U"]["reject"]


def test_token_logistic_runs():
    out = oa.analyze(synth(200, 0.8, 0.5))["families"]["F1"]["logistic_tokens"]
    assert "coef" in out and out["coef"]["T"]["b"] > 0


def test_power_helper_sanity():
    assert oa.mcnemar_power(10, 0.2, 0.75) < oa.mcnemar_power(300, 0.2, 0.75)
    n = oa.n_for_power(0.20, 0.75, 0.8, 0.05)
    assert 100 < n < 300 and oa.mcnemar_power(n + 20, 0.20, 0.75) >= 0.78
    assert oa.n_for_power(0.2, 0.9) < n  # bigger effect -> fewer tasks
    assert oa.power_from_pilot(0, 0, 40)["n"] is None
