"""Post-hoc zero-cost audit over a PlumMe DecisionLog export (readiness gate G3).

The audit verifies; it does not enforce. Enforcement belongs in the system's own
eligibility gate. Every chosen offer must carry an allowed cost class, and no executed
outcome may report a positive billed cost.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable

from .decision_log import DecisionView

DEFAULT_ALLOWED = frozenset({"ANONYMOUS_FREE", "FREE_TIER"})


@dataclass
class CostAuditResult:
    allowed_cost_classes: list[str]
    decisions_audited: int = 0
    choices_audited: int = 0
    outcomes_audited: int = 0
    violations: list[dict] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.choices_audited > 0 and not self.violations

    def to_dict(self) -> dict:
        data = asdict(self)
        data["passed"] = self.passed
        return data


def audit(views: Iterable[DecisionView], allowed: Iterable[str] = DEFAULT_ALLOWED) -> CostAuditResult:
    allowed_set = frozenset(allowed)
    result = CostAuditResult(allowed_cost_classes=sorted(allowed_set))
    for view in views:
        decision = view.decision
        result.decisions_audited += 1
        candidates = {c.get("offer_id"): c for c in decision.get("candidates") or [] if isinstance(c, dict)}
        for choice in decision.get("choices") or []:
            result.choices_audited += 1
            offer_id = choice.get("offer_id")
            candidate = candidates.get(offer_id)
            cost_class = candidate.get("cost_class") if candidate else None
            if cost_class not in allowed_set:
                result.violations.append({
                    "decision_id": view.decision_id,
                    "offer_id": offer_id,
                    "cost_class": cost_class or "MISSING_CANDIDATE_RECORD",
                    "reason": "CHOSEN_OFFER_NOT_FREE",
                })
        for outcome in view.outcomes:
            result.outcomes_audited += 1
            cost = outcome.get("actual_cost_usd")
            if isinstance(cost, (int, float)) and cost > 0:
                result.violations.append({
                    "decision_id": view.decision_id,
                    "receipt_id": outcome.get("receipt_id"),
                    "actual_cost_usd": cost,
                    "reason": "BILLED_OUTCOME",
                })
    return result
