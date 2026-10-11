"""Pilot estimation (FRUITSTACK-EVAL-001 phase 3): effect sizes, variances, discordance
and a sample-size proposal for the confirmatory round. Descriptive only.

The pilot cannot confirm anything (protocol §5.4), so this module reports no p-values
and no verdicts. It estimates, for every pair of arms on the tasks both completed,
the success-rate difference and the mean utility difference with cluster-bootstrap
intervals, the share of discordant task pairs psi, and the per-task utility variance.
From psi it proposes paired sample sizes for the H4 non-inferiority test at the
pre-registered margins. The proposal becomes binding only when the owner freezes and
deposits it (gate G7).

It also counts what the protocol requires to be reported, per arm: successes,
failures (graded 0), unverifiable tasks (no admissible label), missing answers,
unparseable answers and abstentions.
"""
from __future__ import annotations

import math
import random
from collections import defaultdict
from itertools import combinations
from statistics import pvariance
from typing import Iterable

from . import power
from .compare import score_rows, summarize_arms

SCHEMA = "FSE-PILOT/1"
MIN_CLUSTERS = 5


def _quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))]


def outcome_counts(rows: Iterable[dict]) -> dict[str, dict]:
    counts: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        c = counts[row.get("arm", "?")]
        c["items"] += 1
        ev = row.get("evidence") or {}
        status = ev.get("parse_status")
        if status in ("NO_ANSWER", "NO_STRUCTURED_ANSWER"):
            c[status.lower()] += 1
        if ev.get("abstained"):
            c["abstained"] += 1
    return {arm: dict(v) for arm, v in counts.items()}


def pair_estimates(scored: list[dict], a: str, b: str, *, bootstrap: int, seed: int, alpha: float = 0.05) -> dict:
    """Arm a minus arm b on paired tasks, with subfamily-cluster (or task) bootstrap."""
    rows = defaultdict(dict)
    for r in scored:
        if r["arm"] in (a, b):
            rows[r["task_id"]][r["arm"]] = r
    tasks = sorted(t for t, v in rows.items() if a in v and b in v)
    if len(tasks) < 2:
        return {"paired_tasks": len(tasks), "warning": "FEWER_THAN_TWO_PAIRED_TASKS"}
    clusters = defaultdict(list)
    for t in tasks:
        clusters[rows[t][a]["subfamily"]].append(t)
    groups = list(clusters.values())
    use_clusters = len(groups) >= MIN_CLUSTERS

    def stats(sample: list[str]) -> tuple[float, float, float]:
        sa = [rows[t][a] for t in sample]
        sb = [rows[t][b] for t in sample]
        succ = (sum(x["success"] for x in sa) - sum(y["success"] for y in sb)) / len(sample)
        util = (sum(x["utility"] for x in sa) - sum(y["utility"] for y in sb)) / len(sample)
        disc = sum(1 for x, y in zip(sa, sb) if x["success"] != y["success"]) / len(sample)
        return succ, util, disc

    point = stats(tasks)
    rng = random.Random(seed)
    draws = ([], [], [])
    for _ in range(bootstrap):
        sample = ([t for _ in groups for t in groups[rng.randrange(len(groups))]] if use_clusters
                  else [tasks[rng.randrange(len(tasks))] for _ in tasks])
        for i, v in enumerate(stats(sample)):
            draws[i].append(v)
    diffs = [rows[t][a]["utility"] - rows[t][b]["utility"] for t in tasks]
    names = ("success_rate_difference", "mean_utility_difference", "discordance_psi")
    out = {"paired_tasks": len(tasks), "resampling": "cluster_bootstrap_by_subfamily" if use_clusters else "task_bootstrap",
           "per_task_utility_difference_variance": pvariance(diffs) if len(diffs) > 1 else None}
    for i, name in enumerate(names):
        out[name] = {"estimate": point[i], "ci_low": _quantile(draws[i], alpha / 2),
                     "ci_high": _quantile(draws[i], 1 - alpha / 2)}
    sa = [rows[t][a]["success"] for t in tasks]
    sb = [rows[t][b]["success"] for t in tasks]
    out["concordance_table"] = {"both_success": sum(1 for x, y in zip(sa, sb) if x and y),
                                f"{a}_only": sum(1 for x, y in zip(sa, sb) if x and not y),
                                f"{b}_only": sum(1 for x, y in zip(sa, sb) if y and not x),
                                "neither": sum(1 for x, y in zip(sa, sb) if not x and not y)}
    return out


def sample_size_proposal(psi_estimate: float | None, psi_ci_high: float | None, *,
                         margins: tuple[float, ...] = (0.10, 0.05), alpha: float = 0.025, pw: float = 0.80) -> dict:
    """Paired tasks needed at each margin, for the psi point estimate and its upper bound."""
    out = {"alpha_one_sided": alpha, "power": pw, "true_difference": 0.0, "rows": []}
    for margin in margins:
        row = {"margin": margin}
        for label, psi in (("psi_estimate", psi_estimate), ("psi_ci_high", psi_ci_high)):
            if psi is None or psi <= 0:
                row[label] = None
            else:
                row[label] = {"psi": round(psi, 4),
                              "paired_tasks": power.paired_noninferiority_n(margin, min(psi, 1.0), alpha=alpha, power=pw)}
        out["rows"].append(row)
    out["recommendation"] = ("use the psi_ci_high column, which protects power against an optimistic pilot; "
                             "binding only after the owner freezes and deposits it (G7)")
    return out


def analyze(graded_rows: list[dict], *, reference_arm: str = "F1", bootstrap: int = 2000, seed: int = 20261011,
            success_threshold: float = 1.0) -> dict:
    scored, excluded = score_rows(graded_rows, success_threshold)
    arms = sorted({r["arm"] for r in graded_rows})
    labelled = {(r["arm"], r["task_id"]) for r in scored}
    unverifiable = defaultdict(int)
    for r in graded_rows:
        if (r["arm"], r["task_id"]) not in labelled:
            unverifiable[r["arm"]] += 1
    summary = summarize_arms(scored)
    per_arm = {}
    counts = outcome_counts(graded_rows)
    for arm in arms:
        s = summary.get(arm, {})
        n = s.get("labelled_tasks", 0)
        successes = round(s.get("success_rate", 0.0) * n) if n else 0
        utilities = [r["utility"] for r in scored if r["arm"] == arm]
        per_arm[arm] = {**s, "successes": successes, "failures": n - successes, "unverifiable": unverifiable[arm],
                        "utility_variance": pvariance(utilities) if len(utilities) > 1 else None,
                        **{k: v for k, v in counts.get(arm, {}).items() if k != "items"}}
    pairs = {}
    for a, b in combinations(arms, 2):
        # Differences are "other arm minus reference arm" whenever the reference is in the pair.
        first, second = ((b, a) if a == reference_arm else (a, b))
        est = pair_estimates(scored, first, second, bootstrap=bootstrap, seed=seed)
        psi = est.get("discordance_psi", {})
        est["sample_size_proposal"] = sample_size_proposal(psi.get("estimate"), psi.get("ci_high"))
        pairs[f"{first}-{second}"] = est
    warnings = []
    if "A" not in arms:
        warnings.append("ARM_A_MISSING_NOT_A_COMPLETED_PREREGISTERED_PILOT")
    return {"schema": SCHEMA, "descriptive_only": True, "arms": per_arm, "pairs": pairs,
            "excluded_without_label": excluded, "warnings": warnings,
            "note": "No hypothesis is tested here; confirmatory tests run only after G1-G7 pass."}
