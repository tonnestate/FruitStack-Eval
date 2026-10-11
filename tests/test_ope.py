import json

import pytest

from conftest import decision_row, feedback_row, outcome_row
from fruitstack_eval.decision_log import load_views
from fruitstack_eval.ope import OPEConfig, TargetPolicy, evaluate, promotion_review


def explore_log(n_each=40):
    rows = []
    for i in range(n_each):
        rows += [decision_row(f"a{i}", offer="A", propensity=0.5, mode="EXPLORE"), feedback_row(f"a{i}", 1.0)]
        rows += [decision_row(f"b{i}", offer="B", propensity=0.5, mode="EXPLORE"), feedback_row(f"b{i}", 0.0)]
    return rows


CFG = OPEConfig(min_support=30, min_ess=20.0, bootstrap=500)


def test_snips_and_ips_recover_known_target_value(write_log):
    views, warnings = load_views(write_log(explore_log()))
    assert warnings == []
    result = evaluate(views.values(), TargetPolicy("deterministic"), CFG)
    assert result.usable_decisions == 80
    assert result.snips == pytest.approx(1.0)
    assert result.ips == pytest.approx(1.0)
    assert result.behavior_mean_utility == pytest.approx(0.5)
    assert result.effective_sample_size == pytest.approx(40.0)
    assert result.support_by_action == {"A": 40}
    assert result.insufficient_support == {}
    assert result.ci_low == pytest.approx(1.0) and result.ci_high == pytest.approx(1.0)


def test_epsilon_target_mixes_actions(write_log):
    views, _ = load_views(write_log(explore_log()))
    result = evaluate(views.values(), TargetPolicy("epsilon_floor", epsilon=0.5), CFG)
    # target puts 0.75 on A and 0.25 on B; utilities 1 and 0
    assert result.snips == pytest.approx(0.75)


def test_clipping_is_reported(write_log):
    rows = [decision_row("x", offer="A", propensity=0.05, mode="EXPLORE"), feedback_row("x", 1.0)]
    views, _ = load_views(write_log(rows))
    result = evaluate(views.values(), TargetPolicy(), OPEConfig(clip=10.0, bootstrap=0))
    assert result.max_raw_weight == pytest.approx(20.0)
    assert result.clipped_weights == 1
    assert "WEIGHTS_CLIPPED_ESTIMATE_BIASED_TOWARD_BEHAVIOR" in result.warnings


def test_insufficient_support_and_low_ess_flagged(write_log):
    views, _ = load_views(write_log(explore_log(n_each=5)))
    result = evaluate(views.values(), TargetPolicy(), OPEConfig(min_support=30, min_ess=100.0, bootstrap=0))
    assert result.insufficient_support == {"A": 5}
    assert "INSUFFICIENT_ACTION_SUPPORT" in result.warnings
    assert "LOW_EFFECTIVE_SAMPLE_SIZE" in result.warnings


def test_ensemble_fixed_count_policy(write_log):
    rows = []
    for i in range(40):
        rows += [decision_row(f"s{i}", kind="ENSEMBLE", ensemble={"worker_count": 1, "propensity": 0.5,
                                                                   "available_counts": [0, 1, 2, 3]}),
                 feedback_row(f"s{i}", 0.4)]
        rows += [decision_row(f"t{i}", kind="ENSEMBLE", ensemble={"worker_count": 3, "propensity": 0.5,
                                                                   "available_counts": [0, 1, 2, 3]}),
                 feedback_row(f"t{i}", 0.9)]
    views, _ = load_views(write_log(rows))
    three = evaluate(views.values(), TargetPolicy("fixed_count", count=3), CFG)
    one = evaluate(views.values(), TargetPolicy("fixed_count", count=1), CFG)
    assert three.snips == pytest.approx(0.9)
    assert one.snips == pytest.approx(0.4)
    assert three.exclusions == {}


def test_exclusions_are_counted(write_log):
    rows = [decision_row("nofb"),
            decision_row("pin", mode="PINNED"), feedback_row("pin", 1.0),
            decision_row("bad", propensity=0.5), feedback_row("bad", 1.5),
            decision_row("fam", family="ECONOMIC", propensity=0.5), feedback_row("fam", 1.0)]
    views, _ = load_views(write_log(rows))
    result = evaluate(views.values(), TargetPolicy(), OPEConfig(family="INQUIRY", bootstrap=0))
    assert result.exclusions == {"NO_VERIFIED_FEEDBACK": 1, "UTILITY_OUT_OF_RANGE": 1, "OTHER_FAMILY": 2}
    assert result.usable_decisions == 0
    assert "NO_USABLE_LABELLED_DECISIONS" in result.warnings


def test_promotion_review_requires_lower_bound_above_incumbent(write_log):
    views, _ = load_views(write_log(explore_log()))
    good = evaluate(views.values(), TargetPolicy("deterministic"), CFG)
    incumbent = evaluate(views.values(), TargetPolicy("epsilon_floor", epsilon=0.5), CFG)
    review = promotion_review(good, incumbent, CFG)
    assert review["eligible_for_host_review"] is True
    reverse = promotion_review(incumbent, good, CFG)
    assert reverse["eligible_for_host_review"] is False


def test_bootstrap_is_deterministic(write_log):
    rows = []
    for i in range(60):
        rows += [decision_row(f"m{i}", offer="A" if i % 2 else "B", propensity=0.5, mode="EXPLORE"),
                 feedback_row(f"m{i}", (i % 5) / 4)]
    views, _ = load_views(write_log(rows))
    first = evaluate(views.values(), TargetPolicy("epsilon_floor", epsilon=0.4), CFG)
    second = evaluate(views.values(), TargetPolicy("epsilon_floor", epsilon=0.4), CFG)
    assert (first.ci_low, first.ci_high) == (second.ci_low, second.ci_high)
    assert first.ci_low <= first.snips <= first.ci_high


def test_reader_handles_segments_orphans_and_bad_lines(tmp_path):
    current = tmp_path / "decisions.jsonl"
    older = tmp_path / "decisions.jsonl.1"
    older.write_text(json.dumps(decision_row("old")) + "\n" + "{not json\n", encoding="utf-8")
    current.write_text("\n".join([json.dumps(feedback_row("old", 1.0)), json.dumps(outcome_row("ghost")),
                                  json.dumps(decision_row("old"))]) + "\n", encoding="utf-8")
    views, warnings = load_views(current)
    assert list(views) == ["old"]
    assert views["old"].latest_feedback()["verified_utility"] == 1.0
    assert any("invalid JSON" in w for w in warnings)
    assert any("orphan outcome" in w for w in warnings)
    assert any("duplicate decision" in w for w in warnings)


@pytest.mark.parametrize("kwargs", [{"selector": "nope"}, {"selector": "fixed_count"},
                                    {"selector": "deterministic", "count": 2}, {"epsilon": 2.0}])
def test_invalid_target_rejected(kwargs):
    with pytest.raises(ValueError):
        TargetPolicy(**kwargs)
