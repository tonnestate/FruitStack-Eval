from conftest import decision_row
from fruitstack_eval.decision_log import load_views
from fruitstack_eval.drift import detect


def outcome(decision_id, offer, fingerprint, at, reported="m"):
    return {"type": "outcome", "data": {"decision_id": decision_id, "receipt_id": f"r-{decision_id}",
                                        "executed_offer_id": offer, "model_fingerprint": fingerprint,
                                        "provider_reported_model": reported, "recorded_at": at}}


def test_fingerprint_change_opens_new_epoch(write_log):
    rows = []
    for i, (fp, at) in enumerate([("aa", "2026-11-01T10:00:00+00:00"), ("aa", "2026-11-02T10:00:00+00:00"),
                                  ("bb", "2026-11-03T10:00:00+00:00"), ("bb", "2026-11-04T10:00:00+00:00")]):
        rows += [decision_row(f"d{i}"), outcome(f"d{i}", "offer-A", fp, at, reported="vendor/m-v2" if fp == "bb" else "vendor/m-v1")]
    rows += [decision_row("e0"), outcome("e0", "offer-B", "cc", "2026-11-01T11:00:00+00:00")]
    rows += [decision_row("old"), {"type": "outcome", "data": {"decision_id": "old", "executed_offer_id": "offer-B"}}]
    views, _ = load_views(write_log(rows))
    result = detect(views.values())
    assert result["offers"]["offer-A"]["epochs"] == 2
    assert result["offers"]["offer-A"]["changes"] == [{"at": "2026-11-03T10:00:00+00:00", "from": "aa", "to": "bb",
                                                       "reported_model": "vendor/m-v2"}]
    assert result["offers"]["offer-B"]["epochs"] == 1
    assert result["offers_with_drift"] == ["offer-A"]
    assert result["epoch_by_offer_and_decision"]["offer-A"] == {"d0": 0, "d1": 0, "d2": 1, "d3": 1}
    assert result["outcomes_without_fingerprint"] == 1
    assert set(result["warnings"]) == {"SOME_OUTCOMES_WITHOUT_FINGERPRINT", "MODEL_DRIFT_DETECTED_ESTIMATE_WITHIN_EPOCHS"}


def test_out_of_order_rows_are_sorted_by_time(write_log):
    rows = [decision_row("late"), outcome("late", "o", "bb", "2026-11-05T00:00:00+00:00"),
            decision_row("early"), outcome("early", "o", "aa", "2026-11-01T00:00:00+00:00")]
    views, _ = load_views(write_log(rows))
    result = detect(views.values())
    assert result["epoch_by_offer_and_decision"]["o"] == {"early": 0, "late": 1}
