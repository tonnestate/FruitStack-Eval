"""Route the tau2 user simulator through PlumMe (same free-supply discovery, credentials and route choice as the FruitStack workers).

The first simulator call in a comparison pair lets PlumMe pick a route (BEST; providers without credentials are skipped by PlumMe itself)
and records it in OGI013_SIM_ROUTE_FILE; every later call in either arm pins that exact offer, so the simulator model is identical
within the pair. A pinned-route failure fails the turn (the run stays INCOMPLETE) rather than silently switching models.
Every call is appended to <out>/sim-usage.jsonl with provider/model/offer/receipt/tokens/cost.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

from peachme.plumme import PlumMeProvider
from tau2.data_model.message import AssistantMessage
from tau2.user import user_simulator

ROLE = "REASONING"  # an existing PlumMe role; the simulator needs no dedicated one


def _flatten(messages) -> str:
    lines = []
    for m in messages:
        role = getattr(m, "role", "user")
        text = getattr(m, "content", None)
        if text:
            lines.append(f"[{role}] {text}")
    return "\n\n".join(lines) + "\n\n[assistant-turn: write the next message of the simulated customer ONLY, no preface]"



def _single_provider_keys(svc) -> list[str]:
    """The pair's simulator model is fixed for both arms, so choose one that survives losing a provider (free quota exhausts mid-pair): exclude models with fewer than two
    distinct providers currently serving them. A selection hint over PlumMe's own offer table; PlumMe still decides eligibility and the route."""
    try:
        from plumme.knowledge import independence_key
        accepted = {"AVAILABLE", "QUOTA_LOW", "DEGRADED"}
        providers: dict[str, set] = {}
        for o in svc.store.offers.values():
            if str(getattr(getattr(o, "health", None), "value", getattr(o, "health", ""))) in accepted:
                providers.setdefault(str(o.model_key), set()).add(str(o.provider))
        return sorted({independence_key(o) for o in svc.store.offers.values() if len(providers.get(str(o.model_key), ())) < 2})
    except Exception:  # noqa: BLE001 - a hint only; without it the selection is plain BEST as before
        return []

MAX_WAIT_S = 600   # longest cooldown worth waiting for inside a block (per-minute rate-limit windows); a daily quota reset is far beyond it


def _earliest_retry(svc, model_key: str):
    """Seconds until PlumMe's own circuit/quota/credential state lets any route of the pinned model run again; None = no route will become available."""
    waits = []
    for o in svc.store.offers.values():
        if str(o.model_key) != str(model_key) or str(getattr(getattr(o, "health", None), "value", getattr(o, "health", ""))) not in {"AVAILABLE", "QUOTA_LOW", "DEGRADED"}:
            continue
        w = svc.scheduler.availability(o)["retry_after_seconds"]
        if w is not None:
            waits.append(float(w))
    return min(waits) if waits else None


def _hard_excluded_keys(svc, runs_dir: Path) -> list[str]:
    """Models that cannot carry a pair: not in the live-verified allowlist (sim_allowlist.json, written from a real capacity survey) or recorded as quota-exhausted
    within the last 24h (sim_exhausted.jsonl, written when a pinned model failed a block). Selection hint only; PlumMe still decides eligibility and the route."""
    try:
        from plumme.knowledge import independence_key
        banned: set[str] = set()
        allow_file, spent_file = runs_dir / "sim_allowlist.json", runs_dir / "sim_exhausted.jsonl"
        if spent_file.exists():
            for line in spent_file.read_text().splitlines():
                row = json.loads(line) if line.strip() else {}
                if time.time() - row.get("ts", 0) < 86400:
                    banned.add(str(row["model_key"]))
        allowed = set(json.loads(allow_file.read_text())["model_keys"]) if allow_file.exists() else None
        return sorted({independence_key(o) for o in svc.store.offers.values() if str(o.model_key) in banned or (allowed is not None and str(o.model_key) not in allowed)})
    except Exception:  # noqa: BLE001 - a hint only
        return []


def install(svc, route_file: Path, out: Path) -> None:
    route_file, log = Path(route_file), Path(out) / "sim-usage.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)

    def log_call(lease, res, t0, pinned):
        rec = {"ts": t0, "latency_s": round(time.time() - t0, 2), "pinned": bool(pinned), "provider": lease["provider_id"], "model": lease["model_id"],
               "offer_id": lease["offer_id"], "model_key": lease["model_key"], "receipt_id": res["receipt_id"], "input_tokens": res["input_tokens"], "output_tokens": res["output_tokens"],
               "cost_usd": res["cost_usd"], "success": res["success"], "failure_class": res["failure_class"], "attempts": len(res["route_attempts"])}
        with log.open("a") as f:
            f.write(json.dumps(rec) + "\n")

    def generate(model, messages, tools=None, tool_choice=None, call_name=None, **kwargs):
        # text-only simulator: user-side tools are never offered (telecom-style tasks that need them are out of scope)
        model_key = json.loads(route_file.read_text())["model_key"] if route_file.exists() else None
        pinned = model_key  # the pair's simulator MODEL is fixed; PlumMe may choose any eligible route to that model (pinned_model_key)
        provider = PlumMeProvider(svc)

        async def call(prefer_multi_provider=True):
            from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
            req = NeuronRequest(consumer="ogi013-sim", objective="Simulate a tau2 customer", role_id=ROLE, cognitive_owner=CognitiveOwner.CONSUMER,
                                selection_mode=SelectionMode.PINNED_MODEL if model_key else SelectionMode.BEST, pinned_model_key=model_key,
                                required_skill_ids=[], budget=BudgetEnvelope(max_concurrency=1),
                                metadata={"exclude_independence_keys": sorted(set(_hard_excluded_keys(svc, route_file.parent)) | (set(_single_provider_keys(svc)) if prefer_multi_provider else set()))} if not model_key else {})
            neuron = await svc.acquire_neuron(req)
            lease = {"lease_id": neuron.lease_id, "provider_id": neuron.route.provider, "model_id": neuron.route.model,
                     "offer_id": neuron.route.offer_id, "model_key": neuron.route.model_key}
            res = await provider.execute(lease_id=lease["lease_id"], task=_flatten(messages), max_output_tokens=None)   # PlumMe negotiates the limit (PROTOCOL.md); a fixed 1024 let reasoning models exhaust it with EMPTY_CONTENT finish_reason=length
            return lease, res

        # Route selection (no pinned offer yet) tries alternatives: PlumMe's circuit state steers the next pick away from a failing offer.
        # Once the pair model is fixed, only its route may change (PINNED_MODEL); a model with no eligible route fails the pair.
        last = "NO_ATTEMPT"
        succeeded = False
        for attempt in range(60 if pinned else 12):
            t0 = time.time()
            try:
                lease, res = asyncio.run(call(prefer_multi_provider=attempt < 3))   # soft preference: plain BEST once the resilient set is saturated
            except Exception as exc:  # noqa: BLE001 - e.g. PinnedWorkerUnavailable: record and wait, do not crash the benchmark run
                last = type(exc).__name__
                with log.open("a") as f:
                    f.write(json.dumps({"ts": t0, "pinned": bool(pinned), "exception": last, "detail": str(exc)[:200]}) + "\n")
                if pinned:                       # PlumMe's cooldown/quota state decides: wait exactly the window if it is short, otherwise fail the block now (registered discard)
                    wait = _earliest_retry(svc, pinned)
                    with log.open("a") as f:
                        f.write(json.dumps({"ts": t0, "pinned": True, "earliest_retry_s": wait}) + "\n")
                    if wait is None or wait > MAX_WAIT_S:
                        break
                    time.sleep(wait + 2)
                else:
                    time.sleep(10)
                continue
            log_call(lease, res, t0, pinned)
            last = res["failure_class"]
            if res["success"] and res["output"]:
                succeeded = True
                break
            time.sleep(5)
        if not succeeded:
            if pinned:                                  # remember the model for 24h so the re-selection of the discarded block does not pick it again
                with (route_file.parent / "sim_exhausted.jsonl").open("a") as f:
                    f.write(json.dumps({"ts": time.time(), "model_key": pinned, "cause": last}) + "\n")
            raise RuntimeError(f"SIM_ROUTE_FAILED:{last}")
        if pinned is None:
            if not lease["model_key"]:
                raise RuntimeError("SIM_MODEL_KEY_MISSING: chosen route has no model_key, cannot hold the model constant")
            route_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                with route_file.open("x") as f:
                    json.dump({"model_key": lease["model_key"], "offer_id": lease["offer_id"], "provider": lease["provider_id"], "model": lease["model_id"]}, f)
            except FileExistsError:
                pass
        return AssistantMessage(role="assistant", content=res["output"], cost=res["cost_usd"] or 0.0,
                                usage={"prompt_tokens": res["input_tokens"] or 0, "completion_tokens": res["output_tokens"] or 0})

    user_simulator.generate = generate
