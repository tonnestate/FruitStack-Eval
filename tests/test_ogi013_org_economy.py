"""Economy mode (runners/ogi013_org_economy.py + OrgBridge.decide + the agent's _org_decide): escalation needs a stated purpose and a yield, retries stop once a failure is known.
Offline: a FAKE engine spends no inference; every number below is counted by the fake. Synthetic data only."""
import json
from types import SimpleNamespace

import pytest

pytest.importorskip("cherryme")
from ogi013_org_bridge import OrgBridge
from ogi013_org_economy import DEFAULTS, EconomyGate


class FakeEngine:
    """Spends `per_run` dispatches per run, honours call_budget like the real engine (limit on its CUMULATIVE provider_dispatches), delivers or fails on demand."""

    def __init__(self, tmp, deliver=True, dissent=False, per_run=3):
        self.frame, self.triage_log = {}, []
        self.provider_calls = self.provider_dispatches = 0
        self.workspace = SimpleNamespace(events_path=tmp / "events.jsonl")
        self.claims = self.ledger = self
        self.rows, self.runs = {}, []
        self.deliver, self.dissent, self.per_run = deliver, dissent, per_run

    def add_claim(self, claim):
        self.rows[claim.id] = []

    def run(self, claim_ids, **kw):
        self.runs.append(kw)
        cap = kw.get("call_budget")
        spend = self.per_run if cap is None else max(0, min(self.per_run, cap - self.provider_dispatches))
        self.provider_dispatches += spend
        self.provider_calls += spend
        for cid in claim_ids:
            for _ in range(spend):
                ok = self.deliver
                self.rows[cid].append(SimpleNamespace(worker="w", kind="PROPOSAL" if ok else "ATTEMPT_FAILED", epistemic_status="UNVERIFIED", answer_text="", identity={}))
            if self.dissent and spend:
                self.rows[cid].append(SimpleNamespace(worker="w2", kind="PROPOSAL", epistemic_status="DISSENT", answer_text="the action violates the policy", identity={}))

    def load(self, cid):
        return [SimpleNamespace(status=SimpleNamespace(value="UNKNOWN"))]

    def for_claim(self, cid):
        return self.rows.get(cid, [])


def bridge_with(tmp, **kw):
    bridge = OrgBridge(stack=None, sid="s", task_id="2", policy="policy text", work_dir=tmp)
    bridge.engine = FakeEngine(tmp, **kw)
    return bridge


def agent_decide(bridge, gate, action, state=None, uncertain=False):
    """The real FruitStackTau2Agent._org_decide with a minimal fake self/episode (needs the tau2 host environment)."""
    pytest.importorskip("tau2")
    from ogi013_tau2_agent import FruitStackTau2Agent
    events = []
    ep = SimpleNamespace(economy=gate, org=bridge, stats={"escalations": 0, "revisions": 0}, turns=1, event=lambda kind, **d: events.append((kind, d)),
                         step=lambda *a, **k: {"success": False, "output": ""})
    me = SimpleNamespace(write_tools={"book_reservation", "cancel_reservation"}, _abandon_unresolved=lambda e: None)
    state = state or {"transcript": ["USER: please look up SDZQKO", "TOOL RESULT: reservation SDZQKO confirmed"]}
    out = FruitStackTau2Agent._org_decide(me, ep, "prompt", action, state, uncertain=uncertain)
    return out, events


READ = {"action": "tool", "name": "get_reservation_details", "arguments": {"reservation_id": "SDZQKO"}}
WRITE = {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "SDZQKO"}}
MSG = {"action": "message", "content": "Your reservation is confirmed."}


# ---- gate rules ------------------------------------------------------------------------------------------------------------------------------------------------

def test_simple_task_is_not_escalated_but_consequential_and_uncertain_ones_are():
    g = EconomyGate()
    assert g.should_escalate(kind="READ") == (False, "simple_task") and g.should_escalate(kind="MESSAGE") == (False, "simple_task")
    assert g.should_escalate(kind="WRITE") == (True, "consequential_effect") and g.should_escalate(kind="TRANSFER") == (True, "consequential_effect")
    assert g.should_escalate(kind="READ", uncertain=True) == (True, "draft_uncertainty")
    assert g.should_escalate(kind="MESSAGE", alert=1) == (True, "observed_uncertainty")
    assert g.should_escalate(kind="MESSAGE", prior_dissents=1) == (True, "observed_uncertainty")


def test_allowances_leave_room_for_a_quorum_and_a_third_judge():
    assert DEFAULTS["primary_calls"] >= 3 and DEFAULTS["atom_calls"] >= 3          # difficult tasks can still recruit >= 2 independent workers + a tie-breaker


def test_delegation_stops_after_unproductive_escalations_but_consequential_actions_still_escalate():
    g = EconomyGate()
    for _ in range(g.unproductive_limit):
        assert g.should_escalate(kind="READ", uncertain=True)[0]
        g.note_outcome({"delivered": 2, "status": "UNKNOWN", "dissent": [], "atoms": [], "dispatch_total": 3}, "draft_uncertainty")
    assert g.should_escalate(kind="READ", uncertain=True) == (False, "no_new_information")
    assert g.should_escalate(kind="WRITE")[0] is True
    g.note_outcome({"delivered": 2, "status": "REFUTED", "dissent": [], "atoms": [], "dispatch_total": 3}, "consequential_effect")      # a decision-relevant contribution re-opens cooperation
    assert g.should_escalate(kind="READ", uncertain=True) == (True, "draft_uncertainty")


def test_known_supply_failure_stops_non_consequential_escalation_and_atoms():
    g = EconomyGate()
    for _ in range(g.supply_fail_limit):
        g.note_outcome({"delivered": 0, "status": "UNKNOWN", "dissent": [], "atoms": [], "dispatch_total": 6}, "consequential_effect")
    assert g.should_escalate(kind="MESSAGE", alert=2) == (False, "known_supply_failure")
    assert g.should_escalate(kind="WRITE")[0] is True
    assert g.plan_atoms([{"value": "SDZQKO"}], kind="WRITE") == []


def test_a_value_is_never_verified_twice_and_simple_actions_buy_no_atoms():
    g = EconomyGate()
    assert g.plan_atoms([{"value": "SDZQKO"}], kind="READ") == []
    assert [a["value"] for a in g.plan_atoms([{"value": "SDZQKO"}, {"value": "4OG6T3"}], kind="WRITE")] == ["SDZQKO", "4OG6T3"]
    assert g.plan_atoms([{"value": "SDZQKO"}], kind="WRITE") == [] and g.skipped["duplicate_evidence_request"] == 1


# ---- through the real bridge / agent path -------------------------------------------------------------------------------------------------------------

def test_simple_tasks_trigger_no_model_escalation_at_all(tmp_path):
    bridge, gate = bridge_with(tmp_path), EconomyGate()
    for action in [READ, MSG] * 6:
        out, events = agent_decide(bridge, gate, action)
        assert out is action and events[-1][0] == "ORG_SKIPPED" and events[-1][1]["reason"] == "simple_task"
    assert bridge.engine.runs == [] and bridge.engine.provider_dispatches == 0


def test_difficult_actions_are_escalated_with_a_stated_purpose_and_a_dispatch_allowance(tmp_path):
    bridge, gate = bridge_with(tmp_path, dissent=True), EconomyGate()
    out, events = agent_decide(bridge, gate, WRITE)
    kinds = [k for k, _ in events]
    assert "ORG_DECISION" in kinds and bridge.decisions[0]["purpose"] == "consequential_effect"
    assert bridge.engine.runs[0]["call_budget"] == 0 + gate.primary_calls                    # engine counters are cumulative: allowance = dispatches so far + primary_calls
    out, events = agent_decide(bridge, gate, MSG)                                          # an earlier dissent raised the alert: the same plain message is now justified
    assert bridge.decisions[-1]["purpose"] == "observed_uncertainty"


def test_failing_providers_cannot_cause_unbounded_retries(tmp_path):
    actions = ([WRITE] + [MSG] * 9) * 4
    (tmp_path / "a").mkdir()
    frozen = bridge_with(tmp_path / "a", deliver=False, per_run=50)
    frozen.alert = 1
    for action in actions:                                                                  # frozen path: every decision is escalated and nothing bounds the attempts
        frozen.decide(description="x", importance=0.9 if action is WRITE else 0.3, request="r", transcript="t", tool_results="tr", atoms=[])
    econ_dir = tmp_path / "b"
    econ_dir.mkdir()
    econ, gate = bridge_with(econ_dir, deliver=False, per_run=50), EconomyGate()
    econ.alert = 1
    for action in actions:
        agent_decide(econ, gate, action)
    bound = (4 + gate.supply_fail_limit) * (gate.primary_calls + 2 * gate.atom_calls)
    assert econ.engine.provider_dispatches <= bound < frozen.engine.provider_dispatches
    assert gate.skipped.get("known_supply_failure", 0) >= 30


def test_frozen_path_is_unchanged_without_economy(tmp_path):
    bridge = bridge_with(tmp_path)
    rec = bridge.decide(description="x", importance=0.3, request="r", transcript="t", tool_results="tr")
    assert bridge.engine.runs == [{"budget": 8}] and "economy" not in rec and rec["purpose"] is None
