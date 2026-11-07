"""Lean 4 verifier wrapper for the OGI-RH formal tier (design §3.1, §8.5).

The wrapper builds the file itself, so the theorem statement is the locked one by
construction:

    import Lean
    <item imports>
    <arm preamble>            -- auxiliary lemmas; any new axiom is caught by (b)
    theorem <name> : <locked statement> := by
      <arm proof>
    <nonce-tagged check command>

Checks, all fail-closed: (a) compiles, (b) axioms of <name> are a subset of
{propext, Classical.choice, Quot.sound} (the set `#print axioms` reports, via the
same Lean.collectAxioms), (c) statement hash equals the locked hash, (d) a
transitive constant walk from <name> reaches no banned constant (the target theorem
or a blacklisted equivalent).

UNVERIFIED: the Lean check command below has never been compiled here, because Lean
is not installed (design §1). With Lean absent the result is VERIFIER_UNAVAILABLE,
which never passes. Any missing nonce-tagged output line rejects the proof.
Extends /root/fruits/research/fruitstack-rh-research-v1.2/lean_adapter.py
(sha256 be63f062..., strongest status there was COMPILED_ONLY).
"""

from __future__ import annotations

import re
import secrets
import shutil
import subprocess
import tempfile
from pathlib import Path

from ogi_rh.claims import seal, sha256_text, statement_sha256

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_'.]*\Z")

_CHECK = """
open Lean in
partial def ogiReach{nonce} (env : Environment) : List Name → NameSet → NameSet
  | [], seen => seen
  | n :: rest, seen =>
    if seen.contains n then ogiReach{nonce} env rest seen else
    let seen := seen.insert n
    match env.find? n with
    | some ci =>
      let deps := ci.type.getUsedConstants.toList ++
        ((ci.value? (allowOpaque := true)).map (·.getUsedConstants.toList)).getD []
      ogiReach{nonce} env (deps ++ rest) seen
    | none => ogiReach{nonce} env rest seen

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let axs ← liftCoreM (Lean.collectAxioms `{theorem})
  logInfo m!"OGI_AXIOMS_{nonce} {{axs.toList}}"
  let reach := ogiReach{nonce} env [`{theorem}] {{}}
  for b in [{banned}] do
    if reach.contains b then logInfo m!"OGI_BANNED_{nonce} {{b}}"
  logInfo m!"OGI_DONE_{nonce} {{reach.size}}"
"""


def build_source(theorem: str, statement: str, proof: str, *, imports: list[str], banned: list[str],
                 preamble: str = "", nonce: str) -> str:
    body = "\n".join("  " + line for line in proof.strip().splitlines())
    header = "\n".join(["import Lean", *(f"import {m}" for m in imports)])
    check = _CHECK.format(nonce=nonce, theorem=theorem, banned=", ".join(f"`{b}" for b in banned))
    return f"{header}\n\n{preamble.strip()}\n\ntheorem {theorem} : {statement} := by\n{body}\n{check}"


def parse_output(output: str, nonce: str) -> dict:
    axioms = re.search(rf"OGI_AXIOMS_{nonce} \[([^\]]*)\]", output)
    done = re.search(rf"OGI_DONE_{nonce} (\d+)", output)
    return {
        "axioms": sorted(a.strip() for a in axioms.group(1).split(",") if a.strip()) if axioms else None,
        "banned_hits": sorted(set(re.findall(rf"OGI_BANNED_{nonce} (\S+)", output))),
        "walk_complete": bool(done),
    }


def verify(*, theorem: str, statement: str, locked_statement_sha256: str, proof: str,
           banned: list[str], imports: list[str] = (), preamble: str = "",
           lean_cmd: list[str] | None = None, runner=subprocess.run, timeout: int = 600) -> dict:
    """Return a sealed receipt. status is PASS only if checks (a)-(d) all hold."""
    imports, banned = list(imports), list(banned)

    def receipt(status: str, reason: str, **extra) -> dict:
        return seal({"verifier": "lean", "verifier_tier": "FORMAL", "status": status,
                     "passed": status == "PASS", "reason": reason, "theorem": theorem,
                     "statement_sha256": statement_sha256(statement),
                     "locked_statement_sha256": locked_statement_sha256, "banned": banned, **extra})

    if statement_sha256(statement) != locked_statement_sha256:                       # (c)
        return receipt("REJECTED", "STATEMENT_HASH_MISMATCH")
    if not _NAME.match(theorem) or not all(_NAME.match(b) for b in banned) or not banned:
        return receipt("REJECTED", "BAD_THEOREM_OR_BANNED_LIST")
    if lean_cmd is None:
        exe = shutil.which("lean")
        lean_cmd = [exe] if exe else None
    if not lean_cmd:
        return receipt("VERIFIER_UNAVAILABLE", "LEAN_NOT_FOUND")

    nonce = secrets.token_hex(8)
    source = build_source(theorem, statement, proof, imports=imports, banned=banned,
                          preamble=preamble, nonce=nonce)
    try:
        with tempfile.TemporaryDirectory(prefix="ogi-rh-lean-") as tmp:
            path = Path(tmp) / "OgiItem.lean"
            path.write_text(source)
            done = runner([*lean_cmd, str(path)], capture_output=True, text=True,
                          check=False, timeout=timeout)
    except FileNotFoundError:
        return receipt("VERIFIER_UNAVAILABLE", "LEAN_NOT_RUNNABLE")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return receipt("REJECTED", f"LEAN_EXECUTION_FAILED:{type(exc).__name__}")

    output = (done.stdout or "") + (done.stderr or "")
    parsed = parse_output(output, nonce)
    extra = {"source_sha256": sha256_text(source), "log_sha256": sha256_text(output), **parsed}
    if done.returncode != 0:                                                           # (a)
        return receipt("REJECTED", "COMPILE_FAILED", **extra)
    if parsed["axioms"] is None or not parsed["walk_complete"]:
        return receipt("REJECTED", "CHECK_OUTPUT_MISSING", **extra)
    if not set(parsed["axioms"]) <= ALLOWED_AXIOMS:                                    # (b)
        return receipt("REJECTED", "DISALLOWED_AXIOMS", **extra)
    if parsed["banned_hits"]:                                                          # (d)
        return receipt("REJECTED", "BANNED_DEPENDENCY", **extra)
    return receipt("PASS", "ALL_CHECKS_PASSED", **extra)
