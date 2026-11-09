"""T on the REAL PeachMe research path (fs_org_driver.peach_host -> peachme.research.run_research -> PeachMe WorkerPool -> PlumMe scheduler), offline: a scripted
PlumMe ProviderAdapter with three distinct lineages (fs_runtime.fixture_service), no provider call. Checks that every model call is metered with the PlumMe identity and
the settled PeachMe step tokens, that the row validates against a declared roster, and that the component switches reach the real path."""
import pytest

pytest.importorskip("peachme.research")
pytest.importorskip("mangome.work_control")

from runners.fs_org_driver import TEAM_COMPONENTS, Task, peach_host, run_team  # noqa: E402
from runners.fs_runtime import fixture_service  # noqa: E402
from runners.ogi013_learning_hook import LearningHook  # noqa: E402
from runners.ogi013_org_discoveries import Ledger  # noqa: E402


def sig(text):
    return (text or "").rsplit("ANSWER:", 1)[-1].strip() or None if "ANSWER:" in (text or "") else None


@pytest.fixture
def host(tmp_path, monkeypatch):
    monkeypatch.setenv("PLUMME_SELECTION_SPREAD", "0")
    svc = fixture_service(tmp_path / "plumme", {"answer": "math.isqrt"})
    return peach_host(svc, tmp_path / "episodes", worker_budget={"max_calls": 20, "max_tokens": 100000, "max_cost_usd": 0.0})


def run(host, tmp_path, comps=TEAM_COMPONENTS, roster=None):
    t = Task("isqrt", "Which Python call computes an exact integer square root? Final line: ANSWER: <call>", sig, lambda a: float(a == "math.isqrt"), "executed")
    hook = LearningHook(Ledger(tmp_path / "ledger.jsonl"), run_id="r1", apply=True, task="isqrt")
    first = run_team(t, hook=hook, roster=roster or {}, components=comps, research=host, n_solvers=2, max_rounds=1)
    return first


def test_t_runs_run_research_and_meters_every_call(host, tmp_path):
    row = run(host, tmp_path)
    assert row["infra_error"] is None and row["path"] == "peachme.research.run_research"
    assert row["answer"] == "math.isqrt"
    assert row["calls"] > 0 and all(r["independence_key"] for r in row["receipts"] if r["ok"])
    assert row["tokens"]["calls_without_tokens"] == 0 and row["tokens"]["input"] > 0
    assert len(row["lineages"]) == 2                                  # two distinct solver lineages from PlumMe
    roster = {r["model_key"]: r["independence_key"] for r in row["receipts"] if r["ok"]}
    again = run(host, tmp_path, roster=roster)
    assert again["identity_valid"], again.get("identity_reason")
    kinds = {e["type"] for e in row["events"]}
    assert {"PEACHME:RESEARCH_STARTED", "PEACHME:BROTHER_MODE", "PEACHME:COGNITIVE_DIAGNOSIS", "PEACHME:RESEARCH_FINALIZED"} <= kinds


def test_component_switches_reach_the_real_path(host, tmp_path):
    full = run(host, tmp_path)
    assert full["stages"].get("lsd", 0) > 0                          # the switch is meaningful only because LSD is active in full T
    no_apple = run(host, tmp_path, comps=TEAM_COMPONENTS - {"appleme"})
    assert no_apple["arm"] == "T-appleme" and "PEACHME:COGNITIVE_DIAGNOSIS" not in {e["type"] for e in no_apple["events"]}
    no_lsd = run(host, tmp_path, comps=TEAM_COMPONENTS - {"lsd"})
    assert not [r for r in no_lsd["receipts"] if r["stage"].startswith("lsd")]
    with pytest.raises(ValueError, match="research_tree"):
        run(host, tmp_path, comps=TEAM_COMPONENTS - {"research_tree"})


def test_controls_use_the_same_peachme_worker_and_a_pin_holds(host, tmp_path):
    from runners.fs_org_driver import run_samples
    t = Task("isqrt", "Which Python call computes an exact integer square root? Final line: ANSWER: <call>", sig, lambda a: float(a == "math.isqrt"), "executed")
    work, _ev = host.worker(t)
    probe = work("q", "solve")
    member = {probe["model_key"]: probe["independence_key"]}
    work2, _ = host.worker(t)
    row = run_samples(t, work=work2, arm="R_mono", roster=member, cycle=list(member), k=3)
    assert {r["independence_key"] for r in row["receipts"]} == set(member.values())
    assert row["identity_valid"], row.get("identity_reason")
    assert probe.get("decision_id") and probe["output_tokens"] is not None
