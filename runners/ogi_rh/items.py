"""OGI-RH item bank: file lock and prompt/grader leak guard (design §3 independence, §10).

prompts/ files may be shown to arms; grader/ files never. Regenerate the lock after
an authorized item change with:  python -m ogi_rh.items --write-lock  (from runners/)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from ogi_rh.claims import _norm

ITEMS_DIR = Path(__file__).resolve().parents[2] / "evidence" / "ogi-rh-stress-test" / "items"
LOCK_PATH = ITEMS_DIR / "LOCK.json"
_NOT_SECRET_KEYS = {"id", "template_items", "schema", "family", "grader_only", "known_result_id"}


def file_hashes(root: Path = ITEMS_DIR) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.glob("*/*.json"))}


def _strings(obj, key=None):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(v, k)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v, key)
    elif isinstance(obj, str) and key not in _NOT_SECRET_KEYS:
        yield obj


def leaks(root: Path = ITEMS_DIR) -> list[tuple[str, str]]:
    """(prompt file, grader text) pairs where grader-only text appears in a prompt file.

    Matching is on whole normalized words, so a label such as FLAWED or
    NUMERICAL_EVIDENCE leaks if the words appear anywhere in a prompt.
    """
    secrets = {_norm(s) for g in (root / "grader").glob("*.json")
               for s in _strings(json.loads(g.read_text()))} - {""}
    found = []
    for p in sorted((root / "prompts").glob("*.json")):
        text = f" {_norm(p.read_text())} "
        found += [(p.name, s) for s in sorted(secrets) if f" {s} " in text]
    return found


if __name__ == "__main__" and "--write-lock" in sys.argv:
    LOCK_PATH.write_text(json.dumps({"schema": "OGI-RH-ITEM-LOCK/1", "files": file_hashes()},
                                    indent=1) + "\n")
