#!/usr/bin/env python3
"""Readiness gate G3: attempt a paid route through PlumMe's real execution path and
show that it is denied, without any billable provider call.

Harness code, not part of the evaluator: it imports the installed PlumMe on the host
that runs the arms. The evaluator (`fse`) only reads what this script writes.

What it does, with the host's own environment (PLUMME_COST_POLICY, adapters, skills):

1. Records PlumMe's version and install location and the read-only `doctor` verdict
   for the cost policy.
2. Adds a synthetic paid probe offer (`cost_class=PREMIUM`, endpoint
   `https://paid-probe.invalid`) next to the host's real adapters. The probe adapter
   never opens a network connection; it only counts calls.
3. Discovers supply and, for every non-free offer (the probe and any real paid offer),
   asks the one hard-eligibility gate for its verdict and attempts a PINNED
   acquisition. Acquisition creates a local lease only and never calls a provider;
   if it ever succeeds, the lease is discarded unexecuted and the check fails.
4. Runs one unpinned request through the scheduler's fan with only probe offers: the
   free probe offer fails on purpose, so a leaking guard would fall back to the paid
   probe. The paid probe must receive zero calls.
5. Positive control: the same request under policy ANY must reach the paid probe.
   This proves the probe can detect a leak. It is synthetic and bills nothing.

By default the probe uses a fresh temporary state directory, so the production
DecisionLog and credential store are not touched; `--production-credentials` reads
the production credential store so real paid offers are discovered and screened too.

Exit code 0 only if every check passes. Output: <out>/g3_probe.json and the probe's
DecisionLog at <out>/state/decisions.jsonl for `fse costaudit`.
"""
from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

FREE = {"ANONYMOUS_FREE", "FREE_TIER"}
PROBE_PAID_MODEL = "fse-g3-paid-probe"
PROBE_FREE_MODEL = "fse-g3-free-probe"
SCHEMA = "FSE-G3-PROBE/1"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_probe_adapter():
    from plumme.adapters.base import AdapterError, AdapterResult, ProviderAdapter
    from plumme.models import AuthMode, CostClass, ExecutionProtocol, GroundingCapability, RouteOffer, Usage

    class PaidProbeAdapter(ProviderAdapter):
        """Synthetic supply: one PREMIUM offer and one FREE_TIER offer that always fails."""

        name = "fse-g3-probe"
        priority = 99

        def __init__(self) -> None:
            self.calls: list[str] = []

        def _offer(self, model: str, cost_class) -> RouteOffer:
            return RouteOffer(
                adapter=self.name, source_id=self.name, provider="fse-g3-probe", model=model,
                model_family=f"probe-{model}", endpoint="https://paid-probe.invalid/v1", cost_class=cost_class,
                auth_mode=AuthMode.KEYLESS, execution_protocol=ExecutionProtocol.OPENAI_CHAT,
                supports_text_generation=True, context_window=32000, max_output_tokens=512,
                supports_tools=False, supports_vision=False, grounding=GroundingCapability.NONE,
                tags=["fse-g3-probe"],
            )

        async def discover(self, credential=None):
            return [self._offer(PROBE_PAID_MODEL, CostClass.PREMIUM), self._offer(PROBE_FREE_MODEL, CostClass.FREE_TIER)]

        async def execute(self, offer, messages, max_output_tokens, credential):
            self.calls.append(offer.model)
            if offer.model == PROBE_FREE_MODEL:
                raise AdapterError("PROVIDER_UNAVAILABLE", "probe: free offer fails on purpose to force a fallback")
            # Reaching this line means a paid route was selected. Nothing is sent anywhere.
            return AdapterResult(text="PAID PROBE REACHED", usage=Usage(input_tokens=1, output_tokens=1, total_tokens=2),
                                 provider_request_id=f"paid-probe-{len(self.calls)}", metadata={"probe": True})

    return PaidProbeAdapter()


def isolated_settings(base, state_dir: Path, *, keep_credentials: bool, cost_policy: str | None = None):
    state_dir.mkdir(parents=True, exist_ok=True)
    changes = dict(state_dir=state_dir, receipt_file=state_dir / "receipts.jsonl",
                   decision_log=state_dir / "decisions.jsonl")
    if not keep_credentials:
        changes["credential_db"] = state_dir / "credentials.enc.json"
    if cost_policy is not None:
        changes["cost_policy"] = cost_policy
    return dataclasses.replace(base, **changes)


class Checks:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, name: str, passed: bool, *, required: bool = True, **detail) -> bool:
        self.items.append({"check": name, "passed": bool(passed), "required": required, **detail})
        label = ("PASS" if passed else "FAIL") if required else ("INFO+" if passed else "INFO-")
        print(f"[{label}] {name}", file=sys.stderr)
        return passed


async def probe_pinned(service, checks: Checks, probe, *, include_real: bool) -> None:
    from plumme.models import BudgetEnvelope, ExecutionRequest, NeuronRequest, SelectionMode

    offers = await service.store.discover()
    by_id = {o.offer_id: o for o in offers}
    paid = [o for o in offers if str(getattr(o.cost_class, "value", o.cost_class)) not in FREE]
    if not include_real:
        paid = [o for o in paid if o.model == PROBE_PAID_MODEL]
    census = sorted({(o.adapter, str(getattr(o.cost_class, "value", o.cost_class))) for o in offers})
    checks.add("SUPPLY_DISCOVERED_WITH_PROBE", any(o.model == PROBE_PAID_MODEL for o in offers),
               offers=len(offers), adapters_and_cost_classes=[list(x) for x in census])
    request = ExecutionRequest(task="fse g3 cost probe", role_id="REASONING", consumer="fse-g3-probe")
    eligible, rejected = service.scheduler.screen(request)
    eligible_ids = {o.offer_id for o in eligible}
    for offer in paid:
        cost_class = str(getattr(offer.cost_class, "value", offer.cost_class))
        reasons = rejected.get(offer.offer_id, [])
        expected = f"COST_CLASS_{cost_class}_NOT_ALLOWED"
        checks.add("GATE_REJECTS_PAID_OFFER", offer.offer_id not in eligible_ids and expected in reasons,
                   offer_id=offer.offer_id, adapter=offer.adapter, model=offer.model, cost_class=cost_class,
                   gate_reasons=reasons)
        outcome = {"offer_id": offer.offer_id}
        try:
            lease = await service.acquire_neuron(NeuronRequest(
                consumer="fse-g3-probe", objective="fse g3 cost probe", role_id="REASONING",
                selection_mode=SelectionMode.PINNED, pinned_offer_hint=offer.offer_id,
                budget=BudgetEnvelope(max_calls=1, max_output_tokens=16, max_concurrency=1)))
            outcome.update(acquired=True, lease_id=lease.lease_id, executed=False)
        except Exception as exc:  # the expected path: the pinned paid worker is unavailable
            outcome.update(acquired=False, error_type=type(exc).__name__, error=str(exc)[:300])
        checks.add("PINNED_PAID_ACQUISITION_DENIED", not outcome["acquired"], **outcome)
    checks.add("PAID_PROBE_NEVER_CALLED_PINNED", probe.calls.count(PROBE_PAID_MODEL) == 0, probe_calls=list(probe.calls))
    # Informational (gate G5, not G3): PlumMe versions after 37bfc3e also write the refusal
    # into the DecisionLog as a PINNED_DENIED decision with the gate's reasons.
    recorded = [d for d in service.scheduler.decisions.decisions.values()
                if getattr(d, "selector_name", None) == "PINNED_DENIED"]
    covered = {o.offer_id for o in paid if any(o.offer_id in d.hard_rejected for d in recorded)}
    checks.add("REFUSAL_RECORDED_IN_DECISIONLOG", bool(paid) and covered == {o.offer_id for o in paid},
               required=False, recorded_refusals=len(recorded), paid_offers=len(paid))
    _ = by_id


async def probe_fallback(settings, checks: Checks, *, positive_control: bool) -> dict:
    from plumme.models import BudgetEnvelope, ExecutionRequest
    from plumme.service import PlumMeService

    probe = build_probe_adapter()
    service = PlumMeService(settings, adapters=[probe])
    await service.store.discover()
    result = await service.scheduler.fan(
        ExecutionRequest(task="fse g3 fallback probe", role_id="REASONING", consumer="fse-g3-probe",
                         budget=BudgetEnvelope(max_calls=4, max_output_tokens=16, max_concurrency=1)), width=1)
    paid_calls = probe.calls.count(PROBE_PAID_MODEL)
    info = {"policy": settings.cost_policy, "probe_calls": list(probe.calls), "completed": result.completed,
            "selection_reason": result.selection_reason}
    if positive_control:
        checks.add("POSITIVE_CONTROL_ANY_REACHES_PAID_PROBE", paid_calls >= 1, **info)
    else:
        checks.add("FALLBACK_NEVER_REACHES_PAID_PROBE", paid_calls == 0, **info)
    return info


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", required=True, help="evidence directory (created)")
    ap.add_argument("--production-credentials", action="store_true",
                    help="read the production credential store so real paid offers are screened too")
    ap.add_argument("--no-real-adapters", action="store_true",
                    help="probe adapter only (for environments without provider access)")
    args = ap.parse_args(argv)

    import plumme
    from plumme.config import Settings
    from plumme.diagnostics import doctor
    from plumme.service import PlumMeService, default_adapters

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    base = Settings.load()
    checks = Checks()
    checks.add("COST_POLICY_FREE_ONLY_ACTIVE", base.cost_policy == "FREE_ONLY", configured=base.cost_policy,
               source="PLUMME_COST_POLICY")
    report = doctor(base)
    cost_check = next((c.as_dict() for c in report.checks if c.name == "cost policy"), None)
    checks.add("DOCTOR_COST_POLICY_PASS", bool(cost_check) and cost_check["status"] == "PASS", doctor=cost_check)

    settings = isolated_settings(base, out / "state", keep_credentials=args.production_credentials)
    probe = build_probe_adapter()
    adapters = ([] if args.no_real_adapters else default_adapters(settings)) + [probe]
    try:
        service = PlumMeService(settings, adapters=adapters)
    except Exception as exc:
        checks.add("SERVICE_STARTS_WITH_HOST_CONFIGURATION", False, error=f"{type(exc).__name__}: {exc}"[:400])
        service = None
    if service is not None:
        asyncio.run(probe_pinned(service, checks, probe, include_real=not args.no_real_adapters))
        fallback_settings = isolated_settings(base, out / "state-fallback", keep_credentials=False)
        asyncio.run(probe_fallback(fallback_settings, checks, positive_control=False))
    control_settings = isolated_settings(base, out / "state-positive-control", keep_credentials=False, cost_policy="ANY")
    asyncio.run(probe_fallback(control_settings, checks, positive_control=True))

    passed = all(c["passed"] for c in checks.items if c.get("required", True))
    evidence = {
        "schema": SCHEMA,
        "recorded_at": _now(),
        "seconds": round(time.time() - t0, 2),
        "passed": passed,
        "plumme": {"version": plumme.__version__, "module": str(Path(plumme.__file__).resolve().parent)},
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "host": platform.node(),
        "mode": {"production_credentials": args.production_credentials, "real_adapters": not args.no_real_adapters},
        "env_keys": sorted(k for k in os.environ if k.startswith("PLUMME_")),
        "checks": checks.items,
        "decision_logs": {"pinned_probe": str(out / "state" / "decisions.jsonl"),
                          "fallback_probe": str(out / "state-fallback" / "decisions.jsonl"),
                          "positive_control": str(out / "state-positive-control" / "decisions.jsonl")},
        "billing": "no provider call is made for a paid offer; the paid probe endpoint is .invalid and never contacted",
    }
    (out / "g3_probe.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "evidence": str(out / "g3_probe.json")}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
