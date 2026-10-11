"""Independent off-policy evaluation with the support rules of protocol section 5.3.

Estimators: IPS and self-normalized IPS (SNIPS) over logged decisions that carry the
propensity of the behavior policy at decision time and later, independently verified
utility in [0, 1]. Added over the system's own evaluator:

- importance-weight clipping (introduces bias toward the behavior policy; reported),
- minimum logged support per action the target policy would take,
- a seeded percentile bootstrap interval for SNIPS,
- evaluation of consumer-owned ENSEMBLE decisions (fixed worker counts),
- a promotion review that only reports eligibility; promotion stays a host decision.
"""
from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Iterable

from .decision_log import DecisionView

SELECTORS = ("deterministic", "epsilon_floor", "fixed_count")


@dataclass(frozen=True)
class TargetPolicy:
    selector: str = "deterministic"
    epsilon: float = 0.0
    max_candidates: int | None = None
    count: int | None = None

    def __post_init__(self) -> None:
        if self.selector not in SELECTORS:
            raise ValueError(f"selector must be one of {SELECTORS}")
        if not 0.0 <= self.epsilon <= 1.0:
            raise ValueError("epsilon must be in [0, 1]")
        if self.max_candidates is not None and self.max_candidates < 1:
            raise ValueError("max_candidates must be >= 1")
        if self.selector == "fixed_count":
            if self.count is None or not 0 <= self.count <= 4:
                raise ValueError("fixed_count needs count in 0..4")
        elif self.count is not None:
            raise ValueError("count applies only to the fixed_count selector")

    @property
    def decision_kind(self) -> str:
        return "ENSEMBLE" if self.selector == "fixed_count" else "ACQUIRE"

    @classmethod
    def from_dict(cls, data: dict) -> "TargetPolicy":
        return cls(**data)


@dataclass(frozen=True)
class OPEConfig:
    clip: float = 10.0
    min_support: int = 30
    min_ess: float = 100.0
    family_key: str = "task_family"
    family: str | None = None
    bootstrap: int = 2000
    confidence: float = 0.95
    seed: int = 20261011

    def __post_init__(self) -> None:
        if self.clip < 1.0:
            raise ValueError("clip must be >= 1")
        if self.min_support < 1:
            raise ValueError("min_support must be >= 1")
        if self.min_ess <= 0:
            raise ValueError("min_ess must be positive")
        if self.bootstrap < 0:
            raise ValueError("bootstrap must be >= 0")
        if not 0.5 < self.confidence < 1.0:
            raise ValueError("confidence must be in (0.5, 1)")


@dataclass(frozen=True)
class _Row:
    utility: float
    target_p: float
    behavior_p: float
    action: str


@dataclass
class OPEResult:
    target_policy: dict
    config: dict
    labelled_decisions: int
    usable_decisions: int
    ips: float | None = None
    snips: float | None = None
    ci_low: float | None = None
    ci_high: float | None = None
    behavior_mean_utility: float | None = None
    effective_sample_size: float = 0.0
    clipped_weights: int = 0
    max_raw_weight: float | None = None
    support_by_action: dict[str, int] = field(default_factory=dict)
    insufficient_support: dict[str, int] = field(default_factory=dict)
    exclusions: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _acquire_target_probability(choice: dict, policy: TargetPolicy) -> float:
    pool = list(choice.get("admissible_offer_ids") or [])
    if policy.max_candidates is not None:
        pool = pool[: policy.max_candidates]
    offer = choice.get("offer_id")
    if not pool or offer not in pool:
        return 0.0
    if policy.selector == "deterministic" or policy.epsilon == 0.0 or len(pool) == 1:
        return 1.0 if offer == pool[0] else 0.0
    share = policy.epsilon / len(pool)
    return share + ((1.0 - policy.epsilon) if offer == pool[0] else 0.0)


def _extract(views: list[DecisionView], policy: TargetPolicy, config: OPEConfig) -> tuple[list[_Row], Counter, int]:
    exclusions: Counter = Counter()
    rows: list[_Row] = []
    labelled = 0
    for view in views:
        decision = view.decision
        feedback = view.latest_feedback()
        if feedback is None:
            exclusions["NO_VERIFIED_FEEDBACK"] += 1
            continue
        labelled += 1
        try:
            utility = float(feedback.get("verified_utility"))
        except (TypeError, ValueError):
            exclusions["INVALID_UTILITY"] += 1
            continue
        if not math.isfinite(utility) or not 0.0 <= utility <= 1.0:
            exclusions["UTILITY_OUT_OF_RANGE"] += 1
            continue
        features = decision.get("request_features") or {}
        if config.family is not None and features.get(config.family_key) != config.family:
            exclusions["OTHER_FAMILY"] += 1
            continue
        if decision.get("kind") != policy.decision_kind:
            exclusions[f"NOT_{policy.decision_kind}"] += 1
            continue
        if policy.decision_kind == "ACQUIRE":
            choices = decision.get("choices") or []
            if len(choices) != 1:
                exclusions["MULTI_SLOT_UNSUPPORTED"] += 1
                continue
            choice = choices[0]
            if choice.get("behavior_mode") == "PINNED" or features.get("pinned"):
                exclusions["PINNED"] += 1
                continue
            behavior = choice.get("propensity")
            action = str(choice.get("offer_id"))
            target = _acquire_target_probability(choice, policy)
        else:
            ensemble = decision.get("ensemble_choice")
            if not isinstance(ensemble, dict):
                exclusions["NO_ENSEMBLE_CHOICE"] += 1
                continue
            behavior = ensemble.get("propensity")
            action = str(ensemble.get("worker_count"))
            target = 1.0 if ensemble.get("worker_count") == policy.count else 0.0
        try:
            behavior = float(behavior)
        except (TypeError, ValueError):
            exclusions["INVALID_PROPENSITY"] += 1
            continue
        if not math.isfinite(behavior) or not 0.0 < behavior <= 1.0:
            exclusions["INVALID_PROPENSITY"] += 1
            continue
        rows.append(_Row(utility, target, behavior, action))
    return rows, exclusions, labelled


def _snips(pairs: list[tuple[_Row, float]]) -> float | None:
    total = sum(weight for _row, weight in pairs)
    if total <= 0:
        return None
    return sum(weight * row.utility for row, weight in pairs) / total


def _bootstrap_interval(pairs: list[tuple[_Row, float]], config: OPEConfig) -> tuple[float | None, float | None]:
    rng = random.Random(config.seed)
    n = len(pairs)
    stats: list[float] = []
    for _ in range(config.bootstrap):
        value = _snips([pairs[rng.randrange(n)] for _ in range(n)])
        if value is not None:
            stats.append(value)
    if len(stats) < max(10, config.bootstrap // 2):
        return None, None
    stats.sort()
    tail = (1.0 - config.confidence) / 2.0
    low = stats[math.floor(tail * (len(stats) - 1))]
    high = stats[math.ceil((1.0 - tail) * (len(stats) - 1))]
    return low, high


def evaluate(views: Iterable[DecisionView], policy: TargetPolicy, config: OPEConfig | None = None) -> OPEResult:
    config = config or OPEConfig()
    rows, exclusions, labelled = _extract(list(views), policy, config)
    result = OPEResult(target_policy=asdict(policy), config=asdict(config), labelled_decisions=labelled,
                       usable_decisions=len(rows), exclusions=dict(exclusions))
    if not rows:
        result.warnings.append("NO_USABLE_LABELLED_DECISIONS")
        return result
    raw = [row.target_p / row.behavior_p for row in rows]
    weights = [min(value, config.clip) for value in raw]
    pairs = list(zip(rows, weights))
    total = sum(weights)
    squares = sum(weight * weight for weight in weights)
    result.ips = sum(weight * row.utility for row, weight in pairs) / len(rows)
    result.snips = _snips(pairs)
    result.behavior_mean_utility = sum(row.utility for row in rows) / len(rows)
    result.effective_sample_size = (total * total / squares) if squares > 0 else 0.0
    result.clipped_weights = sum(1 for before, after in zip(raw, weights) if after < before)
    result.max_raw_weight = max(raw)
    support = Counter(row.action for row in rows if row.target_p > 0.0)
    result.support_by_action = dict(sorted(support.items()))
    result.insufficient_support = {action: count for action, count in sorted(support.items())
                                   if count < config.min_support}
    if result.snips is not None and config.bootstrap > 0:
        result.ci_low, result.ci_high = _bootstrap_interval(pairs, config)
    if not support:
        result.warnings.append("TARGET_HAS_NO_SUPPORT_IN_LOGS")
    if result.insufficient_support:
        result.warnings.append("INSUFFICIENT_ACTION_SUPPORT")
    if result.effective_sample_size < config.min_ess:
        result.warnings.append("LOW_EFFECTIVE_SAMPLE_SIZE")
    if result.clipped_weights:
        result.warnings.append("WEIGHTS_CLIPPED_ESTIMATE_BIASED_TOWARD_BEHAVIOR")
    return result


PROMOTION_RULE = ("candidate SNIPS lower bound must exceed the incumbent SNIPS estimate on held-out "
                  "families, with sufficient effective sample size and action support; "
                  "promotion itself remains a host decision")


def promotion_review(candidate: OPEResult, incumbent: OPEResult, config: OPEConfig | None = None) -> dict:
    config = config or OPEConfig()
    reasons: list[str] = []
    if candidate.ci_low is None:
        reasons.append("CANDIDATE_HAS_NO_INTERVAL")
    if incumbent.snips is None:
        reasons.append("INCUMBENT_HAS_NO_ESTIMATE")
    if candidate.effective_sample_size < config.min_ess:
        reasons.append("CANDIDATE_ESS_BELOW_MINIMUM")
    if candidate.insufficient_support or not candidate.support_by_action:
        reasons.append("CANDIDATE_ACTION_SUPPORT_BELOW_MINIMUM")
    if not reasons and candidate.ci_low <= incumbent.snips:
        reasons.append("CANDIDATE_LOWER_BOUND_NOT_ABOVE_INCUMBENT")
    return {
        "eligible_for_host_review": not reasons,
        "reasons": reasons,
        "rule": PROMOTION_RULE,
        "candidate_snips": candidate.snips,
        "candidate_ci_low": candidate.ci_low,
        "incumbent_snips": incumbent.snips,
    }
