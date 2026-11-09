import json

import pytest

from ogi_rh import claims as c

KNOWN = c.load_known()


def proof(statement="For all x, P(x).", **kw):
    return {"claim_id": "C1", "statement": statement, "kind": "proof", "lineage": "L1",
            "open_step": "step 3 bound", **kw}


def lean_pass(statement, **kw):
    return c.seal({"verifier": "lean", "verifier_tier": "FORMAL", "status": "PASS", "passed": True,
                   "statement_sha256": c.statement_sha256(statement), **kw})


def informal_pass(statement, judges=("ACCEPT", "ACCEPT"), audit=True):
    return c.seal({"verifier": "panel", "verifier_tier": "RIGOROUS_INFORMAL", "status": "PASS",
                   "passed": True, "statement_sha256": c.statement_sha256(statement),
                   "judges": [{"id": f"j{i}", "verdict": v} for i, v in enumerate(judges)],
                   "expert_audit_confirmed": audit})


def test_proof_without_receipt_stays_candidate_with_open_step():
    row = c.classify(proof(), known=KNOWN)
    assert row["claim_class"] == c.UNVERIFIED_CANDIDATE
    assert row["unresolved_step"] == "step 3 bound" and row["gate_reason"] == "NO_RECEIPT"


def test_candidate_requires_open_step():
    with pytest.raises(ValueError, match="open_step"):
        c.classify(proof(open_step=""), known=KNOWN)


def test_lean_receipt_promotes_to_proof():
    s = "For all x, P(x)."
    row = c.classify(proof(s), lean_pass(s), known=KNOWN)
    assert row["claim_class"] == c.PROOF and row["verifier_tier"] == "FORMAL"
    assert row["unresolved_step"] is None


def test_rigorous_informal_receipt_needs_two_unanimous_judges_and_audit():
    s = "For all x, P(x)."
    assert c.classify(proof(s), informal_pass(s), known=KNOWN)["claim_class"] == c.PROOF
    for bad in (informal_pass(s, judges=("ACCEPT",)), informal_pass(s, judges=("ACCEPT", "REJECT")),
                informal_pass(s, audit=False)):
        assert c.classify(proof(s), bad, known=KNOWN)["claim_class"] == c.UNVERIFIED_CANDIDATE


@pytest.mark.parametrize("mutate", [
    lambda r: {**r, "status": "VERIFIER_UNAVAILABLE", "passed": False},           # resealed below
    lambda r: {**r, "verifier": "model-judge"},
    lambda r: {**r, "verifier_tier": "NUMERICAL"},
])
def test_non_accepting_receipts_do_not_promote(mutate):
    s = "For all x, P(x)."
    receipt = c.seal(mutate(lean_pass(s)))
    assert c.classify(proof(s), receipt, known=KNOWN)["claim_class"] == c.UNVERIFIED_CANDIDATE


def test_tampered_or_mismatched_receipt_does_not_promote():
    s = "For all x, P(x)."
    tampered = {**lean_pass("other"), "statement_sha256": c.statement_sha256(s)}
    assert c.classify(proof(s), tampered, known=KNOWN)["gate_reason"] == "RECEIPT_TAMPERED"
    row = c.classify(proof(s), lean_pass("A weaker statement."), known=KNOWN)
    assert row["claim_class"] == c.UNVERIFIED_CANDIDATE
    assert row["gate_reason"] == "RECEIPT_STATEMENT_MISMATCH"


def test_numerical_claim_never_becomes_proof_even_with_receipt():
    s = "The first 10 zeros lie on the critical line."
    row = c.classify({"claim_id": "N1", "statement": s, "kind": "numerical"}, lean_pass(s), known=KNOWN)
    assert row["claim_class"] == c.NUMERICAL_EVIDENCE and row["verifier_tier"] is None


def test_known_result_becomes_known_result_even_with_valid_receipt():
    s = "ζ has infinitely many zeros on the critical line Re(s) = 1/2."
    row = c.classify(proof(s), lean_pass(s), known=KNOWN)
    assert row["claim_class"] == c.KNOWN_RESULT
    assert row["known_result_id"] == "K-HARDY-INFINITELY-MANY" and row["novelty_class"] == "KNOWN"
    alias = c.classify(proof("Hardy's theorem"), known=KNOWN)
    assert alias["claim_class"] == c.KNOWN_RESULT


def test_judge_supplied_known_match_and_reformulation():
    row = c.classify(proof("A paraphrase of Selberg."), known=KNOWN,
                     known_match_id="K-SELBERG-POSITIVE-PROPORTION")
    assert row["claim_class"] == c.KNOWN_RESULT
    ref = c.classify({"claim_id": "R1", "statement": "RH iff Q holds.", "kind": "reformulation"},
                     known=KNOWN)
    assert ref["claim_class"] == c.REFORMULATION and ref["novelty_class"] == "UNCHECKED"


def test_rh_level_proof_needs_external_expert_review():
    s = c.RH_STATEMENT
    assert c.classify(proof(s), lean_pass(s), known=KNOWN)["gate_reason"] == \
        "RH_LEVEL_NEEDS_EXTERNAL_EXPERT_REVIEW"
    assert c.classify(proof(s), lean_pass(s, external_expert_review=True),
                      known=KNOWN)["claim_class"] == c.PROOF


def test_unknown_kind_rejected():
    with pytest.raises(ValueError):
        c.classify({"claim_id": "X", "statement": "s", "kind": "PROOF"}, known=KNOWN)


def test_journal_hash_chain_detects_edits(tmp_path):
    j = tmp_path / "claims.jsonl"
    c.record_claim(j, c.classify(proof(), known=KNOWN))
    c.record_claim(j, c.classify(proof("Hardy's theorem"), known=KNOWN))
    assert c.journal_valid(j)
    lines = j.read_text().splitlines()
    event = json.loads(lines[0])
    event["payload_json"] = event["payload_json"].replace("UNVERIFIED_CANDIDATE", "PROOF")
    j.write_text("\n".join([json.dumps(event), lines[1]]) + "\n")
    assert not c.journal_valid(j)


def test_known_results_list_is_marked_unverified_and_well_formed():
    assert len(KNOWN) >= 40
    assert len({e["id"] for e in KNOWN}) == len(KNOWN)
    for e in KNOWN:
        assert e["citation_status"] == "UNVERIFIED_OFFLINE"
        assert e["statement"] and isinstance(e["citation"], str)
        assert "doi" not in e["citation"].lower()
