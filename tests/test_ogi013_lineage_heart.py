"""LineageHeart (runners/ogi013_lineage_heart.py): the reviewer-lineage exclusion and the author preference actually reach PlumMe, and the route's lineage comes back in the lease.
Fake PlumMe service that honours request.metadata['exclude_independence_keys'] and PINNED_MODEL like PlumMe's scheduler; no network, no model."""
import asyncio
import sys
from types import SimpleNamespace

import pytest

pytest.importorskip("plumme")
pytest.importorskip("peachme")
from ogi013_pilot_fixtures import ROOT

sys.path.insert(0, str(ROOT / "runners"))
from ogi013_lineage_heart import LineageHeart
from peachme import PeachError
from peachme.plumme import PlumMeProvider
from plumme.models import SelectionMode
from plumme.budget import BudgetExceeded


def route(model_key, group, provider="prov"):
    return SimpleNamespace(offer_id=f"offer-{model_key}", model=model_key.split("@")[0], provider=provider, model_key=model_key, independence_group=group, model_family=group, cost_class=SimpleNamespace(value="FREE_TIER"),
                           input_cost_per_million=0.0, output_cost_per_million=0.0, context_window=32000, output_limit_per_response=4096)


class FakePlumMe:
    """BEST = first route whose lineage is not excluded; PINNED_MODEL = that model's route if not excluded. Records every request."""

    def __init__(self, routes, ignore_exclusion=False):
        self.routes, self.requests, self.ignore = routes, [], ignore_exclusion

    async def acquire_neuron(self, req, *, min_context_tokens=None):
        self.requests.append(req)
        self.min_context_tokens = min_context_tokens
        excluded = set(req.metadata.get("exclude_independence_keys") or []) if not self.ignore else set()
        pool = [r for r in self.routes if r.independence_group not in excluded]
        if req.selection_mode == SelectionMode.PINNED_MODEL:
            pool = [r for r in pool if r.model_key == req.pinned_model_key]
        if not pool:
            raise RuntimeError("NO_ELIGIBLE_ROUTE")
        r = pool[0]
        return SimpleNamespace(lease_id=f"lease-{r.model_key}", neuron_id="n1", role_id=req.role_id, cognitive_owner=SimpleNamespace(value="CONSUMER"), effective_skill_ids=[], route=r)


ROUTES = [route("alpha@x", "lineage-alpha"), route("beta@x", "lineage-beta"), route("gamma@x", "lineage-gamma")]


def acquire(heart):
    return asyncio.run(heart.acquire(role_id="REASONING", objective="o", required_skill_ids=()))


def test_the_exclusion_reaches_plumme_and_the_lease_carries_the_lineage():
    svc = FakePlumMe(ROUTES)
    heart = LineageHeart(svc)
    heart.exclude_independence_keys = ("lineage-alpha", None, "")
    lease = acquire(heart)
    assert svc.requests[0].metadata == {"exclude_independence_keys": ["lineage-alpha"]}      # PlumMe's own mechanism (the one CherryMe's bridge uses), empty/None keys dropped
    facts = heart.lease_facts(lease["lease_id"])
    assert facts == {"independence_key": "lineage-beta", "model_key": "beta@x", "prefer_met": None,
                     "cost_class": "FREE_TIER", "input_cost_per_million": 0.0, "output_cost_per_million": 0.0,
                     "context_window": 32000, "output_limit": 4096}
    heart.exclude_independence_keys = ("lineage-alpha", "lineage-beta")
    assert heart.lease_facts(acquire(heart)["lease_id"])["independence_key"] == "lineage-gamma"          # a third lineage when two are used
    assert heart.lease_facts("unknown-lease") == {} and heart.lease_facts(None) == {}


def test_context_floor_is_bound_to_acquisition_and_route_limit_comes_from_the_lease():
    svc = FakePlumMe(ROUTES)
    heart = LineageHeart(svc)
    heart.min_context_tokens = 24000
    lease = acquire(heart)
    assert svc.min_context_tokens == 24000
    assert heart.lease_facts(lease["lease_id"])["output_limit"] == 4096


def test_without_a_lineage_left_the_acquisition_fails_instead_of_reviewing_ones_own_work():
    heart = LineageHeart(FakePlumMe(ROUTES))
    heart.exclude_independence_keys = tuple(r.independence_group for r in ROUTES)
    with pytest.raises(RuntimeError, match="NO_ELIGIBLE_ROUTE"):
        acquire(heart)


def test_a_service_that_returns_an_excluded_lineage_is_refused():
    heart = LineageHeart(FakePlumMe(ROUTES, ignore_exclusion=True))
    heart.exclude_independence_keys = ("lineage-alpha",)
    with pytest.raises(PeachError, match="EXCLUDED_LINEAGE_RETURNED"):
        acquire(heart)


def test_the_authors_model_is_preferred_for_a_revision_and_a_miss_is_recorded():
    svc = FakePlumMe(ROUTES)
    heart = LineageHeart(svc)
    heart.prefer_model_key = "gamma@x"
    lease = acquire(heart)
    facts = heart.lease_facts(lease["lease_id"])
    assert facts["model_key"] == "gamma@x" and facts["prefer_met"] is True and svc.requests[0].selection_mode == SelectionMode.PINNED_MODEL
    heart.prefer_model_key = "missing@x"
    facts = heart.lease_facts(acquire(heart)["lease_id"])
    assert facts["prefer_met"] is False and facts["model_key"] == "alpha@x" and svc.requests[-1].selection_mode == SelectionMode.BEST      # any admissible route, the miss is on record


@pytest.mark.parametrize("error", [BudgetExceeded("call budget exhausted"), type("ParentBudgetExhausted", (RuntimeError,), {})("parent budget exhausted")])
def test_a_budget_refusal_does_not_fall_back_to_another_model(error):
    class BudgetService(FakePlumMe):
        async def acquire_neuron(self, req, *, min_context_tokens=None):
            self.requests.append(req)
            self.min_context_tokens = min_context_tokens
            raise error

    heart = LineageHeart(BudgetService(ROUTES))
    heart.prefer_model_key = "gamma@x"
    with pytest.raises(type(error)):
        acquire(heart)
    assert len(heart.service.requests) == 1
    assert heart.service.requests[0].selection_mode == SelectionMode.PINNED_MODEL


def test_the_lease_keeps_every_field_peachmes_own_provider_returns():
    base = asyncio.run(PlumMeProvider(FakePlumMe(ROUTES)).acquire(role_id="REASONING", objective="o", required_skill_ids=()))
    mine = acquire(LineageHeart(FakePlumMe(ROUTES)))
    assert mine.keys() >= base.keys() and all(mine[k] == v for k, v in base.items())
