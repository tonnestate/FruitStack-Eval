"""OGI-013 RG/2 bridge: a consequential tau2 decision becomes a CherryMe claim and CherryMe's own engine organises the work.

Reuse only (no second engine): CherryMeEngine under responsibility_runtime() (RG/2 graph, triage 'auto', competence-based staffing, independent
verification, recovery, contribution ledger), PlumMe via connect_plumme (AUTO supply), PeachMe BudgetedPlumMeService (session accounting for every child call),
EvidenceVerifier (quote-checked PASS/CONTRADICT against host-hashed excerpts), optional KnowledgeStore (persistence across decisions/tasks).

Claim: "<action> follows the policy and is justified by the customer's request and the observed system data."
Grounding (host-supplied, hash-checked): policy chunks, the conversation tail, tool results the environment returned. A model never supplies a source.
How many workers a decision gets is decided by the engine (triage/need/conflict), not by this module. This module only decides WHETHER a decision is put
to the engine (consequential effect, or an alert from an earlier dissent/failure) and what to do with the outcome (see Verdict)."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

CHUNK = 5800                      # RetrievedSource excerpts are limited to 6000 characters by CherryMe
MAX_SOURCES = 12                  # HostGrounding limit
QUESTIONS_PER_DECISION = 8        # engine question budget for one claim; the engine stops earlier when the claim is resolved


def _chunks(text: str, size: int = CHUNK) -> list[str]:
    text = text.strip()
    return [text[i:i + size] for i in range(0, len(text), size)] if text else []


def environment_sources(task_id: str, policy: str, transcript: str, tool_results: str):
    """Host-issued excerpts of the tau2 environment (policy, conversation, tool output). The receipt id is the content digest; no retrieval is claimed."""
    from cherryme.host_grounding import RetrievedSource
    parts = [("policy", c) for c in _chunks(policy)][:6] + [("conversation", c) for c in _chunks(transcript[-CHUNK:])] + [("system-data", c) for c in _chunks(tool_results[-2 * CHUNK:])]
    out = []
    for i, (group, text) in enumerate(parts[:MAX_SOURCES]):
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        out.append(RetrievedSource(source_ref=f"https://tau2-environment.invalid/{task_id}/{group}/{i}", excerpt=text, excerpt_sha256=digest,
                                   retrieval_receipt_id=f"tau2-env:{digest[:16]}", source_group=group))
    return out


class OrgBridge:
    """One per Episode (one tau2 task per process). Lazy: nothing is built or spent until the first consequential decision."""

    def __init__(self, stack: Any, sid: str, task_id: str, policy: str, work_dir: Path):
        self.stack, self.sid, self.task_id, self.policy, self.dir = stack, sid, task_id, policy, work_dir
        self.engine = None
        self.sources: list = []
        self.alert = 0                                  # earlier dissent/refutation/failure in this episode (structured signal, escalates the importance of later claims)
        self.decisions: list[dict] = []
        self.ablate = set(filter(None, os.environ.get("OGI013_ORG_ABLATE", "").split(",")))   # pre-registered ablations: triage,verify,knowledge

    def _build(self) -> None:
        from cherryme.appleme_bridge import connect_appleme
        from cherryme.engine import CherryMeEngine
        from cherryme.knowledge import KnowledgeStore
        from cherryme.orchestrator import ResolutionAwareOrchestrator
        from cherryme.plumme_bridge import connect_plumme
        from cherryme.runtime import responsibility_runtime
        from cherryme.verification import EvidenceVerifier
        from cherryme.models import QuestionType
        from peachme.cherry_accounting import BudgetedPlumMeService
        svc = BudgetedPlumMeService(self.stack.svc, self.stack.store, self.sid, authorize_model_input=lambda text, view: text)
        registry, investigator = connect_plumme(service=svc, refresh=True, host_grounding_provider=lambda question: self._grounding(question))
        state = Path(os.environ.get("OGI013_ORG_STATE_DIR") or self.dir)       # shared across the tasks of ONE arm (set by the launch script); isolation between arms = separate dirs
        state.mkdir(parents=True, exist_ok=True)
        knowledge = KnowledgeStore(state / "knowledge.jsonl") if "knowledge" not in self.ablate else None
        runtime = responsibility_runtime(triage="off" if "triage" in self.ablate else "auto", knowledge_store=knowledge)
        self.dir.mkdir(parents=True, exist_ok=True)

        class Falsify:                                   # the question type the decision claim is put under: try to refute the action (SCIENCE-type grounding is done by the verifier)
            def choose(self, claim, state_features):
                return QuestionType.FALSIFY

        assurance = connect_appleme(workspace_root=self.dir / "appleme")
        self.state = state
        self.engine = CherryMeEngine(workspace_root=state / "cherry", registry=registry, investigator=investigator, assurance_tier=assurance,
                                     orchestrator=ResolutionAwareOrchestrator(Falsify()), orchestration_skill=runtime["orchestration_skill"], frame=runtime["frame"])
        # This PlumMe revision's BudgetEnvelope requires an integer per-response cap (newer PlumMe accepts none). Use the cap every other FruitStack step in this harness uses
        # (fs.infer max_output_tokens=2048) so all arms share one per-response limit; it is not a task, token or call budget.
        investigator.max_output_tokens = investigator.verifier_max_output_tokens = int(os.environ.get("OGI013_RESPONSE_TOKENS", "2048"))
        real_investigate, trace_file = investigator.investigate, self.dir / "investigator-exceptions.log"

        def traced(question, agent):                       # instrumentation only: the engine records a bare INVESTIGATOR_EXCEPTION; keep the cause
            try:
                return real_investigate(question, agent)
            except Exception:  # noqa: BLE001
                import traceback
                with trace_file.open("a") as f:
                    f.write(f"--- {question.type} agent={getattr(agent, 'id', None)}\n{traceback.format_exc()}\n")
                raise
        investigator.investigate = traced
        self._reserve_simulator_route(registry)
        if "verify" not in self.ablate:
            investigator.evidence_verifier = EvidenceVerifier(investigator.run_worker, claim_lookup=lambda cid: self.engine.claims.load(cid)[0].text)

    def _reserve_simulator_route(self, registry) -> None:
        """The user simulator is pinned to one model for the pair; agent-side workers must not compete for that throttled free route (benchmark infrastructure isolation)."""
        route_file = os.environ.get("OGI013_SIM_ROUTE_FILE")
        try:
            key = json.loads(Path(route_file).read_text())["model_key"] if route_file and Path(route_file).exists() else None
            card = registry._agents.get(key) if key else None
            if card is not None:
                from dataclasses import replace
                registry._agents[key] = replace(card, enabled=False)
        except Exception:  # noqa: BLE001 - isolation is best effort; the run records which models the workers used
            pass

    def _grounding(self, question):
        from cherryme.host_grounding import HostGrounding
        return HostGrounding(question_id=question.id, sources=tuple(self.sources), search_backend="tau2-environment", corpus_family="tau2-airline-environment")

    def decide(self, *, description: str, importance: float, request: str, transcript: str, tool_results: str) -> dict:
        """Put one decision to the CherryMe engine. Returns status (SUPPORTED/REFUTED/CONFLICT/UNKNOWN), dissent texts, and the organisation the engine actually used."""
        from cherryme.models import Claim
        if self.engine is None:
            self._build()
        self.sources = environment_sources(self.task_id, self.policy, transcript, tool_results)
        claim = Claim(text=f"{description} follows the policy and is justified by the customer's request and the observed system data.",
                      importance=min(1.0, importance + 0.1 * self.alert), objective=request[:1000])
        self.engine.add_claim(claim)
        calls_before, dispatches_before = self.engine.provider_calls, self.engine.provider_dispatches
        self.engine.run([claim.id], budget=QUESTIONS_PER_DECISION)
        final = self.engine.claims.load(claim.id)[0]
        rows = self.engine.ledger.for_claim(claim.id)
        dissent = [{"worker": r.worker, "kind": r.kind, "text": (r.answer_text or "")[:600]} for r in rows if r.epistemic_status == "DISSENT"]
        rec = {"claim": claim.id, "status": final.status.value, "importance": claim.importance, "rows": len(rows), "workers": sorted({str(r.worker) for r in rows if r.worker}),
               "dissent": dissent, "provider_calls": self.engine.provider_calls - calls_before, "provider_dispatches": self.engine.provider_dispatches - dispatches_before,
               "triage": (self.engine.triage_log[-1]["status"] if self.engine.triage_log else None)}
        if final.status.value in ("REFUTED", "CONFLICT") or dissent:
            self.alert = min(self.alert + 1, 3)
        self.decisions.append(rec)
        return rec
