"""PeachMe's PlumMeProvider plus the two selection facts the collaboration depends on.

Integration defect it removes: Episode.step set `heart.exclude_independence_keys` / `heart.prefer_model_key`, but nothing in PeachMe or PlumMe reads those attributes (PlumMe's scheduler reads
`request.metadata["exclude_independence_keys"]`), so in the live runtime a reviewer could be the author's own lineage. And PeachRuntime.attach() stores only a whitelist of lease fields in the session
environment (no independence_key / model_key), so every step's lineage was None. This subclass puts the exclusion into the NeuronRequest metadata (PlumMe's own mechanism, the one CherryMe's bridge
uses), pins the author's model for a revision when a route exists (any admissible route otherwise, recorded as prefer_met=False) and keeps the route's lineage per lease (`lease_facts`) because PeachMe
will not. PlumMe still decides eligibility, cost class and the route."""
from __future__ import annotations

import threading

from peachme import PeachError
from peachme.plumme import PlumMeProvider


def _per_thread(name, default):
    """Per-step routing attributes are thread-local (parallel organisation): concurrent workers set and read them on their own thread (asyncio.run executes acquire() on the calling thread)."""
    def get(self):
        return getattr(self._tl, name, default)

    def put(self, value):
        setattr(self._tl, name, value)
    return property(get, put)


class LineageHeart(PlumMeProvider):
    exclude_independence_keys = _per_thread("exclude_independence_keys", ())      # set per step by Episode.step
    prefer_model_key = _per_thread("prefer_model_key", None)
    exclude_small_models = _per_thread("exclude_small_models", False)             # lead decision 2026-10-31: applies to all roles (PlumMe narrows eligibility; never widens)
    strict_prefer = _per_thread("strict_prefer", False)                           # roster-pinned calls: no silent handover to another model when the pinned one cannot be leased
    min_context_tokens = _per_thread("min_context_tokens", None)                  # routes that cannot hold the request are not leased (PlumMe screen, request.metadata)

    def __init__(self, service, **kw):
        super().__init__(service, **kw)
        self._tl = threading.local()
        self._facts: dict[str, dict] = {}

    def lease_facts(self, lease_id: str | None) -> dict:
        """Lineage facts of a lease acquired through this heart: independence_key, model_key, prefer_met (None = no preference was asked)."""
        return dict(self._facts.get(lease_id) or {})

    async def acquire(self, *, role_id: str, objective: str, required_skill_ids: tuple[str, ...], max_cost_usd: float | None = None) -> dict:
        from plumme.knowledge import independence_key
        from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
        excluded = sorted({str(k) for k in self.exclude_independence_keys if k})

        def request(pin: str | None):
            return NeuronRequest(consumer="peachme", objective=objective, role_id=role_id, cognitive_owner=CognitiveOwner.CONSUMER,
                                 selection_mode=SelectionMode.PINNED_MODEL if pin else SelectionMode.BEST, pinned_model_key=pin, required_skill_ids=list(required_skill_ids),
                                 budget=BudgetEnvelope(max_concurrency=1, max_cost_usd=max_cost_usd),
                                 metadata={**({"exclude_independence_keys": excluded} if excluded else {}), **({"exclude_small_models": True} if self.exclude_small_models else {}), **({"min_context_tokens": self.min_context_tokens} if self.min_context_tokens else {})})

        lease, prefer_met = None, None
        if self.prefer_model_key:
            try:
                lease, prefer_met = await self.service.acquire_neuron(request(self.prefer_model_key)), True
            except Exception as exc:  # noqa: BLE001 - the preference is soft: no route for that model -> any admissible route, and the miss is recorded
                if self.strict_prefer:      # a roster-pinned call: the miss is a FAILED step, never a silent handover (the roster rule decides after two failed steps)
                    raise PeachError("EXECUTION_NOT_PERFORMED_PINNED_MODEL_UNAVAILABLE") from exc
                lease, prefer_met = None, False
        if lease is None:
            lease = await self.service.acquire_neuron(request(None))
        route = lease.route
        key = independence_key(route)
        if key in excluded:                    # PlumMe must never hand back an excluded lineage; if it does, fail closed instead of reviewing one's own work
            raise PeachError("EXCLUDED_LINEAGE_RETURNED")
        self._facts[lease.lease_id] = {"independence_key": key, "model_key": getattr(route, "model_key", None), "prefer_met": prefer_met}
        return {
            "lease_id": lease.lease_id, "neuron_id": lease.neuron_id, "role_id": lease.role_id, "cognitive_owner": lease.cognitive_owner.value,
            "effective_skill_ids": list(lease.effective_skill_ids), "offer_id": route.offer_id, "model_id": route.model, "provider_id": route.provider,
            "cost_class": getattr(getattr(route, "cost_class", None), "value", getattr(route, "cost_class", None)),
            "input_cost_per_million": getattr(route, "input_cost_per_million", None), "output_cost_per_million": getattr(route, "output_cost_per_million", None),
            "context_window": getattr(route, "context_window", None),
            "output_limit": getattr(route, "output_limit_per_response", None) or getattr(route, "max_output_tokens", None),
        }
