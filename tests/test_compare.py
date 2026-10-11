import pytest

from fruitstack_eval.compare import paired_noninferiority, score_rows, summarize_arms


def result(task_id, arm, passed, subfamily, cost=0.0, quota=2.0):
    return {"task_id": task_id, "arm": arm, "family": "SOFTWARE", "subfamily": subfamily,
            "evidence": {"provenance": "HARNESS_OBSERVED", "tests_total": 1, "tests_passed": int(passed)},
            "quota_units": quota, "cost_eur": cost, "wall_seconds": 10}


def dataset(new_pass_rate_bad=False, clusters=6, per_cluster=30):
    rows = []
    for c in range(clusters):
        for i in range(per_cluster):
            tid = f"c{c}-t{i}"
            ref_pass = i % 10 != 0           # reference: 90 % success
            new_pass = ref_pass if not new_pass_rate_bad else i % 2 == 0  # bad: 50 %
            rows.append(result(tid, "A", ref_pass, f"sub{c}", cost=0.05))
            rows.append(result(tid, "F4", new_pass, f"sub{c}", cost=0.0))
    return rows


def test_parity_supported_when_equal_and_cheaper():
    scored, excluded = score_rows(dataset())
    assert excluded == {}
    h4 = paired_noninferiority(scored, "F4", "A", 0.10, bootstrap=500)
    assert h4["method"] == "cluster_bootstrap_by_subfamily"
    assert h4["mean_success_difference"] == 0.0
    assert h4["non_inferior"] and h4["cheaper_per_success"]
    assert h4["verdict"] == "PARITY_SUPPORTED"


def test_parity_rejected_when_worse():
    scored, _ = score_rows(dataset(new_pass_rate_bad=True))
    h4 = paired_noninferiority(scored, "F4", "A", 0.10, bootstrap=500)
    assert not h4["non_inferior"]
    assert h4["verdict"] == "PARITY_NOT_SUPPORTED"
    assert h4["discordance"] > 0


def test_few_clusters_fall_back_to_task_bootstrap():
    scored, _ = score_rows(dataset(clusters=2))
    h4 = paired_noninferiority(scored, "F4", "A", 0.10, bootstrap=200)
    assert h4["method"] == "task_bootstrap"
    assert "FEWER_THAN_FIVE_SUBFAMILIES_TASK_LEVEL_BOOTSTRAP" in h4["warnings"]


def test_worker_claims_are_excluded_and_duplicates_rejected():
    rows = dataset(clusters=1, per_cluster=2)
    rows.append({**result("x", "A", True, "s"), "evidence": {"provenance": "WORKER_CLAIMED", "tests_total": 1,
                                                             "tests_passed": 1}})
    scored, excluded = score_rows(rows)
    assert excluded == {"NOT_A_LABEL": 1}
    with pytest.raises(ValueError):
        score_rows(rows + [rows[0]])


def test_summary_reports_quota_and_cost():
    scored, _ = score_rows(dataset(clusters=1, per_cluster=10))
    summary = summarize_arms(scored)
    assert summary["A"]["success_rate"] == pytest.approx(0.9)
    assert summary["F4"]["cost_per_success_eur"] == 0.0
    assert summary["A"]["utility_per_quota_unit"] == pytest.approx(9 / 20)
