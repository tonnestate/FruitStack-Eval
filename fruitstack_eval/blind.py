"""Blinded human grading packets (gate G4), schema FSE-BLIND/1.

Use it for families graded by people (research synthesis) and for the blind audit of
the deterministic inquiry grader. `export` shuffles answers from all arms, gives each a
random blind id, strips the arm and redacts model, vendor and system names from the
answer text. The key that maps blind ids back to arms stays with the operator; its
SHA-256 goes into the manifest, which is committed before grading starts. `ingest`
checks the key against that hash, requires every blind id to be graded exactly once on
the pre-registered scale, and only then joins grades back to arms.

A grader may mark an item VOID when the reference itself turns out to be wrong or
ambiguous. Voiding happens blind, before arms are revealed, and a voided task is
removed from every arm, never from one arm only.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from datetime import datetime, timezone

SCHEMA = "FSE-BLIND/1"
SCALE = (0.0, 0.5, 1.0)
REDACT = ("claude", "anthropic", "gpt", "chatgpt", "openai", "gemini", "gemma", "google", "llama", "meta", "mistral",
          "mixtral", "qwen", "alibaba", "deepseek", "grok", "xai", "nemotron", "nvidia", "kimi", "moonshot", "glm",
          "zhipu", "phi", "microsoft", "cohere", "command r", "cherryme", "plumme", "appleme", "fruitstack", "sonnet",
          "opus", "haiku")
_REDACT_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in sorted(REDACT, key=len, reverse=True)) + r")[\w.-]*",
                        re.I)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical(rows) -> str:
    return "".join(json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows)


def redact(text: str | None) -> tuple[str, int]:
    if not text:
        return "", 0
    count = 0

    def sub(_match):
        nonlocal count
        count += 1
        return "[REDACTED]"

    return _REDACT_RE.sub(sub, text), count


def export(results: list[dict], tasks: list[dict], *, seed: int, sample: float = 1.0,
           created_at: str | None = None) -> tuple[list[dict], list[dict], dict]:
    """Return (sheet, key, manifest). Results need task_id, arm and output."""
    if not 0 < sample <= 1:
        raise ValueError("sample must be in (0, 1]")
    by_task = {t["task_id"]: t for t in tasks}
    rows = [r for r in results if r.get("task_id") in by_task]
    unknown = sorted({r.get("task_id") for r in results if r.get("task_id") not in by_task})
    if unknown:
        raise ValueError(f"results for unknown tasks: {unknown[:5]}")
    rng = random.Random(seed)
    if sample < 1:
        chosen_tasks = sorted(by_task)
        rng.shuffle(chosen_tasks)
        keep = set(chosen_tasks[: max(1, round(sample * len(chosen_tasks)))])
        rows = [r for r in rows if r["task_id"] in keep]           # sample whole tasks: every arm of a task
    order = list(range(len(rows)))
    rng.shuffle(order)
    sheet, key, redactions = [], [], 0
    for position, index in enumerate(order):
        row = rows[index]
        blind_id = f"B{rng.getrandbits(48):012x}"
        answer, n = redact(row.get("output"))
        redactions += n
        task = by_task[row["task_id"]]
        sheet.append({"blind_id": blind_id, "position": position, "task_id": row["task_id"], "prompt": task["prompt"],
                      "reference": task["reference"], "answer": answer, "grade": None, "void": False, "note": ""})
        key.append({"blind_id": blind_id, "task_id": row["task_id"], "arm": row["arm"]})
    manifest = {"schema": SCHEMA, "created_at": created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "items": len(sheet), "tasks": len({r["task_id"] for r in key}), "arms": sorted({r["arm"] for r in key}),
                "scale": list(SCALE), "seed_sha256": _sha(str(seed)), "sample": sample, "redactions": redactions,
                "sheet_sha256": _sha(_canonical(sheet)), "key_sha256": _sha(_canonical(key))}
    return sheet, key, manifest


def ingest(manifest: dict, key: list[dict], graded: list[dict], *, grader: str) -> dict:
    """Validate a graded sheet and join it to arms. Raises ValueError on any violation."""
    if manifest.get("schema") != SCHEMA:
        raise ValueError("unknown blind manifest schema")
    if _sha(_canonical(key)) != manifest.get("key_sha256"):
        raise ValueError("key does not match the committed key hash")
    if not grader or not grader.strip():
        raise ValueError("grader identity is required")
    arm_of = {k["blind_id"]: k for k in key}
    seen: set[str] = set()
    problems = []
    for row in graded:
        bid = row.get("blind_id")
        if bid not in arm_of:
            problems.append(f"unknown blind id {bid}")
            continue
        if bid in seen:
            problems.append(f"blind id graded twice: {bid}")
        seen.add(bid)
        if row.get("void") is True:
            continue
        g = row.get("grade")
        if isinstance(g, bool) or not isinstance(g, (int, float)) or float(g) not in SCALE:
            problems.append(f"{bid}: grade must be one of {SCALE}")
    missing = sorted(set(arm_of) - seen)
    if missing:
        problems.append(f"{len(missing)} blind ids not graded")
    if problems:
        raise ValueError("; ".join(problems[:10]))
    voided_tasks = sorted({arm_of[r["blind_id"]]["task_id"] for r in graded if r.get("void") is True})
    labels = []
    for row in graded:
        k = arm_of[row["blind_id"]]
        if k["task_id"] in voided_tasks:
            continue
        labels.append({"task_id": k["task_id"], "arm": k["arm"], "blind_id": row["blind_id"],
                       "evidence": {"provenance": "EXTERNALLY_VERIFIED", "blinded": True, "grade": float(row["grade"]),
                                    "grader": grader, "blind_manifest": manifest["key_sha256"][:16]}})
    return {"labels": labels, "voided_tasks": voided_tasks, "items": len(graded)}


def agreement(labels: list[dict], deterministic: dict[tuple[str, str], float]) -> dict:
    """Agreement of blind human grades with deterministic grades, per (task_id, arm)."""
    pairs = [(l["evidence"]["grade"], deterministic[(l["task_id"], l["arm"])]) for l in labels
             if (l["task_id"], l["arm"]) in deterministic]
    if not pairs:
        return {"items": 0, "exact_agreement": None, "disagreements": 0}
    agree = sum(1 for a, b in pairs if a == b)
    return {"items": len(pairs), "exact_agreement": agree / len(pairs), "disagreements": len(pairs) - agree}
