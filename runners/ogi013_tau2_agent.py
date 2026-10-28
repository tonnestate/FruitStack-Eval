"""OGI-013 adapter: the integrated FruitStack as a tau2-bench agent (official tasks, official environment, official grader).

Every agent turn is decided THROUGH the integrated stack - never CherryMe -> PlumMe directly:
  MangoMe  : one WorkIdentity + EXECUTE turn per task (isolated database), authority re-verified at every PeachMe context read
  OrangeMe : the project memory ledger (isolated local git ledgers) that PeachMe requires for every context
  PeachMe  : session, budget, reflex arc, egress; every model call is a PeachMe step (prepare -> infer) whose receipts and usage land in the session ledger
  PlumMe   : the heart - dynamic qualified zero-charge supply behind PeachMe's PlumMeProvider
  CherryMe : Brother Mode rounds (solution / challenge / revision, lineage kept in its ContributionLedger) for FIXED and consequence-triggered review in ADAPTIVE
  AppleMe  : trajectory assurance observed every turn; an unhealthy state becomes a HEALTH_WARNING signal in PeachMe, whose BLOCK reflex stops the agent (effective, not decorative)

Three conditions share the same supply, controls and budgets:
  single   : one worker decides each turn; tool effects still pass Pomelo's gate.
  fixed    : CherryMe reviews every valid action with another lineage.
  adaptive : a predeclared consequence rule reviews writes/transfers; other actions use one worker. This is not a learned competence policy.
Usage: imported by ogi013_tau2_run.py (registers the agent factory)."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Any, Optional

from tau2.agent.base_agent import HalfDuplexAgent
from tau2.data_model.message import AssistantMessage, Message, MultiToolMessage, ToolCall, ToolMessage, UserMessage
from tau2.environment.tool import Tool
from tau2.environment.toolkit import TOOL_TYPE_ATTR, ToolType

from ogi013_single_e import majority_action, read_k

MODES = ("single", "fixed", "adaptive", "rg2", "single_e")
SYSTEM = """You are a customer service agent. Follow the <policy> strictly.
In each turn you do exactly ONE of: send a message to the user, or make one tool call. Never both.
Reply with EXACTLY ONE JSON object and nothing else:
  {{"action": "message", "content": "<text for the user>"}}
  {{"action": "tool", "name": "<tool name>", "arguments": {{...}}}}
When the conversation is finished, say so in a message. Only use the tools listed below, with their documented arguments.
<policy>
{policy}
</policy>
<tools>
{tools}
</tools>"""


def _is_write(tool: Tool) -> bool:
    fn = getattr(tool, "_func", None)
    fn = getattr(fn, "__func__", fn)
    return getattr(fn, TOOL_TYPE_ATTR, None) == ToolType.WRITE


def _tool_card(tool: Tool) -> str:
    schema = tool.openai_schema.get("function", {})
    return json.dumps({"name": schema.get("name"), "description": (schema.get("description") or "")[:700], "parameters": schema.get("parameters", {}).get("properties", {}),
                       "required": schema.get("parameters", {}).get("required", [])}, ensure_ascii=False)


def parse_action(text: str | None) -> dict | None:
    """First JSON object of the reply with a valid action."""
    if not text:
        return None
    decoder = json.JSONDecoder()
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = decoder.raw_decode(text[m.start():])
        except ValueError:
            continue
        if isinstance(obj, dict) and obj.get("action") in ("message", "tool"):
            if obj["action"] == "message" and isinstance(obj.get("content"), str):
                return obj
            if obj["action"] == "tool" and isinstance(obj.get("name"), str) and isinstance(obj.get("arguments", {}), dict):
                obj.setdefault("arguments", {})
                return obj
    return None


def _action_digest(action: dict) -> str:
    return hashlib.sha256(json.dumps(action, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


def should_organize(mode: str, action: dict, write_tools: set[str]) -> bool:
    if mode == "fixed":
        return True
    if mode == "adaptive":
        return action["action"] == "tool" and (action["name"] in write_tools or action["name"] == "transfer_to_human_agents")
    return False


class Stack:
    """Process-wide integrated FruitStack (built once). Per-episode state lives in Episode."""
    _inst: Optional["Stack"] = None

    @classmethod
    def get(cls, out: Path) -> "Stack":
        if cls._inst is None:
            cls._inst = cls(out)
        return cls._inst

    def __init__(self, out: Path):
        required = ("OGI013_WORK_REF", "OGI013_TURN_ID", "OGI013_ACTOR_ID", "OGI013_PROJECT_REF")
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise RuntimeError("HOST_BOUND_WORK_REQUIRED: " + ", ".join(missing))
        from cherryme.appleme_bridge import connect_appleme
        from mangome.runtime import get_service
        from orangeme.runtime import OrangeRuntime
        from peachme import SessionStore
        from peachme.fruitstack import AppleAssuranceAdapter, FruitStackSession, MangoWorkAdapter, OrangeMemoryAdapter
        from peachme.plumme import PlumMeProvider
        from plumme.config import Settings
        from plumme.credentials import CredentialSource, CredentialSourceKind
        from plumme.service import PlumMeService, default_adapters
        self.out = out
        out.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("PLUMME_STATE_DIR", str(out / "plumme-state"))
        (Path(os.environ["PLUMME_STATE_DIR"]) / "knowledge").mkdir(parents=True, exist_ok=True)
        snap = Path("/root/fruits/research/FRUITSTACK-EVAL-004/inputs/models.dev-api.json")
        if snap.exists() and not (Path(os.environ["PLUMME_STATE_DIR"]) / "knowledge" / "models.dev-api.json").exists():
            import shutil
            shutil.copyfile(snap, Path(os.environ["PLUMME_STATE_DIR"]) / "knowledge" / "models.dev-api.json")
        settings = Settings.load()
        self.svc = PlumMeService(settings, adapters=default_adapters(settings))
        if os.environ.get("FLM_KEY"):
            self.svc.credentials.register_source(CredentialSource("freellmapi", CredentialSourceKind.ENV_REFERENCE, "freellmapi-isolated-instance", {"var": "FLM_KEY"}))
        asyncio.run(self.svc.discover())
        self.mango = get_service()
        self.orange = OrangeRuntime()
        orange_project = self.orange.registry.resolve("FruitStack OGI Evaluation")["project_id"]
        self.appleme = connect_appleme(workspace_root=out / "appleme")
        self.store = SessionStore(out / "peachme.sqlite3")
        self.heart = PlumMeProvider(self.svc)
        self.fs = FruitStackSession(self.store, self.heart, MangoWorkAdapter(self.mango), OrangeMemoryAdapter(self.orange, project_ref=orange_project), assurance=AppleAssuranceAdapter(getattr(self.appleme, "service", None) or self.appleme._service),
                                    authorize_model_input=lambda text, view: text)
        self.projects: dict[str, str] = {}

    def project(self, workspace: str) -> tuple[str, str, str]:
        """Use only a work identity and active turn admitted by the invoking host."""
        values = {name: os.environ.get(name) for name in (
            "OGI013_WORK_REF", "OGI013_TURN_ID", "OGI013_ACTOR_ID", "OGI013_PROJECT_REF"
        )}
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise RuntimeError("HOST_BOUND_WORK_REQUIRED: " + ", ".join(missing))
        return values["OGI013_WORK_REF"], values["OGI013_PROJECT_REF"], values["OGI013_TURN_ID"]


class Episode:
    def __init__(self, stack: Stack, mode: str, task_id: str, domain: str, log: Path):
        self.stack, self.mode, self.task_id, self.domain, self.log = stack, mode, task_id, domain, log
        fs = stack.fs
        self.actor = os.environ["OGI013_ACTOR_ID"]
        self.work, self.project, self.turn_id = stack.project(f"/ogi013/tau2/{domain}/{mode}")
        self.session = stack.store.open(self.actor, work_ref=self.project, memory_ref="memory/working")  # PeachMe restores by MangoMe project key (as peachme.mission does)
        self.sid = self.session.session_id
        fs.bind_turn_authority(self.sid, work_ref=self.work, turn_id=self.turn_id, actor_id=self.actor)
        self.org = None
        self.economy = None            # EconomyGate when OGI013_ORG_ECONOMY=1 (opt-in; the frozen conditions run without it)
        self.collab_issues = 0         # collaboration reviews in this episode that found issues (the alert that justifies later cooperation)
        if mode == "rg2":                                                    # child calls of CherryMe's engine are accounted by PeachMe, which requires a configured session budget
            env = os.environ.get       # a ceiling exists only if the host authorized one; absent = None = accounted but not capped (cash: none authorized). Nothing is invented.
            fs.governance.configure(self.sid, self.store_revision(stack), max_calls=int(env("OGI013_SESSION_MAX_CALLS")) if env("OGI013_SESSION_MAX_CALLS") else None,
                                    max_tokens=int(env("OGI013_SESSION_MAX_TOKENS")) if env("OGI013_SESSION_MAX_TOKENS") else None,
                                    max_cost_usd=float(env("OGI013_SESSION_MAX_COST_USD")) if env("OGI013_SESSION_MAX_COST_USD") else None)
        from cherryme.contributions import ContributionLedger
        from cherryme.models import Claim
        self.ledger = ContributionLedger()
        self.claim = Claim(text=f"Resolve the customer's request in tau2 {domain} task {task_id} within the policy.")
        self.signal = stack.appleme.start_run(claims=[self.claim], frame={"appleme": {"root_goal": self.claim.text, "definition_of_done": "The customer's request is resolved or transferred according to the policy, "
                                              "with no repeated failing action.", "policy": {"no_progress_heartbeat_threshold": 8}}}, budget=1, call_budget=None)
        self.run_id = self.signal.target_run_id
        self.assurance_id = self.signal.assurance_id
        self.step_n = 0
        self.turns = 0
        self.stopped = False
        self.seen_results: set[str] = set()
        self.verified_results = 0
        self.stats = {"steps": 0, "step_retries": 0, "escalations": 0, "challenges_found": 0, "revisions": 0, "reflex_blocks": 0, "unknown_steps": 0, "tokens_in": 0, "tokens_out": 0, "models": {}}

    def store_revision(self, stack: Stack) -> int:
        return stack.store.get(self.sid).revision

    def event(self, kind: str, **data: Any) -> None:
        with self.log.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "task": self.task_id, "mode": self.mode, "sid": self.sid, "event": kind, **data}, default=str) + "\n")

    # one model call = one PeachMe step on the integrated stack; transient supply conditions are handled by PlumMe/PeachMe contracts, not by the benchmark
    def step(self, prompt: str, tag: str, *, exclude: tuple = (), prefer: str | None = None) -> dict:
        from peachme import PeachError
        fs, last = self.stack.fs, None
        for attempt in range(4):
            self.step_n += 1
            key = f"{self.task_id}:{self.turns}:{tag}:{self.step_n}"
            s = self.stack.store.get(self.sid)
            self.stack.heart.exclude_independence_keys = tuple(x for x in exclude if x)
            self.stack.heart.prefer_model_key = prefer if attempt == 0 else None
            t0 = time.monotonic()
            try:
                turn = asyncio.run(fs.prepare(self.sid, s.revision, role_id="REASONING", objective=f"tau2 {self.domain} turn"))
                env = self.stack.store.get(self.sid).environment or {}
                out = asyncio.run(fs.infer(turn, step_key=key, task=prompt, max_output_tokens=2048,
                                           reserve_tokens=self.reserve(prompt),
                                           ))
            except PeachError as exc:
                code = str(exc)
                last = code
                self.event("STEP_REFUSED", step=key, code=code, attempt=attempt + 1)
                if code.startswith("REFLEX_BLOCKED"):
                    raise
                if code.startswith(("EXECUTION_NOT_PERFORMED", "EXECUTION_OUTPUT_UNUSABLE")):
                    self.stats["step_retries"] += 1
                    continue
                if code.startswith("EXECUTION_NOT_CONFIRMED"):
                    self.stats["unknown_steps"] += 1
                    # UNKNOWN retains its reservation until host reconciliation. An inference step has no external effect, so the host (this harness)
                    # records it ABANDONED (lost / possibly billed; stays in the books and is reported as an unknown step) and continues with a NEW step key.
                    try:
                        fs.steps.reconcile(self.sid, self.stack.store.get(self.sid).revision, key, verdict="ABANDONED")
                    except PeachError as rec_exc:
                        self.event("STEP_RECONCILE_FAILED", step=key, error=str(rec_exc)[:200])
                        raise
                    self.event("STEP_ABANDONED", step=key, code=code)
                    continue
                raise
            self.stats["steps"] += 1
            st = out.step
            self.stats["tokens_in"] += st.input_tokens or 0
            self.stats["tokens_out"] += st.output_tokens or 0
            self.stats["models"][out.model] = self.stats["models"].get(out.model, 0) + 1
            self.event("STEP", step=key, tag=tag, model=out.model, receipt=st.receipt_id, tokens_in=st.input_tokens, tokens_out=st.output_tokens, seconds=round(time.monotonic() - t0, 2),
                       independence_key=env.get("independence_key"), model_key=env.get("model_key"))
            return {"success": True, "output": out.output, "model_key": env.get("model_key") or out.model, "independence_key": env.get("independence_key"), "receipt_id": st.receipt_id}
        return {"success": False, "output": None, "failure_class": last or "NO_ADMISSIBLE_WORKER"}

    def reserve(self, prompt: str) -> int | None:
        snap = self.stack.fs.governance.snapshot(self.sid)
        if snap is None:
            return None
        # UTF-8 bytes conservatively bound input tokens without excluding ordinary small-context free routes.
        needed = len(prompt.encode("utf-8")) + 2048
        return int(needed if snap["tokens_remaining"] is None else min(needed, snap["tokens_remaining"]))

    def blocking(self) -> list[str]:
        return list(self.stack.fs.vitals(self.sid).blocking)

    def assure(self, event: dict) -> str:
        """AppleMe observes the turn; an unhealthy assessment becomes a HEALTH_WARNING signal in PeachMe (BLOCK reflex)."""
        sig = self.stack.appleme.observe_event(target_run_id=self.run_id, event=event, claim=self.claim)
        try:
            self.stack.fs.check_assurance(self.sid, assurance_id=self.assurance_id, event_key=f"{self.task_id}:{self.turns}")
        except Exception as exc:  # noqa: BLE001 - assurance trouble must be visible, not silent
            self.event("ASSURANCE_ERROR", error=str(exc)[:200])
        self.event("ASSURANCE", health=sig.health_state, recommendation=sig.recommendation, blocking=self.blocking())
        return sig.health_state

    def close(self, reason: str) -> None:
        if self.stopped:
            return
        self.stopped = True
        try:
            self.stack.appleme.finish_run(target_run_id=self.run_id, claims=[self.claim], stop_reason=reason)
        except Exception as exc:  # noqa: BLE001
            self.event("ASSURANCE_CLOSE_ERROR", error=str(exc)[:200])
        snap = self.stack.fs.governance.snapshot(self.sid)
        rows = [{"kind": r.kind, "reason": r.reason, "worker": r.worker, "status": r.epistemic_status} for r in self.ledger.rows]
        self.event("EPISODE_CLOSED", reason=reason, stats=self.stats, budget=snap, contributions=rows)


class FruitStackTau2Agent(HalfDuplexAgent[dict]):
    def __init__(self, tools: list[Tool], domain_policy: str, *, mode: str, task: Any, domain: str, out: Path):
        super().__init__(tools=tools, domain_policy=domain_policy)
        if mode not in MODES:
            raise ValueError(f"unsupported OGI-013 mode: {mode}")
        self.mode, self.task, self.domain, self.out = mode, task, domain, out
        self.k = read_k(os.environ) if mode == "single_e" else None   # fail before any spend
        self.write_tools = {t.name for t in tools if _is_write(t)}
        self.prompt_head = SYSTEM.format(policy=domain_policy, tools="\n".join(_tool_card(t) for t in tools))
        self.ep: Optional[Episode] = None

    def get_init_state(self, message_history: Optional[list[Message]] = None) -> dict:
        stack = Stack.get(self.out)
        self.ep = Episode(stack, self.mode, getattr(self.task, "id", "task"), self.domain, self.out / "fruitstack-events.jsonl")
        if self.mode == "rg2":
            from ogi013_org_bridge import OrgBridge
            self.ep.org = OrgBridge(stack, self.ep.sid, str(getattr(self.task, "id", "task")), self.domain_policy, self.out / "org")
            from ogi013_org_economy import EconomyGate
            self.ep.economy = EconomyGate.from_env() or (EconomyGate() if os.environ.get("OGI013_ORG_COLLAB") == "1" else None)
            self.ep.structure_policy = self._structure_policy(f"{self.domain}:{getattr(self.task, 'id', 'task')}")
        self.ep.event("EPISODE_OPENED", work=self.ep.work, turn=self.ep.turn_id, assurance=self.ep.assurance_id, write_tools=sorted(self.write_tools))
        return {"transcript": [], "n_calls": 0}

    @staticmethod
    def _line(m: Message) -> str:
        if isinstance(m, UserMessage):
            return f"USER: {m.content}"
        if isinstance(m, ToolMessage):
            return f"TOOL RESULT ({m.id}): {str(m.content)[:3000]}"
        if isinstance(m, AssistantMessage):
            if m.tool_calls:
                tc = m.tool_calls[0]
                return f"ASSISTANT TOOL CALL: {tc.name}({json.dumps(tc.arguments, ensure_ascii=False)})"
            return f"ASSISTANT: {m.content}"
        return str(m)

    def _decision_prompt(self, state: dict) -> str:
        return self.prompt_head + "\n<conversation>\n" + "\n".join(state["transcript"]) + "\n</conversation>\nYour next action (one JSON object):"

    def generate_next_message(self, message, state: dict):
        ep = self.ep
        ep.turns += 1
        msgs = message.tool_messages if isinstance(message, MultiToolMessage) else [message]
        for m in msgs:
            state["transcript"].append(self._line(m))
            if isinstance(m, ToolMessage) and m.error:                      # observed tool error: the same error repeated is what AppleMe watches for
                ep.last_error = hashlib.sha256(str(m.content)[:200].encode()).hexdigest()[:12]
            elif isinstance(m, ToolMessage):                                 # environment-returned content not seen before is information gain (not a model claim)
                h = hashlib.sha256(str(m.content).encode()).hexdigest()
                if h not in ep.seen_results:
                    ep.seen_results.add(h)
                    ep.verified_results += 1
        blocking = ep.blocking()
        if blocking:                                                             # the reflex arc is binding: no further model spending, the agent stops acting
            ep.stats["reflex_blocks"] += 1
            ep.event("REFLEX_STOP", blocking=blocking)
            msg = AssistantMessage.text("I am unable to continue with this request; I am handing it over to a human agent. ###STOP###")
            state["transcript"].append("ASSISTANT: <reflex stop>")
            ep.close("REFLEX_BLOCKED")
            return msg, state
        prompt = self._decision_prompt(state)
        draft = ep.step(prompt, "draft")
        action = parse_action(draft["output"]) if draft["success"] else None
        if self.mode == "single_e":
            draft, action = self._single_e_vote(ep, prompt, draft, action)
        used_format_retry = False
        if action is None and draft["success"]:
            used_format_retry = True
            fix = ep.step(prompt + "\nYour previous reply was not a single valid JSON object. Reply with ONE valid JSON object only.", "format")
            action = parse_action(fix["output"]) if fix["success"] else None
            draft = fix if action else draft
        final_text = draft["output"]
        if self.mode == "rg2" and action is not None:
            if os.environ.get("OGI013_ORG_COLLAB") == "1":       # exploratory branch: the economy gate decides WHETHER, Brother Mode does the cooperating on the actual solution
                action = self._org_collab(ep, prompt, draft, action, state, uncertain=used_format_retry)
            else:
                action = self._org_decide(ep, prompt, action, state, uncertain=used_format_retry)
        if action is not None and should_organize(self.mode, action, self.write_tools):
            ep.stats["escalations"] += 1
            final_text, action = self._organize(ep, prompt, draft, action)
        if action is None:
            action = {"action": "message", "content": "I'm sorry, I could not complete that step. Could you please repeat your request?"}
            ep.event("NO_VALID_ACTION")
        if action["action"] == "tool":
            names = {t.name for t in self.tools}
            if action["name"] not in names:
                ep.event("UNKNOWN_TOOL", name=action["name"])
                action = {"action": "message", "content": "I'm sorry, I cannot do that. Is there anything else I can help you with?"}
        if action["action"] == "tool":
            msg = AssistantMessage.text("", tool_calls=[ToolCall(id=f"call_{uuid.uuid4().hex[:10]}", name=action["name"], arguments=action["arguments"], requestor="assistant")])
            state["transcript"].append(f"ASSISTANT TOOL CALL: {action['name']}({json.dumps(action['arguments'], ensure_ascii=False)})")
        else:
            msg = AssistantMessage.text(action["content"])
            state["transcript"].append(f"ASSISTANT: {action['content']}")
        outcome = "COUNTED_FAILURE" if getattr(ep, "last_error", None) and action["action"] == "tool" else "PROGRESS"
        ep.assure({"question_type": f"ACT:{action['name']}" if action["action"] == "tool" else "SAY", "question_outcome": outcome, "verified_evidence_total": ep.verified_results, "mutation_error": {"code": getattr(ep, "last_error", None)} if outcome == "COUNTED_FAILURE" else {}})
        ep.last_error = None
        return msg, state

    def _single_e_vote(self, ep: Episode, prompt: str, first: dict, first_action: dict | None) -> tuple[dict, dict | None]:
        """SINGLE-E: k independent drafts from the same supply (each a normal PeachMe step), majority canonical action. No critique, revision or organisation.
        Returns the winning draft and action; if no draft parses, the first draft and None so the existing format retry path runs."""
        drafts = [(first, first_action)]
        for i in range(1, self.k):
            d = ep.step(prompt, f"draft_{i}")
            drafts.append((d, parse_action(d["output"]) if d["success"] else None))
        ep.stats["single_e_drafts"] = ep.stats.get("single_e_drafts", 0) + len(drafts)
        winner, info = majority_action([a for _, a in drafts])
        ep.event("SINGLE_E_VOTE", k=self.k, counts=info["counts"], winner_index=info["winner_index"], ties=info["ties"])
        if winner is None:
            return first, None
        return drafts[info["winner_index"]][0], winner

    def _structure_policy(self, task_ref: str):
        """Host structure policy for this arm: OFF (engine triage decides; default), FIXED, RANDOMIZED (training phase, propensity logged) or LEARNED (gated + authorized only)."""
        from ogi013_org_policy import HostStructurePolicy
        mode = os.environ.get("OGI013_ORG_POLICY_MODE", "OFF").upper()
        learned = None
        if mode == "LEARNED":
            from train_org_policy import OrgPolicy
            learned = OrgPolicy(os.environ["OGI013_ORG_LEARNED_DIR"])
        return HostStructurePolicy(mode, task_ref=task_ref, domain=self.domain, store_dir=Path(os.environ.get("OGI013_ORG_STATE_DIR") or (self.out / "org")),
                                   fixed_arm=os.environ.get("OGI013_ORG_FIXED_ARM"), learned=learned, authorized=os.environ.get("OGI013_ORG_LEARNED_AUTHORIZED") == "1",
                                   seed_salt=os.environ.get("OGI013_ORG_SEED_SALT", ""))

    @staticmethod
    def _abandon_unresolved(ep: Episode) -> None:
        """Engine child inference that ended in an unknown outcome leaves PeachMe steps unresolved, which blocks the next turn (STEP_RECONCILIATION_REQUIRED). As with the
        agent's own unknown steps, the host records them ABANDONED (an inference step has no external effect; the loss stays in the books)."""
        fs = ep.stack.fs
        for key in fs.steps.unresolved(ep.sid):
            fs.steps.reconcile(ep.sid, ep.stack.store.get(ep.sid).revision, key, verdict="ABANDONED")
            ep.stats["unknown_steps"] += 1
            ep.event("STEP_ABANDONED", step=key, code="ENGINE_CHILD_STEP_UNRESOLVED")

    def _org_decide(self, ep: Episode, prompt: str, action: dict, state: dict, uncertain: bool = False) -> dict:
        """RG/2: every proposed action is put to CherryMe's engine as a claim; the engine decides (triage on structured signals, staffing, verification,
        consolidation) how much cognition it deserves. An engine failure never kills the episode (ORG_ERROR is logged and the draft stands); a verified/consolidated dissent triggers a revision."""
        from ogi013_org_bridge import atomic_values
        lines = state["transcript"]
        request = next((l[6:] for l in lines if l.startswith("USER: ")), "")
        if action["action"] == "tool":
            desc = f"The assistant's tool call {action['name']}({json.dumps(action['arguments'], ensure_ascii=False)})"
            importance = 0.9 if action["name"] in self.write_tools else 0.6 if action["name"] == "transfer_to_human_agents" else 0.3   # structured tool type, not a worker label
        else:
            desc = f"The assistant's reply to the customer: {action['content'][:800]}"
            importance = 0.3
        try:
            kind = ("WRITE" if action["name"] in self.write_tools else "TRANSFER" if action["name"] == "transfer_to_human_agents" else "READ") if action["action"] == "tool" else "MESSAGE"
            purpose = None
            if ep.economy is not None:                    # economy mode: cooperation is bought only for a stated purpose; otherwise the single draft stands and nothing is dispatched
                go, purpose = ep.economy.should_escalate(kind=kind, alert=ep.org.alert, prior_dissents=sum(1 for d in ep.org.decisions if d["dissent"]), uncertain=uncertain)
                if not go:
                    ep.event("ORG_SKIPPED", action=action.get("name", "message"), reason=purpose, action_kind=kind)
                    return action
            features = {"importance": importance, "kind": kind, "step_index": ep.turns, "prior_alerts": ep.org.alert, "n_prior_org_decisions": len(ep.org.decisions),
                        "n_prior_dissents": sum(1 for d in ep.org.decisions if d["dissent"])}
            rec = ep.org.decide(description=desc, importance=importance, request=request, transcript="\n".join(lines),
                                tool_results="\n".join(l for l in lines if l.startswith("TOOL RESULT")),
                                structure_policy=getattr(ep, "structure_policy", None), features=features,
                                atoms=atomic_values(action), user_text="\n".join(l for l in lines if l.startswith("USER: ")),
                                economy=ep.economy, purpose=purpose, kind=kind)
        except Exception as exc:  # noqa: BLE001 - visible, not silent; the benchmark outcome must not depend on a bridge crash
            ep.event("ORG_ERROR", error=f"{type(exc).__name__}: {str(exc)[:300]}")
            self._abandon_unresolved(ep)
            return action
        self._abandon_unresolved(ep)
        ep.stats["escalations"] += 1
        ep.event("ORG_DECISION", action=action.get("name", "message"), **{k: v for k, v in rec.items() if k != "dissent"}, dissent_n=len(rec["dissent"]))
        if rec["status"] in ("REFUTED", "CONFLICT") or rec["dissent"]:
            issues = "\n".join(f"- {d['text']}" for d in rec["dissent"]) or "- the verified evidence contradicts the proposed action"
            fix = ep.step(prompt + "\nIndependent reviewers raised these issues with your proposed action:\n" + issues +
                          "\nReconsider against the policy. Reply with ONE valid JSON action.", "revise")
            revised = parse_action(fix["output"]) if fix["success"] else None
            if revised is not None:
                ep.stats["revisions"] += 1
                dig = lambda a: hashlib.sha256(json.dumps(a, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
                ep.event("ORG_REVISION", claim=rec["claim"], draft=dig(action), revised=dig(revised), action_changed=dig(action) != dig(revised),
                         trigger="VERIFIED_DISSENT" if rec["status"] in ("REFUTED", "CONFLICT") else "WORKER_DISSENT")   # causal record: only a changed action after worker dissent counts as an effect
                return revised
        return action

    def _org_collab(self, ep: Episode, prompt: str, draft: dict, action: dict, state: dict, uncertain: bool = False) -> dict:
        """RG/2 + Brother Mode without duplicate review (see ogi013_org_collab): the economy gate decides whether cooperation is justified and records its purpose; the cooperation reviews the
        ACTUAL proposed solution with the full task materials (policy, conversation, tool results), re-examines revisions, lets a specialist adjudicate an unresolved objection, and records
        which contribution materially improved the result. An unchanged answer that was independently validated is reported as validated, never as an improvement."""
        from ogi013_org_collab import collaborate
        kind = ("WRITE" if action["name"] in self.write_tools else "TRANSFER" if action["name"] == "transfer_to_human_agents" else "READ") if action["action"] == "tool" else "MESSAGE"
        go, purpose = ep.economy.should_escalate(kind=kind, alert=ep.collab_issues, prior_dissents=ep.collab_issues, uncertain=uncertain)
        if not go:
            ep.event("ORG_SKIPPED", action=action.get("name", "message"), reason=purpose, action_kind=kind)
            return action

        def work(p: str, stage: str, prefer=None, exclude=()):
            return ep.step(p, stage, exclude=tuple(exclude), prefer=prefer.split("#")[0] if prefer else None)

        seed = {"text": draft["output"], "model_key": draft.get("model_key"), "independence_key": draft.get("independence_key"), "receipt_id": draft.get("receipt_id")}
        task_prompt = prompt + "\n(Reminder for any reviewer: the reply must stay a single valid JSON action and must comply with the policy and the tool documentation.)"
        try:
            out = collaborate(task_prompt=task_prompt, seed=seed, work=work, ledger=ep.ledger, claim_id=ep.claim.id, parse=parse_action, digest=_action_digest)
        except Exception as exc:  # noqa: BLE001 - visible; the benchmark outcome must not depend on the collaboration layer
            ep.event("ORG_ERROR", error=f"{type(exc).__name__}: {str(exc)[:300]}")
            return action
        found = any(a.get("found_issues") for a in out.attribution)
        ep.stats["escalations"] += 1
        ep.stats["challenges_found"] += sum(1 for a in out.attribution if a.get("found_issues"))
        ep.event("ORG_COLLAB", purpose=purpose, action=action.get("name", "message"), action_kind=kind, stop=out.stop_reason, calls=out.calls, rounds=out.rounds, changed=out.changed,
                 improved=out.improved, validated=out.validated, review_unavailable=out.review_unavailable, specialist=out.specialist_used, unresolved=out.unresolved,
                 attribution=out.attribution, failures=out.failures, agreement=out.agreement, ungrounded_agreement=out.ungrounded_agreement,
                 overruled=out.overruled, final_reviewed=out.final_reviewed)
        if out.changed and out.final_action is not None:
            ep.stats["revisions"] += 1
            ep.event("ORG_REVISION", claim=ep.claim.id, draft=_action_digest(action), revised=_action_digest(out.final_action), action_changed=True, trigger="CRITICISM_REVISED")
        ep.collab_issues += 1 if found else 0
        ep.economy.note_outcome({"dissent": [1] if found else [], "status": "REFUTED" if out.changed else "UNKNOWN", "atoms": [], "delivered": 0 if out.review_unavailable else 1,
                                 "dispatch_total": out.calls}, purpose)
        return out.final_action if (out.changed and out.final_action is not None) else action

    def _organize(self, ep: Episode, prompt: str, draft: dict, action: dict) -> tuple[str, dict]:
        """CherryMe Brother Mode on the first draft: a different lineage challenges it against the policy, the author revises on criticism. Calls go through PeachMe steps."""
        from cherryme.brother import run_rounds

        def work(p: str, stage: str, prefer=None, exclude=()):
            r = ep.step(p, stage, exclude=tuple(exclude), prefer=prefer.split("#")[0] if prefer else None)
            return r

        seed = {"text": draft["output"], "model_key": draft.get("model_key"), "independence_key": draft.get("independence_key"), "receipt_id": draft.get("receipt_id")}
        task_prompt = prompt + "\n(Reminder for any reviewer: the reply must stay a single valid JSON action and must comply with the policy and the tool documentation.)"
        res = run_rounds(task_prompt=task_prompt, brief="", work=work, ledger=ep.ledger, claim_id=ep.claim.id, n_solvers=1, review_single=True, seed_solution=seed, max_rounds=2)
        ep.stats["challenges_found"] += res.issues_found
        ep.stats["revisions"] += res.revised
        ep.event("ORGANIZED", issues=res.issues_found, revised=res.revised, rounds=res.rounds, stop=res.stop_reason, failures=res.failures)
        for text in reversed(list(res.positions.values())):
            parsed = parse_action(text)
            if parsed is not None:
                return text, parsed
        return draft["output"], action

    def stop(self, message=None, state=None) -> None:
        if self.ep is not None:
            self.ep.close("TASK_ENDED")


def make_factory(mode: str, out: Path, domain_of_task=lambda task: "unknown"):
    def factory(tools, domain_policy, **kwargs):
        task = kwargs.get("task")
        return FruitStackTau2Agent(tools, domain_policy, mode=mode, task=task, domain=domain_of_task(task), out=out)
    return factory
