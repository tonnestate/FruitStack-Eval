"""Shared synthetic fixtures for the pilot tests: receipts as PlumMe writes them, sim-usage rows, whole arm directories. No inference."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "evidence/ogi013-pilot"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


guard = load("pilot_guard", PILOT / "pilot_guard.py")
BUDGET = json.loads((PILOT / "pilot_budget.json").read_text())
ARMS = ["pilot-1/single", "pilot-1/collab"]
RESERVE = BUDGET["reserve_tokens_per_dispatch"]
_n = [0]


def receipt(ok=True, tin=100, tout=10, cost_class="FREE_TIER", failure="RATE_LIMITED", cost_usd=None, lineage="lineage-a", model="m-a", usage=True):
    _n[0] += 1
    r = {"receipt_id": f"rc{_n[0]}", "success": ok, "cost_class": cost_class, "independence_key": lineage, "model": model, "provider": "prov", "failure_class": None if ok else failure,
         "started_at": "2026-10-28T10:00:00Z", "finished_at": "2026-10-28T10:00:01Z"}
    if usage:
        r["usage"] = {"input_tokens": tin, "output_tokens": tout, "cost_usd": cost_usd}
    return r


def write_arm(runs, arm, receipts=(), sim_ids=(), sim_extra=()):
    """Receipts as PlumMe writes them (agent AND simulator dispatches); sim-usage.jsonl lists the simulator ones by receipt id (plus rows whose receipt is missing)."""
    d = Path(runs) / arm
    (d / "fruitstack/plumme-state").mkdir(parents=True, exist_ok=True)
    (d / "fruitstack/plumme-state/receipts.jsonl").write_text("".join(json.dumps(r) + "\n" for r in receipts))
    by_id = {r["receipt_id"]: r for r in receipts}
    sim = [{"receipt_id": i, "success": by_id[i]["success"], "model_key": BUDGET["simulator_model_key"], "input_tokens": (by_id[i].get("usage") or {}).get("input_tokens"),
            "output_tokens": (by_id[i].get("usage") or {}).get("output_tokens"), "cost_usd": None} for i in sim_ids] + list(sim_extra)
    (d / "sim-usage.jsonl").write_text("".join(json.dumps(r) + "\n" for r in sim))
    return d
