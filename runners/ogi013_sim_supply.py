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

        async def call():
            from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
            req = NeuronRequest(consumer="ogi013-sim", objective="Simulate a tau2 customer", role_id=ROLE, cognitive_owner=CognitiveOwner.CONSUMER,
                                selection_mode=SelectionMode.PINNED_MODEL if model_key else SelectionMode.BEST, pinned_model_key=model_key,
                                required_skill_ids=[], budget=BudgetEnvelope(max_concurrency=1),
                                metadata={} if model_key else {"exclude_independence_keys": _single_provider_keys(svc)})
            neuron = await svc.acquire_neuron(req)
            lease = {"lease_id": neuron.lease_id, "provider_id": neuron.route.provider, "model_id": neuron.route.model,
                     "offer_id": neuron.route.offer_id, "model_key": neuron.route.model_key}
            res = await provider.execute(lease_id=lease["lease_id"], task=_flatten(messages), max_output_tokens=1024)
            return lease, res

        # Route selection (no pinned offer yet) tries alternatives: PlumMe's circuit state steers the next pick away from a failing offer.
        # Once the pair model is fixed, only its route may change (PINNED_MODEL); a model with no eligible route fails the pair.
        last = "NO_ATTEMPT"
        for attempt in range(60 if pinned else 12):
            t0 = time.time()
            try:
                lease, res = asyncio.run(call())
            except Exception as exc:  # noqa: BLE001 - e.g. PinnedWorkerUnavailable: record and wait, do not crash the benchmark run
                last = type(exc).__name__
                with log.open("a") as f:
                    f.write(json.dumps({"ts": t0, "pinned": bool(pinned), "exception": last, "detail": str(exc)[:200]}) + "\n")
                time.sleep(10)
                continue
            log_call(lease, res, t0, pinned)
            last = res["failure_class"]
            if res["success"] and res["output"]:
                break
            time.sleep(5)
        else:
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
