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
    assert r["rule"] == "WEIGHTS_DECIDE_UNVERIFIED" and r["provisional"] and r["verified_improvement"] is False
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
