import json
from pathlib import Path

import pytest


def decision_row(decision_id, *, kind="ACQUIRE", offer="A", pool=("A", "B"), propensity=1.0,
                 mode="DETERMINISTIC", cost_classes=None, family=None, ensemble=None):
    cost_classes = cost_classes or {o: "FREE_TIER" for o in pool}
    features = {"task_family": family} if family else {}
    data = {
        "decision_id": decision_id,
        "kind": kind,
        "request_features": features,
        "candidates": [{"offer_id": o, "cost_class": cost_classes[o]} for o in pool],
        "choices": [] if kind == "ENSEMBLE" else [{
            "slot": 0, "offer_id": offer, "behavior_mode": mode, "propensity": propensity,
            "admissible_offer_ids": list(pool),
        }],
    }
    if ensemble is not None:
        data["ensemble_choice"] = ensemble
    return {"type": "decision", "data": data}


def feedback_row(decision_id, utility, state="VERIFIED"):
    return {"type": "feedback", "data": {"decision_id": decision_id, "verified_utility": utility,
                                         "epistemic_state": state, "verifier": "host"}}


def outcome_row(decision_id, cost=None):
    return {"type": "outcome", "data": {"decision_id": decision_id, "receipt_id": f"r-{decision_id}",
                                        "actual_cost_usd": cost}}


@pytest.fixture
def write_log(tmp_path):
    def _write(rows, name="decisions.jsonl"):
        path = Path(tmp_path) / name
        path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        return path
    return _write
