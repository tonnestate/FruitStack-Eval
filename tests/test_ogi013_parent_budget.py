"""QA-1 outage fix: the parent budget is per execution context (real SwarmScheduler + real step_parent_budget), and a budget refusal is never reported as an unavailable pinned model."""
import asyncio
import sys
import threading
import time
from contextvars import ContextVar
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
from ogi013_lineage_heart import LineageHeart  # noqa: E402
from ogi013_pilot_gate import step_parent_budget  # noqa: E402
from plumme.budget import ParentBudgetExhausted  # noqa: E402
from plumme.scheduler import SwarmScheduler  # noqa: E402


class Svc:                                          # PlumMeService's set_parent_budget / parent_budget / acquire-time check on the real scheduler slot
    def __init__(self):
        self.scheduler = SwarmScheduler.__new__(SwarmScheduler)
        self.scheduler._parent_budget = ContextVar(f"plumme_parent_budget_test_{id(self)}", default=None)

    def set_parent_budget(self, p):
        self.scheduler.parent_budget = p

    @property
    def parent_budget(self):
        return getattr(self.scheduler, "parent_budget", None)

    async def acquire(self):
        p = self.parent_budget
        cause = p.exhausted() if p is not None else None
        if cause:
            raise ParentBudgetExhausted(cause)
        if p is not None:
            p.reserve(500, 500)
        return p


def _step(svc, out, name, calls, n, hang=None):
    try:
        with step_parent_budget(svc, 100_000, calls, who=name) as own:
            for _ in range(n):
                assert asyncio.run(svc.acquire()) is own, f"{name}: saw another step's budget"
            if hang:
                hang.wait(5)
        out[name] = "ok"
    except ParentBudgetExhausted as exc:
        out[name] = f"refused {exc}"


def test_hung_step_does_not_block_later_steps():
    svc, out, hang = Svc(), {}, threading.Event()
    t = threading.Thread(target=_step, args=(svc, out, "hung", 2, 1, hang), daemon=True)
    t.start()
    time.sleep(0.1)
    for name in ("S", "E", "T2", "S2", "T1"):
        th = threading.Thread(target=_step, args=(svc, out, name, 10, 3))
        th.start()
        th.join()
    hang.set()
    t.join(2)
    assert all(out[n] == "ok" for n in ("S", "E", "T2", "S2", "T1")), out


def test_concurrent_steps_each_run_under_their_own_budget():
    svc, out = Svc(), {}
    ths = [threading.Thread(target=_step, args=(svc, out, f"w{i}", 3, 3)) for i in range(8)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    assert len(out) == 8 and all(v == "ok" for v in out.values()), out


def test_step_budget_is_still_enforced():
    svc, out = Svc(), {}
    th = threading.Thread(target=_step, args=(svc, out, "over", 2, 3))
    th.start()
    th.join()
    assert out["over"].startswith("refused"), out


def test_enclosing_budget_stays_in_charge_within_one_context():
    svc = Svc()
    with step_parent_budget(svc, 100_000, 5, who="outer") as outer:
        with step_parent_budget(svc, 100_000, 1, who="inner") as inner:
            assert inner is None and svc.parent_budget is outer
    assert svc.parent_budget is None


class _Refusing:
    def __init__(self, exc):
        self.exc = exc

    async def acquire_neuron(self, request):
        raise self.exc


def _heart(exc):
    h = LineageHeart(_Refusing(exc))
    h.prefer_model_key, h.strict_prefer = "m@default", True
    return h


def test_budget_refusal_is_not_reported_as_unavailable_pinned_model():
    with pytest.raises(ParentBudgetExhausted):
        asyncio.run(_heart(ParentBudgetExhausted("calls")).acquire(role_id="r", objective="o", required_skill_ids=()))


def test_missing_route_is_still_a_pinned_model_unavailable_step():
    from peachme import PeachError
    with pytest.raises(PeachError, match="PINNED_MODEL_UNAVAILABLE"):
        asyncio.run(_heart(RuntimeError("NO_EQUIVALENT_ROUTE")).acquire(role_id="r", objective="o", required_skill_ids=()))
