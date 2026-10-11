"""Readiness gate G6: recompute every reported metric from the raw logs and compare.

An evidence directory produced by the runners holds raw logs (DecisionLogs, results,
interventions) and the derived reports that were committed (independence.json,
g5_logcheck.json, pilot/estimates.json, ...). `replay` recomputes each derived report
from the raw files with the current evaluator and compares it with the committed one,
ignoring only fields that record when something was computed. A difference means the
report cannot be reproduced from its logs.

The steps are declared in `<evidence>/replay.toml`:

    [[step]]
    name = "g2-independence"
    command = ["independence", "--scored", "g2/scored.jsonl"]
    expected = "g2/independence.json"

Paths are relative to the evidence directory; commands are `fse` subcommands. A step
that must write a file (`fse inquiry grade --out`) writes below `replay/`, which `run`
creates, so committed files are never overwritten.
"""
from __future__ import annotations

import contextlib
import io
import json
import tomllib
from pathlib import Path

VOLATILE = frozenset({"graded_at", "created_at", "recorded_at", "finished_at", "seconds", "sealed_at"})


def _strip(value):
    if isinstance(value, dict):
        return {k: _strip(v) for k, v in value.items() if k not in VOLATILE}
    if isinstance(value, list):
        return [_strip(v) for v in value]
    return value


def _diff(a, b, path="$", out=None, limit=20):
    out = [] if out is None else out
    if len(out) >= limit:
        return out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}.{k}: {'missing in replay' if k not in a else 'missing in committed report'}")
            else:
                _diff(a[k], b[k], f"{path}.{k}", out, limit)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path}: length {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            _diff(x, y, f"{path}[{i}]", out, limit)
    elif isinstance(a, float) and isinstance(b, float):
        if abs(a - b) > 1e-12 * max(1.0, abs(a), abs(b)):
            out.append(f"{path}: {a!r} != {b!r}")
    elif a != b:
        out.append(f"{path}: {a!r} != {b!r}")
    return out


def _absolutize(command: list[str], root: Path) -> list[str]:
    """Resolve arguments that name files inside the evidence directory."""
    out = []
    for arg in command:
        candidate = root / arg
        out.append(str(candidate) if not arg.startswith("-") and ("/" in arg or candidate.exists()) else arg)
    return out


def run(evidence: Path, cli_main) -> dict:
    evidence = Path(evidence)
    spec = tomllib.loads((evidence / "replay.toml").read_text(encoding="utf-8"))
    steps = spec.get("step", [])
    if not steps:
        raise ValueError("replay.toml declares no [[step]]")
    (evidence / "replay").mkdir(exist_ok=True)       # replay outputs never overwrite committed files
    results = []
    for step in steps:
        name, expected = step["name"], evidence / step["expected"]
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = cli_main(_absolutize(list(step["command"]), evidence))
        item = {"step": name, "exit_code": code, "expected": step["expected"]}
        try:
            produced = json.loads(buffer.getvalue())
        except json.JSONDecodeError:
            item.update(status="NO_JSON_OUTPUT")
            results.append(item)
            continue
        if not expected.exists():
            item.update(status="EXPECTED_REPORT_MISSING")
        else:
            committed = json.loads(expected.read_text(encoding="utf-8"))
            differences = _diff(_strip(produced), _strip(committed))
            item.update(status="REPRODUCED" if not differences else "DIFFERS", differences=differences)
        results.append(item)
    return {"gate": "G6-replay", "passed": all(r["status"] == "REPRODUCED" for r in results), "steps": results}
