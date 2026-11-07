"""Mechanics tests for the OGI-013 organisational learner.

ALL DATA IN THIS FILE IS SYNTHETIC. These tests prove that the pipeline runs, joins, refuses and records correctly.
They are NOT scientific evidence about organisational structure. Real verdicts come only from real store data.

Run: PYTHONPATH=runners:.:/root/fruits/integration/ogi013-cherry-org:/root/fruits/integration/ogi013-plum-org/src \
     KERAS_BACKEND=jax /root/SUPPLY-001/venv3.12/bin/python -m pytest -q tests/test_ogi013_org_learning.py
"""
import hashlib
import importlib.util
import json
import random
from pathlib import Path

import pytest

pytest.importorskip("plumme")  # needs the FruitStack components (CI installs only this repo)
pytest.importorskip("cherryme")

from ogi013_org_learning import (DECISION_SCHEMA, OUTCOME_SCHEMA, RESULT_SCHEMA, attribute_episode_outcome,
                                 load_training_table)
from train_org_policy import KINDS, PERMITTED, OrgPolicy, run

HAS_KERAS = importlib.util.find_spec("keras") is not None
needs_keras = pytest.mark.skipif(not HAS_KERAS, reason="keras not importable in this interpreter")
GATE = Path(__file__).resolve().parents[1] / "evidence" / "ogi013-learning" / "ORG_GATE_V1.json"


class FakeService:
    """SYNTHETIC stand-in for plumme PlumService.record_decision_feedback."""

    def __init__(self):
        self.calls = []
        self.feedback = {}

    def record_decision_feedback(self, **kw):
        self.calls.append(kw)
        self.feedback.setdefault(kw["decision_id"], []).append(kw)
        return {"ok": True}

    def decision_view(self, decision_id):
        return {"feedback": list(self.feedback.get(decision_id, []))}


def _features(rng, kind="READ"):
    return {"importance": round(rng.random(), 3), "kind": kind, "step_index": rng.randrange(10), "prior_alerts": rng.randrange(4),
            "n_prior_org_decisions": rng.randrange(30), "n_prior_dissents": rng.randrange(5)}


def _write_store(store: Path, tasks: list[dict]):
    """tasks: [{task_ref, arm, structure, kind, reward, n}] - SYNTHETIC."""
    t = store / "training"
    t.mkdir(parents=True, exist_ok=True)
    rng = random.Random(7)
    with (t / "decisions.jsonl").open("w") as fd, (t / "decision_results.jsonl").open("w") as fr, (t / "outcomes.jsonl").open("w") as fo:
        for spec in tasks:
            for i in range(spec.get("n", 10)):
                rid = f"{spec['task_ref']}-{i}"
                fr.write(json.dumps({"schema": RESULT_SCHEMA, "row_id": rid, "task_ref": spec["task_ref"], "action_changed": False}) + "\n")
                fd.write(json.dumps({"schema": DECISION_SCHEMA, "row_id": rid, "task_ref": spec["task_ref"], "domain": "synthetic", "arm_mode": spec["arm"],
                                     "structure": spec["structure"], "propensity": 0.25 if spec["arm"] == "RANDOMIZED" else None,
                                     "features": _features(rng, spec["kind"])}) + "\n")
            if spec.get("reward") is not None:
                fo.write(json.dumps({"schema": OUTCOME_SCHEMA, "task_ref": spec["task_ref"], "reward": spec["reward"],
                                     "epistemic_state": "VERIFIED", "grader_result_sha256": "ab" * 32}) + "\n")


def test_attribution_credits_each_decision_once_and_is_idempotent(tmp_path):
    svc = FakeService()
    kw = dict(task_ref="T1", domain="synthetic", reward=1.0, grader_ref="tau2-official-grader", result_sha256="cd" * 32,
              decision_ids=["d1", "d2"], store_dir=tmp_path)
    first = attribute_episode_outcome(svc, **kw)
    assert [c["decision_id"] for c in svc.calls] == ["d1", "d2"]
    assert all(c["scope"] == "ENSEMBLE" and c["attribution_basis"] == "EPISODE_OFFICIAL_GRADER" and c["epistemic_state"] == "VERIFIED"
               and c["verified_utility"] == 1.0 and c["verifier"] == "tau2-official-grader" for c in svc.calls)
    second = attribute_episode_outcome(svc, **kw)
    assert len(svc.calls) == 2                       # repeat wrote nothing to the service
    assert second == first
    lines = (tmp_path / "training" / "outcomes.jsonl").read_text().splitlines()
    assert len(lines) == 1 and json.loads(lines[0])["schema"] == OUTCOME_SCHEMA


def test_attribution_retry_deduplicates_feedback_after_partial_failure(tmp_path):
    class FailOnceAfterPersist(FakeService):
        failed = False

        def record_decision_feedback(self, **kw):
            result = super().record_decision_feedback(**kw)
            if kw["decision_id"] == "d1" and not self.failed:
                self.failed = True
                raise RuntimeError("simulated interruption after durable feedback append")
            return result

    svc = FailOnceAfterPersist()
    kw = dict(task_ref="T-retry", domain="synthetic", reward=0.75, grader_ref="tau2-official-grader",
              result_sha256="ef" * 32, decision_ids=["d1", "d2"], store_dir=tmp_path)
    with pytest.raises(RuntimeError, match="simulated interruption"):
        attribute_episode_outcome(svc, **kw)

    row = attribute_episode_outcome(svc, **kw)
    assert [call["decision_id"] for call in svc.calls] == ["d1", "d2"]
    assert all(call["scope"] == "ENSEMBLE" for call in svc.calls)
    assert len((tmp_path / "training" / "outcomes.jsonl").read_text().splitlines()) == 1
    assert row["decision_ids"] == ["d1", "d2"]


def test_verified_episode_feedback_replays_through_plumme_across_tasks(tmp_path):
    from types import SimpleNamespace

    from plumme.decisions import DecisionLog
    from plumme.policy import KerasShadowPolicy
    from plumme.service import PlumMeService

    decision_path = tmp_path / "plumme-decisions.jsonl"

    def service():
        out = object.__new__(PlumMeService)
        out.scheduler = SimpleNamespace(decisions=DecisionLog(decision_path))
        out.scheduler.decisions.subscribe(KerasShadowPolicy())
        return out

    svc = service()
    ids = []
    for task_ref, reward in (("task-one", 1.0), ("task-two", 0.0)):
        decision = svc.record_consumer_ensemble_decision(
            question_id=task_ref, claim_revision=0, question_type="SCIENCE", skill_digest="d" * 64,
            topology="SINGLE", worker_count=1, candidate_offer_ids=["model-a"], independent_groups=["family-a"],
            available_counts=[0, 1], selected_model_keys=["model-a"],
        )
        ids.append(decision["decision_id"])
        attribute_episode_outcome(
            svc, task_ref=task_ref, domain="offline", reward=reward, grader_ref="tau2-official-grader",
            result_sha256=("a" if reward else "b") * 64, decision_ids=[decision["decision_id"]],
            store_dir=tmp_path / "ogi-store",
        )

    resumed = service()
    assert [resumed.decision_view(did)["verified_utility"] for did in ids] == [1.0, 0.0]
    shadow = resumed.scheduler.decisions.subscribers[0]
    assert [row["verified_utility"] for row in shadow.ensemble_rows] == [1.0, 0.0]
    assert shadow.model_quality == {}  # ensemble outcomes do not fabricate worker competence


@pytest.mark.parametrize("field,value", [
    ("domain", "other-domain"),
    ("reward", 0.25),
    ("grader_ref", "other-grader"),
    ("decision_ids", ["d2"]),
])
def test_same_result_hash_rejects_conflicting_verified_outcome(tmp_path, field, value):
    svc = FakeService()
    kw = dict(task_ref="T-conflict", domain="synthetic", reward=0.75, grader_ref="tau2-official-grader",
              result_sha256="cd" * 32, decision_ids=["d1"], store_dir=tmp_path)
    attribute_episode_outcome(svc, **kw)

    with pytest.raises(ValueError, match="CONFLICTING_EPISODE_OUTCOME"):
        attribute_episode_outcome(svc, **{**kw, field: value})
    assert [call["decision_id"] for call in svc.calls] == ["d1"]


@pytest.mark.parametrize("bad", [1.5, -0.1, float("nan"), True, "1.0"])
def test_attribution_refuses_reward_outside_unit_interval(tmp_path, bad):
    with pytest.raises(ValueError):
        attribute_episode_outcome(FakeService(), task_ref="T", domain="d", reward=bad, grader_ref="g", result_sha256="x",
                                  decision_ids=["d1"], store_dir=tmp_path)


def test_join_keeps_only_verified_randomized_as_trainable(tmp_path):
    _write_store(tmp_path, [  # SYNTHETIC
        {"task_ref": "ok", "arm": "RANDOMIZED", "structure": "S3", "kind": "WRITE", "reward": 1.0, "n": 2},
        {"task_ref": "fixed_arm", "arm": "FIXED", "structure": "S0", "kind": "READ", "reward": 0.0, "n": 2},
        {"task_ref": "no_outcome", "arm": "RANDOMIZED", "structure": "S1", "kind": "READ", "reward": None, "n": 2},
    ])
    table = load_training_table(tmp_path)
    assert len(table) == 6                           # all rows returned
    trainable = {r["task_ref"] for r in table if r["eligible_for_training"]}
    assert trainable == {"ok"}
    ok_row = next(r for r in table if r["task_ref"] == "ok")
    assert ok_row["reward"] == 1.0 and ok_row["result"]["action_changed"] is False


def test_too_few_rows_refuses_with_insufficient_evidence_and_no_weights(tmp_path):
    _write_store(tmp_path / "store", [  # SYNTHETIC: 2 tasks, far below min_rows
        {"task_ref": f"s{i}", "arm": "RANDOMIZED", "structure": ["S0", "S1", "S2", "S3"][i % 4], "kind": "READ", "reward": 1.0} for i in range(2)])
    out = tmp_path / "out"
    att = run(tmp_path / "store", GATE, out)
    assert att["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert att["weights"] is None
    assert not list(out.glob("weights*"))
    on_disk = json.loads((out / "attestation.json").read_text())
    assert on_disk["verdict"] == "INSUFFICIENT_EVIDENCE" and on_disk["failed_checks"]


def test_orgpolicy_abstains_when_attestation_does_not_permit(tmp_path):
    (tmp_path / "attestation.json").write_text(json.dumps({"verdict": "NOT_BETTER_THAN_BASELINE_OR_MISCALIBRATED", "weights": None}))
    pol = OrgPolicy(tmp_path)
    assert pol.attestation["verdict"].startswith("NOT_BETTER")
    assert pol.recommend({"importance": 0.5, "kind": "WRITE", "step_index": 1, "prior_alerts": 0,
                          "n_prior_org_decisions": 0, "n_prior_dissents": 0}) is None
    assert OrgPolicy(tmp_path / "missing").recommend({}) is None


@needs_keras
def test_large_synthetic_run_records_gate_outcome_and_consistent_attestation(tmp_path):
    """SYNTHETIC: 60 tasks x 10 decisions, arm fixed per task (episode-level label). Base success 0.3; +0.3 when S3 on WRITE tasks.
    Records whatever the gate says. Asserts the attestation is complete and hash-consistent, NOT that the gate passes."""
    rng = random.Random(1013)
    tasks = []
    for i in range(60):
        structure = ["S0", "S1", "S2", "S3"][i % 4]
        kind = KINDS[rng.randrange(len(KINDS))]
        p = 0.3 + (0.3 if (structure == "S3" and kind == "WRITE") else 0.0)
        tasks.append({"task_ref": f"syn-{i:03d}", "arm": "RANDOMIZED", "structure": structure, "kind": kind,
                      "reward": 1.0 if rng.random() < p else 0.0, "n": 10})
    store, out = tmp_path / "store", tmp_path / "out"
    _write_store(store, tasks)
    att = run(store, GATE, out)
    for key in ("verdict", "checks", "failed_checks", "thresholds", "counts", "data_sha256", "split", "versions", "activation"):
        assert key in att, key
    assert att["counts"]["eligible_rows"] == 600 and att["counts"]["eligible_tasks"] == 60
    assert att["activation"].startswith("NOT_ACTIVATED")
    if att["weights"] is None:
        pytest.fail(f"expected training to run on 600 rows, got {att['verdict']} {att['failed_checks']}")
    for name, digest in att["weights"]["files"].items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest
    print("SYNTHETIC gate verdict:", att["verdict"], "failed:", att["failed_checks"], "gain:", att["evaluation"]["test"]["logloss_gain_over_best_baseline"])
    pol = OrgPolicy(out)
    feats = {"importance": 0.5, "kind": "WRITE", "step_index": 1, "prior_alerts": 0, "n_prior_org_decisions": 0, "n_prior_dissents": 0}
    if att["verdict"] == PERMITTED:
        assert pol.permitted and pol.recommend(feats) in ("S0", "S1", "S2", "S3")
    else:
        assert not pol.permitted and pol.recommend(feats) is None
