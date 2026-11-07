"""OGI-013 organisational learning store: episode outcome attribution and the training-table join.

Plain Python only (no keras, no numpy at import time). Contract: evidence/ogi013-learning/SPEC.md.
Files under <store_dir>/training/: decisions.jsonl (OGI013-ORG-DECISION/1), decision_results.jsonl
(OGI013-ORG-DECISION-RESULT/1), outcomes.jsonl (OGI013-ORG-OUTCOME/1). Append-only.
"""
from __future__ import annotations

import json
from hashlib import sha256
import math
from datetime import datetime, timezone
from pathlib import Path

DECISION_SCHEMA = "OGI013-ORG-DECISION/1"
RESULT_SCHEMA = "OGI013-ORG-DECISION-RESULT/1"
OUTCOME_SCHEMA = "OGI013-ORG-OUTCOME/1"
STRUCTURES = ("S0", "S1", "S2", "S3")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _append(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def _reward(reward) -> float:
    if isinstance(reward, bool) or not isinstance(reward, (int, float)):
        raise ValueError("reward must be a float")
    r = float(reward)
    if not (math.isfinite(r) and 0.0 <= r <= 1.0):
        raise ValueError("reward must lie in [0, 1] (covers {0.0, 1.0})")
    return r


def attribute_episode_outcome(service, *, task_ref, domain, reward, grader_ref, result_sha256, decision_ids, store_dir,
                              tokens=None, calls=None, wall_seconds=None, economic=None) -> dict:
    """Credit one verified episode reward to every decision of the episode, then log one outcome row.

    Idempotent per (task_ref, result_sha256), including retries after partial feedback writes.
    """
    if not (task_ref and grader_ref and result_sha256):
        raise ValueError("task_ref, grader_ref and result_sha256 are required")
    r = _reward(reward)
    ids = list(decision_ids or [])
    if not ids:
        raise ValueError("decision_ids must be non-empty")
    path = Path(store_dir) / "training" / "outcomes.jsonl"
    for row in _read(path):
        if row.get("task_ref") == task_ref and row.get("grader_result_sha256") == result_sha256:
            if any(row.get(key) != value for key, value in {
                "domain": domain, "reward": r, "grader": grader_ref, "decision_ids": ids,
            }.items()):
                raise ValueError("CONFLICTING_EPISODE_OUTCOME")
            return row
    for did in ids:
        note = "OGI013-EPISODE-OUTCOME/1:" + sha256(f"{task_ref}|{result_sha256}|{did}".encode()).hexdigest()
        existing = service.decision_view(did).get("feedback", [])
        if any(item.get("note") == note for item in existing):
            continue
        service.record_decision_feedback(decision_id=did, epistemic_state="VERIFIED", verified_utility=r, verifier=grader_ref,
                                         note=note, scope="ENSEMBLE", attribution_basis="EPISODE_OFFICIAL_GRADER")
    row = {"schema": OUTCOME_SCHEMA, "task_ref": task_ref, "domain": domain, "reward": r, "epistemic_state": "VERIFIED",
           "grader": grader_ref, "grader_result_sha256": result_sha256, "decision_ids": ids, "tokens": tokens, "calls": calls,
           "wall_seconds": wall_seconds, "economic": economic or {"cash_known_usd": None, "entitlement_value_usd_est": None},
           "created_at": _now()}
    _append(path, row)
    return row


def load_training_table(store_dir) -> list[dict]:
    """All decision rows joined by task_ref to their completion result and verified outcome.

    Every row is returned; ``eligible_for_training`` is True only for VERIFIED outcome + RANDOMIZED arm (propensity known).
    ponytail: one outcome and one result per task_ref (last row wins); per-decision results are not modelled.
    """
    t = Path(store_dir) / "training"
    outcomes = {o["task_ref"]: o for o in _read(t / "outcomes.jsonl")}
    # Completion events identify a decision row_id, not a task_ref.
    results = {x["row_id"]: x for x in _read(t / "decision_results.jsonl") if x.get("row_id")}
    table = []
    for d in _read(t / "decisions.jsonl"):
        tr = d.get("task_ref")
        o = outcomes.get(tr)
        res = results.get(d.get("row_id"))
        prop = d.get("propensity")
        row = dict(d)
        row["result"] = {k: v for k, v in res.items() if k != "schema"} if res else None
        row["reward"] = o["reward"] if o else None
        row["epistemic_state"] = o["epistemic_state"] if o else None
        row["eligible_for_training"] = bool(
            tr and o and o.get("epistemic_state") == "VERIFIED"
            and d.get("arm_mode") == "RANDOMIZED"
            and isinstance(prop, (int, float)) and not isinstance(prop, bool) and 0.0 < prop <= 1.0
            and d.get("structure") in STRUCTURES
        )
        table.append(row)
    return table
