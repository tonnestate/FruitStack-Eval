#!/usr/bin/env python3
"""OGI-013 technical start proof: ONE real mission through the REAL integrated FruitStack in isolated-but-real evaluation state (PEACH-MISSION/1, reused unchanged).

MangoMe (own database, real WorkIdentity + EXECUTE turn) -> PeachMe (session, budget, reflex, egress) -> CherryMe (responsibility graph) -> PlumMe (AUTO supply, zero-charge dispatch, ParentBudget)
-> provider -> PeachMe ledger -> CherryMe consolidation -> AppleMe assurance + reflex signals -> verified knowledge -> MangoMe checkpoint -> OrangeMe ledger entry.
PeachMe's PomeloMe bridge and durable effect ledger are exercised separately with a harmless local adapter; no canonical authorization or external effect is claimed.
Not scientific evidence: a single hand-made claim proves the path, nothing more. State: ogi-013/env.sh (MANGOME_DATABASE=mangome_ogi013_eval, OrangeMe on local bare git ledgers).
Usage: ogi013_stack_proof.py OUT_DIR"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path

from ogi013_run_guard import ensure_empty_output

ACTOR = "claude-code-ogi"


def run_local_pomelo_proof(out: Path, work: str, actor: str = ACTOR) -> dict:
    """Exercise PeachMe's trusted effect bridge against an isolated local tool."""
    from peachme.pomelo import PomeloEffectBridge
    from pomelome import AuthorityEnvelope, EffectClass, EffectGateway
    from pomelome.budget import BudgetEnvelope
    from pomelome.effects import EffectObservation
    from pomelome.ir import EffectNode, ExecutionPlan
    from pomelome.store import SqliteEffectStore

    class LocalProofEffect:
        def dispatch(self, intent):
            return EffectObservation(success=True, external_ref="local-proof:" + intent.effect_id)

        def probe(self, intent):
            return None

    effect_store = SqliteEffectStore(out / "pomelo-effects.sqlite3")
    effect_gateway = EffectGateway(effect_store, {"local_proof": LocalProofEffect()})
    effect_authority = AuthorityEnvelope(
        authority_id=f"ogi013-local-proof:{work}", principal=actor,
        capabilities=frozenset({"tool:local_proof"}),
    )

    def approved_effect(session_id, intent):
        return (
            ExecutionPlan(plan_id="ogi013-local-proof", nodes=[EffectNode(
                id=intent.effect_id, tool=intent.tool,
                effect_class=intent.effect_class, args=intent.args,
                required_capabilities=intent.required_capabilities,
            )]),
            BudgetEnvelope(max_model_calls=0, max_reads=0, max_effects=1,
                           max_parallelism=1, max_cost_usd=0),
        )

    effect_bridge = PomeloEffectBridge(
        effect_gateway, lambda session_id, intent: effect_authority, approved_effect,
    )
    effect_session = "ogi013-proof-" + uuid.uuid4().hex[:8]
    effect = effect_bridge.execute(
        effect_session, effect_key="local-proof", tool="local_proof",
        effect_class=EffectClass.IDEMPOTENT_WRITE.value, args={"work_ref": work},
    )
    effect_record = effect_store.get_effect(effect.effect_id)
    if not effect.dispatched or effect.state != "RECONCILED" or not effect.receipt_id or not effect_record:
        raise RuntimeError("PomeloMe local effect proof was not durably reconciled")
    return {
        "state": effect.state, "dispatched": effect.dispatched,
        "receipt_id": effect.receipt_id, "durable_state": effect_record["state"],
    }


def main(out: Path) -> int:
    ensure_empty_output(out)
    out.mkdir(parents=True, exist_ok=True)
    os.environ["PLUMME_STATE_DIR"] = str(out / "plumme-state")
    (out / "plumme-state" / "knowledge").mkdir(parents=True, exist_ok=True)
    import shutil
    snap = Path("/root/fruits/research/FRUITSTACK-EVAL-004/inputs/models.dev-api.json")
    if snap.exists() and not (out / "plumme-state" / "knowledge" / "models.dev-api.json").exists():
        shutil.copyfile(snap, out / "plumme-state" / "knowledge" / "models.dev-api.json")
    from cherryme.appleme_bridge import connect_appleme
    from cherryme.engine import CherryMeEngine
    from cherryme.knowledge import KnowledgeStore
    from cherryme.models import QuestionType
    from cherryme.orchestrator import ResolutionAwareOrchestrator
    from cherryme.plumme_bridge import connect_plumme
    from cherryme.runtime import responsibility_runtime
    from mangome.runtime import get_service
    from orangeme.runtime import OrangeRuntime
    from peachme import SessionStore
    from peachme.fruitstack import AppleAssuranceAdapter, CherryBrainAdapter, FruitStackSession, MangoWorkAdapter, OrangeMemoryAdapter
    from peachme.mission import MissionAuthority, MissionRequest, run_mission
    from peachme.plumme import PlumMeProvider
    from plumme.config import Settings
    from plumme.credentials import CredentialSource, CredentialSourceKind
    from plumme.service import PlumMeService, default_adapters

    mango = get_service()
    entered = mango.enter_work(workspace_id=f"/ogi013/{uuid.uuid4().hex[:8]}", workspace_title="OGI-013 stack proof", actor_id=ACTOR,
                               request_text="Check one arithmetic claim through the full organization (technical start proof)")
    work, project = entered["work_identity"]["entity_id"], entered["project"]["project_key"]
    ort = OrangeRuntime()
    try:                                                                  # the OrangeMe project carries the MangoMe project key: one reference in both stores
        ort.register_project(project, os.environ["ORANGEME_SOURCE_REPO"], "main", {"vps": os.environ["ORANGEME_SOURCE_REPO"]})
    except Exception:
        pass
    led = ort.project_ledger(project)
    if led.get("memory/working") is None:
        led.put("memory/working", {"verified_findings": []}, expected_revision=0)    # an EMPTY authoritative entry; content only ever arrives as verified findings

    settings = Settings.load()
    svc = PlumMeService(settings, adapters=default_adapters(settings))
    svc.credentials.register_source(CredentialSource("freellmapi", CredentialSourceKind.ENV_REFERENCE, "freellmapi-isolated-instance", {"var": "FLM_KEY"}))
    asyncio.run(svc.discover())

    registry, investigator = connect_plumme(service=svc, refresh=True)
    nodes = [{"id": "SUM", "mandate": "add the numbers and state the total", "skills": ["reasoning"]},
             {"id": "CHECK", "mandate": "re-compute the total independently and judge the claim", "skills": ["falsify"], "function": "VERIFY", "depends_on": ["SUM"]}]
    runtime = responsibility_runtime(tools=(), frame={"responsibility_context": {"responsibilities": nodes}})
    frame = {k: v for k, v in runtime["frame"].items() if k != "responsibility_triage"}
    assurance = connect_appleme(workspace_root=out / "cherry")

    class Falsify:
        def choose(self, claim, state_features):
            return QuestionType.FALSIFY

    engine = CherryMeEngine(workspace_root=out / "cherry", registry=registry, investigator=investigator, assurance_tier=assurance, orchestrator=ResolutionAwareOrchestrator(Falsify()),
                            orchestration_skill=runtime["orchestration_skill"], frame=frame)
    store = SessionStore(out / "peachme.sqlite3")
    rt = FruitStackSession(store, PlumMeProvider(svc), MangoWorkAdapter(mango), OrangeMemoryAdapter(ort), brain=CherryBrainAdapter(engine),
                           assurance=AppleAssuranceAdapter(assurance.service), authorize_model_input=lambda text, view: text)
    authority = MissionAuthority(work_ref=work, project_ref=project, memory_ref="memory/working", actor_id=ACTOR, authorized_by=ACTOR)
    request = MissionRequest(mission_id="ogi013-start-" + uuid.uuid4().hex[:6], objective="Is the sum of 12, 7, 19 and 4 equal to 42?", claims=(("The sum of 12, 7, 19 and 4 equals 42.", 0.5),),
                             budget=2, call_budget=10, session_budget={"max_calls": 14, "max_tokens": 120000, "max_cost_usd": 1.0})
    record = run_mission(rt, authority, request, knowledge_store=KnowledgeStore(out / "knowledge.jsonl"))
    pomelo_effect = run_local_pomelo_proof(out, work)
    (out / "mission_record.json").write_text(json.dumps(record, indent=1, default=str))
    ev = {e["type"]: e for e in record["events"]}
    print(json.dumps({"state": record["state"], "error_code": record["error_code"], "event_types": [e["type"] for e in record["events"]],
                      "accounting": (ev.get("INQUIRY_EXECUTED") or {}).get("accounting"), "assurance": [e.get("health") for e in record["events"] if e["type"] == "ASSURANCE_OBSERVED"],
                      "work_ref": work, "database": os.environ.get("MANGOME_DATABASE"),
                      "pomelo_effect": pomelo_effect}, indent=1, default=str))
    return 0 if record["state"] in ("COMPLETED", "UNRESOLVED") else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
