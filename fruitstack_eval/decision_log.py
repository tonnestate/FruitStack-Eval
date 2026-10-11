"""Read-only reader for PlumMe DecisionLog exports.

PlumMe persists append-only JSONL rows of the form {"type": ..., "data": {...}} with
types "decision", "outcome" and "feedback". Rotated segments are named
<file>.1, <file>.2, ... where the highest suffix is the oldest. This reader does not
import PlumMe: the evaluator must stay independent of the system under test.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

ROW_TYPES = ("decision", "outcome", "feedback")


@dataclass
class DecisionView:
    decision: dict
    outcomes: list[dict] = field(default_factory=list)
    feedback: list[dict] = field(default_factory=list)

    @property
    def decision_id(self) -> str:
        return self.decision["decision_id"]

    def latest_feedback(self) -> dict | None:
        return self.feedback[-1] if self.feedback else None


def segment_paths(path: Path, max_segments: int = 64) -> list[Path]:
    """Existing segments, oldest first, current file last."""
    path = Path(path)
    older = [path.with_name(f"{path.name}.{i}") for i in range(max_segments, 0, -1)]
    return [p for p in [*older, path] if p.exists()]


def read_events(path: Path) -> tuple[list[tuple[str, dict]], list[str]]:
    events: list[tuple[str, dict]] = []
    warnings: list[str] = []
    for segment in segment_paths(path):
        for lineno, line in enumerate(segment.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(f"{segment.name}:{lineno}: invalid JSON ({exc.msg})")
                continue
            kind = raw.get("type") if isinstance(raw, dict) else None
            data = raw.get("data") if isinstance(raw, dict) else None
            if kind not in ROW_TYPES or not isinstance(data, dict):
                warnings.append(f"{segment.name}:{lineno}: unknown or malformed row")
                continue
            if "decision_id" not in data:
                warnings.append(f"{segment.name}:{lineno}: {kind} row without decision_id")
                continue
            events.append((kind, data))
    return events, warnings


def load_views(path: Path) -> tuple[dict[str, DecisionView], list[str]]:
    """Group events by decision in file order. Orphans and duplicates become warnings."""
    events, warnings = read_events(path)
    views: dict[str, DecisionView] = {}
    for kind, data in events:
        decision_id = data["decision_id"]
        if kind == "decision":
            if decision_id in views:
                warnings.append(f"duplicate decision {decision_id}")
                continue
            views[decision_id] = DecisionView(decision=data)
            continue
        view = views.get(decision_id)
        if view is None:
            warnings.append(f"orphan {kind} for unknown decision {decision_id}")
            continue
        (view.outcomes if kind == "outcome" else view.feedback).append(data)
    return views, warnings
