import re
import subprocess
from types import SimpleNamespace

import pytest

from ogi_rh import claims as c
from ogi_rh import lean_verifier as lv

STMT = "∀ θ : ℝ, 0 ≤ 3 + 4 * Real.cos θ + Real.cos (2 * θ)"
ARGS = dict(theorem="ogi_f1_01", statement=STMT, locked_statement_sha256=c.statement_sha256(STMT),
            proof="nlinarith [sq_nonneg (Real.cos θ + 1)]", banned=["Target.thm"],
            imports=["Mathlib"])


def stub(axioms="propext, Classical.choice, Quot.sound", banned=(), rc=0, done=True, seen=None):
    """Fake `lean`: reads the generated file, echoes nonce-tagged lines like the real check would."""
    def run(cmd, **kw):
        src = open(cmd[-1]).read()
        if seen is not None:
            seen.append(src)
        nonce = re.search(r"OGI_DONE_([0-9a-f]+)", src).group(1)
        out = [f"OGI_AXIOMS_{nonce} [{axioms}]"] + [f"OGI_BANNED_{nonce} {b}" for b in banned]
        out += [f"OGI_DONE_{nonce} 42"] if done else []
        return SimpleNamespace(returncode=rc, stdout="\n".join(out), stderr="")
    return run


def test_lean_absent_is_unavailable_and_never_passes(monkeypatch):
    monkeypatch.setattr(lv.shutil, "which", lambda name: None)
    r = lv.verify(**ARGS)
    assert r["status"] == "VERIFIER_UNAVAILABLE" and r["passed"] is False
    assert c.classify({"claim_id": "a", "statement": STMT, "kind": "proof", "open_step": "all"},
                      r, known=[])["claim_class"] == c.UNVERIFIED_CANDIDATE


def test_missing_executable_at_run_time_is_unavailable():
    def boom(*a, **k):
        raise FileNotFoundError
    assert lv.verify(**ARGS, lean_cmd=["/nonexistent/lean"], runner=boom)["status"] == "VERIFIER_UNAVAILABLE"


def test_clean_stub_run_passes_and_promotes():
    seen = []
    r = lv.verify(**ARGS, lean_cmd=["lean"], runner=stub(seen=seen))
    assert r["status"] == "PASS" and r["passed"] and c.receipt_intact(r)
    assert f"theorem ogi_f1_01 : {STMT} := by" in seen[0]          # statement fixed by construction
    assert seen[0].startswith("import Lean\nimport Mathlib")
    row = c.classify({"claim_id": "a", "statement": STMT, "kind": "proof"}, r, known=[])
    assert row["claim_class"] == c.PROOF


@pytest.mark.parametrize("runner,reason", [
    (stub(axioms="propext, sorryAx"), "DISALLOWED_AXIOMS"),
    (stub(axioms="propext, my_axiom"), "DISALLOWED_AXIOMS"),
    (stub(banned=["Target.thm"]), "BANNED_DEPENDENCY"),
    (stub(rc=1), "COMPILE_FAILED"),
    (stub(done=False), "CHECK_OUTPUT_MISSING"),
])
def test_rejections(runner, reason):
    r = lv.verify(**ARGS, lean_cmd=["lean"], runner=runner)
    assert (r["status"], r["reason"], r["passed"]) == ("REJECTED", reason, False)


def test_statement_hash_mismatch_rejected_before_running():
    r = lv.verify(**{**ARGS, "statement": STMT.replace("0 ≤", "-1 ≤")}, lean_cmd=["lean"],
                  runner=lambda *a, **k: pytest.fail("must not run"))
    assert r["reason"] == "STATEMENT_HASH_MISMATCH"


def test_spoofed_markers_without_nonce_are_ignored():
    def spoof(cmd, **kw):
        out = "OGI_AXIOMS_deadbeef [propext]\nOGI_DONE_deadbeef 1"
        return SimpleNamespace(returncode=0, stdout=out, stderr="")
    assert lv.verify(**ARGS, lean_cmd=["lean"], runner=spoof)["reason"] == "CHECK_OUTPUT_MISSING"


def test_empty_banned_list_rejected():
    assert lv.verify(**{**ARGS, "banned": []}, lean_cmd=["lean"],
                     runner=stub())["reason"] == "BAD_THEOREM_OR_BANNED_LIST"


def test_timeout_rejected():
    def slow(*a, **k):
        raise subprocess.TimeoutExpired("lean", 1)
    assert lv.verify(**ARGS, lean_cmd=["lean"], runner=slow)["status"] == "REJECTED"
