"""COLLAB-1 acceptance: a multi-task campaign through the REAL launcher (run_collab1.py -> run_arm.sh -> bootstrap -> official tau2 -> the real stack, gate, ParentBudget, guard and evaluator). The only substitution is the
provider transport (tests/ogi013_offline_transport, scripted per task and condition). MangoMe runs on a scratch copy of the evaluation database. No inference, no network (proxies point at a dead port)."""
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from ogi013_pilot_fixtures import ROOT
from test_ogi013_pilot_e2e import REAL, scratch_db  # noqa: F401 - the scratch database fixture is shared with the pilot end-to-end tests

DATA = REAL / "benchmarks/tau2-bench/data/tau2"

pytest.importorskip("plumme")
pytestmark = pytest.mark.skipif(not (REAL / "env.sh").is_file() or not (REAL / "runs/work.env").is_file() or not (REAL / "benchmarks/tau2-bench").is_dir() or not shutil.which("mongosh"),
                                reason="needs the ogi-013 evaluation base, the tau2 checkout and a local MongoDB")
CONDS = ["SINGLE", "COLLAB", "SINGLE-E"]
WRONG = {"name": "cancel_reservation", "arguments": {"reservation_id": "4WQ150"}}                    # exists in every airline database; the API does not check the policy -> a state-changing deviation
MSG = {"message": "Done. Is there anything else I can help with?"}
OK_REVIEW = "ISSUES: NONE\nChecked the action against the policy and the conversation: it matches the customer's request and the reservation facts."


def writes(ref):
    tid = ref.split(":")[1]
    task = next(t for t in json.loads((DATA / "domains/airline/tasks.json").read_text()) if str(t["id"]) == tid)
    return [{"name": a["name"], "arguments": a["arguments"]} for a in task["evaluation_criteria"]["actions"] if a["name"] in ("book_reservation", "cancel_reservation", "update_reservation_flights",
                                                                                                                              "update_reservation_passengers", "update_reservation_baggages")]


def spec():
    sim = ["Hello, I need help with my request.", "Yes, that is correct, please go on.", "###STOP###"]
    tasks = {}
    # S1 premature stop: the customer confirms and stops in ONE message, before the write
    tasks["airline:24"] = {"*": {"sim": ["Hello, I would like to book a round trip.", "Yes, that is correct, please proceed. ###STOP###"], "draft": [{"message": "Please confirm the flights and the payment."}, MSG]}}
    # S3 critique prevents a wrong write (COLLAB), the draw of three drafts out-votes it (SINGLE-E), SINGLE executes it
    ok = writes("airline:25")[0]
    tasks["airline:25"] = {"*": {"sim": sim, "draft": [WRONG, MSG, MSG], "challenge": ["ISSUES: FOUND\nThe action cancels a booking although the customer asked to book a trip; book the requested trip instead.", OK_REVIEW], "revise": [ok]},
                           "SINGLE-E": {"draft": [WRONG, ok, ok, MSG, MSG, MSG]}}
    # S4 a correct action is rejected by the critique and replaced by a wrong write (COLLAB)
    ok = writes("airline:30")[-1]
    tasks["airline:30"] = {"*": {"sim": sim, "draft": [ok, MSG, MSG], "challenge": ["ISSUES: FOUND\nThe update must be replaced by a cancellation of the reservation.", OK_REVIEW], "revise": [WRONG]},
                           "SINGLE-E": {"draft": [ok, ok, ok, MSG, MSG, MSG]}}
    # S5 the PILOT-4 shape, repaired: the rejected cancel became a transfer, the termination review adopts a continuing alternative, the booking is completed
    ok = writes("airline:35")[0]
    keep_going = 'OPEN_REQUESTS: book the requested trip\nTERMINATION_REQUIRED_CLAUSE: NONE\nALTERNATIVE: {"action": "message", "content": "I cannot cancel that booking under the policy. Let us continue with your booking."}\nVERDICT: CONTINUE'
    tasks["airline:35"] = {"*": {"sim": sim, "draft": [ok, MSG, MSG]}, "COLLAB": {"draft": [WRONG, ok, MSG, MSG], "challenge": ["ISSUES: FOUND\nCancellation is not allowed here; transfer the customer to a human agent.", OK_REVIEW],
                                                                              "revise": [{"name": "transfer_to_human_agents", "arguments": {"summary": "cancellation not possible"}}], "termination": [keep_going]},
                           "SINGLE-E": {"draft": [ok, ok, ok, MSG, MSG, MSG]}}
    # S7 one error replaced by a different error (a second wrong write): the executed deviation stays visible
    ok = writes("airline:8")[-1]
    other = {"name": "cancel_reservation", "arguments": {"reservation_id": "VAAOXJ"}}
    tasks["airline:8"] = {"*": {"sim": sim, "draft": [ok, MSG, MSG]}, "COLLAB": {"draft": [WRONG, MSG, MSG], "challenge": ["ISSUES: FOUND\nThis cancels the wrong booking; cancel the other one instead.", OK_REVIEW], "revise": [other]},
                          "SINGLE-E": {"draft": [ok, ok, ok, MSG, MSG, MSG]}}
    # S6 a provider that rejects every 5th request and an answer cut off by the output limit (continuation); the work still succeeds
    ok = writes("airline:37")[-1]
    tasks["airline:37"] = {"*": {"sim": sim, "draft": [ok, MSG, MSG], "challenge": [OK_REVIEW], "fail_every": 5, "truncate_first_draft": 40}, "SINGLE-E": {"draft": [ok, ok, ok, MSG, MSG, MSG], "fail_every": 5, "truncate_first_draft": 40}}
    tasks["airline:16"] = {"*": {"sim_fail": True}}                                                      # simulator outage: whole-block discard, 3 attempts, INFRA_INCOMPLETE (non-success)
    return {"tasks": tasks}


ORDERS = {"airline:24": CONDS, "airline:25": ["COLLAB", "SINGLE-E", "SINGLE"], "airline:30": ["SINGLE-E", "SINGLE", "COLLAB"], "airline:35": ["SINGLE", "COLLAB", "SINGLE-E"], "airline:37": ["COLLAB", "SINGLE", "SINGLE-E"], "airline:16": ["SINGLE-E", "COLLAB", "SINGLE"], "airline:8": ["COLLAB", "SINGLE-E", "SINGLE"]}


def world(tmp: Path, db: str, refs=tuple(ORDERS), budget_edit=None):
    base, code, transport = tmp / "base", tmp / "code", tmp / "transport"
    (base / "runs").mkdir(parents=True)
    (base / "benchmarks").mkdir()
    (base / "benchmarks/tau2-bench").symlink_to(REAL / "benchmarks/tau2-bench")
    (base / "env.sh").write_text((REAL / "env.sh").read_text().replace("mangome_ogi013_eval", db).replace(f"D={REAL}", f"D={base}"))
    shutil.copy(REAL / "runs/work.env", base / "runs/work.env")
    for n in ("chat", "project"):
        subprocess.run(["git", "clone", "-q", "--bare", str(REAL / f"slots/D/ledgers/{n}.git"), str(base / f"slots/D/ledgers/{n}.git")], check=True)
    shutil.copytree(ROOT / "runners", code / "runners", ignore=shutil.ignore_patterns("__pycache__"))
    for d in ("ogi013-pilot", "ogi013-phase2", "ogi013-collab1"):
        shutil.copytree(ROOT / "evidence" / d, code / "evidence" / d, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "tests/ogi013_offline_transport", transport)
    (code / ".gitignore").write_text("__pycache__/\n")
    subprocess.run("git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm sim", shell=True, cwd=code, check=True)
    manifest = {"study": "OGI-013-COLLAB-1-ACCEPTANCE", "version": 2, "conditions": CONDS, "single_e": {"k": 3, "scope": "writes"},
                "tasks": [{"stratum": "write-opportunity", "domain": "airline", "task_id": r.split(":")[1], "task_ref": r, "order": ORDERS[r]} for r in refs]}
    (tmp / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (tmp / "spec.json").write_text(json.dumps(spec()))
    budget = json.loads((code / "evidence/ogi013-collab1/collab1_budget.json").read_text())
    budget["manifest_sha256"] = hashlib.sha256((tmp / "manifest.json").read_bytes()).hexdigest()
    if budget_edit:
        budget_edit(budget)
    (tmp / "budget.json").write_text(json.dumps(budget, indent=1))
    (tmp / "approval.txt").write_text(hashlib.sha256((tmp / "budget.json").read_bytes()).hexdigest() + "\n")
    return SimpleNamespace(tmp=tmp, base=base, code=code, transport=transport, C=base / "runs/collab1", log=tmp / "transport.jsonl")


def launch(w, *extra, approval=None, wait=True, timeout=3000):
    env = {k: v for k, v in os.environ.items() if not any(t in k.upper() for t in ("API_KEY", "FLM_KEY", "TOKEN", "SECRET")) and k not in ("PLUMME_STATE_DIR",)}
    env.update({"PILOT_OFFLINE_TRANSPORT": str(w.transport), "PILOT_OFFLINE_TRANSPORT_LOG": str(w.log), "PILOT_OFFLINE_CAMPAIGN": str(w.tmp / "spec.json"), "PILOT_POLL_S": "1",
                "HTTP_PROXY": "http://127.0.0.1:9", "HTTPS_PROXY": "http://127.0.0.1:9", "ALL_PROXY": "http://127.0.0.1:9", "http_proxy": "http://127.0.0.1:9", "https_proxy": "http://127.0.0.1:9", "NO_PROXY": "127.0.0.1,localhost"})
    cmd = [sys.executable, str(w.code / "evidence/ogi013-collab1/run_collab1.py"), "--approval", approval or str(w.tmp / "approval.txt"), "--base", str(w.base), "--budget", str(w.tmp / "budget.json"),
           "--manifest", str(w.tmp / "manifest.json"), *extra]
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    if not wait:
        return p
    out, err = p.communicate(timeout=timeout)
    return SimpleNamespace(rc=p.returncode, out=out, err=err)


def records(w):
    return {p.relative_to(w.C).as_posix(): json.loads(p.read_text()) for p in sorted(w.C.glob("*/*.episode.json"))}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_launcher_refuses_without_approval_and_on_a_modified_manifest(tmp_path, scratch_db):
    w = world(tmp_path, scratch_db, refs=("airline:24",))
    assert launch(w, approval=str(tmp_path / "nope.txt")).rc == 2
    (tmp_path / "manifest.json").write_text((tmp_path / "manifest.json").read_text() + " ")
    r = launch(w)
    assert r.rc == 2 and "manifest" in r.err and not w.C.exists()


def test_a_multi_task_campaign_through_the_real_launcher_survives_a_restart_and_is_evaluated(tmp_path, scratch_db):
    w = world(tmp_path, scratch_db)
    p = launch(w, wait=False)
    deadline = time.time() + 2400
    while time.time() < deadline and p.poll() is None:                                              # interrupt the campaign after four finished episodes
        if sum(1 for r in records(w).values() if r["status"] in ("DONE", "BUDGET_STOP", "TIMEOUT")) >= 4:
            os.killpg(p.pid, signal.SIGTERM)
            break
        time.sleep(2)
    out, err = p.communicate(timeout=300)
    assert p.returncode in (130, 0), err[-800:]
    before = {k: sha(w.C / k.replace(".episode.json", "") / "tasks" / k.split("/")[0].split("_")[1] / "official-result.json") for k, r in records(w).items() if r["status"] == "DONE"}
    assert len(before) >= 4
    r = launch(w)                                                                                    # restart: unfinished work only
    assert r.rc == 0, (r.rc, r.err[-1500:])
    after = records(w)
    for k, h in before.items():
        assert sha(w.C / k.replace(".episode.json", "") / "tasks" / k.split("/")[0].split("_")[1] / "official-result.json") == h      # completed episodes were never run again
    assert len(after) == 18 and all(v["status"] == "DONE" for v in after.values()), {k: v["status"] for k, v in after.items()}
    sent = [json.loads(x) for x in w.log.read_text().splitlines()]
    assert sent and all(x["provider"].startswith("offline-") for x in sent)                          # only the scripted transport ever answered
    rep = json.loads((w.C / "report.json").read_text())
    # ---- what each scripted scenario must produce, from the OFFICIAL results ---------------------------------------------------------------------------------------
    def reward(ref, cond):
        d = w.C / ref.replace(":", "_") / cond / "tasks" / ref.split(":")[1] / "official-result.json"
        return json.loads(d.read_text())["reward_info"]["reward"]
    assert [reward("airline:24", c) for c in CONDS] == [0.0, 0.0, 0.0]                              # simulator STOP with the booking pending
    assert [reward("airline:25", c) for c in CONDS] == [0.0, 1.0, 1.0]                              # critique prevented the wrong write; the vote out-voted it; SINGLE executed it
    assert [reward("airline:30", c) for c in CONDS] == [1.0, 0.0, 1.0]                              # the critique rejected a correct action
    assert [reward("airline:35", c) for c in CONDS] == [1.0, 1.0, 1.0]                              # the PILOT-4 shape, repaired: no transfer, the booking is completed
    assert [reward("airline:8", c) for c in CONDS] == [1.0, 0.0, 1.0]                               # one wrong write replaced by a different wrong write (validated-correct: the two correct writes reviewed in 35 and 37)
    assert [reward("airline:37", c) for c in CONDS] == [1.0, 1.0, 1.0]                              # providers failing and continuing answers did not stop the work
    o = rep["decision_outcomes"]
    assert (o.get("PREVENTED_WRITE_ERROR"), o.get("CORRECT_BLOCKED"), o.get("ERROR_REPLACED_BY_DIFFERENT_ERROR"), o.get("VALIDATED_CORRECT")) == (2, 1, 1, 2)
    assert rep["premature_stop_episodes"] == {"SINGLE": 1, "COLLAB": 1, "SINGLE-E": 1}
    e1 = rep["confirmatory"]["E1"]
    assert (e1["a_only"], e1["b_only"], e1["pairs"]) == (1, 2, 7) and not e1["significant_at_0.05"]
    assert rep["decision_quality"]["COLLAB"]["unnecessary_transfer_episodes"] == 0 and rep["decision_quality"]["SINGLE"]["state_changing_deviation_episodes"] == 1          # the repaired transfer never happened
    assert rep["decision_quality"]["COLLAB"]["state_changing_deviation_episodes"] == 2
    ev35 = [json.loads(x) for x in (w.C / "airline_35/COLLAB/tasks/35/fruitstack-events.jsonl").read_text().splitlines()]
    assert any(e["event"] == "CONTINUITY_CHECKPOINT" for e in ev35) and json.loads((w.C / "airline_35/COLLAB/tasks/35/continuity.json").read_text())["objectives"]         # written to the real MangoMe graph
    assert rep["infra_incomplete_blocks"] == ["airline_16"] and rep["episode_status"] == {"DONE": 18, "MISSING": 3}                # the outage block is non-success and stays visible
    assert rep["resources"]["COLLAB"]["requests"] > 0 and rep["resources"]["SINGLE-E"]["requests"] > rep["resources"]["SINGLE"]["requests"]          # k drafts on the writes cost more requests
    assert rep["resources"]["COLLAB"]["cash_usd"] == 0.0
    # request accounting: the continuation made one receipt stand for several provider requests, and the guard counted them all
    u = subprocess.run([sys.executable, str(w.code / "evidence/ogi013-pilot/pilot_guard.py"), "usage", str(w.base / "runs"), "collab1/airline_37/SINGLE"], capture_output=True, text=True).stdout
    rows = [json.loads(x) for x in (w.C / "airline_37/SINGLE/fruitstack/plumme-state/receipts.jsonl").read_text().splitlines()]
    assert json.loads(u)["dispatches"] == sum(max(1, int((x["metadata"] or {}).get("provider_attempt_count") or 0)) for x in rows) > len(rows)
    # the report is reproducible
    sys.path.insert(0, str(w.code / "evidence/ogi013-collab1"))
    first = (w.C / "report.json").read_bytes()
    subprocess.run([sys.executable, str(w.code / "evidence/ogi013-collab1/analyze_study.py"), str(w.C), str(tmp_path / "manifest.json"), str(tmp_path / "budget.json"), str(w.base / "benchmarks/tau2-bench/data/tau2")],
                   check=True, capture_output=True)
    assert (w.C / "report.json").read_bytes() == first


def test_the_study_base_is_an_isolated_copy_and_never_overwrites(tmp_path):
    prep = __import__("importlib.util").util.spec_from_file_location("prep", ROOT / "evidence/ogi013-collab1/prepare_study_base.py")
    mod = __import__("importlib.util").util.module_from_spec(prep)
    prep.loader.exec_module(mod)
    db = f"mangome_ogi013_prep_{os.getpid()}_{__import__('uuid').uuid4().hex[:8]}"
    before = mod.counts(mod.SOURCE_DB)
    try:
        assert mod.main(["--target", str(tmp_path / "b"), "--db", db]) == 0
        info = json.loads((tmp_path / "b/STUDY_BASE.json").read_text())
        assert info["collection_counts"] == before and mod.counts(mod.SOURCE_DB) == before          # a faithful copy; the evaluation database is untouched
        assert db in (tmp_path / "b/env.sh").read_text() and mod.SOURCE_DB not in (tmp_path / "b/env.sh").read_text()
        assert mod.main(["--target", str(tmp_path / "b"), "--db", db]) == 2 and mod.main(["--target", str(tmp_path / "c"), "--db", db]) == 2          # no overwrite of the directory nor of the database
        assert info["ledger_heads"] == {n: subprocess.run(["git", "--git-dir", str(REAL / f"slots/D/ledgers/{n}.git"), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() for n in ("chat", "project")}
    finally:
        mod.mongosh(f"db.getSiblingDB('{db}').dropDatabase()")


def test_collab1_tasks_share_no_id_with_c3_and_no_runner_reads_the_reference():
    m = json.loads((ROOT / "evidence/ogi013-collab1/study_manifest_v2.json").read_text())
    c3_airline = {str(i) for i in json.loads((DATA / "domains/airline/split_tasks.json").read_text())["test"]}
    lines = (REAL / "runs/retail_test_tasks.txt").read_text().splitlines()
    c3_retail = set(lines[1].split())                                                                 # the actual C3 retail task list (train 26 + held-out 14 by the registered hash split)
    mine = {(t["domain"], t["task_id"]) for t in m["tasks"]}
    assert not mine & ({("airline", i) for i in c3_airline} | {("retail", i) for i in c3_retail})
    assert len(mine) == m["n_tasks"] == 48 and all(sorted(t["order"]) == sorted(CONDS) for t in m["tasks"])
    for pos in (0, 2):                                                                                # balanced: each condition first / last equally often
        assert {c: sum(t["order"][pos] == c for t in m["tasks"]) for c in CONDS} == {c: 16 for c in CONDS}
