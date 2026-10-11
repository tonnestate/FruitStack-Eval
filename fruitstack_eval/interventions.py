"""Typed log of human interventions (protocol section 6, threat 3; hypothesis H8).

Authority acts (sign, promote, approve, merge, account administration, stop) are
allowed in every phase. Cognitive acts (hints, repairs, rephrasing, doing the task,
overriding a verdict, picking an output) are protocol deviations in the confirmatory
phase. Every act carries the minutes it took, so human time enters the cost C_O.
"""
from __future__ import annotations

import json
import uuid
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

AUTHORITY_ACTIONS = frozenset({"PROMOTE_POLICY", "APPROVE_EFFECT", "SIGN", "MERGE", "ACCOUNT_ADMIN", "STOP"})
COGNITIVE_ACTIONS = frozenset({"HINT", "REPAIR", "REPHRASE", "MANUAL_TASK", "OVERRIDE_VERDICT", "SELECT_OUTPUT"})
KINDS = {"AUTHORITY": AUTHORITY_ACTIONS, "COGNITIVE": COGNITIVE_ACTIONS}
PHASES = frozenset({"DEVELOPMENT", "PILOT", "CONFIRMATORY"})
MAX_MINUTES = 24 * 60


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Intervention:
    actor: str
    kind: str
    action: str
    minutes: float
    phase: str
    refs: tuple[str, ...] = ()
    note: str | None = None
    recorded_at: str = field(default_factory=_utc_now)
    intervention_id: str = field(default_factory=lambda: f"intervention_{uuid.uuid4().hex}")

    def __post_init__(self) -> None:
        if not self.actor or not self.actor.strip():
            raise ValueError("actor is required")
        if self.kind not in KINDS:
            raise ValueError(f"kind must be one of {sorted(KINDS)}")
        if self.action not in KINDS[self.kind]:
            raise ValueError(f"action {self.action} does not belong to kind {self.kind}")
        if (isinstance(self.minutes, bool) or not isinstance(self.minutes, (int, float))
                or not 0 <= self.minutes <= MAX_MINUTES):
            raise ValueError(f"minutes must be in 0..{MAX_MINUTES}")
        if self.phase not in PHASES:
            raise ValueError(f"phase must be one of {sorted(PHASES)}")
        parsed = datetime.fromisoformat(self.recorded_at)
        if parsed.tzinfo is None:
            raise ValueError("recorded_at must carry a timezone")
        object.__setattr__(self, "refs", tuple(self.refs))

    @property
    def is_deviation(self) -> bool:
        return self.kind == "COGNITIVE" and self.phase == "CONFIRMATORY"

    def to_dict(self) -> dict:
        data = asdict(self)
        data["refs"] = list(self.refs)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Intervention":
        values = dict(data)
        values["refs"] = tuple(values.get("refs") or ())
        return cls(**values)


def append(path: Path, item: Intervention) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")


def load(path: Path) -> tuple[list[Intervention], list[str]]:
    items: list[Intervention] = []
    warnings: list[str] = []
    path = Path(path)
    if not path.exists():
        return items, warnings
    seen: set[str] = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = Intervention.from_dict(json.loads(line))
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            warnings.append(f"line {lineno}: {exc}")
            continue
        if item.intervention_id in seen:
            warnings.append(f"line {lineno}: duplicate {item.intervention_id}")
            continue
        seen.add(item.intervention_id)
        items.append(item)
    return items, warnings


def summarize(items: Iterable[Intervention], verified_tasks: int | None = None) -> dict:
    items = list(items)
    count_by_kind: Counter = Counter(item.kind for item in items)
    minutes_by_kind: dict[str, float] = defaultdict(float)
    monthly: dict[str, Counter] = defaultdict(Counter)
    for item in items:
        minutes_by_kind[item.kind] += float(item.minutes)
        month = datetime.fromisoformat(item.recorded_at).astimezone(timezone.utc).strftime("%Y-%m")
        monthly[month][item.kind] += 1
    deviations = [item.intervention_id for item in items if item.is_deviation]
    summary = {
        "interventions": len(items),
        "count_by_kind": {kind: count_by_kind.get(kind, 0) for kind in sorted(KINDS)},
        "minutes_by_kind": {kind: round(minutes_by_kind.get(kind, 0.0), 2) for kind in sorted(KINDS)},
        "total_minutes": round(sum(minutes_by_kind.values()), 2),
        "confirmatory_deviations": deviations,
        "monthly": {month: dict(sorted(counts.items())) for month, counts in sorted(monthly.items())},
    }
    if verified_tasks is not None:
        if verified_tasks <= 0:
            raise ValueError("verified_tasks must be positive")
        summary["per_100_verified_tasks"] = {
            kind: round(100.0 * count_by_kind.get(kind, 0) / verified_tasks, 3) for kind in sorted(KINDS)
        }
    return summary
