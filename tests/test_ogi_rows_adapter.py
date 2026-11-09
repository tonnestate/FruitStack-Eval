import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import ogi_analyze as oa  # noqa: E402
import ogi_rows_adapter as ad  # noqa: E402


def rec(model, lin, ok=True, stage="solve", i=100, o=50):
    return {"stage": stage, "ok": ok, "model_key": model, "independence_key": lin, "receipt_id": "r", "prefer": model,
            "input_tokens": i, "output_tokens": o}


# Real driver row shape (run_episode / run_samples / run_multi after grade_after), trimmed.
def drow(task, arm, reward, models=("a", "b"), valid=True, effect=None, why=None):
    rc = [rec(m, f"L{m}") for m in models]
    r = {"task": task, "arm": arm, "answer": "x", "how": "SELECTED", "calls": len(rc), "failures": 0, "seconds": 1.0,
         "members": [{"lineage": f"L{m}", "first": "x", "final": "x"} for m in models], "receipts": rc,
         "tokens": {"input": 100 * len(rc), "output": 50 * len(rc), "calls_without_tokens": 0},
         "identity_valid": valid, "exclusion": None if valid else f"INFRA_IDENTITY:{why}", "reward": reward}
    if effect:
        r["effect"] = effect
    return r


def test_mapping_and_exclusion_reason():
    eff = {"class": "CORRECTED", "corrected_members": 1, "damaged_members": 0, "first_correct": 0, "members": 2}
    rows = [drow("t1", "T", 1.0, effect=eff), drow("t1", "S", 0.0, ("a",)),
            drow("t1", "E_div", 0.0, valid=False, why="SINGLE_LINEAGE_ROW"),
            drow("t1", "applied", 1.0), drow("t1", "R_mono", None)]
    out = ad.adapt_rows(rows, "F1")
    by = {r["arm"]: r for r in out}
    assert by["T"]["correct"] and by["T"]["member_first_correct"] == [False, False] and by["T"]["tokens_in"] == 200
    assert by["S_a"]["valid"] and by["T"]["family"] == "F1"
    assert by["E_div"]["exclusion"] == "INFRA_IDENTITY:SINGLE_LINEAGE_ROW" and not by["E_div"]["valid"]
    assert by["applied"]["exclusion"] == "NOT_STUDY_ARM:applied"
    assert by["R_mono"]["exclusion"] == "NOT_GRADED"
    _, ex = oa.split_valid(out)
    assert ex["n_excluded"] == 3 and ex["by_reason"]["INFRA_IDENTITY:SINGLE_LINEAGE_ROW"] == 1


def test_study_roles_contrasts_in_one_holm_family():
    rows = []
    for i in range(60):
        t = f"t{i}"
        eff = {"first_correct": 0, "members": 2}
        rows += [drow(t, "T", 1.0, effect=eff), drow(t, "E_div", float(i % 2)), drow(t, "R_mono", float(i % 3 == 0), ("a",)),
                 drow(t, "G_mas", float(i % 2)), drow(t, "S", float(i % 4 == 0), ("a",)), drow(t, "S", 0.0, ("b",))]
    # S rows of two members share arm names only per model: S_a / S_b
    rep = oa.analyze(ad.adapt_rows(rows, "F1"), roles=oa.STUDY_ROLES)
    c = rep["families"]["F1"]["contrasts"]
    for k in ("primary:T_vs_E", "secondary:H3_E_vs_R_mono", "secondary:H3_R_mono_vs_best_single",
              "secondary:G_mas_vs_E", "secondary:T_vs_G_mas"):
        assert k in c and "p_holm" in c[k]
    assert c["primary:T_vs_E"]["reject"] and c["secondary:T_vs_G_mas"]["reject"]
    assert [k for k in c if k.startswith("primary")] == ["primary:T_vs_E"]
