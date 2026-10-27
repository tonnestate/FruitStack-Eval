"""OGI-013 trusted host composer for the tau2 sandbox (isolated eval state, no external effects).

Same pattern as ogi013_stack_proof.run_local_pomelo_proof: a per-effect AuthorityEnvelope and single-effect
plan bound to the requesting tool. Scope: tau2 benchmark tools only; the DB path comes from OGI013_EFFECT_DB.
Not a canonical MangoMe authorization.
"""
from __future__ import annotations

import os
from pathlib import Path

ACTOR = os.environ.get("ORANGEME_AGENT_ID", "claude-code-ogi")


def host_effects() -> dict:
    from pomelome import AuthorityEnvelope, EffectGateway
    from pomelome.budget import BudgetEnvelope
    from pomelome.ir import EffectNode, ExecutionPlan
    from pomelome.store import SqliteEffectStore

    db = Path(os.environ["OGI013_EFFECT_DB"])
    db.parent.mkdir(parents=True, exist_ok=True)
    gateway = EffectGateway(SqliteEffectStore(db), {})

    def authority(session_id, intent):
        return AuthorityEnvelope(
            authority_id=f"ogi013-tau2:{session_id}", principal=ACTOR,
            capabilities=frozenset({f"tool:{intent.tool}", f"effect:{str(getattr(intent.effect_class, 'value', intent.effect_class)).lower()}"}),
        )

    def plan(session_id, intent):
        return (
            ExecutionPlan(plan_id=f"ogi013-tau2:{intent.effect_id}", nodes=[EffectNode(
                id=intent.effect_id, tool=intent.tool, effect_class=intent.effect_class,
                args=intent.args, required_capabilities=intent.required_capabilities,
            )]),
            BudgetEnvelope(max_model_calls=0, max_reads=1, max_effects=1,
                           max_parallelism=1, max_cost_usd=0),
        )

    return {"gateway": gateway, "authority_provider": authority, "plan_provider": plan}
