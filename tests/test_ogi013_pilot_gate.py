"""Pilot corrections (evidence/ogi013-pilot + runners/ogi013_pilot_gate.py): fail-closed usage, budgets enforced BEFORE provider dispatch, and the pilot really runs COLLAB against SINGLE.
Synthetic receipts, no inference, the pilot is never executed."""
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "evidence/ogi013-pilot"
sys.path.insert(0, str(ROOT / "runners"))
import importlib.util

spec = importlib.util.spec_from_file_location("pilot_guard", PILOT / "pilot_guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
import ogi013_pilot_gate as gate

BUDGET = json.loads((PILOT / "pilot_budget.json").read_text())
ARMS = ["pilot-1/single", "pilot-1/collab"]
RESERVE = BUDGET["reserve_tokens_per_dispatch"]


def rows(runs, arm, receipts=(), sim=()):
    d = runs / arm
    (d / "fruitstack/plumme-state").mkdir(parents=True, exist_ok=True)
    (d / "fruitstack/plumme-state/receipts.jsonl").write_text("".join(json.dumps(r) + "\n" for r in receipts))
    (d / "sim-usage.jsonl").write_text("".join(json.dumps(r) + "\n" for r in sim))


def ok(n_in=100, n_out=10):
    return {"success": True, "usage": {"input_tokens": n_in, "output_tokens": n_out}}


# ---- missing usage fails closed -----------------------------------------------------------------------------------------------------------------------------------

def test_a_successful_dispatch_without_usage_halts_and_is_never_counted_as_zero(tmp_path):
    rows(tmp_path, ARMS[0], receipts=[ok(), {"success": True, "usage": {}}, {"success": True}], sim=[{"success": True, "input_tokens": 0, "output_tokens": 0}])
    u = guard.usage(str(tmp_path), ARMS, RESERVE)
    assert u["receipts_without_usage"] == 3 and u["dispatches"] == 4          # two receipts and one simulator call recorded nothing
    assert any(w.startswith("MISSING_USAGE") for w in guard.exceeded(BUDGET, u))
    assert any(w.startswith("MISSING_USAGE") for w in guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]))


def test_a_failed_dispatch_without_usage_is_charged_the_reserve_not_zero(tmp_path):
    rows(tmp_path, ARMS[0], receipts=[ok(), {"success": False, "usage": None}], sim=[{"success": False}])
    u = guard.usage(str(tmp_path), ARMS, RESERVE)
    assert u["receipts_without_usage"] == 0 and u["unmetered_failures"] == 2 and u["tokens"] == 110 + 2 * RESERVE
    assert guard.usage(str(tmp_path), ARMS)["tokens"] == 110                       # (the plain CLI view without a reserve still reports what was recorded)


def test_an_arm_without_a_cap_and_a_budget_without_reserve_refuse(tmp_path):
    rows(tmp_path, "pilot-1/unknown", receipts=[ok()])
    assert any("no cap" in w for w in guard.precheck(BUDGET, str(tmp_path), ["pilot-1/unknown"], "pilot-1/unknown"))
    assert guard.precheck({k: v for k, v in BUDGET.items() if k != "reserve_tokens_per_dispatch"}, str(tmp_path), ARMS, ARMS[0]) == ["budget declares no reserve_tokens_per_dispatch (fail closed)"]


# ---- budgets are enforced before the dispatch ---------------------------------------------------------------------------------------------------------------------

def test_precheck_refuses_the_dispatch_that_would_cross_a_cap(tmp_path):
    cap = BUDGET["arms"][ARMS[0]]["max_dispatches"]
    rows(tmp_path, ARMS[0], receipts=[ok() for _ in range(cap - 1)])
    assert guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]) == []                # dispatch number `cap` is still allowed
    rows(tmp_path, ARMS[0], receipts=[ok() for _ in range(cap)])
    why = guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0])
    assert why and all("would exceed" in w for w in why) and not guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS))      # nothing is over yet: the NEXT dispatch is what is refused
    tok_cap = BUDGET["arms"][ARMS[0]]["max_tokens"]
    rows(tmp_path, ARMS[0], receipts=[ok(tok_cap - RESERVE, 1)])                      # 1 dispatch, the reserve for the next one would cross the token cap
    assert any("tokens" in w and "would exceed" in w for w in guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]))
    rows(tmp_path, ARMS[0], receipts=[ok(tok_cap - RESERVE - 2, 1)])
    assert guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]) == []


def test_precheck_enforces_the_cumulative_cap_across_arms(tmp_path):
    tight = {**BUDGET, "cumulative": {**BUDGET["cumulative"], "max_dispatches": 100}}          # the arm caps (40 + 80) sum to the pilot cap, so the pilot cap is tightened to show it binds on its own
    rows(tmp_path, ARMS[0], receipts=[ok() for _ in range(40)])
    rows(tmp_path, ARMS[1], receipts=[ok() for _ in range(59)])
    assert guard.precheck(tight, str(tmp_path), ARMS, ARMS[1]) == []
    rows(tmp_path, ARMS[1], receipts=[ok() for _ in range(60)])
    assert any(w.startswith("pilot: next dispatch would exceed 100") for w in guard.precheck(tight, str(tmp_path), ARMS, ARMS[1]))


def _env(monkeypatch, runs, budget=None):
    path = runs / "budget.json"
    path.write_text(json.dumps(budget or BUDGET))
    for k, v in {"OGI013_PILOT_BUDGET": str(path), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs),
                 "OGI013_PILOT_ARMS": ",".join(ARMS), "OGI013_PILOT_ARM": ARMS[1], "OGI013_PILOT_START": "9999999999"}.items():
        monkeypatch.setenv(k, v)


def test_the_gate_is_inactive_without_a_budget_and_fail_closed_with_one(tmp_path, monkeypatch):
    monkeypatch.delenv("OGI013_PILOT_BUDGET", raising=False)
    gate.check()                                                                      # the frozen conditions never set it: no effect
    _env(monkeypatch, tmp_path)
    gate.check()                                                                      # within budget: allowed
    monkeypatch.delenv("OGI013_PILOT_ARM")
    with pytest.raises(gate.PilotBudgetStop, match="misconfigured"):
        gate.check()
    assert (tmp_path / "PILOT_HALT").is_file()


def test_the_gate_halts_on_exhaustion_and_on_missing_usage_and_stays_halted(tmp_path, monkeypatch):
    _env(monkeypatch, tmp_path)
    rows(tmp_path, ARMS[1], receipts=[ok() for _ in range(BUDGET["arms"][ARMS[1]]["max_dispatches"])])
    with pytest.raises(gate.PilotBudgetStop, match="would exceed"):
        gate.check()
    halt = json.loads((tmp_path / "PILOT_HALT").read_text())
    assert halt["by"] == "pre-dispatch gate"
    with pytest.raises(gate.PilotBudgetStop, match="PILOT_HALT exists"):              # once halted, every later dispatch is refused
        gate.check()
    other = tmp_path / "second"
    other.mkdir()
    _env(monkeypatch, other)
    rows(other, ARMS[1], receipts=[{"success": True}])
    with pytest.raises(gate.PilotBudgetStop, match="MISSING_USAGE"):
        gate.check()


def test_an_unreadable_budget_or_guard_is_a_refusal_not_a_pass(tmp_path, monkeypatch):
    _env(monkeypatch, tmp_path)
    monkeypatch.setenv("OGI013_PILOT_BUDGET", str(tmp_path / "nope.json"))
    with pytest.raises(gate.PilotBudgetStop, match="gate error"):
        gate.check()


def test_the_gate_runs_before_the_provider_dispatch_in_both_dispatch_paths():
    agent = (ROOT / "runners/ogi013_tau2_agent.py").read_text()
    step = agent[agent.index("    def step(self, prompt"):]
    assert step.index("pilot_gate()") < step.index("fs.prepare(") < step.index("fs.infer(") and "pilot_gate()" not in step.split("except PeachError")[1].split("self.stats[\"steps\"]")[0]
    sim = (ROOT / "runners/ogi013_sim_supply.py").read_text()
    loop = sim[sim.index("        for attempt in range(60"):]
    assert loop.index("pilot_gate()") < loop.index("asyncio.run(call(") and loop.index("pilot_gate()") < loop.index("            try:")        # outside the try: a stop is never retried


def test_episode_step_refuses_before_touching_the_stack(tmp_path, monkeypatch):
    pytest.importorskip("tau2")
    from ogi013_tau2_agent import Episode
    _env(monkeypatch, tmp_path)
    rows(tmp_path, ARMS[1], receipts=[ok() for _ in range(BUDGET["arms"][ARMS[1]]["max_dispatches"])])
    with pytest.raises(gate.PilotBudgetStop):
        Episode.step(SimpleNamespace(stack=SimpleNamespace(fs=None)), "prompt", "tag")      # fs=None: any attempt to prepare/infer would raise AttributeError instead of PilotBudgetStop


# ---- the pilot really compares COLLAB with SINGLE ---------------------------------------------------------------------------------------------------------------------

def test_pilot_script_runs_collab_against_single_on_the_pilot_checkout():
    script = (PILOT / "run_pilot.sh").read_text()
    single = next(ln for ln in script.splitlines() if "pilot-1/single" in ln and "setsid" in ln)
    collab = next(ln for ln in script.splitlines() if "pilot-1/collab" in ln and "setsid" in ln)
    assert " single " in single and "OGI013_ORG_COLLAB" not in single and "OGI013_PILOT_ARM=pilot-1/single" in single
    assert " rg2 " in collab and "OGI013_ORG_COLLAB=1" in collab and "OGI013_PILOT_ARM=pilot-1/collab" in collab        # the arm that used to run the economy mode only
    assert "run_org.sh" not in script and "ogi013-org\n" not in script and "PILOT_CODE" in script and "ogi013_org_collab.py" in script
    arm = (PILOT / "run_arm.sh").read_text()
    assert "D=${PILOT_CODE:?" in arm and "/ogi013-org " not in arm and "D=/root" not in arm
    assert set(BUDGET["arms"]) == set(ARMS) and f'OGI013_PILOT_ARMS="{",".join(ARMS)}"' in script
    assert f'airline {"single"} pilot-1-task{BUDGET["task"]["id"]}' in single and f' {BUDGET["task"]["id"]} airline ' in collab


def test_pilot_refuses_to_start_without_the_owners_approval(tmp_path):
    r = subprocess.run(["bash", str(PILOT / "run_pilot.sh")], env={"PATH": "/usr/bin:/bin", "PILOT_APPROVAL": str(tmp_path / "missing")}, capture_output=True, text=True, timeout=60)
    assert r.returncode == 2 and "REFUSED" in r.stdout
