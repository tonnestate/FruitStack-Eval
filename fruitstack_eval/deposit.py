"""Readiness gate G7: a deposit manifest of everything a confirmatory run is bound to.

The owner deposits the manifest and the files it lists (protocol export, task-set
manifest, thresholds, rubric and procedure versions, frozen sample sizes) with a
timestamping repository (OSF, Zenodo) and records the DOI. The manifest makes later
changes detectable: every file is listed with its SHA-256, and the manifest itself
carries a digest. G7 passes only with a DOI, which only the owner can obtain.
"""
from __future__ import annotations

import hashlib
import json
import tomllib
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "FSE-DEPOSIT/1"
REQUIRED_LABELS = ("protocol", "task_manifest", "g2_thresholds", "pilot_procedure", "freeze")
FREEZE_KEYS = ("margin", "discordance_psi", "paired_tasks", "alpha_one_sided", "power", "rubric", "inquiry_schema")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_freeze(path: Path) -> list[str]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8")).get("freeze", {})
    problems = [f"freeze.{k} missing" for k in FREEZE_KEYS if k not in data]
    if not problems:
        if not 0 < float(data["margin"]) < 1:
            problems.append("freeze.margin must be in (0, 1)")
        if not 0 < float(data["discordance_psi"]) <= 1:
            problems.append("freeze.discordance_psi must be in (0, 1]")
        if int(data["paired_tasks"]) < 1:
            problems.append("freeze.paired_tasks must be positive")
    return problems


def build(files: dict[str, Path], *, created_at: str | None = None) -> dict:
    missing = [label for label in REQUIRED_LABELS if label not in files]
    if missing:
        raise ValueError(f"deposit needs {missing}")
    problems = check_freeze(files["freeze"])
    if problems:
        raise ValueError("; ".join(problems))
    items = []
    for label, path in sorted(files.items()):
        data = Path(path).read_bytes()
        items.append({"label": label, "file": Path(path).name, "bytes": len(data), "sha256": _sha(data)})
    body = {"schema": SCHEMA, "created_at": created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "items": items, "doi": None}
    body["digest"] = _sha(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return body


def verify(manifest: dict, files: dict[str, Path]) -> dict:
    problems = []
    body = {k: v for k, v in manifest.items() if k not in ("digest", "doi")}
    body["doi"] = None
    if _sha(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")) != manifest.get("digest"):
        problems.append("manifest digest does not match")
    for item in manifest.get("items", []):
        path = files.get(item["label"])
        if path is None or not Path(path).exists():
            problems.append(f"{item['label']}: file not supplied")
        elif _sha(Path(path).read_bytes()) != item["sha256"]:
            problems.append(f"{item['label']}: content changed since the deposit manifest was built")
    if not manifest.get("doi"):
        problems.append("NO_DOI: the owner has not recorded a deposit DOI yet")
    return {"gate": "G7", "passed": not problems, "problems": problems, "doi": manifest.get("doi")}
