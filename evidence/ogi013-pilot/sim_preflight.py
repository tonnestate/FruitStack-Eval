#!/usr/bin/env python3
"""Simulator preflight for the pilot: is the pinned customer-simulator model executable RIGHT NOW? No inference. It builds a PlumMe service exactly as the arms do (fresh state dir, model-catalogue
snapshot, optional FLM_KEY source, metadata discovery) and asks PlumMe's own hard-eligibility gate whether a route of the pinned model passes. Exit 0 = executable, 1 = not (with PlumMe's reasons),
2 = the check itself could not run. usage: sim_preflight.py ROUTE_FILE STATE_DIR   (ROUTE_FILE = {"model_key": ...}); run with the host python and the same PYTHONPATH as the arms."""
import asyncio
import json
import os
import shutil
import sys
from pathlib import Path


def check(svc, model_key: str) -> dict:
    from ogi013_sim_supply import _earliest_retry, _explain
    known = any(str(o.model_key) == str(model_key) for o in svc.store.offers.values())
    wait = _earliest_retry(svc, model_key) if known else None
    return {"model_key": model_key, "model_known_to_plumme": known, "executable": known and wait == 0.0, "retry_after_s": wait, "explain": _explain(svc, model_key) if known else {}}


ZERO_CASH_CLASSES = ("ANONYMOUS_FREE", "FREE_TIER", "LOCAL", "TRIAL_CREDIT", "INCLUDED")      # the classes the pilot may use at USD 0.00 (pilot_guard); priced fields below are deliberately non-zero


class _ContractService:
    """A PlumMe stand-in for the lease CONTRACT only: it records the budget frozen at acquisition and runs PlumMe's REAL `_check_execution_budget` on every execution, then answers with a canned success.
    No provider lease is taken, nothing is dispatched, no network. Every request the arms' own code builds (ogi013_sim_supply, LineageHeart, PeachMe's provider and cash estimate) goes through it."""

    def __init__(self, cost_class: str):
        from types import SimpleNamespace
        self.cost_class, self.terms, self.checked, self.n = cost_class, {}, [], 0
        self.route = SimpleNamespace(offer_id="offer-c", model="contract-model", provider="prov-c", model_key="contract-model@x", independence_group="L-c", model_family="L-c",
                                     cost_class=SimpleNamespace(value=cost_class), input_cost_per_million=1.0, output_cost_per_million=2.0, context_window=32000, output_limit_per_response=4096)
        self.store, self.scheduler = SimpleNamespace(offers={}), SimpleNamespace(screen=lambda req: ([], {}), availability=lambda o: {"retry_after_seconds": None, "circuit_open": False,
                                                                                                                                   "credential_available": True, "quota_exhausted": False})

    async def acquire_neuron(self, req):
        from types import SimpleNamespace
        self.n += 1
        lid = f"lease-contract-{self.n}"
        self.terms[lid] = req.budget
        return SimpleNamespace(lease_id=lid, neuron_id=f"n{self.n}", role_id=req.role_id, cognitive_owner=SimpleNamespace(value="CONSUMER"), effective_skill_ids=[], route=self.route)

    async def execute_lease(self, ex):
        from types import SimpleNamespace
        from plumme.service import _check_execution_budget
        _check_execution_budget(self.terms[ex.lease_id], ex.budget)           # raises AuthorityDenied("LEASE_BUDGET_EXPANSION") exactly where PlumMe would
        self.checked.append(ex.lease_id)
        usage = SimpleNamespace(input_tokens=10, output_tokens=5, cost_usd=0.0)
        return SimpleNamespace(success=True, output="contract ok", receipt=SimpleNamespace(receipt_id=f"rcpt-{len(self.checked)}", decision_id=None, model="contract-model", usage=usage),
                               route_attempts=[{"failure_class": None}], no_equivalent_route=False, verification="NOT_VERIFIED", failure_class=None, execution_certainty="EXECUTED")


def contract_check(budget_path: str, guard_path: str) -> dict:
    """Would any lease the pilot takes be refused at EXECUTION by PlumMe's lease contract (an execution may narrow, never expand, the budget of its lease)? Covers the customer simulator
    (real ogi013_sim_supply under the pilot's env) and the agent steps (real LineageHeart acquire/execute with the cash values FruitStackSession passes: acquire = governance cost_remaining,
    execute = its per-dispatch cash estimate) for every zero-cash cost class. No inference, no real lease."""
    import asyncio
    import tempfile
    from types import SimpleNamespace
    cases, saved = [], dict(os.environ)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            budget = json.loads(Path(budget_path).read_text())
            arms = list(budget["arms"]) or ["contract/probe"]          # a campaign budget declares one default per-episode cap instead of named arms
            runs = tmp / "runs"
            for a in arms:
                (runs / a / "fruitstack/plumme-state").mkdir(parents=True)
                (runs / a / "fruitstack/plumme-state/receipts.jsonl").write_text("")
                (runs / a / "sim-usage.jsonl").write_text("")
            os.environ.update({"OGI013_PILOT_BUDGET": str(budget_path), "OGI013_PILOT_GUARD": str(guard_path), "OGI013_PILOT_RUNS": str(runs), "OGI013_PILOT_ARMS": ",".join(arms),
                               "OGI013_PILOT_ARM": arms[-1], "OGI013_PILOT_START": str(__import__("time").time())})
            from tau2.user import user_simulator
            import ogi013_sim_supply as sim
            from ogi013_lineage_heart import LineageHeart
            from peachme.fruitstack import FruitStackSession
            original = user_simulator.generate
            for cls in ZERO_CASH_CLASSES:
                svc = _ContractService(cls)
                route_file = tmp / f"sim-{cls}.route"
                route_file.write_text(json.dumps({"model_key": "contract-model@x"}))
                try:
                    sim.install(svc, route_file, tmp / f"out-{cls}")
                    user_simulator.generate("ignored", [SimpleNamespace(role="user", content="Hello")])
                    cases.append({"path": "simulator", "cost_class": cls, "ok": bool(svc.checked), "detail": "executed under the lease budget" if svc.checked else "no execution reached the lease check"})
                except Exception as exc:  # noqa: BLE001
                    cases.append({"path": "simulator", "cost_class": cls, "ok": False, "detail": f"{type(exc).__name__}: {str(exc)[:160]}"})
                finally:
                    user_simulator.generate = original
                svc = _ContractService(cls)
                heart = LineageHeart(svc)
                try:
                    env = asyncio.run(heart.acquire(role_id="REASONING", objective="contract", required_skill_ids=(), max_cost_usd=0.0))           # zero cash left: governance cost_remaining
                    est = FruitStackSession._dispatch_cash_estimate(env, "task " * 50, None)
                    asyncio.run(heart.execute(lease_id=env["lease_id"], task="task " * 50, max_output_tokens=None, max_total_tokens=int(budget["max_tokens_per_step"]), max_cost_usd=est))
                    cases.append({"path": "agent", "cost_class": cls, "ok": bool(svc.checked), "detail": f"executed under the lease budget (cash estimate {est})"})
                except Exception as exc:  # noqa: BLE001
                    cases.append({"path": "agent", "cost_class": cls, "ok": False, "detail": f"{type(exc).__name__}: {str(exc)[:160]}"})
    finally:
        os.environ.clear()
        os.environ.update(saved)
    return {"ok": bool(cases) and all(c["ok"] for c in cases), "cases": cases}


def build_service(state_dir: Path):
    from plumme.config import Settings
    from plumme.credentials import CredentialSource, CredentialSourceKind
    from plumme.service import PlumMeService, default_adapters
    os.environ["PLUMME_STATE_DIR"] = str(state_dir / "plumme-state")
    (state_dir / "plumme-state" / "knowledge").mkdir(parents=True, exist_ok=True)
    snap = Path("/root/fruits/research/FRUITSTACK-EVAL-004/inputs/models.dev-api.json")
    if snap.exists():
        shutil.copyfile(snap, state_dir / "plumme-state" / "knowledge" / "models.dev-api.json")
    settings = Settings.load()
    svc = PlumMeService(settings, adapters=default_adapters(settings))
    if os.environ.get("FLM_KEY"):
        svc.credentials.register_source(CredentialSource("freellmapi", CredentialSourceKind.ENV_REFERENCE, "freellmapi-isolated-instance", {"var": "FLM_KEY"}))
    asyncio.run(svc.discover())
    return svc


def main(argv) -> int:
    if len(argv) == 4 and argv[1] == "--contract":                      # usage: sim_preflight.py --contract BUDGET_FILE PILOT_GUARD_PY (offline, no service, no network)
        try:
            result = contract_check(argv[2], argv[3])
        except Exception as exc:  # noqa: BLE001 - a check that cannot run must not pass
            print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:300]}"}))
            return 2
        print(json.dumps(result))
        return 0 if result["ok"] else 1
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        model_key = json.loads(Path(argv[1]).read_text())["model_key"]
        result = check(build_service(Path(argv[2])), model_key)
    except Exception as exc:  # noqa: BLE001 - a preflight that cannot run must not pass
        print(json.dumps({"executable": False, "error": f"{type(exc).__name__}: {str(exc)[:300]}"}))
        return 2
    print(json.dumps(result, default=str))
    return 0 if result["executable"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
