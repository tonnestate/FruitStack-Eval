"""Sandboxed execution of untrusted candidate code.

Pattern reused from runners/ogi013_code_task.py (Sandbox.run_python): bwrap with a read-only host,
network off, only the workspace writable. Additions: fresh temp dir per run, /root and /home hidden
(datasets, keys and evidence live there) with only the interpreter's prefixes bound back, rlimits,
process-group kill on timeout. Without bwrap the run falls back to rlimits only and says so in the
evidence ("isolation"), so a grader row can never silently claim network isolation it did not have.
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


def _limits(cpu_s: int, mem_mb: int) -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_s, cpu_s + 1))
    resource.setrlimit(resource.RLIMIT_AS, (mem_mb << 20, mem_mb << 20))
    resource.setrlimit(resource.RLIMIT_FSIZE, (64 << 20, 64 << 20))
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run_python(files: dict[str, str], argv: list[str], *, python: str = sys.executable,
               timeout: float = 120, mem_mb: int = 4096) -> dict:
    """Write `files` into a fresh temp dir and run `python <argv>` there.

    Returns {exit, timeout, stdout, stderr, isolation, outputs}; `outputs` holds the text of every
    `*.json` file in the workspace after the run (how the test harness reports results)."""
    python = os.path.abspath(python)                 # the sandbox chdirs; keep the venv symlink (not realpath)
    with tempfile.TemporaryDirectory(prefix="ogi-sbx-") as d:
        for name, text in files.items():
            Path(d, name).write_text(text, encoding="utf-8")
        cmd = [python, "-E", "-s", *argv]
        if shutil.which("bwrap"):
            isolation = "bwrap-unshare-all-rlimit"
            binds = _exposed(python)
            hide = [a for r in HIDDEN_ROOTS if os.path.isdir(r) for a in ("--tmpfs", r)]
            cmd = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
                   *hide, *binds, "--bind", d, d, "--unshare-all", "--cap-drop", "ALL", "--die-with-parent",
                   "--new-session", "--chdir", d, *cmd]
        elif os.environ.get("OGI_ALLOW_UNSANDBOXED") == "1":   # explicit opt-in only; recorded in evidence
            isolation = "rlimit-only"
        else:                                                    # fail closed: never run untrusted candidate code unisolated by default
            raise RuntimeError("SANDBOX_UNAVAILABLE: bwrap not found; set OGI_ALLOW_UNSANDBOXED=1 to run with rlimits only")
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": d, "PYTHONDONTWRITEBYTECODE": "1",
               "MPLBACKEND": "Agg", "PYTHONHASHSEED": "0"}
        p = subprocess.Popen(cmd, cwd=d, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                             errors="replace", start_new_session=True,
                             preexec_fn=lambda: _limits(int(timeout) + 1, mem_mb))
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
