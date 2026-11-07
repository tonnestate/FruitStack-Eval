"""OGI-013 coding-driver submit gate (driver defect fix, AMENDMENT-DRIVER-1).

Defect it removes: the first FruitStack run on django__django-11019 let the episode `submit` without an actual source-code
diff, and Brother Mode then criticised a text answer instead of a code patch. That does not test code problem-solving.

What this module does, and nothing more:
  * `check_submit()` rejects a submit when (a) the workspace has no substantive source-code diff against the base
    revision, or (b) no relevant test run happened after the most recent source edit. The rejection text is neutral
    (it names the missing evidence, never a solution); the driver returns it to the agent as the tool result and the
    episode continues through the existing coding tools under the existing hard limits.
  * `snapshot(label)` freezes an accepted patch (P0 before criticism, P1 after revision, ...) as an immutable file with
    its sha256. Brother Mode may only be started with `review_target()`, which raises unless P0 exists.
  * Every decision is appended to `gate.jsonl` for the evidence folder.

It never edits the workspace, never reads hidden tests, gold patches or hints, and never decides success.

"Relevant test run" (objective, outcome-independent):
  the run happened after the last source edit, the runner output shows >= 1 executed test, and either the command named
  no labels (whole suite) or at least one named test file/module references the package of a changed source file
  (e.g. a change to django/forms/widgets.py makes any test file that mentions "django.forms" relevant).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

RAN_RE = re.compile(r"^Ran (\d+) tests? in ", re.M)                                  # unittest / Django runner
PYTEST_RE = re.compile(r"(\d+) (?:passed|failed|errors?)\b")                          # pytest summary
NO_DIFF = "SUBMIT_REJECTED: the workspace has no source-code change relative to the base revision. Change the code, then submit."
NO_TEST = ("SUBMIT_REJECTED: no test run that exercises the changed code was recorded after your last source edit. "
           "Run the relevant existing tests with run_tests, inspect the result, then submit.")


@dataclass(frozen=True)
class SubmitDecision:
    accepted: bool
    reason: str
    diff: str
    diff_sha256: str | None
    changed_source_files: tuple


class GateError(RuntimeError):
    pass


class CodingGate:
    def __init__(self, workspace: str | Path, base_commit: str, out_dir: str | Path, *,
                 source_prefixes: tuple = ("django/",), test_prefixes: tuple = ("tests/",)):
        self.ws = Path(workspace).resolve()
        self.base = base_commit
        self.out = Path(out_dir).resolve()
        self.out.mkdir(parents=True, exist_ok=True)
        self.src_prefixes = source_prefixes
        self.test_prefixes = test_prefixes
        self._seq = 0
        self._last_edit_seq = -1
        self._tests: list[dict] = []
        self._snapshots: dict[str, str] = {}
        if subprocess.run(["git", "cat-file", "-e", f"{base_commit}^{{commit}}"], cwd=self.ws, capture_output=True).returncode:
            raise GateError(f"base commit {base_commit} not present in {self.ws}")

    # ---- event recording (called by the driver after each tool call) ----------------------------------------------
    def record_edit(self, path: str) -> None:
        self._seq += 1
        rel = self._rel(path)
        if self._is_source(rel):
            self._last_edit_seq = self._seq
        self._log({"event": "edit", "seq": self._seq, "path": rel, "source": self._is_source(rel)})

    def record_test_run(self, command, exit_code: int, output: str) -> dict:
        self._seq += 1
        argv = shlex.split(command) if isinstance(command, str) else list(command)
        n = sum(int(x) for x in RAN_RE.findall(output)) or sum(int(x) for x in PYTEST_RE.findall(output))
        entry = {"event": "test_run", "seq": self._seq, "argv": argv, "exit_code": exit_code, "tests_executed": n,
                 "labels": self._labels(argv)}
        self._tests.append(entry)
        self._log(entry)
        return entry

    # ---- gate ------------------------------------------------------------------------------------------------------
    def check_submit(self) -> SubmitDecision:
        diff, substantive, files = self._source_diff()
        if not substantive:
            return self._decide(False, NO_DIFF, diff, files)
        relevant = [t for t in self._tests if t["seq"] > self._last_edit_seq and t["tests_executed"] >= 1
                    and self._is_relevant(t["labels"], files)]
        if not relevant:
            return self._decide(False, NO_TEST, diff, files)
        return self._decide(True, f"ACCEPTED: relevant test run seq={relevant[-1]['seq']}", diff, files)

    def snapshot(self, label: str, decision: SubmitDecision) -> Path:
        if not decision.accepted:
            raise GateError("only an accepted submission can be snapshotted")
        if not re.fullmatch(r"P\d+", label):
            raise GateError("snapshot labels are P0, P1, ...")
        path = self.out / f"{label}.diff"
        if path.exists():
            raise GateError(f"{label} already frozen; snapshots are immutable")
        path.write_text(decision.diff)
        os.chmod(path, 0o444)
        self._snapshots[label] = decision.diff_sha256
        self._log({"event": "snapshot", "label": label, "sha256": decision.diff_sha256, "files": list(decision.changed_source_files)})
        return path

    def review_target(self) -> str:
        """The only legitimate input for Brother Mode's consequential patch review: the frozen P0 diff."""
        p0 = self.out / "P0.diff"
        if "P0" not in self._snapshots or not p0.exists():
            raise GateError("Brother Mode review requested without a frozen candidate patch P0")
        text = p0.read_text()
        if hashlib.sha256(text.encode()).hexdigest() != self._snapshots["P0"]:
            raise GateError("P0.diff changed after it was frozen")
        return text

    def outcome_without_patch(self, limit_hit: str) -> dict:
        rec = {"event": "episode_end", "outcome": "NO_PATCH", "limit_hit": limit_hit, "snapshots": dict(self._snapshots)}
        self._log(rec)
        return rec

    # ---- internals -------------------------------------------------------------------------------------------------
    def _rel(self, path: str) -> str:
        p = Path(path)
        return str((p if p.is_absolute() else self.ws / p).resolve().relative_to(self.ws))

    def _is_source(self, rel: str) -> bool:
        return rel.startswith(self.src_prefixes) and not rel.startswith(self.test_prefixes) and rel.endswith(".py")

    def _source_diff(self):
        with tempfile.TemporaryDirectory() as tmp:            # temporary index: includes new files, never touches the agent's index
            env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
            subprocess.run(["git", "read-tree", self.base], cwd=self.ws, env=env, check=True, capture_output=True)
            subprocess.run(["git", "add", "-A", "--", *self.src_prefixes], cwd=self.ws, env=env, check=True, capture_output=True)
            spec = [*self.src_prefixes] + [f":(exclude){p}" for p in self.test_prefixes]
            full = subprocess.run(["git", "diff", "--cached", "--no-color", self.base, "--", *spec], cwd=self.ws, env=env,
                                  capture_output=True, text=True, check=True).stdout
            # --name-only ignores -w, so substance is judged from the hunks of the whitespace-insensitive patch
            ws_patch = subprocess.run(["git", "diff", "--cached", "--no-color", "-w", "--ignore-blank-lines", self.base, "--", *spec],
                                      cwd=self.ws, env=env, capture_output=True, text=True, check=True).stdout
        files = tuple(m.group(2) for m in re.finditer(r"^diff --git a/(\S+) b/(\S+)\n(?:(?!diff --git ).*\n)*?@@ ", ws_patch, re.M)
                      if m.group(2).endswith(".py"))
        return full, bool(files), files

    def _labels(self, argv: list) -> list:
        return [a for a in argv[1:] if not a.startswith("-") and not a.endswith(("runtests.py", "pytest", "python", "python3"))
                and not re.fullmatch(r"\d+", a) and (re.fullmatch(r"[\w.]+", a) or "/" in a or "::" in a)]

    def _test_files_for(self, label: str) -> list:
        if "/" in label or "::" in label:                           # pytest path
            p = self.ws / label.split("::")[0]
            return [p] if p.is_file() else sorted(p.rglob("test*.py")) if p.is_dir() else []
        parts = label.split(".")
        for k in range(len(parts), 0, -1):                          # Django dotted label -> tests/<a>/<b>.py or package dir
            for root in self.test_prefixes:
                base = self.ws / root / Path(*parts[:k])
                if base.with_suffix(".py").is_file():
                    return [base.with_suffix(".py")]
                if base.is_dir():
                    return sorted(base.rglob("*.py"))
        return []

    def _is_relevant(self, labels: list, changed: tuple) -> bool:
        if not labels:
            return True                                             # whole-suite run with >= 1 executed test
        # package of each changed file, only when at least two levels deep ("django.forms", never bare "django")
        packages = {".".join(Path(f).with_suffix("").parts[:-1]) for f in changed if len(Path(f).parts) >= 3}
        modules = {".".join(Path(f).with_suffix("").parts) for f in changed}
        for label in labels:
            for tf in self._test_files_for(label):
                text = tf.read_text(errors="ignore")
                if any(m in text for m in modules) or any(p and p in text for p in packages):
                    return True
        return False

    def _decide(self, ok: bool, reason: str, diff: str, files: tuple) -> SubmitDecision:
        sha = hashlib.sha256(diff.encode()).hexdigest() if diff else None
        d = SubmitDecision(ok, reason, diff, sha, files)
        self._log({"event": "submit_check", "seq": self._seq, "accepted": ok, "reason": reason, "diff_sha256": sha,
                   "changed_source_files": list(files)})
        return d

    def _log(self, rec: dict) -> None:
        rec = {"t": time.time(), **rec}
        with open(self.out / "gate.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
