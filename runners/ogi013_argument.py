"""Evidence rule for knowledge questions (QA runner only; code runs keep ogi013_candidates.classify_objection).

An objection or reply is GROUNDED if it has all three labelled parts in its own words:
  CLAIM        which answer is wrong and why
  EVIDENCE     a computation, a derivation step, a cited rule or a stated fact the claim rests on
  CONSEQUENCE  which option follows and how it differs from the judged answer
If EVIDENCE contains runnable code (a fenced python block) the host executes it and checks that the stated `RESULT:` reproduces; a computation that does not run or does not
reproduce is UNGROUNDED. No model judges another model's evidence; correctness is decided later only by the key.

    A complete argument is only `formal`; a matching computation is only `reproduced`. Neither establishes relevance, true premises, valid inference, or independent confirmation.
    Those facts stay explicit as unassessed until an independent verifier supplies them. `ledger_ground` maps the evidence form to the shared ledger kind while preserving these checks."""
from __future__ import annotations

import ast
import os
import re
import resource
import selectors
import signal
import subprocess
import sys
import time

LABELS = ("CLAIM", "EVIDENCE", "CONSEQUENCE")
MIN_LEN = {"CLAIM": 15, "EVIDENCE": 20, "CONSEQUENCE": 10}
_LABEL = re.compile(r"^[ \t>*_#-]*(CLAIM|EVIDENCE|CONSEQUENCE)[ \t*_]*[:\-][ \t*_]*", re.I | re.M)
_OPTION = re.compile(r"(?:option|answer|choice)\s*\(?\s*([A-J])\b|\(([A-J])\)")
_APPROVAL = re.compile(r"\s*(\[(UNGROUNDED_APPROVAL|NO_VOTE|APPROVE[^\]]*)\]|ISSUES:\s*NONE|APPROVE)", re.I)
_ALLOWED_IMPORTS = {"math", "fractions", "decimal", "itertools", "statistics", "cmath"}
_FORBIDDEN_NAMES = {"open", "exec", "eval", "compile", "__import__", "input", "globals", "locals", "getattr", "setattr", "delattr", "vars", "breakpoint", "exit", "quit"}
RUN_SECONDS = 5
OUTPUT_LIMIT = 64 * 1024

CRITIC_INSTRUCTIONS = (
    "\nIf you find an error, write 'ISSUES: FOUND' and then exactly these three labelled parts, each in your own words:\n"
    "CLAIM: which answer is wrong and why.\n"
    "EVIDENCE: the computation, derivation step, cited rule or stated fact the claim rests on (if you give code, use a ```python block that prints its result and "
    "write 'RESULT: <value>' with the value you expect it to print).\n"
    "CONSEQUENCE: which option follows and how it differs from the judged answer.\n"
    "If you find no error, write 'ISSUES: NONE'.\n")
REPLY_INSTRUCTIONS = (
    "\nIf you answer an objection, use the same three labelled parts (CLAIM, EVIDENCE, CONSEQUENCE) in your own words; a reply without all three counts as no evidence. "
    "End with 'ANSWER: <letter>'.\n")


def parse_parts(text: str) -> dict:
    """Labelled parts of a text: {label: body}; a missing label is absent."""
    marks = list(_LABEL.finditer(text or ""))
    parts: dict = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        parts.setdefault(m.group(1).upper(), (text[m.end():end]).strip())
    return parts


def _static_ok(code: str) -> str | None:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return f"syntax error: {exc.msg}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            if any(n.split(".")[0] not in _ALLOWED_IMPORTS for n in names):
                return f"import not allowed: {names}"
        if isinstance(node, ast.Name) and node.id in _FORBIDDEN_NAMES:
            return f"name not allowed: {node.id}"
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            return f"attribute not allowed: {node.attr}"
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            return f"name not allowed: {node.id}"
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.startswith("__"):
            return "string not allowed"
    return None


def _sandbox_cmd(code: str) -> list | None:
    """bubblewrap: no network/pid/ipc/user namespaces shared, unprivileged uid, empty tmpfs as the only writable and visible home, only the interpreter's prefix and system libraries
    mounted read-only (no host secrets). None when bwrap is missing: fail closed, the argument is then UNGROUNDED. The AST check is a first filter, not the isolation boundary."""
    import shutil
    bwrap = shutil.which("bwrap")
    if not bwrap:
        return None
    real = os.path.realpath(sys.executable)
    prefix = os.path.realpath(sys.base_prefix)
    cmd = [bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--uid", "65534", "--gid", "65534", "--tmpfs", "/tmp", "--chdir", "/tmp", "--dev", "/dev", "--proc", "/proc"]
    for path in sorted({prefix, "/usr", "/lib", "/lib64", "/bin"}):
        if os.path.exists(path):
            cmd += ["--ro-bind", path, path]
    return cmd + [real, "-I", "-S", "-c", code]


def run_code(code: str) -> tuple[bool, str]:
    """Host execution of a computation: AST pre-filter, then bubblewrap isolation (see _sandbox_cmd), CPU/memory/time limits, no environment."""
    bad = _static_ok(code)
    if bad:
        return False, bad

    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (RUN_SECONDS, RUN_SECONDS))
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    cmd = _sandbox_cmd(code)
    if cmd is None:
        return False, "no sandbox available (bwrap): computation not executed"
    return _run_bounded(cmd, RUN_SECONDS + 2, OUTPUT_LIMIT, limits)


def _run_bounded(cmd: list, timeout: float, limit: int, preexec) -> tuple[bool, str]:
    """Run `cmd` reading at most `limit` bytes of stdout+stderr together; more than that kills the child (the computation does not reproduce)."""
    p = subprocess.Popen(cmd, env={}, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=preexec, start_new_session=True)
    sel = selectors.DefaultSelector()
    sel.register(p.stdout, selectors.EVENT_READ, "out")
    sel.register(p.stderr, selectors.EVENT_READ, "err")
    bufs: dict = {"out": [], "err": []}
    total, deadline = 0, time.monotonic() + timeout

    def kill():
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.kill()
        p.wait()
    while sel.get_map():
        left = deadline - time.monotonic()
        if left <= 0:
            kill()
            return False, "timeout"
        for key, _ in sel.select(min(left, 0.5)):
            chunk = os.read(key.fd, 65536)
            if not chunk:
                sel.unregister(key.fileobj)
                continue
            total += len(chunk)
            if total > limit:
                kill()
                return False, f"output overflow (> {limit} bytes): computation killed"
            bufs[key.data].append(chunk)
    try:
        p.wait(timeout=max(0.1, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        kill()
        return False, "timeout"
    out, err = b"".join(bufs["out"]).decode("utf-8", "replace"), b"".join(bufs["err"]).decode("utf-8", "replace")
    return p.returncode == 0, (out if p.returncode == 0 else err)[-500:]


def _norm_value(s: str) -> str:
    s = (s or "").strip().strip("`$ ").replace(",", "")
    try:
        return repr(round(float(eval_number(s)), 9))
    except ValueError:
        return re.sub(r"\s+", "", s).lower()


def eval_number(s: str) -> float:
    """float() of a plain number or a simple fraction like -3/2; anything else raises ValueError."""
    if re.fullmatch(r"-?\d+\s*/\s*-?\d+", s):
        a, b = (float(x) for x in s.split("/"))
        return a / b
    return float(s)


def reproduces(code: str, stated: str) -> tuple[bool, str]:
    ok, out = run_code(code)
    if not ok:
        return False, f"did not run: {out.strip()[:120]}"
    want = _norm_value(stated)
    got = [_norm_value(line) for line in out.strip().splitlines() if line.strip()]
    return (want in got), f"stated {stated.strip()!r}, printed {out.strip()[:120]!r}"


def classify_argument(text: str, task_text: str = "") -> dict:
    """See the module docstring. `task_text` is accepted for call compatibility with classify_objection; it plays no role (a verbatim quote is not an argument)."""
    checks = {"formal_complete": False, "computation_reproduced": None,
              "relevance_assessed": False, "independent_confirmation": False}
    if _APPROVAL.match(text or ""):
        return {"kind": "suggestion", "argument": {"reason": "approval"}, "checks": checks}
    parts = parse_parts(text)
    missing = [k for k in LABELS if k not in parts]
    if missing:
        return {"kind": "suggestion", "argument": {"reason": f"missing parts {missing}"}, "checks": checks}
    short = [k for k in LABELS if len(parts[k]) < MIN_LEN[k]]
    if short:
        return {"kind": "suggestion", "argument": {"reason": f"parts too short {short}"}, "checks": checks}
    if not _OPTION.search(parts["CONSEQUENCE"]):
        return {"kind": "suggestion", "argument": {"reason": "consequence names no option"}, "checks": checks}
    checks["formal_complete"] = True
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", parts["EVIDENCE"], re.S)
    if not blocks:
        return {"kind": "formal", "argument": {"reason": "complete CLAIM/EVIDENCE/CONSEQUENCE, nothing executed", "executed": False}, "checks": checks}
    stated = re.search(r"RESULT\s*[:=]\s*(.+)", parts["EVIDENCE"])
    if not stated:
        checks["computation_reproduced"] = False
        return {"kind": "suggestion", "argument": {"reason": "computation without a stated RESULT"}, "checks": checks}
    detail = []
    for code in blocks:
        ok, why = reproduces(code, stated.group(1))
        detail.append(why)
        if ok:
            checks["computation_reproduced"] = True
            return {"kind": "reproduced", "argument": {"reason": "computation reproduced in the sandbox; relevance and conclusion not assessed", "executed": True, "detail": why}, "checks": checks}
    checks["computation_reproduced"] = False
    return {"kind": "suggestion", "argument": {"reason": "computation not reproduced", "executed": True, "detail": detail}, "checks": checks}


def ledger_ground(g: dict) -> dict:
    """Keep argument status distinct from the ledger's quote/command evidence kind."""
    level = g.get("kind")
    return {**g, "kind": {"formal": "quote", "reproduced": "command"}.get(level, level), "level": level}
