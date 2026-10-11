"""Readiness gate G2: reliability and error correlation of free provider groups.

Input: scored calibration rows (see `calibration.score`) with a `group` per row, the
independence key the labor market assigned to the executed offer. For each group the
module reports end-to-end execution, answer parsing and accuracy. For each pair of
groups it reports, on the tasks both executed, the phi coefficient of their error
indicators, the joint error rate and the share of joint errors with the same wrong
answer (correlated errors defeat voting more than correlated difficulty does).

G2 passes when at least `min_groups` groups qualify and are pairwise independent under
the frozen thresholds. A pair whose phi is undefined (one group never or always wrong
on the shared tasks) is UNDETERMINED and does not count as independent.
"""
from __future__ import annotations

import math
import random
import tomllib
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Thresholds:
    version: str
    min_calls: int
    min_execution_rate: float
    min_shared_tasks: int
    max_phi: float
    max_same_wrong_share: float
    min_groups: int
    bootstrap: int = 2000
    seed: int = 20261011

    @classmethod
    def load(cls, path: Path) -> "Thresholds":
        data = tomllib.loads(Path(path).read_text(encoding="utf-8"))["g2"]
        return cls(**data)


def _phi(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    n11 = sum(1 for x, y in zip(a, b) if x and y)
    n1_ = sum(a)
    n_1 = sum(b)
    denom = n1_ * (n - n1_) * n_1 * (n - n_1)
    if denom == 0:
        return None
    return (n * n11 - n1_ * n_1) / math.sqrt(denom)


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, round(q * (len(ordered) - 1))))]


def group_stats(rows: list[dict]) -> dict:
    calls = len(rows)
    executed = [r for r in rows if r["executed"]]
    parsed = [r for r in executed if r["parsed"]]
    correct = [r for r in executed if r["correct"]]
    return {
        "calls": calls,
        "executed": len(executed),
        "execution_rate": len(executed) / calls if calls else 0.0,
        "parse_rate": len(parsed) / len(executed) if executed else None,
        "accuracy": len(correct) / len(executed) if executed else None,
        "offers": sorted({r.get("offer_id") for r in rows if r.get("offer_id")}),
        "models": sorted({r.get("model") for r in rows if r.get("model")}),
        "fingerprints": sorted({r.get("model_fingerprint") for r in executed if r.get("model_fingerprint")}),
        "receipts": sum(1 for r in executed if r.get("receipt_id")),
    }


def pair_stats(rows_a: dict[str, dict], rows_b: dict[str, dict], thresholds: Thresholds) -> dict:
    shared = sorted(t for t in rows_a if t in rows_b and rows_a[t]["executed"] and rows_b[t]["executed"])
    ea = [0 if rows_a[t]["correct"] else 1 for t in shared]
    eb = [0 if rows_b[t]["correct"] else 1 for t in shared]
    both_wrong = [t for t, x, y in zip(shared, ea, eb) if x and y]
    same_wrong = [t for t in both_wrong
                  if rows_a[t]["answer_given"] is not None and rows_a[t]["answer_given"] == rows_b[t]["answer_given"]]
    phi = _phi(ea, eb)
    out = {"shared_tasks": len(shared), "phi": phi, "joint_error_rate": len(both_wrong) / len(shared) if shared else None,
           "same_wrong_share": len(same_wrong) / len(both_wrong) if both_wrong else 0.0,
           "phi_ci": [None, None]}
    if phi is not None and len(shared) >= 2:
        rng = random.Random(thresholds.seed)
        draws = []
        for _ in range(thresholds.bootstrap):
            idx = [rng.randrange(len(shared)) for _ in shared]
            value = _phi([ea[i] for i in idx], [eb[i] for i in idx])
            if value is not None:
                draws.append(value)
        if draws:
            out["phi_ci"] = [_quantile(draws, 0.025), _quantile(draws, 0.975)]
    if len(shared) < thresholds.min_shared_tasks:
        out["verdict"] = "INSUFFICIENT_SHARED_TASKS"
    elif phi is None:
        out["verdict"] = "UNDETERMINED_NO_ERROR_VARIANCE"
    elif phi <= thresholds.max_phi and out["same_wrong_share"] <= thresholds.max_same_wrong_share:
        out["verdict"] = "INDEPENDENT"
    else:
        out["verdict"] = "CORRELATED"
    return out


def analyze(scored: Iterable[dict], thresholds: Thresholds) -> dict:
    by_group: dict[str, list[dict]] = defaultdict(list)
    missing_group = 0
    for row in scored:
        if not row.get("group"):
            missing_group += 1
            continue
        by_group[row["group"]].append(row)
    groups = {g: group_stats(rows) for g, rows in sorted(by_group.items())}
    qualified = sorted(g for g, s in groups.items()
                       if s["calls"] >= thresholds.min_calls and s["execution_rate"] >= thresholds.min_execution_rate
                       and s["receipts"] == s["executed"])
    for g, s in groups.items():
        s["qualified"] = g in qualified
    task_rows = {g: {r["task_id"]: r for r in rows} for g, rows in by_group.items()}
    pairs = {}
    for a, b in combinations(sorted(by_group), 2):
        pairs[f"{a}|{b}"] = pair_stats(task_rows[a], task_rows[b], thresholds)
    independent = {frozenset(k.split("|")) for k, v in pairs.items() if v["verdict"] == "INDEPENDENT"}
    best: tuple[str, ...] = ()
    for size in range(len(qualified), 0, -1):
        for combo in combinations(qualified, size):
            if size == 1 or all(frozenset(p) in independent for p in combinations(combo, 2)):
                best = combo
                break
        if best:
            break
    blockers = []
    if missing_group:
        blockers.append("ROWS_WITHOUT_GROUP")
    if len(qualified) < thresholds.min_groups:
        blockers.append("TOO_FEW_QUALIFIED_GROUPS")
    if len(best) < thresholds.min_groups:
        blockers.append("NO_INDEPENDENT_SET_OF_REQUIRED_SIZE")
    return {"gate": "G2", "passed": not blockers, "blockers": blockers, "thresholds": thresholds.__dict__,
            "groups": groups, "pairs": pairs, "qualified_groups": qualified,
            "largest_independent_set": list(best), "rows_without_group": missing_group}
