"""Replay of the primary comparison from raw evidence (gate G6, hypothesis H4).

Each result row holds raw evidence, not a precomputed score, so every number in a
report can be recomputed with the pre-registered rubric. Row format (JSON lines):

{"task_id": ..., "arm": ..., "family": ..., "subfamily": ..., "evidence": {...},
 "quota_units": float, "cost_eur": float, "wall_seconds": float}

H4 is a paired non-inferiority test on verified success with a one-sided percentile
bootstrap, resampling subfamilies (clusters) when at least five exist and tasks
otherwise. Parity additionally requires a lower cost per verified success.
"""
from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Iterable

from .rubric import NotALabel, utility

MIN_CLUSTERS = 5


def _number(row: dict, key: str) -> float:
    value = row.get(key, 0.0)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{key} must be a non-negative number")
    return float(value)


def score_rows(rows: Iterable[dict], success_threshold: float = 1.0) -> tuple[list[dict], dict[str, int]]:
    """Attach rubric utility and success; rows without an admissible label are excluded."""
    if not 0.0 < success_threshold <= 1.0:
        raise ValueError("success_threshold must be in (0, 1]")
    scored: list[dict] = []
    excluded: dict[str, int] = defaultdict(int)
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row.get("arm"), row.get("task_id"))
        if not all(isinstance(part, str) and part for part in key):
            raise ValueError("every row needs a non-empty arm and task_id")
        if key in seen:
            raise ValueError(f"duplicate result for arm {key[0]} task {key[1]}")
        seen.add(key)
        try:
            value = utility(row.get("family"), row.get("evidence") or {})
        except NotALabel:
            excluded["NOT_A_LABEL"] += 1
            continue
        scored.append({
            "task_id": row["task_id"], "arm": row["arm"], "subfamily": str(row.get("subfamily") or "unknown"),
            "utility": value, "success": value >= success_threshold,
            "quota_units": _number(row, "quota_units"), "cost_eur": _number(row, "cost_eur"),
            "wall_seconds": _number(row, "wall_seconds"),
        })
    return scored, dict(excluded)


def summarize_arms(scored: Iterable[dict]) -> dict[str, dict]:
    by_arm: dict[str, list[dict]] = defaultdict(list)
    for row in scored:
        by_arm[row["arm"]].append(row)
    summary: dict[str, dict] = {}
    for arm, rows in sorted(by_arm.items()):
        utility_sum = sum(r["utility"] for r in rows)
        successes = sum(1 for r in rows if r["success"])
        quota = sum(r["quota_units"] for r in rows)
        cost = sum(r["cost_eur"] for r in rows)
        summary[arm] = {
            "labelled_tasks": len(rows),
            "mean_utility": utility_sum / len(rows),
            "success_rate": successes / len(rows),
            "utility_per_quota_unit": utility_sum / quota if quota > 0 else None,
            "cost_eur": cost,
            "cost_per_success_eur": cost / successes if successes else None,
            "mean_wall_seconds": sum(r["wall_seconds"] for r in rows) / len(rows),
        }
    return summary


def _percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[math.floor(q * (len(ordered) - 1))]


def paired_noninferiority(scored: Iterable[dict], new_arm: str, reference_arm: str, margin: float, *,
                          alpha: float = 0.025, bootstrap: int = 2000, seed: int = 20261011) -> dict:
    if not 0.0 < margin < 1.0:
        raise ValueError("margin must be in (0, 1)")
    if not 0.0 < alpha < 0.5:
        raise ValueError("alpha must be in (0, 0.5)")
    if bootstrap < 100:
        raise ValueError("bootstrap must be >= 100")
    scored = list(scored)
    by_arm = {arm: {r["task_id"]: r for r in scored if r["arm"] == arm} for arm in (new_arm, reference_arm)}
    common = sorted(set(by_arm[new_arm]) & set(by_arm[reference_arm]))
    result: dict = {"new_arm": new_arm, "reference_arm": reference_arm, "margin": margin, "alpha": alpha,
                    "pairs": len(common), "warnings": []}
    if len(common) < 2:
        result.update(non_inferior=False, verdict="INSUFFICIENT_PAIRS")
        result["warnings"].append("FEWER_THAN_TWO_PAIRED_TASKS")
        return result
    clusters: dict[str, list[float]] = defaultdict(list)
    diffs: list[float] = []
    for task_id in common:
        new, ref = by_arm[new_arm][task_id], by_arm[reference_arm][task_id]
        diff = float(new["success"]) - float(ref["success"])
        diffs.append(diff)
        clusters[new["subfamily"]].append(diff)
    rng = random.Random(seed)
    means: list[float] = []
    if len(clusters) >= MIN_CLUSTERS:
        method = "cluster_bootstrap_by_subfamily"
        groups = list(clusters.values())
        for _ in range(bootstrap):
            sample = [d for _ in groups for d in groups[rng.randrange(len(groups))]]
            means.append(sum(sample) / len(sample))
    else:
        method = "task_bootstrap"
        result["warnings"].append("FEWER_THAN_FIVE_SUBFAMILIES_TASK_LEVEL_BOOTSTRAP")
        for _ in range(bootstrap):
            sample = [diffs[rng.randrange(len(diffs))] for _ in diffs]
            means.append(sum(sample) / len(sample))
    lower = _percentile(means, alpha)
    common_ids = set(common)
    summary = summarize_arms([r for r in scored if r["task_id"] in common_ids
                              and r["arm"] in (new_arm, reference_arm)])
    new_cost = summary.get(new_arm, {}).get("cost_per_success_eur")
    ref_cost = summary.get(reference_arm, {}).get("cost_per_success_eur")
    cheaper = new_cost is not None and ref_cost is not None and new_cost < ref_cost
    non_inferior = lower > -margin
    result.update({
        "method": method,
        "clusters": len(clusters),
        "discordance": sum(1 for d in diffs if d != 0.0) / len(diffs),
        "mean_success_difference": sum(diffs) / len(diffs),
        "one_sided_lower_bound": lower,
        "non_inferior": non_inferior,
        "cost_per_success_eur": {new_arm: new_cost, reference_arm: ref_cost},
        "cheaper_per_success": cheaper,
        "verdict": "PARITY_SUPPORTED" if non_inferior and cheaper else "PARITY_NOT_SUPPORTED",
    })
    return result
