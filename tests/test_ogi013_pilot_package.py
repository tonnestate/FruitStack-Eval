"""Pilot package: comparative report (official-result ingestion, verdict separation, identical controls, unknowns), simulator preflight, and the launcher end to end with stubbed arms
(completion, budget halt that preserves evidence, arm failure, interruption, never restarting on its own). No model, no network."""
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

from ogi013_pilot_fixtures import ARMS, BUDGET, PILOT, ROOT, load, receipt, write_arm

report = load("pilot_report", PILOT / "pilot_report.py")
STUB = ROOT / "tests/ogi013_pilot_stub_arm.py"
SIM = BUDGET["simulator_model_key"]


# ---- report -----------------------------------------------------------------------------------------------------------------------------------------------------------

def official(reward, task="24", seed=42, policy="POLICY TEXT", calls=("get_reservation_details", "book_reservation"), termination="user_stop"):
    return {"task_id": task, "seed": seed, "policy": policy, "duration": 100.0, "start_time": "t0", "end_time": "t1", "termination_reason": termination,
            "reward_info": {"reward": reward, "action_checks": [{"action": {"name": c}, "action_match": reward == 1.0} for c in calls]},
            "messages": [{"role": "assistant", "content": "", "tool_calls": [{"name": c, "arguments": {}}]} for c in calls] + [{"role": "assistant", "content": "All done."}]}


def collab_event(improved=True, validated=False, independent=True, unresolved=(), ungrounded=False):
    return {"event": "ORG_COLLAB", "purpose": "consequential_effect", "action": "book_reservation", "draft": "d1", "final": "d2", "changed": improved, "improved": improved, "validated": validated,
            "ungrounded_agreement": ungrounded, "final_reviewed": improved or validated, "independent_review": independent, "review_unavailable": False, "specialist": False, "calls": 3, "stop": "NO_ISSUES",
            "unresolved": list(unresolved), "overruled": [], "agreement": [], "attribution": [], "failures": [],
            "trail": [{"stage": "SOLUTION", "model": "a", "lineage": "L-a", "status": "UNVERIFIED", "text": "draft"}, {"stage": "CRITIQUE", "model": "b", "lineage": "L-b", "status": "DISSENT", "text": "wrong id"},
                      {"stage": "REVISION", "model": "a", "lineage": "L-a", "status": "UNVERIFIED", "text": "fixed"}]}


def make_arm(root, pilot, name, result, events=(), receipts=None, sim_model=SIM, collab_flag="", code="head1", heads=None, interrupted=False, wall=(100.0, 160.0), log="OGI013_SOURCE plumme=aaa"):
    rel = f"pilot-1/{name}"
    rows = receipts if receipts is not None else [receipt() for _ in range(5)]
    write_arm(root, rel, rows, sim_ids=[rows[1]["receipt_id"], rows[3]["receipt_id"]] if len(rows) > 3 else [])
    (root / rel / "sim-usage.jsonl").write_text("".join(json.dumps({"receipt_id": rows[i]["receipt_id"], "success": True, "model_key": sim_model}) + "\n" for i in (1, 3) if len(rows) > 3))
    td = root / rel / "tasks" / "24"
    td.mkdir(parents=True, exist_ok=True)
    if result is not None:
        (td / "official-result.json").write_text(json.dumps(result))
    (td / "fruitstack-events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    if interrupted:
        (td / "RUN_INTERRUPTED.json").write_text("{}")
    pilot.mkdir(parents=True, exist_ok=True)
    (pilot / f"conditions-{name}.json").write_text(json.dumps({"arm": name, "started_at": wall[0], "ended_at": wall[1], "code_head": code, "slot_heads": heads or {"chat": "c1", "project": "p1"},
                                                                 "env": {"OGI013_ORG_COLLAB": collab_flag, "OGI013_ORG_POLICY_MODE": "OFF" if collab_flag else None}}))
    (pilot / f"{name}.log").write_text(log + "\n")


def build(tmp, single_reward=0.0, collab_reward=1.0, collab_events=None, **kw):
    runs, pilot = tmp / "runs", tmp / "runs/pilot-1"
    make_arm(runs, pilot, "single", official(single_reward), **kw.get("single", {}))
    make_arm(runs, pilot, "collab", official(collab_reward), events=collab_events if collab_events is not None else [collab_event(), {"event": "ORG_REVISION", "action_changed": True}],
             **{"collab_flag": "1", **kw.get("collab", {})})
    budget = tmp / "budget.json"
    budget.write_text(json.dumps(BUDGET))
    return report.build_report(runs, pilot, budget), runs, pilot, budget


def test_official_results_are_ingested_and_the_dispatches_counted_once(tmp_path):
    rep, *_ = build(tmp_path)
    s, c = rep["arms"]["single"], rep["arms"]["collab"]
    assert (s["reward"], c["reward"]) == (0.0, 1.0) and s["termination_reason"] == "user_stop" and s["task_id"] == "24" and s["seed"] == 42
    assert [a["name"] for a in c["actions"]] == ["get_reservation_details", "book_reservation"] and c["final_message"] == "All done."
    assert c["action_checks"][0] == {"name": "get_reservation_details", "matched": True} and s["action_checks"][0]["matched"] is False
    assert s["resources"]["dispatches"] == 5 and s["resources"]["simulator_dispatches"] == 2 and s["resources"]["agent_dispatches"] == 3         # the two simulator receipts are not counted twice
    assert s["wall_clock_s"] == 60.0 and s["resources"]["tokens_recorded"] == 5 * 110 and s["resources"]["cash_usd_recorded"] == 0.0


def test_the_verdict_keeps_execution_intervention_improvement_and_statistics_apart(tmp_path):
    rep, *_ = build(tmp_path)
    v = rep["verdict"]
    assert v["benchmark_executed_in_both_arms"] and v["independent_review_occurred"] and v["action_changing_intervention_documented"]
    assert v["improvement_over_single"].startswith("OBSERVED_IN_THIS_PAIR") and v["statistical_evidence"].startswith("NOT ESTABLISHED")
    assert rep["comparison"]["improving_reviews"] == 1 and rep["comparison"]["collaboration_calls"] == 3


def test_a_higher_reward_without_a_documented_intervention_is_not_credited_to_the_collaboration(tmp_path):
    rep, *_ = build(tmp_path, collab_events=[collab_event(improved=False, validated=True)])
    v = rep["verdict"]
    assert not v["action_changing_intervention_documented"] and v["improvement_over_single"].startswith("HIGHER_REWARD_WITHOUT_A_DOCUMENTED_INTERVENTION")
    assert rep["comparison"]["validated_unchanged_reviews"] == 1                                                    # mere agreement is counted as agreement, not improvement


@pytest.mark.parametrize("single,collab,expect", [(1.0, 1.0, "NONE_OBSERVED (equal"), (1.0, 0.0, "NONE_OBSERVED (COLLAB reward is lower)")])
def test_equal_or_lower_collaboration_rewards_are_not_improvements(tmp_path, single, collab, expect):
    rep, *_ = build(tmp_path, single_reward=single, collab_reward=collab)
    assert rep["verdict"]["improvement_over_single"].startswith(expect) and rep["verdict"]["statistical_evidence"].startswith("NOT ESTABLISHED")


def test_an_interrupted_or_stopped_arm_makes_the_comparison_not_assessable(tmp_path):
    rep, *_ = build(tmp_path, collab={"interrupted": True})
    assert not rep["verdict"]["benchmark_executed_in_both_arms"] and rep["verdict"]["improvement_over_single"].startswith("NOT_ASSESSABLE")
    rep2, *_ = build(tmp_path / "b", collab_events=[collab_event(), {"event": "BUDGET_STOP", "source": "collaboration"}])
    assert not rep2["verdict"]["benchmark_executed_in_both_arms"]
    rep3, *_ = build(tmp_path / "c")
    (tmp_path / "c/runs/pilot-1/collab/tasks/24/official-result.json").unlink()
    assert not report.build_report(tmp_path / "c/runs", tmp_path / "c/runs/pilot-1", tmp_path / "c/budget.json")["verdict"]["benchmark_executed_in_both_arms"]


def test_identical_controls_are_verified_from_the_evidence_not_assumed(tmp_path):
    rep, *_ = build(tmp_path)
    assert rep["controls"]["identical"] and all(x["equal"] for x in rep["controls"]["checks"].values())
    for label, kw in {"simulator": {"collab": {"sim_model": "other-model@x"}}, "code": {"collab": {"code": "head2"}}, "ledger": {"collab": {"heads": {"chat": "zz", "project": "p1"}}},
                      "components": {"collab": {"log": "OGI013_SOURCE plumme=bbb"}}}.items():
        rep, *_ = build(tmp_path / label, **kw)
        assert not rep["controls"]["identical"], label
    rep, *_ = build(tmp_path / "flag", single={"collab_flag": "1"})                                                  # the SINGLE arm must not carry the collaboration flag
    assert not rep["controls"]["checks"]["only_intended_difference"]["equal"] and not rep["controls"]["identical"]
    runs = tmp_path / "pol/runs"
    make_arm(runs, runs / "pilot-1", "single", official(0.0))
    make_arm(runs, runs / "pilot-1", "collab", official(1.0, policy="A DIFFERENT POLICY"), events=[collab_event()], collab_flag="1")
    (tmp_path / "pol/budget.json").write_text(json.dumps(BUDGET))
    assert not report.build_report(runs, runs / "pilot-1", tmp_path / "pol/budget.json")["controls"]["checks"]["policy_sha256"]["equal"]


def test_unknown_usage_cash_and_lineage_are_listed_never_silently_zero(tmp_path):
    rows = [receipt(), receipt(usage=False), receipt(lineage=None), receipt(cost_class="NORMAL"), receipt(ok=False, failure="TIMEOUT", usage=False)]
    rep, *_ = build(tmp_path, single={"receipts": rows})
    text = " ".join(rep["unknowns"])
    assert "without recorded usage" in text and "unknown cash exposure" in text and "unknown lineage" in text and "charged at the reserve" in text and "cost_usd not reported" in text
    assert "NOT zero-cash: the cash exposure is NOT bounded" in text and "all zero-cash" in text       # the wording follows the classes: a paid class is never described as bounded


def test_the_markdown_report_carries_the_four_questions_and_the_collaboration_trace(tmp_path):
    rep, runs, pilot, budget = build(tmp_path)
    md = report.render(rep)
    for needle in ("Benchmark executed in both arms", "Independent review occurred", "Improvement over SINGLE", "Statistical evidence", "Controls identical across arms: **True**", "review 1", "wrong id", "Unknown or unproven"):
        assert needle in md
    assert report.main(["x", "report", str(runs), str(pilot), str(budget)]) == 0 and (pilot / "report.json").is_file() and (pilot / "report.md").is_file()


# ---- simulator preflight --------------------------------------------------------------------------------------------------------------------------------------------

def fake_service(eligible_keys, retry_after=None, known=(SIM,)):
    offers = {f"offer-{k}": SimpleNamespace(model_key=k, provider="prov") for k in known}
    scheduler = SimpleNamespace(screen=lambda req: ([o for o in offers.values() if o.model_key in eligible_keys], {}),
                                availability=lambda o: {"retry_after_seconds": retry_after, "circuit_open": False, "credential_available": True, "quota_exhausted": retry_after is not None})
    return SimpleNamespace(store=SimpleNamespace(offers=offers), scheduler=scheduler)


@pytest.fixture
def preflight():
    pytest.importorskip("tau2")
    pytest.importorskip("plumme")
    sys.path.insert(0, str(ROOT / "runners"))
    return load("sim_preflight", PILOT / "sim_preflight.py")


def test_preflight_passes_only_when_plumme_would_run_the_pinned_model_now(preflight):
    assert preflight.check(fake_service({SIM}), SIM)["executable"] is True
    cooling = preflight.check(fake_service(set(), retry_after=120.0), SIM)
    assert cooling["executable"] is False and cooling["retry_after_s"] == 120.0 and cooling["model_known_to_plumme"]
    unknown = preflight.check(fake_service({SIM}, known=("other@x",)), SIM)
    assert unknown["executable"] is False and unknown["model_known_to_plumme"] is False


def test_a_preflight_that_cannot_run_does_not_pass(preflight, tmp_path, capsys):
    assert preflight.main(["x", str(tmp_path / "missing.json"), str(tmp_path / "state")]) == 2 and '"executable": false' in capsys.readouterr().out


# ---- launcher end to end (stubbed arms) ------------------------------------------------------------------------------------------------------------------------------

@pytest.fixture
def launcher(tmp_path):
    """A throw-away checkout (git, clean) holding the real pilot scripts and a stub run_arm.sh, a fake ogi-013 base with a slot-D ledger snapshot, and the owner's approval."""
    code, base = tmp_path / "code", tmp_path / "base"
    pil = code / "evidence/ogi013-pilot"
    pil.mkdir(parents=True)
    for f in ("pilot_guard.py", "pilot_report.py", "pilot_budget.json", "run_pilot.sh"):
        shutil.copy(PILOT / f, pil / f)
    (code / "runners").mkdir()
    for f in ("ogi013_org_collab.py", "ogi013_pilot_gate.py", "ogi013_lineage_heart.py"):
        (code / "runners" / f).write_text("# stub\n")
    (pil / "run_arm.sh").write_text(f'#!/bin/bash\nexec python3 {STUB} "$@"\n')
    (pil / "run_arm.sh").chmod(0o755)
    (pil / "run_pilot.sh").chmod(0o755)
    (code / ".gitignore").write_text("__pycache__/\n")                                  # as in the real repository
    subprocess.run("git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm init", shell=True, cwd=code, check=True)
    work = tmp_path / "ledger-src"
    work.mkdir()
    subprocess.run("git init -q && git -c user.email=t@t -c user.name=t commit -q --allow-empty -m ledger", shell=True, cwd=work, check=True)
    for n in ("chat", "project"):
        subprocess.run(["git", "clone", "-q", "--bare", str(work), str(base / "slots/D/ledgers" / f"{n}.git")], check=True)
    (base / "runs").mkdir(exist_ok=True)
    approval = tmp_path / "approval.txt"
    import hashlib
    approval.write_text(hashlib.sha256((pil / "pilot_budget.json").read_bytes()).hexdigest() + "\n")

    def run(scenario="ok", approve=True, wait=True, **env):
        e = {**os.environ, "PILOT_BASE": str(base), "STUB_SCENARIO": scenario, "PILOT_POLL_S": "0.2", **{k: str(v) for k, v in env.items()}}
        e.pop("PILOT_APPROVAL", None)
        if approve:
            e["PILOT_APPROVAL"] = str(approval)
        p = subprocess.Popen(["bash", str(pil / "run_pilot.sh")], env=e, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
        if not wait:
            return p
        out, err = p.communicate(timeout=120)
        return SimpleNamespace(rc=p.returncode, out=out, err=err)

    return SimpleNamespace(run=run, base=base, runs=base / "runs", pilot=base / "runs/pilot-2", code=code, tmp=tmp_path)


def test_a_complete_matched_pilot_runs_both_arms_with_isolated_state_and_one_difference(launcher):
    r = launcher.run("ok")
    assert r.rc == 0, r.err
    p, env = launcher.pilot, {a: json.loads((launcher.runs / f"pilot-2/{a}/stub-env.json").read_text()) for a in ("single", "collab")}
    assert env["single"]["args"][1:5] == ["24", "airline", "single", "pilot-2-task24"] and env["collab"]["args"][1:5] == ["24", "airline", "rg2", "pilot-2-task24"]      # same task, domain, simulator route
    assert not env["single"]["OGI013_ORG_COLLAB"] and env["collab"]["OGI013_ORG_COLLAB"] == "1" and env["collab"]["OGI013_ORG_POLICY_MODE"] == "OFF"          # the one intended difference
    assert env["single"]["args"][5] != env["collab"]["args"][5] and env["single"]["OGI013_ORG_STATE_DIR"] != env["collab"]["OGI013_ORG_STATE_DIR"]          # isolated ledgers and organisational state
    for a in ("single", "collab"):
        assert (Path(env[a]["args"][5]) / "ledgers/chat.git").is_dir() and env[a]["OGI013_PILOT_ARM"] == f"pilot-2/{a}"
        assert env[a]["PILOT_SESSION_MAX_CALLS"] == str(BUDGET["arms"][f"pilot-1/{a}"]["max_dispatches"]) and env[a]["PILOT_SESSION_MAX_COST_USD"] == "0.0"      # PeachMe ceilings from the budget file
        assert env[a]["OGI013_PILOT_BUDGET"] and env[a]["OGI013_PILOT_ARMS"] == "pilot-2/single,pilot-2/collab"                                               # the pre-dispatch gate is armed for both
    assert json.loads((p / "conditions-single.json").read_text())["slot_heads"] == json.loads((p / "conditions-collab.json").read_text())["slot_heads"]   # identical initial ledger state
    md = (p / "report.md").read_text()
    assert "Controls identical across arms: **True**" in md and "OBSERVED_IN_THIS_PAIR" in md and "NOT ESTABLISHED" in md
    assert (p / "pilot_budget.json").is_file() and (p / "code-head.txt").is_file() and (launcher.runs / "stub-launches.txt").read_text().count("\n") == 2


def test_nothing_starts_without_exact_approval_a_clean_checkout_or_an_executable_simulator(launcher):
    r = launcher.run("ok", approve=False)
    assert r.rc == 2 and "REFUSED" in r.out and not launcher.pilot.exists()
    (launcher.code / "dirty.txt").write_text("x")
    assert launcher.run("ok").rc == 2 and not launcher.pilot.exists()
    (launcher.code / "dirty.txt").unlink()
    r = launcher.run("components_fail")
    assert r.rc == 2 and "refusing rather than installing" in r.err and not launcher.pilot.exists() and not (launcher.runs / "stub-launches.txt").exists()      # non-canonical components: refused, nothing installed or launched
    r = launcher.run("preflight_fail")
    assert r.rc == 4 and "not executable" in r.err and not launcher.pilot.exists() and not (launcher.runs / "stub-launches.txt").exists()      # no arm was ever launched


def test_a_budget_violation_stops_the_arm_preserves_the_evidence_and_the_collab_arm_never_starts(launcher):
    t0 = time.time()
    r = launcher.run("over_budget")
    assert r.rc == 3 and "halted by the budget guard" in r.err and time.time() - t0 < 50          # the guard killed the sleeping arm, it did not wait for it
    halt = json.loads((launcher.runs / "PILOT_HALT").read_text())
    assert halt["by"] == "watch" and any("arm pilot-2/single over its cap" in w for w in halt["why"])
    assert len((launcher.runs / "pilot-2/single/fruitstack/plumme-state/receipts.jsonl").read_text().splitlines()) == 400          # nothing deleted
    assert not (launcher.runs / "pilot-2/collab").exists() and (launcher.pilot / "report.md").is_file()
    assert "NOT_ASSESSABLE" in (launcher.pilot / "report.md").read_text() or "Benchmark executed in both arms: **False**" in (launcher.pilot / "report.md").read_text()


def test_a_failed_arm_keeps_its_evidence_and_nothing_is_retried(launcher):
    r = launcher.run("arm_fail")
    assert r.rc == 5 and "SINGLE arm failed" in r.err and not (launcher.runs / "pilot-2/collab").exists()
    assert (launcher.runs / "stub-launches.txt").read_text().count("\n") == 1                      # launched once, never again
    assert (launcher.runs / "pilot-2/single/fruitstack/plumme-state/receipts.jsonl").is_file()


def test_an_interrupted_pilot_preserves_everything_and_never_restarts_on_its_own(launcher):
    p = launcher.run("hang", wait=False)
    deadline = time.time() + 60
    while time.time() < deadline and not (launcher.runs / "pilot-2/single/fruitstack/plumme-state/receipts.jsonl").exists():
        time.sleep(0.2)
    time.sleep(1.0)
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    out, err = p.communicate(timeout=60)
    assert p.returncode == 130 and "interrupted by TERM" in (launcher.pilot / "INTERRUPTED").read_text()
    assert (launcher.runs / "pilot-2/single/fruitstack/plumme-state/receipts.jsonl").is_file() and (launcher.pilot / "report.md").is_file() and (launcher.pilot / "conditions-single.json").is_file()
    assert json.loads((launcher.pilot / "conditions-single.json").read_text())["exit_code"] == 130
    time.sleep(1.0)
    assert (launcher.runs / "stub-launches.txt").read_text().count("\n") == 1 and not (launcher.runs / "pilot-2/collab").exists()          # nothing relaunched itself
    again = launcher.run("ok")
    assert again.rc == 2 and "already exists" in again.err and (launcher.runs / "stub-launches.txt").read_text().count("\n") == 1             # a second start is refused, not resumed


def test_the_real_arm_launcher_is_the_shared_one_pointed_at_the_pilot_checkout():
    arm = (PILOT / "run_arm.sh").read_text()
    assert "D=${PILOT_CODE:?" in arm and "D=/root" not in arm and "--preflight" in arm and "OGI013_SESSION_MAX_CALLS=${PILOT_SESSION_MAX_CALLS:-" in arm
    assert "ogi013_tau2_run.py" in arm and "--mode $4" in arm and "--llm-user plumme/auto" in arm and "PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH" in arm          # as ogi-013/runs/run_org.sh
    assert "model" not in arm.lower().replace("--mode", "").replace("model_key", "") or "allowlist" not in arm                                                     # no invented model restriction


REAL_BASE = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013")


@pytest.mark.skipif(not (REAL_BASE / "env.sh").is_file() or not (REAL_BASE / "runs/work.env").is_file(), reason="needs the ogi-013 base (env.sh, work.env)")
def test_the_real_arm_launcher_resolves_the_pilot_checkout_after_sourcing_the_shared_env_files():
    """Dry run against the REAL env.sh / work.env: they assign D=<research dir>, which used to redirect the code path (a defect found by this very check). Nothing is executed."""
    def dry(*args, **env):
        e = {**os.environ, "PILOT_DRY_RUN": "1", "PILOT_CODE": str(ROOT), **env}
        r = subprocess.run([str(PILOT / "run_arm.sh"), *args], env=e, capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, r.stderr
        return dict(line.split("=", 1) for line in r.stdout.splitlines() if "=" in line)
    pre = dry("--preflight", "/tmp/r.route", "/tmp/state")
    script = pre["COMMAND"].split("--runner ")[1].split()[0]
    assert script == str(PILOT / "sim_preflight.py") and Path(script).is_file()                       # the preflight script is found inside the pilot checkout
    single = dry("pilot-1/single", "24", "airline", "single", "pilot-1-task24", "/tmp/slot-single", PILOT_SESSION_MAX_CALLS="70", PILOT_SESSION_MAX_TOKENS="100000", PILOT_SESSION_MAX_COST_USD="0.0")
    collab = dry("pilot-1/collab", "24", "airline", "rg2", "pilot-1-task24", "/tmp/slot-collab", PILOT_SESSION_MAX_CALLS="110", PILOT_SESSION_MAX_TOKENS="180000", PILOT_SESSION_MAX_COST_USD="0.0",
                 OGI013_ORG_COLLAB="1", OGI013_ORG_POLICY_MODE="OFF")
    for d, mode, slot in ((single, "single", "slot-single"), (collab, "rg2", "slot-collab")):
        assert d["CODE"] == str(ROOT) and d["PYTHONPATH"].startswith(f"{ROOT}/runners:") and f"--mode {mode} " in d["COMMAND"] and "--task 24 --domain airline" in d["COMMAND"]
        assert "--runner runners/ogi013_tau2_run.py" in d["COMMAND"] and d["ORANGEME_CHAT_REPO"] == f"/tmp/{slot}/ledgers/chat.git" and d["OGI013_SIM_ROUTE_FILE"].endswith("/runs/pilot-1-task24.route")
        assert d["PLUMME_ZERO_CHARGE_DISPATCH"] == "<unset>" and d["PLUMME_TRIAL_CREDIT"] == "<unset>"      # the supply is not narrowed: full eligible PlumMe pool, no invented model restriction
    assert (single["OGI013_SESSION_MAX_CALLS"], single["OGI013_SESSION_MAX_TOKENS"], single["OGI013_SESSION_MAX_COST_USD"]) == ("70", "100000", "0.0")
    assert collab["OGI013_ORG_COLLAB"] == "1" and single["OGI013_ORG_COLLAB"] == "<unset>" and single["COMMAND"].split("--out ")[1] != collab["COMMAND"].split("--out ")[1]


def test_components_must_resolve_from_the_canonical_checkouts_or_the_pilot_refuses(tmp_path):
    vc = load("verify_components", PILOT / "verify_components.py")
    root, tau2 = tmp_path / "components", tmp_path / "tau2"
    for repo in vc.COMPONENTS.values():
        (root / repo).mkdir(parents=True)
    tau2.mkdir()
    r = vc.resolve("json", root / "MangoMe")                                                      # a stdlib module is not inside the canonical checkout: the bootstrap would reinstall
    assert not r["canonical"] and r["origin"]
    assert vc.resolve("definitely_not_installed_xyz", root / "MangoMe") == {"module": "definitely_not_installed_xyz", "origin": None, "canonical": False}
    assert vc.main(["x", str(root), str(tau2)]) == 1                                                # nothing canonical here -> exit 1, nothing is installed by the check
    assert vc.main(["x"]) == 2


@pytest.mark.skipif(not (REAL_BASE / "env.sh").is_file(), reason="needs the ogi-013 base")
def test_with_the_real_environment_every_component_resolves_from_the_canonical_checkouts():
    """Real env files + real hostpython: the pilot's PYTHONPATH makes all seven components and tau2 canonical, so the bootstrap installs NOTHING into the shared host venv."""
    comp = Path("/root/fruits/integration/ogi013-org-components")
    if not comp.is_dir():
        pytest.skip("components root missing")
    r = subprocess.run([str(PILOT / "run_arm.sh"), "--verify-components"], env={**os.environ, "PILOT_CODE": str(ROOT)}, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stdout[-400:] + r.stderr[-400:]
    out = json.loads(r.stdout.strip().splitlines()[-1])
    assert out["all_canonical"] and {m["module"] for m in out["modules"]} >= {"mangome", "orangeme", "peachme", "pomelome", "plumme", "cherryme", "appleme", "tau2"}
    script = (PILOT / "run_pilot.sh").read_text()
    assert script.index("--verify-components") < script.index("--preflight")                         # refused before anything is created


def test_the_report_states_what_one_paired_episode_cannot_separate(tmp_path):
    rep, *_ = build(tmp_path)
    text = " ".join(rep["caveats"])
    assert "n = 1" in text and "customer simulator is an LLM" in text and "Fixed arm order" in text and "no effect size" in text
    assert "Why this is a pilot and not evidence" in report.render(rep)
    rep2, *_ = build(tmp_path / "x", collab_events=[], collab={"code": "other"})
    assert any("controls check FAILED" in c for c in rep2["caveats"]) and any("tested nothing about the collaboration" in c for c in rep2["caveats"])


def test_the_budget_file_carries_exactly_the_owner_stated_limits():
    c = BUDGET["cumulative"]
    assert (c["max_dispatches"], c["max_tokens"], c["max_wall_minutes"], c["max_cash_usd"], BUDGET["max_tokens_per_step"]) == (180, 280000, 90, 0.0, 24000)
    assert sum(a["max_dispatches"] for a in BUDGET["arms"].values()) == c["max_dispatches"] and set(BUDGET["arms"]) == {"pilot-1/single", "pilot-1/collab"}
    assert all(a["max_tokens"] <= c["max_tokens"] and BUDGET["max_tokens_per_step"] <= a["max_tokens"] for a in BUDGET["arms"].values())
    assert BUDGET["status"].startswith("PROPOSAL") and BUDGET["reserve_tokens_per_dispatch"] == 4000 and BUDGET["max_consecutive_failures"] == 20


# ---- lease contract, pilot identity (found by the first live attempt, pilot-1) ---------------------------------------------------------------------------------------

def test_the_launcher_refuses_before_any_arm_when_the_lease_contract_check_fails(launcher):
    r = launcher.run("contract_fail")
    assert r.rc == 2 and "lease-contract check failed" in r.err and not (launcher.runs / "stub-launches.txt").exists() and not launcher.pilot.exists()


def test_a_new_pilot_id_never_touches_the_failed_attempt_and_pilot_1_is_never_reused(launcher):
    old = launcher.runs / "pilot-1"
    (old / "single").mkdir(parents=True)
    (old / "single.log").write_text("SIM_ROUTE_FAILED:AuthorityDenied\n")
    before = {str(p.relative_to(old)): p.read_bytes() for p in old.rglob("*") if p.is_file()}
    assert launcher.run("ok").rc == 0 and launcher.pilot.is_dir()                                       # default id is pilot-2
    assert {str(p.relative_to(old)): p.read_bytes() for p in old.rglob("*") if p.is_file()} == before     # the failed attempt is byte-identical
    refused = launcher.run("ok", PILOT_ID="pilot-1")
    assert refused.rc == 2 and "never reused" in refused.err


def test_a_later_pilot_id_runs_under_the_same_approved_budget_hash():
    guard = load("pilot_guard", PILOT / "pilot_guard.py")
    budget = json.loads((PILOT / "pilot_budget.json").read_text())
    assert guard.arm_cap(budget, "pilot-2/single") == budget["arms"]["pilot-1/single"] and guard.arm_cap(budget, "pilot-2/collab") == budget["arms"]["pilot-1/collab"]
    assert guard.arm_cap(budget, "pilot-2/other") is None and guard.arm_cap({"arms": {"a/single": {}, "b/single": {}}}, "c/single") is None          # no cap, or an ambiguous one: fail closed
    assert guard.session_env(budget, "pilot-2/collab")["OGI013_SESSION_MAX_CALLS"] == "110"


def test_the_lease_contract_check_passes_for_every_zero_cash_class_and_catches_a_widened_execution(preflight, monkeypatch):
    import ogi013_sim_supply as sim
    ok = preflight.contract_check(str(PILOT / "pilot_budget.json"), str(PILOT / "pilot_guard.py"))
    assert ok["ok"] and {c["path"] for c in ok["cases"]} == {"simulator", "agent"} and len(ok["cases"]) == 2 * len(preflight.ZERO_CASH_CLASSES)

    original = sim.PlumMeProvider.execute

    async def widened(self, **kw):                  # the PILOT-1 defect: an execution without the cash cap of its zero-cash lease
        kw["max_cost_usd"] = None
        return await original(self, **kw)
    monkeypatch.setattr(sim.PlumMeProvider, "execute", widened)
    bad = preflight.contract_check(str(PILOT / "pilot_budget.json"), str(PILOT / "pilot_guard.py"))
    assert not bad["ok"] and all("AuthorityDenied" in c["detail"] for c in bad["cases"] if c["path"] == "simulator") and all(not c["ok"] for c in bad["cases"] if c["path"] == "simulator")


def test_the_contract_check_does_not_leak_its_pilot_environment(preflight, monkeypatch):
    monkeypatch.delenv("OGI013_PILOT_BUDGET", raising=False)
    preflight.contract_check(str(PILOT / "pilot_budget.json"), str(PILOT / "pilot_guard.py"))
    assert "OGI013_PILOT_BUDGET" not in os.environ and "OGI013_PILOT_RUNS" not in os.environ
