"""Dry-run and guard tests for the OGI-013 c3 block queue. No launcher, no provider, no real run."""
import json
import os
import pathlib
import subprocess

import pytest

QDIR = pathlib.Path(__file__).resolve().parents[1] / "evidence" / "ogi013-c3-prereg" / "queue"
BLOCK = QDIR / "block_queue.sh"
COND = QDIR / "run_condition.sh"
ALL = "SINGLE SINGLE-E FIXED RG2-OFF RG2-OFF-NOPERSIST RG2-NO-TRIAGE RG2-NO-VERIFY RG2-NO-KNOWLEDGE RG2-LEARNED RG2-RANDOMIZED"
GOOD = {"OGI013_SINGLE_E_K": "3", "OGI013_ORG_LEARNED_DIR": "/nonexistent-learned", "OGI013_ORG_LEARNED_AUTHORIZED": "1"}
FORBIDDEN = ("run1.sh", "queue.sh", "c2-")
BASE = {k: v for k, v in os.environ.items()
        if not k.startswith(("OGI013_", "PLUMME_")) and k not in ("DRY_RUN", "LAUNCHER", "RUNS_DIR", "CONDITIONS")}
CAMP = "c3-test"


def block(runs, args, conds=ALL, dry=True, extra=None):
    env = dict(BASE, RUNS_DIR=str(runs), CONDITIONS=conds)
    if dry:
        env["DRY_RUN"] = "1"
    env.update(extra or {})
    return subprocess.run(["bash", str(BLOCK), *args], env=env, capture_output=True, text=True, timeout=120)


def cond(runs, args, extra=None):
    env = dict(BASE, RUNS_DIR=str(runs), DRY_RUN="1")
    env.update(extra or {})
    return subprocess.run(["bash", str(COND), *args], env=env, capture_output=True, text=True, timeout=60)


def env_of(runs, task, condition):
    text = (runs / CAMP / task / f"{condition}.log").read_text()
    return dict(line[4:].split("=", 1) for line in text.splitlines() if line.startswith("ENV "))


def order_of(runs, task):
    return json.loads((runs / CAMP / task / "BLOCK.json").read_text())["condition_order"]


def test_order_is_reproducible_permutation(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    for d in (a, b):
        d.mkdir()
        assert block(d, [CAMP, "airline", "A", "1013", "t1"], extra=GOOD).returncode == 0
    assert order_of(a, "t1") == order_of(b, "t1")
    assert sorted(order_of(a, "t1")) == sorted(ALL.split())


def test_different_task_gives_different_order(tmp_path):
    block(tmp_path, [CAMP, "airline", "A", "1013", "t1", "t2"], extra=GOOD)
    assert order_of(tmp_path, "t1") != order_of(tmp_path, "t2")


def test_one_route_file_per_task(tmp_path):
    block(tmp_path, [CAMP, "airline", "A", "1013", "t1", "t2"], extra=GOOD)
    routes = {}
    for t in ("t1", "t2"):
        vals = {env_of(tmp_path, t, c)["OGI013_SIM_ROUTE_FILE"] for c in ALL.split()}
        assert len(vals) == 1, (t, vals)
        routes[t] = vals.pop()
    assert routes["t1"] != routes["t2"]
    assert routes["t1"].endswith(f"{CAMP}-t1.route")


def test_state_dirs_shared_for_rg2_off_fresh_for_noPersist(tmp_path):
    block(tmp_path, [CAMP, "airline", "A", "1013", "t1", "t2"], conds="RG2-OFF RG2-OFF-NOPERSIST", extra=GOOD)
    s = lambda t, c: env_of(tmp_path, t, c)["OGI013_ORG_STATE_DIR"]
    assert s("t1", "RG2-OFF") == s("t2", "RG2-OFF")
    assert s("t1", "RG2-OFF-NOPERSIST") != s("t2", "RG2-OFF-NOPERSIST")
    assert s("t1", "RG2-OFF") != s("t1", "RG2-OFF-NOPERSIST")


def test_learned_requires_authorization(tmp_path):
    args = [CAMP, "t1", "airline", "RG2-LEARNED", "A"]
    assert cond(tmp_path, args).returncode == 2
    assert cond(tmp_path, args, {"OGI013_ORG_LEARNED_DIR": "/x"}).returncode == 2
    assert cond(tmp_path, args, {"OGI013_ORG_LEARNED_DIR": "/x", "OGI013_ORG_LEARNED_AUTHORIZED": "1"}).returncode == 0


def test_single_e_requires_k(tmp_path):
    args = [CAMP, "t1", "airline", "SINGLE-E", "A"]
    assert cond(tmp_path, args).returncode == 2
    assert cond(tmp_path, args, {"OGI013_SINGLE_E_K": "3"}).returncode == 0


def test_brother_condition_activates_controller_and_clears_inherited_flag(tmp_path):
    args = [CAMP, "task", "airline", "BROTHER", "A"]
    result = cond(tmp_path, args, {"OGI013_ORG_COLLAB": "1"})
    assert result.returncode == 0, result.stderr
    assert "ENV OGI013_ORG_COLLAB=1" in result.stdout
    assert "ENV OGI013_ORG_POLICY_MODE=OFF" in result.stdout
    assert "CMD " in result.stdout and "c3-test/task/BROTHER task airline rg2" in result.stdout
    assert "OGI013_ORG_COLLAB" in next(line for line in result.stdout.splitlines() if line.startswith("UNSET "))


def test_non_brother_condition_clears_inherited_collaboration_flag(tmp_path):
    result = cond(tmp_path, [CAMP, "task", "airline", "SINGLE", "A"], {"OGI013_ORG_COLLAB": "1"})
    assert result.returncode == 0
    assert "OGI013_ORG_COLLAB" in next(line for line in result.stdout.splitlines() if line.startswith("UNSET "))
    assert "ENV OGI013_ORG_COLLAB=1" not in result.stdout


def test_brother_flag_reaches_the_live_queue_launcher_without_provider_calls(tmp_path):
    launcher = tmp_path / "launcher.sh"
    launcher.write_text(
        '#!/bin/bash\n'
        'printf "%s|%s|%s\\n" "$2" "$4" "${OGI013_ORG_COLLAB:-unset}" >> "$RUNS_DIR/launcher-env.txt"\n'
        'mkdir -p "$RUNS_DIR/$1/tasks/$2"\n'
        'echo \'{"reward_info":null}\' > "$RUNS_DIR/$1/tasks/$2/official-result.json"\n'
    )
    launcher.chmod(0o755)
    env = dict(BASE, RUNS_DIR=str(tmp_path), CONDITIONS="BROTHER", LAUNCHER=str(launcher), OGI013_ORG_COLLAB="1")
    result = subprocess.run(
        ["bash", str(BLOCK), CAMP, "airline", "A", "1013", "task1"],
        env=env, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "launcher-env.txt").read_text().strip() == "task1|rg2|1"
    assert (tmp_path / CAMP / "task1" / "BLOCK_DONE").is_file()


def test_research_arms_share_one_offline_queue_block(tmp_path):
    launcher = tmp_path / "launcher.sh"
    launcher.write_text(
        '#!/bin/bash\n'
        'condition="${1##*/}"\n'
        'printf "%s|%s|%s|%s|%s|%s|%s\\n" "$condition" "$2" "$4" "${OGI013_ORG_COLLAB:-unset}" '
        '"${OGI013_SINGLE_E_K:-unset}" "${OGI013_ORG_POLICY_MODE:-unset}" "${OGI013_ORG_STATE_DIR:-unset}" >> "$RUNS_DIR/arms.txt"\n'
        'mkdir -p "$RUNS_DIR/$1/tasks/$2"\n'
        'echo \'{"reward_info":null}\' > "$RUNS_DIR/$1/tasks/$2/official-result.json"\n'
    )
    launcher.chmod(0o755)
    conditions = "SINGLE SINGLE-E FIXED BROTHER"
    env = dict(BASE, RUNS_DIR=str(tmp_path), CONDITIONS=conditions, LAUNCHER=str(launcher),
               OGI013_SINGLE_E_K="3", OGI013_ORG_COLLAB="1")

    result = subprocess.run(
        ["bash", str(BLOCK), CAMP, "airline", "A", "1013", "task1", "task2"],
        env=env, capture_output=True, text=True, timeout=60,
    )

    assert result.returncode == 0, result.stderr
    records = {
        (row[1], row[0]): row
        for line in (tmp_path / "arms.txt").read_text().splitlines()
        for row in [line.split("|")]
    }
    assert len(records) == 8
    assert {condition: records[("task1", condition)][2] for condition in conditions.split()} == {
        "SINGLE": "single", "SINGLE-E": "single_e", "FIXED": "fixed", "BROTHER": "rg2"
    }
    for task in ("task1", "task2"):
        assert records[(task, "SINGLE")][3:6] == ["unset", "unset", "unset"]
        assert records[(task, "SINGLE-E")][3:6] == ["unset", "3", "unset"]
        assert records[(task, "FIXED")][3:6] == ["unset", "unset", "unset"]
        assert records[(task, "BROTHER")][3:6] == ["1", "unset", "OFF"]
        block_dir = tmp_path / CAMP / task
        assert (block_dir / "BLOCK_DONE").is_file()
        for condition in conditions.split():
            assert json.loads((block_dir / condition / "tasks" / task / "official-result.json").read_text()) == {"reward_info": None}
    brother_state = records[("task1", "BROTHER")][6]
    assert brother_state == records[("task2", "BROTHER")][6]
    assert brother_state == str(tmp_path / CAMP / "state" / "BROTHER")
    progress = (tmp_path / CAMP / "progress.txt").read_text()
    assert all(f"{task} {condition} attempt=1 exit=0" in progress for task in ("task1", "task2") for condition in conditions.split())
    assert "QUEUE_DONE" in progress


def test_no_forbidden_references(tmp_path):
    block(tmp_path, [CAMP, "airline", "A", "1013", "t1", "t2"], extra=GOOD)
    for p in tmp_path.rglob("*"):
        if p.is_file():
            text = p.read_text(errors="ignore")
            for f in FORBIDDEN:
                assert f not in text, (p, f)


def test_discarded_and_retried_on_route_failure(tmp_path):
    fake = tmp_path / "fake_launcher.sh"
    fake.write_text('#!/bin/bash\n'
                    'n=$(cat "$FAKE_COUNT" 2>/dev/null || echo 0); n=$((n+1)); echo $n > "$FAKE_COUNT"\n'
                    'mkdir -p "$RUNS_DIR/$1/tasks/$2"; echo \'{"reward_info":null}\' > "$RUNS_DIR/$1/tasks/$2/official-result.json"\n'
                    '[ "$n" -eq 1 ] && echo SIM_ROUTE_FAILED\nexit 0\n')
    fake.chmod(0o755)
    env = dict(BASE, RUNS_DIR=str(tmp_path), CONDITIONS="FIXED", LAUNCHER=str(fake),
               FAKE_COUNT=str(tmp_path / "count"))
    r = subprocess.run(["bash", str(BLOCK), CAMP, "airline", "A", "1013", "t1"],
                       env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    camp = tmp_path / CAMP
    assert (camp / "discarded" / "t1-attempt1").is_dir()
    assert json.loads((camp / "t1" / "BLOCK.json").read_text())["attempt"] == 2
    assert "discarded attempt=1" in (camp / "progress.txt").read_text()
    assert (tmp_path / "count").read_text().strip() == "2"


def test_discarded_block_restores_persistent_state_and_live_run_needs_explicit_runs_dir(tmp_path):
    """The persistent state of a discarded block must be rolled back (no contamination of the persistence/learning arms); a live call without RUNS_DIR is refused."""
    import os, subprocess, textwrap
    here = pathlib.Path(__file__).resolve().parents[1] / "evidence" / "ogi013-c3-prereg" / "queue"
    runs = tmp_path / "runs"; runs.mkdir()
    fake = tmp_path / "launcher.sh"
    fake.write_text(textwrap.dedent('''\
        #!/bin/bash
        # args: OUTDIR TASK DOMAIN MODE PAIRROUTE SLOT ; writes into the persistent arm state, and fails the simulator on attempt 1 only
        echo "$@" >> "$RUNS_DIR/launch.log"
        mkdir -p "$OGI013_ORG_STATE_DIR" && echo "written-by-$2" >> "$OGI013_ORG_STATE_DIR/marker"
        echo '{"model_key":"sim-x@default"}' > "$OGI013_SIM_ROUTE_FILE"
        mkdir -p "$RUNS_DIR/$1/tasks/$2"
        echo '{"reward_info":null}' > "$RUNS_DIR/$1/tasks/$2/official-result.json"
        if [ ! -f "$RUNS_DIR/second-attempt" ]; then touch "$RUNS_DIR/second-attempt"; echo SIM_ROUTE_FAILED; fi
        '''))
    fake.chmod(0o755)
    env = {**os.environ, "RUNS_DIR": str(runs), "CONDITIONS": "RG2-OFF", "LAUNCHER": str(fake)}
    r = subprocess.run(["bash", str(here / "block_queue.sh"), "c3-test", "retail", "A", "7", "t1"], env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    marker = runs / "c3-test" / "state" / "RG2-OFF" / "marker"
    # attempt 1 was discarded and its state write rolled back; only the kept attempt's write remains
    assert marker.read_text().count("written-by-t1") == 1
    assert (runs / "c3-test" / "discarded" / "t1-attempt1").is_dir()
    assert json.loads((runs / "c3-test" / "t1" / "BLOCK.json").read_text())["sim_model_key"] == "sim-x@default"
    env2 = {k: v for k, v in env.items() if k != "RUNS_DIR"}
    r2 = subprocess.run(["bash", str(here / "block_queue.sh"), "c3-test2", "retail", "A", "7", "t1"], env=env2, capture_output=True, text=True, timeout=60)
    assert r2.returncode == 2


def test_nonzero_launcher_blocks_without_false_queue_done(tmp_path):
    fake = tmp_path / "fail.sh"
    fake.write_text("#!/bin/sh\nexit 7\n")
    fake.chmod(0o755)
    env = dict(BASE, RUNS_DIR=str(tmp_path), CONDITIONS="FIXED", LAUNCHER=str(fake))
    r = subprocess.run(["bash", str(BLOCK), CAMP, "retail", "A", "1013", "task1"],
                       env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode != 0
    progress = (tmp_path / CAMP / "progress.txt").read_text()
    assert "EXECUTION_FAILED" in progress
    assert "QUEUE_DONE" not in progress
    assert not (tmp_path / CAMP / "task1" / "BLOCK_DONE").exists()


def test_success_exit_without_official_result_is_not_complete(tmp_path):
    fake = tmp_path / "empty.sh"
    fake.write_text("#!/bin/sh\nexit 0\n")
    fake.chmod(0o755)
    env = dict(BASE, RUNS_DIR=str(tmp_path), CONDITIONS="FIXED", LAUNCHER=str(fake))
    r = subprocess.run(["bash", str(BLOCK), CAMP, "retail", "A", "1013", "task1"],
                       env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode != 0
    assert "MISSING_OR_INVALID_OFFICIAL_RESULT" in (tmp_path / CAMP / "progress.txt").read_text()
    assert not (tmp_path / CAMP / "task1" / "BLOCK_DONE").exists()


def test_mixed_domain_keys_preserve_canonical_runner_task_id(tmp_path):
    r = cond(tmp_path, [CAMP, "airline:25", "mixed", "RG2-RANDOMIZED", "D"])
    assert r.returncode == 0, r.stderr
    assert "CMD " in r.stdout
    assert "airline:25/RG2-RANDOMIZED 25 airline rg2" in r.stdout
    assert "/airline:25" in r.stdout
    bad = cond(tmp_path, [CAMP, "25", "mixed", "RG2-RANDOMIZED", "D"])
    assert bad.returncode == 2


def test_third_simulator_failure_marks_task_incomplete_and_the_queue_continues(tmp_path):
    """Registered maximum = 3 attempts per task: the 3rd simulator-route failure makes the task INFRA_INCOMPLETE (never retried further), the other tasks still run."""
    fake = tmp_path / "sim.sh"
    fake.write_text('#!/bin/bash\nif [ "$2" = bad ]; then echo SIM_ROUTE_FAILED; exit 1; fi\nmkdir -p "$RUNS_DIR/$1/tasks/$2"\necho \'{"reward_info":{"reward":1.0}}\' > "$RUNS_DIR/$1/tasks/$2/official-result.json"\n')
    fake.chmod(0o755)
    env = dict(BASE, RUNS_DIR=str(tmp_path), CONDITIONS="FIXED", LAUNCHER=str(fake))
    r = subprocess.run(["bash", str(BLOCK), CAMP, "retail", "A", "1013", "bad", "good"], env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    prog = (tmp_path / CAMP / "progress.txt").read_text()
    assert prog.count("discarded attempt=") == 3 and "bad INFRA_INCOMPLETE attempts=3" in prog
    assert (tmp_path / CAMP / "discarded" / "bad-INFRA_INCOMPLETE.txt").is_file()
    assert (tmp_path / CAMP / "good" / "BLOCK_DONE").is_file() and not (tmp_path / CAMP / "bad" / "BLOCK_DONE").exists()
    assert "QUEUE_INCOMPLETE" in prog and "QUEUE_DONE" not in prog
    r2 = subprocess.run(["bash", str(BLOCK), CAMP, "retail", "A", "1013", "bad"], env=env, capture_output=True, text=True, timeout=60)   # a rerun must not start a 4th attempt
    assert r2.returncode == 0 and (tmp_path / CAMP / "progress.txt").read_text().count("discarded attempt=") == 3
