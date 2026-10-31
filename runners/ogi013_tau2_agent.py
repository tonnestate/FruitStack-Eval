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
import copy
import hashlib
import json
import os
import re
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Optional

from tau2.agent.base_agent import HalfDuplexAgent
from tau2.data_model.message import AssistantMessage, Message, MultiToolMessage, ToolCall, ToolMessage, UserMessage
from tau2.environment.tool import Tool
from tau2.environment.toolkit import TOOL_TYPE_ATTR, ToolType

from ogi013_pilot_gate import PilotBudgetStop
from ogi013_pilot_gate import check as pilot_gate
from ogi013_pilot_gate import step_parent_budget
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


STOP_PREFIXES = ("SESSION_BUDGET_EXHAUSTED", "BUDGET_", "REFLEX_BLOCKED")


def _is_stop(exc: BaseException) -> bool:
    """A budget / reflex stop ends the episode: it is never converted into a failed worker, an ORG_ERROR, or an unreviewed action."""
    from peachme import PeachError
    return isinstance(exc, PilotBudgetStop) or (isinstance(exc, PeachError) and str(exc).startswith(STOP_PREFIXES))


def _action_digest(action: dict) -> str:
    return hashlib.sha256(json.dumps(action, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


DECLINE_ACTION = {"action": "message", "content": "I'm sorry, I cannot do that. Is there anything else I can help you with?"}      # the host's generic decline (also used for a refused tool call)


def _is_terminating(action: dict) -> bool:
    """An action that ends the interaction rather than advancing it: a human transfer."""
    return action.get("action") == "tool" and action.get("name") == "transfer_to_human_agents"


def should_organize(mode: str, action: dict, write_tools: set[str]) -> bool:
    if mode == "fixed":
        return True
    if mode == "adaptive":
        return action["action"] == "tool" and (action["name"] in write_tools or action["name"] == "transfer_to_human_agents")
    return False


def count_tokens(messages: list[dict], model_id: str | None):
    """(tokens, tokenizer) from litellm's LOCAL tokenizers (no network, no provider call); (None, None) when unavailable. Only names with a tokenizer litellm ships are passed through."""
    try:
        import litellm
        name = str(model_id or "").lower()
        model = name if name.startswith(("gpt-", "o1", "o3", "o4", "chatgpt", "claude")) else "gpt-4"
        return int(litellm.token_counter(model=model, messages=messages)), model
    except Exception:  # noqa: BLE001 - the PlumMe estimate still governs
        return None, None


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
        from ogi013_lineage_heart import LineageHeart
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
        from ogi013_credential_health import prepare_state
        prepare_state(Path(os.environ["PLUMME_STATE_DIR"]))      # campaigns only: credential health earlier episodes learned (exhausted billing) is not forgotten by this process
        settings = Settings.load()
        self.svc = PlumMeService(settings, adapters=default_adapters(settings))
        if os.environ.get("FLM_KEY"):
            self.svc.credentials.register_source(CredentialSource("freellmapi", CredentialSourceKind.ENV_REFERENCE, "freellmapi-isolated-instance", {"var": "FLM_KEY"}))
        if os.environ.get("OGI013_PILOT_RUNS"):
            from ogi013_credential_health import latch_exhaustion
            latch_exhaustion(self.svc)
        asyncio.run(self.svc.discover())
        self.mango = get_service()
        self.orange = OrangeRuntime()
        orange_project = self.orange.registry.resolve("FruitStack OGI Evaluation")["project_id"]
        self.appleme = connect_appleme(workspace_root=out / "appleme")
        self.store = SessionStore(out / "peachme.sqlite3")
        self.heart = LineageHeart(self.svc)                  # PlumMeProvider + lineage exclusion / author preference / lineage in the lease (ogi013_lineage_heart)
        if os.environ.get("OGI013_FIXED_MODEL"):             # the fixed single-model competitor (ChatGPT headless, ONE pinned model; no PlumMe selection, no organisation): see ogi013_codex_heart
            from ogi013_codex_heart import CodexHeadlessHeart
            self.heart = CodexHeadlessHeart(os.environ["OGI013_FIXED_MODEL"], Path(os.environ["PLUMME_STATE_DIR"]) / "receipts.jsonl")
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


def budget_refusal_kind(code: str, remaining, needed) -> str | None:
    """Which budget does a BUDGET_EXHAUSTED refusal mean? 'episode' = the episode's own PeachMe session token budget (remaining < what the step must reserve): the episode ends at the first refusal
    (INFRA_BUDGET_EXHAUSTED). 'provider' = provider/trial/parent-level exhaustion: supply, handled by the roster rule."""
    if "BUDGET_EXHAUSTED" not in (code or ""):
        return None
    return "episode" if remaining is not None and (needed is None or remaining < needed) else "provider"


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
        from cherryme.continuity import ContinuityLedger
        self.continuity = ContinuityLedger(log.with_name("continuity.json"), objective=f"{domain} task {task_id}")      # cognitive continuity across corrections (CherryMe CM-CONT/1); not a work or truth store
        self.collab_issues = 0         # collaboration reviews in this episode that found issues (the alert that justifies later cooperation)
        self.budget_stopped = False
        if mode == "rg2" or os.environ.get("OGI013_PILOT_BUDGET"):          # child calls of CherryMe's engine are accounted by PeachMe, which requires a configured session budget; the pilot configures it for BOTH arms
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
        self._lock = threading.RLock()                 # shared by forks: log appends and stats updates are serialised
        self.call_gate = None                          # parallel organisation P4: CallGate (cap on simultaneous provider calls), set by the team driver
        self.timing = None                             # parallel organisation P5: TimingRecorder, set by the team driver
        self.token_cap = None                          # episode-wide token cap enforced across forks (each fork is its own PeachMe session)
        self.gov_cfg = None
        self.flags: dict = {}                          # shared by forks: episode-level infrastructure findings (budget exhaustion)
        self.turns = 0
        self.stopped = False
        self.seen_results: set[str] = set()
        self.verified_results = 0
        self.stats = {"steps": 0, "step_retries": 0, "escalations": 0, "challenges_found": 0, "revisions": 0, "reflex_blocks": 0, "unknown_steps": 0, "tokens_in": 0, "tokens_out": 0, "models": {}}

    def store_revision(self, stack: Stack) -> int:
        return stack.store.get(self.sid).revision

    call_gate = None          # class defaults keep Episodes built without __init__ (tests) working
    timing = None
    token_cap = None
    gov_cfg = None

    def _lk(self):
        return self.__dict__.setdefault("_lock", threading.RLock())

    def _flags(self) -> dict:
        return self.__dict__.setdefault("flags", {})

    def fork(self) -> "Episode":
        """Parallel organisation: a concurrent worker gets its OWN PeachMe session (sessions are sequential by design) on the same work and turn; log, stats, lock, gate and timing are shared."""
        child = copy.copy(self)
        child.session = self.stack.store.open(self.actor, work_ref=self.project, memory_ref="memory/working")
        child.sid = child.session.session_id
        self.stack.fs.bind_turn_authority(child.sid, work_ref=self.work, turn_id=self.turn_id, actor_id=self.actor)
        if getattr(self, "gov_cfg", None):
            self.stack.fs.governance.configure(child.sid, child.store_revision(self.stack), **self.gov_cfg)
        child.step_n = 0
        return child

    def _gated(self, fn, role: str):
        """P4/P5: the provider call itself runs inside the cap on simultaneous calls; queue wait, latency and outcome class are recorded as wall-clock intervals."""
        from contextlib import nullcontext
        from ogi013_conc import outcome_class
        with (self.call_gate.slot() if self.call_gate is not None else nullcontext()):
            t = time.monotonic()
            try:
                out = fn()
            except Exception as exc:  # noqa: BLE001
                if self.timing is not None:
                    self.timing.add(outcome_class(str(exc)), t, time.monotonic(), role=role)
                raise
            if self.timing is not None:
                self.timing.add("ok", t, time.monotonic(), role=role)
            return out

    def bump(self, key: str, n: int = 1) -> None:
        with self._lk():
            self.stats[key] += n

    def event(self, kind: str, **data: Any) -> None:
        with self._lk(), self.log.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "task": self.task_id, "mode": self.mode, "sid": self.sid, "event": kind, **data}, default=str) + "\n")

    # one model call = one PeachMe step on the integrated stack; transient supply conditions are handled by PlumMe/PeachMe contracts, not by the benchmark
    def step(self, prompt: str, tag: str, *, exclude: tuple = (), prefer: str | None = None, sticky_attempts: int = 1) -> dict:
        from peachme import PeachError
        fs, last = self.stack.fs, None
        if self._flags().get("budget_exhausted"):
            raise PeachError("BUDGET_EPISODE_EXHAUSTED: " + self._flags()["budget_exhausted"])
        for attempt in range(6 if os.environ.get("OGI013_PILOT_RUNS") else 4):                              # campaigns: 6 (AMENDMENT-1 X; every attempt is a counted dispatch under the 110-request ceiling, the real bound); the frozen C-conditions keep 4
            try:
                pilot_gate()                                  # pilot only: refuse BEFORE the provider dispatch when a budget would be crossed or usage is missing
            except PilotBudgetStop as exc:
                self.budget_stopped = True
                self.event("BUDGET_STOP", source="pilot_gate", error=str(exc)[:300])
                raise
            self.step_n += 1
            key = f"{self.task_id}:{self.turns}:{tag}:{self.step_n}"
            s = self.stack.store.get(self.sid)
            self.stack.heart.exclude_independence_keys = tuple(x for x in exclude if x)
            self.stack.heart.prefer_model_key = prefer if attempt < sticky_attempts else None
            self.stack.heart.strict_prefer = prefer is not None and sticky_attempts >= 99      # roster-pinned call (ogi013_roster.STICKY_ALL): no silent handover
            self.stack.heart.exclude_small_models = True      # lead decision 2026-10-31: the small-model exclusion applies to ALL roles; a role the pool cannot fill ends the episode INFRA_SUPPLY
            self.stack.heart.min_context_tokens = (len(prompt) // 3 + 3000) if os.environ.get("OGI013_PILOT_RUNS") else None      # campaigns only: the request's own size (PlumMe's chars/3 estimate) plus room for the answer
            if self.token_cap is not None and self.stats["tokens_in"] + self.stats["tokens_out"] >= self.token_cap:
                self.budget_stopped = True
                self.event("BUDGET_STOP", source="episode_token_cap", cap=self.token_cap)
                raise PeachError("BUDGET_EPISODE_TOKEN_CAP")
            t0 = time.monotonic()
            try:
                turn = asyncio.run(fs.prepare(self.sid, s.revision, role_id="REASONING", objective=f"tau2 {self.domain} turn"))
                env = self.stack.store.get(self.sid).environment or {}
                facts = getattr(self.stack.heart, "lease_facts", lambda _id: {})(env.get("lease_id"))        # PeachMe stores only a whitelist of lease fields: the lineage comes from the heart
                max_out, reserve = self.output_budget(prompt, env)
                tokens, calls = self.step_authorization()
                with step_parent_budget(self.stack.svc, tokens, calls, account_to=getattr(getattr(self.stack, "out", None), "parent", None), who=key) as parent:           # pilot: the step's tokens AND provider requests are enforced across continuations and retries
                    out = self._gated(lambda: asyncio.run(fs.infer(turn, step_key=key, task=prompt, max_output_tokens=max_out, reserve_tokens=reserve)), tag)
                    if parent is not None:
                        parent.receipted = True
                self._step_parent = parent.snapshot() if parent is not None else None
            except PeachError as exc:
                code = str(exc)
                last = code
                self.event("STEP_REFUSED", step=key, code=code, attempt=attempt + 1)
                if "BUDGET_EXHAUSTED" in code and "SESSION_BUDGET" not in code:
                    # which budget? the episode's own (PeachMe session budget: remaining tokens below what this step must reserve) ends the episode at the FIRST refusal; a provider-level
                    # exhaustion is supply and the roster rule handles it
                    snap = fs.governance.snapshot(self.sid) or {}
                    rem = snap.get("tokens_remaining")
                    need = locals().get("reserve")
                    if budget_refusal_kind(code, rem, need) == "episode":
                        reason = f"episode token budget: {rem} tokens remaining, the step must reserve {need}"
                        self._flags()["budget_exhausted"] = reason
                        self.budget_stopped = True
                        self.event("INFRA_BUDGET_EXHAUSTED", step=key, reason=reason, code=code)
                        raise PeachError("BUDGET_EPISODE_EXHAUSTED: " + reason)
                    self.event("BUDGET_REFUSAL_PROVIDER_LEVEL", step=key, code=code, tokens_remaining=rem, reserve=need)
                if code.startswith("REFLEX_BLOCKED"):
                    raise
                if code.startswith(("EXECUTION_NOT_PERFORMED", "EXECUTION_OUTPUT_UNUSABLE")):
                    self.bump("step_retries")
                    continue
                if code.startswith("EXECUTION_NOT_CONFIRMED"):
                    self.bump("unknown_steps")
                    # UNKNOWN retains its reservation until host reconciliation. An inference step has no external effect, so the host (this harness)
                    # records it ABANDONED (lost / possibly billed; stays in the books and is reported as an unknown step) and continues with a NEW step key.
                    try:
                        fs.steps.reconcile(self.sid, self.stack.store.get(self.sid).revision, key, verdict="ABANDONED")
                    except PeachError as rec_exc:
                        self.event("STEP_RECONCILE_FAILED", step=key, error=str(rec_exc)[:200])
                        raise
                    self.event("STEP_ABANDONED", step=key, code=code)
                    continue
                if code.startswith(("SESSION_BUDGET_EXHAUSTED", "BUDGET_")):
                    self.budget_stopped = True
                    self.event("BUDGET_STOP", source="peachme_governance", code=code)
                raise
            self.bump("steps")
            st = out.step
            from ogi013_pilot_gate import token_limits
            lim = token_limits()
            used = (st.input_tokens or 0) + (st.output_tokens or 0)
            if lim is not None and used > lim["per_step"]:             # pilot: the owner's per-step ceiling holds on what the provider RECORDED too, whatever the pre-dispatch estimate said
                self.budget_stopped = True
                self.event("BUDGET_STOP", source="step_ceiling", code="BUDGET_STEP_CEILING_EXCEEDED", recorded=used, ceiling=lim["per_step"], step=key)
                raise PeachError("BUDGET_STEP_CEILING_EXCEEDED")
            with self._lk():
                self.stats["tokens_in"] += st.input_tokens or 0
                self.stats["tokens_out"] += st.output_tokens or 0
                self.stats["models"][out.model] = self.stats["models"].get(out.model, 0) + 1
            self.event("STEP", step=key, tag=tag, model=out.model, receipt=st.receipt_id, tokens_in=st.input_tokens, tokens_out=st.output_tokens, seconds=round(time.monotonic() - t0, 2), input_estimate=(getattr(self, "_input_estimate", None) or {}), step_requests=(getattr(self, "_step_parent", None) or {}).get("provider_attempt_count"), step_tokens_charged=(getattr(self, "_step_parent", None) or {}).get("charged_tokens"),
                       independence_key=facts.get("independence_key"), model_key=facts.get("model_key"), prefer_met=facts.get("prefer_met"))
            return {"success": True, "output": out.output, "model_key": facts.get("model_key") or out.model, "independence_key": facts.get("independence_key"), "receipt_id": st.receipt_id}
        return {"success": False, "output": None, "failure_class": last or "NO_ADMISSIBLE_WORKER"}

    MIN_ANSWER_TOKENS = 2048    # pilot: a step that cannot afford at least this much answer is not dispatched (a budget stop, not a truncated answer)

    def checkpoint_continuity(self) -> None:
        """Write the continuity record to MangoMe's canonical work graph (checkpoint_work, idempotent per record sequence) so that a restart or another worker finds it there; a failure is recorded, never fatal."""
        led = self.continuity
        try:
            self.stack.fs.mango.checkpoint(self.work, self.actor, "COGNITIVE_CONTINUITY", {**led.checkpoint_payload(), "idempotency_key": f"cont-{self.sid}-{led.seq}"}, turn_id=self.turn_id)
            self.event("CONTINUITY_CHECKPOINT", seq=led.seq, open_objectives=len(led.open_objectives()))
        except Exception as exc:  # noqa: BLE001
            self.event("CONTINUITY_CHECKPOINT_FAILED", error=f"{type(exc).__name__}: {str(exc)[:200]}")

    def step_authorization(self) -> tuple[int | None, int | None]:
        """(tokens, provider requests) the owner's budget allows THIS step in total, continuations and retries included; (None, None) outside the pilot."""
        from ogi013_pilot_gate import token_limits
        limits = token_limits()
        if limits is None:
            return None, None
        remaining = (self.stack.fs.governance.snapshot(self.sid) or {}).get("tokens_remaining")
        tokens = min(c for c in (limits["per_step"], limits["headroom"], remaining) if c is not None)
        return int(tokens), int(limits["calls"])

    def provider_messages(self, prompt: str, env: dict) -> list[dict]:
        """The COMPLETE provider-facing input, built exactly as PlumMe's scheduler builds it: a system message with the lease's skill instructions and the task as the user message."""
        skills = getattr(self.stack.svc, "skills", None)
        system = skills.execution_instructions_for_skills(env.get("role_id") or "REASONING", list(env.get("effective_skill_ids") or [])) if skills is not None else ""
        return [{"role": "system", "content": system}, {"role": "user", "content": prompt}]

    def input_tokens(self, prompt: str, env: dict) -> dict:
        """Pre-dispatch input tokens of the complete provider-facing input. Two independent measures, the larger one governs (no multiplier of ours): PlumMe's own gating estimate (the number its
        scheduler subtracts from the reservation to size the response, SwarmScheduler.estimate_input_tokens) and a real tokenizer count (litellm's local tokenizers; OpenAI/Anthropic model names use
        their own, every other model the generic cl100k encoding - the provider's real tokenizer is not available before dispatch)."""
        from plumme.scheduler import SwarmScheduler
        msgs = self.provider_messages(prompt, env)
        plumme = SwarmScheduler.estimate_input_tokens(msgs)
        counted, tokenizer = count_tokens(msgs, env.get("model_id"))
        return {"bound": max(plumme, counted or 0), "plumme": plumme, "counted": counted, "tokenizer": tokenizer}

    def output_budget(self, prompt: str, env: dict) -> tuple[int | None, int | None]:
        """(max_output_tokens, reserve_tokens) for one step. Outside the pilot: unchanged (2048 per response, reserve = prompt bytes + 2048) - the frozen conditions keep their behaviour.
        In the pilot the step's token authorization is the reservation: min(the owner-approved per-step ceiling, the pilot ledger's remaining headroom, PeachMe's remaining session tokens); no fixed output cap is set.
        PlumMe sizes the first response as min(route limit, reservation - its input estimate) and, when an answer is cut off at the route's limit, CONTINUES it; every request of the step (first attempt and each
        continuation) is checked beforehand against the same authorization by the step's ParentBudget (ogi013_pilot_gate.step_parent_budget), which also clamps each response to the headroom left. A step is refused
        before dispatch only when the counted input (the larger of PlumMe's estimate and a real tokenizer, see input_tokens) leaves less than MIN_ANSWER_TOKENS of the authorization."""
        from ogi013_pilot_gate import token_limits
        from peachme import PeachError
        limits = token_limits()
        if limits is None:
            return 2048, self.reserve(prompt)
        est = self.input_tokens(prompt, env)
        self._input_estimate = est
        inp = est["bound"]
        snap = self.stack.fs.governance.snapshot(self.sid)
        reserve = int(min(c for c in (limits["per_step"], limits["headroom"], (snap or {}).get("tokens_remaining")) if c is not None))
        if reserve - inp < self.MIN_ANSWER_TOKENS:
            raise PeachError("BUDGET_HEADROOM_BELOW_MIN_ANSWER")
        return None, reserve

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
        reason = "BUDGET_STOP" if self.budget_stopped else reason
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
        cont = self.ep.continuity
        record = ("\n<your_earlier_decisions>\n" + cont.summary() + "\n(Open items stay open until closed with a reason; a rejected action does not close them.)\n</your_earlier_decisions>") if cont.seq else ""       # CM-CONT/1, only once something was recorded
        return self.prompt_head + "\n<conversation>\n" + "\n".join(state["transcript"]) + "\n</conversation>" + record + "\nYour next action (one JSON object):"

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
        if self.mode == "single_e" and self._single_e_applies(action):
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
                action = dict(DECLINE_ACTION)
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

    def _single_e_applies(self, action: dict | None) -> bool:
        """OGI013_SINGLE_E_SCOPE=all (default, the registered C3 behaviour): k drafts at every turn. =writes (COLLAB-1): the extra drafts are spent on the decisions COLLAB reviews - a write or a transfer -
        and only there, so the effort is matched per consequential decision and not per turn."""
        if os.environ.get("OGI013_SINGLE_E_SCOPE", "all") != "writes":
            return True
        return action is not None and action["action"] == "tool" and (action["name"] in self.write_tools or action["name"] == "transfer_to_human_agents")

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
            try:
                return ep.step(p, stage, exclude=tuple(exclude), prefer=prefer.split("#")[0] if prefer else None)
            except Exception as exc:  # noqa: BLE001 - an unavailable worker (no admissible route, refused step) is a failed attempt for Brother Mode's loop guards, a stop is not
                if _is_stop(exc):
                    raise
                return {"success": False, "output": None, "model_key": None, "independence_key": None, "receipt_id": None, "failure_class": (str(exc) or type(exc).__name__)[:80]}

        seed = {"text": draft["output"], "model_key": draft.get("model_key"), "independence_key": draft.get("independence_key"), "receipt_id": draft.get("receipt_id")}
        task_prompt = prompt + "\n(Reminder for any reviewer: the reply must stay a single valid JSON action and must comply with the policy and the tool documentation.)"
        try:
            out = collaborate(task_prompt=task_prompt, seed=seed, work=work, ledger=ep.ledger, claim_id=ep.claim.id, parse=parse_action, digest=_action_digest,
                              terminating=_is_terminating, policy_text=self.domain_policy, continuity=ep.continuity)
        except Exception as exc:  # noqa: BLE001 - visible; the benchmark outcome must not depend on the collaboration layer
            if _is_stop(exc):
                ep.budget_stopped = True
                ep.event("BUDGET_STOP", source="collaboration", error=f"{type(exc).__name__}: {str(exc)[:300]}")
                raise
            ep.event("ORG_ERROR", error=f"{type(exc).__name__}: {str(exc)[:300]}")
            return action
        found = any(a.get("found_issues") for a in out.attribution)
        ep.stats["escalations"] += 1
        ep.stats["challenges_found"] += sum(1 for a in out.attribution if a.get("found_issues"))
        ep.event("ORG_COLLAB", purpose=purpose, action=action.get("name", "message"), action_kind=kind, stop=out.stop_reason, calls=out.calls, rounds=out.rounds, changed=out.changed,
                 improved=out.improved, validated=out.validated, review_unavailable=out.review_unavailable, specialist=out.specialist_used, unresolved=out.unresolved,
                 attribution=out.attribution, failures=out.failures, agreement=out.agreement, ungrounded_agreement=out.ungrounded_agreement,
                 overruled=out.overruled, final_reviewed=out.final_reviewed, independent_review=out.independent_review, trail=out.trail, termination=out.termination, declined=out.declined, final_text=out.final_text if out.final_action is not None else None, draft=_action_digest(action),
                 final=_action_digest(out.final_action) if out.final_action is not None else None)
        if out.changed and out.final_action is not None:
            ep.stats["revisions"] += 1
            ep.event("ORG_REVISION", claim=ep.claim.id, draft=_action_digest(action), revised=_action_digest(out.final_action), action_changed=True, trigger="CRITICISM_REVISED")
        ep.collab_issues += 1 if found else 0
        ep.economy.note_outcome({"dissent": [1] if found else [], "status": "REFUTED" if out.changed else "UNKNOWN", "atoms": [], "delivered": 0 if out.review_unavailable else 1,
                                 "dispatch_total": out.calls}, purpose)
        if out.termination is not None:
            ep.checkpoint_continuity()
        if out.declined:                                              # the rejected action is declined without ending the work; the customer's other requests stay open
            ep.event("ORG_DECLINE", action=action.get("name", "message"), reason="termination_not_required")
            return dict(DECLINE_ACTION)
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
