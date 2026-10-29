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

SIM_MIN_ANSWER = 512   # pilot: the customer simulator's replies are short; a step that cannot afford this much answer is a budget stop, never a truncated reply

MAX_WAIT_S = float(os.environ.get("OGI013_SIM_MAX_WAIT_S", "900"))   # (COLLAB-1 launcher sets 120: a pinned simulator route that is cooling down longer than that ends the block attempt promptly - SIM_ROUTE_FAILED, whole-block discard, PlumMe selects another model - instead of waiting ~10 minutes per reply)  # longest cooldown worth waiting for inside a block: PlumMe credential cooldowns of ~600 s were observed (Groq); a daily quota reset is far beyond it


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


def _selection_pool(runs_dir: Path) -> list[str]:
    """Models that may carry a new pair: the live-verified allowlist (sim_allowlist.json, from a real capacity survey) minus models recorded as quota-exhausted within the
    recent failures (sim_exhausted.jsonl, written when a pinned model failed a block; excluded until PlumMe's own retry window ends, else one hour). Empty = no allowlist, plain PlumMe BEST. The ROUTE is always PlumMe's choice."""
    allow_file, spent_file = runs_dir / "sim_allowlist.json", runs_dir / "sim_exhausted.jsonl"
    if not allow_file.exists():
        return []
    spent = set()
    if spent_file.exists():
        for line in spent_file.read_text().splitlines():
            row = json.loads(line) if line.strip() else {}
            if time.time() < row.get("until", row.get("ts", 0) + 3600):      # rows without a recorded window (older format) count for one hour only
                spent.add(str(row["model_key"]))
    return [k for k in sorted(json.loads(allow_file.read_text())["model_keys"]) if k not in spent]


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

        pool = [] if model_key else _selection_pool(route_file.parent)
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
        for attempt in range(60 if pinned else max(12, 2 * len(pool))):
            pilot_gate()                                      # pilot only: before every simulator dispatch attempt (outside the try: a stop must not be retried)
            limits = token_limits()                           # pilot only: the same per-step / headroom bounds the agent steps get, covering the simulator's usage too
            total_cap = None if limits is None else min(limits["per_step"], limits["headroom"])
            if total_cap is not None and total_cap - len(_flatten(messages).encode("utf-8")) < SIM_MIN_ANSWER:
                raise PilotBudgetStop(f"simulator step cannot afford {SIM_MIN_ANSWER} answer tokens (cap {total_cap})")
            t0 = time.time()
            failed_wait = None
            try:
                with step_parent_budget(svc, total_cap, None if limits is None else limits["calls"], account_to=log.parent, who="simulator") as parent:            # pilot: tokens and provider requests of this simulator reply, continuations and retries included
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
                failed_wait = 5
            # PlumMe's own cooldown/quota state decides what happens next: a short window is waited out exactly, a long one (daily quota) fails the block now (registered discard).
            # While SELECTING a model, a model with no route at all is simply skipped (the next pool model is tried); the whole pool being cooled down beyond the window fails the block.
            if keys:
                wait = _earliest_retry(svc, keys)
                with log.open("a") as f:
                    f.write(json.dumps({"ts": t0, "pinned": bool(pinned), "earliest_retry_s": wait, "scope": "pinned" if pinned else "pool"}) + "\n")
                idle = idle + 1 if wait == 0.0 else 0
                if pinned and (wait is None or wait > MAX_WAIT_S or idle >= 3):     # an "available" route that still cannot be acquired three times in a row is not recovering
                    break
                if not pinned and wait is not None and wait > MAX_WAIT_S and attempt >= len(pool) - 1:
                    break
                failed_wait = (wait + 2) if wait is not None else (failed_wait or 1)
            time.sleep(failed_wait if failed_wait is not None else 10)
        if not succeeded:
            if pinned:                                  # remember the model until its retry window ends so the re-selection of the discarded block does not pick it again
                with (route_file.parent / "sim_exhausted.jsonl").open("a") as f:
                    window = _earliest_retry(svc, pinned)
                    f.write(json.dumps({"ts": time.time(), "model_key": pinned, "cause": last, "until": time.time() + (window if window else 3600)}) + "\n")      # (was outside the with: ValueError on a closed file)
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
