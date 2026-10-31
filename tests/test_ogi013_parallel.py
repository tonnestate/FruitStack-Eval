"""Parallel organisation order: engineering tests, scripted, no model calls."""
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_conc as oc2  # noqa: E402


def test_7_concurrency_cap_is_never_exceeded_with_six_ready_calls():
    gate = oc2.CallGate(cap=2)
    seen = []

    def call():
        with gate.slot():
            seen.append(gate.in_flight)
            time.sleep(0.05)
    ts = [threading.Thread(target=call) for _ in range(6)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert gate.max_seen == 2 and max(seen) <= 2 and len(seen) == 6


def test_8_timing_shares_match_injected_waits_within_5_percent():
    clock = {"t": 0.0}
    rec = oc2.TimingRecorder(clock=lambda: clock["t"])
    rec.add("ok", 0, 30)                       # 30 s of provider time
    rec.add("rate_limit", 30, 50)              # 20 s
    rec.add("retry_wait", 50, 60)              # 10 s
    rec.add("ok", 10, 40)                      # overlaps the first call: wall-clock union is still 30..40 -> ok covers 0..40 = 40 s
    clock["t"] = 100.0
    r = rec.report()
    assert abs(r["wall_share"]["ok"] - 0.40) <= 0.05 * 0.40 + 1e-9 and abs(r["wall_share"]["rate_limit"] - 0.20) <= 0.01 and abs(r["wall_share"]["retry_wait"] - 0.10) <= 0.005
    assert r["sum_seconds"]["ok"] == 60.0 and r["wall_clock_seconds"]["ok"] == 40.0       # overlap counted once on the wall clock
    assert abs(r["any_activity_share"] - 0.60) <= 0.03


def test_outcome_classes():
    assert oc2.outcome_class(None) == "ok" and oc2.outcome_class("EXECUTION_NOT_PERFORMED_RATE_LIMITED") == "rate_limit"
    assert oc2.outcome_class("EXECUTION_NOT_PERFORMED_PROVIDER_UNAVAILABLE") == "provider_unavailable" and oc2.outcome_class("EXECUTION_OUTPUT_UNUSABLE_X") == "unusable_output"


# ---- 12 exchange protocol --------------------------------------------------------------------------------------------------------------------------------------
from ogi013_vote import Ledger, OPEN, WITHDRAWN  # noqa: E402

EV = {"kind": "command", "repro": {"tool": "run_python", "args": {"code": "x"}}}


def objection_ledger():
    led, ev = Ledger(), []
    led.emit = lambda k, **kw: ev.append(k)
    oid = led.objection("S1", "L2", "the patch accepts 5x", ground=EV)
    return led, oid, ev


def test_12_author_evidence_then_critic_withdraws_with_evidence_ends_withdrawn():
    led, oid, ev = objection_ledger()
    assert led.reply(oid, "author", "evidence", "ran it: ValueError raised", EV)["ok"]
    r = led.reply(oid, "critic", "withdraw", "confirmed with my own run", EV)
    assert r["event"] == "WITHDRAWN" and led.objs[0]["state"] == WITHDRAWN and led.objs[0]["decided_by"] == "withdrawn_with_evidence"
    assert ev.count("REPLY") == 2 and led.arbitration_due("S1") == []


def test_12_critic_maintains_then_the_specialist_is_due_exactly_once():
    led, oid, ev = objection_ledger()
    led.reply(oid, "author", "evidence", "it raises", EV)
    assert led.reply(oid, "critic", "maintain", "new case: '1h1h' passes", EV)["event"] == "ARBITRATION_DUE"
    assert [o["id"] for o in led.arbitration_due("S1")] == [oid]
    led.objs[0]["arbitrated"] = True                                 # the driver marks it when the specialist has been called
    assert led.arbitration_due("S1") == []
    assert led.reply(oid, "critic", "maintain", "again", EV)["event"] == "REPLY_REFUSED"          # the limit of 2 exchanges holds


def test_12_a_reply_without_evidence_is_logged_ungrounded_and_changes_nothing():
    led, oid, ev = objection_ledger()
    r = led.reply(oid, "author", "evidence", "I disagree", {"kind": "suggestion"})
    assert r["event"] == "UNGROUNDED_REPLY" and "UNGROUNDED_REPLY" in ev and led.objs[0]["state"] == OPEN and led.objs[0]["exchanges"] == 0
    assert led.reply(oid, "critic", "withdraw", "ok", EV)["event"] == "REPLY_REFUSED"          # wrong turn order


def test_12_author_concession_needs_no_evidence_and_the_critic_can_still_respond():
    led, oid, _ = objection_ledger()
    assert led.reply(oid, "author", "concede", "you are right, revising")["ok"] and led.objs[0]["exchanges"] == 1


# ---- 10 over-conservatism guard ---------------------------------------------------------------------------------------------------------------------------------
import ogi013_candidates as oc  # noqa: E402


def _checker(table):
    def check(diff, repros):
        p, f, rp = table[diff]
        return {"passed": p, "failed": f, "repro": {o: rp.get(o, True) for o in repros}}
    return check


def test_10_visible_tests_pass_but_a_grounded_repro_of_a_named_case_fails_the_flip_is_adopted_and_a_no_flip_is_rejected():
    led = oc.CandidateLedger(_checker({"d0": (5, 0, {"O2": False}), "d1": (5, 0, {"O2": True}), "d2": (5, 0, {"O2": False})}))
    led.consider_revision("S1", "first", "d0", [])
    led.add_repro("O2", {"tool": "run_python"})                       # the critic's reproduction of the named failing case becomes a check
    flip = led.consider_revision("S1", "rev1", "d1", ["O2"])
    assert flip["adopted"] and led.best()["label"] == "rev1"
    led2 = oc.CandidateLedger(_checker({"d0": (5, 0, {"O2": False}), "d2": (5, 0, {"O2": False})}))
    led2.consider_revision("S1", "first", "d0", [])
    led2.add_repro("O2", {"tool": "run_python"})
    no_flip = led2.consider_revision("S1", "rev1", "d2", ["O2"])
    assert not no_flip["adopted"] and no_flip["reason"].startswith("REPRO_STILL_FAILING")


# ---- 6 adoption under concurrency, 5 determinism -----------------------------------------------------------------------------------------------------------------
import random  # noqa: E402


def test_6_two_revisions_finishing_at_once_only_the_verified_improvement_is_adopted_and_the_incumbent_never_regresses():
    for trial in range(20):
        led = oc.CandidateLedger(_checker({"d0": (5, 0, {"O2": False}), "good": (5, 0, {"O2": True}), "bad": (3, 2, {"O2": True})}))
        led.consider_revision("S1", "first", "d0", [])
        led.add_repro("O2", {"tool": "run_python"})
        gate, out = threading.Barrier(2), {}

        def rev(label, diff):
            gate.wait()
            time.sleep(random.random() * 0.01)
            out[label] = led.consider_revision("S1", label, diff, ["O2"])
        ts = [threading.Thread(target=rev, args=("rev1", "good")), threading.Thread(target=rev, args=("rev2", "bad"))]
        [t.start() for t in ts]
        [t.join() for t in ts]
        assert out["rev2"]["adopted"] is False and led.best()["diff"] == "good" and led.incumbent("S1")["diff"] == "good"


def test_5_twenty_random_interleavings_give_the_same_final_candidate_set_and_protected_best():
    table = {"a0": (5, 0, {}), "b0": (5, 0, {}), "a1": (6, 0, {}), "b1": (5, 0, {})}
    finals = set()
    for seed in range(20):
        rnd = random.Random(seed)
        led = oc.CandidateLedger(_checker(table))
        jobs = [lambda: led.consider_revision("S1", "first", "a0", []), lambda: led.consider_revision("S2", "first", "b0", [])]
        rnd.shuffle(jobs)
        ts = [threading.Thread(target=lambda j=j: (time.sleep(rnd.random() * 0.005), j())) for j in jobs]
        [t.start() for t in ts]
        [t.join() for t in ts]
        revs = [lambda: led.consider_revision("S1", "rev1", "a1", ["Oq"]), lambda: led.consider_revision("S2", "rev1", "b1", ["Oq"])]
        rnd.shuffle(revs)
        ts = [threading.Thread(target=lambda j=j: (time.sleep(rnd.random() * 0.005), j())) for j in revs]
        [t.start() for t in ts]
        [t.join() for t in ts]
        finals.add((tuple(sorted((c["id"], c["status"]) for c in led.cands)), led.best()["id"]))
    assert len(finals) == 1 and next(iter(finals))[1] == "S1:rev1"


# ---- 1 no leak before the barrier (concurrent), 11 late solver stays blind ----------------------------------------------------------------------------------------
from types import SimpleNamespace  # noqa: E402


def _team(tmp_path):
    import ogi013_team_code as tc
    t = tc.TeamState("GOAL TEXT", tmp_path / "team_state.md")
    t.pos = {"S1": SimpleNamespace(id="S1", model="m1", status="open", rev=0, diff="", test_tail="", slot="solver1"),
             "S2": SimpleNamespace(id="S2", model="m2", status="open", rev=0, diff="", test_tail="", slot="solver2")}
    t.independent = True
    return t


def test_1_and_11_concurrent_blind_solvers_see_nothing_and_a_late_solver_stays_blind_after_the_barrier(tmp_path):
    t = _team(tmp_path)
    seen = {"S1": [], "S2": []}
    stop = threading.Event()

    def worker(pid):
        while not stop.is_set():
            seen[pid].append(t.text(pid))
            time.sleep(0.002)
    ths = [threading.Thread(target=worker, args=(p,)) for p in ("S1", "S2")]
    [x.start() for x in ths]
    time.sleep(0.05)
    t.pos["S1"].diff = "+SECRET_ONE_FIX"                       # solver 1 submits its first position
    t.pos["S1"].test_tail = "Ran 3 tests SECRET_ONE_TAIL"
    t.independent = False                                       # the barrier opens for the team (S2 is late)
    time.sleep(0.05)
    late_before = list(seen["S2"])
    t.pos["S2"].diff = "+SECOND_FIX"                            # S2's own first submission
    time.sleep(0.05)
    stop.set()
    [x.join() for x in ths]
    assert all(x == "" for x in seen["S2"][:len(late_before)])                       # no team state at all, before AND after the barrier, until its own submission
    assert all("SECRET_ONE_FIX" not in x and "SECRET_ONE_TAIL" not in x for x in seen["S2"][:len(late_before)])
    assert "SECRET_ONE_FIX" in seen["S2"][-1] and "SECOND_FIX" in seen["S2"][-1]    # afterwards it is released into the shared state
    assert "GOAL TEXT" in t.text("S1") and "STATE VERSION" in t.text("S1")


def test_12_author_reply_tool_inside_the_agent_loop_runs_the_exchange(tmp_path):
    import ogi013_code_task as ct
    import ogi013_team_code as tc
    t = tc.TeamState("Anything else must raise ValueError for 5x input in the task text", tmp_path / "ts.md")
    oid = t.objection("S1", "L2", "5x is accepted", ground=EV)
    t.pos = {"S1": SimpleNamespace(id="S1", model="m", status="open", rev=0, diff="+x", test_tail="", slot="solver1")}
    ev = []
    t.emit = lambda k, **kw: ev.append(k)
    acts = iter(['{"action": "tool", "name": "reply", "arguments": {"id": "%s", "evidence": "I disagree"}}' % oid,
                 '{"action": "tool", "name": "reply", "arguments": {"id": "%s", "evidence": "the task text says \\"Anything else must raise ValueError\\" and 5x raises it"}}' % oid,
                 '{"action": "message", "content": "done"}'])

    class Ep:
        def blocking(self): return None
        def event(self, kind, **k): ev.append(kind)
        def step(self, prompt, role, **k):
            return {"success": True, "output": next(acts), "model_key": "m", "independence_key": "m", "receipt_id": "r"}
    ctx = SimpleNamespace(ep=Ep(), deadline=time.monotonic() + 60, keys={}, gate=None, effects=None)
    ct.agent_loop(ctx, "author", "h", SimpleNamespace(), {"read_file"}, gated=True, gate=SimpleNamespace(check_submit=lambda: SimpleNamespace(accepted=True, reason="ok", diff_sha256="x")), team=t, limit=3)
    assert "UNGROUNDED_REPLY" in ev and "REPLY" in ev                       # the evidence-free reply changed nothing; the quote-grounded one was recorded
    assert t.objs[0]["exchanges"] == 1 and t.objs[0]["declined"] is True and t.objs[0]["state"] == OPEN
