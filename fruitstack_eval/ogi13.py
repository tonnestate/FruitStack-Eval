"""OGI-013 independent, conservative evaluation of task-variable organisation.

This module imports NO FruitStack product package. It only reads trusted-host
observation exports. It checks schema and pair comparability, not the authenticity
of external grader receipts or provider billing. No result authorizes policy
promotion, and this module NEVER computes or claims an AGI/OGI pass.
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Any, Iterable

SCHEMA = "FSE-OGI13-PAIR/1"
ARMS = frozenset(("FIXED", "ADAPTIVE"))
PARITY_KEYS = (
    "benchmark_id", "benchmark_revision", "task_manifest_digest",
    "grader_digest", "model_pool_digest", "skills_digest", "tools_digest",
    "budget_digest", "supply_regime_id",
)
RESOURCE_KEYS = (
    "provider_calls", "total_tokens", "quota_units", "cost_usd",
    "wall_seconds", "human_minutes",
)


def _nonempty(row: dict, field: str) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"MISSING_{field.upper()}")
    return value


def _number(row: dict, name: str) -> float | int | None:
    value = row.get(name)
    if value is None:
        return None
    integer = name in ("provider_calls", "total_tokens")
    if type(value) not in ((int,) if integer else (int, float)):
        raise ValueError(f"INVALID_{name.upper()}")
    if value < 0 or not math.isfinite(value):
        raise ValueError(f"INVALID_{name.upper()}")
    return value


def _check_row(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("INVALID_OBSERVATION")
    row = dict(raw)
    for field in ("task_id", "arm", *PARITY_KEYS, "work_ref", "trace_ref"):
        _nonempty(row, field)
    if row["arm"] not in ARMS:
        raise ValueError("INVALID_ARM")
    status = row.get("grade_status")
    if status not in ("VERIFIED", "UNKNOWN", "INCOMPLETE"):
        raise ValueError("INVALID_GRADE_STATUS")
    grade = row.get("grade")
    if status == "VERIFIED":
        if type(grade) not in (int, float) or not math.isfinite(grade) or not 0 <= grade <= 1:
            raise ValueError("INVALID_VERIFIED_GRADE")
        _nonempty(row, "grader_receipt_ref")
        _nonempty(row, "independent_verifier")
    elif grade is not None:
        raise ValueError("UNVERIFIED_GRADE_PROVIDED")
    for k in RESOURCE_KEYS:
        row[k] = _number(row, k)
    # All provider-facing attempts are counted, including failed/censored ones.
    # Receipt gaps do not disappear merely because a task graded successfully.
    refs = row.get("provider_receipt_refs")
    if not isinstance(refs, list) or any(not isinstance(r, str) or not r.strip() for r in refs):
        raise ValueError("INVALID_PROVIDER_RECEIPTS")
    if len(refs) != len(set(refs)):
        raise ValueError("DUPLICATE_PROVIDER_RECEIPT")
    n_calls = row["provider_calls"]
    if n_calls is not None and len(refs) > n_calls:
        raise ValueError("RECEIPTS_EXCEED_CALLS")
    edges = row.get("competence_edges")
    if not isinstance(edges, list) or any(not isinstance(e, str) or not e.strip() for e in edges):
        raise ValueError("INVALID_COMPETENCE_EDGES")
    if len(edges) != len(set(edges)):
        raise ValueError("DUPLICATE_COMPETENCE_EDGE")
    row["competence_edges"] = tuple(sorted(edges))
    # Fail closed on evidence completeness. A receipt label is only an identifier,
    # NOT cryptographic or semantic verification.
    row["_usage_complete"] = (
        n_calls is not None and len(refs) == n_calls
        and all(row[k] is not None for k in RESOURCE_KEYS)
    )
    return row


def compare_paired(rows: Iterable[dict]) -> dict[str, Any]:
    """Return descriptive outcome and per-success efficiency of matched arms.

    VERIFIED grades are independently *asserted* by the export; the evaluator
    cannot attest that the referenced grader signed the receipt. UNKNOWN and
    INCOMPLETE are included in the randomized-task success denominator as
    non-success and surfaced explicitly, never quietly dropped. Only exact
    benchmark/model/tool/skill/budget/supply parity enters a matched pair.
    """
    by_task: dict[str, dict[str, dict]] = defaultdict(dict)
    n_rows = 0
    for raw in rows:
        row = _check_row(raw)
        n_rows += 1
        arm_rows = by_task[row["task_id"]]
        if row["arm"] in arm_rows:
            raise ValueError("DUPLICATE_TASK_ARM")
        arm_rows[row["arm"]] = row
    out: dict[str, Any] = {
        "schema": SCHEMA,
        "observation_rows": n_rows,
        "assigned_tasks": len(by_task),
        "paired_tasks": 0,
        "unmatched_tasks": [],
        "confounded_tasks": [],
        "missing_usage_tasks": [],
        "incomplete_grade_tasks": [],
        "edge_ambiguous_tasks": [],
        "overall": {},
        "by_one_added_edge": {},
        "organisational_advantage_proven": False,
        "causal_effect_proven": False,
        "grader_provenance_attested": False,
        "policy_promotion_authorized": False,
        "limitations": [
            "OBSERVATION_ONLY_NO_PRE_REGISTERED_RANDOMISATION_ATTESTED",
            "GRADER_AND_PROVIDER_RECEIPT_REFERENCES_NOT_AUTHENTICATED",
            "NO_OFFICIAL_BENCHMARK_GRADER_VERIFIED_BY_THIS_MODULE",
        ],
    }
    matched: list[tuple[str, dict, dict, str | None]] = []
    for task_id, arms in sorted(by_task.items()):
        if set(arms) != ARMS:
            out["unmatched_tasks"].append(task_id)
            continue
        fixed, adapt = arms["FIXED"], arms["ADAPTIVE"]
        if any(fixed[k] != adapt[k] for k in PARITY_KEYS):
            out["confounded_tasks"].append(task_id)
            continue
        if not (fixed["_usage_complete"] and adapt["_usage_complete"]):
            out["missing_usage_tasks"].append(task_id)
        if fixed["grade_status"] != "VERIFIED" or adapt["grade_status"] != "VERIFIED":
            out["incomplete_grade_tasks"].append(task_id)
        add = set(adapt["competence_edges"]) - set(fixed["competence_edges"])
        remove = set(fixed["competence_edges"]) - set(adapt["competence_edges"])
        one_edge = next(iter(add)) if len(add) == 1 and not remove else None
        if one_edge is None:
            out["edge_ambiguous_tasks"].append(task_id)
        matched.append((task_id, fixed, adapt, one_edge))

    def statistics(matched_rows: list[tuple[str, dict, dict, str | None]]) -> dict[str, Any]:
        n = len(matched_rows)
        if n == 0:
            return {"pairs": 0, "verified_grade_pairs": 0,
                    "successes": {"FIXED": 0, "ADAPTIVE": 0},
                    "success_rate": {"FIXED": None, "ADAPTIVE": None},
                    "success_rate_delta": None,
                    "resources_per_verified_success": {
                        name: {"FIXED": None, "ADAPTIVE": None, "delta": None}
                        for name in RESOURCE_KEYS},
                    "complete_usage_pairs": 0,
                    "mean_resource_delta": {name: None for name in RESOURCE_KEYS}}

        successes = {
            arm: sum(row[arm]["grade_status"] == "VERIFIED" and row[arm]["grade"] == 1
                     for _, fixed, adapt, _ in matched_rows
                     for row in ({"FIXED": fixed, "ADAPTIVE": adapt},))
            for arm in ("FIXED", "ADAPTIVE")
        }
        success_rates = {arm: successes[arm] / n for arm in successes}
        usage_rows = [(f, a) for _, f, a, _ in matched_rows if f["_usage_complete"] and a["_usage_complete"]]
        per_success: dict[str, dict] = {}
        mean_delta: dict[str, float | None] = {}
        for metric in RESOURCE_KEYS:
            pairs_with_metric = [(f, a) for _, f, a, _ in matched_rows if f[metric] is not None and a[metric] is not None]
            mean_delta[metric] = (
                sum(a[metric] - f[metric] for f, a in pairs_with_metric) / len(pairs_with_metric)
                if pairs_with_metric else None
            )
            # Require COMPLETE measurements across every included task before
            # using the denominator; partial USD bills are not real ROI.
            complete = len(pairs_with_metric) == n
            values = {
                arm: (
                    sum(row[arm][metric] for _, f, a, _ in matched_rows
                        for row in ({"FIXED": f, "ADAPTIVE": a},)) / successes[arm]
                    if complete and successes[arm] else None
                )
                for arm in successes
            }
            per_success[metric] = {
                **values,
                "delta": (
                    values["ADAPTIVE"] - values["FIXED"]
                    if values["ADAPTIVE"] is not None and values["FIXED"] is not None
                    else None
                ),
            }
        return {
            "pairs": n,
            "verified_grade_pairs": sum(f["grade_status"] == a["grade_status"] == "VERIFIED"
                                        for _, f, a, _ in matched_rows),
            "successes": successes,
            "success_rate": success_rates,
            "success_rate_delta": success_rates["ADAPTIVE"] - success_rates["FIXED"],
            "complete_usage_pairs": len(usage_rows),
            "mean_resource_delta": mean_delta,
            "resources_per_verified_success": per_success,
        }

    out["paired_tasks"] = len(matched)
    out["overall"] = statistics(matched)
    by_edge: dict[str, list] = defaultdict(list)
    for item in matched:
        if item[3] is not None:
            by_edge[item[3]].append(item)
    out["by_one_added_edge"] = {edge: statistics(items) for edge, items in sorted(by_edge.items())}
    if out["missing_usage_tasks"]:
        out["limitations"].append("INCOMPLETE_RESOURCE_ACCOUNTING")
    if out["incomplete_grade_tasks"]:
        out["limitations"].append("INCOMPLETE_OR_UNVERIFIED_GRADING")
    if out["confounded_tasks"]:
        out["limitations"].append("MISMATCHED_RESOURCES_OR_BENCHMARK")
    if out["paired_tasks"] < 2:
        out["limitations"].append("INSUFFICIENT_PAIRED_TASKS")
    return out
