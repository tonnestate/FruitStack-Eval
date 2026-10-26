"""Run official tau2-bench tasks with the OGI-013 FruitStack agent and Pomelo tool gate."""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import types
from pathlib import Path

TAU2 = Path(os.environ.get("OGI013_TAU2_ROOT", "/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench"))
sys.path.insert(0, str(TAU2 / "src"))

from tau2.data_model.simulation import TextRunConfig
from tau2.evaluator.evaluator import EvaluationType
from tau2.registry import registry
from tau2.runner import batch
from tau2.runner.helpers import get_tasks

from ogi013_tau2_agent import FruitStackTau2Agent, Stack as FruitStack
from ogi013_run_guard import ensure_empty_output
from pomelome.effects import EffectObservation
from peachme.pomelo import effect_identity


def _host_effects(peach):
    if peach.effects is None:
        raise RuntimeError("POMELOME_HOST_BRIDGE_REQUIRED")
    return peach.effects


class _ToolBridge:
    def __init__(self, env, message):
        self.env, self.message = env, message

    def _call(self):
        result = self.env.make_tool_call(
            self.message.name,
            requestor=self.message.requestor,
            **self.message.arguments,
        )
        self.env.sync_tools()
        return result

    def dispatch(self, intent) -> EffectObservation:
        try:
            return EffectObservation(success=True, data=self._call(), external_ref=self.message.id)
        except Exception as exc:
            return EffectObservation(success=False, data={"error": str(exc)}, external_ref=self.message.id)

    def probe(self, intent) -> EffectObservation | None:
        # τ² tools expose no general idempotency probe; an ambiguous dispatched effect must stay unresolved.
        return None

def _install_agent(out: Path, domain: str):
    def factory(tools, domain_policy, **kwargs):
        task = kwargs.get("task")
        return FruitStackTau2Agent(
            tools, domain_policy, mode=MODE, task=task, domain=domain,
            out=out,
        )
    registry.register_agent_factory(factory, name="ogi013_fruitstack")


def run_one(task_id: str, domain: str, mode: str, out: Path, *, host_effects=None, llm_user=None):
    global MODE
    if mode not in {"single", "fixed", "adaptive"}:
        raise ValueError(f"unsupported OGI-013 mode: {mode}")
    MODE = mode
    out.mkdir(parents=True, exist_ok=True)
    stack = FruitStack.get(out / "fruitstack")
    if host_effects is not None:
        stack.fs.attach_host_effects(**host_effects)
    _host_effects(stack.fs)
    task = next(t for t in get_tasks(domain) if t.id == task_id)
    task_out = out / "tasks" / task_id
    task_out.mkdir(parents=True, exist_ok=True)
    _install_agent(task_out, domain)

    original_build = batch.build_orchestrator
    parent_use = {"tool_calls": 0}

    def build_with_bridge(config, task, **kwargs):
        orchestrator = original_build(config, task, **kwargs)
        env = orchestrator.environment
        agent = orchestrator.agent
        original = env.get_response
        env._ogi013_original_get_response = original

        def mediated(this, message):
            ep = agent.ep
            if ep is None:
                from tau2.data_model.message import ToolMessage
                return ToolMessage(id=message.id, content="Error: Pomelo execution gate is unavailable", requestor=message.requestor, role="tool", error=True)
            parent_use["tool_calls"] += 1
            write = any(t.name == message.name and FruitStackTau2Agent._is_write(t) for t in agent.tools)
            try:
                from pomelome.models import EffectClass

                peach = agent.ep.stack.fs
                effects = _host_effects(peach)
                # The trusted host supplies the bridge, authority, approved plan and budget.
                effects.gateway.adapters[message.name] = _ToolBridge(this, message)
                session = agent.ep.stack.store.get(agent.ep.sid)
                effect_class = EffectClass.IRREVERSIBLE if write else EffectClass.READ
                peach.execute_effect(
                    agent.ep.sid, session.revision, effect_key=message.id,
                    tool=message.name, effect_class=effect_class.value,
                    args=message.arguments,
                    required_capabilities=(f"tool:{message.name}",),
                )
                effect_id = effect_identity(agent.ep.sid, message.id)
                record = effects.gateway.store.get_effect(effect_id)
                observation = record.get("observation") if record else None
                response = observation.get("data") if observation else None
                failed = not observation or observation.get("success") is not True
                if failed and observation:
                    response = observation.get("data") or observation.get("message") or "effect failed"
                content = json.dumps(response, ensure_ascii=False, default=str) if not isinstance(response, str) else response
                from tau2.data_model.message import ToolMessage
                return ToolMessage(id=message.id, content=content, requestor=message.requestor, role="tool", error=failed)
            except Exception as exc:
                ep.event("POMELO_TOOL_ERROR", tool=message.name, error=str(exc)[:300])
                from tau2.data_model.message import ToolMessage
                return ToolMessage(id=message.id, content=f"Error: Pomelo refused or could not reconcile tool call: {exc}", requestor=message.requestor, role="tool", error=True)

        env.get_response = types.MethodType(mediated, env)
        return orchestrator

    batch.build_orchestrator = build_with_bridge
    try:
        config = TextRunConfig(
            domain=domain,
            task_ids=[task_id],
            agent="ogi013_fruitstack",
            llm_agent="FruitStack/PlumMe",
            **({"llm_user": llm_user} if llm_user else {}),
            max_steps=40,
            max_errors=8,
            seed=42,
        )
        result = batch.run_single_task(
            config, task, seed=42, evaluation_type=EvaluationType.ALL,
            save_dir=out / "tau2-logs", verbose_logs=True,
        )
        (task_out / "official-result.json").write_text(result.model_dump_json(indent=2), encoding="utf-8")
        print(json.dumps({"task_id": task_id, "reward": result.reward_info.reward if result.reward_info else None,
                          "pomelo_tool_calls": parent_use["tool_calls"], "result": str(task_out / "official-result.json")}, default=str))
    finally:
        batch.build_orchestrator = original_build


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--mode", choices=["single", "fixed", "adaptive"], required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--host-composer", required=True,
                        help="trusted host module exposing host_effects()")
    parser.add_argument("--llm-user", help="tau2 user-simulator model; hold constant across comparison arms")
    args = parser.parse_args(argv)
    try:
        ensure_empty_output(args.out)
    except FileExistsError as exc:
        parser.error(str(exc))
    os.environ.setdefault("ORANGEME_SOURCE_REPO", str(TAU2))
    composer = importlib.import_module(args.host_composer)
    host_effects = composer.host_effects()
    if not isinstance(host_effects, dict) or set(host_effects) != {
        "gateway", "authority_provider", "plan_provider"
    }:
        raise RuntimeError("HOST_EFFECTS_COMPOSITION_INVALID")
    run_one(args.task, args.domain, args.mode, args.out, host_effects=host_effects, llm_user=args.llm_user)


if __name__ == "__main__":
    main()
