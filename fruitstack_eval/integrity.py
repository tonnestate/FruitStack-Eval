"""Readiness gate G1: repository integrity, read from git only.

For every repository involved in a run, the gate requires

- `main` equal to its mirror `sync/local-truth` (the accepted VPS truth);
- the package version at `main` at least the configured minimum;
- every required path present at `main` (capabilities the hypotheses need);
- every required commit contained in `main` (proposals that must be integrated).

The check runs on local clones, so it never needs credentials beyond a fetch. A clone
whose remote-tracking refs are stale gives a stale answer; `--fetch` refreshes them
first, and every result records the SHAs it compared.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .gitutil import GitError, git

_VERSION = re.compile(r"""__version__\s*=\s*["']([^"']+)["']|^version\s*=\s*["']([^"']+)["']""", re.M)


@dataclass(frozen=True)
class RepoRequirement:
    name: str
    main: str = "main"
    mirror: str | None = "sync/local-truth"
    version_file: str | None = None
    min_version: str | None = None
    required_paths: tuple[str, ...] = ()
    required_commits: tuple[str, ...] = ()
    reason: str = ""


@dataclass
class RepoResult:
    name: str
    passed: bool
    main_sha: str | None = None
    mirror_sha: str | None = None
    version: str | None = None
    problems: list[str] = field(default_factory=list)
    checks: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"name": self.name, "passed": self.passed, "main_sha": self.main_sha, "mirror_sha": self.mirror_sha,
                "version": self.version, "problems": self.problems, "checks": self.checks}


def load_requirements(path: Path) -> list[RepoRequirement]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    repos = data.get("repo", {})
    if not repos:
        raise ValueError("requirements file needs [repo.<name>] tables")
    out = []
    for name, spec in repos.items():
        commits = tuple(spec.get("required_commits", []))
        for sha in commits:
            if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
                raise ValueError(f"{name}: required commit {sha!r} is not a hex SHA")
        if bool(spec.get("min_version")) != bool(spec.get("version_file")):
            raise ValueError(f"{name}: min_version and version_file go together")
        out.append(RepoRequirement(
            name=name, main=spec.get("main", "main"), mirror=spec.get("mirror", "sync/local-truth") or None,
            version_file=spec.get("version_file"), min_version=spec.get("min_version"),
            required_paths=tuple(spec.get("required_paths", [])), required_commits=commits,
            reason=spec.get("reason", ""),
        ))
    return out


def version_tuple(text: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", text.split("+")[0].split("-")[0])
    if not parts:
        raise ValueError(f"not a version: {text!r}")
    return tuple(int(p) for p in parts)


def _ref(repo: Path, remote: str, branch: str) -> str | None:
    try:
        return git(repo, "rev-parse", "--verify", f"refs/remotes/{remote}/{branch}^{{commit}}").strip()
    except GitError:
        return None


def check_repo(clone: Path, req: RepoRequirement, *, remote: str = "origin", fetch: bool = False) -> RepoResult:
    result = RepoResult(name=req.name, passed=False)
    if not (clone / ".git").exists() and not (clone / "HEAD").exists():
        result.problems.append(f"no git clone at {clone}")
        return result
    if fetch:
        try:
            git(clone, "fetch", "--quiet", remote, f"+refs/heads/*:refs/remotes/{remote}/*")
        except GitError as exc:
            result.problems.append(f"fetch failed: {exc}")
            return result
    main = _ref(clone, remote, req.main)
    result.main_sha = main
    if main is None:
        result.problems.append(f"{remote}/{req.main} does not exist")
        return result
    if req.mirror:
        mirror = _ref(clone, remote, req.mirror)
        result.mirror_sha = mirror
        result.checks["mirror_equal"] = mirror == main
        if mirror is None:
            result.problems.append(f"{remote}/{req.mirror} does not exist")
        elif mirror != main:
            result.problems.append(f"TRUTH_NOT_NORMALIZED: {req.main} {main[:12]} != {req.mirror} {mirror[:12]}")
    if req.version_file:
        try:
            text = git(clone, "show", f"{main}:{req.version_file}")
            match = _VERSION.search(text)
            if not match:
                raise ValueError("no version assignment found")
            result.version = match.group(1) or match.group(2)
            ok = version_tuple(result.version) >= version_tuple(req.min_version)
            result.checks["version_at_least"] = {"minimum": req.min_version, "found": result.version, "ok": ok}
            if not ok:
                result.problems.append(f"version {result.version} < required {req.min_version}")
        except (GitError, ValueError) as exc:
            result.problems.append(f"version unreadable from {req.version_file}: {exc}")
    paths = {}
    for path in req.required_paths:
        try:
            git(clone, "cat-file", "-e", f"{main}:{path}")
            paths[path] = True
        except GitError:
            paths[path] = False
            result.problems.append(f"required path missing at {req.main}: {path}")
    if paths:
        result.checks["required_paths"] = paths
    commits = {}
    for sha in req.required_commits:
        try:
            full = git(clone, "rev-parse", "--verify", f"{sha}^{{commit}}").strip()
        except GitError:
            commits[sha] = "UNKNOWN_COMMIT"
            result.problems.append(f"required commit {sha} is not in this clone (fetch the proposal branch)")
            continue
        try:
            git(clone, "merge-base", "--is-ancestor", full, main)
            commits[sha] = "CONTAINED"
        except GitError:
            commits[sha] = "NOT_IN_MAIN"
            result.problems.append(f"required commit {sha[:12]} is not contained in {req.main}")
    if commits:
        result.checks["required_commits"] = commits
    result.passed = not result.problems
    return result


def check(requirements: list[RepoRequirement], clones: Path, *, remote: str = "origin", fetch: bool = False) -> dict:
    results = [check_repo(Path(clones) / req.name, req, remote=remote, fetch=fetch) for req in requirements]
    return {
        "gate": "G1",
        "passed": bool(results) and all(r.passed for r in results),
        "repos": [r.to_dict() for r in results],
        "note": "SHAs are those of the local remote-tracking refs at check time; use --fetch for a current answer.",
    }
