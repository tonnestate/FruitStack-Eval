"""Final order C.2-C.4 / D3, AMENDMENT-MANGO-1: scripted team episode on REAL MongoDB, no model calls, no episode start.
Run: MANGOME_TEST_MONGO_URI=mongodb://127.0.0.1:27017 PYTHONPATH=<components> pytest tests/test_ogi013_mango_acceptance.py"""
import asyncio
import json
import os
import signal
import subprocess
import sys
import textwrap
import time
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

URI = os.environ.get("MANGOME_TEST_MONGO_URI")
pytestmark = pytest.mark.skipif(not URI, reason="MANGOME_TEST_MONGO_URI not configured")
RUNNERS = str(Path(__file__).resolve().parent.parent / "runners")
sys.path.insert(0, RUNNERS)

SCRIPT = textwrap.dedent("""
    import json, os, sys, tempfile, time
    sys.path.insert(0, %r)
    from pathlib import Path
    from types import SimpleNamespace
    from mangome.storage.mongo import MongoStore
    from mangome.work_control import WorkGovernedMangoMeService
    from peachme.fruitstack import MangoWorkAdapter
    from ogi013_mango_ledger import MangoLedger
    from ogi013_team_code import TeamState
    from ogi013_vote import judge_vote, tally
    db, out, mode = os.environ["MANGOME_DATABASE"], Path(os.environ["OUT"]), os.environ["MODE"]
    svc = WorkGovernedMangoMeService(MongoStore(os.environ["MANGOME_MONGODB_URI"], db))
    if mode == "restore":
        led = MangoLedger(MangoWorkAdapter(svc), os.environ["WORK"], "host", os.environ["TURN"], "restore")
        t = TeamState.restore(led, out / "restored_state.md")
        (out / "restored.txt").write_text(t.text())
        print(json.dumps({"ok": True})); sys.exit(0)
    e = svc.enter_work(workspace_id=tempfile.mkdtemp(), workspace_title="scripted", actor_id="host", request_text="scripted team episode " + db)
    work, turn = e["work_identity"]["entity_id"], e["turn"]["entity_id"]
    led = MangoLedger(MangoWorkAdapter(svc), work, "host", turn, "scripted")
    t = TeamState("fix the issue", out / "team_state.md"); t.mango = led
    pos = lambda i, m, d: SimpleNamespace(id=i, model=m, status="open", rev=0, diff=d, test_tail="Ran 3 tests ... OK" if d else "")
    t.pos["S1"] = pos("S1", "model-a", "+fix one\\n"); t.pos["S2"] = pos("S2", "model-b", "+fix two\\n")
    led.write("TEAM_SNAPSHOT", "S1:first", {"pos": "S1", "sha256": "x"}); led.write("TEAM_SNAPSHOT", "S2:first", {"pos": "S2", "sha256": "y"})
    t.decisions.append("S1 produced its first gate-accepted diff"); t.decisions.append("S2 produced its first gate-accepted diff")
    oid = t.objection("S1", "lineage-b", "the fix misses the second branch (django/x.py:10)", grounded=True)
    t.pos["S1"].diff += "+second branch\\n"; t.pos["S1"].rev = 1; t.pos["S1"].status = "revised"
    t.revise("S1", 1, True, [oid])
    t.decisions.append("S1 revised after criticism (revision 1, changed)")
    open(out / "ids.json", "w").write(json.dumps({"work": work, "turn": turn, "db": db}))
    (out / "before.txt").write_text(t.text())               # state before the (optional) kill: persisted by text()
    if mode == "kill_after_revision":
        print("READY", flush=True); time.sleep(120)
    ns = time.monotonic_ns()
    t.reexamine("S1", f"ISSUES: NONE\\n{oid}: RESOLVED", "lineage-b", ("lineage-a",), [(time.monotonic_ns(), "ran tests")])
    t.pos["S1"].status = "validated"
    votes = [judge_vote("APPROVE: EXCELLENT\\nchecked django/x.py ran tests ok\\nOWN_OBJECTIONS: " + ("%%s fixed in revision 1" %% oid if lin == "lineage-b" else "NONE"), lin, t.objs, "S1", [(time.monotonic_ns(), "ok")], 0, True) for lin in ("lineage-b", "lineage-c", "lineage-d")]
    t.votes += [{"voter": v, "verdict": x["verdict"]} for v, x in zip(("b", "c", "d"), votes)]
    t.release = {"class": tally(votes), "released": "S1", "sha256": "z"}
    t.persist(); (out / "after.txt").write_text(t.text())
    print(json.dumps({"class": t.release["class"], "work": work}))
""" % RUNNERS)


def run(mode, db, out, extra=None, wait=True):
    env = {**os.environ, "MANGOME_BACKEND": "mongo", "MANGOME_MONGODB_URI": URI, "MANGOME_DATABASE": db, "MANGOME_ZERO_TOUCH_BOOTSTRAP": "0", "OUT": str(out), "MODE": mode,
           "PYTHONDONTWRITEBYTECODE": "1", **(extra or {})}
    p = subprocess.Popen([sys.executable, "-c", SCRIPT], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if not wait:
        return p
    o, e = p.communicate(timeout=180)
    assert p.returncode == 0, e[-1500:]
    return json.loads(o.strip().splitlines()[-1])


def count_writes(db, work_ref=None, label="") -> int:
    """MangoMe checkpoint writes recorded for the test (reported per test in the repair report; MANGO_COUNTS_OUT=file appends them)."""
    from mangome.storage.mongo import MongoStore
    st = MongoStore(URI, db)
    n = st.db["work_checkpoints"].count_documents({"work_id": work_ref} if work_ref else {})
    st.client.close()
    if os.environ.get("MANGO_COUNTS_OUT"):
        with open(os.environ["MANGO_COUNTS_OUT"], "a") as fh:
            fh.write(json.dumps({"test": label, "checkpoints": n}) + "\n")
    return n


def drop(db):
    from mangome.storage.mongo import MongoStore
    s = MongoStore(URI, db)
    s.client.drop_database(db)
    s.client.close()


def test_scripted_episode_is_readable_through_mcp_work_context(tmp_path):
    db = f"mangome_accept_{uuid.uuid4().hex}"
    try:
        r = run("full", db, tmp_path)
        assert r["class"] == "RELEASED_UNANIMOUS_EXCELLENT"
        ids = json.loads((tmp_path / "ids.json").read_text())
        count_writes(db, ids["work"], "scripted_episode_mcp_readback")
        os.environ.update({"MANGOME_BACKEND": "mongo", "MANGOME_MONGODB_URI": URI, "MANGOME_DATABASE": db, "MANGOME_ZERO_TOUCH_BOOTSTRAP": "0"})
        from mcp.client.client import Client
        from mangome import worker_mcp_server
        from mangome.runtime import reset_service_for_tests
        reset_service_for_tests()

        async def read():
            async with Client(worker_mcp_server.mcp) as c:
                res = await c.call_tool("mangome_query", {"operation": "WORK_CONTEXT", "payload": {"work_ref": ids["work"]}})
                return res.structured_content.get("result", res.structured_content)
        out = asyncio.run(read())
        ctx = out if "progressive" in out else out["result"]          # the facade envelope or its result, depending on the client
        full = ctx["progressive"]["latest_checkpoint"]["payload"]
        assert {p["id"] for p in full["pos"]} == {"S1", "S2"} and all(p["sha256"] for p in full["pos"])
        assert [o["state"] for o in full["objs"]] == ["VERIFIED_RESOLVED"] and full["release"]["class"] == "RELEASED_UNANIMOUS_EXCELLENT" and len(full["votes"]) == 3
        reset_service_for_tests()
    finally:
        drop(db)


def test_restart_restores_team_state_byte_identical_from_mangome_alone(tmp_path):
    db = f"mangome_restart_{uuid.uuid4().hex}"
    try:
        p = run("kill_after_revision", db, tmp_path, wait=False)
        assert p.stdout.readline().strip() == "READY"
        p.send_signal(signal.SIGKILL)                      # the episode dies after the revision
        p.wait()
        ids = json.loads((tmp_path / "ids.json").read_text())
        count_writes(db, ids["work"], "restart_restore_before_kill")
        run("restore", db, tmp_path, extra={"WORK": ids["work"], "TURN": ids["turn"]})
        assert (tmp_path / "restored.txt").read_text() == (tmp_path / "before.txt").read_text()
    finally:
        drop(db)


def test_two_episodes_get_distinct_work_and_turn_and_cannot_cross_write_or_read(tmp_path):
    from mangome.storage.mongo import MongoStore
    from mangome.work_control import WorkGovernedMangoMeService
    from ogi013_mango_ledger import InfraMangoFailed, MangoLedger
    from peachme.fruitstack import MangoWorkAdapter
    db = f"mangome_d3_{uuid.uuid4().hex}"
    svc = WorkGovernedMangoMeService(MongoStore(URI, db))
    try:
        eps = []
        for i in range(2):
            e = svc.enter_work(workspace_id=str(tmp_path / f"ep{i}"), workspace_title=f"ep{i}", actor_id="host", request_text=f"scripted episode number {i} of the D3 test")
            eps.append((e["work_identity"]["entity_id"], e["turn"]["entity_id"]))
        (wa, ta), (wb, tb) = eps
        assert wa != wb and ta != tb
        ad = MangoWorkAdapter(svc)
        la, lb = MangoLedger(ad, wa, "host", ta, "A"), MangoLedger(ad, wb, "host", tb, "B")
        la.write("TEAM_STATE_FULL", "full", {"goal": "A-goal"})
        lb.write("TEAM_STATE_FULL", "full", {"goal": "B-goal"})
        assert la.latest()["goal"] == "A-goal" and lb.latest()["goal"] == "B-goal"        # neither reads the other's checkpoints
        count_writes(db, wa, "two_episodes_A"); count_writes(db, wb, "two_episodes_B")
        assert ad.turn_authorized(wa, ta, "host") and not ad.turn_authorized(wa, tb, "host") and not ad.turn_authorized(wb, ta, "host")
        with pytest.raises(InfraMangoFailed):                                              # A's work with B's turn: a cross write is refused (fail closed)
            MangoLedger(ad, wa, "host", tb, "X").write("TEAM_STATE_FULL", "full", {"goal": "cross"})
        assert la.latest()["goal"] == "A-goal"
    finally:
        svc.store.client.drop_database(db)


def test_forced_mangome_write_error_ends_the_episode_infra_mangome_failed(tmp_path):
    """C.2: not an Exception subclass (no `except Exception` can swallow it), and the driver's exit writes status INFRA_MANGOME_FAILED."""
    import ogi013_team_code as tc
    from ogi013_mango_ledger import InfraMangoFailed, MangoLedger

    class Broken:
        def checkpoint(self, *a, **k):
            raise RuntimeError("mongo down")
    led = MangoLedger(Broken(), "w", "a", "t", "r")
    assert not issubclass(InfraMangoFailed, Exception)
    t = tc.TeamState("goal", tmp_path / "ts.md")
    t.mango = led
    with pytest.raises(InfraMangoFailed):
        t.text()
    events = []
    ep = SimpleNamespace(event=lambda k, **kw: events.append(k), close=lambda s: events.append("closed:" + s), work="w", turn_id="t", project="p")
    assert tc.infra_failed_exit(ep, tmp_path, InfraMangoFailed("x"), time.monotonic()) == 3
    assert json.loads((tmp_path / "run.json").read_text())["status"] == "INFRA_MANGOME_FAILED" and "closed:INFRA_MANGOME_FAILED" in events


def test_eval_scoped_mcp_is_read_only_and_reads_the_evaluation_database(tmp_path):
    """D1: real MCP stdio round trip against the evaluation-scoped instance on a scratch evaluation database."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    db = f"mangome_eval_scope_{uuid.uuid4().hex}"
    out = tmp_path
    try:
        run("full", db, out)
        ids = json.loads((out / "ids.json").read_text())
        params = StdioServerParameters(command=sys.executable, args=[str(Path(RUNNERS) / "mangome_eval_mcp.py"), "--database", db],
                                       env={**os.environ, "MANGOME_MONGODB_URI": URI, "MANGOME_BACKEND": "mongo", "MANGOME_WORKSPACE_ROOT": str(out)})

        async def go():
            async with stdio_client(params) as (r, w):
                async with ClientSession(r, w) as session:
                    await session.initialize()
                    names = {t.name for t in (await session.list_tools()).tools}
                    res = await session.call_tool("mangome_query", {"operation": "WORK_CONTEXT", "payload": {"work_ref": ids["work"]}})
                    try:
                        denied = await session.call_tool("mangome_work", {"operation": "CHECKPOINT_WORK", "payload": {}})
                        denied_error = denied.is_error
                    except Exception:  # noqa: BLE001 - unknown tool
                        denied_error = True
                    return names, res, denied_error
        names, res, denied_error = asyncio.run(go())
        assert names == {"mangome_status", "mangome_observe", "mangome_query"} and denied_error
        payload = json.dumps(res.structured_content, default=str)
        assert "TEAM_STATE_FULL" in payload or "RELEASED_UNANIMOUS_EXCELLENT" in payload
        refused = subprocess.run([sys.executable, str(Path(RUNNERS) / "mangome_eval_mcp.py"), "--database", "mangome"], capture_output=True, text=True)
        assert refused.returncode != 0 and "REFUSED" in (refused.stderr + refused.stdout)
    finally:
        drop(db)


def test_4_concurrent_solvers_and_critics_write_at_once_no_write_lost_gap_free_sequence_and_identical_restore(tmp_path):
    """Parallel order test 4: two solvers and two critics hit the ledger at the same time against real MongoDB."""
    import threading

    import ogi013_team_code as tc
    from mangome.storage.mongo import MongoStore
    from mangome.work_control import WorkGovernedMangoMeService
    from ogi013_mango_ledger import MangoLedger
    from peachme.fruitstack import MangoWorkAdapter
    db = f"mangome_conc_{uuid.uuid4().hex}"
    svc = WorkGovernedMangoMeService(MongoStore(URI, db))
    try:
        e = svc.enter_work(workspace_id=str(tmp_path / "w"), workspace_title="conc", actor_id="host", request_text="concurrent ledger writes test")
        work, turn = e["work_identity"]["entity_id"], e["turn"]["entity_id"]
        led = MangoLedger(MangoWorkAdapter(svc), work, "host", turn, "conc")
        t = tc.TeamState("goal", tmp_path / "ts.md")
        t.mango = led
        for pid in ("S1", "S2"):
            t.pos[pid] = SimpleNamespace(id=pid, model="m", status="open", rev=0, diff="", test_tail="", slot="solver1" if pid == "S1" else "solver2")
        gate = threading.Barrier(4)

        def solver(pid):
            gate.wait()
            for i in range(5):
                t.pos[pid].diff = f"+{pid} v{i}\n"
                t.pos[pid].test_tail = f"Ran {i} tests"
                t.persist()

        def critic(n):
            gate.wait()
            for i in range(5):
                t.objection("S1" if n == 0 else "S2", f"lin{n}", f"critic {n} objection {i}", ground={"kind": "quote", "quote": "x"})
        ths = [threading.Thread(target=solver, args=("S1",)), threading.Thread(target=solver, args=("S2",)), threading.Thread(target=critic, args=(0,)), threading.Thread(target=critic, args=(1,))]
        [x.start() for x in ths]
        [x.join() for x in ths]
        t.persist()
        st = MongoStore(URI, db)
        rows = list(st.db["work_checkpoints"].find({"work_id": work}))
        seqs = sorted(r["payload"]["seq"] for r in rows)
        assert len(rows) == led.writes and seqs == list(range(1, led.writes + 1))              # nothing lost, sequence numbers gap-free
        live = t.text()
        restored = tc.TeamState.restore(MangoLedger(MangoWorkAdapter(svc), work, "host", turn, "restore"), tmp_path / "ts2.md")
        assert restored.text() == live and len(restored.objs) == 10                               # rendered from MangoMe alone == the live state
        st.client.close()
    finally:
        svc.store.client.drop_database(db)
