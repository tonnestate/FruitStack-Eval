"""Fixed single-model competitor: ChatGPT headless (Codex CLI, ChatGPT login) pinned to ONE model, behind the same PeachMe provider interface the FruitStack arms use.

The owner's baseline (Terra 6.0, alternative Luna 6.0) is not a PlumMe route (no API key, no gateway: a ChatGPT-account session reached only through `codex exec`). This is the smallest
integration that lets the unchanged tau2 harness (Episode.step -> PeachMe session -> `heart`) call it: the same acquire/execute contract as PeachMe's PlumMeProvider, one lease per call,
a receipt row written in PlumMe's receipts format (so the pilot guard, accounting and decision-level tooling read it unchanged), and NOTHING of FruitStack's organisation (no CherryMe,
no reviewer, no second model, no AUTO re-selection): the model identity never changes.

Isolation: a dedicated CODEX_HOME (auth only - no user hooks, no AGENTS.md, no MCP servers, read-only sandbox, ephemeral session, empty working directory), so the competitor receives the task
prompt and nothing else of this machine's agent context. Honest accounting: Codex adds a constant tool/instruction scaffold to every call (measured 13,039 input tokens for an empty
prompt, calibrated at first use); the guard-visible `usage` is net of that constant, the raw numbers are kept in the receipt metadata."""
from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from pathlib import Path

from peachme import PeachError

HOME = Path(os.environ.get("OGI013_CODEX_HOME", "/root/.plumme/codex-headless-home"))
CODEX = os.environ.get("OGI013_CODEX_BIN", "codex")
TIMEOUT_S = float(os.environ.get("OGI013_CODEX_TIMEOUT_S", "300"))


def _env() -> dict:
    return {**os.environ, "CODEX_HOME": str(HOME)}


def _classify(text: str) -> str:
    t = text.lower()
    if "not supported when using codex" in t or "model_not_found" in t:
        return "MODEL_NOT_FOUND"
    if "usage limit" in t or "rate limit" in t or "429" in t:
        return "RATE_LIMITED"
    if "401" in t or "unauthorized" in t or "log in" in t:
        return "AUTH_FAILED"
    return "PROVIDER_UNAVAILABLE"


class CodexHeadlessHeart:
    exclude_independence_keys: tuple = ()          # interface compatibility with LineageHeart (Episode.step sets these; a fixed single model ignores them)
    prefer_model_key: str | None = None

    def __init__(self, model: str, receipts_path: Path):
        self.model = model
        self.receipts = Path(receipts_path)
        self.receipts.parent.mkdir(parents=True, exist_ok=True)
        self._facts: dict[str, dict] = {}
        self._overhead: int | None = None
        self.workdir = Path(os.environ.get("OGI013_CODEX_WORKDIR", "/tmp/ogi013-codex-empty"))
        self.workdir.mkdir(parents=True, exist_ok=True)

    def lease_facts(self, lease_id: str | None) -> dict:
        return dict(self._facts.get(lease_id) or {})

    async def acquire(self, *, role_id: str, objective: str, required_skill_ids: tuple[str, ...], max_cost_usd: float | None = None) -> dict:
        lease = f"lease_codex_{uuid.uuid4().hex}"
        self._facts[lease] = {"independence_key": "chatgpt-codex", "model_key": f"{self.model}@fixed", "prefer_met": None}
        return {"lease_id": lease, "neuron_id": f"codex-headless:{self.model}", "role_id": role_id, "cognitive_owner": "CONSUMER", "effective_skill_ids": list(required_skill_ids),
                "offer_id": f"codex-headless:{self.model}", "model_id": self.model, "provider_id": "chatgpt-codex", "cost_class": "INCLUDED",
                "input_cost_per_million": 0.0, "output_cost_per_million": 0.0, "context_window": 272000, "output_limit": None}

    async def _run(self, prompt: str) -> tuple[dict, str]:
        cmd = [CODEX, "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only", "-m", self.model, "-c", 'approval_policy="never"', "-C", str(self.workdir), "--json", "-"]
        proc = await asyncio.create_subprocess_exec(*cmd, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, env=_env())
        try:
            out, _ = await asyncio.wait_for(proc.communicate(prompt.encode()), timeout=TIMEOUT_S)
        except asyncio.TimeoutError:
            proc.kill()
            raise
        text, usage, errors, tools = "", {}, [], 0
        for line in out.decode(errors="replace").splitlines():
            try:
                ev = json.loads(line)
            except ValueError:
                errors.append(line[:300])
                continue
            item = ev.get("item") or {}
            if ev.get("type") == "item.completed":
                if item.get("type") == "agent_message":
                    text = item.get("text") or text
                elif item.get("type") == "error":
                    errors.append(str(item.get("message"))[:300])
                elif item.get("type") not in ("reasoning",):
                    tools += 1                                                  # any non-message item = the model used a tool: a limitation, recorded
            elif ev.get("type") == "turn.completed":
                usage = ev.get("usage") or {}
            elif ev.get("type") in ("turn.failed", "error"):
                errors.append(json.dumps(ev)[:300])
        return {"text": text, "usage": usage, "errors": errors, "tool_items": tools, "exit": proc.returncode}, out.decode(errors="replace")[-300:]

    async def _scaffold(self) -> int:
        """Codex's constant per-call scaffold, measured once per process with a one-word prompt."""
        if self._overhead is None:
            r, _ = await self._run("Reply with: OK")
            u = r["usage"]
            self._overhead = max(0, int(u.get("input_tokens") or 0) - 6)
        return self._overhead

    async def execute(self, *, lease_id: str, task: str, max_output_tokens: int | None = None, max_total_tokens: int | None = None, max_cost_usd: float | None = None) -> dict:
        started = time.time()
        rid = f"receipt_codex_{uuid.uuid4().hex}"
        failure, res, tail = None, {"text": "", "usage": {}, "errors": [], "tool_items": 0, "exit": None}, ""
        try:
            overhead = await self._scaffold()
            pdir = self.receipts.parent / "codex-prompts"                      # provenance: the exact text the fixed model received
            pdir.mkdir(exist_ok=True)
            (pdir / f"{rid}.txt").write_text(task, encoding="utf-8")
            res, tail = await self._run(task)
            if res["exit"] not in (0, None) or not res["text"]:
                failure = _classify(" ".join(res["errors"]) + " " + tail)
        except asyncio.TimeoutError:
            failure, overhead = "TIMEOUT", self._overhead or 0
        raw_in, raw_out = int(res["usage"].get("input_tokens") or 0), int(res["usage"].get("output_tokens") or 0)
        net_in = max(0, raw_in - (self._overhead or 0)) if raw_in else None
        usage = {"input_tokens": net_in, "output_tokens": raw_out if raw_in else None, "total_tokens": (net_in + raw_out) if net_in is not None else None, "cost_usd": 0.0}
        ok = failure is None
        row = {"receipt_id": rid, "provider_request_id": None, "attempt_id": f"attempt_{uuid.uuid4().hex}", "neuron_id": f"codex-headless:{self.model}", "role_id": "REASONING",
               "adapter": "codex-headless", "provider": "chatgpt-codex", "model": self.model, "model_family": "gpt", "credential_handle": None,
               "started_at": time.strftime("%Y-%m-%dT%H:%M:%S.000000Z", time.gmtime(started)), "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S.000000Z", time.gmtime()),
               "success": ok, "output": res["text"] if ok else "", "failure_class": failure, "failure_message": " ".join(res["errors"])[:300] or None, "usage": usage,
               "fallback_level": 0, "metadata": {"provider_attempt_count": 1, "protocol": "CODEX_EXEC", "raw_input_tokens": raw_in, "cached_input_tokens": res["usage"].get("cached_input_tokens"),
                                                 "raw_output_tokens": raw_out, "scaffold_tokens": self._overhead, "tool_items": res["tool_items"], "model_identity": "pinned-fixed"},
               "offer_id": f"codex-headless:{self.model}", "cost_class": "INCLUDED", "runtime_id": "codex-exec", "canonical_model_id": self.model, "independence_key": "chatgpt-codex",
               "latency_ms": round((time.time() - started) * 1000, 3)}
        with self.receipts.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
        return {"execution": "EXECUTED" if ok else ("NOT_EXECUTED" if failure in ("MODEL_NOT_FOUND", "RATE_LIMITED", "AUTH_FAILED") else "UNCERTAIN"), "dispatches": 1,
                "route_attempts": [{"failure_class": failure, "success": ok, "offer_id": row["offer_id"]}], "no_equivalent_route": False, "receipt_id": rid, "success": ok,
                "output": row["output"], "verification": None, "model": self.model, "input_tokens": usage["input_tokens"], "output_tokens": usage["output_tokens"], "cost_usd": 0.0,
                "failure_class": failure}
