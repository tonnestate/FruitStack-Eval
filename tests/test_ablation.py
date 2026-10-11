import pytest

from fruitstack_eval.ablation import analyze, load_configs
from fruitstack_eval.compare import score_rows


def rows_for(arm, utility_of_task, tasks=30, subfamilies=6):
    rows = []
    for t in range(tasks):
        passed = round(utility_of_task(t) * 10)
        rows.append({"task_id": f"t{t}", "arm": arm, "family": "SOFTWARE", "subfamily": f"s{t % subfamilies}",
                     "evidence": {"provenance": "HARNESS_OBSERVED", "tests_total": 10, "tests_passed": passed},
                     "quota_units": 2.0, "cost_eur": 0.0, "wall_seconds": 1.0})
    return rows


TWO = {"BASE": frozenset(), "A": frozenset({"a"}), "B": frozenset({"b"}), "FULL": frozenset({"a", "b"})}


def two_component_data():
    values = {"BASE": 0.3, "A": 0.5, "B": 0.4, "FULL": 0.7}   # a: +0.2, b: +0.1, interaction: +0.1
    scored, _ = score_rows([r for arm, v in values.items() for r in rows_for(arm, lambda t, v=v: v)])
    return scored


def test_shapley_and_leave_one_out_on_known_effects():
    result = analyze(two_component_data(), TWO, bootstrap=200)
    assert result["leave_one_out"]["a"]["estimate"] == pytest.approx(0.3)
    assert result["leave_one_out"]["b"]["estimate"] == pytest.approx(0.2)
    assert result["total_gain"]["estimate"] == pytest.approx(0.4)
    assert result["interaction_residual"]["estimate"] == pytest.approx(-0.1)
    assert result["shapley"]["a"]["estimate"] == pytest.approx(0.25)
    assert result["shapley"]["b"]["estimate"] == pytest.approx(0.15)
    assert result["shapley_efficiency_gap"] == pytest.approx(0.0)
    assert result["resampling"] == "cluster_bootstrap_by_subfamily"


def test_real_effect_separated_from_null_component():
    configs = {"BASE": frozenset(), "A": frozenset({"a"}), "B": frozenset({"b"}), "FULL": frozenset({"a", "b"})}
    base = lambda t: 0.3 + 0.1 * (t % 3)
    noise = lambda t: 0.1 if t % 2 == 0 else -0.1          # b helps half the tasks, hurts the other half
    arms = {"BASE": base, "A": lambda t: base(t) + 0.2, "B": lambda t: base(t) + noise(t),
            "FULL": lambda t: base(t) + 0.2 + noise(t)}
    scored, _ = score_rows([r for arm, f in arms.items() for r in rows_for(arm, f)])
    result = analyze(scored, configs, bootstrap=1000)
    a, b = result["leave_one_out"]["a"], result["leave_one_out"]["b"]
    assert a["estimate"] == pytest.approx(0.2) and a["excludes_zero"] and a["p_holm"] < 0.05
    assert b["estimate"] == pytest.approx(0.0) and not b["excludes_zero"] and b["p_holm"] > 0.05
    assert result["shapley"]["b"]["ci_low"] < 0 < result["shapley"]["b"]["ci_high"]


def test_incomplete_factorial_keeps_available_leave_one_out():
    configs = {k: v for k, v in TWO.items() if k != "B"}
    scored = [r for r in two_component_data() if r["arm"] != "B"]
    result = analyze(scored, configs, bootstrap=200)
    assert "shapley" not in result
    assert "SHAPLEY_UNAVAILABLE_FULL_FACTORIAL_INCOMPLETE" in result["warnings"]
    assert result["leave_one_out_missing"] == ["a"]
    assert result["leave_one_out"]["b"]["estimate"] == pytest.approx(0.2)


def test_full_system_arm_is_required():
    with pytest.raises(ValueError):
        analyze(two_component_data(), {k: v for k, v in TWO.items() if k != "FULL"}, bootstrap=200)


def test_only_tasks_present_in_every_arm_are_used():
    scored = [r for r in two_component_data() if not (r["arm"] == "A" and r["task_id"] == "t0")]
    result = analyze(scored, TWO, bootstrap=200)
    assert result["paired_tasks"] == 29 and result["tasks_not_in_every_arm"] == 1


def test_utility_per_quota_metric():
    result = analyze(two_component_data(), TWO, metric="utility_per_quota", bootstrap=200)
    assert result["leave_one_out"]["a"]["estimate"] == pytest.approx(0.15)   # 0.3 utility per task / 2 quota units


def test_config_file_validation(tmp_path):
    path = tmp_path / "arms.toml"
    path.write_text('[arms]\nBASE = []\nFULL = ["a", "b"]\nDUP = ["b", "a"]\n', encoding="utf-8")
    with pytest.raises(ValueError):
        load_configs(path)
    path.write_text('[arms]\nBASE = []\nFULL = ["a"]\n', encoding="utf-8")
    assert load_configs(path) == {"BASE": frozenset(), "FULL": frozenset({"a"})}


def test_component_registry_is_well_formed():
    import tomllib
    from pathlib import Path
    data = tomllib.loads((Path(__file__).resolve().parent.parent / "config" / "components.toml").read_text(encoding="utf-8"))
    statuses = {name: c["switch_status"] for name, c in data["component"].items()}
    assert set(statuses.values()) <= {"VERIFIED", "INJECTABLE", "MISSING", "UNVERIFIED"}
    assert all({"repo", "off", "where", "switch_status"} <= set(c) for c in data["component"].values())
