"""Protected paths for governed self-modification (learning loop 4).

A commit written by the system itself carries the trailer `FruitStack-Origin: system`.
Such commits may never touch protected paths: guards, assurance rules, gates, logging,
governance and this evaluator. Commits by human or AI builders that touch protected
paths are allowed but listed for explicit host review.

Merge commits are skipped; the commits they bring in are checked individually.
"""
from __future__ import annotations

import re
import tomllib
from fnmatch import fnmatch
from pathlib import Path

from .gitutil import git, resolve

SYSTEM_TRAILER = re.compile(r"(?im)^FruitStack-Origin:\s*system\s*$")


def load_manifest(path: Path) -> dict[str, tuple[str, ...]]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    repos = data.get("repos", {})
    manifest = {name: tuple(entry.get("paths", [])) for name, entry in repos.items()}
    for name, paths in manifest.items():
        if not paths:
            raise ValueError(f"repository {name} has no protected paths")
    return manifest


def check(repo: Path, name: str, base: str, head: str, manifest: dict[str, tuple[str, ...]]) -> dict:
    if name not in manifest:
        raise ValueError(f"no protected-path entry for repository {name!r}")
    patterns = manifest[name]
    repo = Path(repo)
    base_sha, head_sha = resolve(repo, base), resolve(repo, head)
    commits = git(repo, "rev-list", "--no-merges", f"{base_sha}..{head_sha}").split()
    violations, reviews = [], []
    for sha in commits:
        files = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", sha).splitlines()
        touched = sorted(f for f in files if any(fnmatch(f, p) for p in patterns))
        if not touched:
            continue
        message = git(repo, "show", "-s", "--format=%B", sha)
        entry = {"commit": sha, "files": touched}
        (violations if SYSTEM_TRAILER.search(message) else reviews).append(entry)
    return {
        "repository": name,
        "base": base_sha,
        "head": head_sha,
        "commits_checked": len(commits),
        "violations": violations,
        "host_review_required": reviews,
        "passed": not violations,
    }
