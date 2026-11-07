"""OGI-013 offline round trip: real PlumMe DecisionLog <-> organisational learning loop.

ALL DATA IN THIS FILE IS SYNTHETIC TEST DATA (task 'syn-task-1', fake grader ref, fake hashes).
It proves PLUMBING only (record -> attribute -> read back -> build_ensemble -> idempotent re-attribution).
It is NOT a scientific result about organisational structure.

No network, no provider calls: PlumMeService is built with adapters=[] and a temp PLUMME_STATE_DIR.

Run: cd /root/fruits/integration/ogi013-org && PYTHONPATH=runners:.:/root/fruits/integration/ogi013-cherry-org:/root/fruits/integration/ogi013-plum-org/src:/root/fruits/integration/ogi013-peach-org/src /root/fruits/integration/ogi013-hostpython-org/bin/python -m pytest -q tests/test_ogi013_decisionlog_roundtrip.py
"""
import pytest

pytest.importorskip("plumme")  # needs the FruitStack components (CI installs only this repo)
from ogi013_org_learning import attribute_episode_outcome

from plumme.keras_data import build_ensemble
from plumme.service import PlumMeService
from plumme.config import Settings


def test_decisionlog_roundtrip_is_real_and_idempotent(tmp_path, monkeypatch):
    monkeypatch.setenv("PLUMME_STATE_DIR", str(tmp_path / "plumme-state"))
    settings = Settings.load()
    service = PlumMeService(settings, adapters=[])

    # (2) real ENSEMBLE decision through the real service validation
    created = service.record_consumer_ensemble_decision(
        question_id="Q-test-1", claim_revision=0, question_type="FALSIFY",
        skill_digest="ab" * 32, topology="SINGLE", worker_count=1,
        candidate_offer_ids=[], independent_groups=[],
        available_counts=[0, 1],
    )
    decision_id = created["decision_id"]
    assert created["kind"] == "ENSEMBLE"

    # (3) real service.record_decision_feedback via the runner
    store_dir = tmp_path / "store"
    row = attribute_episode_outcome(
        service, task_ref="syn-task-1", domain="synthetic", reward=1.0,
        grader_ref="tau2-official-grader", result_sha256="ab" * 32,
        decision_ids=[decision_id], store_dir=store_dir,
    )
    assert row["reward"] == 1.0
    assert row["epistemic_state"] == "VERIFIED"

    # (4) read back from the real DecisionLog
    view = service.decision_view(decision_id)
    feedback = view.get("feedback") or []
    assert len(feedback) == 1, feedback
    fb = feedback[-1]
    assert fb["epistemic_state"] == "VERIFIED"
    assert fb["verified_utility"] == 1.0
    assert fb["scope"] == "ENSEMBLE"
    assert fb["verifier"] == "tau2-official-grader"
    supply_regime_id = view["decision"]["supply_regime_id"]

    # (5) training-table join over the real log
    ds = build_ensemble(service.scheduler.decisions, supply_regime_id)
    assert len(ds.rows) == 1, (ds.rows, ds.exclusions)
    assert ds.rows[0]["label_verified_ensemble_utility"] == 1.0
    assert ds.rows[0]["worker_count"] == 1

    # (6) idempotent: second attribution writes no second feedback line
    again = attribute_episode_outcome(
        service, task_ref="syn-task-1", domain="synthetic", reward=1.0,
        grader_ref="tau2-official-grader", result_sha256="ab" * 32,
        decision_ids=[decision_id], store_dir=store_dir,
    )
    assert again == row
    assert len(service.decision_view(decision_id).get("feedback") or []) == 1
    lines = (store_dir / "training" / "outcomes.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
