"""Sandboxed execution of untrusted candidate code.

Pattern reused from runners/ogi013_code_task.py (Sandbox.run_python): bwrap with a read-only host,
network off, only the workspace writable. Additions: fresh temp dir per run, /root and /home hidden
(datasets, keys and evidence live there) with only the interpreter's prefixes bound back, /tmp replaced
by an empty tmpfs (the evaluator's own temp files are invisible), a separate pid namespace, rlimits,
process-group kill on timeout.

Fail closed. Without bwrap, `wrap` raises SANDBOX_UNAVAILABLE. Only a non-confirmatory (dev) run may
fall back to rlimits only, and only with OGI_ALLOW_UNSANDBOXED=1; the row then says "rlimit-only".
Confirmatory runs ignore OGI_ALLOW_UNSANDBOXED and additionally require `preflight()` to show that
bwrap can actually create the namespaces (a bwrap binary that cannot unshare would otherwise turn every
candidate into an ERROR and silently bias the evidence).
"""
from __future__ import annotations

import functools
import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HIDDEN_ROOTS = ("/root", "/home")
MAX_OUTPUT = 20_000
ISOLATED = "bwrap-unshare-all-rlimit"


@functools.lru_cache(maxsize=None)
def _exposed(python: str) -> list[str]:
    """bwrap args that make `python` (a venv and its base interpreter) usable under the hidden roots:
    the venv dir, the dir holding the base interpreter, and every symlink hop to the binary."""
    prefix, base = subprocess.run([python, "-I", "-c", "import sys;print(sys.prefix);print(sys.base_prefix)"],
                                  capture_output=True, text=True, timeout=30, check=True).stdout.split()
    dirs = list(dict.fromkeys([prefix, os.path.dirname(base)]))
    args = [a for d in dirs if d.startswith(HIDDEN_ROOTS) for a in ("--ro-bind", d, d)]
    p = python
    while os.path.islink(p):
        target = os.readlink(p)
        if p.startswith(HIDDEN_ROOTS) and not any(p.startswith(d + os.sep) for d in dirs):
            args += ["--symlink", target, p]
        p = os.path.join(os.path.dirname(p), target)
    return args


def limits(cpu_s: int, mem_mb: int) -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_s, cpu_s + 1))
    resource.setrlimit(resource.RLIMIT_AS, (mem_mb << 20, mem_mb << 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (64 << 20, 64 << 20))
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def wrap(argv: list[str], workdir: str, python: str, *, confirmatory: bool,
         allow_unsandboxed: bool | None = None) -> tuple[list[str], str]:
    """-> (command running `python -E -s <argv>` inside the sandbox with only `workdir` writable, isolation).
    allow_unsandboxed=None reads OGI_ALLOW_UNSANDBOXED; the evaluator passes the grader's decision instead."""
    cmd = [python, "-E", "-s", *argv]
    if shutil.which("bwrap"):
        hide = [a for r in HIDDEN_ROOTS if os.path.isdir(r) for a in ("--tmpfs", r)]
        return ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
                *hide, *_exposed(python), "--bind", workdir, workdir, "--unshare-all", "--cap-drop", "ALL",
                "--die-with-parent", "--new-session", "--chdir", workdir, *cmd], ISOLATED
    if confirmatory:                                         # OGI_ALLOW_UNSANDBOXED is deliberately not consulted
        raise RuntimeError("SANDBOX_UNAVAILABLE: confirmatory grading requires bwrap (OGI_ALLOW_UNSANDBOXED is ignored)")
    if allow_unsandboxed is None:
        allow_unsandboxed = os.environ.get("OGI_ALLOW_UNSANDBOXED") == "1"
    if allow_unsandboxed:                                    # dev mode, explicit opt-in only; recorded in evidence
        return cmd, "rlimit-only"
    raise RuntimeError("SANDBOX_UNAVAILABLE: bwrap not found; set OGI_ALLOW_UNSANDBOXED=1 to run with rlimits only (dev mode)")


_PREFLIGHT_OK: set[str] = set()


def preflight(python: str) -> None:
    """Confirmatory safeguard: prove bwrap can unshare and run `python` here. Success is cached per interpreter."""
    if python in _PREFLIGHT_OK:
        return
    with tempfile.TemporaryDirectory(prefix="ogi-pre-") as d:
        cmd, _ = wrap(["-c", "import os; print(os.getpid())"], d, python, confirmatory=True)
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, timeout=60, env={"PATH": "/usr/bin:/bin"})
    if r.returncode != 0 or r.stdout.strip() in ("", str(os.getpid())):
        raise RuntimeError(f"SANDBOX_UNAVAILABLE: bwrap preflight failed (exit {r.returncode}): {r.stderr[-300:]}")
    _PREFLIGHT_OK.add(python)


def env(home: str) -> dict:
    return {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home, "PYTHONDONTWRITEBYTECODE": "1",
            "MPLBACKEND": "Agg", "PYTHONHASHSEED": "0"}


def run_python(files: dict[str, str], argv: list[str], *, python: str = sys.executable,
               timeout: float = 120, mem_mb: int = 4096, confirmatory: bool = False) -> dict:
    """Write `files` into a fresh temp dir and run `python <argv>` there (one-shot; no grading).

    Returns {exit, timeout, stdout, stderr, isolation, outputs}; `outputs` holds the text of every
    `*.json` file in the workspace after the run. Never use `outputs` as a verdict: the code wrote it."""
    python = os.path.abspath(python)                 # the sandbox chdirs; keep the venv symlink (not realpath)
    with tempfile.TemporaryDirectory(prefix="ogi-sbx-") as d:
        for name, text in files.items():
            Path(d, name).write_text(text, encoding="utf-8")
        cmd, isolation = wrap(argv, d, python, confirmatory=confirmatory)
        p = subprocess.Popen(cmd, cwd=d, env=env(d), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                             errors="replace", start_new_session=True,
                             preexec_fn=lambda: limits(int(timeout) + 1, mem_mb))
        timed_out = False
        try:
            out, err = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(p.pid, signal.SIGKILL)
            out, err = p.communicate()
        outputs = {f.name: f.read_text(errors="replace")[:MAX_OUTPUT] for f in Path(d).glob("*.json") if f.is_file()}
    return {"exit": p.returncode, "timeout": timed_out, "stdout": out[-MAX_OUTPUT:], "stderr": err[-MAX_OUTPUT:],
            "isolation": isolation, "outputs": outputs}
