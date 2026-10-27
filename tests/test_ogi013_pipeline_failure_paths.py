"""End-to-end failure injection for the REAL block_queue.sh + supervisor.sh against a sandbox runs dir and a fake launcher.
Proves: technical failures never produce BLOCK_DONE / QUEUE_DONE / PIPELINE_COMPLETE; interrupted blocks are recovered with state restored;
mixed airline/retail keys reach the launcher with the right domain and raw task id. No provider calls."""
import os, re, signal, subprocess, textwrap, time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "evidence/ogi013-supervisor/supervisor.sh"
KPY = "/root/SUPPLY-001/venv3.12/bin/python"
pytestmark = pytest.mark.skipif(not Path(KPY).exists(), reason="needs the VPS venv for the split helper")

LAUNCHER = textwrap.dedent('''\
    #!/bin/bash
    # fake run_org.sh: OUTARG TASK DOMAIN MODE PAIR SLOT ; behaviour from $R/behavior
    R=$(cd "$(dirname "$0")" && pwd); echo "$3 $2 $4" >> "$R/calls.log"
    B=$(cat "$R/behavior")
    [ -n "${OGI013_ORG_STATE_DIR:-}" ] && { mkdir -p "$OGI013_ORG_STATE_DIR"; echo "$2" >> "$OGI013_ORG_STATE_DIR/touched"; }
    case "$B" in
      ok) mkdir -p "$R/$1/tasks/$2"; echo '{"reward_info":{"reward":1.0}}' > "$R/$1/tasks/$2/official-result.json" ;;
      crash) exit 1 ;;
      nores) exit 0 ;;
      simfail) echo SIM_ROUTE_FAILED; exit 1 ;;
      hang) sleep 300 ;;
    esac
''')


def sandbox(tmp_path, behavior="ok"):
    r = tmp_path / "runs"
    for t in (2, 3):
        for arm in ("fixed", "adaptive"):
            d = r / f"c2-airline-test/{t}-{arm}/tasks/{t}"; d.mkdir(parents=True); (d / "official-result.json").write_text("{}")
    (r / "retail_test_tasks.txt").write_text("3\n5 9 12 17\n")
    (r / "run_org.sh").write_text(LAUNCHER); (r / "run_org.sh").chmod(0o755)
    (r / "behavior").write_text(behavior)
    src = SUP.read_text().replace("R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs;", f"R={r};").replace("sleep 60", "sleep 0").replace("2 6 8 13 16 18 19 22 24 25 26 29 30 31 32 35 37 44 45 48", "2 3")
    pre = tmp_path / "prereg"; pre.mkdir()                      # the lock is written next to PROTOCOL.md: keep it OUT of the real repo
    (pre / "PROTOCOL.md").write_text((ROOT / "evidence/ogi013-c3-prereg/PROTOCOL.md").read_text())
    src = src.replace("P=$EV/ogi013-c3-prereg; Q=$P/queue", f"Q=$EV/ogi013-c3-prereg/queue; P={pre}")
    assert f"P={pre}" in src
    (tmp_path / "sup.sh").write_text(src)
    funcs = re.sub(r"^for s in wait_c2.*\Z", "", src, flags=re.S | re.M)
    (tmp_path / "funcs.sh").write_text(funcs)
    return r


def sh(tmp_path, body, timeout=120):
    return subprocess.run(["bash", "-c", f"source {tmp_path}/funcs.sh; {body}"], capture_output=True, text=True, timeout=timeout, env={**os.environ, "DRY_RUN": ""})


def test_success_routes_mixed_domains_and_marks_done(tmp_path):
    r = sandbox(tmp_path)
    p = sh(tmp_path, "stage_phaseA"); assert p.returncode == 0, p.stderr[-400:]
    calls = (r / "calls.log").read_text().split("\n")
    assert "airline 2 rg2" in calls and "airline 3 rg2" in calls and any(c.startswith("retail ") for c in calls)
    c = r / "c3-phaseA"
    assert all((d / "BLOCK_DONE").exists() for d in c.iterdir() if d.name.startswith(("airline:", "retail:")))
    assert "QUEUE_DONE" in (c / "progress.txt").read_text()


@pytest.mark.parametrize("behavior,cause", [("crash", "EXECUTION_FAILED"), ("nores", "MISSING_OR_INVALID_OFFICIAL_RESULT"), ("simfail", "BLOCKED")])
def test_technical_failure_never_completes(tmp_path, behavior, cause):
    r = sandbox(tmp_path, behavior)
    p = sh(tmp_path, "stage_phaseA"); assert p.returncode != 0
    c = r / "c3-phaseA"; prog = (c / "progress.txt").read_text()
    assert cause in prog and "QUEUE_DONE" not in prog and not list(c.glob("*/BLOCK_DONE"))
    if behavior == "simfail":
        assert len(list((c / "discarded").iterdir())) == 2          # attempts 1-2 discarded, attempt 3 ends BLOCKED
    # the whole supervisor must halt BLOCKED, never PIPELINE_COMPLETE
    for s in ("wait_c2", "c2_eval", "prereg", "demo"): (r / "supervisor/stages").mkdir(parents=True, exist_ok=True); (r / f"supervisor/stages/{s}.done").write_text("x")
    (r / "supervisor/demo_success.txt").write_text("True")
    shutil_rm = subprocess.run(["bash", "-c", f"rm -rf {c}"]); assert shutil_rm.returncode == 0
    subprocess.run(["bash", str(tmp_path / "sup.sh")], capture_output=True, text=True, timeout=300)
    status = (r / "supervisor/status.txt").read_text()
    assert "BLOCKED phaseA" in status and "PIPELINE_COMPLETE" not in status and not (r / "supervisor/stages/phaseA.done").exists()


def test_interrupted_block_is_recovered_and_state_restored(tmp_path):
    r = sandbox(tmp_path)
    assert sh(tmp_path, "stage_phaseA").returncode == 0           # first run completes everything (baseline state with touched marks)
    state = r / "c3-phaseA/state/RG2-RANDOMIZED/touched"; before = state.read_text()
    (r / "behavior").write_text("hang")
    for arm in ("fixed", "adaptive"):
        d = r / f"c2-airline-test/4-{arm}/tasks/4"; d.mkdir(parents=True); (d / "official-result.json").write_text("{}")
    # new task block that gets killed mid-run (extra airline task appears)
    
    proc = subprocess.Popen(["bash", "-c", f"source {tmp_path}/funcs.sh; airline_tasks() {{ echo '2 3 4'; }}; stage_phaseA"], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(300):
        if (r / "c3-phaseA/airline:4/BLOCK.json").exists() and "airline 4" in (r / "calls.log").read_text(): break
        time.sleep(0.2)
    else:
        pytest.fail("the block to be interrupted never started")
    os.killpg(proc.pid, signal.SIGKILL); proc.wait()
    out = sh(tmp_path, 'pending "$R/c3-phaseA" airline:2 airline:3 airline:4').stdout
    assert out.split() == ["airline:4"]                               # finished blocks are skipped, the interrupted one is re-queued
    assert state.read_text() == before                                # the killed attempt left no trace in persistent state
    assert list((r / "c3-phaseA/discarded").glob("airline:4-interrupted*"))
    (r / "behavior").write_text("ok")
    assert sh(tmp_path, "airline_tasks() { echo '2 3 4'; }; stage_phaseA").returncode == 0 and (r / "c3-phaseA/airline:4/BLOCK_DONE").exists()


def test_incomplete_c2_cohort_cannot_shrink_the_sample(tmp_path):
    r = sandbox(tmp_path)
    assert sh(tmp_path, "validate_airline_cohort").returncode == 0
    (r / "c2-airline-test/3-adaptive/tasks/3/official-result.json").unlink()          # one missing official result: recorded, not silently dropped
    assert sh(tmp_path, "validate_airline_cohort").returncode == 0
    assert (r / "supervisor/c2_missing_official_results.txt").read_text().split() == ["3-adaptive"]
    subprocess.run(["rm", "-rf", str(r / "c2-airline-test/3-fixed")])                  # a missing task directory changes the cohort: must fail
    assert sh(tmp_path, "validate_airline_cohort").returncode != 0
    assert "2 6 8 13 16 18 19 22 24 25 26 29 30 31 32 35 37 44 45 48" in SUP.read_text()
