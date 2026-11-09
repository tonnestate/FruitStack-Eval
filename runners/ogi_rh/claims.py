"""OGI-RH claim schema and deterministic promotion gate (design §5, §8.1).

Offline only: no model or provider call. The gate never *creates* evidence; it
only maps a claim plus an optional verifier receipt onto one taxonomy class.

Journal pattern (hash-chained events) copied from
/root/fruits/research/fruitstack-rh-research-v1.2/fruitstack_rh.py (_event /
journal_valid, sha256 4f338bc6...), moved from DuckDB to JSONL so this module has
no dependency beyond the stdlib.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

PROOF = "PROOF"
UNVERIFIED_CANDIDATE = "UNVERIFIED_CANDIDATE"
NUMERICAL_EVIDENCE = "NUMERICAL_EVIDENCE"
REFORMULATION = "REFORMULATION"
KNOWN_RESULT = "KNOWN_RESULT"
CLASSES = (PROOF, UNVERIFIED_CANDIDATE, NUMERICAL_EVIDENCE, REFORMULATION, KNOWN_RESULT)

# What the submitter says the claim is. The gate decides the class.
KINDS = ("proof", "numerical", "reformulation")

KNOWN_RESULTS_PATH = Path(__file__).with_name("known_results.json")

# Frozen RH target, copied verbatim from fruitstack_rh.RH_TARGET["statement"].
RH_STATEMENT = "∀ ρ ∈ ℂ, (ζ(ρ)=0 ∧ 0<Re(ρ) ∧ Re(ρ)<1) → Re(ρ)=1/2"


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def statement_sha256(statement: str) -> str:
    """Hash of a statement with whitespace runs collapsed (only whitespace is normalized)."""
    return sha256_text(" ".join(statement.split()))


def seal(receipt: dict) -> dict:
    """Return the receipt with receipt_sha256 over all other fields."""
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    return {**body, "receipt_sha256": sha256_text(canonical(body))}


def receipt_intact(receipt: dict) -> bool:
    return isinstance(receipt, dict) and seal(receipt).get("receipt_sha256") == receipt.get("receipt_sha256")


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    return " ".join(re.sub(r"[^\w]+", " ", text).split())


def load_known(path: Path = KNOWN_RESULTS_PATH) -> list[dict]:
    return json.loads(Path(path).read_text())["entries"]


def match_known(statement: str, known: list[dict]) -> str | None:
    """Exact match after normalization against statement and aliases.

    ponytail: exact normalized match only; paraphrases are caught by the §5
    retrieval + blinded-judge step, which passes its verdict as known_match_id.
    """
    target = _norm(statement)
    for entry in known:
        if target in {_norm(s) for s in [entry["statement"], *entry.get("aliases", [])]}:
            return entry["id"]
    return None


def receipt_accepts(receipt: dict | None, statement: str) -> tuple[bool, str]:
    """Does this receipt license PROOF for exactly this statement? (§3 tiers 1-2, §5 table)."""
    if receipt is None:
        return False, "NO_RECEIPT"
    if not receipt_intact(receipt):
        return False, "RECEIPT_TAMPERED"
    if receipt.get("statement_sha256") != statement_sha256(statement):
        return False, "RECEIPT_STATEMENT_MISMATCH"
    if receipt.get("status") != "PASS" or receipt.get("passed") is not True:
        return False, f"RECEIPT_NOT_PASS:{receipt.get('status')}"
    tier = receipt.get("verifier_tier")
    if tier == "FORMAL":
        if receipt.get("verifier") != "lean":
            return False, "FORMAL_RECEIPT_NOT_LEAN"
    elif tier == "RIGOROUS_INFORMAL":
        judges = receipt.get("judges") or []
        if len(judges) < 2 or any(j.get("verdict") != "ACCEPT" for j in judges):
            return False, "JUDGES_NOT_UNANIMOUS_OR_FEWER_THAN_2"
        if receipt.get("expert_audit_confirmed") is not True:
            return False, "EXPERT_AUDIT_NOT_CONFIRMED"
    else:
        return False, f"UNKNOWN_TIER:{tier}"
    if _norm(statement) == _norm(RH_STATEMENT) and receipt.get("external_expert_review") is not True:
        return False, "RH_LEVEL_NEEDS_EXTERNAL_EXPERT_REVIEW"
    return True, "ACCEPTED"


def classify(claim: dict, receipt: dict | None = None, *, known: list[dict] | None = None,
             known_match_id: str | None = None) -> dict:
    """Map a claim to exactly one class. Rules, in order:

    1. kind == numerical          -> NUMERICAL_EVIDENCE (never upgraded, receipt ignored)
    2. matches a known result     -> KNOWN_RESULT (recall, never discovery)
    3. kind == reformulation      -> REFORMULATION
    4. proof + accepting receipt  -> PROOF
    5. otherwise                  -> UNVERIFIED_CANDIDATE, which requires open_step
    """
    kind = claim.get("kind")
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    statement = claim["statement"]
    if known is None:
        known = load_known()
    match = known_match_id or match_known(statement, known)
    accepted, reason = receipt_accepts(receipt, statement)

    if kind == "numerical":
        cls = NUMERICAL_EVIDENCE
    elif match:
        cls = KNOWN_RESULT
    elif kind == "reformulation":
        cls = REFORMULATION
    elif accepted:
        cls = PROOF
    else:
        cls = UNVERIFIED_CANDIDATE
    if cls == UNVERIFIED_CANDIDATE and not (claim.get("open_step") or "").strip():
        raise ValueError("UNVERIFIED_CANDIDATE requires open_step (the first unresolved step)")

    return {
        "claim_id": claim["claim_id"],
        "statement": statement,
        "statement_sha256": statement_sha256(statement),
        "claim_class": cls,
        "verifier_tier": receipt.get("verifier_tier") if (receipt and cls == PROOF) else None,
        "verifier_receipt": receipt.get("receipt_sha256") if receipt else None,
        "gate_reason": reason,
        "unresolved_step": claim.get("open_step") if cls == UNVERIFIED_CANDIDATE else None,
        "novelty_class": "KNOWN" if match else "UNCHECKED",
        "known_result_id": match,
        "evidence_refs": list(claim.get("evidence_refs", [])),
        "lineage": claim.get("lineage"),
    }


def _event_hash(seq: int, event_type: str, object_id: str, body: str, previous: str) -> str:
    return sha256_text(f"{seq}|{event_type}|{object_id}|{body}|{previous}")


def append_event(journal: Path, event_type: str, object_id: str, payload: dict) -> dict:
    journal = Path(journal)
    lines = journal.read_text().splitlines() if journal.exists() else []
    prior = json.loads(lines[-1]) if lines else None
    seq, previous = (prior["seq"] + 1, prior["event_hash"]) if prior else (1, "0" * 64)
    body = canonical(payload)
    event = {"seq": seq, "event_type": event_type, "object_id": object_id, "payload_json": body,
             "previous_hash": previous, "event_hash": _event_hash(seq, event_type, object_id, body, previous)}
    with journal.open("a") as fh:
        fh.write(canonical(event) + "\n")
    return event


def record_claim(journal: Path, row: dict) -> dict:
    if row.get("claim_class") not in CLASSES:
        raise ValueError("row must come from classify()")
    return append_event(journal, "CLAIM_CLASSIFIED", row["claim_id"], row)


def journal_valid(journal: Path) -> bool:
    previous = "0" * 64
    for expected_seq, line in enumerate(Path(journal).read_text().splitlines(), 1):
        e = json.loads(line)
        digest = _event_hash(e["seq"], e["event_type"], e["object_id"], e["payload_json"], previous)
        if e["seq"] != expected_seq or e["previous_hash"] != previous or e["event_hash"] != digest:
            return False
        previous = digest
    return True
