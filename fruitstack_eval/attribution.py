"""Build-time attribution report (protocol section 6, threat 4).

Measures who wrote the code as it stands at a given revision, using `git blame`:
every surviving line is attributed to the commit that last changed it, and each commit
to a builder. A commit is attributed, in this order, by

1. the trailer `FruitStack-Builder: <name>`, the convention every builder should follow,
2. explicit rules on author or message (for example a Co-Authored-By trailer),
3. an explicit commit range given by the caller (for example main..web/chatgpt=CHATGPT),
4. the branch it was merged from, recognized in merge messages (web/chatgpt, web/claude),
5. otherwise UNATTRIBUTED.

Lines whose blame stops at a shallow-clone boundary are reported separately, because
their true origin is unknown. Use a full clone for confirmatory reports.
"""
from __future__ import annotations

import re
import tomllib
from collections import Counter
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from .gitutil import GitError, git, is_shallow, resolve

UNATTRIBUTED = "UNATTRIBUTED"
SHALLOW_BOUNDARY = "UNKNOWN_SHALLOW_BOUNDARY"
_HEADER = re.compile(r"^([0-9a-f]{40}) \d+ \d+")
_BUILDER_TRAILER = re.compile(r"(?im)^FruitStack-Builder:\s*([A-Za-z0-9_.-]+)\s*$")


@dataclass(frozen=True)
class Rule:
    builder: str
    field: str
    pattern: re.Pattern


@dataclass(frozen=True)
class Rules:
    version: str
    rules: tuple[Rule, ...]
    branch_rules: tuple[tuple[str, str], ...]
    include: tuple[str, ...]
    critical: tuple[str, ...]


def load_rules(path: Path) -> Rules:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    rules = []
    for item in data.get("rule", []):
        if item.get("field") not in ("author", "message"):
            raise ValueError("rule field must be 'author' or 'message'")
        rules.append(Rule(item["builder"], item["field"], re.compile(item["pattern"])))
    return Rules(
        version=str(data.get("version", "unversioned")),
        rules=tuple(rules),
        branch_rules=tuple((branch, builder) for branch, builder in data.get("branch_rules", {}).items()),
        include=tuple(data.get("include", ["*.py"])),
        critical=tuple(data.get("critical", [])),
    )


def _matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch(path, pattern) for pattern in patterns)


def _branch_origins(repo: Path, rev: str, rules: Rules) -> dict[str, str]:
    """Map commits introduced by merges of known branches to their builder."""
    origins: dict[str, str] = {}
    if not rules.branch_rules:
        return origins
    for merge in git(repo, "rev-list", "--merges", rev).split():
        message = git(repo, "log", "-1", "--format=%B", merge)
        builder = next((b for branch, b in rules.branch_rules if branch in message), None)
        if builder is None:
            continue
        try:
            introduced = git(repo, "rev-list", f"{merge}^1..{merge}^2").split()
        except GitError:
            continue  # parent missing in a shallow clone
        for sha in introduced:
            origins.setdefault(sha, builder)
    return origins


def range_origins(repo: Path, ranges: list[tuple[str, str]]) -> dict[str, str]:
    """Map every commit in each 'base..head' range to the given builder (first range wins)."""
    origins: dict[str, str] = {}
    for spec, builder in ranges:
        if ".." not in spec:
            raise ValueError(f"range {spec!r} must look like base..head")
        for sha in git(repo, "rev-list", "--no-merges", spec).split():
            origins.setdefault(sha, builder)
    return origins


def parse_range(text: str) -> tuple[str, str]:
    spec, sep, builder = text.rpartition("=")
    if not sep or not spec or not builder:
        raise ValueError(f"range {text!r} must look like base..head=BUILDER")
    return spec, builder.upper()


def classify(repo: Path, sha: str, rules: Rules, origins: dict[str, str]) -> str:
    meta = git(repo, "show", "-s", "--format=%an <%ae>%x1f%B", sha)
    author, _, message = meta.partition("\x1f")
    trailer = _BUILDER_TRAILER.search(message)
    if trailer:
        return trailer.group(1).upper()
    for rule in rules.rules:
        if rule.pattern.search(author if rule.field == "author" else message):
            return rule.builder
    return origins.get(sha, UNATTRIBUTED)


def _blame_counts(repo: Path, rev: str, path: str) -> tuple[Counter, set[str]]:
    counts: Counter = Counter()
    boundaries: set[str] = set()
    current = None
    for line in git(repo, "blame", "--line-porcelain", rev, "--", path).splitlines():
        header = _HEADER.match(line)
        if header:
            current = header.group(1)
            counts[current] += 1
        elif line == "boundary" and current is not None:
            boundaries.add(current)
    return counts, boundaries


def _shares(counter: Counter) -> dict[str, float]:
    total = sum(counter.values())
    return {key: round(value / total, 4) for key, value in sorted(counter.items())} if total else {}


def report(repo: Path, rules: Rules, rev: str = "HEAD", ranges: list[tuple[str, str]] | None = None) -> dict:
    repo = Path(repo)
    head = resolve(repo, rev)
    shallow = is_shallow(repo)
    origins = range_origins(repo, ranges or [])
    for sha, builder in _branch_origins(repo, head, rules).items():
        origins.setdefault(sha, builder)
    builders: dict[str, str] = {}
    lines: Counter = Counter()
    critical: Counter = Counter()
    files = [p for p in git(repo, "ls-tree", "-r", "--name-only", head).splitlines() if _matches(p, rules.include)]
    for path in files:
        counts, boundaries = _blame_counts(repo, head, path)
        for sha, count in counts.items():
            if shallow and sha in boundaries:
                builder = SHALLOW_BOUNDARY
            else:
                if sha not in builders:
                    builders[sha] = classify(repo, sha, rules, origins)
                builder = builders[sha]
            lines[builder] += count
            if _matches(path, rules.critical):
                critical[builder] += count
    warnings = []
    if shallow:
        warnings.append("SHALLOW_CLONE_LINES_AT_BOUNDARY_ARE_UNKNOWN")
    if lines.get(UNATTRIBUTED):
        warnings.append("SOME_LINES_UNATTRIBUTED")
    return {
        "revision": head,
        "rules_version": rules.version,
        "ranges": [f"{spec}={builder}" for spec, builder in (ranges or [])],
        "shallow": shallow,
        "files": len(files),
        "lines_by_builder": dict(sorted(lines.items())),
        "share_by_builder": _shares(lines),
        "critical_lines_by_builder": dict(sorted(critical.items())),
        "critical_share_by_builder": _shares(critical),
        "warnings": warnings,
    }
