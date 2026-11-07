"""OGI-013 single coding task: the integrated FruitStack (PlumMe AUTO, PeachMe, Pomelo gate, CherryMe Brother Mode) on a repository task with executable acceptance tests.

Reuses the tau2 adapter's Stack / Episode / FruitStackTau2Agent._org_collab / SINGLE-E vote unchanged; this module only supplies the coding toolbox (list_dir, read_file, search, edit_file, run_tests),
the turn loop, and the Pomelo-gated tool execution. The agent never sees the hidden acceptance tests, the gold patch or hints; the verdict comes from the task's own evaluator, run afterwards.

usage (inside the host python, see evidence/ogi013-single-task/run_code_arm.sh):
  ogi013_code_task.py --workdir DIR --task-json task.json --python VENV_PY --out OUT --mode single|rg2 [--max-turns 40]"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

from ogi013_coding_gate import CodingGate, GateError
SYSTEM = """You are a software engineer fixing an issue in the repository checked out in the working directory. Work in steps; each step is exactly ONE action.
Reply with EXACTLY ONE JSON object and nothing else. A tool call ALWAYS has this shape (the tool name goes in "name", its parameters in "arguments"):
  {{"action": "tool", "name": "read_file", "arguments": {{"path": "django/forms/widgets.py", "start": 1, "end": 120}}}}
  {{"action": "tool", "name": "submit", "arguments": {{}}}}      (hands in your finished change; a plain message {{"action": "message", "content": "..."}} does the same)
Tools:
  list_dir   {{"path": "<dir relative to repo root>"}}
  read_file  {{"path": "<file>", "start": <first line, default 1>, "end": <last line, default start+199>}}      (numbered lines; at most 250 per call)
  search     {{"pattern": "<regex>", "path": "<dir or file, default .>"}}      (grep -rn, at most 40 hits)
  edit_file  {{"path": "<file>", "old": "<exact existing text, must occur exactly once>", "new": "<replacement text>"}}      (tests/ is read-only)
  run_tests  {{"modules": ["forms_tests.tests.test_media", ...]}}      (Django test labels; runs tests/runtests.py with the project's Python and returns the tail of the output)
  run_python {{"code": "<python source>", "label": "<optional: a short name if this is a reproduction check of the issue; exit 0 = the issue is fixed>"}}      (runs a script in the repo root with the project's Python; no network, only the repository is readable/writable)
<issue>
{issue}
</issue>"""
MAX_RESULT_CHARS = 6000
KEEP_FULL = 3          # the latest tool results stay in full, older ones are cut to a short head (keeps every request inside the models' context windows)


class Sandbox:
    def __init__(self, workdir: Path, python: str, readonly: bool = False):
        self.root, self.python, self.readonly = workdir.resolve(), python, readonly
        self.last_run: tuple | None = None          # (argv, exit code, full output) of the latest run_tests, for the submit gate
        self.last_py: tuple | None = None           # (label, exit code, output) of the latest run_python

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
        if self.readonly:
            raise ValueError("this workspace is read-only for you")
        p = self._path(path)
        if "tests" in p.relative_to(self.root).parts[:1]:
            raise ValueError("tests/ is read-only")
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            raise ValueError(f"'old' must occur exactly once in {path}; it occurs {n} times")
        new_text = text.replace(old, new)
        p.write_text(new_text)
        if p.suffix == ".py":                 # AMENDMENT-DRIVER-2 R3: a syntactically invalid edit is reverted and reported by error type only
            chk = subprocess.run([self.python, "-c", "import py_compile,sys,tempfile;d=tempfile.TemporaryDirectory();py_compile.compile(sys.argv[1],cfile=d.name+'/x.pyc',doraise=True)", str(p)],
                                 capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
            if chk.returncode:
                p.write_text(text)
                m = re.search(r"(SyntaxError|IndentationError|TabError)[^\n]*", chk.stderr)
                ln = re.search(r"line (\d+)", chk.stderr)
                detail = re.sub(r"^\w+Error:\s*", "", m.group(0)) if m else "invalid syntax"
                raise ValueError(f"EDIT_REJECTED: {m.group(0).split(':')[0] if m else 'SyntaxError'} at line {ln.group(1) if ln else '?'}: {detail[:160]} (the file was left unchanged)")
        return f"OK: edited {path}"

    def run_tests(self, modules: list[str]) -> str:
        if not modules or not all(re.fullmatch(r"[\w.]+", m) for m in modules):
            raise ValueError("modules must be Django test labels")
        env = {"PYTHONWARNINGS": "ignore", "PATH": "/usr/bin:/bin", "PYTHONPATH": str(self.root), "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        argv = [self.python, "tests/runtests.py", "--parallel", "1", "-v", "2", *modules]
        r = subprocess.run(argv, cwd=self.root, capture_output=True, text=True, timeout=900, env=env)
        self.last_run = (argv, r.returncode, r.stdout + r.stderr)
        return f"exit={r.returncode}\n" + (r.stdout + r.stderr)[-3000:]


    def run_python(self, code: str, label: str = "") -> str:
        """Addendum 5: reproduction / probe scripts. bwrap: read-only host, network off, only the workspace writable; an audit hook additionally limits open() to the workspace, the interpreter and system libraries."""
        hook = ("import sys,os\nR=[os.path.realpath(x) for x in (%r,sys.prefix,sys.base_prefix,'/usr','/lib','/lib64','/etc/ld.so.cache','/proc/self','/dev/null','/dev/urandom','/tmp')]\n"
                "def h(e,a):\n if e=='open' and isinstance(a[0],(str,bytes)) and not isinstance(a[0],int):\n  p=os.path.realpath(os.fsdecode(a[0]))\n  if not any(p==r or p.startswith(r+os.sep) for r in R): raise PermissionError('path outside the repository: '+p)\n"
                " if e=='subprocess.Popen' and a[1] and (os.path.basename(str(a[1][0]))=='git' or str(a[1][-1]).startswith('git log ')): return\n if e in ('subprocess.Popen','os.system','os.exec','os.posix_spawn','os.fork'): raise PermissionError('process creation is not available')\nsys.addaudithook(h)\n") % str(self.root)
        env = {"PYTHONWARNINGS": "ignore", "PATH": "/usr/bin:/bin", "PYTHONPATH": f"{self.root}:{self.root}/tests", "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
        argv = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--bind", str(self.root), str(self.root), "--unshare-net", "--die-with-parent",
                "--chdir", str(self.root), self.python, "-c", hook + code]
        r = subprocess.run(argv, capture_output=True, text=True, timeout=300, env=env)
        out = (r.stdout + r.stderr)
        self.last_py = (label, r.returncode, out)
        return f"exit={r.returncode}\n" + out[-3000:]


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
    last_run = max((i for i in range(1, n) if transcript[i]["role"] == "result" and transcript[i - 1]["text"].startswith("run_tests(")), default=-1)     # AMENDMENT-DRIVER-2: the latest test result stays in full
    for i, e in enumerate(transcript):
        if e["role"] == "result" and i < n - KEEP_FULL and i != last_run:
            out.append(f"TOOL RESULT: {e['text'][:500]}{' [...]' if len(e['text']) > 500 else ''}")
        else:
            out.append({"call": "ASSISTANT TOOL CALL: ", "result": "TOOL RESULT: "}[e["role"]] + e["text"])
    return "\n".join(out)


_POMELO_LOCK = threading.RLock()


def pomelo_call(ep: Episode, sb: Sandbox, effects, name: str, args: dict, write: bool) -> tuple[str, bool]:
    from peachme.pomelo import effect_identity
    from pomelome.models import EffectClass
    fn = getattr(sb, name, None)
    if fn is None or name.startswith("_"):
        return f"Error: unknown tool {name}", True
    key = f"{name}-{uuid.uuid4().hex[:10]}"
    with _POMELO_LOCK:          # the gateway's adapter registry is keyed by tool name: concurrent workers must not overwrite each other's bridge between registration and execution
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


AUTHOR_NOTE = ("\nWhen the fix is complete and you have run the relevant existing tests, submit it. A submission is accepted only with a source change under django/ and a "
               "test run that exercises it after your last edit.")
CRITIC_HEAD = ("You are an independent code reviewer. The repository in the working directory is a copy that already contains a colleague's proposed change. You may read files, search and run "
               "tests; you cannot edit. Inspect the change and run the relevant existing tests yourself, then finish with a plain message (no tool call) whose FIRST line is exactly "
               "'ISSUES: NONE' or 'ISSUES: FOUND', followed by the specific problems and the evidence you observed (test output, code facts).\n"
               "Reply with EXACTLY ONE JSON object per step, either a tool call {{\"action\": \"tool\", \"name\": ..., \"arguments\": {{...}}}} with list_dir/read_file/search/run_tests/run_python "
               "(same arguments as in the task description below) or {{\"action\": \"message\", \"content\": ...}}.\n<issue>\n{issue}\n</issue>\n")
LIMITS = {"author": 40, "critic": 15, "reviser": 25}


class Ctx:
    """Per-thread views (parallel organisation): `ep` and `last_session` are thread-local when a worker thread binds its own forked episode; the main thread keeps the original."""
    def __init__(self, ep, effects, gate, deadline, out):
        self._tl = threading.local()
        self._ep = ep
        self.effects, self.gate, self.deadline, self.out = effects, gate, deadline, out
        self.keys = {"author": set()}
        self._ls_main: dict = {}

    @property
    def ep(self):
        return getattr(self._tl, "ep", None) or self._ep

    @ep.setter
    def ep(self, value):
        self._ep = value

    def bind_thread_ep(self, ep) -> None:
        self._tl.ep = ep
        self._tl.last_session = {}

    def unbind_thread_ep(self) -> None:
        self._tl.ep = None

    @property
    def last_session(self) -> dict:
        return getattr(self._tl, "last_session", None) if getattr(self._tl, "ep", None) is not None else self._ls_main

    @last_session.setter
    def last_session(self, value: dict) -> None:
        if getattr(self._tl, "ep", None) is not None:
            self._tl.last_session = value
        else:
            self._ls_main = value


STALL_TURNS_WITHOUT_ACTION = 8
NO_PROGRESS_TURNS = 8        # Addendum 3 F: a role session stops after this many consecutive turns without progress (replaces the fixed turn cap)
HARD_TURNS = 400             # absolute safety bound of one session; reaching it is reported as a defect, never expected
from ogi013_roster import FAILED_STEPS_BEFORE_CHANGE, STICKY_ALL, InfraSupply, reason_class  # noqa: E402
SUPPLY_WAITS, SUPPLY_WAIT_SECONDS = 10, 60   # NO_ELIGIBLE_NEURON is a supply condition: wait up to 10 minutes per step before the stage fails
NOMINAL_TURNS = 40           # reference length for stall condition (d) "50% of the session's turn limit"


EXPLORATION_ALLOWANCE = 12   # Addendum 5 B: distinct read/search calls of a challenger/voter/helper that can count as progress
TEST_LINE = re.compile(r"^(.+?) \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure|unexpected success)\s*$", re.M)


def visible_results(output: str) -> dict:
    """Per-test outcome of a verbose run_tests output: name -> passed (ok / expected failure). Agent-visible signal only."""
    return {m.group(1): m.group(2) in ("ok", "expected failure") for m in TEST_LINE.finditer(output or "")}


def grounded_text(text: str, sess: dict) -> bool:
    """Addendum 5 B: grounded = cites a test label / run_python output of a command the session executed itself, or a file:line it read."""
    if any(k and k in text for k in sess.get("cmd_keys", ())):
        return True
    return any(any(r.endswith(m.group(1)) or m.group(1).endswith(r) for r in sess.get("reads", ())) for m in re.finditer(r"([\w./]+\.py):\d+", text))


CODE_TOOLS = {"list_dir", "read_file", "search", "edit_file", "run_tests", "run_python", "submit"}


def parse_code_action(text):
    """Read strict tau2 actions plus a tolerant encoding of the same intent (models often write {"action": "<tool>", ...flat arguments...} or {"action": "tool", "name": ..} with
    a stray code fence). Format tolerance only: it never invents a tool, an argument or a value. Identical for every arm."""
    if not text:
        return None
    decoder = json.JSONDecoder()
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = decoder.raw_decode(text[m.start():])
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("action") == "message" and isinstance(obj.get("content"), str):
            return obj
        if obj.get("action") == "tool" and isinstance(obj.get("name"), str) and isinstance(obj.get("arguments", {}), dict):
            obj.setdefault("arguments", {})
            return obj
        name = next((obj[k] for k in ("name", "action", "tool") if isinstance(obj.get(k), str) and obj[k] in CODE_TOOLS), None)
        if name:
            args = obj["arguments"] if isinstance(obj.get("arguments"), dict) else {k: v for k, v in obj.items() if k not in ("action", "name", "tool", "arguments")}
            return {"action": "tool", "name": name, "arguments": args}
    return None


def outcome_key(output: str) -> tuple:
    ran = re.findall(r"^Ran (\d+) tests?", output or "", re.M)
    return (int(ran[-1]) if ran else 0, len(re.findall(r"\.\.\. (?:FAIL|ERROR)\s*$", output or "", re.M)), "OK" in (output or "")[-200:])


def _agent_loop(ctx: Ctx, role: str, head: str, sb: Sandbox, allowed: set, *, exclude=(), prefer=None, gated: bool, gate=None, team=None, helper=None, limit=None, view=None, wait_supply=True, roster=None, role_key=None):
    """One role's tool loop. Returns (final, first_step): final = the accepted SubmitDecision (gated author/reviser) or the critic's message text, or a string 'STOP:<why>'.
    team: shared team state (inserted, hash-logged, into every prompt). helper(cond, wip) -> text|None: asked once per stall condition (Addendum 3 B.3)."""
    ep, transcript, first = ctx.ep, [], None
    gate = gate or ctx.gate
    nominal = limit or NOMINAL_TURNS
    np_turns, seen_reads, tests_run, fail_streak = 0, set(), False, 0
    stall = {"zero": 0, "rejected": 0, "idle": 0, "used": set(), "watch": None}
    ctx.last_session = {"test_runs": 0, "turns": 0, "py_runs": 0, "cmd_keys": [], "check_ns": [], "checks": [], "check_log": [], "reads": set(), "progress": [], "role": role}
    best_vis: dict = {}                                 # Addendum 5: this session's best-so-far visible record (test name -> ever passed)
    repro: dict = {}                                    # label -> last result (True = exit 0) of the session's own reproduction checks
    regressed = False

    def resolve_watch(recovered: bool):
        w = stall["watch"]
        if w:
            ep.event("HELP_GIVEN", role=role, condition=w["cond"], helper_model=w["model"], recovered=recovered, turns_after=ctx.last_session["turns"] - w["turn"])
            stall["watch"] = None

    def step(*a, **k):
        """Infrastructure failures are not evidence about the work: NO_ELIGIBLE_NEURON (supply momentarily exhausted) is waited out, logged, and does not count as a turn."""
        for waited in range((SUPPLY_WAITS if wait_supply else 0) + 1):
            try:
                return ep.step(*a, **k)
            except RuntimeError as exc:
                if "NO_ELIGIBLE_NEURON" not in str(exc):
                    raise
                if waited >= (SUPPLY_WAITS if wait_supply else 0) or time.monotonic() + SUPPLY_WAIT_SECONDS > ctx.deadline:
                    if wait_supply:
                        raise InfraSupply(f"NO_ELIGIBLE_NEURON after {waited} supply waits for role {role_key or role}") from exc
                    raise
                ep.event("SUPPLY_WAIT", role=role, waited=waited + 1, seconds=SUPPLY_WAIT_SECONDS)
                t_w = time.monotonic()
                time.sleep(SUPPLY_WAIT_SECONDS)
                if getattr(ep, "timing", None) is not None:
                    ep.timing.add("retry_wait", t_w, time.monotonic(), role=role)

    def progress_check(made) -> None:
        nonlocal np_turns
        if made:
            ctx.last_session["progress"].append(ctx.last_session["turns"])
            ep.event("PROGRESS", role=role, turn=ctx.last_session["turns"], label=made if isinstance(made, str) else "progress")
        np_turns = 0 if made else np_turns + 1

    for turn in range(limit or HARD_TURNS):
        ctx.last_session["turns"] = turn
        if time.monotonic() > ctx.deadline:
            resolve_watch(False)
            return "STOP:TIME_LIMIT", first
        blocking = ep.blocking()
        if blocking:
            return "STOP:REFLEX_BLOCKED", first
        if stall["watch"] and turn - stall["watch"]["turn"] >= 5:
            resolve_watch(False)
        if helper and gated:
            cond = ("zero_tests" if stall["zero"] >= 2 else "edit_rejected" if stall["rejected"] >= 2 else "idle" if stall["idle"] >= STALL_TURNS_WITHOUT_ACTION
                    else "half_budget" if turn == nominal // 2 else None)
            if cond and cond not in stall["used"]:
                stall["used"].add(cond)
                stall.update(zero=0, rejected=0, idle=0)
                recent = "\n".join(f"{e['text'][:200]}" for e in transcript[-12:])
                ep.event("HELP_REQUESTED", role=role, condition=cond, turn=turn)
                answer, hmodel = helper(cond, gate._source_diff()[0], (sb.last_run[2][-3000:] if sb.last_run else "(no test run yet)"), recent)
                if answer:
                    transcript.append({"role": "result", "text": "HELP FROM A COLLEAGUE (unverified): " + answer[:3000]})
                    stall["watch"] = {"cond": cond, "turn": turn, "model": hmodel}
        if np_turns >= NO_PROGRESS_TURNS:
            ep.event("LOOP_GUARD", guard="NO_PROGRESS_8_TURNS", role=role, turn=turn, test_runs=ctx.last_session["test_runs"])
            resolve_watch(False)
            return "STOP:NO_PROGRESS", first
        ts = (team.prompt(view) if hasattr(team, "prompt") else team.text(view)) if team else ""      # MangoMe is the live shared workspace: the prompt text comes from a MangoMe read
        if team:
            ep.event("TEAM_STATE", role=role, sha=hashlib.sha256(ts.encode()).hexdigest(), turn=turn)
        prompt = head + (f"\n<team_state>\n{ts}\n</team_state>" if ts else "") + "\n<work_so_far>\n" + render(transcript) + "\n</work_so_far>\nYour next action (one JSON object):"
        rk = role_key if roster is not None else None
        pinned = roster.pinned(rk) if rk else None
        pref = pinned or (prefer if first is None else first["model_key"])   # R8: a roster role keeps ONE model for the whole episode; otherwise AMENDMENT-DRIVER-2 R1 (sticky within the session)
        sticky = STICKY_ALL if rk else 2
        d = step(prompt, role, exclude=tuple(exclude), prefer=pref, sticky_attempts=sticky)
        if rk:
            if d["success"]:
                fail_streak = 0
                roster.note_model(d["model_key"])
                if roster.pinned(rk) is None:
                    roster.pin(rk, d["model_key"], d.get("independence_key"))
                elif d["model_key"] != roster.pinned(rk):          # executed by a model other than the pinned one: never silent - a ROSTER_CHANGE with its reason class, then the executed model is the pin
                    roster.change(rk, f"executed by {d['model_key']} instead of the pinned {roster.pinned(rk)} (receipt {d.get('receipt_id')})", "handover")
                    roster.pin(rk, d["model_key"], d.get("independence_key"))
            else:
                fail_streak += 1
                if pinned and fail_streak >= FAILED_STEPS_BEFORE_CHANGE:     # declared failure of the pinned model: exactly one ROSTER_CHANGE, then AUTO picks the replacement
                    roster.change(rk, f"{fail_streak} consecutive failed steps on {pinned}: {d.get('failure_class')}", reason_class(d.get("failure_class")))
                    fail_streak, first = 0, None
        if d["success"] and first is not None and not rk and d["model_key"] != first["model_key"]:
            ep.event("ROLE_HANDOVER", role=role, label="AUTHOR_HANDOVER" if role == "author" else "ROLE_HANDOVER", from_model=first["model_key"], to_model=d["model_key"], reason="2 consecutive provider failures")
            first = {**first, "model_key": d["model_key"]}
        if d["success"] and first is None:
            first = d
        if d["success"] and d.get("independence_key"):
            ctx.keys.setdefault(role, set()).add(d["independence_key"])
        action = parse_code_action(d["output"]) if d["success"] else None
        if action is None and d["success"]:
            fix = step(prompt + "\nYour previous reply was not a single valid JSON object. Reply with ONE valid JSON object only.", role, exclude=tuple(exclude), prefer=pref, sticky_attempts=sticky)
            action = parse_code_action(fix["output"]) if fix["success"] else None
        if action is None:
            ep.event("BAD_ACTION", role=role, model=d.get("model_key"), output=(d.get("output") or "")[:400], failure=d.get("failure_class"))
            transcript.append({"role": "result", "text": "Error: your reply was not a valid action; reply with one JSON object."})
            progress_check(False)
            continue
        if action["action"] == "message" or action.get("name") == "submit":
            if not gated:                                                       # the critic's plain message is its verdict
                if action["action"] == "message":
                    return action["content"], first
                transcript.append({"role": "result", "text": "Error: use a plain message to give your verdict."})
                continue
            dec = gate.check_submit()
            ep.event("SUBMIT_CHECK", role=role, accepted=dec.accepted, reason=dec.reason, sha=dec.diff_sha256)
            if dec.accepted:
                resolve_watch(True)
                progress_check("first_gate_accepted_submit")
                return dec, first
            transcript.append({"role": "call", "text": "submit()"})
            transcript.append({"role": "result", "text": dec.reason})          # the gate's neutral text, verbatim
            progress_check(False)
            continue
        name, args = action["name"], action.get("arguments", {})
        if name in ("decline", "reply") and gated and team is not None:           # exchange protocol: the author answers an objection WITH EVIDENCE (a reproduction or a task-text quote) or concedes
            from ogi013_candidates import classify_objection
            evidence = str(args.get("evidence") or args.get("reason") or "")
            transcript.append({"role": "call", "text": f"{name}({json.dumps(args, ensure_ascii=False)[:300]})"})
            action = "concede" if str(args.get("action", "")).lower() == "concede" else "evidence"
            r = team.reply(str(args.get("id", "")), "author", action, evidence, classify_objection(evidence, team.goal, ctx.last_session["check_log"]))
            transcript.append({"role": "result", "text": {"UNGROUNDED_REPLY": "UNGROUNDED_REPLY: a reply needs evidence (the output of a command you ran, or a verbatim quote of the task text); nothing changed.",
                                                          "REPLY_REFUSED": "reply refused (not an open objection, wrong turn, or the limit of 2 exchanges)."}.get(r["event"], f"recorded: {r['event']}")})
            progress_check(False)
            continue
        if name not in allowed:
            ep.event("BAD_TOOL", role=role, model=d.get("model_key"), name=name)
            transcript.append({"role": "result", "text": f"Error: tool {name} is not available to you"})
            progress_check(False)
            continue
        text, failed = pomelo_call(ep, sb, ctx.effects, name, args, write=name == "edit_file")
        transcript.append({"role": "result", "text": text})
        ep.event("TOOL", role=role, name=name, failed=failed, args=json.dumps(args)[:300])
        made = False
        if name in ("list_dir", "read_file", "search"):
            stall["idle"] += 1
            sig = (name, json.dumps(args, sort_keys=True))
            if (not gated or not tests_run) and sig not in seen_reads:           # read-only roles, and author-type roles until their first run_tests (FIX: dev06): the first EXPLORATION_ALLOWANCE distinct calls count
                seen_reads.add(sig)
                made = "exploration" if len(seen_reads) <= EXPLORATION_ALLOWANCE else False
            if name == "read_file" and not failed:
                ctx.last_session["reads"].add(str(args.get("path", "")))
        elif name == "run_python":
            stall["idle"] = 0
            ctx.last_session["py_runs"] += 1
            if sb.last_py:
                ctx.last_session["check_ns"].append(time.monotonic_ns())
                ctx.last_session["checks"].append((time.monotonic_ns(), sb.last_py[2]))
                ctx.last_session["check_log"].append({"tool": "run_python", "args": {"code": args.get("code", ""), "label": args.get("label", "")}, "output": sb.last_py[2], "failing": sb.last_py[1] != 0})
            if sb.last_py:
                ok_py = sb.last_py[1] == 0
                lab = (sb.last_py[0] or "").strip()
                ctx.last_session["cmd_keys"] += [lab or "run_python", "run_python"]
                if gated and lab:
                    if repro.get(lab) is False and ok_py and not regressed:     # a reproduction check flips fail -> pass with no visible regression
                        made = "repro_check_flipped"
                    repro[lab] = ok_py
        if name == "edit_file":
            stall["idle"] = 0                                                   # a syntax-valid edit alone is NOT progress (Addendum 5)
            stall["rejected"] = stall["rejected"] + 1 if (failed and "EDIT_REJECTED" in text) else 0
            if gated and not failed:
                gate.record_edit(args["path"])
        if name == "run_tests" and sb.last_run:
            stall["idle"] = 0
            ctx.last_session["test_runs"] += 1
            tests_run = True
            ctx.last_session["check_ns"].append(time.monotonic_ns())
            ctx.last_session["checks"].append((time.monotonic_ns(), sb.last_run[2]))
            ctx.last_session["check_log"].append({"tool": "run_tests", "args": {"modules": list(args.get("modules", []))}, "output": sb.last_run[2], "failing": sb.last_run[1] != 0})
            ctx.last_session["cmd_keys"] += list(args.get("modules", []))
            if gated:
                cur = visible_results(sb.last_run[2])
                improved = any(ok_ and not best_vis.get(n, False) for n, ok_ in cur.items())
                regressed = any(best_vis.get(n, False) and not ok_ for n, ok_ in cur.items())
                for n, ok_ in cur.items():
                    best_vis[n] = best_vis.get(n, False) or ok_
                if improved and not regressed:                                  # strictly better than the session's best so far, nothing that passed before fails now
                    made = "visible_tests_better"
                entry = gate.record_test_run(*sb.last_run)
                stall["zero"] = stall["zero"] + 1 if entry["tests_executed"] == 0 else 0
                if entry["tests_executed"] > 0:
                    resolve_watch(True)
            else:
                ep.event("CRITIC_TEST_RUN", argv=sb.last_run[0][2:], exit_code=sb.last_run[1])
        progress_check(made)
    resolve_watch(False)
    return "STOP:MAX_TURNS", first


def agent_loop(ctx: Ctx, role: str, *a, **kw):
    """Runs one role session and logs its end (Addendum 5 guard audit: turns, progress turns, stop reason)."""
    ctx.ep.event("SESSION_START", role=role)
    res = _agent_loop(ctx, role, *a, **kw)
    ls = ctx.last_session
    stop = res[0] if isinstance(res[0], str) and res[0].startswith("STOP:") else "DELIVERED"
    ctx.ep.event("SESSION_END", role=role, turns=ls.get("turns", 0) + 1, progress_turns=len(ls.get("progress", [])), progress_at=ls.get("progress", []), stop=stop)
    return res


def main(argv=None) -> int:
    from ogi013_tau2_agent import Episode, Stack, _is_stop
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", type=Path, required=True)
    ap.add_argument("--task-json", type=Path, required=True)
    ap.add_argument("--python", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mode", choices=["single", "rg2"], required=True, help="single = author only, no criticism (submits P0); rg2 = FruitStack organisation (P0 -> independent Brother critic -> revision P1)")
    ap.add_argument("--wall-seconds", type=int, default=3600)
    a = ap.parse_args(argv)
    task = json.loads(a.task_json.read_text())
    a.out.mkdir(parents=True, exist_ok=True)
    stack = Stack.get(a.out / "fruitstack")
    import ogi013_host_composer
    effects = ogi013_host_composer.host_effects()
    stack.fs.attach_host_effects(**effects)
    effects = stack.fs.effects
    sb = Sandbox(a.workdir, a.python)
    ep = Episode(stack, a.mode, task["instance_id"], "django", a.out / "fruitstack-events.jsonl")
    if a.mode != "rg2":
        env = os.environ.get
        stack.fs.governance.configure(ep.sid, ep.store_revision(stack), max_calls=int(env("OGI013_SESSION_MAX_CALLS")) if env("OGI013_SESSION_MAX_CALLS") else None,
                                      max_tokens=int(env("OGI013_SESSION_MAX_TOKENS")) if env("OGI013_SESSION_MAX_TOKENS") else None, max_cost_usd=0.0)
    gate = CodingGate(a.workdir, task["base_commit"], a.out / "gate")
    t0 = time.monotonic()
    ctx = Ctx(ep, effects, gate, t0 + a.wall_seconds, a.out)
    issue = task["problem_statement"]
    author_head = SYSTEM.format(issue=issue) + AUTHOR_NOTE
    ep.event("EPISODE_OPENED", work=ep.work, mode=a.mode)
    status, review = "NO_PATCH", None
    try:
        final, first = agent_loop(ctx, "author", author_head, sb, {"list_dir", "read_file", "search", "edit_file", "run_tests", "run_python"}, gated=True)
        if isinstance(final, str):
            gate.outcome_without_patch(final)
            ep.event("NO_PATCH", limit=final)
        else:
            gate.snapshot("P0", final)
            status = "P0_SUBMITTED"
            ep.event("P0_FROZEN", sha=final.diff_sha256, author_model=first and first["model_key"], author_keys=sorted(ctx.keys["author"]), files=list(final.changed_source_files))
            if a.mode == "rg2":
                p0_copy = a.out / "p0_workspace"
                shutil.copytree(a.workdir, p0_copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                critic_sb = Sandbox(p0_copy, a.python, readonly=True)
                author_keys = tuple(sorted(ctx.keys["author"]))
                target = gate.review_target()
                from cherryme.brother import run_rounds
                from cherryme.contributions import ContributionLedger
                ledger = ContributionLedger()

                def work(p: str, stage: str, prefer=None, exclude=()):
                    try:
                        if stage == "challenge":
                            out, st = agent_loop(ctx, "critic", CRITIC_HEAD.format(issue=issue) + "\n" + p, critic_sb, {"list_dir", "read_file", "search", "run_tests"},
                                                 exclude=author_keys, gated=False)
                        elif stage == "revise":
                            out, st = agent_loop(ctx, "reviser", author_head + "\n" + p + "\nYour final answer is the repository state: change the files if the criticism is right, re-run the relevant "
                                                 "tests, then submit.", sb, {"list_dir", "read_file", "search", "edit_file", "run_tests", "run_python"}, prefer=prefer.split("#")[0] if prefer else None, gated=True)
                            if not isinstance(out, str):
                                gate.snapshot("P1", out)
                                out = out.diff
                        else:
                            return {"success": False, "output": None, "failure_class": f"STAGE_NOT_USED:{stage}"}
                    except Exception as exc:  # noqa: BLE001
                        if _is_stop(exc):
                            raise
                        return {"success": False, "output": None, "model_key": None, "independence_key": None, "receipt_id": None, "failure_class": (str(exc) or type(exc).__name__)[:80]}
                    if isinstance(out, str) and out.startswith("STOP:"):
                        return {"success": False, "output": None, "model_key": st and st["model_key"], "independence_key": st and st["independence_key"], "receipt_id": st and st["receipt_id"], "failure_class": out}
                    return {"success": True, "output": out, "model_key": st["model_key"], "independence_key": st["independence_key"], "receipt_id": st["receipt_id"]}

                seed = {"text": target, "model_key": first and first["model_key"], "independence_key": next(iter(author_keys), None), "receipt_id": first and first["receipt_id"]}
                prompt = f"Task: resolve this issue in the repository.\n{issue}\n"
                res = run_rounds(task_prompt=prompt, brief="", work=work, ledger=ledger, claim_id=ep.claim.id, n_solvers=1, review_single=True, seed_solution=seed, max_rounds=1)
                review = {"stop": res.stop_reason, "calls": res.calls, "issues_found": res.issues_found, "revised": res.revised, "failures": res.failures,
                          "rows": [{"kind": r.kind, "worker": r.worker, "independence_key": r.identity.get("independence_key"), "status": r.epistemic_status, "text": r.answer_text} for r in res.rows]}
                (a.out / "review.json").write_text(json.dumps(review, indent=1, default=str))
                ep.event("BROTHER_REVIEW", stop=res.stop_reason, issues_found=res.issues_found, revised=res.revised, author_keys=list(author_keys),
                         critic_keys=[r["independence_key"] for r in review["rows"] if r["kind"] == "CRITIQUE"])
                status = "P1_SUBMITTED" if (a.out / "gate" / "P1.diff").exists() else "P0_FINAL"
    except BaseException as exc:  # noqa: BLE001 - a stop is recorded; an accepted snapshot stays the submission, nothing is synthesised
        ep.event("RUN_STOPPED", exception=type(exc).__name__, error=str(exc)[:400], budget_stop=_is_stop(exc))
        if status == "NO_PATCH":
            gate.outcome_without_patch(type(exc).__name__)
        elif status == "P0_SUBMITTED":
            status = "P0_FINAL"
    ep.close(status)
    final_diff = next((p.read_text() for p in (a.out / "gate" / "P1.diff", a.out / "gate" / "P0.diff") if p.exists()), "")
    (a.out / "final.diff").write_text(final_diff)
    summary = {"status": status, "seconds": round(time.monotonic() - t0, 1), "stats": ep.stats, "final_diff_bytes": len(final_diff), "review": {k: v for k, v in (review or {}).items() if k != "rows"}}
    (a.out / "run.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps(summary, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
