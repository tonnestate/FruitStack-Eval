from types import SimpleNamespace
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runners import pilot_inquiry


def test_f3_requires_assurance_and_composer_offer():
    args = SimpleNamespace(arm="F3", no_assurance=False, composer_offer=None)
    assert "--composer-offer" in pilot_inquiry.f3_configuration_error(args)
    args.composer_offer = "free-offer"
    args.no_assurance = True
    assert "--no-assurance" in pilot_inquiry.f3_configuration_error(args)
    args.no_assurance = False
    assert pilot_inquiry.f3_configuration_error(args) is None


def test_quota_counts_only_decisions_with_a_provider_choice():
    service = SimpleNamespace(scheduler=SimpleNamespace(decisions=SimpleNamespace(decisions={
        "ensemble": SimpleNamespace(kind="ENSEMBLE", choices=[object()]),
        "denied": SimpleNamespace(kind="ACQUIRE", choices=[]),
        "provider": SimpleNamespace(kind="ACQUIRE", choices=[object()]),
    })))
    assert pilot_inquiry.decision_count(service) == 1


@pytest.mark.parametrize("usd, expected", [(0.0, 0.0), (None, None), (0.01, None)])
def test_eur_cost_is_reported_only_when_usd_receipt_proves_zero(usd, expected):
    assert pilot_inquiry.cost_eur_from_usd(usd) == expected


@pytest.mark.parametrize("receipts, provider_calls, expected", [
    ([], 0, 0.0),
    ([], 1, None),
    ([{"usage": {"cost_usd": 0.0}}], 1, 0.0),
    ([{"usage": {"cost_usd": 0.01}}], 0, None),
    ([{"usage": {"cost_usd": None}}], 1, None),
    ([{"usage": {"cost_usd": 0.01}}], 1, None),
])
def test_f3_cost_requires_zero_cost_for_every_receipt(receipts, provider_calls, expected):
    assert pilot_inquiry.receipt_cost_eur(receipts, provider_calls) == expected
