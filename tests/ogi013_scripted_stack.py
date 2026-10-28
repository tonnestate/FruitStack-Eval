"""Scripted FruitStack for the integrated-runtime tests: the REAL Episode, FruitStackTau2Agent, FruitStackSession, SessionStore, BudgetGovernance, LineageHeart, collaborate() and CherryMe's Brother Mode;
only the model providers are scripted (a fake PlumMe service that honours lineage exclusion / pinning like PlumMe's scheduler and returns receipts with usage and a route cost class). Zero network."""
import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from ogi013_pilot_fixtures import ROOT

sys.path.insert(0, str(ROOT / "runners"))
from ogi013_lineage_heart import LineageHeart  # noqa: E402
from peachme import SessionStore  # noqa: E402
from peachme.fruitstack import FruitStackSession, MangoWorkAdapter, OrangeMemoryAdapter  # noqa: E402
from plumme.models import SelectionMode  # noqa: E402

BAD = {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"}}
GOOD = {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"}}
J = json.dumps
NONE_WITH_GROUNDS = "ISSUES: NONE\nPolicy: refund window 24h, booked 2h ago -> eligible. HAT001 is the reservation in the CONVERSATION."
FOUND = "ISSUES: FOUND\nWRONG1 is not the customer's booking; the CONVERSATION names HAT001. Cancel HAT001."


def stage_of(task: str) -> str:
    if "A colleague criticised it" in task:
        return "revise"
    if "A colleague proposed this solution" in task:
        return "challenge"
    if "additional specialist" in task:
        return "specialist"
    if "not a single valid JSON object" in task:
        return "format"
    return "draft"


def route(model_key, lineage, cost_class="FREE_TIER", price=0.0):
    return SimpleNamespace(offer_id=f"offer-{model_key}", model=model_key.split("@")[0], provider=f"prov-{lineage}", model_key=model_key, independence_group=lineage, model_family=lineage,
                           cost_class=SimpleNamespace(value=cost_class), input_cost_per_million=price, output_cost_per_million=price, context_window=32000, output_limit_per_response=4096)


POOL = [route("alpha@x", "L-alpha"), route("beta@x", "L-beta"), route("gamma@x", "L-gamma"), route("delta@x", "L-delta")]


class ScriptedPlumMe:
    """Stands in for PlumMeService. `script[stage]` is consumed in order: a str = success with usage; {"nousage": str} = success without usage; {"fail": CLASS} = rejected before processing;
    {"timeout": True} = uncertain failure; an exhausted list repeats nothing and fails (RATE_LIMITED). Records every request and every execution."""

    def __init__(self, script, routes=POOL, tokens_per_call=(400, 100)):
        self.script = {k: list(v) for k, v in script.items()}
        self.routes, self.requests, self.executed, self.leases, self.n = routes, [], [], {}, 0
        self.tokens_per_call = tokens_per_call

    async def acquire_neuron(self, req):
        self.requests.append(req)
        excluded = set(req.metadata.get("exclude_independence_keys") or [])
        pool = [r for r in self.routes if r.independence_group not in excluded]
        if req.selection_mode == SelectionMode.PINNED_MODEL:
            pool = [r for r in pool if r.model_key == req.pinned_model_key]
        if not pool:
            raise RuntimeError("NO_ELIGIBLE_ROUTE")
        self.n += 1
        lease = SimpleNamespace(lease_id=f"lease-{self.n}", neuron_id=f"n{self.n}", role_id=req.role_id, cognitive_owner=SimpleNamespace(value="CONSUMER"), effective_skill_ids=[], route=pool[0])
        self.leases[lease.lease_id] = lease
        return lease

    async def execute_lease(self, ex):
        route_ = self.leases[ex.lease_id].route
        stage = stage_of(ex.task)
        queue = self.script.get(stage, [])
        item = queue.pop(0) if queue else {"fail": "RATE_LIMITED"}
        self.executed.append({"stage": stage, "model_key": route_.model_key, "lineage": route_.independence_group, "task": ex.task, "item": item})
        rid = f"rcpt-{len(self.executed)}"
        tin, tout = self.tokens_per_call
        if isinstance(item, dict) and "fail" in item:
            return SimpleNamespace(success=False, output=None, receipt=SimpleNamespace(receipt_id=rid, model=route_.model, usage=None), route_attempts=[{"failure_class": item["fail"]}], no_equivalent_route=False,
                                   verification="NOT_VERIFIED", failure_class=item["fail"], execution_certainty="NOT_EXECUTED")
        if isinstance(item, dict) and item.get("timeout"):
            return SimpleNamespace(success=False, output=None, receipt=SimpleNamespace(receipt_id=rid, model=route_.model, usage=None), route_attempts=[{"failure_class": "TIMEOUT"}], no_equivalent_route=False,
                                   verification="NOT_VERIFIED", failure_class="TIMEOUT", execution_certainty="UNCERTAIN")
        text = item["nousage"] if isinstance(item, dict) else item
        usage = SimpleNamespace(input_tokens=None, output_tokens=None, cost_usd=None) if isinstance(item, dict) else SimpleNamespace(input_tokens=tin, output_tokens=tout, cost_usd=0.0)
        return SimpleNamespace(success=True, output=text, receipt=SimpleNamespace(receipt_id=rid, model=route_.model, usage=usage), route_attempts=[{"failure_class": None}], no_equivalent_route=False,
                               verification="NOT_VERIFIED", failure_class=None, execution_certainty="EXECUTED")


class FakeMango:
    def session_restore(self, project_ref):
        return {"restore_state": "STATE_FOUND", "productive_execution_allowed": False, "next_executable_items": []}

    def work_context(self, ref):
        return {"work": {"entity_id": ref}}

    def __init__(self):
        self.store = SimpleNamespace(get=lambda table, turn_id: {"work_id": "work-1", "actor_id": "worker:test", "status": "BOUND", "mode": "EXECUTE"})


class FakeOrange:
    def project_ledger(self, project):
        return SimpleNamespace(get=lambda key: {"revision": 3, "event": "PE-3", "value": {"decisions": []}})


class FakeApple:
    def evaluate(self, assurance_id):
        return SimpleNamespace(health_state=SimpleNamespace(value="HEALTHY"))


class ScriptedStack:
    """The `Stack` the agent expects (store, fs, heart, appleme, project(), svc) built on real PeachMe parts."""

    def __init__(self, tmp: Path, script, routes=POOL, tokens_per_call=(400, 100)):
        self.svc = ScriptedPlumMe(script, routes, tokens_per_call)
        self.store = SessionStore(tmp / "peachme.sqlite3")
        self.heart = LineageHeart(self.svc)
        self.fs = FruitStackSession(self.store, self.heart, MangoWorkAdapter(FakeMango()), OrangeMemoryAdapter(FakeOrange(), project_ref="project-1"), assurance=FakeApple(),
                                    authorize_model_input=lambda text, view: text)
        self.appleme = SimpleNamespace(start_run=lambda **kw: SimpleNamespace(target_run_id="run-1", assurance_id="assurance-1"),
                                       observe_event=lambda **kw: SimpleNamespace(health_state="HEALTHY", recommendation="CONTINUE"), finish_run=lambda **kw: None)

    def project(self, workspace):
        return "work-1", "project-1", "turn-1"


def make_agent(monkeypatch, tmp: Path, script, *, mode="rg2", collab=True, budget=None, routes=POOL, tokens_per_call=(400, 100)):
    """The real FruitStackTau2Agent on a scripted stack. budget = (max_calls, max_tokens, max_cost_usd) as the pilot configures PeachMe's session budget."""
    from tau2.environment.tool import as_tool
    from tau2.environment.toolkit import ToolType, is_tool

    import ogi013_tau2_agent as agent_mod

    @is_tool(ToolType.READ)
    def get_reservation_details(reservation_id: str) -> str:
        """Get the details of a reservation.

        Args:
            reservation_id: The reservation id.

        Returns:
            The reservation details.
        """
        return "{}"

    @is_tool(ToolType.WRITE)
    def cancel_reservation(reservation_id: str) -> str:
        """Cancel a reservation.

        Args:
            reservation_id: The reservation id.

        Returns:
            The result.
        """
        return "{}"

    stack = ScriptedStack(tmp, script, routes, tokens_per_call)
    monkeypatch.setenv("OGI013_ACTOR_ID", "worker:test")
    monkeypatch.setenv("OGI013_ORG_COLLAB", "1") if collab else monkeypatch.delenv("OGI013_ORG_COLLAB", raising=False)
    for k in ("OGI013_ORG_ECONOMY", "OGI013_PILOT_BUDGET", "OGI013_SESSION_MAX_CALLS", "OGI013_SESSION_MAX_TOKENS", "OGI013_SESSION_MAX_COST_USD"):
        monkeypatch.delenv(k, raising=False)
    if budget:                                                        # the pilot's own configuration: PeachMe session ceilings AND the pre-dispatch gate (over an empty provider ledger)
        from ogi013_pilot_fixtures import BUDGET, PILOT
        runs = tmp / "runs"
        runs.mkdir(exist_ok=True)
        (runs / "budget.json").write_text(json.dumps(BUDGET))
        for k, v in {"OGI013_PILOT_BUDGET": str(runs / "budget.json"), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"), "OGI013_PILOT_RUNS": str(runs),
                     "OGI013_PILOT_ARMS": "pilot-1/single,pilot-1/collab", "OGI013_PILOT_ARM": "pilot-1/collab" if mode == "rg2" else "pilot-1/single", "OGI013_PILOT_START": "9999999999"}.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setenv("OGI013_SESSION_MAX_CALLS", str(budget[0]))
        monkeypatch.setenv("OGI013_SESSION_MAX_TOKENS", str(budget[1]))
        monkeypatch.setenv("OGI013_SESSION_MAX_COST_USD", str(budget[2]))
    monkeypatch.setattr(agent_mod.Stack, "get", classmethod(lambda cls, out: stack))
    out = tmp / "task"
    out.mkdir(parents=True, exist_ok=True)
    agent = agent_mod.FruitStackTau2Agent([as_tool(get_reservation_details), as_tool(cancel_reservation)], "POLICY: refunds only within 24h.", mode=mode, task=SimpleNamespace(id="24"), domain="airline", out=out)
    state = agent.get_init_state()
    return agent, state, stack, out


def say(agent, state, text="Please cancel flight HAT001, I booked it 2 hours ago."):
    """One agent turn on a customer message; returns (action dict, state)."""
    from tau2.data_model.message import UserMessage
    msg, state = agent.generate_next_message(UserMessage(role="user", content=text), state)
    if msg.tool_calls:
        return {"action": "tool", "name": msg.tool_calls[0].name, "arguments": msg.tool_calls[0].arguments}, state
    return {"action": "message", "content": msg.content}, state


def events(out: Path):
    f = out / "fruitstack-events.jsonl"
    return [json.loads(line) for line in f.read_text().splitlines()] if f.is_file() else []
