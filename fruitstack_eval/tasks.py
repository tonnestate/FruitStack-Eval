"""Task registry with committed reference answers (readiness gate G4).

Reference answers are committed before any system output is seen: only a salted
SHA-256 commitment of each reference and a hash of each prompt go into the public
manifest. Prompts stay private as well, so held-out tasks cannot leak into model
training through the deposit. Salts and references stay with the owner and are
revealed only for verification after the confirmatory run.
"""
from __future__ import annotations

import hashlib
import json
import secrets
from collections import defaultdict
from datetime import datetime, timezone
from typing import Callable, Iterable

SCHEMA = "FSE-TASKS/1"
FAMILIES = frozenset({"INQUIRY", "SOFTWARE", "RESEARCH", "ECONOMIC"})
SPLITS = frozenset({"TRAIN", "HELDOUT"})
REQUIRED = ("task_id", "family", "subfamily", "split", "prompt", "reference")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def commitment(salt: str, reference: str) -> str:
    return _sha256(f"{salt}\x1f{reference}")


def validate(rows: Iterable[dict]) -> list[str]:
    """Return a list of problems; an empty list means the task set is admissible."""
    problems: list[str] = []
    seen: set[str] = set()
    split_by_subfamily: dict[str, set[str]] = defaultdict(set)
    rows = list(rows)
    if not rows:
        return ["task set is empty"]
    for index, row in enumerate(rows):
        missing = [key for key in REQUIRED if not isinstance(row.get(key), str) or not row[key].strip()]
        if missing:
            problems.append(f"row {index}: missing or empty {missing}")
            continue
        if row["task_id"] in seen:
            problems.append(f"row {index}: duplicate task_id {row['task_id']}")
        seen.add(row["task_id"])
        if row["family"] not in FAMILIES:
            problems.append(f"row {index}: unknown family {row['family']}")
        if row["split"] not in SPLITS:
            problems.append(f"row {index}: unknown split {row['split']}")
        split_by_subfamily[f"{row['family']}/{row['subfamily']}"].add(row["split"])
    for subfamily, splits in sorted(split_by_subfamily.items()):
        if len(splits) > 1:
            problems.append(f"subfamily {subfamily} appears in both TRAIN and HELDOUT")
    if split_by_subfamily and not any("HELDOUT" in s for s in split_by_subfamily.values()):
        problems.append("no HELDOUT subfamily: generalization cannot be tested")
    return problems


def commit(rows: Iterable[dict], salt_factory: Callable[[], str] = lambda: secrets.token_hex(16),
           created_at: str | None = None) -> tuple[dict, dict[str, str]]:
    """Build the public manifest and the private salt table."""
    rows = list(rows)
    problems = validate(rows)
    if problems:
        raise ValueError("; ".join(problems))
    salts: dict[str, str] = {}
    entries = []
    for row in sorted(rows, key=lambda r: r["task_id"]):
        salt = salt_factory()
        salts[row["task_id"]] = salt
        entries.append({
            "task_id": row["task_id"],
            "family": row["family"],
            "subfamily": row["subfamily"],
            "split": row["split"],
            "prompt_sha256": _sha256(row["prompt"]),
            "reference_commitment": commitment(salt, row["reference"]),
        })
    manifest = {
        "schema": SCHEMA,
        "created_at": created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "tasks": entries,
        "digest": _sha256(canonical_json(entries)),
    }
    return manifest, salts


def verify(manifest: dict, rows: Iterable[dict], salts: dict[str, str]) -> list[str]:
    """Check revealed prompts, references and salts against a deposited manifest."""
    problems: list[str] = []
    if manifest.get("schema") != SCHEMA:
        problems.append("unknown manifest schema")
    entries = manifest.get("tasks") or []
    if _sha256(canonical_json(entries)) != manifest.get("digest"):
        problems.append("manifest digest does not match its task list")
    by_id = {row.get("task_id"): row for row in rows}
    for entry in entries:
        task_id = entry.get("task_id")
        row = by_id.get(task_id)
        salt = salts.get(task_id)
        if row is None or salt is None:
            problems.append(f"{task_id}: revealed row or salt missing")
            continue
        if _sha256(row.get("prompt", "")) != entry.get("prompt_sha256"):
            problems.append(f"{task_id}: prompt differs from the committed prompt")
        if commitment(salt, row.get("reference", "")) != entry.get("reference_commitment"):
            problems.append(f"{task_id}: reference differs from the committed reference")
    return problems
