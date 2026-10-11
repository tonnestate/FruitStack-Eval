"""Revision-evident sealing of append-only logs (readiness gate G5).

A seal records the SHA-256 of every row of every log, in logical order (rotated
DecisionLog segments oldest first), plus a digest over the whole record. Commit the
seal to git or deposit it, and the logs become revision-evident: any later edit,
deletion or reordering of a sealed row is detected when the logs are checked against
the seal.

Logs may legitimately change in two ways, and both are reported, never hidden:
rows appended after the seal (APPEND_ONLY), and the oldest rows dropped by segment
retention (RETENTION_DROPPED, with the number of rows). Anything else is TAMPERED.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .decision_log import segment_paths

SCHEMA = "FSE-SEAL/1"
LOG_KINDS = ("decisionlog", "jsonl")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _files(path: Path, kind: str) -> list[Path]:
    if kind not in LOG_KINDS:
        raise ValueError(f"log kind must be one of {LOG_KINDS}")
    files = segment_paths(path) if kind == "decisionlog" else ([Path(path)] if Path(path).exists() else [])
    if not files:
        raise ValueError(f"log not found: {path}")
    return files


def row_hashes(path: Path, kind: str) -> tuple[list[str], list[dict]]:
    hashes: list[str] = []
    files = []
    for file in _files(Path(path), kind):
        data = file.read_bytes()
        files.append({"name": file.name, "bytes": len(data), "sha256": _sha(data)})
        hashes.extend(_sha(line) for line in data.splitlines() if line.strip())
    return hashes, files


def _root(hashes: list[str]) -> str:
    return _sha("\n".join(hashes).encode("ascii"))


def seal(logs: dict[str, tuple[Path, str]], created_at: str | None = None) -> tuple[dict, dict[str, list[str]]]:
    """Return (manifest, rows). `logs` maps a log name to (path, kind)."""
    if not logs:
        raise ValueError("nothing to seal")
    entries, rows = {}, {}
    for name, (path, kind) in sorted(logs.items()):
        hashes, files = row_hashes(Path(path), kind)
        rows[name] = hashes
        entries[name] = {"path": str(path), "kind": kind, "rows": len(hashes), "root": _root(hashes), "files": files}
    rows_digest = _sha(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("ascii"))
    body = {"schema": SCHEMA,
            "created_at": created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "logs": entries, "rows_digest": rows_digest}
    body["digest"] = _sha(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return body, rows


def _check_manifest(manifest: dict, rows: dict[str, list[str]]) -> list[str]:
    problems = []
    if manifest.get("schema") != SCHEMA:
        problems.append("unknown seal schema")
    body = {k: v for k, v in manifest.items() if k != "digest"}
    if _sha(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")) != manifest.get("digest"):
        problems.append("seal digest does not match the seal")
    if _sha(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("ascii")) != manifest.get("rows_digest"):
        problems.append("row list does not match the seal")
    for name, entry in (manifest.get("logs") or {}).items():
        if _root(rows.get(name, [])) != entry.get("root") or len(rows.get(name, [])) != entry.get("rows"):
            problems.append(f"{name}: row list does not match its sealed root")
    return problems


def compare_rows(old: list[str], new: list[str]) -> dict:
    """Classify how `new` relates to the sealed `old` row sequence."""
    if new[:len(old)] == old:
        return {"status": "UNCHANGED" if len(new) == len(old) else "APPEND_ONLY",
                "dropped": 0, "appended": len(new) - len(old)}
    starts = [i for i, h in enumerate(old) if new and h == new[0]]
    for d in starts:
        kept = old[d:]
        if new[:len(kept)] == kept:
            return {"status": "RETENTION_DROPPED", "dropped": d, "appended": len(new) - len(kept)}
    if not new:
        return {"status": "RETENTION_DROPPED", "dropped": len(old), "appended": 0}
    first = next((i for i, (a, b) in enumerate(zip(old, new)) if a != b), min(len(old), len(new)))
    return {"status": "TAMPERED", "first_mismatch_row": first, "dropped": None, "appended": None}


def verify(manifest: dict, rows: dict[str, list[str]], *, allow_retention: bool = True) -> dict:
    """Check the logs named in a seal against their current content."""
    problems = _check_manifest(manifest, rows)
    logs = {}
    if not problems:
        for name, entry in sorted(manifest["logs"].items()):
            try:
                current, _ = row_hashes(Path(entry["path"]), entry["kind"])
            except ValueError as exc:
                logs[name] = {"status": "MISSING", "error": str(exc)}
                problems.append(f"{name}: {exc}")
                continue
            outcome = compare_rows(rows[name], current)
            logs[name] = outcome
            if outcome["status"] == "TAMPERED":
                problems.append(f"{name}: sealed rows changed (first mismatch at row {outcome['first_mismatch_row']})")
            elif outcome["status"] == "RETENTION_DROPPED" and not allow_retention:
                problems.append(f"{name}: {outcome['dropped']} sealed rows no longer present")
    return {"passed": not problems, "sealed_at": manifest.get("created_at"), "digest": manifest.get("digest"),
            "logs": logs, "problems": problems}


def write(manifest: dict, rows: dict[str, list[str]], out: Path) -> tuple[Path, Path]:
    out = Path(out)
    rows_path = out.with_name(out.name + ".rows.json")
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows_path.write_text(json.dumps(rows, sort_keys=True) + "\n", encoding="utf-8")
    return out, rows_path


def read(path: Path) -> tuple[dict, dict[str, list[str]]]:
    path = Path(path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    rows = json.loads(path.with_name(path.name + ".rows.json").read_text(encoding="utf-8"))
    return manifest, rows
