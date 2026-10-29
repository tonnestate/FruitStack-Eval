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
import random
import time
from pathlib import Path

from ogi013_pilot_gate import PilotBudgetStop, step_parent_budget, token_limits
from ogi013_pilot_gate import check as pilot_gate
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

PINNED_RETRY_WINDOW_S = 120.0   # longest PlumMe-reported cooldown a pinned simulator route is waited out (AMENDMENT-1 M); longer or unknown = the attempt ends
SIM_MIN_ANSWER = 512   # pilot: the customer simulator's replies are short; a step that cannot afford this much answer is a budget stop, never a truncated reply

# (no wait/timeout constant: PlumMe's eligibility decides NOW; a route that is not eligible is never waited for - owner correction 2026-10-29)


def lease_cash(total_cap):
    """The ONE cash value of a simulator dispatch: the lease is acquired with it and every execution of that lease carries the SAME value, because PlumMe lets an execution narrow, never expand,
    the budget frozen at acquisition (plumme.service._check_execution_budget: a missing cap on an execution of a capped lease is LEASE_BUDGET_EXPANSION - what stopped PILOT-1 before any inference).
    Pilot (a token cap is in force): zero cash. Otherwise no cap on either side."""
    return None if total_cap is None else 0.0


def _earliest_retry(svc, model_keys):
    """Seconds until PlumMe lets any route of the given model(s) run again. 0.0 = a route passes PlumMe's hard eligibility gate (scheduler.screen) right now; otherwise the shortest KNOWN
    circuit/quota/credential cooldown among the models' routes; None = no route has a known recovery time (nothing to wait for). Offers that the gate rejects without any cooldown
    (e.g. no credential configured for that provider) neither count as available nor as a window."""
    from plumme.models import ExecutionRequest
    wanted = {str(k) for k in ([model_keys] if isinstance(model_keys, str) else model_keys)}
    eligible, _rejected = svc.scheduler.screen(ExecutionRequest(task="ogi013-sim-wait", role_id=ROLE))
    if any(str(o.model_key) in wanted for o in eligible):
        return 0.0
    waits = []
    for o in svc.store.offers.values():
        if str(o.model_key) in wanted:
            w = svc.scheduler.availability(o)["retry_after_seconds"]
            if w is not None:
                waits.append(float(w))
    return min(waits) if waits else None


def _explain(svc, model_key: str) -> dict:
    """Why PlumMe refuses every route of a model right now: its own hard-gate rejection codes and runtime availability per offer (diagnostic row in sim-usage.jsonl)."""
    try:
        from plumme.models import ExecutionRequest
        _eligible, rejected = svc.scheduler.screen(ExecutionRequest(task="ogi013-sim-explain", role_id=ROLE))
        out = {}
        for oid, o in svc.store.offers.items():
            if str(o.model_key) == str(model_key):
                av = svc.scheduler.availability(o)
                out[f"{o.provider}:{oid[-6:]}"] = {"rejected": rejected.get(oid) or rejected.get(getattr(o, "offer_id", oid)), "circuit_open": av["circuit_open"], "credential_available": av["credential_available"],
                                                   "quota_exhausted": av["quota_exhausted"], "retry_after_s": av["retry_after_seconds"]}
        return out
    except Exception as exc:  # noqa: BLE001 - diagnostic only
        return {"explain_failed": f"{type(exc).__name__}: {exc}"[:200]}


def _exhausted_providers(runs_dir: Path) -> set[str]:
    """Providers whose every known credential is EXHAUSTED in the campaign's credential registry (ogi013_credential_health). A state, not a timer."""
    f = Path(runs_dir) / "credential_health.json"
    if not f.exists():
        return set()
    try:
        reg = json.loads(f.read_text())
    except ValueError:
        return set()
    renewals = Path(runs_dir) / "credential_renewals.json"
    renewed = json.loads(renewals.read_text()) if renewals.exists() else {}
    by_provider: dict[str, list[bool]] = {}
    for handle, src in (reg.get("sources") or {}).items():
        ex = (reg.get("exhausted") or {}).get(handle)
        by_provider.setdefault(str(src.get("provider")), []).append(bool(ex) and float(renewed.get(handle, 0)) <= float(ex["at"]))
    return {p for p, flags in by_provider.items() if flags and all(flags)}


def _selection_pool(runs_dir: Path, svc=None) -> list[str]:
    """Models that may carry a new pair: the live-verified allowlist (sim_allowlist.json, from a real capacity survey) minus models that NO non-exhausted provider can serve. Exhaustion comes from the
    credential registry (an EXHAUSTED credential stays out until positive evidence of renewal) - never from a clock. A model is NOT excluded when another provider can serve it; the ROUTE is
    always PlumMe's choice. Empty = no allowlist, plain PlumMe BEST. sim_exhausted.jsonl is evidence only."""
    allow_file = runs_dir / "sim_allowlist.json"
    if not allow_file.exists():
        return []
    dead = _exhausted_providers(runs_dir)
    spent = set()
    if dead and svc is not None:
        keys = {str(o.model_key) for o in svc.store.offers.values()}
        for key in keys:
            serving = {o.provider for o in svc.store.offers.values() if str(o.model_key) == key}
            if serving <= dead:
                spent.add(key)
    return [k for k in sorted(json.loads(allow_file.read_text())["model_keys"]) if k not in spent]


_FIXED_HEART = {}


def _fixed_simulator_reply(log: Path, log_call, messages, model: str):
    from ogi013_codex_heart import CodexHeadlessHeart
    pilot_gate()                                          # pilot only: before every simulator dispatch (a stop is never retried)
    heart = _FIXED_HEART.get(model)
    if heart is None:
        heart = _FIXED_HEART[model] = CodexHeadlessHeart(model, Path(os.environ["PLUMME_STATE_DIR"]) / "receipts.jsonl")
    t0 = time.time()
    lease = asyncio.run(heart.acquire(role_id=ROLE, objective="Simulate a tau2 customer", required_skill_ids=()))
    res = asyncio.run(heart.execute(lease_id=lease["lease_id"], task=_flatten(messages)))
    log_call({"lease_id": lease["lease_id"], "provider_id": lease["provider_id"], "model_id": lease["model_id"], "offer_id": lease["offer_id"], "model_key": f"{model}@fixed"}, res, t0, True)
    if not (res["success"] and res["output"]):
        raise RuntimeError(f"SIM_ROUTE_FAILED:{res['failure_class']}")
    return AssistantMessage(role="assistant", content=res["output"], cost=0.0, usage={"prompt_tokens": res["input_tokens"] or 0, "completion_tokens": res["output_tokens"] or 0})


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
        fixed_sim = os.environ.get("OGI013_SIM_FIXED_MODEL")
        if fixed_sim:                                         # VALIDATION-1: the user simulator is ONE pinned model (ChatGPT headless) for every arm of the cohort: its identity cannot change and no free route can vanish under it
            return _fixed_simulator_reply(log, log_call, messages, fixed_sim)
        # text-only simulator: user-side tools are never offered (telecom-style tasks that need them are out of scope)
        model_key = json.loads(route_file.read_text())["model_key"] if route_file.exists() else None
        pinned = model_key  # the pair's simulator MODEL is fixed; PlumMe may choose any eligible route to that model (pinned_model_key)
        provider = PlumMeProvider(svc)

        pool = [] if model_key else _selection_pool(route_file.parent, svc)
        random.Random(route_file.name).shuffle(pool)       # the order in which allowlisted models are tried for this pair

        async def call(prefer_multi_provider=True, pick=None, total_cap=None):
            from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
            use = model_key or pick
            req = NeuronRequest(consumer="ogi013-sim", objective="Simulate a tau2 customer", role_id=ROLE, cognitive_owner=CognitiveOwner.CONSUMER,
                                selection_mode=SelectionMode.PINNED_MODEL if use else SelectionMode.BEST, pinned_model_key=use,
                                required_skill_ids=[], budget=BudgetEnvelope(max_concurrency=1, max_cost_usd=lease_cash(total_cap)),     # pilot: zero cash is authorised -> PlumMe admits no priced route
                                metadata={"exclude_independence_keys": _single_provider_keys(svc)} if (not use and prefer_multi_provider) else {})
            neuron = await svc.acquire_neuron(req)
            lease = {"lease_id": neuron.lease_id, "provider_id": neuron.route.provider, "model_id": neuron.route.model,
                     "offer_id": neuron.route.offer_id, "model_key": neuron.route.model_key}
            res = await provider.execute(lease_id=lease["lease_id"], task=_flatten(messages), max_output_tokens=None, max_total_tokens=total_cap, max_cost_usd=lease_cash(total_cap))   # PlumMe negotiates the limit (PROTOCOL.md); a fixed 1024 let reasoning models exhaust it with EMPTY_CONTENT finish_reason=length
            return lease, res

        # Route selection (no pinned offer yet) tries alternatives: PlumMe's circuit state steers the next pick away from a failing offer.
        # Once the pair model is fixed, only its route may change (PINNED_MODEL); a model with no eligible route fails the pair.
        last = "NO_ATTEMPT"
        succeeded = False
        keys = [pinned] if pinned else (pool or [])
        idle = 0
        # Never sleeps. A failed call is followed at once by the next eligible route/model (PlumMe's circuit and credential state steer it away from the failing one); a pinned model that has no eligible
        # route left ends this attempt NOW (SIM_ROUTE_FAILED -> whole-block discard, a fresh block selects another model); nothing eligible anywhere is SUPPLY_UNAVAILABLE, reported immediately.
        for attempt in range(8 if pinned else max(12, 2 * len(pool))):
            pilot_gate()                                      # pilot only: before every simulator dispatch attempt (outside the try: a stop must not be retried)
            limits = token_limits()                           # pilot only: the same per-step / headroom bounds the agent steps get, covering the simulator's usage too
            total_cap = None if limits is None else min(limits["per_step"], limits["headroom"])
            if total_cap is not None and total_cap - len(_flatten(messages).encode("utf-8")) < SIM_MIN_ANSWER:
                raise PilotBudgetStop(f"simulator step cannot afford {SIM_MIN_ANSWER} answer tokens (cap {total_cap})")
            t0 = time.time()
            try:
                with step_parent_budget(svc, total_cap, None if limits is None else limits["calls"], account_to=log.parent, who="simulator") as parent:            # pilot: tokens and provider requests of this simulator reply, cont
                    lease, res = asyncio.run(call(prefer_multi_provider=attempt < 3, pick=pool[attempt % len(pool)] if pool else None, total_cap=total_cap))
                    if parent is not None and res["success"]:
                        parent.receipted = True   # soft preference: plain BEST once the resilient set is saturated
            except PilotBudgetStop:                           # a budget stop (also from the step budget) is never retried
                raise
            except Exception as exc:  # noqa: BLE001 - e.g. PinnedWorkerUnavailable: record, never crash the benchmark run
                last = type(exc).__name__
                with log.open("a") as f:
                    f.write(json.dumps({"ts": t0, "pinned": bool(pinned), "exception": last, "detail": str(exc)[:200],
                                        "why": _explain(svc, pinned or (pool[attempt % len(pool)] if pool else ""))}) + "\n")
            else:
                log_call(lease, res, t0, pinned)
                last = res["failure_class"]
                if res["success"] and res["output"]:
                    succeeded = True
                    break
            if keys:
                wait = _earliest_retry(svc, keys)      # 0.0 = a route is eligible right now; anything else is information, never a duration to sit out
                with log.open("a") as f:
                    f.write(json.dumps({"ts": t0, "pinned": bool(pinned), "eligible_now": wait == 0.0, "scope": "pinned" if pinned else "pool"}) + "\n")
                idle = idle + 1 if wait == 0.0 else 0
                if pinned and wait is not None and 0.0 < wait <= PINNED_RETRY_WINDOW_S:
                    time.sleep(wait + 1.0)                     # PlumMe's OWN known short window (circuit/model cooldown) on the only route of the block's pinned model: discarding a block over seconds would throw away finished work. Never an exhausted pool/credential (those have no retry time).
                    continue
                if pinned and (wait != 0.0 or idle >= 3):     # no eligible route (quota, exhausted credential/pool, no credential, long window) or an "available" route that keeps failing: end the attempt now
                    break
                if not pinned and wait != 0.0 and attempt >= len(pool) - 1:
                    last = "SUPPLY_UNAVAILABLE"        # every allowlisted model was tried and none has an eligible route
                    break
        if not succeeded and not pinned:
            last = "SUPPLY_UNAVAILABLE"                 # a whole selection pass over the allowlist produced no answer: nothing is serving the simulator right now (the launcher defers the block, no attempt consumed)
        if not succeeded:
            if pinned:                                  # evidence only (not an exclusion window): which model failed a block, why, and which providers were unusable
                with (route_file.parent / "sim_exhausted.jsonl").open("a") as f:
                    providers = sorted({k.rsplit(":", 1)[0] for k, v in _explain(svc, pinned).items() if isinstance(v, dict) and (v.get("rejected") or not v.get("credential_available", True) or v.get("quota_exhausted"))})
                    f.write(json.dumps({"ts": time.time(), "model_key": pinned, "cause": last, "providers": providers}) + "\n")
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
