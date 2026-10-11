"""Pre-registered utility rubric FSE-RUBRIC/1: one scale in [0, 1] for all task families.

Only evidence observed by a harness or verified externally becomes a label. A worker's
own claim of success raises NotALabel and never enters an evaluation.

SOFTWARE  share of executable tests passed
INQUIRY   blinded grade 0 (wrong), 0.5 (partial) or 1 (correct)
RESEARCH  F1 of claim precision (supported / asserted) and key-point recall
ECONOMIC  outcome score if the correctness audit passed and no penalty event occurred,
          else 0; penalty events (complaint, refund, moderation removal) are reported
          separately by the caller because a [0, 1] label cannot go negative
"""
from __future__ import annotations

import math

RUBRIC_VERSION = "FSE-RUBRIC/1"
ALLOWED_PROVENANCE = frozenset({"HARNESS_OBSERVED", "EXTERNALLY_VERIFIED"})
INQUIRY_GRADES = frozenset({0.0, 0.5, 1.0})


class NotALabel(ValueError):
    """The evidence may not be used as a learning or evaluation label."""


def _count(evidence: dict, key: str) -> int:
    value = evidence.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{key} must be a non-negative integer")
    return value


def _unit(evidence: dict, key: str) -> float:
    value = evidence.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number")
    value = float(value)
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{key} must be in [0, 1]")
    return value


def utility(family: str, evidence: dict) -> float:
    provenance = evidence.get("provenance")
    if provenance not in ALLOWED_PROVENANCE:
        raise NotALabel(f"provenance {provenance!r} is not an admissible label source")
    if family == "SOFTWARE":
        total = _count(evidence, "tests_total")
        passed = _count(evidence, "tests_passed")
        if total == 0 or passed > total:
            raise ValueError("need 0 <= tests_passed <= tests_total and tests_total > 0")
        return passed / total
    if family == "INQUIRY":
        if evidence.get("blinded") is not True:
            raise NotALabel("inquiry grades must come from a grader blinded to the arm")
        grade = _unit(evidence, "grade")
        if grade not in INQUIRY_GRADES:
            raise ValueError("grade must be 0, 0.5 or 1")
        return grade
    if family == "RESEARCH":
        asserted = _count(evidence, "claims_asserted")
        supported = _count(evidence, "claims_supported")
        total = _count(evidence, "key_points_total")
        covered = _count(evidence, "key_points_covered")
        if supported > asserted or total == 0 or covered > total:
            raise ValueError("inconsistent research evidence counts")
        precision = supported / asserted if asserted else 0.0
        recall = covered / total
        return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    if family == "ECONOMIC":
        passed = evidence.get("correctness_audit_passed")
        if not isinstance(passed, bool):
            raise ValueError("correctness_audit_passed must be true or false")
        penalties = _count(evidence, "penalty_events")
        score = _unit(evidence, "outcome_score")
        return score if passed and penalties == 0 else 0.0
    raise ValueError(f"unknown family {family!r}")
