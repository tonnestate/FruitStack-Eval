"""Model drift epochs from per-call fingerprints (protocol section 6, threat 1).

PlumMe records a `model_fingerprint` on every DecisionOutcome. For each executed offer,
outcomes are ordered by `recorded_at`; every change of fingerprint opens a new epoch.
Effects in a confirmatory analysis are estimated within epochs, so a provider silently
swapping the model behind an unchanged offer cannot masquerade as organizational change.
Outcomes written before fingerprints existed are counted, not guessed.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .decision_log import DecisionView


def detect(views: Iterable[DecisionView]) -> dict:
    by_offer: dict[str, list[tuple[str, str, str | None, str]]] = defaultdict(list)
    missing = 0
    for view in views:
        for outcome in view.outcomes:
            offer = outcome.get("executed_offer_id")
            fingerprint = outcome.get("model_fingerprint")
            if not offer or not fingerprint:
                missing += 1
                continue
            by_offer[offer].append((str(outcome.get("recorded_at") or ""), fingerprint,
                                    outcome.get("provider_reported_model"), view.decision_id))
    offers: dict[str, dict] = {}
    epoch_of: dict[str, dict[str, int]] = defaultdict(dict)
    for offer, rows in sorted(by_offer.items()):
        rows.sort(key=lambda row: row[0])
        epoch, previous, changes = 0, None, []
        for recorded_at, fingerprint, reported, decision_id in rows:
            if previous is not None and fingerprint != previous:
                epoch += 1
                changes.append({"at": recorded_at, "from": previous, "to": fingerprint, "reported_model": reported})
            epoch_of[offer][decision_id] = epoch
            previous = fingerprint
        offers[offer] = {
            "calls": len(rows),
            "distinct_fingerprints": len({row[1] for row in rows}),
            "epochs": epoch + 1,
            "changes": changes,
        }
    drifted = sorted(offer for offer, info in offers.items() if info["changes"])
    warnings = []
    if missing:
        warnings.append("SOME_OUTCOMES_WITHOUT_FINGERPRINT")
    if drifted:
        warnings.append("MODEL_DRIFT_DETECTED_ESTIMATE_WITHIN_EPOCHS")
    return {
        "offers": offers,
        "offers_with_drift": drifted,
        "outcomes_without_fingerprint": missing,
        "epoch_by_offer_and_decision": {offer: dict(m) for offer, m in sorted(epoch_of.items())},
        "warnings": warnings,
    }
