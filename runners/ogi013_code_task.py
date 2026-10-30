"""OGI-013 single coding task: the integrated FruitStack (PlumMe AUTO, PeachMe, Pomelo gate, CherryMe Brother Mode) on a repository task with executable acceptance tests.

Reuses the tau2 adapter's Stack / Episode / FruitStackTau2Agent._org_collab / SINGLE-E vote unchanged; this module only supplies the coding toolbox (list_dir, read_file, search, edit_file, run_tests),
the turn loop, and the Pomelo-gated tool execution. The agent never sees the hidden acceptance tests, the gold patch or hints; the verdict comes from the task's own evaluator, run afterwards.

usage (inside the host python, see evidence/ogi013-single-task/run_code_arm.sh):
  ogi013_code_task.py --workdir DIR --task-json task.json --python VENV_PY --out OUT --mode single|rg2|single_e [--max-turns 40]"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

from ogi013_tau2_agent import Episode, FruitStackTau2Agent, Stack, _is_stop, parse_action

SYSTEM = """You are a software engineer fixing an issue in the repository checked out in the working directory. Work in steps; each step is exactly ONE action.
Reply with EXACTLY ONE JSON object and nothing else:
  {{"action": "tool", "name": "<tool name>", "arguments": {{...}}}}
  {{"action": "message", "content": "<final summary>"}}      (this submits your work and ends the session; send it only when the fix is complete and verified)
Tools:
  list_dir   {{"path": "<dir relative to repo root>"}}
  read_file  {{"path": "<file>", "start": <first line, default 1>, "end": <last line, default start+199>}}      (numbered lines; at most 250 per call)
  search     {{"pattern": "<regex>", "path": "<dir or file, default .>"}}      (grep -rn, at most 40 hits)
  edit_file  {{"path": "<file>", "old": "<exact existing text, must occur exactly once>", "new": "<replacement text>"}}      (tests/ is read-only)
  run_tests  {{"modules": ["forms_tests.tests.test_media", ...]}}      (Django test labels; runs tests/runtests.py with the project's Python and returns the tail of the output)
<issue>
{issue}
</issue>"""
MAX_RESULT_CHARS = 6000
KEEP_FULL = 3          # the latest tool results stay in full, older ones are cut to a short head (keeps every request inside the models' context windows)


class Sandbox:
    def __init__(self, workdir: Path, python: str):
        self.root, self.python = workdir.resolve(), python

    def _path(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if self.root != p and self.root not in p.parents or ".git" in p.relative_to(self.root).parts:
            raise ValueError(f"path outside the repository: {rel}")
        return p

    def list_dir(self, path: str = ".") -> str:
        p = self._path(path)
        return "\n".join(sorted(f"{x.name}{'/' if x.is_dir() else ''}" for x in p.iterdir() if x.name != ".git"))[:MAX_RESULT_CHARS]

    def read_file(self, path: str, start: int = 1, end: int | None = None) -> str:
        lines = self._path(path).read_text(errors="replace").splitlines()
        start = max(1, int(start))
        end = min(int(end) if end else start + 199, start + 249, len(lines))
        return "\n".join(f"{i + 1}: {lines[i]}" for i in range(start - 1, end))[:MAX_RESULT_CHARS] + f"\n[lines {start}-{end} of {len(lines)}]"

    def search(self, pattern: str, path: str = ".") -> str:
        r = subprocess.run(["grep", "-rnE", "--include=*.py", "-m", "20", pattern, str(self._path(path))], capture_output=True, text=True, timeout=60)
        hits = [l.replace(str(self.root) + "/", "") for l in r.stdout.splitlines()[:40]]
        return "\n".join(l[:240] for l in hits) or "(no matches)"

    def edit_file(self, path: str, old: str, new: str) -> str:
        p = self._path(path)
        if "tests" in p.relative_to(self.root).parts[:1]:
            raise ValueError("tests/ is read-only")
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            raise ValueError(f"'old' must occur exactly once in {path}; it occurs {n} times")
        p.write_text(text.replace(old, new))
        return f"OK: edited {path}"

    def run_tests(self, modules: list[str]) -> str:
        if not modules or not all(re.fullmatch(r"[\w.]+", m) for m in modules):
            raise ValueError("modules must be Django test labels")
        env = {"PYTHONWARNINGS": "ignore", "PATH": "/usr/bin:/bin", "PYTHONPATH": str(self.root), "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        r = subprocess.run([self.python, "tests/runtests.py", "--parallel", "1", *modules], cwd=self.root, capture_output=True, text=True, timeout=900, env=env)
        return f"exit={r.returncode}\n" + (r.stdout + r.stderr)[-3000:]


class _Bridge:
    """Pomelo adapter for one tool call (the same shape as the tau2 runner's _ToolBridge)."""
    def __init__(self, fn, args):
        self.fn, self.args = fn, args

    def dispatch(self, intent):
        from pomelome.effects import EffectObservation
        try:
            return EffectObservation(success=True, data=self.fn(**self.args), external_ref=intent.effect_id)
        except Exception as exc:  # noqa: BLE001 - a tool error is an observation for the model
            return EffectObservation(success=False, data={"error": f"{type(exc).__name__}: {exc}"}, external_ref=intent.effect_id)

    def probe(self, intent):
        return None


def render(transcript: list[dict]) -> str:
    out, n = [], len(transcript)
    for i, e in enumerate(transcript):
        if e["role"] == "result" and i < n - KEEP_FULL:
            out.append(f"TOOL RESULT: {e['text'][:500]}{' [...]' if len(e['text']) > 500 else ''}")
        else:
            out.append({"call": "ASSISTANT TOOL CALL: ", "result": "TOOL RESULT: "}[e["role"]] + e["text"])
    return "\n".join(out)


def pomelo_call(ep: Episode, sb: Sandbox, effects, name: str, args: dict, write: bool) -> tuple[str, bool]:
    from peachme.pomelo import effect_identity
    from pomelome.models import EffectClass
    fn = getattr(sb, name, None)
    if fn is None or name.startswith("_"):
        return f"Error: unknown tool {name}", True
    key = f"{name}-{uuid.uuid4().hex[:10]}"
    effects.gateway.adapters[name] = _Bridge(fn, args)
    rev = ep.stack.store.get(ep.sid).revision
    ep.stack.fs.execute_effect(ep.sid, rev, effect_key=key, tool=name, effect_class=(EffectClass.IRREVERSIBLE if write else EffectClass.READ).value, args=args,
                               required_capabilities=(f"tool:{name}",))
    rec = effects.gateway.store.get_effect(effect_identity(ep.sid, key))
    obs = rec.get("observation") if rec else None
    if not obs:
        return "Error: the execution gate returned no observation", True
    data = obs.get("data")
    failed = obs.get("success") is not True
    if isinstance(data, dict) and set(data) == {"error"}:
        data = f"Error: {data['error']}"
    return (data if isinstance(data, str) else json.dumps(data, default=str))[:MAX_RESULT_CHARS], failed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, required=True)
    ap.add_argument("--task-json", type=Path, required=True)
    ap.add_argument("--python", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mode", choices=["single", "rg2", "single_e"], required=True)
    ap.add_argument("--max-turns", type=int, default=40)
    a = ap.parse_args(argv)
    task = json.loads(a.task_json.read_text())
    a.out.mkdir(parents=True, exist_ok=True)
    stack = Stack.get(a.out / "fruitstack")
    import ogi013_host_composer
    effects = ogi013_host_composer.host_effects()
    stack.fs.attach_host_effects(**effects)
    effects = stack.fs.effects                              # the attached gateway wrapper (as the tau2 runner's _host_effects)
    sb = Sandbox(a.workdir, a.python)
    log = a.out / "fruitstack-events.jsonl"
    ep = Episode(stack, a.mode, task["instance_id"], "django", log)
    if a.mode != "rg2":                                    # the organised mode configures the session ceilings itself; the other modes get the same ones
        env = os.environ.get
        stack.fs.governance.configure(ep.sid, ep.store_revision(stack), max_calls=int(env("OGI013_SESSION_MAX_CALLS")) if env("OGI013_SESSION_MAX_CALLS") else None,
                                      max_tokens=int(env("OGI013_SESSION_MAX_TOKENS")) if env("OGI013_SESSION_MAX_TOKENS") else None, max_cost_usd=0.0)
    agent = object.__new__(FruitStackTau2Agent)            # the existing organisation methods (_org_collab, _single_e_vote) run on this host object unchanged
    agent.mode, agent.task, agent.domain, agent.out, agent.tools = a.mode, type("T", (), {"id": task["instance_id"]})(), "django", a.out, []
    agent.k = int(os.environ.get("OGI013_SINGLE_E_K", "2")) if a.mode == "single_e" else None
    agent.write_tools = {"edit_file"}
    agent.domain_policy = task["problem_statement"]
    agent.ep = ep
    if a.mode == "rg2":
        from ogi013_org_economy import EconomyGate
        ep.economy = EconomyGate.from_env() or EconomyGate()
    head = SYSTEM.format(issue=task["problem_statement"])
    transcript: list[dict] = []
    state = {"transcript": []}
    ep.event("EPISODE_OPENED", work=ep.work, mode=a.mode, write_tools=["edit_file"])
    t0, status = time.monotonic(), "MAX_TURNS"
    try:
        for turn in range(a.max_turns):
            ep.turns = turn + 1
            blocking = ep.blocking()
            if blocking:
                ep.event("REFLEX_STOP", blocking=blocking)
                status = "REFLEX_BLOCKED"
                break
            prompt = head + "\n<work_so_far>\n" + render(transcript) + "\n</work_so_far>\nYour next action (one JSON object):"
            draft = ep.step(prompt, "draft")
            action = parse_action(draft["output"]) if draft["success"] else None
            if a.mode == "single_e" and agent._single_e_applies(action):
                draft, action = agent._single_e_vote(ep, prompt, draft, action)
            used_retry = False
            if action is None and draft["success"]:
                used_retry = True
                fix = ep.step(prompt + "\nYour previous reply was not a single valid JSON object. Reply with ONE valid JSON object only.", "format")
                action = parse_action(fix["output"]) if fix["success"] else None
                draft = fix if action else draft
            if action is None:
                ep.event("NO_VALID_ACTION", failure=draft.get("failure_class"))
                transcript.append({"role": "result", "text": "Error: your reply was not a valid action; reply with one JSON object."})
                continue
            if action["action"] == "tool" and action["name"] == "edit_file":
                ep.event("DRAFT_ACTION", action=action)       # the author's original proposal, kept for the paired original-vs-revised comparison
            if a.mode == "rg2":
                action = agent._org_collab(ep, prompt, draft, action, state, uncertain=used_retry)
            if action["action"] == "message":
                ep.event("SUBMIT", content=action["content"][:500])
                status = "SUBMITTED"
                break
            name, args = action["name"], action.get("arguments", {})
            transcript.append({"role": "call", "text": f"{name}({json.dumps(args, ensure_ascii=False)[:1500]})"})
            text, failed = pomelo_call(ep, sb, effects, name, args, write=name in agent.write_tools)
            transcript.append({"role": "result", "text": text})
            if name == "edit_file":
                ep.event("EDIT_APPLIED", args=args, ok=not failed)
            ep.assure({"question_type": f"ACT:{name}", "question_outcome": "COUNTED_FAILURE" if failed else "PROGRESS", "verified_evidence_total": ep.verified_results + turn,
                       "mutation_error": {"code": hashlib.sha256(text[:200].encode()).hexdigest()[:12]} if failed else {}})
    except BaseException as exc:  # noqa: BLE001 - a stop is recorded and everything already written is kept
        status = f"STOPPED:{type(exc).__name__}"
        ep.event("RUN_STOPPED", exception=type(exc).__name__, error=str(exc)[:400], budget_stop=_is_stop(exc))
    ep.close(status)
    diff = subprocess.run(["git", "-C", str(a.workdir), "diff"], capture_output=True, text=True).stdout
    (a.out / "patch.diff").write_text(diff)
    summary = {"status": status, "seconds": round(time.monotonic() - t0, 1), "turns": ep.turns, "stats": ep.stats, "patch_bytes": len(diff)}
    (a.out / "run.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps(summary, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
