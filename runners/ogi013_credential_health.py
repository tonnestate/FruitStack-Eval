"""Credential-health carry-forward across processes (OGI-013 harness; PlumMe's routing is untouched).

Root cause it removes: PlumMe keeps credential health (billing disablement, cooldowns, failure counts) in the state directory of ONE process; every episode of a campaign has its own state directory, so a
credential that returned BILLING_OR_CREDIT_EXHAUSTED (Groq, 2026-10-29) looked healthy again to the next episode, the next block attempt and the next simulator selection; and inside one process PlumMe resets the
billing counters when the window expires, so the same ~600 s cooldown repeated instead of growing.

Mechanism (active only when OGI013_PILOT_RUNS is set, i.e. in campaigns; the frozen conditions never set it): at episode start every earlier episode's `credential_sources.json` (finished, failed, interrupted or
archived) is merged into ONE registry `<runs>/credential_health.json` (the most recent evidence per credential wins) and the registry is written as the new episode's `credential_sources.json`, which PlumMe loads
natively; at exit the episode's own health is merged back. Billing exhaustion is sticky and escalating: the registry counts exhaustion events per credential without an intervening success and re-disables the
credential until `last_failure + PlumMe's own backoff_s("billing", events)` (10 min, 20, 40 ... 24 h). A cooldown that merely expired is not evidence of renewed credit: the credential is tried again only after that
window and only a SUCCESS resets the count; one more exhaustion doubles the window."""
from __future__ import annotations

import atexit
import copy
import json
import os
import tempfile
import time
from pathlib import Path

BILLING = "BILLING_OR_CREDIT_EXHAUSTED"
STATE_FILE = "credential_sources.json"


def _backoff(events: int) -> float:
    from plumme.backoff import backoff_s
    return backoff_s("billing", events)


def _evidence(health: dict) -> float:
    return max(float(health.get("last_success_at") or 0), float(health.get("last_failure_at") or 0))


class Registry:
    def __init__(self, path: Path):
        self.path = Path(path)
        data = {}
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = {}
        self.sources: dict[str, dict] = data.get("sources", {})
        self.billing: dict[str, dict] = data.get("billing", {})

    def merge_state(self, state_file: Path) -> None:
        try:
            rows = json.loads(Path(state_file).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for s in rows:
            handle, health = s.get("handle"), s.get("health") or {}
            if not handle:
                continue
            old = self.sources.get(handle)
            if old is None or _evidence(health) >= _evidence(old.get("health") or {}):
                self.sources[handle] = s
            b = self.billing.setdefault(handle, {"events": 0, "last_at": 0.0})
            failed_at = float(health.get("last_failure_at") or 0)
            if health.get("last_failure_class") == BILLING and failed_at > b["last_at"]:
                b["events"] += 1
                b["last_at"] = failed_at
            if float(health.get("last_success_at") or 0) > b["last_at"]:        # evidence of renewed availability: the only thing that resets the count
                b["events"] = 0

    def seed_rows(self, now: float | None = None) -> list[dict]:
        now = time.time() if now is None else now
        rows = []
        for handle, s in self.sources.items():
            s = copy.deepcopy(s)
            b = self.billing.get(handle) or {}
            if b.get("events", 0) > 0 and b.get("last_at"):
                until = float(b["last_at"]) + _backoff(int(b["events"]))
                if until > now:
                    s.setdefault("health", {}).update(disabled_until=max(float(s["health"].get("disabled_until") or 0), until), disabled_reason="billing")
            rows.append(s)
        return rows

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(prefix=".credential_health.", dir=str(self.path.parent))
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"sources": self.sources, "billing": self.billing}, f, sort_keys=True)
        os.replace(temp, self.path)


def harvest_all(registry: Registry, runs: Path, skip: Path | None = None) -> int:
    """Merge every earlier episode's credential health (oldest first, so the latest evidence wins)."""
    files = sorted((p for p in Path(runs).rglob(f"fruitstack/plumme-state/{STATE_FILE}") if skip is None or skip not in p.parents), key=lambda p: p.stat().st_mtime)
    for f in files:
        registry.merge_state(f)
    return len(files)


def prepare_state(state_dir: Path) -> None:
    """Called by the harness before PlumMe is built: seed the episode's credential health from the campaign registry and arrange for it to be merged back at exit."""
    runs = os.environ.get("OGI013_PILOT_RUNS")
    if not runs:
        return
    state_dir = Path(state_dir)
    reg = Registry(Path(runs) / "credential_health.json")
    harvest_all(reg, Path(runs), skip=state_dir)
    reg.save()
    seed = reg.seed_rows()
    target = state_dir / STATE_FILE
    if seed and not target.exists():
        target.write_text(json.dumps(seed, indent=1), encoding="utf-8")

    def merge_back() -> None:
        try:
            r = Registry(Path(runs) / "credential_health.json")
            r.merge_state(target)
            r.save()
        except Exception:  # noqa: BLE001 - bookkeeping must never fail an episode
            pass
    atexit.register(merge_back)
