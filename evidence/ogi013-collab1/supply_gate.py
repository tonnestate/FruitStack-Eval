#!/usr/bin/env python3
"""Verified simulator capacity (COLLAB-1, AMENDMENT-1 section K). Eligibility is not capacity: PlumMe can list a route as eligible that then answers RATE_LIMITED. This performs ONE real, tiny,
zero-cash completion through PlumMe (the same PlumMeProvider/lease path the simulator uses) on allowlisted models until one answers, and writes the answering model to the block's route file so the block
starts on a model that has just served a request. Exit 0 = verified (route file written), 3 = SUPPLY_UNAVAILABLE (no model answered; nothing consumed but the probe requests, logged in supply_gate.jsonl).
Exit 4 = nothing was probeable (every pool/credential is already known EXHAUSTED or blocked in PlumMe's persistent pool health): no request was made at all.
usage: supply_gate.py RUNS_DIR ROUTE_FILE   (host python, same PYTHONPATH as the arms)"""
import asyncio
import json
import os
import random
import sys
import time
from pathlib import Path


def seed_pool_health(svc, runs: Path) -> None:
    """Replay evidence this campaign already holds through PlumMe's own failure path so the persistent pool health knows it: (1) every credential the registry holds EXHAUSTED, (2) the latest
    failure receipt per provider in the campaign's state directories re-classified by PlumMe's (corrected) classifier. Idempotent; nothing is dispatched."""
    from plumme.failures import classify_http
    sched, seen = svc.scheduler, set()
    sched._load_pool_state()
    reg = json.loads((runs / "credential_health.json").read_text()) if (runs / "credential_health.json").exists() else {}
    by_provider = {}
    for o in svc.store.offers.values():
        by_provider.setdefault(o.provider, o)
    for handle in (reg.get("exhausted") or {}):
        prov = (reg.get("sources") or {}).get(handle, {}).get("provider")
        o = by_provider.get(prov)
        if o is not None and o.quota_pool_id not in sched.pool_state:
            sched.observe_pool_failure(o, "BILLING_OR_CREDIT_EXHAUSTED", f"credential {handle} exhausted (registry)")
            seen.add(o.quota_pool_id)
    latest = {}
    for f in runs.rglob("receipts.jsonl"):
        for line in f.read_text(errors="replace").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            m = r.get("failure_message") or ""
            if not r.get("success") and r.get("failure_class") in ("RATE_LIMITED", "BILLING_OR_CREDIT_EXHAUSTED") and m.startswith("HTTP 429") and (r.get("provider") not in latest or r.get("finished_at", "") > latest[r["provider"]].get("finished_at", "")):
                latest[r["provider"]] = r
    for prov, r in latest.items():
        o = by_provider.get(prov)
        cls = classify_http(429, r.get("failure_message") or "")[0]
        if o is not None and cls == "BILLING_OR_CREDIT_EXHAUSTED" and o.quota_pool_id not in sched.pool_state:
            sched.observe_pool_failure(o, cls, r.get("failure_message"))


def main(runs: Path, route_file: Path) -> int:
    sys.path[:0] = [str(Path(__file__).resolve().parents[2] / "runners")]
    state = runs / "supply-gate" / "fruitstack" / "plumme-state"                       # harvested by the credential registry like any episode's state
    (state / "knowledge").mkdir(parents=True, exist_ok=True)
    os.environ["PLUMME_STATE_DIR"], os.environ["OGI013_PILOT_RUNS"] = str(state), str(runs)
    os.environ["PLUMME_SHARED_HEALTH_DIR"] = str(runs)                                       # PlumMe's persistent pool health (pool_health.json) is shared by every episode and this gate
    snap = Path("/root/fruits/research/FRUITSTACK-EVAL-004/inputs/models.dev-api.json")
    if snap.exists() and not (state / "knowledge" / "models.dev-api.json").exists():
        import shutil
        shutil.copyfile(snap, state / "knowledge" / "models.dev-api.json")
    from ogi013_credential_health import latch_exhaustion, prepare_state
    prepare_state(state)
    import ogi013_sim_supply as sim
    from peachme.plumme import PlumMeProvider
    from plumme.config import Settings
    from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
    from plumme.service import PlumMeService, default_adapters
    settings = Settings.load()
    svc = PlumMeService(settings, adapters=default_adapters(settings))
    latch_exhaustion(svc)
    asyncio.run(svc.discover())
    seed_pool_health(svc, runs)
    pool = sim._selection_pool(runs, svc)
    random.shuffle(pool)
    log = runs / "supply_gate.jsonl"
    provider = PlumMeProvider(svc)
    probeable = [k for k in pool if sim._earliest_retry(svc, k) == 0.0]
    if not probeable:
        with log.open("a") as f:
            f.write(json.dumps({"ts": time.time(), "verdict": "SUPPLY_UNAVAILABLE", "probeable": 0, "note": "no request made: every route's pool is EXHAUSTED/blocked in pool_health.json"}) + "\n")
        return 4
    for key in probeable:
        t0, row = time.time(), {"ts": time.time(), "model_key": key}
        try:
            async def one():
                req = NeuronRequest(consumer="ogi013-supply-gate", objective="Supply gate", role_id=sim.ROLE, cognitive_owner=CognitiveOwner.CONSUMER, selection_mode=SelectionMode.PINNED_MODEL,
                                    pinned_model_key=key, required_skill_ids=[], budget=BudgetEnvelope(max_concurrency=1, max_cost_usd=0.0), metadata={})
                n = await svc.acquire_neuron(req)
                res = await provider.execute(lease_id=n.lease_id, task="[user] Reply with the single word OK.", max_output_tokens=None, max_total_tokens=2000, max_cost_usd=0.0)
                return n, res
            n, res = asyncio.run(one())
            row.update(provider=n.route.provider, success=bool(res["success"] and res["output"]), failure_class=res["failure_class"], latency_s=round(time.time() - t0, 2),
                       input_tokens=res["input_tokens"], output_tokens=res["output_tokens"])
            if row["success"]:
                route_file.parent.mkdir(parents=True, exist_ok=True)
                route_file.write_text(json.dumps({"model_key": n.route.model_key, "offer_id": n.route.offer_id, "provider": n.route.provider, "model": n.route.model, "verified_by": "supply_gate"}))
                with log.open("a") as f:
                    f.write(json.dumps(row) + "\n")
                return 0
        except Exception as exc:  # noqa: BLE001 - a model that cannot be probed is simply not capacity
            row.update(success=False, exception=type(exc).__name__, detail=str(exc)[:160])
        with log.open("a") as f:
            f.write(json.dumps(row) + "\n")
    with log.open("a") as f:
        f.write(json.dumps({"ts": time.time(), "verdict": "SUPPLY_UNAVAILABLE", "tried": len(pool)}) + "\n")
    return 3


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
