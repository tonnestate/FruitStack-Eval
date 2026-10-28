"""Collaboration step (runners/ogi013_org_collab.py): SOLVE -> CHALLENGE -> REVISE -> re-examine -> specialist -> CONSOLIDATE with the real cherryme.brother rounds and the real ContributionLedger.
Workers are scripted mocks: no model, no network. Synthetic tasks; these tests prove mechanics and attribution, not benchmark outcomes."""
import hashlib
import json
from types import SimpleNamespace

import pytest

pytest.importorskip("cherryme")
from cherryme.contributions import ContributionLedger
from ogi013_org_collab import collaborate

PROMPT = "POLICY: refunds only within 24h.\nCONVERSATION: user asks to cancel flight HAT001 booked 2h ago.\nYour next action (one JSON object):"
BAD = {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"}}
GOOD = {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"}}


def parse(text):
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else None
    except (TypeError, ValueError):
        return None


def digest(action):
    return hashlib.sha256(json.dumps(action, sort_keys=True).encode()).hexdigest()[:12]


class Workers:
    """Scripted worker pool: `script[stage]` is a list of outputs consumed in order (a string, or None = provider failure). Records every call."""

    def __init__(self, **script):
        self.script = {k: list(v) for k, v in script.items()}
        self.calls = []
        self.n = 0

    def __call__(self, prompt, stage, prefer=None, exclude=()):
        self.calls.append({"stage": stage, "prompt": prompt, "exclude": tuple(exclude), "prefer": prefer})
        self.n += 1
        queue = self.script.get(stage, [])
        out = queue.pop(0) if queue else None
        if out is None:
            return {"success": False, "output": "", "model_key": f"unavailable-{self.n}", "independence_key": None, "receipt_id": f"r{self.n}", "failure_class": "RATE_LIMITED"}
        return {"success": True, "output": out, "model_key": f"{stage}-model-{self.n}", "independence_key": f"lineage-{stage}-{self.n}", "receipt_id": f"r{self.n}", "failure_class": None}

    def stages(self):
        return [c["stage"] for c in self.calls]


def run(workers, seed_action=BAD, max_rounds=2):
    ledger = ContributionLedger()
    seed = {"text": json.dumps(seed_action), "model_key": "draft-model", "independence_key": "lineage-draft", "receipt_id": "r0"}
    out = collaborate(task_prompt=PROMPT, seed=seed, work=workers, ledger=ledger, claim_id="C-1", parse=parse, digest=digest, max_rounds=max_rounds)
    return out, ledger


def test_good_solution_is_independently_validated_without_repeated_escalation():
    w = Workers(challenge=["ISSUES: NONE\nPolicy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION."])
    out, ledger = run(w, seed_action=GOOD)
    assert w.stages() == ["challenge"] and out.calls == 1                         # one independent review, nothing else was asked
    assert out.validated and not out.improved and not out.changed and not out.review_unavailable
    assert [r.kind for r in ledger.rows] == ["SOLUTION", "CRITIQUE"] and ledger.rows[1].epistemic_status == "UNVERIFIED"
    assert out.attribution == [{"role": "critique", "model": "challenge-model-1", "lineage": "lineage-challenge-1", "found_issues": False, "materially_improved": False,
                                "examined": digest(GOOD), "grounds": "Policy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION.", "grounds_stated": True}]
    assert out.agreement[0]["agreed_with"] == digest(GOOD) and out.final_reviewed and not out.ungrounded_agreement       # who agreed, with which answer, on what stated grounds
    assert "state the specific checks" in w.calls[0]["prompt"]                                                              # the reviewer is asked for grounds, not just a verdict
    assert w.calls[0]["exclude"] == ("lineage-draft",)                            # the reviewer is a different lineage than the author


def test_a_bare_agreement_is_recorded_but_is_not_validation():
    w = Workers(challenge=["ISSUES: NONE"])
    out, _ = run(w, seed_action=GOOD)
    assert out.ungrounded_agreement and not out.validated and not out.improved and not out.changed and out.final_action == GOOD
    assert out.agreement == [{"model": "challenge-model-1", "lineage": "lineage-challenge-1", "agreed_with": digest(GOOD), "grounds": "", "grounds_stated": False}]
    wrong = Workers(challenge=["ISSUES: NONE\nLooks fine."])                                                               # grounds are recorded verbatim; agreement on a WRONG answer is still only a claim
    out2, _ = run(wrong, seed_action=BAD)
    assert out2.validated and out2.final_action == BAD and out2.agreement[0]["grounds"] == "Looks fine."


def test_flawed_solution_is_criticised_improved_and_the_revision_is_examined_again():
    w = Workers(challenge=["ISSUES: FOUND\nThe reservation id WRONG1 is not the customer's booking; use HAT001 (see CONVERSATION).", "ISSUES: NONE"], revise=[json.dumps(GOOD)])
    out, ledger = run(w)
    assert w.stages() == ["challenge", "revise", "challenge"]                       # SOLVE(seed) -> CHALLENGE -> REVISE -> CHALLENGE again
    assert PROMPT in w.calls[0]["prompt"] and "WRONG1" in w.calls[0]["prompt"]       # the reviewer sees the task MATERIALS and the actual proposed solution
    assert json.dumps(GOOD) in w.calls[2]["prompt"] and "WRONG1" not in w.calls[2]["prompt"]       # the second review examines the REVISED solution
    assert w.calls[1]["prefer"] == "draft-model"                                     # the author revises their own solution
    assert out.changed and out.improved and not out.validated and out.final_action == GOOD and out.unresolved == []
    assert [r.kind for r in ledger.rows] == ["SOLUTION", "CRITIQUE", "REVISION", "CRITIQUE"]
    assert [r.epistemic_status for r in ledger.rows][1] == "DISSENT"
    roles = {(a["role"], a.get("found_issues"), a.get("materially_improved", a.get("changed_action"))) for a in out.attribution}
    assert ("critique", True, True) in roles and ("revision", None, True) in roles and ("critique", False, False) in roles   # who improved the result, from the ledger


def test_unresolved_disagreement_stays_visible_and_one_specialist_adjudicates():
    w = Workers(challenge=["ISSUES: FOUND\nUse HAT001, WRONG1 is not the booking."], revise=[json.dumps(BAD)], specialist=[json.dumps(BAD)])        # the author rejects, the specialist agrees with the author
    out, ledger = run(w)
    assert w.stages() == ["challenge", "revise", "specialist"] and out.specialist_used
    assert "Use HAT001" in w.calls[2]["prompt"] and set(w.calls[2]["exclude"]) >= {"lineage-draft", "lineage-challenge-1"}       # the dossier carries the objection; further lineages only
    assert not out.changed and not out.improved and not out.validated
    assert len(out.unresolved) == 1 and "HAT001" in out.unresolved[0]["objection"]                  # the objection is NOT dropped
    w2 = Workers(challenge=["ISSUES: FOUND\nUse HAT001.", "ISSUES: NONE\nPolicy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION."], revise=[json.dumps(BAD) + " "], specialist=[json.dumps(GOOD)])      # the author rejects, the specialist sides with the critic
    out2, _ = run(w2)
    assert w2.stages() == ["challenge", "revise", "specialist", "challenge"]                                              # the specialist's answer is examined once more
    assert set(w2.calls[3]["exclude"]) >= {"lineage-draft", "lineage-challenge-1", "lineage-specialist-3"} and json.dumps(GOOD) in w2.calls[3]["prompt"]
    assert out2.changed and out2.improved and out2.final_action == GOOD and out2.unresolved == [] and out2.specialist_used and out2.final_reviewed
    assert out2.overruled == [{"author": "draft-model", "author_position": digest(BAD), "overruled_by": "specialist-model-3", "author_grounds": json.dumps(BAD) + " "}]      # the author's rejection is kept
    assert next(a for a in out2.attribution if a["role"] == "specialist") == {"role": "specialist", "model": "specialist-model-3", "lineage": "lineage-specialist-3",
                                                                              "changed_action": True, "grounds": json.dumps(GOOD)}
    w3 = Workers(challenge=["ISSUES: FOUND\nUse HAT001.", "ISSUES: FOUND\nHAT001 is a flight number, not a reservation id."], revise=[json.dumps(BAD)], specialist=[json.dumps(GOOD)])
    out3, _ = run(w3)                                                                                                    # the re-review objects to the specialist's answer: it stays visible, the answer is not called reviewed
    assert out3.changed and not out3.final_reviewed and len(out3.unresolved) == 1 and "flight number" in out3.unresolved[0]["objection"]


def test_unavailable_workers_cause_no_retry_loop_and_are_never_counted_as_agreement():
    w = Workers(challenge=[None, None, None, None], revise=[None], specialist=[None])
    out, ledger = run(w)
    assert out.calls <= 3 and len(w.calls) <= 3                                      # bounded by Brother Mode's own loop guards
    assert out.review_unavailable and not out.validated and not out.improved and not out.changed
    assert [r.kind for r in ledger.rows] == ["SOLUTION", "ATTEMPT_FAILED"] and out.failures[0]["class"] == "RATE_LIMITED"


def test_an_unchanged_answer_after_criticism_is_not_an_improvement():
    w = Workers(challenge=["ISSUES: FOUND\nmaybe check HAT001"], revise=[json.dumps(BAD)], specialist=[None])
    out, _ = run(w)
    assert not out.improved and not out.changed and out.unresolved and out.final_action == BAD       # nothing improved: the objection is kept, the action stays the draft


def test_the_trail_records_every_step_and_independence_needs_a_known_different_lineage():
    w = Workers(challenge=["ISSUES: FOUND\nuse HAT001", "ISSUES: NONE\nchecked"], revise=[json.dumps(GOOD)])
    out, _ = run(w)
    assert [t["stage"] for t in out.trail] == ["SOLUTION", "CRITIQUE", "REVISION", "CRITIQUE"] and json.dumps(BAD) in out.trail[0]["text"] and "HAT001" in out.trail[1]["text"]
    assert [t["lineage"] for t in out.trail] == ["lineage-draft", "lineage-challenge-1", "lineage-revise-2", "lineage-challenge-3"] and out.independent_review
    unknown = Workers(challenge=["ISSUES: NONE\nchecked"])
    unknown_worker = lambda prompt, stage, prefer=None, exclude=(): {**unknown(prompt, stage, prefer, exclude), "independence_key": None}        # a reviewer whose lineage PlumMe did not report
    ledger = ContributionLedger()
    seed = {"text": json.dumps(GOOD), "model_key": "draft-model", "independence_key": "lineage-draft", "receipt_id": "r0"}
    res = collaborate(task_prompt=PROMPT, seed=seed, work=unknown_worker, ledger=ledger, claim_id="C-2", parse=parse, digest=digest)
    assert not res.independent_review and res.validated                                      # grounded agreement is recorded, but independence is NOT proven by an unknown lineage
    same = lambda prompt, stage, prefer=None, exclude=(): {**unknown(prompt, stage, prefer, exclude), "independence_key": "lineage-draft"}
    res = collaborate(task_prompt=PROMPT, seed=seed, work=same, ledger=ContributionLedger(), claim_id="C-3", parse=parse, digest=digest)
    assert not res.independent_review                                                         # nor is a reviewer of the author's own lineage


def test_attribution_comes_from_the_ledger_with_lineage():
    w = Workers(challenge=["ISSUES: FOUND\nfix to HAT001", "ISSUES: NONE"], revise=[json.dumps(GOOD)])
    out, ledger = run(w)
    crits = [r for r in ledger.rows if r.kind == "CRITIQUE"]
    solution, revision = next(r for r in ledger.rows if r.kind == "SOLUTION"), next(r for r in ledger.rows if r.kind == "REVISION")
    assert crits[0].identity["independence_key"] == "lineage-challenge-1" and crits[1].identity["independence_key"] == "lineage-challenge-3"      # each critique carries its own lineage
    assert revision.detail["revises"] == solution.id and revision.detail["responding_to"] == [crits[0].id]                                          # the revision answers exactly the first critique


# ---- through the agent hook and the report ---------------------------------------------------------------------------------------------------------------------------

def _agent_collab(workers, action, gate=None, uncertain=False):
    pytest.importorskip("tau2")
    from ogi013_org_economy import EconomyGate
    from ogi013_tau2_agent import FruitStackTau2Agent
    events = []
    ep = SimpleNamespace(economy=gate or EconomyGate(), ledger=ContributionLedger(), claim=SimpleNamespace(id="C-ep"), collab_issues=0, stats={"escalations": 0, "challenges_found": 0, "revisions": 0},
                         event=lambda kind, **d: events.append((kind, d)), step=lambda p, stage, exclude=(), prefer=None: workers(p, stage, prefer, exclude))
    me = SimpleNamespace(write_tools={"cancel_reservation"})
    draft = {"output": json.dumps(action), "model_key": "draft-model", "independence_key": "lineage-draft", "receipt_id": "r0"}
    out = FruitStackTau2Agent._org_collab(me, ep, PROMPT, draft, action, {"transcript": []}, uncertain=uncertain)
    return out, events, ep


def test_agent_hook_escalates_a_write_improves_it_and_records_the_causal_revision():
    w = Workers(challenge=["ISSUES: FOUND\nuse HAT001", "ISSUES: NONE"], revise=[json.dumps(GOOD)])
    out, events, ep = _agent_collab(w, BAD)
    kinds = [k for k, _ in events]
    assert out == GOOD and kinds == ["ORG_COLLAB", "ORG_REVISION"] and ep.collab_issues == 1
    assert events[0][1]["purpose"] == "consequential_effect" and events[1][1]["action_changed"] is True and events[1][1]["trigger"] == "CRITICISM_REVISED"


def test_agent_hook_does_not_escalate_a_simple_read_and_a_validated_answer_is_no_revision():
    w = Workers(challenge=["ISSUES: NONE\nPolicy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION."])
    read = {"action": "tool", "name": "get_reservation_details", "arguments": {"reservation_id": "HAT001"}}
    out, events, _ = _agent_collab(w, read)
    assert out == read and events[0][0] == "ORG_SKIPPED" and w.calls == []
    out, events, _ = _agent_collab(w, GOOD)                                          # a write is reviewed; the reviewer finds nothing: validated, no ORG_REVISION
    assert out == GOOD and [k for k, _ in events] == ["ORG_COLLAB"] and events[0][1]["validated"] and not events[0][1]["improved"]


def test_report_counts_the_collaboration_and_only_a_changed_action_establishes_success(tmp_path):
    from rg2_trace_report import build_report

    def episode(root, events):
        task = root / "tasks" / "2"
        task.mkdir(parents=True)
        (task / "fruitstack-events.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")
        (task / "official-result.json").write_text(json.dumps({"reward_info": {"reward": 1.0}}))
        return build_report(root)

    critique = {"role": "critique", "model": "m", "lineage": "l1", "found_issues": False, "materially_improved": False}
    validated = episode(tmp_path / "a", [{"event": "ORG_COLLAB", "validated": True, "improved": False, "attribution": [critique], "unresolved": [], "calls": 1},
                                         {"event": "EPISODE_CLOSED", "stats": {"revisions": 0}}])
    assert validated["verdict"]["worker_contribution"] is True and validated["verdict"]["organisational_success"] is False
    assert "validated_unchanged=1" in validated["evidence"]["collaboration"]
    improved_events = [{"event": "ORG_COLLAB", "validated": False, "improved": True, "unresolved": [], "calls": 3,
                        "attribution": [{**critique, "found_issues": True, "materially_improved": True}, {"role": "revision", "model": "a", "lineage": "l0", "changed_action": True}]},
                       {"event": "ORG_REVISION", "claim": "C-ep", "action_changed": True, "trigger": "CRITICISM_REVISED"}]
    improved = episode(tmp_path / "b", improved_events)
    assert improved["verdict"]["causal_effect_on_decision"] is True and improved["verdict"]["organisational_success"] is True


def test_committed_trace_is_what_the_code_produces():
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "evidence" / "ogi013-collab"))
    from make_trace import render
    assert render() == (root / "evidence" / "ogi013-collab" / "COLLAB_TRACE.md").read_text()
