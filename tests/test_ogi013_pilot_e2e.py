"""End-to-end simulation of the pilot launcher (no live inference). The REAL run_pilot.sh -> run_arm.sh -> host bootstrap -> ogi013_tau2_run.py -> official tau2 airline task 24 -> FruitStack
(MangoMe, OrangeMe, PeachMe, PlumMe, CherryMe, AppleMe, PomeloMe) with the real pre-dispatch gate, PeachMe governance, PlumMe lease contract, receipts, guard and report. The ONLY substitution is the
provider transport (tests/ogi013_offline_transport/sitecustomize.py replaces plumme.service.default_adapters). MangoMe runs on a scratch COPY of the evaluation database (the evaluation database
itself is only read); the provider environment is stripped and every outbound HTTP proxy points at a dead port, so a patch that silently failed could not reach a provider."""
import hashlib
import json
import os
import shutil
import subprocess
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

from ogi013_pilot_fixtures import PILOT, ROOT

pytest.importorskip("plumme")        # needs the real components in the interpreter that runs pytest (not in the CI replica, which has none)

REAL = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013")


COMPONENTS = Path(os.environ.get("PILOT_COMPONENTS", "/root/fruits/integration/ogi013-org-components"))


def _dirty_components() -> list[str]:
    """Component checkouts the real launcher would resolve (run_arm.sh: PILOT_COMPONENTS) that carry uncommitted changes."""
    if not COMPONENTS.is_dir():
        return []                                                                                  # reported separately as a missing directory, not as dirty
    return [d.name for d in sorted(COMPONENTS.iterdir()) if (d / ".git").exists() and subprocess.run(["git", "-C", str(d), "status", "--porcelain"], capture_output=True, text=True).stdout.strip()]


_DIRTY = _dirty_components()


pytestmark = [pytest.mark.skipif(not (REAL / "env.sh").is_file() or not (REAL / "runs/work.env").is_file() or not (REAL / "benchmarks/tau2-bench").is_dir() or not shutil.which("mongosh"),
                                 reason="needs the ogi-013 evaluation base, the tau2 checkout and a local MongoDB"),
              pytest.mark.skipif(not COMPONENTS.is_dir(), reason=f"PILOT_COMPONENTS directory does not exist: {COMPONENTS}"),
              pytest.mark.skipif(bool(_DIRTY), reason="the host bootstrap refuses a DIRTY_SOURCE component checkout (its logged commit would not identify the code that runs); dirty: " + ", ".join(_DIRTY))]


def _mongosh(js: str) -> str:
    return subprocess.run(["mongosh", "--quiet", "--eval", js], capture_output=True, text=True, timeout=120, check=True).stdout.strip()


@pytest.fixture(scope="module")
def scratch_db():
    """A scratch copy of the evaluation MangoMe database, UNIQUELY OWNED by this fixture invocation (name = pid + random suffix): concurrent or orphaned test processes can never drop, re-copy or read each other's
    database. Reads the source, writes only its own copy, drops only its own copy; the source must come out unchanged. An existing database of that name is refused, never reused."""
    name = f"mangome_ogi013_e2e_{os.getpid()}_{uuid.uuid4().hex[:8]}"
    probe = "JSON.stringify(db.getSiblingDB('mangome_ogi013_eval').getCollectionNames().sort().map(c=>[c,db.getSiblingDB('mangome_ogi013_eval')[c].countDocuments()]))"
    before = _mongosh(probe)
    assert name not in json.loads(_mongosh("JSON.stringify(db.getMongo().getDBNames())")), "scratch database name collision"
    _mongosh("const s=db.getSiblingDB('mangome_ogi013_eval'); s.getCollectionNames().forEach(c=>s[c].aggregate([{$out:{db:'%s',coll:c}}]));" % name)
    try:
        yield name
    finally:
        _mongosh("db.getSiblingDB('%s').dropDatabase()" % name)
    assert _mongosh(probe) == before, "the evaluation database must not be touched by the simulation"


def _world(tmp: Path, db: str, mutate_budget=None):
    base, code, transport = tmp / "base", tmp / "code", tmp / "transport"
    (base / "runs").mkdir(parents=True)
    (base / "benchmarks").mkdir()
    (base / "benchmarks/tau2-bench").symlink_to(REAL / "benchmarks/tau2-bench")
    (base / "env.sh").write_text((REAL / "env.sh").read_text().replace("mangome_ogi013_eval", db).replace(f"D={REAL}", f"D={base}"))
    shutil.copy(REAL / "runs/work.env", base / "runs/work.env")
    if (REAL / "runs/host_budget.env").is_file():
        shutil.copy(REAL / "runs/host_budget.env", base / "runs/host_budget.env")
    for n in ("chat", "project"):
        subprocess.run(["git", "clone", "-q", "--bare", str(REAL / f"slots/D/ledgers/{n}.git"), str(base / f"slots/D/ledgers/{n}.git")], check=True)
    shutil.copytree(ROOT / "runners", code / "runners", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(PILOT, code / "evidence/ogi013-pilot", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "tests/ogi013_offline_transport", transport)
    (code / ".gitignore").write_text("__pycache__/\n")
    budget = code / "evidence/ogi013-pilot/pilot_budget.json"
    if mutate_budget:
        b = json.loads(budget.read_text())
        mutate_budget(b)
        budget.write_text(json.dumps(b, indent=1))
    subprocess.run("git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm sim", shell=True, cwd=code, check=True)
    approval = tmp / "approval.txt"
    approval.write_text(hashlib.sha256(budget.read_bytes()).hexdigest() + "\n")
    log = tmp / "transport.jsonl"
    return SimpleNamespace(base=base, code=code, transport=transport, approval=approval, log=log, runs=base / "runs", pilot=base / "runs/pilot-3")


def _run(w, scenario=None):
    env = {k: v for k, v in os.environ.items() if not any(t in k.upper() for t in ("API_KEY", "FLM_KEY", "TOKEN", "SECRET")) and k not in ("PLUMME_STATE_DIR", "PILOT_APPROVAL", "PILOT_BASE")}
    env.update({"PILOT_BASE": str(w.base), "PILOT_APPROVAL": str(w.approval), "PILOT_OFFLINE_TRANSPORT": str(w.transport), "PILOT_OFFLINE_TRANSPORT_LOG": str(w.log), "PILOT_POLL_S": "1",
                "HTTP_PROXY": "http://127.0.0.1:9", "HTTPS_PROXY": "http://127.0.0.1:9", "ALL_PROXY": "http://127.0.0.1:9", "http_proxy": "http://127.0.0.1:9", "https_proxy": "http://127.0.0.1:9",
                "NO_PROXY": "127.0.0.1,localhost", "PILOT_OFFLINE_SCENARIO": scenario or ""})
    if not scenario:
        env.pop("PILOT_OFFLINE_SCENARIO")
    r = subprocess.run(["bash", str(w.code / "evidence/ogi013-pilot/run_pilot.sh")], env=env, capture_output=True, text=True, timeout=1400)
    return SimpleNamespace(rc=r.returncode, out=r.stdout, err=r.stderr)


def _rows(path):
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()] if Path(path).is_file() else []


def _events(w, arm):
    return _rows(w.pilot / arm / "tasks/24/fruitstack-events.jsonl")


def test_both_arms_run_end_to_end_through_the_real_launcher_with_only_the_transport_substituted(tmp_path, scratch_db):
    w = _world(tmp_path, scratch_db)
    r = _run(w)
    assert r.rc == 0, (r.err[-1500:], r.out[-500:])
    # the transport was the only thing that answered, and it answered both arms
    sent = _rows(w.log)
    assert sent and all(x["provider"].startswith("offline-") for x in sent) and not (w.runs / "PILOT_HALT").exists()
    for arm in ("single", "collab"):
        d = w.pilot / arm
        official = json.loads((d / "tasks/24/official-result.json").read_text())
        assert official["reward_info"] is not None and official["task_id"] == "24"                                  # the official tau2 grader ran
        receipts = _rows(d / "fruitstack/plumme-state/receipts.jsonl")
        assert receipts and all(x["success"] is not None for x in receipts)
        assert {x.get("cost_class") for x in receipts if x.get("cost_class")} <= {"FREE_TIER"}                       # zero cash: only the free class was ever dispatched
        sim = _rows(d / "sim-usage.jsonl")
        assert sim and all(s.get("success") for s in sim if "success" in s)                                           # the simulator went through PlumMe's lease contract (the PILOT-1 failure point)
    single_ev, collab_ev = [e["event"] for e in _events(w, "single")], [e["event"] for e in _events(w, "collab")]
    assert "ORG_COLLAB" not in single_ev and "ORG_COLLAB" in collab_ev                                               # OGI013_ORG_COLLAB=1 is what turned collaboration on, and only in COLLAB
    collab = next(e for e in _events(w, "collab") if e["event"] == "ORG_COLLAB")
    assert collab["action"] == "book_reservation" and collab["independent_review"] is True and collab["changed"] is True and collab["final_reviewed"] is True
    assert {t["lineage"] for t in collab["trail"] if t["stage"] == "CRITIQUE"} and collab["agreement"] and all(a["grounds_stated"] for a in collab["agreement"])
    # the guard, the gate and the report agree with the evidence
    report = json.loads((w.pilot / "report.json").read_text())
    assert report["verdict"]["benchmark_executed_in_both_arms"] is True and report["verdict"]["independent_review_occurred"] is True
    assert report["controls"]["identical"] is True, report["controls"]
    assert report["arms"]["collab"]["resources"]["dispatches"] > report["arms"]["single"]["resources"]["dispatches"]                           # collaboration visibly cost more
    assert report["arms"]["single"]["resources"]["cash_usd_recorded"] == 0.0 and report["arms"]["collab"]["resources"]["cash_usd_recorded"] == 0.0 and report["arms"]["collab"]["resources"]["failed"] == 0
    assert "NOT ESTABLISHED" in (w.pilot / "report.md").read_text()
    assert report["verdict"]["action_changing_intervention_documented"] is True and "statistical_evidence" in report["verdict"]


def test_a_total_provider_rejection_stops_the_pilot_without_a_retry_storm_or_a_collab_arm(tmp_path, scratch_db):
    w = _world(tmp_path, scratch_db)
    r = _run(w, "fail")
    assert r.rc in (3, 5), (r.rc, r.err[-800:])
    assert not (w.pilot / "collab").exists() or r.rc == 3
    assert (w.pilot / "report.md").is_file() and (w.pilot / "single").is_dir()                                       # evidence preserved, report written
    assert len(_rows(w.log)) == 0 or all(x["provider"].startswith("offline-") for x in _rows(w.log))
    assert (w.pilot / "single.log").read_text().count("RuntimeError: SIM_ROUTE_FAILED") == 1
    assert len(_rows(w.pilot / "single/fruitstack/plumme-state/receipts.jsonl")) <= 12                                 # a bounded number of rejected attempts, not a storm


def test_a_paid_only_world_dispatches_nothing_through_the_real_launcher(tmp_path, scratch_db):
    w = _world(tmp_path, scratch_db)
    r = _run(w, "paid")
    assert r.rc in (3, 4, 5), (r.rc, r.err[-800:])
    assert _rows(w.log) == []                                                                                         # no priced route ever reached the transport


def test_the_pre_dispatch_gate_halts_a_real_arm_at_its_cap_and_collab_never_starts(tmp_path, scratch_db):
    def tiny(b):
        b["arms"]["pilot-1/single"]["max_dispatches"] = 3
        b["cumulative"]["max_dispatches"] = 3
    w = _world(tmp_path, scratch_db, mutate_budget=tiny)
    r = _run(w)
    assert r.rc == 3, (r.rc, r.err[-800:])
    assert (w.runs / "PILOT_HALT").is_file() and not (w.pilot / "collab").exists()
    assert len(_rows(w.log)) <= 3 + 1                                                                                 # nothing dispatched beyond the cap
    assert (w.pilot / "report.md").is_file()


def test_the_offline_transport_is_refused_against_the_real_base(tmp_path):
    w = SimpleNamespace()
    env = {**os.environ, "PILOT_OFFLINE_TRANSPORT": str(tmp_path), "PILOT_BASE": str(REAL), "PILOT_APPROVAL": str(tmp_path / "x")}
    r = subprocess.run(["bash", str(PILOT / "run_pilot.sh")], env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 2 and "only allowed with a PILOT_BASE other than the real evaluation base" in r.stderr
    env.pop("PILOT_BASE")
    r = subprocess.run(["bash", str(PILOT / "run_pilot.sh")], env=env, capture_output=True, text=True, timeout=60)
    assert r.returncode == 2 and "only allowed" in r.stderr


def test_a_long_conversation_with_prompts_over_22_kb_runs_to_the_official_grade(tmp_path, scratch_db):
    """pilot-3 stopped at step 10 (BUDGET_HEADROOM_BELOW_MIN_ANSWER) when the prompt passed ~22 KB, because input tokens were bounded by BYTES against the 24,000 per-step ceiling."""
    w = _world(tmp_path, scratch_db)
    r = _run(w, "long")
    assert r.rc == 0, (r.err[-800:], r.out[-300:])
    assert max(x["bytes"] for x in _rows(w.log) if x["stage"] in ("draft", "challenge", "revise")) > 22000      # the old bound would have refused these
    for arm in ("single", "collab"):
        assert json.loads((w.pilot / arm / "tasks/24/official-result.json").read_text())["reward_info"] is not None
        assert "BUDGET_STOP" not in [e["event"] for e in _events(w, arm)]
