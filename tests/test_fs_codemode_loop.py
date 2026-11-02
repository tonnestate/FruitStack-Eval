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
    for lvl, step in (("verified", 0.10), ("formal", 0.03), ("none", 0.0), ("failed", 0.0)):
        b2 = WeightBook(P)
        rec = b2.update("N", "L", lvl)
        assert rec["step"] == step and abs(b2.comp("N") - (0.5 + step)) < 1e-9 and abs(b2.coop("N", "L") - (0.5 + step)) < 1e-9
    for _ in range(50):
        b.update("N", "L", "verified")
    assert b.comp("N") == P.max_weight and b.coop("L", "N") == P.max_weight                 # bounded; pair weight is symmetric
    run = lambda: [WeightBook(P).update("N", "L", l)["after"] for l in ("verified", "formal", "none")]  # noqa: E731
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
def test_high_weight_never_overrides_a_verified_objection():
    c = CooperationControl(P, models=("L", "N"))
    c.book.competence["L"] = 0.95
    c.observe({"kind": "CRITIQUE", "critic": "N", "target": "L", "verification": "verified", "hit": True, "row": "r1"})
    out = c.close({"signatures": {"L": "A", "N": "F"}, "first": {"L": "A", "N": "F"}})
    assert out["rule"] == "VERIFIED_LAST_OBJECTION" and out["final_model"] == "N" and out["weights_consulted"] is False


def test_low_weight_never_suppresses_a_verified_objection():
    c = CooperationControl(P, models=("L", "N"))
    c.book.cooperation[frozenset(("L", "N"))] = 0.0
    c.book.competence["N"] = 0.0
    st = {"point": "REPLY_OR_FINISH", "options": ["REPLY", "FINISH"], "author": "L", "signatures": {"L": "A", "N": "F"}, "disagree": True, "models": ["L", "N"], "verifications": ["verified"]}
    assert c.decide(st) == "REPLY"
    assert c.decide({**st, "verifications": ["none"]}) == "FINISH"                            # an ungrounded objection is not forced through


# ---- scripted runs through the real Brother Mode path ------------------------------------------------------------------------------------------------------------
class Org:
    def __init__(self, behave):
        self.behave, self.log = behave, []

    def __call__(self, prompt, stage, prefer=None, exclude=()):
        pool = ["L", "N"]
        pick = prefer if prefer in pool else next((m for m in pool if m not in exclude), None)
        out = self.behave(pick, stage, prompt)
        text, verification = out if isinstance(out, tuple) else (out, None)
        self.log.append((pick, stage))
        return {"success": True, "output": text, "model_key": pick, "independence_key": pick, "receipt_id": f"{pick}-{stage}-{len(self.log)}",
                **({"verification": verification} if verification else {})}


def run(behave, control, parallel=False):
    return run_rounds(task_prompt="TASK", brief="", work=Org(behave), ledger=ContributionLedger(), claim_id="c1", signature=letter, control=control, parallel=parallel)


def chain_8512(keep):
    def behave(m, stage, p):
        if stage == "solve":
            return "KEY: A" if m == "L" else "KEY: F"
        if stage == "challenge":
            return ("ISSUES: FOUND\nCLAIM: A is wrong. KEY: F", "verified") if "KEY: A" in p else "ISSUES: NONE"
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
        assert ctl.book.comp("N") > 0.5 and any(r["type"] == "WEIGHT_UPDATE" and r["level"] == "verified" for r in logs)
        assert [d["point"] for d in res.decisions][:1] == ["CRITIQUE_OR_FINISH"] and res.decisions[0]["choice"] == "CRITIQUE"


def test_verified_objection_beats_a_high_weight_when_the_author_keeps_its_answer():
    ctl = CooperationControl(P, models=("L", "N"))
    ctl.book.competence["L"] = 0.95
    ctl.book.cooperation[frozenset(("L", "N"))] = 0.9          # a strong pair: the exchange still pays, so the objection is actually raised
    res = run(chain_8512(keep=True), ctl)
    assert res.decisions[0]["choice"] == "CRITIQUE"
    assert res.closing["rule"] == "VERIFIED_LAST_OBJECTION" and res.closing["final_model"] == "N" and res.closing["weights_consulted"] is False


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
    assert run(chain_7855(), ctl2).closing["detail"]["chosen_answer"] == "A"


def test_without_a_control_brother_mode_is_unchanged():
    res = run(chain_8512(keep=False), None)
    assert res.closing is None and res.decisions == [] and res.stop_reason in ("NO_ISSUES", "NO_CHANGE", "CONVERGED")


def test_a_high_weight_can_end_the_exchange_early_but_it_cannot_override_evidence_that_exists():
    ctl = CooperationControl(P, models=("L", "N"))
    ctl.book.competence["L"] = 0.95                              # with the prior pair weight the exchange does not pay: the loop finishes WITHOUT a critique (no objection exists)
    res = run(chain_8512(keep=True), ctl)
    assert res.decisions[0]["choice"] == "FINISH" and res.stop_reason == "CONTROL_FINISH" and res.closing["rule"] == "WEIGHTS_DECIDE_UNVERIFIED" and res.closing["final_model"] == "L"


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
