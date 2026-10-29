"""Pre-dispatch gate (runners/ogi013_pilot_gate.py): inactive without a pilot budget, fail closed with one, refuses BEFORE the provider dispatch in both dispatch paths, stays halted, records
the stop. Synthetic receipts, no inference."""
import json
import sys
from types import SimpleNamespace

import pytest

from ogi013_pilot_fixtures import ARMS, BUDGET, PILOT, ROOT, receipt, write_arm

sys.path.insert(0, str(ROOT / "runners"))
import ogi013_pilot_gate as gate


def _env(monkeypatch, runs, budget=None, arm=ARMS[1]):
    path = runs / "budget.json"
    path.write_text(json.dumps(budget or BUDGET))
    for k, v in {"OGI013_PILOT_BUDGET": str(path), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs), "OGI013_PILOT_ARMS": ",".join(ARMS),
                 "OGI013_PILOT_ARM": arm, "OGI013_PILOT_START": "9999999999"}.items():
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


def test_the_gate_halts_on_exhaustion_and_stays_halted_with_the_evidence_in_place(tmp_path, monkeypatch):
    _env(monkeypatch, tmp_path)
    write_arm(tmp_path, ARMS[1], [receipt() for _ in range(BUDGET["arms"][ARMS[1]]["max_dispatches"])])
    with pytest.raises(gate.PilotBudgetStop, match="would exceed"):
        gate.check()
    assert json.loads((tmp_path / "PILOT_HALT").read_text())["by"] == "pre-dispatch gate"
    with pytest.raises(gate.PilotBudgetStop, match="PILOT_HALT exists"):              # once halted, every later dispatch is refused
        gate.check()
    assert (tmp_path / ARMS[1] / "fruitstack/plumme-state/receipts.jsonl").is_file()   # and nothing was removed


@pytest.mark.parametrize("bad,match", [(receipt(usage=False), "MISSING_USAGE"), (receipt(cost_class="NORMAL"), "UNKNOWN_CASH_EXPOSURE"), (receipt(cost_class=None), "UNKNOWN_CASH_EXPOSURE")])
def test_the_gate_halts_on_unknown_usage_and_unknown_cash(tmp_path, monkeypatch, bad, match):
    _env(monkeypatch, tmp_path)
    write_arm(tmp_path, ARMS[1], [bad])
    with pytest.raises(gate.PilotBudgetStop, match=match):
        gate.check()


def test_the_gate_halts_on_a_failure_storm(tmp_path, monkeypatch):
    _env(monkeypatch, tmp_path)
    write_arm(tmp_path, ARMS[1], [receipt(ok=False, usage=False) for _ in range(BUDGET["max_consecutive_failures"])])
    with pytest.raises(gate.PilotBudgetStop, match="consecutive failed dispatches"):
        gate.check()


def test_an_unreadable_budget_or_guard_is_a_refusal_not_a_pass(tmp_path, monkeypatch):
    _env(monkeypatch, tmp_path)
    monkeypatch.setenv("OGI013_PILOT_BUDGET", str(tmp_path / "nope.json"))
    with pytest.raises(gate.PilotBudgetStop, match="gate error"):
        gate.check()


def test_the_gate_runs_before_the_provider_dispatch_in_both_dispatch_paths():
    agent = (ROOT / "runners/ogi013_tau2_agent.py").read_text()
    step = agent[agent.index("    def step(self, prompt"):]
    assert step.index("pilot_gate()") < step.index("fs.prepare(") < step.index("fs.infer(")
    sim = (ROOT / "runners/ogi013_sim_supply.py").read_text()
    loop = sim[sim.index("        for attempt in range(60"):]
    assert loop.index("pilot_gate()") < loop.index("asyncio.run(call(") and loop.index("pilot_gate()") < loop.index("            try:")        # outside the try: a stop is never retried


def test_episode_step_refuses_before_touching_the_stack_and_records_the_stop(tmp_path, monkeypatch):
    pytest.importorskip("tau2")
    from ogi013_tau2_agent import Episode
    _env(monkeypatch, tmp_path)
    write_arm(tmp_path, ARMS[1], [receipt() for _ in range(BUDGET["arms"][ARMS[1]]["max_dispatches"])])
    ep = object.__new__(Episode)
    ep.stack, ep.log, ep.task_id, ep.mode, ep.sid, ep.budget_stopped, ep.step_n = SimpleNamespace(fs=None), tmp_path / "events.jsonl", "24", "rg2", "s", False, 0
    with pytest.raises(gate.PilotBudgetStop):
        ep.step("prompt", "tag")                                                       # fs=None: any attempt to prepare/infer would raise AttributeError instead of PilotBudgetStop
    assert ep.budget_stopped and json.loads((tmp_path / "events.jsonl").read_text().splitlines()[-1])["event"] == "BUDGET_STOP"


def test_token_limits_count_agent_and_simulator_usage_and_carry_the_per_step_ceiling(tmp_path, monkeypatch):
    monkeypatch.delenv("OGI013_PILOT_BUDGET", raising=False)
    assert gate.token_limits() is None                                                     # outside the pilot: nothing changes
    _env(monkeypatch, tmp_path)
    rows = [receipt(tin=10000, tout=0) for _ in range(3)]
    write_arm(tmp_path, ARMS[1], rows, sim_ids=[rows[2]["receipt_id"]])                     # 20k agent + 10k simulator tokens
    lim = gate.token_limits()
    assert lim == {"headroom": BUDGET["arms"][ARMS[1]]["max_tokens"] - 30000, "per_step": BUDGET["max_tokens_per_step"], "calls": BUDGET["arms"][ARMS[1]]["max_dispatches"] - 3}
    write_arm(tmp_path, ARMS[0], [receipt(tin=BUDGET["cumulative"]["max_tokens"] - 30000 - 500, tout=0)])
    assert gate.token_limits()["headroom"] == 500                                           # the pilot-wide cap binds once the other arm has used its share
    monkeypatch.setenv("OGI013_PILOT_BUDGET", str(tmp_path / "missing.json"))
    with pytest.raises(gate.PilotBudgetStop, match="token limits unavailable"):
        gate.token_limits()


def test_the_requests_left_count_provider_requests_not_receipts(tmp_path, monkeypatch):
    _env(monkeypatch, tmp_path)
    r = receipt(tin=100, tout=10)
    r["metadata"] = {"provider_attempt_count": 4}                                          # one receipt, four provider requests (continuations / retries)
    write_arm(tmp_path, ARMS[1], [r, receipt()])
    assert gate.token_limits()["calls"] == BUDGET["arms"][ARMS[1]]["max_dispatches"] - 5
