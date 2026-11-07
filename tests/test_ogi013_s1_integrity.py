"""S1 integrity correction (2026-11-07): the second solver slot must never fall back to solver1/Luna, both solver identities are validated from actual receipts and lineages, a missing
independent member fails closed as INFRA_INCOMPLETE, unverified weights are labelled provisional, and the stored S1 rows are reclassified offline. Offline only; no provider call."""
import json
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

import ogi013_qa1 as q1
import ogi013_s1 as s1
from fs_codemode.loop import CooperationControl, LoopParams

HERE = Path(__file__).resolve().parents[1] / "evidence" / "ogi013-small-proof"


def test_solver_slots_are_claimed_once_and_never_fall_back():
    slots = q1.SolverSlots()
    assert [slots.claim(), slots.claim()] == ["solver1", "solver2"]
    assert slots.claim() is None and slots.claim() is None                 # the old code returned "solver1" here (the S1 defect)


def good(model, lineage, receipt="r"):
    return {"model": model, "lineage": lineage, "receipt": receipt, "submitted": True}


def test_identity_validation_uses_receipts_and_lineages_not_row_counts():
    ok = {"S1": good(q1.LUNA_KEY, "luna"), "S2": good(q1.NEMO_KEY, "nemotron")}
    assert q1.solver_identity_problems(ok, ("luna", "nemotron"), (q1.LUNA_KEY, q1.NEMO_KEY)) == []
    twice = {"S1": good(q1.LUNA_KEY, "luna", "a"), "S2": good(q1.LUNA_KEY, "luna", "b")}      # two solution rows, one lineage
    p = q1.solver_identity_problems(twice, ("luna", "nemotron"), (q1.LUNA_KEY, q1.NEMO_KEY))
    assert any("not distinct" in x for x in p) and any("did not contribute" in x for x in p)
    assert q1.solver_identity_problems({"S1": good(q1.LUNA_KEY, "luna")}, None, None)          # one position only
    no_receipt = {"S1": good(q1.LUNA_KEY, "luna"), "S2": good(q1.NEMO_KEY, "nemotron", None)}
    assert any("no execution receipt" in x for x in q1.solver_identity_problems(no_receipt))
    pinned_only = {"S1": good(q1.LUNA_KEY, "luna"), "S2": {**good(q1.NEMO_KEY, "nemotron"), "submitted": False}}
    assert q1.solver_identity_problems(pinned_only)                                            # an intended roster entry that never submitted does not count


def test_unverified_weights_close_as_provisional_with_the_disagreement_preserved():
    c = CooperationControl(LoopParams(), models=("L", "N"))
    c.book.competence["L"] = 0.95                                              # weights without any verified evidence
    r = c.close({"signatures": {"L": "A", "N": "F"}, "first": {"L": "A", "N": "F"}})
    assert r["rule"] == "UNRESOLVED_PRIMARY_RETAINED" and r["provisional"] and r["verified_improvement"] is False and r["final_answer"] == "A"
    assert {x["answer"] for x in r["unresolved_disagreement"]} == {"A", "F"}
    assert q1.selection_status(r) == "PROVISIONAL_UNVERIFIED"
    agree = c.close({"signatures": {"L": "A", "N": "A"}, "first": {"L": "A", "N": "A"}})
    assert agree["rule"] == "CONSENSUS" and not agree["provisional"] and agree["unresolved_disagreement"] == [] and q1.selection_status(agree) == "CONSENSUS"


def test_classify_t_row_separates_cooperation_duplication_infra_and_controller():
    base = {"status": "OK", "lineages": {"positions": {"S1": "luna", "S2": "nemotron"}}, "final_positions": {q1.LUNA_KEY: "A", q1.NEMO_KEY: "B"}, "loop_closing": {"rule": "CONSENSUS"}}
    assert s1.classify_t_row(base) == {"cooperation": "GENUINE_LUNA_NEMOTRON", "controller": "CONSENSUS", "valid_duo": True, "luna_twice_in_final_positions": False}
    dup = {**base, "lineages": {"positions": {"S1": "luna"}}, "final_positions": {q1.LUNA_KEY: "A", q1.LUNA_KEY + "#1": "B"}, "loop_closing": {"rule": "WEIGHTS_DECIDE_UNVERIFIED"}}
    c = s1.classify_t_row(dup)
    assert c["cooperation"] == "LUNA_ONLY_DUPLICATION" and c["controller"] == "PROVISIONAL_UNVERIFIED" and not c["valid_duo"] and c["luna_twice_in_final_positions"]
    assert s1.classify_t_row({"status": "INFRA_FAILED"})["cooperation"] == "INFRA_FAILED"
    ver = s1.classify_t_row({**base, "loop_closing": {"rule": "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION"}})
    assert ver["controller"] == "VERIFIED_OBJECTION"


def test_stored_s1_rows_are_reclassified_12_luna_only_4_genuine_and_the_raw_file_is_untouched():
    rows = [json.loads(l) for l in (HERE / "s1_results" / "results.jsonl").open()]
    sel = json.loads((HERE / "selection.json").read_text())
    r = s1.reclassify(rows, sel)
    assert r["cooperation_tally"] == {"GENUINE_LUNA_NEMOTRON": 4, "LUNA_ONLY_DUPLICATION": 12, "INFRA_FAILED": 0} and r["luna_twice_rows"] == 12
    assert r["valid_duo_rows"] == ["1876", "605", "3121", "693"]
    assert r["controller_tally"]["VERIFIED_OBJECTION"] == 0 and r["controller_tally"]["PROVISIONAL_UNVERIFIED"] == 8
    assert len(rows) == 32 and (HERE / "s1_results" / "S1_RESULT.md").read_text().startswith("# S1 result")     # raw rows and the historical verdict file are preserved


# ---- run_T in duo mode against a scripted episode -------------------------------------------------------------------------------------------------------
def duo_ctx(tmp_path, monkeypatch, nemotron_ok, luna_calls):
    class MangoService:
        def __init__(self):
            self.latest = {}

        def checkpoint(self, work_ref, actor_id, kind, body, *, turn_id):
            self.latest[work_ref] = {"progressive": {"latest_checkpoint": {"kind": kind, "payload": body}}}

        def work_context(self, work_ref):
            return self.latest.get(work_ref, {})

    class Episode:
        def __init__(self):
            self.work, self.actor, self.turn_id, self.sid = "w", "a", "t", "s"
            self.claim, self.stats = SimpleNamespace(id="c1"), {"tokens_in": 0, "tokens_out": 0}
            self.timing = SimpleNamespace(report=lambda: {})
            self.lock, self.calls = threading.Lock(), 0

        def fork(self):
            return self

        def event(self, *a, **k):
            pass

        def _flags(self):
            return {}

        def step(self, prompt, tag, *, exclude=(), prefer=None, **_):
            with self.lock:
                self.calls += 1
            if "Solve the task yourself, independently." in prompt:
                if not nemotron_ok:
                    return {"success": False, "output": None, "model_key": None, "independence_key": None, "receipt_id": None, "decision_id": None, "failure_class": "PROVIDER_UNAVAILABLE"}
                return {"success": True, "output": "ANSWER: B", "model_key": q1.NEMO_KEY, "independence_key": "nemotron", "receipt_id": "rn", "decision_id": "dn"}
            return {"success": True, "output": "ISSUES: NONE", "model_key": prefer or q1.NEMO_KEY, "independence_key": "nemotron", "receipt_id": "rn2", "decision_id": "dn2"}

    def luna(ctx, prompt):
        luna_calls.append(prompt[:40])
        out = "ANSWER: A" if "Solve the task yourself, independently." in prompt else "ISSUES: NONE"
        return {"success": True, "output": out, "model_key": q1.LUNA_KEY, "independence_key": "luna", "receipt_id": f"rl{len(luna_calls)}", "decision_id": None}

    (tmp_path / "events").mkdir(exist_ok=True)
    svc, ep = MangoService(), Episode()
    monkeypatch.setattr(q1, "luna_step", luna)
    monkeypatch.setattr(q1.time, "sleep", lambda _s: None)
    monkeypatch.setattr(q1, "check_budget", lambda _e: None)
    adapter = SimpleNamespace(service=svc, checkpoint=svc.checkpoint)
    return SimpleNamespace(out=tmp_path, s_model=None, luna_tokens=0, stop=None, run_budget=None, episode=lambda *a, **k: ep, stack=SimpleNamespace(fs=SimpleNamespace(mango=adapter))), ep


Q = {"id": "offline", "question": "Choose the supported option.", "options": ["A is unsupported", "B is supported"]}


def test_a_failed_nemotron_solve_never_becomes_a_second_luna_solve_and_the_row_fails_closed(tmp_path, monkeypatch):
    luna_calls = []
    ctx, ep = duo_ctx(tmp_path, monkeypatch, nemotron_ok=False, luna_calls=luna_calls)
    with pytest.raises(q1.Infra) as e:
        q1.run_T(ctx, Q, duo=True, loop=True)
    assert e.value.kind == "INFRA_INCOMPLETE" and "did not contribute" in str(e.value)
    solves = [p for p in luna_calls if "Solve the task yourself" in p or "independent" in p.lower()]
    assert len(luna_calls) == 1, luna_calls                                      # Luna solved once as solver1; the retry of the failed solver2 solve did not become a Luna call


def test_duo_row_records_actual_identities_and_marks_the_unverified_selection_provisional(tmp_path, monkeypatch):
    luna_calls = []
    ctx, ep = duo_ctx(tmp_path, monkeypatch, nemotron_ok=True, luna_calls=luna_calls)
    row = q1.run_T(ctx, Q, duo=True, loop=True)
    lins = {p["lineage"] for p in row["solver_identities"].values() if p["submitted"]}
    assert lins == {"luna", "nemotron"} and all(p["receipt"] for p in row["solver_identities"].values())
    assert row["selection_status"] == "PROVISIONAL_UNVERIFIED" and row["verified_improvement"] is False
    assert {x["answer"] for x in row["unresolved_disagreement"]} == {"A", "B"}
    assert s1.classify_t_row({"status": "OK", **row})["cooperation"] == "GENUINE_LUNA_NEMOTRON"


# ---- controller regression observed in the 12 Luna-only S1 rows (initial 8/12, observed final 6/12) -----------------------------------------------------
def _archive():
    return {r["qid"]: r for r in (json.loads(l) for l in (HERE / "s1_results" / "results.jsonl").open()) if r["arm"] == "T"}


@pytest.mark.parametrize(("qid", "key", "initial", "observed"), [("11613", "H", "H", "F"), ("11894", "D", "D", "H"), ("1659", "H", "H", "G"), ("464", "E", "F", "E")])
def test_observed_s1_cases_the_second_same_lineage_sample_no_longer_overrides_the_initial_answer(qid, key, initial, observed):
    row = _archive()[qid]
    assert row["key"] == key and row["first_by_pos"]["S1"] == initial and row["letter"] == observed          # the archived observation is unchanged
    cf = s1.counterfactual_t_row(row)
    assert cf["hypothetical_final"] == initial and cf["hypothetical_rule"] == "SAME_LINEAGE_NO_INDEPENDENCE"
    assert cf["independent_collaboration"] is False and cf["verified_improvement"] is False
    assert {x["answer"] for x in cf["unresolved_disagreement"]} == {initial, observed}                       # the disagreement is preserved with its status
    assert all(x["source"] == "same_lineage_sample_not_evidence" for x in cf["unresolved_disagreement"])


def test_counterfactual_tallies_are_labelled_hypothetical_and_distinguish_observed_from_replayed():
    cf = s1.counterfactual(list(_archive().values()) and [json.loads(l) for l in (HERE / "s1_results" / "results.jsonl").open()], json.loads((HERE / "selection.json").read_text()))
    assert cf["luna_only_12"] == {"initial": "8/12", "observed_final": "6/12", "hypothetical_final": "8/12"}
    assert cf["lost_by_observed"] == ["11613", "11894", "1659"] and cf["recovered_by_observed"] == ["464"]
    assert cf["genuine_4"] == {"initial": "2/4", "observed_final": "3/4", "hypothetical_final": "3/4"}      # genuine rows unchanged (605 keeps its documented concession path)
    assert cf["LABEL"].startswith("observed = archived result; hypothetical")


def ctl_with(models=("L", "N")):
    return CooperationControl(LoopParams(), models=models)


def test_the_choice_does_not_depend_on_which_sample_registered_first():
    for sigs in ({"L": "F", "L#1": "H"}, {"L": "H", "L#1": "F"}):
        c = ctl_with(("L",))
        c.primary_first = lambda: "H"
        r = c.close({"signatures": sigs, "first": dict(sigs), "models": list(sigs)})
        assert r["final_answer"] == "H" and r["rule"] == "SAME_LINEAGE_NO_INDEPENDENCE"                       # the old tie-break returned whichever sample finished first


def test_same_lineage_agreement_is_not_independent_consensus():
    r = ctl_with(("L",)).close({"signatures": {"L": "A", "L#1": "A"}, "first": {"L": "A", "L#1": "A"}, "models": ["L", "L#1"]})
    assert r["rule"] == "SAME_LINEAGE_NO_INDEPENDENCE" and r["independent_collaboration"] is False and r["verified_improvement"] is False and q1.selection_status(r) == "SAME_LINEAGE_NOT_INDEPENDENT"


def test_a_critique_between_two_samples_of_one_model_cannot_move_weights_or_count_as_verified():
    c = ctl_with(("L", "N"))
    ev = {"kind": "CRITIQUE", "critic": "L#1", "target": "L", "verification": "independently_confirmed", "relevance_assessed": True, "independent_confirmation": True, "hit": True, "row": "x"}
    c.observe(ev)
    assert c.book.comp("L") == LoopParams().prior_competence
    r = c.close({"signatures": {"L": "A", "L#1": "B", "N": "A"}, "first": {"L": "A", "L#1": "B", "N": "A"}, "models": ["L", "L#1", "N"]})
    assert r["verified_improvement"] is False and r["rule"] != "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION"


def test_genuine_independent_confirmed_criticism_can_still_change_the_initial_answer():
    c = ctl_with(("L", "N"))
    c.observe({"kind": "CRITIQUE", "critic": "N", "target": "L", "verification": "independently_confirmed", "relevance_assessed": True, "independent_confirmation": True, "hit": True, "row": "r1"})
    r = c.close({"signatures": {"L": "A", "N": "F"}, "first": {"L": "A", "N": "F"}, "models": ["L", "N"]})
    assert r["rule"] == "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION" and r["final_answer"] == "F" and r["verified_improvement"] is True and r["independent_collaboration"] is True


def test_weights_without_evidence_retain_the_initial_answer_and_weights_with_evidence_are_still_provisional():
    base = {"signatures": {"L": "A", "N": "F"}, "first": {"L": "A", "N": "F"}, "models": ["L", "N"]}
    equal = ctl_with().close(base)
    assert equal["rule"] == "UNRESOLVED_PRIMARY_RETAINED" and equal["final_answer"] == "A" and equal["provisional"] and equal["verified_improvement"] is False
    assert {x["answer"] for x in equal["unresolved_disagreement"]} == {"A", "F"}
    c = ctl_with()
    c.book.competence["N"] = 0.7                                     # a margin of at least one verified update (0.10) over the primary
    r = c.close(base)
    assert r["rule"] == "WEIGHTS_DECIDE_UNVERIFIED" and r["final_answer"] == "F" and r["provisional"] and r["verified_improvement"] is False
