#!/usr/bin/env python3
"""OGI-013 host launcher: repair the existing Python runtime, then run the real runner.

Use the same host Python executable for installation, imports and execution.
Install the OFFICIAL tau2-bench from an existing checkout, never PyPI 'tau2'
(which is unrelated). Canonical FruitStack checkouts are reused in place.
This launcher creates no actor, WorkIdentity, AuthorityEnvelope or tool approval.
"""
from __future__ import annotations

import argparse
import shutil
import os
from pathlib import Path
import subprocess
import sys
import tomllib

COMPONENTS = {
    "mangome": "MangoMe",
    "orangeme": "OrangeMe",
    "peachme": "PeachMe",
    "pomelome": "PomeloMe",
    "plumme": "PlumMe",
    "cherryme": "CherryMe",
    "appleme": "AppleMe",
}


def run(*args: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(args, check=True, env=env)


def verify_python(python: str) -> None:
    result = subprocess.run(
        [python, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
        capture_output=True, text=True, check=True,
    )
    if result.stdout.strip() not in {"3.12", "3.13"}:
        raise RuntimeError(f"Official tau2-bench requires Python 3.12 or 3.13; got {result.stdout.strip()}")


def in_python(python: str, statement: str, *, env: dict[str, str] | None = None) -> bool:
    return subprocess.run([python, "-c", statement], env=env).returncode == 0


def install(python: str, source: Path) -> None:
    # Never pip install tau2 from the index; install ONLY the pinned local tree.
    if in_python(python, "import pip"):
        run(python, "-m", "pip", "install", "--disable-pip-version-check", "-e", str(source))
        return
    if shutil.which("uv"):
        run("uv", "pip", "install", "--python", python, "-e", str(source))
        return
    raise RuntimeError("Neither pip in host Python nor uv available to install existing source")


def verify_tau2_source(source: Path) -> None:
    project = source / "pyproject.toml"
    if not project.is_file() or not (source / "src" / "tau2").is_dir():
        raise ValueError("Expected an existing official tau2-bench source checkout")
    with project.open("rb") as stream:
        meta = tomllib.load(stream)
    url = str(meta.get("project", {}).get("urls", {}).get("Repository", ""))
    if "github.com/sierra-research/tau2-bench" not in url.lower():
        raise ValueError("Source does not identify official sierra-research/tau2-bench repository")


def is_module_from_source(python: str, checkout: Path, *, env: dict[str, str]) -> bool:
    source_path = str((checkout / "src").resolve())
    return in_python(python, (
        "from pathlib import Path; import tau2, loguru; "
        "p=Path(tau2.__file__).resolve(); "
        "assert p.is_relative_to(Path(" + repr(source_path) + "))"
    ), env=env)


def is_component_from_checkout(python: str, module: str, checkout: Path) -> bool:
    expected = str(checkout.resolve())
    return in_python(python, (
        "from pathlib import Path; from importlib.util import find_spec; "
        "s=find_spec(" + repr(module) + "); assert s is not None and s.origin; "
        "assert Path(s.origin).resolve().is_relative_to(Path(" + repr(expected) + "))"
    ))


def parse(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--host-python", required=True, type=Path)
    p.add_argument("--tau2-checkout", required=True, type=Path)
    p.add_argument("--components-root", required=True, type=Path)
    p.add_argument("--runner", required=True, type=Path)
    options, options.runner_args = p.parse_known_args(argv)
    return options


def main(argv: list[str] | None = None) -> int:
    args = parse(argv)
    # Keep the venv entrypoint: resolving it dereferences the symlink to base Python.
    python = os.path.abspath(args.host_python)
    source = args.tau2_checkout.resolve()
    root = args.components_root.resolve()
    runner = args.runner.resolve()
    if not Path(python).is_file() or not runner.is_file():
        raise FileNotFoundError("Host Python or requested OGI-013 runner does not exist")
    verify_python(python)
    verify_tau2_source(source)
    if not root.is_dir():
        raise FileNotFoundError("Canonical component checkout root does not exist")
    # Install only existing canonical components and only when missing from host.
    # No mutable source copy, no new repository, no credentials.
    env = os.environ.copy()
    if not is_module_from_source(python, source, env=env):
        install(python, source)
        if not is_module_from_source(python, source, env=env):
            raise RuntimeError("Official tau2 and loguru still not importable from the pinned source")
    for module, repo in COMPONENTS.items():
        checkout = root / repo
        if not ((checkout / "pyproject.toml").is_file() or (checkout / "setup.py").is_file()):
            raise FileNotFoundError(f"Missing canonical checkout for {repo}: {checkout}")
        if not is_component_from_checkout(python, module, checkout):
            install(python, checkout)
        if not is_component_from_checkout(python, module, checkout):
            raise RuntimeError(f"{module} is not installed from canonical checkout {checkout}")
        head = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        print(f"OGI013_SOURCE {module}={head}", flush=True)
    print(f"OGI013_RUNTIME python={python}", flush=True)
    run(python, str(runner), *args.runner_args, env=env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
