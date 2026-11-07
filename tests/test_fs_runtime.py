"""FruitStack host entrypoint (runners/fs_runtime.py): executed checks, the success contract, operational supply shortage, and one offline-fixture run end to end.
No provider or model call: offline-fixture uses the public PlumMe adapter interface, operational uses an injected PlumMe service without adapters."""
from pathlib import Path

import pytest

import fs_runtime as fr

CONFIG = Path(__file__).resolve().parents[1] / "config" / "fs_runtime" / "offline_fixture.toml"
ENV = ("ORANGEME_HOME", "ORANGEME_CHAT_REPO", "ORANGEME_PROJECT_REPO", "ORANGEME_ALLOW_LOCAL_LEDGER", "ORANGEME_NO_PUSH", "ORANGEME_AGENT_ID", "ORANGEME_ADMIN_IDS",
       "ORANGEME_SOURCE_REPO", "PHYSALIS_DATA_DIR", "PHYSALIS_STATE_DIR", "PLUMME_STATE_DIR")


@pytest.fixture
def env(monkeypatch, tmp_path):
    for k in ENV:                                   # registered with monkeypatch so the run's environment changes are undone
        monkeypatch.setenv(k, "")
    monkeypatch.setenv("MANGOME_BACKEND", "memory")
    monkeypatch.setenv("PLUMME_STATE_DIR", str(tmp_path / "plumme-state"))


def test_executed_checks_run_the_candidate():
    assert fr.exact_isqrt("math.isqrt")["relation"] == "SUPPORTS"
    assert fr.exact_isqrt("math.isqrt()")["relation"] == "SUPPORTS"
    assert fr.exact_isqrt("math.sqrt")["relation"] == "CONTRADICTS"            # float, inexact for large n
    assert fr.exact_comb("math.comb")["relation"] == "SUPPORTS"
    assert fr.exact_comb("math.perm")["relation"] == "CONTRADICTS"
    for unsafe in ("os.system", "__import__", "math.__class__", ""):
        assert fr.exact_isqrt(unsafe)["relation"] == "CONTRADICTS"           # only callables of the math module are ever executed


def _record(state="UNRESOLVED", drop=(), extra=()):
    events = [{"type": t} for t in fr.REQUIRED_EVENTS + ("TOOL_EVIDENCE", "CANDIDATE_VERIFIED", "RESEARCH_STEP") if t not in drop] + [{"type": t} for t in extra]
    for e in events:
        if e["type"] == "STATE_RETURNED":
            e["mangome"] = {"checkpoint_id": "CP-1"}
    return {"state": state, "events": events}


def test_unresolved_is_a_valid_integration_path_but_never_success():
    c = fr.success_contract(_record("UNRESOLVED"), analyses=1, check=True, receipts=1)
    assert c["integration_path_ok"] and not c["mission_success"]
    assert fr.success_contract(_record("COMPLETED"), analyses=1, check=True, receipts=1)["mission_success"]


@pytest.mark.parametrize("record,receipts,problem", [
    (_record(drop=("STATE_RETURNED",)), 1, "missing:STATE_RETURNED"),
    (_record(drop=("CANDIDATE_VERIFIED",)), 1, "missing:CANDIDATE_VERIFIED"),
    (_record(extra=("RESEARCH_STEP_FAILED",)), 1, "failed:RESEARCH_STEP_FAILED"),
    (_record(), 0, "tool_receipts:0<1"),
    (_record("ERROR"), 1, "state:ERROR"),
])
def test_a_broken_integration_path_is_never_converted_into_success(record, receipts, problem):
    c = fr.success_contract(record, analyses=1, check=True, receipts=receipts)
    assert not c["integration_path_ok"] and problem in c["integration_problems"]


def test_operational_without_supply_reports_the_shortage_and_starts_no_mission(env, tmp_path):
    from plumme.config import Settings
    from plumme.service import PlumMeService

    def no_supply():
        svc = PlumMeService(Settings.load(), adapters=[])
        import asyncio
        asyncio.run(svc.discover())
        return svc
    summary = fr.run(fr.load_config(CONFIG), tmp_path / "out", "operational", service_factory=no_supply)
    assert [m["state"] for m in summary["missions"]] == ["NOT_STARTED", "NOT_STARTED"]
    assert all(m["error_code"] == "SUPPLY_UNAVAILABLE" and "work_ref" not in m for m in summary["missions"])
    assert fr.exit_code(summary) == 2 and not summary["integration_path_ok"]
    assert summary["learning"]["report"]["discoveries"] == 0 and "orange_projected" not in summary["learning"]
    assert not (tmp_path / "out" / "A").exists()


def test_offline_fixture_end_to_end_learning_lifecycle_without_scripted_benefit(env, tmp_path):
    summary = fr.run(fr.load_config(CONFIG), tmp_path / "out", "offline-fixture")
    assert summary["mode"].startswith("OFFLINE_FIXTURE")
    assert [m["tag"] for m in summary["missions"]] == ["A", "B", "B-control"]
    assert summary["integration_path_ok"], [m["integration_problems"] for m in summary["missions"]]
    assert fr.exit_code(summary) == 0
    assert all(m["state"] in ("UNRESOLVED", "COMPLETED") and m["mission_success"] == (m["state"] == "COMPLETED") for m in summary["missions"])
    a, b, ctl = summary["missions"]
    assert a["captured_discoveries"] and b["knowledge_applied"] == a["captured_discoveries"] and ctl["knowledge_applied"] == []
    states = summary["learning"]["report"]["by_state"]
    assert states.get("NO_EFFECT_OBSERVED") == 1 and "BENEFIT_OBSERVED" not in states
    out = summary["learning"]["outcomes"][0]
    assert out["reward"] == out["control_reward"] and out["grader"] == "executed"
