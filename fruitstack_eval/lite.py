"""FruitStack-Lite pin check (readiness gate G6).

The Lite manifest lists the components hypotheses H1 to H3 need, each with the exact
commit a confirmatory run must use. UNPINNED entries keep the gate closed on purpose.
"""
from __future__ import annotations

import tomllib
from pathlib import Path

from .gitutil import GitError, git

UNPINNED = "UNPINNED"


def load_manifest(path: Path) -> list[dict]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    components = data.get("component", [])
    names = [c.get("name") for c in components]
    if not components or any(not n for n in names) or len(set(names)) != len(names):
        raise ValueError("manifest needs components with unique, non-empty names")
    for component in components:
        if not component.get("commit"):
            raise ValueError(f"component {component['name']} has no commit (use {UNPINNED})")
    return components


def check(components: list[dict], workspace: Path) -> dict:
    statuses = []
    for component in components:
        name, pinned = component["name"], component["commit"]
        status = {"name": name, "pinned": pinned}
        clone = Path(workspace) / name
        if pinned == UNPINNED:
            status["status"] = "UNPINNED"
        elif not (clone / ".git").exists():
            status["status"] = "MISSING_CLONE"
        else:
            try:
                head = git(clone, "rev-parse", "HEAD").strip()
            except GitError:
                head = ""
            status["head"] = head
            ok = len(pinned) >= 7 and head.startswith(pinned)
            status["status"] = "PINNED_OK" if ok else "MISMATCH"
        statuses.append(status)
    return {"components": statuses, "ready": all(s["status"] == "PINNED_OK" for s in statuses)}
