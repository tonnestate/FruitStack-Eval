"""Offline tests for runners/ogi013_org_policy.py and the OrgBridge.decide structure-policy hook.

Synthetic inputs: these test policy mechanics, not benchmark outcomes.
Bridge hook: uses a STUB engine (frame dict, add_claim, run, claims.load, ledger.for_claim, workspace.events_path); the real CherryMeEngine is not constructed.
"""
import json
from types import SimpleNamespace

import pytest

from ogi013_org_policy import STRUCTURES, HostStructurePolicy
from ogi013_org_bridge import OrgBridge


def make(mode, tmp_path, **kw):
    return HostStructurePolicy(mode, task_ref=kw.pop("task_ref", "task-1"), domain="airline", store_dir=tmp_path, **kw)


def attest(weights, verdict):
    return {"verdict": verdict}


class Learned:
    def __init__(self, attestation=None, answer="S2", permitted=None):
        self.attestation = attestation
        self.permitted = (attestation or {}).get("verdict") == "LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM" if permitted is None else permitted
        self.answer = answer

    def recommend(self, features):
        return self.answer


def test_off_returns_off_tuple(tmp_path):
    assert make("OFF", tmp_path).choose({}, 0) == (None, None, None, "OFF")


def test_fixed_returns_arm(tmp_path):
    name, ctx, prop, mode = make("FIXED", tmp_path, fixed_arm="S3").choose({}, 5)
    assert (name, ctx, prop, mode) == ("S3", {"challenge": True, "verify": True}, None, "FIXED")


def test_fixed_requires_known_arm(tmp_path):
    with pytest.raises(ValueError):
        make("FIXED", tmp_path, fixed_arm="S9")


def test_randomized_reproducible_covers_all_arms_with_propensity(tmp_path):
    p = make("RANDOMIZED", tmp_path)
    draws = [p.choose({}, i) for i in range(200)]
    assert draws == [make("RANDOMIZED", tmp_path).choose({}, i) for i in range(200)]
    assert {d[0] for d in draws} == set(STRUCTURES)
    assert all(d[2] == 0.25 and d[3] == "RANDOMIZED" for d in draws)
    assert all(d[1] == STRUCTURES[d[0]] for d in draws)


def test_learned_refuses_without_authorization(tmp_path):
    with pytest.raises(RuntimeError, match="LEARNED_POLICY_NOT_AUTHORIZED"):
        make("LEARNED", tmp_path, learned=Learned(attest(None, "LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM")), authorized=False)


def test_learned_refuses_without_learner(tmp_path):
    with pytest.raises(RuntimeError, match="LEARNED_POLICY_NOT_AUTHORIZED"):
        make("LEARNED", tmp_path, learned=None, authorized=True)


def test_learned_refuses_without_attestation(tmp_path):
    with pytest.raises(RuntimeError, match="LEARNED_POLICY_NOT_AUTHORIZED"):
        make("LEARNED", tmp_path, learned=Learned(None), authorized=True)


def test_learned_refuses_when_learner_reports_not_permitted_despite_permitting_verdict(tmp_path):
    # e.g. weight hashes no longer match the attestation: the learner's own permitted flag is False
    with pytest.raises(RuntimeError, match="LEARNED_POLICY_NOT_AUTHORIZED"):
        make("LEARNED", tmp_path, learned=Learned(attest(None, "LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM"), permitted=False), authorized=True)


def test_learned_refuses_non_permitting_verdict(tmp_path):
    with pytest.raises(RuntimeError, match="LEARNED_POLICY_NOT_AUTHORIZED"):
        make("LEARNED", tmp_path, learned=Learned(attest(None, "NOT_BETTER_THAN_BASELINE_OR_MISCALIBRATED")), authorized=True)


def test_learned_works_when_all_present_and_abstain_is_off(tmp_path):
    a = attest(None, "LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM")
    assert make("LEARNED", tmp_path, learned=Learned(a, "S1"), authorized=True).choose({}, 0) == ("S1", {"challenge": True}, None, "LEARNED")
    assert make("LEARNED", tmp_path, learned=Learned(a, None), authorized=True).choose({}, 0) == (None, None, None, "OFF")


def test_decisions_jsonl_append_only_with_spec_fields(tmp_path):
    p = make("FIXED", tmp_path, fixed_arm="S0")
    r1 = p.record_decision(features={"importance": 0.5}, structure="S0", propensity=None, arm_mode="FIXED", claim_id="c1")
    p.finish_decision(r1, accounting={"responsibility_count": 1}, contributions={"PROPOSAL:SUPPORTED": 1}, revised=False,
                      action_changed=False, provider_calls=2, provider_dispatches=2, plumme_ensemble_decision_id="e1")
    path = tmp_path / "training" / "decisions.jsonl"
    before = path.read_bytes()
    p.record_decision(features={}, structure="S1", propensity=None, arm_mode="FIXED", claim_id="c2")
    assert path.read_bytes().startswith(before)
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(rows) == 3
    decision = rows[0]
    assert decision["schema"] == "OGI013-ORG-DECISION/1" and decision["row_id"] == r1
    assert {"task_ref", "domain", "arm_mode", "structure", "propensity", "features", "claim_id", "plumme_ensemble_decision_id", "accounting",
            "contributions", "revised", "action_changed", "provider_calls", "provider_dispatches", "created_at"} <= set(decision)
    assert rows[1]["schema"] == "OGI013-ORG-DECISION-RESULT/1" and rows[1]["row_id"] == r1 and rows[1]["provider_calls"] == 2


class StubLedger:
    def __init__(self, rows):
        self.rows = rows

    def for_claim(self, claim_id):
        return [SimpleNamespace(kind=k, epistemic_status=s, worker=None, answer_text=None) for c, k, s in self.rows if c == claim_id]


class StubEngine:
    def __init__(self, workspace, frame):
        self.frame = frame
        self.seen_context = []
        self.provider_calls = self.provider_dispatches = 0
        self.triage_log = []
        self.workspace = SimpleNamespace(events_path=workspace / "events.jsonl")
        self.ledger = StubLedger([])
        self.claims = SimpleNamespace(load=lambda cid: [SimpleNamespace(status=SimpleNamespace(value="SUPPORTED"))])
        self.added = []

    def add_claim(self, claim):
        self.added.append(claim)
        self.ledger.rows.append((claim.id, "PROPOSAL", "SUPPORTED"))

    def run(self, claim_ids, budget):
        self.seen_context.append(dict(self.frame.get("responsibility_context", {})) if "responsibility_context" in self.frame else "ABSENT")
        self.provider_calls += 2
        self.provider_dispatches += 2
        with self.workspace.events_path.open("a") as f:
            f.write(json.dumps({"claim_id": claim_ids[0], "routing": {"ensemble": {"accounting": {"activation_count": 1},
                                                                                  "plumme_ensemble_decision_id": "pl-7"}}}) + "\n")


def decide_kwargs():
    return dict(description="book the flight", importance=0.4, request="change my seat", transcript="user: hi", tool_results="ok")


def test_bridge_hook_sets_and_removes_context_and_logs(tmp_path):
    bridge = OrgBridge(stack=None, sid="s", task_id="t", policy="policy text", work_dir=tmp_path)
    engine = StubEngine(tmp_path, frame={"responsibility_triage": "auto"})
    bridge.engine = engine
    policy = HostStructurePolicy("FIXED", task_ref="t", domain="airline", store_dir=tmp_path, fixed_arm="S1")
    rec = bridge.decide(**decide_kwargs(), structure_policy=policy, features={"importance": 0.4})
    assert engine.seen_context == [{"challenge": True}]
    assert "responsibility_context" in engine.frame          # FIXED keeps the key set
    off = bridge.decide(**decide_kwargs(), structure_policy=HostStructurePolicy("OFF", task_ref="t", domain="airline", store_dir=tmp_path))
    assert engine.seen_context[-1] == "ABSENT" and "responsibility_context" not in engine.frame
    rows = [json.loads(x) for x in (tmp_path / "training" / "decisions.jsonl").read_text().splitlines()]
    results = [r for r in rows if r["schema"].endswith("RESULT/1")]
    assert [r["plumme_ensemble_decision_id"] for r in results] == ["pl-7"] * 2  # 2 decisions with a policy, OFF still logged
    assert results[0]["accounting"] == {"activation_count": 1} and results[0]["contributions"] == {"PROPOSAL:SUPPORTED": 1}
    assert rec["status"] == "SUPPORTED" and off["status"] == "SUPPORTED"


def test_bridge_without_policy_leaves_frame_untouched(tmp_path):
    bridge = OrgBridge(stack=None, sid="s", task_id="t", policy="p", work_dir=tmp_path)
    engine = StubEngine(tmp_path, frame={"responsibility_context": {"verify": True}})
    bridge.engine = engine
    bridge.decide(**decide_kwargs())
    assert engine.seen_context == [{"verify": True}]
    assert engine.frame == {"responsibility_context": {"verify": True}}
    assert not (tmp_path / "training").exists()
