"""Readiness gate G5: completeness of the run logs, checked field by field.

G5 needs, for every run, decisions with the propensities they had at decision time,
per-call model fingerprints, quota consumption, cost, evidence and human
interventions, sealed so that later edits are detectable. This module checks a
DecisionLog export and a typed intervention log for exactly that. A field that is
absent counts as missing; nothing is inferred or filled in.
"""
from __future__ import annotations

import math
from collections import Counter
from pathlib import Path
from typing import Iterable

from . import interventions as interventions_mod
from .costaudit import DEFAULT_ALLOWED
from .decision_log import DecisionView

DECISION_FIELDS = ("decision_id", "created_at", "kind", "policy_name", "policy_version", "selector_name",
                   "eligible_offer_ids", "hard_rejected", "candidates", "request_features")
CHOICE_FIELDS = ("slot", "offer_id", "behavior_mode", "propensity", "admissible_offer_ids")
ENSEMBLE_FIELDS = ("topology", "worker_count", "available_counts", "propensity", "probability_basis")
FEEDBACK_FIELDS = ("feedback_id", "decision_id", "epistemic_state", "verified_utility", "verifier", "recorded_at")
EXECUTED_OUTCOME_FIELDS = ("receipt_id", "executed_offer_id", "model_fingerprint", "input_tokens", "output_tokens",
                           "latency_ms")
MAX_EXAMPLES = 20


def _missing(obj: dict, fields: Iterable[str]) -> list[str]:
    return [f for f in fields if obj.get(f) is None]


def _propensity_ok(value) -> bool:
    return (not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
            and 0.0 < float(value) <= 1.0)


class _Problems:
    def __init__(self) -> None:
        self.counts: Counter = Counter()
        self.examples: list[dict] = []

    def add(self, code: str, **context) -> None:
        self.counts[code] += 1
        if len(self.examples) < MAX_EXAMPLES:
            self.examples.append({"code": code, **context})


def check_decision_log(views: Iterable[DecisionView], log_warnings: list[str], *,
                       expect_cost_policy: str | None = None,
                       free_classes: Iterable[str] = DEFAULT_ALLOWED) -> dict:
    free = frozenset(free_classes)
    problems = _Problems()
    kinds: Counter = Counter()
    stats = Counter()
    fingerprints: set[str] = set()
    verifiers: Counter = Counter()
    for view in views:
        d = view.decision
        stats["decisions"] += 1
        kinds[d.get("kind")] += 1
        for f in _missing(d, DECISION_FIELDS):
            problems.add("DECISION_FIELD_MISSING", decision_id=d.get("decision_id"), field=f)
        policy = (d.get("request_features") or {}).get("cost_policy")
        if policy is None:
            problems.add("COST_POLICY_NOT_RECORDED", decision_id=d.get("decision_id"))
        elif expect_cost_policy and policy != expect_cost_policy:
            problems.add("UNEXPECTED_COST_POLICY", decision_id=d.get("decision_id"), found=policy)
        candidates = {c.get("offer_id"): c for c in d.get("candidates") or [] if isinstance(c, dict)}
        chosen = set()
        if d.get("kind") == "ENSEMBLE":
            choice = d.get("ensemble_choice")
            if not isinstance(choice, dict):
                problems.add("ENSEMBLE_CHOICE_MISSING", decision_id=d.get("decision_id"))
            else:
                for f in _missing(choice, ENSEMBLE_FIELDS):
                    problems.add("ENSEMBLE_FIELD_MISSING", decision_id=d.get("decision_id"), field=f)
                if not _propensity_ok(choice.get("propensity")):
                    problems.add("PROPENSITY_INVALID", decision_id=d.get("decision_id"))
        else:
            choices = d.get("choices") or []
            if d.get("selector_name") == "PINNED_DENIED":
                stats["pinned_denied"] += 1
            elif not choices and d.get("eligible_offer_ids"):
                problems.add("NO_CHOICE_DESPITE_ELIGIBLE_OFFERS", decision_id=d.get("decision_id"))
            for choice in choices:
                stats["choices"] += 1
                for f in _missing(choice, CHOICE_FIELDS):
                    problems.add("CHOICE_FIELD_MISSING", decision_id=d.get("decision_id"), field=f)
                if not _propensity_ok(choice.get("propensity")):
                    problems.add("PROPENSITY_INVALID", decision_id=d.get("decision_id"), slot=choice.get("slot"))
                offer = choice.get("offer_id")
                chosen.add(offer)
                candidate = candidates.get(offer)
                if candidate is None:
                    problems.add("CHOSEN_OFFER_WITHOUT_CANDIDATE_RECORD", decision_id=d.get("decision_id"), offer_id=offer)
                elif candidate.get("cost_class") is None:
                    problems.add("COST_CLASS_MISSING", decision_id=d.get("decision_id"), offer_id=offer)
        for outcome in view.outcomes:
            stats["outcomes"] += 1
            executed = outcome.get("executed_offer_id") is not None or outcome.get("structural_state") != "FAILED"
            if not executed:
                stats["outcomes_not_executed"] += 1
                continue
            stats["outcomes_executed"] += 1
            for f in _missing(outcome, EXECUTED_OUTCOME_FIELDS):
                problems.add("OUTCOME_FIELD_MISSING", decision_id=d.get("decision_id"),
                             receipt_id=outcome.get("receipt_id"), field=f)
            if outcome.get("model_fingerprint"):
                fingerprints.add(outcome["model_fingerprint"])
            offer = outcome.get("executed_offer_id")
            if offer is not None and chosen and offer not in chosen:
                problems.add("EXECUTED_OFFER_NOT_CHOSEN", decision_id=d.get("decision_id"), offer_id=offer)
            cost_class = (candidates.get(offer) or {}).get("cost_class")
            if outcome.get("actual_cost_usd") is None:
                if cost_class in free:
                    problems.add("COST_UNKNOWN_FOR_FREE_OFFER", decision_id=d.get("decision_id"),
                                 receipt_id=outcome.get("receipt_id"), cost_class=cost_class)
                else:
                    problems.add("COST_UNKNOWN_FOR_NON_FREE_OFFER", decision_id=d.get("decision_id"),
                                 receipt_id=outcome.get("receipt_id"), cost_class=cost_class)
        for fb in view.feedback:
            stats["feedback"] += 1
            for f in _missing(fb, FEEDBACK_FIELDS):
                problems.add("FEEDBACK_FIELD_MISSING", feedback_id=fb.get("feedback_id"), field=f)
            utility = fb.get("verified_utility")
            if not isinstance(utility, (int, float)) or isinstance(utility, bool) or not 0.0 <= utility <= 1.0:
                problems.add("FEEDBACK_UTILITY_OUT_OF_RANGE", feedback_id=fb.get("feedback_id"))
            if fb.get("verifier"):
                verifiers[fb["verifier"]] += 1
    for warning in log_warnings:
        problems.add("LOG_WARNING", detail=warning)
    return {
        "stats": dict(stats), "kinds": dict(kinds), "distinct_fingerprints": len(fingerprints),
        "verifiers": dict(verifiers), "problem_counts": dict(problems.counts), "problem_examples": problems.examples,
    }


def check(views: Iterable[DecisionView], log_warnings: list[str], *, interventions_path: Path | None,
          seal_result: dict | None = None, expect_cost_policy: str | None = None,
          require_feedback: bool = False) -> dict:
    """G5 verdict. Missing evidence is reported as a blocker, never as a pass."""
    log = check_decision_log(views, log_warnings, expect_cost_policy=expect_cost_policy)
    blockers = []
    stats = log["stats"]
    if not stats.get("decisions"):
        blockers.append("NO_DECISIONS")
    if not stats.get("outcomes_executed"):
        blockers.append("NO_EXECUTED_OUTCOMES")
    if log["problem_counts"]:
        blockers.append("FIELD_PROBLEMS")
    if require_feedback and not stats.get("feedback"):
        blockers.append("NO_VERIFIED_FEEDBACK")
    interventions = {"present": False}
    if interventions_path is None or not Path(interventions_path).exists():
        blockers.append("NO_INTERVENTION_LOG")
    else:
        items, warnings = interventions_mod.load(Path(interventions_path))
        interventions = {"present": True, "entries": len(items), "warnings": warnings,
                         "summary": interventions_mod.summarize(items, None)}
        if warnings:
            blockers.append("INTERVENTION_LOG_INVALID_ROWS")
    if seal_result is None:
        blockers.append("NOT_SEALED")
    elif not seal_result.get("passed"):
        blockers.append("SEAL_CHECK_FAILED")
    return {"gate": "G5", "passed": not blockers, "blockers": blockers, "decision_log": log,
            "interventions": interventions, "seal": seal_result}
