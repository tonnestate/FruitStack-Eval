"""Evidence rule for knowledge questions (QA runner only; code runs keep ogi013_candidates.classify_objection).

An objection or reply is GROUNDED if it has all three labelled parts in its own words:
  CLAIM        which answer is wrong and why
  EVIDENCE     a computation, a derivation step, a cited rule or a stated fact the claim rests on
  CONSEQUENCE  which option follows and how it differs from the judged answer
If EVIDENCE contains runnable code (a fenced python block) the host executes it and checks that the stated `RESULT:` reproduces; a computation that does not run or does not
reproduce is UNGROUNDED. No model judges another model's evidence; correctness is decided later only by the key.

Result: {"kind": "command"} (executed and reproduced), {"kind": "quote"} (stated evidence, nothing runnable) or {"kind": "suggestion"} (not grounded), plus an "argument" report.
`command`/`quote` are the kinds the shared ledger accepts as evidence (ogi013_vote); here they mean executed / stated."""
from __future__ import annotations

import ast
import re
import resource
import subprocess
import sys
import tempfile

LABELS = ("CLAIM", "EVIDENCE", "CONSEQUENCE")
MIN_LEN = {"CLAIM": 15, "EVIDENCE": 20, "CONSEQUENCE": 10}
_LABEL = re.compile(r"^[ \t>*_#-]*(CLAIM|EVIDENCE|CONSEQUENCE)[ \t*_]*[:\-][ \t*_]*", re.I | re.M)
_OPTION = re.compile(r"(?:option|answer|choice)\s*\(?\s*([A-J])\b|\(([A-J])\)")
_APPROVAL = re.compile(r"\s*(\[(UNGROUNDED_APPROVAL|NO_VOTE|APPROVE[^\]]*)\]|ISSUES:\s*NONE|APPROVE)", re.I)
_ALLOWED_IMPORTS = {"math", "fractions", "decimal", "itertools", "functools", "statistics", "cmath", "operator"}
_FORBIDDEN_NAMES = {"open", "exec", "eval", "compile", "__import__", "input", "globals", "locals", "getattr", "setattr", "delattr", "vars", "breakpoint", "exit", "quit"}
RUN_SECONDS = 5

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
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return f"attribute not allowed: {node.attr}"
    return None


def run_code(code: str) -> tuple[bool, str]:
    """Host execution of a computation: allow-listed imports, a fresh interpreter in an empty directory, CPU/memory/time limits, no environment."""
    bad = _static_ok(code)
    if bad:
        return False, bad

    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (RUN_SECONDS, RUN_SECONDS))
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    with tempfile.TemporaryDirectory() as d:
        try:
            p = subprocess.run([sys.executable, "-I", "-S", "-c", code], cwd=d, env={}, capture_output=True, text=True, timeout=RUN_SECONDS + 2, preexec_fn=limits)
        except subprocess.TimeoutExpired:
            return False, "timeout"
    return p.returncode == 0, (p.stdout if p.returncode == 0 else p.stderr)[-500:]


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
    if _APPROVAL.match(text or ""):
        return {"kind": "suggestion", "argument": {"reason": "approval"}}
    parts = parse_parts(text)
    missing = [k for k in LABELS if k not in parts]
    if missing:
        return {"kind": "suggestion", "argument": {"reason": f"missing parts {missing}"}}
    short = [k for k in LABELS if len(parts[k]) < MIN_LEN[k]]
    if short:
        return {"kind": "suggestion", "argument": {"reason": f"parts too short {short}"}}
    if not _OPTION.search(parts["CONSEQUENCE"]):
        return {"kind": "suggestion", "argument": {"reason": "consequence names no option"}}
    blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", parts["EVIDENCE"], re.S)
    if not blocks:
        return {"kind": "quote", "argument": {"reason": "stated evidence", "executed": False}}
    stated = re.search(r"RESULT\s*[:=]\s*(.+)", parts["EVIDENCE"])
    if not stated:
        return {"kind": "suggestion", "argument": {"reason": "computation without a stated RESULT"}}
    detail = []
    for code in blocks:
        ok, why = reproduces(code, stated.group(1))
        detail.append(why)
        if ok:
            return {"kind": "command", "argument": {"reason": "computation reproduced", "executed": True, "detail": why}}
    return {"kind": "suggestion", "argument": {"reason": "computation not reproduced", "executed": True, "detail": detail}}
