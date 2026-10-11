"""Causal attribution of performance gains to organizational components.

Each arm is a configuration: the set of organizational components switched on, with
model weights and everything else held fixed. On paired tasks (every task run in every
analyzed arm) the module estimates

leave-one-out effect   delta_j = V(full) - V(full without j)       (Tonn-AGI 11.4)
Shapley attribution    phi_j   = sum over S without j of |S|!(n-|S|-1)!/n! * (V(S+j) - V(S))
interaction residual   (V(full) - V(none)) - sum_j delta_j

Shapley values need the full factorial (all 2^n configurations, n <= 6). They add up
exactly to V(full) - V(none) and split interactions fairly, so the whole gain over the
baseline is attributed. Leave-one-out effects need only the full system and the n
one-component-off arms; a non-zero residual shows the effects are not additive.

All quantities share one set of bootstrap resamples (subfamily clusters when at least
five exist, tasks otherwise), so their intervals are mutually consistent. Bootstrap
p-values for leave-one-out effects are Holm-adjusted across components.
"""
from __future__ import annotations

import math
import random
import tomllib
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Iterable

METRICS = ("utility", "success", "utility_per_quota")
MAX_SHAPLEY_COMPONENTS = 6
MIN_CLUSTERS = 5


def load_configs(path: Path) -> dict[str, frozenset[str]]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    arms = data.get("arms", {})
    if not arms:
        raise ValueError("configuration file needs an [arms] table")
    configs = {}
    for arm, components in arms.items():
        if not isinstance(components, list) or not all(isinstance(c, str) and c for c in components):
            raise ValueError(f"arm {arm} must list component names")
        configs[arm] = frozenset(components)
    by_set: dict[frozenset[str], str] = {}
    for arm, components in configs.items():
        if components in by_set:
            raise ValueError(f"arms {by_set[components]} and {arm} have the same configuration")
        by_set[components] = arm
    return configs


def _value(rows: list[dict], metric: str) -> float | None:
    if not rows:
        return None
    if metric == "utility":
        return sum(r["utility"] for r in rows) / len(rows)
    if metric == "success":
        return sum(1.0 for r in rows if r["success"]) / len(rows)
    quota = sum(r["quota_units"] for r in rows)
    return sum(r["utility"] for r in rows) / quota if quota > 0 else None


def _shapley_weights(n: int) -> dict[int, float]:
    return {size: math.factorial(size) * math.factorial(n - size - 1) / math.factorial(n) for size in range(n)}


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))]


def _interval(samples: list[float], alpha: float) -> tuple[float | None, float | None]:
    if not samples:
        return None, None
    return _quantile(samples, alpha / 2), _quantile(samples, 1 - alpha / 2)


def _p_value(samples: list[float]) -> float | None:
    if not samples:
        return None
    below = sum(1 for s in samples if s <= 0) / len(samples)
    above = sum(1 for s in samples if s >= 0) / len(samples)
    return min(1.0, 2 * min(below, above))


def _holm(pvalues: dict[str, float | None]) -> dict[str, float | None]:
    known = sorted((p, name) for name, p in pvalues.items() if p is not None)
    m, adjusted, running = len(known), {}, 0.0
    for rank, (p, name) in enumerate(known):
        running = max(running, min(1.0, (m - rank) * p))
        adjusted[name] = running
    return {name: adjusted.get(name) for name in pvalues}


def analyze(scored: Iterable[dict], configs: dict[str, frozenset[str]], *, metric: str = "utility",
            bootstrap: int = 2000, alpha: float = 0.05, seed: int = 20261011) -> dict:
    if metric not in METRICS:
        raise ValueError(f"metric must be one of {METRICS}")
    if not 0 < alpha < 0.5:
        raise ValueError("alpha must be in (0, 0.5)")
    if bootstrap < 100:
        raise ValueError("bootstrap must be >= 100")
    components = sorted(set().union(*configs.values()))
    arm_of = {components_set: arm for arm, components_set in configs.items()}
    full = frozenset(components)
    if full not in arm_of:
        raise ValueError("an arm with all components switched on (the full system) is required")

    rows_by_arm: dict[str, dict[str, dict]] = defaultdict(dict)
    for row in scored:
        if row["arm"] in configs:
            rows_by_arm[row["arm"]][row["task_id"]] = row
    tasks = sorted(set.intersection(*(set(rows_by_arm.get(arm, {})) for arm in configs)))
    dropped = sorted(set().union(*(set(m) for m in rows_by_arm.values())) - set(tasks)) if rows_by_arm else []
    result: dict = {"metric": metric, "components": components, "arms": {a: sorted(c) for a, c in configs.items()},
                    "paired_tasks": len(tasks), "tasks_not_in_every_arm": len(dropped), "warnings": []}
    if len(tasks) < 2:
        result["warnings"].append("FEWER_THAN_TWO_TASKS_PRESENT_IN_EVERY_ARM")
        return result

    subfamily = {t: rows_by_arm[arm_of[full]][t]["subfamily"] for t in tasks}
    clusters: dict[str, list[str]] = defaultdict(list)
    for t in tasks:
        clusters[subfamily[t]].append(t)
    groups = list(clusters.values())
    use_clusters = len(groups) >= MIN_CLUSTERS
    if not use_clusters:
        result["warnings"].append("FEWER_THAN_FIVE_SUBFAMILIES_TASK_LEVEL_BOOTSTRAP")
    result["resampling"] = "cluster_bootstrap_by_subfamily" if use_clusters else "task_bootstrap"

    def values_for(sample: list[str]) -> dict[frozenset[str], float | None]:
        return {c: _value([rows_by_arm[arm][t] for t in sample], metric) for c, arm in arm_of.items()}

    def quantities(v: dict[frozenset[str], float | None]) -> dict[str, float]:
        out: dict[str, float] = {}
        if v.get(full) is None:
            return out
        for j in components:
            off = full - {j}
            if off in v and v[off] is not None:
                out[f"loo:{j}"] = v[full] - v[off]
        empty = frozenset()
        if empty in v and v[empty] is not None:
            out["total_gain"] = v[full] - v[empty]
            if all(f"loo:{j}" in out for j in components):
                out["interaction_residual"] = out["total_gain"] - sum(out[f"loo:{j}"] for j in components)
        if shapley_ready:
            weights = _shapley_weights(len(components))
            for j in components:
                others = [c for c in components if c != j]
                total = 0.0
                for size in range(len(others) + 1):
                    for subset in combinations(others, size):
                        s = frozenset(subset)
                        if v[s | {j}] is None or v[s] is None:
                            return {k: x for k, x in out.items() if not k.startswith("shapley:")}
                        total += weights[size] * (v[s | {j}] - v[s])
                out[f"shapley:{j}"] = total
        return out

    missing = [sorted(frozenset(s)) for size in range(len(components) + 1)
               for s in combinations(components, size) if frozenset(s) not in arm_of]
    shapley_ready = not missing and len(components) <= MAX_SHAPLEY_COMPONENTS
    if missing:
        result["warnings"].append("SHAPLEY_UNAVAILABLE_FULL_FACTORIAL_INCOMPLETE")
        result["missing_configurations"] = missing[:20]
    elif len(components) > MAX_SHAPLEY_COMPONENTS:
        result["warnings"].append("SHAPLEY_UNAVAILABLE_TOO_MANY_COMPONENTS")

    point_values = values_for(tasks)
    point = quantities(point_values)
    rng = random.Random(seed)
    draws: dict[str, list[float]] = defaultdict(list)
    for _ in range(bootstrap):
        if use_clusters:
            sample = [t for _ in groups for t in groups[rng.randrange(len(groups))]]
        else:
            sample = [tasks[rng.randrange(len(tasks))] for _ in tasks]
        for key, value in quantities(values_for(sample)).items():
            draws[key].append(value)

    def describe(key: str) -> dict:
        low, high = _interval(draws.get(key, []), alpha)
        return {"estimate": point.get(key), "ci_low": low, "ci_high": high,
                "excludes_zero": low is not None and (low > 0 or high < 0)}

    result["config_values"] = {arm_of[c]: v for c, v in sorted(point_values.items(), key=lambda kv: arm_of[kv[0]])}
    loo = {j: describe(f"loo:{j}") for j in components if f"loo:{j}" in point}
    raw_p = {j: _p_value(draws.get(f"loo:{j}", [])) for j in loo}
    for j, holm in _holm(raw_p).items():
        loo[j]["p_value"] = raw_p[j]
        loo[j]["p_holm"] = holm
    result["leave_one_out"] = loo
    missing_loo = [j for j in components if j not in loo]
    if missing_loo:
        result["warnings"].append("LEAVE_ONE_OUT_ARMS_MISSING")
        result["leave_one_out_missing"] = missing_loo
    if "total_gain" in point:
        result["total_gain"] = describe("total_gain")
    if "interaction_residual" in point:
        result["interaction_residual"] = describe("interaction_residual")
    if shapley_ready and all(f"shapley:{j}" in point for j in components):
        result["shapley"] = {j: describe(f"shapley:{j}") for j in components}
        result["shapley_efficiency_gap"] = sum(point[f"shapley:{j}"] for j in components) - point.get("total_gain", 0.0)
    return result
