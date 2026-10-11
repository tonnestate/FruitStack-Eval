from conftest import decision_row, outcome_row
from fruitstack_eval.costaudit import audit
from fruitstack_eval.decision_log import load_views


def test_free_choices_pass(write_log):
    views, _ = load_views(write_log([decision_row("d1"), outcome_row("d1", cost=0.0)]))
    result = audit(views.values())
    assert result.passed and result.choices_audited == 1 and result.outcomes_audited == 1


def test_paid_choice_and_billed_outcome_fail(write_log):
    rows = [decision_row("d1", offer="B", cost_classes={"A": "FREE_TIER", "B": "PREMIUM"}),
            outcome_row("d1", cost=0.02),
            decision_row("d2", offer="A", cost_classes={"A": "UNKNOWN", "B": "FREE_TIER"})]
    views, _ = load_views(write_log(rows))
    result = audit(views.values())
    reasons = sorted(v["reason"] for v in result.violations)
    assert reasons == ["BILLED_OUTCOME", "CHOSEN_OFFER_NOT_FREE", "CHOSEN_OFFER_NOT_FREE"]
    assert not result.passed


def test_empty_log_does_not_pass(write_log):
    views, _ = load_views(write_log([]))
    assert audit(views.values()).passed is False


def test_allowed_classes_are_configurable(write_log):
    views, _ = load_views(write_log([decision_row("d1", cost_classes={"A": "INCLUDED", "B": "FREE_TIER"})]))
    assert not audit(views.values()).passed
    assert audit(views.values(), allowed={"INCLUDED", "FREE_TIER"}).passed
