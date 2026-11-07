"""Brother Mode closed loop (offline, deterministic): weight update table, link-3 invariants, EVC choice, and scripted runs through the REAL cherryme.brother path."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
from cherryme.brother import run_rounds  # noqa: E402
from cherryme.contributions import ContributionLedger  # noqa: E402
from fs_codemode.loop import CooperationControl, LoopParams, WeightBook  # noqa: E402

P = LoopParams()


def letter(t):
    m = re.search(r"KEY: (\w+)", t or "")
    return m.group(1) if m else None


# ---- link 1: the update table --------------------------------------------------------------------------------------------------------------------------
def test_update_table_bounds_and_determinism():
    b = WeightBook(P)
    for lvl, step in (("independently_confirmed", 0.10), ("verified", 0.0), ("reproduced", 0.0), ("formal", 0.0), ("none", 0.0), ("failed", 0.0)):
        b2 = WeightBook(P)
        rec = b2.update("N", "L", lvl, relevance_assessed=lvl == "independently_confirmed", independent_confirmation=lvl == "independently_confirmed")
        assert rec["step"] == step and abs(b2.comp("N") - (0.5 + step)) < 1e-9 and abs(b2.coop("N", "L") - (0.5 + step)) < 1e-9
    for _ in range(50):
        b.update("N", "L", "independently_confirmed", relevance_assessed=True, independent_confirmation=True)
    assert b.comp("N") == P.max_weight and b.coop("L", "N") == P.max_weight                 # bounded; pair weight is symmetric
    run = lambda: [WeightBook(P).update("N", "L", l)["after"] for l in ("independently_confirmed", "formal", "none")]  # noqa: E731
    assert run() == run()


# ---- link 2: EVC picks FINISH when the expected gain does not pay -------------------------------------------------------------------------------------------
def test_evc_finishes_when_gain_is_below_cost_and_critiques_otherwise():
    state = {"point": "CRITIQUE_OR_FINISH", "options": ["CRITIQUE", "FINISH"], "signatures": {"L": "A", "N": "F"}, "disagree": True, "models": ["L", "N"], "round": 0, "calls": 2}
    assert CooperationControl(P, models=("L", "N")).decide(state) == "CRITIQUE"              # priors: the exchange pays
    c = CooperationControl(P, models=("L", "N"))
    c.book.cooperation[frozenset(("L", "N"))] = 0.0                                          # the pair cannot resolve anything: gain <= 0 - cost
    assert c.decide(state) == "FINISH"
    agree = {**state, "signatures": {"L": "A", "N": "A"}, "disagree": False}
    hi = CooperationControl(P, models=("L", "N"))
    hi.book.competence.update({"L": 0.95, "N": 0.95})
    assert hi.decide(agree) == "FINISH"                                                      # two strong members agree: a critique round does not pay


# ---- link 3: evidence over weights, both directions ---------------------------------------------------------------------------------------------------------
def test_high_weight_never_overrides_an_independently_confirmed_objection():
    c = CooperationControl(P, models=("L", "N"))
    c.book.competence["L"] = 0.95
    c.observe({"kind": "CRITIQUE", "critic": "N", "target": "L", "verification": "independently_confirmed", "relevance_assessed": True, "independent_confirmation": True, "hit": True, "row": "r1"})
    out = c.close({"signatures": {"L": "A", "N": "F"}, "first": {"L": "A", "N": "F"}})
    assert out["rule"] == "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION" and out["final_model"] == "N" and out["weights_consulted"] is False


def test_formal_concession_with_confirmed_evidence_is_not_misclassified_as_formal_only():
    c = CooperationControl(P, models=("L", "N"))
    c.observe({"kind": "REVISION", "author": "L", "changed": True, "answer_changed": True, "levels": ["formal", {"verification": "independently_confirmed", "relevance_assessed": True, "independent_confirmation": True}]})
    assert c.concessions == []


def test_low_weight_never_suppresses_an_independently_confirmed_objection():
    c = CooperationControl(P, models=("L", "N"))
    c.book.cooperation[frozenset(("L", "N"))] = 0.0
    c.book.competence["N"] = 0.0
    st = {"point": "REPLY_OR_FINISH", "options": ["REPLY", "FINISH"], "author": "L", "signatures": {"L": "A", "N": "F"}, "disagree": True, "models": ["L", "N"], "verifications": [{"verification": "independently_confirmed", "relevance_assessed": True, "independent_confirmation": True}]}
    assert c.decide(st) == "REPLY"
    assert c.decide({**st, "verifications": [{"verification": "none"}]}) == "FINISH"         # an ungrounded objection is not forced through


def test_unattested_or_irrelevant_reproduction_cannot_update_weights_or_override_closing():
    from fs_codemode.loop import independently_confirmed
    assert not independently_confirmed(None)
    assert not independently_confirmed("independently_confirmed")
    c = CooperationControl(P, models=("L", "N"))
    c.book.competence["L"] = 0.95
    c.observe({"kind": "CRITIQUE", "critic": "N", "target": "L", "verification": "independently_confirmed", "hit": True, "row": "forged"})
    c.observe({"kind": "CRITIQUE", "critic": "N", "target": "L", "verification": "independently_confirmed", "relevance_assessed": False, "independent_confirmation": True, "hit": True, "row": "irrelevant"})
    assert c.book.comp("N") == P.prior_competence
    assert c.close({"signatures": {"L": "A", "N": "F"}, "first": {"L": "A", "N": "F"}})["rule"] == "UNRESOLVED_PRIMARY_RETAINED"


def test_verified_contribution_is_applied_once_and_audits_all_checks():
    log = []
    c = CooperationControl(P, log=log.append, models=("L", "N"))
    event = {"kind": "CRITIQUE", "critic": "N", "target": "L", "verification": "independently_confirmed",
             "relevance_assessed": True, "independent_confirmation": True, "hit": True, "row": "critique-1"}
    c.observe(event)
    c.observe(event)
    updates = [row for row in log if row["type"] == "WEIGHT_UPDATE"]
    assert len(updates) == 2 and [row["step"] for row in updates] == [P.step_verified, 0.0]
    assert updates[1]["duplicate"] and updates[0]["relevance_assessed"] and updates[0]["independent_confirmation"]


def test_unverified_contribution_can_be_promoted_before_its_single_learning_update():
    b = WeightBook(P)
    first = b.update("N", "L", "reproduced", contribution_id="promoted-1")
    promoted = b.update("N", "L", "independently_confirmed", relevance_assessed=True,
                        independent_confirmation=True, contribution_id="promoted-1")
    replay = b.update("N", "L", "independently_confirmed", relevance_assessed=True,
                      independent_confirmation=True, contribution_id="promoted-1")

    assert first["step"] == 0.0
    assert promoted["step"] == P.step_verified and not promoted.get("duplicate", False)
    assert replay["step"] == 0.0 and replay["duplicate"]
    assert b.comp("N") == 0.6


# ---- scripted runs through the real Brother Mode path ------------------------------------------------------------------------------------------------------------
class Org:
    def __init__(self, behave):
        self.behave, self.log, self.n_solve, self.lock = behave, [], 0, __import__("threading").Lock()

    def __call__(self, prompt, stage, prefer=None, exclude=()):
        pool = ["L", "N"]
        pick = prefer if prefer in pool else next((m for m in pool if m not in exclude), None)
        if stage == "solve" and prefer not in pool and not exclude:           # concurrent solves are routed to DISTINCT members, as a real router does (the old mock gave both to L)
            with self.lock:
                pick, self.n_solve = pool[self.n_solve % len(pool)], self.n_solve + 1
        out = self.behave(pick, stage, prompt)
        text, verification, checks = (*out, {}) if isinstance(out, tuple) and len(out) == 2 else out if isinstance(out, tuple) else (out, None, {})
        self.log.append((pick, stage))
        return {"success": True, "output": text, "model_key": pick, "independence_key": pick, "receipt_id": f"{pick}-{stage}-{len(self.log)}",
                **({"verification": verification, **checks} if verification else {})}


def run(behave, control, parallel=False):
    return run_rounds(task_prompt="TASK", brief="", work=Org(behave), ledger=ContributionLedger(), claim_id="c1", signature=letter, control=control, parallel=parallel)


def chain_8512(keep):
    def behave(m, stage, p):
        if stage == "solve":
            return "KEY: A" if m == "L" else "KEY: F"
        if stage == "challenge":
            return ("ISSUES: FOUND\nCLAIM: A is wrong. KEY: F", "independently_confirmed", {"relevance_assessed": True, "independent_confirmation": True}) if "KEY: A" in p else "ISSUES: NONE"
        return "KEY: A" if keep else "O1 accepted. KEY: F"
    return behave


def test_8512_like_accepted_concession_chain_through_brother_mode():
    for parallel in (False, True):
        ctl = CooperationControl(P, models=("L", "N"))
        logs = []
        ctl.log = lambda r: logs.append(r)
        ctl.book.log = ctl.log
        res = run(chain_8512(keep=False), ctl, parallel)
        assert res.closing["rule"] == "CONSENSUS" and {letter(t) for t in res.positions.values()} == {"F"}
        assert ctl.book.comp("N") > 0.5 and any(r["type"] == "WEIGHT_UPDATE" and r["level"] == "independently_confirmed" and r["step"] == P.step_verified for r in logs)
        assert [d["point"] for d in res.decisions][:1] == ["CRITIQUE_OR_FINISH"] and res.decisions[0]["choice"] == "CRITIQUE"


def test_independently_confirmed_objection_beats_a_high_weight_when_the_author_keeps_its_answer():
    ctl = CooperationControl(P, models=("L", "N"))
    ctl.book.competence["L"] = 0.95
    ctl.book.cooperation[frozenset(("L", "N"))] = 0.9          # a strong pair: the exchange still pays, so the objection is actually raised
    res = run(chain_8512(keep=True), ctl)
    assert res.decisions[0]["choice"] == "CRITIQUE"
    assert res.closing["rule"] == "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION" and res.closing["final_model"] == "N" and res.closing["weights_consulted"] is False


def chain_7855():
    def behave(m, stage, p):
        if stage == "solve":
            return "KEY: G" if m == "L" else "KEY: A"
        if stage == "challenge":
            return ("ISSUES: FOUND\nCLAIM: A is wrong. KEY: G", "formal") if "KEY: A" in p else "ISSUES: NONE"
        return "KEY: G"                                        # N concedes to the formal objection
    return behave


def test_7855_like_formal_concession_is_recorded_and_the_first_answer_stays_a_candidate():
    ctl = CooperationControl(P, models=("L", "N"))
    logs = []
    ctl.log = lambda r: logs.append(r)
    res = run(chain_7855(), ctl)
    assert any(r["type"] == "CONCEDED_TO_FORMAL" and r["author"] == "N" and r["before"] == "A" and r["after"] == "G" for r in logs)
    assert res.closing["rule"] == "FORMAL_CONCESSION_KEEPS_FIRST_ANSWER_CANDIDATE"
    assert {"model": "N", "answer": "A", "source": "first_answer_kept_after_CONCEDED_TO_FORMAL", "competence": 0.5} in res.closing["detail"]["candidates"]
    ctl2 = CooperationControl(P, models=("L", "N"))
    ctl2.book.competence["N"] = 0.9                            # weights decide only among unverified candidates
    assert run(chain_7855(), ctl2).closing["detail"]["chosen_answer"] == "G"  # weights choose only among retained candidates; the concession does not certify A or G


def test_without_a_control_brother_mode_is_unchanged():
    res = run(chain_8512(keep=False), None)
    assert res.closing is None and res.decisions == [] and res.stop_reason in ("NO_ISSUES", "NO_CHANGE", "CONVERGED")


def test_high_weights_cannot_skip_the_mandatory_independent_critique():
    ctl = CooperationControl(P, models=("L", "N"))
    ctl.book.competence["L"] = 0.95                              # with the prior pair weight the exchange does not pay: the loop finishes WITHOUT a critique (no objection exists)
    def no_issue(m, stage, prompt):
        if stage == "solve":
            return "KEY: A" if m == "L" else "KEY: F"
        return "ISSUES: NONE"
    res = run(no_issue, ctl)
    assert res.decisions[0]["choice"] == "CRITIQUE" and res.rounds == 1
    assert res.stop_reason == "NO_ISSUES" and res.closing["rule"] == "UNRESOLVED_PRIMARY_RETAINED"


def test_evc_stops_optional_revision_after_the_mandatory_critique():
    from fs_codemode.loop import LoopParams

    ctl = CooperationControl(LoopParams(extra_tokens=1_000_000), models=("L", "N"))

    def costly_exchange(m, stage, _prompt):
        if stage == "solve":
            return "KEY: A" if m == "L" else "KEY: F"
        if stage == "challenge":
            return ("ISSUES: FOUND\nA formal objection", "formal")
        raise AssertionError("EVC should stop before dispatching a revision")

    res = run(costly_exchange, ctl)
    assert res.rounds == 1 and not res.revised
    assert [row.kind for row in res.rows] == ["SOLUTION", "SOLUTION", "CRITIQUE", "CRITIQUE"]
    assert res.decisions[0]["choice"] == "CRITIQUE"
    assert any(d["point"] == "REPLY_OR_FINISH" and d["choice"] == "FINISH" for d in res.decisions)


def test_invalid_controller_action_fails_closed():
    class Invalid:
        def decide(self, state):
            return "FINISH"
        def observe(self, event):
            pass
        def close(self, state):
            return {}
    import pytest
    with pytest.raises(ValueError, match="invalid controller decision"):
        run(chain_8512(keep=True), Invalid())


def test_adapter_writes_every_decision_with_its_inputs_to_mangome():
    from types import SimpleNamespace
    written = []
    led = SimpleNamespace(write=lambda kind, key, payload: written.append((kind, key, payload)))
    from ogi013_brother_loop import make_control
    ctl = make_control(led, "8512", ("L", "N"))
    res = run(chain_8512(keep=False), ctl)
    kinds = [w[2]["type"] for w in written]
    assert {"ACTION", "WEIGHT_UPDATE", "CLOSING"} <= set(kinds) and all(w[0] == "LOOP_DECISION" and w[1].startswith("8512:") for w in written)
    action = next(w[2] for w in written if w[2]["type"] == "ACTION")
    assert "scores" in action and "weights" in action and "state" in action and action["consolidation"] is not None       # inputs are logged, incl. the existing consolidation view
    assert res.closing["rule"] == "CONSENSUS"


def test_adapter_uses_pinned_roster_order_when_unverified_candidates_tie():
    from types import SimpleNamespace
    from ogi013_brother_loop import make_control

    control = make_control(SimpleNamespace(write=lambda *args: None), "tie", models=("first", "second"))
    closing = control.close({"signatures": {"second": "B", "first": "A"}, "first": {"second": "B", "first": "A"}})
    assert closing["final_model"] == "first" and closing["final_answer"] == "A"


def test_plumme_verified_reviewer_history_survives_restart_and_changes_later_evc(tmp_path):
    import pytest
    pytest.importorskip("plumme")
    from types import SimpleNamespace
    from plumme.decisions import DecisionLog
    from plumme.service import PlumMeService
    from ogi013_brother_loop import make_control, reviewer_improvement_signal

    path = tmp_path / "decisions.jsonl"
    service = object.__new__(PlumMeService)
    service.scheduler = SimpleNamespace(decisions=DecisionLog(path), cost_policy=None, supply_regime_id="test", policy_stack={})
    service.skills = None
    for i in range(3):
        decision = service.record_consumer_ensemble_decision(
            question_id=f"cal-{i}", claim_revision=0, question_type="QA1_MC", skill_digest="d" * 64,
            topology="SEQUENTIAL_INDEPENDENT", worker_count=2, candidate_offer_ids=[],
            independent_groups=["critic-source", "author-source"], available_counts=[0, 1, 2],
            candidate_model_keys=["critic", "author"], selected_model_keys=["critic", "author"],
        )
        service.record_review_feedback(
            decision["decision_id"], reviewer_model_key="critic", proposer_model_key="author", task_class="QA1_MC",
            improved_outcome=False, verifier="offline-independent-grader",
        )

    replayed = DecisionLog(path)
    signal = reviewer_improvement_signal(replayed, "critic", "QA1_MC")
    assert signal == {"n": 3, "improved": 0, "rate": 0.0}
    decision = next(d for d in replayed.decisions.values() if d.request_features.get("question_id") == "cal-0")
    replayed.decisions[decision.decision_id] = decision.model_copy(update={"independence": {"selected_groups": ["shared", "shared"]}})
    assert reviewer_improvement_signal(replayed, "critic", "QA1_MC") == {"n": 2, "improved": 0, "rate": 0.0}
    replayed.decisions[decision.decision_id] = decision

    params = LoopParams(lam_c_per_1k_tokens=0.01)
    records = []
    ctl = make_control(SimpleNamespace(write=lambda *args: records.append(args)), "next-task", ("critic", "author"),
                       params, decision_log=replayed, task_class="QA1_MC")
    state = {"point": "CRITIQUE_OR_FINISH", "options": ["CRITIQUE", "FINISH"], "signatures": {"critic": "A", "author": "B"},
             "disagree": True, "models": ["critic", "author"]}
    baseline = CooperationControl(params, models=("critic", "author")).evc(state)["scores"]["CRITIQUE"]
    learned = ctl.evc(state)["scores"]["CRITIQUE"]
    assert baseline > 0 > learned
    assert ctl.decide(state) == "FINISH"
    action = next(row[2] for row in records if row[2]["type"] == "ACTION")
    assert action["review_history"] == [{"n": 3, "improved": 0, "task_class": "QA1_MC"}]
    assert reviewer_improvement_signal(replayed, "critic", "OTHER") == {"n": 0, "improved": 0, "rate": None}
