"""Repair order 1 (R1-R5, R8): scripted tests, no model calls."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_candidates as oc  # noqa: E402
from ogi013_roster import MAX_MODELS, Roster, next_solver_role  # noqa: E402

TASK = ("parse_duration() silently accepts invalid input and rejects upper-case units\n\nUnits are case-insensitive: parse_duration(\"2H5M\") == 7500.\n"
        "The whole string must consist of <number><unit> parts with units h, m, s, each unit at most once, in the order h, m, s. Anything else must raise ValueError, e.g. \"\", \"10\", \"5x\", \"1h 30m\", \"30m1h\", \"1h1h\".\n")


def fake_checker(table):
    """table: diff -> (passed, failed, {oid: bool})"""
    def check(diff, repros):
        p, f, rp = table[diff]
        return {"passed": p, "failed": f, "repro": {o: rp.get(o, True) for o in repros}}
    return check


# ---- R1 ------------------------------------------------------------------------------------------------------------------------------------------------
def ledger(table):
    writes = []
    return oc.CandidateLedger(fake_checker(table), on_write=lambda k, key, p: writes.append((k, key, p))), writes


def test_r1_first_candidate_is_adopted_and_written_with_sha():
    led, writes = ledger({"d0": (5, 0, {})})
    r = led.consider_revision("S1", "first", "d0", [])
    assert r["adopted"] and writes[0][0] == "TEAM_CANDIDATE" and writes[0][2]["diff_sha256"] == oc.sha256("d0")


def test_r1_revision_without_grounded_objection_is_rejected_and_incumbent_stays():
    led, _ = ledger({"d0": (5, 0, {}), "d1": (5, 0, {})})
    led.consider_revision("S1", "first", "d0", [])
    r = led.consider_revision("S1", "rev1", "d1", [])
    assert not r["adopted"] and r["reason"] == "NO_GROUNDED_OBJECTION_ADDRESSED" and led.incumbent("S1")["diff"] == "d0" and led.best()["diff"] == "d0"


def test_r1_lower_visible_score_is_rejected():
    led, _ = ledger({"d0": (5, 0, {}), "d1": (4, 1, {})})
    led.consider_revision("S1", "first", "d0", [])
    led.add_repro("O2", {"tool": "run_python"})
    r = led.consider_revision("S1", "rev1", "d1", ["O2"])
    assert not r["adopted"] and r["reason"] == "VISIBLE_SCORE_LOWER" and led.best()["label"] == "first"


def test_r1_repro_must_pass_for_every_claimed_objection():
    led, _ = ledger({"d0": (5, 0, {"O2": False}), "d1": (5, 0, {"O2": False})})
    led.consider_revision("S1", "first", "d0", [])
    led.add_repro("O2", {"tool": "run_python"})
    r = led.consider_revision("S1", "rev1", "d1", ["O2"])
    assert not r["adopted"] and r["reason"].startswith("REPRO_STILL_FAILING:O2")


def test_r1_adopted_revision_fixing_the_repro_becomes_best_and_earlier_candidates_stay_candidates():
    table = {"d0": (5, 0, {"O2": False}), "d1": (5, 0, {"O2": True}), "d2": (4, 1, {"O2": True})}
    led, _ = ledger(table)
    led.consider_revision("S1", "first", "d0", [])
    led.add_repro("O2", {"tool": "run_python"})
    assert led.consider_revision("S1", "rev1", "d1", ["O2"])["adopted"]
    led.add_repro("O3", {"tool": "run_python"})
    r = led.consider_revision("S1", "rev2", "d2", ["O3"])           # harmful revision: lower score
    assert not r["adopted"] and led.best()["label"] == "rev1"
    assert [c["status"] for c in led.cands] == ["SUPERSEDED", "ADOPTED", "REJECTED_REVISION"]


def test_r1_ties_pick_the_earliest_candidate_and_the_replayed_duration_case_selects_first():
    led, _ = ledger({"first": (2, 0, {}), "rev1": (2, 0, {}), "rev2": (2, 0, {})})
    led.consider_revision("S3", "first", "first", [])
    r1 = led.consider_revision("S3", "rev1", "rev1", [])            # claims only ungrounded objections -> nothing claimed
    r2 = led.consider_revision("S3", "rev2", "rev2", [])
    assert not r1["adopted"] and not r2["adopted"] and led.best()["label"] == "first"


# ---- R2 ------------------------------------------------------------------------------------------------------------------------------------------------
def test_r2_command_output_grounds_and_records_the_reproduction():
    log = [{"tool": "run_python", "args": {"code": "parse_duration('5x')"}, "failing": True, "output": "Traceback (most recent call last):\nValueError: bad unit in '5x'"}]
    g = oc.classify_objection("The patch accepts 5x. I ran it:\nTraceback (most recent call last):\nValueError: bad unit in '5x'", TASK, log)
    assert g["kind"] == "command" and g["repro"]["tool"] == "run_python"


def test_r2_verbatim_task_quote_grounds_but_a_paraphrase_does_not():
    assert oc.classify_objection('The task says "Anything else must raise ValueError" and the patch does not.', TASK, [])["kind"] == "quote"
    assert oc.classify_objection('The solution did not handle all edge cases such as leading/trailing whitespace and multiple spaces between digits and units.', TASK, [])["kind"] == "suggestion"
    assert oc.classify_objection('The task says "something it never said at all here" ok.', TASK, [])["kind"] == "suggestion"


def test_r2_replayed_duration_objections_none_is_grounded():
    ts = Path("/root/fruits/integration/ogi013-collab-proof/evidence/ogi013-micro/runs/micro__duration-1/T/team_state.md")
    if not ts.exists():
        pytest.skip("evidence not present")
    text = ts.read_text()
    o4 = text[text.index("- O4 on S3"):text.index("- O5 on S3")]
    assert oc.classify_objection(o4, TASK, [])["kind"] == "suggestion"          # O4 (whitespace tolerance) must not force a revision


# ---- R3 ------------------------------------------------------------------------------------------------------------------------------------------------
def test_r3_release_class_and_sha_citation():
    sha = oc.sha256("final diff")
    assert oc.release_class(True) == "RELEASED_UNANIMOUS_EXCELLENT" and oc.release_class(False) == "CANDIDATE_NO_CONSENSUS"
    assert oc.cites_sha(f"APPROVE: EXCELLENT for {sha}", sha) and oc.cites_sha(f"candidate {sha[:12]} ok", sha)
    assert not oc.cites_sha("APPROVE: EXCELLENT for the patch", sha) and not oc.cites_sha(f"candidate {oc.sha256('other')[:12]}", sha)


# ---- R4 ------------------------------------------------------------------------------------------------------------------------------------------------
DUR = Path("/root/fruits/research/OGI013-MICRO/micro__duration-1")


@pytest.mark.skipif(not DUR.exists(), reason="micro task tree not present")
def test_r4_a_reviewer_that_only_reads_team_state_can_run_the_command(tmp_path):
    py = str(DUR / "venv38/bin/python")
    labels = oc.visible_labels(DUR / "base")
    assert labels
    block = oc.howto_block(py, labels)
    cmd = oc.parse_shell(block)                                   # all the reviewer has: the block text
    tree = oc.tree_with_diff(DUR / "base", "", tmp_path / "tree")
    r = subprocess.run(cmd, shell=True, cwd=tree, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    assert "Ran " in (r.stdout + r.stderr) and "Ran 0 tests" not in (r.stdout + r.stderr)


@pytest.mark.skipif(not DUR.exists(), reason="micro task tree not present")
def test_r4_driver_runs_visible_checks_itself(tmp_path):
    tree = oc.tree_with_diff(DUR / "base", "", tmp_path / "t")
    res = oc.run_visible(str(DUR / "venv38/bin/python"), tree, oc.visible_labels(tree))
    assert res["executed"] > 0 and res["failed"] == 0


# ---- R5 / R8 -------------------------------------------------------------------------------------------------------------------------------------------
def test_r5_infra_author_failed_rule_matches_the_recorded_solo_run():
    assert oc.infra_author_failed({"steps": 16, "step_retries": 16}, 0)           # duration-1 S: 16 steps, 16 retries, no snapshot
    assert not oc.infra_author_failed({"steps": 16, "step_retries": 16}, 1)
    assert not oc.infra_author_failed({"steps": 25, "step_retries": 5}, 0)


def test_r8_roster_stays_constant_and_forced_failure_makes_exactly_one_change():
    ev = []
    r = Roster(emit=lambda k, **kw: ev.append(k))
    r.pin("solver1", "m-a", "A")
    r.pin("critic", "m-c", "C")
    for _ in range(200):                                         # a long episode: pins never move
        assert r.pinned("solver1") == "m-a" and r.pinned("critic") == "m-c"
    r.change("critic", "2 consecutive failed steps")
    r.pin("critic", "m-d", "D")
    assert ev.count("ROSTER_CHANGE") == 1 and r.pinned("critic") == "m-d" and r.check()["ok"]


def test_r8_more_than_five_models_without_a_change_fails_the_check():
    r = Roster()
    for i in range(6):
        r.note_model(f"m{i}")
    assert not r.check()["ok"] and r.check()["distinct_models"] == 6 > MAX_MODELS
    r.change("critic", "declared failure")
    assert r.check()["ok"]


def test_r8_solver_slots():
    r = Roster()
    assert next_solver_role(r, {}) == "solver1"
    r.pin("solver1", "a", "A")
    assert next_solver_role(r, {}) == "solver2"
    r.pin("solver2", "b", "B")
    assert next_solver_role(r, {"solver1": True, "solver2": False}) == "solver2"


def _loop_with_roster(script, roster, role_key="critic"):
    import time
    import ogi013_code_task as ct
    prefers, events, it = [], [], iter(script)

    class Ep:
        def blocking(self): return None
        def event(self, kind, **k): events.append(kind)
        def step(self, prompt, role, *, exclude=(), prefer=None, sticky_attempts=1):
            prefers.append((prefer, sticky_attempts))
            return next(it)
    ctx = SimpleNamespace(ep=Ep(), deadline=time.monotonic() + 60, keys={}, gate=None, effects=None)
    roster.emit = ctx.ep.event
    ct.pomelo_call = lambda ep, sb, eff, name, args, write: ("x", False)
    res = ct.agent_loop(ctx, "critic", "h", SimpleNamespace(), {"read_file"}, gated=False, roster=roster, role_key=role_key)
    return res, prefers, events


def _ok(model, action):
    return {"success": True, "output": action, "model_key": model, "independence_key": model.split("-")[0], "receipt_id": "r"}


FAIL = {"success": False, "output": None, "failure_class": "EXECUTION_NOT_PERFORMED_RATE_LIMITED"}
READ = '{"action": "tool", "name": "read_file", "arguments": {"path": "a.py"}}'
MSG = '{"action": "message", "content": "ISSUES: NONE"}'


def test_r8_pinned_model_is_requested_on_every_step_with_all_retries_sticky():
    r = Roster()
    res, prefers, ev = _loop_with_roster([_ok("m-a", READ), _ok("m-a", READ), _ok("m-a", MSG)], r)
    assert r.pinned("critic") == "m-a" and prefers[0][0] is None and all(p == ("m-a", 99) for p in prefers[1:]) and "ROSTER_CHANGE" not in ev


def test_r8_two_failed_steps_create_exactly_one_roster_change_and_a_new_pin():
    r = Roster()
    res, prefers, ev = _loop_with_roster([_ok("m-a", READ), FAIL, FAIL, _ok("m-b", MSG)], r)
    assert ev.count("ROSTER_CHANGE") == 1 and r.pinned("critic") == "m-b" and prefers[3][0] is None       # the replacement is chosen by AUTO, then pinned
