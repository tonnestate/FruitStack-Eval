import json

import pytest

from fruitstack_eval import pilot

REF = "x"


def row(task, arm, grade, sub, status="PARSED", abstained=False, label=True):
    ev = {"provenance": "HARNESS_OBSERVED" if label else "WORKER_CLAIM", "blinded": True, "grade": grade,
          "parse_status": status, "abstained": abstained}
    return {"task_id": task, "arm": arm, "family": "INQUIRY", "subfamily": sub, "evidence": ev,
            "quota_units": 1 if arm == "F1" else 20, "cost_eur": 0.0, "wall_seconds": 1.0}


def data():
    rows = []
    for i in range(50):
        sub = f"S{i % 5}"
        f1 = 1.0 if i % 2 == 0 else 0.5           # F1 succeeds on even tasks
        f3 = 1.0 if i % 5 != 4 else 0.0           # F3 succeeds on 40 of 50
        rows.append(row(f"t{i}", "F1", f1, sub))
        rows.append(row(f"t{i}", "F3", f3, sub, status="NO_STRUCTURED_ANSWER" if f3 == 0 else "PARSED"))
    rows[1]["evidence"]["provenance"] = "WORKER_CLAIM"            # one unverifiable F3 row
    return rows


def test_pilot_estimates_are_descriptive_and_paired():
    result = pilot.analyze(data(), bootstrap=300)
    assert result["descriptive_only"] and "ARM_A_MISSING_NOT_A_COMPLETED_PREREGISTERED_PILOT" in result["warnings"]
    f1, f3 = result["arms"]["F1"], result["arms"]["F3"]
    assert f1["successes"] == 25 and f1["failures"] == 25 and f1["unverifiable"] == 0
    assert f3["unverifiable"] == 1 and f3["labelled_tasks"] == 49 and f3["no_structured_answer"] == 10
    pair = result["pairs"]["F3-F1"]
    assert pair["paired_tasks"] == 49 and pair["resampling"] == "cluster_bootstrap_by_subfamily"
    table = pair["concordance_table"]
    assert sum(table.values()) == 49
    psi = (table["F3_only"] + table["F1_only"]) / 49
    assert pair["discordance_psi"]["estimate"] == pytest.approx(psi)
    assert pair["success_rate_difference"]["estimate"] == pytest.approx((table["F3_only"] - table["F1_only"]) / 49)
    assert pair["discordance_psi"]["ci_low"] <= psi <= pair["discordance_psi"]["ci_high"]
    rows = pair["sample_size_proposal"]["rows"]
    assert rows[0]["margin"] == 0.10 and rows[0]["psi_estimate"]["paired_tasks"] > 0
    assert rows[0]["psi_ci_high"]["paired_tasks"] >= rows[0]["psi_estimate"]["paired_tasks"]
    assert "p_value" not in json.dumps(result)


def test_sample_size_proposal_matches_power_table():
    proposal = pilot.sample_size_proposal(0.2, 0.3)
    ten = proposal["rows"][0]
    assert ten["psi_estimate"]["paired_tasks"] == 157 and ten["psi_ci_high"]["paired_tasks"] == 236
    assert pilot.sample_size_proposal(None, None)["rows"][0]["psi_estimate"] is None
