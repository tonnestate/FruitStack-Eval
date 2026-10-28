"""Fail-closed pilot guard (evidence/ogi013-pilot/pilot_guard.py): approval gate, usage accounting, cap detection, and a real process-group stop. No inference; synthetic receipts."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pilot_guard", ROOT / "evidence/ogi013-pilot/pilot_guard.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
BUDGET = json.loads((ROOT / "evidence/ogi013-pilot/pilot_budget.json").read_text())


def arm(runs, name, receipts, sim=0):
    d = runs / name
    (d / "fruitstack/plumme-state").mkdir(parents=True)
    (d / "fruitstack/plumme-state/receipts.jsonl").write_text("\n".join(json.dumps({"success": True, "usage": {"input_tokens": 1000, "output_tokens": 100}}) for _ in range(receipts)) + "\n")
    (d / "sim-usage.jsonl").write_text("\n".join(json.dumps({"success": True, "input_tokens": 500, "output_tokens": 50}) for _ in range(sim)) + "\n")


def test_approval_must_name_exactly_this_budget(tmp_path):
    b = tmp_path / "b.json"
    b.write_text('{"x": 1}')
    ok, bad = tmp_path / "ok", tmp_path / "bad"
    ok.write_text(hashlib.sha256(b.read_bytes()).hexdigest() + "  approved by owner\n")
    bad.write_text("0" * 64)
    assert guard.verify_approval(str(b), str(ok)) and not guard.verify_approval(str(b), str(bad)) and not guard.verify_approval(str(b), str(tmp_path / "missing"))
    assert guard.main(["x", "verify-approval", str(b), str(tmp_path / "missing")]) == 2        # no approval = refusal, never a default


def test_usage_counts_every_dispatch_and_simulator_call(tmp_path):
    arm(tmp_path, "pilot-1/single", receipts=10, sim=4)
    u = guard.usage(str(tmp_path), ["pilot-1/single"])
    assert u["dispatches"] == 14 and u["tokens"] == 10 * 1100 + 4 * 550
    assert guard.exceeded(BUDGET, u) == []


def test_caps_are_detected_per_arm_and_cumulatively(tmp_path):
    arm(tmp_path, "pilot-1/single", receipts=60, sim=0)                       # over the SINGLE arm cap (45), still under the cumulative cap (150)
    u = guard.usage(str(tmp_path), ["pilot-1/single"])
    assert any("pilot-1/single" in w or "SINGLE" in w for w in guard.exceeded({**BUDGET, "arms": {"pilot-1/single": BUDGET["arms"]["SINGLE"]}}, u))
    arm(tmp_path, "pilot-1/econ", receipts=100, sim=0)
    assert any("dispatches" in w for w in guard.exceeded(BUDGET, guard.usage(str(tmp_path), ["pilot-1/single", "pilot-1/econ"])))
    assert guard.exceeded(BUDGET, {"dispatches": 1, "tokens": 1, "per_arm": {}}, started_at=time.time() - 91 * 60) == ["wall clock over the cap"]


def test_watch_stops_the_running_process_group_when_a_cap_is_exceeded(tmp_path):
    arm(tmp_path, "pilot-1/single", receipts=200, sim=0)
    budget = tmp_path / "budget.json"
    budget.write_text(json.dumps(BUDGET))
    victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
    (tmp_path / "pids").write_text(str(victim.pid))
    rc = guard.main(["x", "watch", str(budget), str(tmp_path), str(tmp_path / "pids"), "pilot-1/single"])
    victim.wait(timeout=10)
    assert rc == 3 and victim.returncode is not None and (tmp_path / "PILOT_HALT").is_file()
