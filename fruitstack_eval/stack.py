"""Stack preflight: is the whole FruitStack installed from its canonical source before an evaluation starts?

An evaluation of one part without the others measures a different system. Before any run the host checks, for every
component in ``config/stack.toml``:

- the distribution is installed in the host interpreter (read from package metadata in a subprocess; no product
  package is imported, so the evaluator stays independent of the system under test);
- an editable install points at a git checkout whose HEAD equals that checkout's ``origin/main`` and has no local
  changes (the canonical source, not a hand-patched copy);
- required paths exist (for example the CogC skill directory) and required systemd units are active.

A required component that fails any check blocks the run; optional components are reported only.
"""
from __future__ import annotations

import json
import subprocess
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

_PROBE = r"""
import json, sys
from importlib import metadata
out = {}
for name in json.loads(sys.argv[1]):
    try:
        dist = metadata.distribution(name)
    except metadata.PackageNotFoundError:
        out[name] = {"installed": False}
        continue
    direct = dist.read_text("direct_url.json")
    info = {"installed": True, "version": dist.version}
    if direct:
        d = json.loads(direct)
        info["url"] = d.get("url")
        info["editable"] = bool((d.get("dir_info") or {}).get("editable"))
        info["vcs_commit"] = (d.get("vcs_info") or {}).get("commit_id")
    out[name] = info
print(json.dumps(out))
"""


@dataclass(frozen=True)
class Component:
    name: str
    dist: str | None = None
    required: bool = True
    paths: tuple[str, ...] = ()
    units: tuple[str, ...] = ()
    role: str = ""


@dataclass
class ComponentResult:
    name: str
    required: bool
    ok: bool = False
    checks: dict = field(default_factory=dict)
    problems: list[str] = field(default_factory=list)


def load(path: Path) -> list[Component]:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for name, spec in (data.get("component") or {}).items():
        out.append(Component(name=name, dist=spec.get("dist"), required=bool(spec.get("required", True)),
                             paths=tuple(spec.get("paths", [])), units=tuple(spec.get("units", [])), role=spec.get("role", "")))
    if not out:
        raise ValueError("stack config needs [component.<name>] tables")
    return out


def _git(directory: Path, *args: str) -> str | None:
    done = subprocess.run(["git", "-C", str(directory), *args], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def _checkout_of(url: str | None) -> Path | None:
    if not url or not url.startswith("file://"):
        return None
    path = Path(url[len("file://"):])
    while path != path.parent:
        if (path / ".git").exists():
            return path
        path = path.parent
    return None


def probe_distributions(python: str, dists: list[str]) -> dict:
    done = subprocess.run([python, "-I", "-c", _PROBE, json.dumps(dists)], capture_output=True, text=True, timeout=120)
    if done.returncode != 0:
        raise ValueError(f"cannot read package metadata with {python}: {done.stderr.strip()[-300:]}")
    return json.loads(done.stdout)


def unit_active(unit: str) -> bool:
    done = subprocess.run(["systemctl", "is-active", unit], capture_output=True, text=True)
    return done.stdout.strip() == "active"


def check(components: list[Component], python: str, *, fetch: bool = False, units_probe=unit_active) -> dict:
    meta = probe_distributions(python, [c.dist for c in components if c.dist])
    results = []
    for c in components:
        r = ComponentResult(name=c.name, required=c.required)
        if c.dist:
            info = meta.get(c.dist, {"installed": False})
            r.checks["distribution"] = {"name": c.dist, **info}
            if not info.get("installed"):
                r.problems.append(f"{c.dist} is not installed in {python}")
            else:
                checkout = _checkout_of(info.get("url"))
                if info.get("editable") and checkout is not None:
                    if fetch:
                        _git(checkout, "fetch", "--quiet", "origin")
                    head, main = _git(checkout, "rev-parse", "HEAD"), _git(checkout, "rev-parse", "refs/remotes/origin/main")
                    dirty = bool(_git(checkout, "status", "--porcelain", "--untracked-files=no"))
                    r.checks["checkout"] = {"path": str(checkout), "head": head, "origin_main": main, "dirty": dirty}
                    if head is None or main is None or head != main:
                        r.problems.append(f"checkout {checkout} HEAD {str(head)[:12]} != origin/main {str(main)[:12]}")
                    if dirty:
                        r.problems.append(f"checkout {checkout} has local changes")
                elif info.get("vcs_commit"):
                    r.checks["installed_commit"] = info["vcs_commit"]
                else:
                    r.problems.append(f"{c.dist} {info.get('version')} is not installed from a git checkout: source commit unknown")
        for p in c.paths:
            exists = Path(p).exists()
            r.checks.setdefault("paths", {})[p] = exists
            if not exists:
                r.problems.append(f"missing path {p}")
        for unit in c.units:
            active = units_probe(unit)
            r.checks.setdefault("units", {})[unit] = active
            if not active:
                r.problems.append(f"unit {unit} is not active")
        r.ok = not r.problems
        results.append(r)
    blocking = [r.name for r in results if r.required and not r.ok]
    return {"gate": "STACK", "passed": not blocking, "blocking": blocking, "python": python,
            "components": [{"name": r.name, "required": r.required, "ok": r.ok, "checks": r.checks, "problems": r.problems}
                           for r in results]}
