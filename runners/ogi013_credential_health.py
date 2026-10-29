"""Credential-health carry-forward across processes (OGI-013 harness; PlumMe's routing is untouched).

Root cause it removes: PlumMe keeps credential health (billing disablement, cooldowns, failure counts) in the state directory of ONE process; every episode of a campaign has its own state directory, so a
credential that returned BILLING_OR_CREDIT_EXHAUSTED (Groq, 2026-10-29) looked healthy again to the next episode, the next block attempt and the next simulator selection; and inside one process PlumMe resets the
billing counters when the window expires, so the same ~600 s cooldown repeated instead of growing.

Mechanism (active only when OGI013_PILOT_RUNS is set, i.e. in campaigns; the frozen conditions never set it): at episode start every earlier episode's `credential_sources.json` is merged into ONE registry
`<runs>/credential_health.json` (most recent evidence per credential wins) and the registry is written as the new episode's `credential_sources.json`, which PlumMe reads natively; at exit the
episode's own health is merged back.

EXHAUSTED is a state, not a timer (owner corrections 2026-10-29): BILLING_OR_CREDIT_EXHAUSTED marks the credential EXHAUSTED at once; it stays ineligible in every process, episode and restart. No 600 s
cooldown, no exponential ladder, no timer that makes it healthy. Recovery follows the credential's RENEWAL CYCLE (explicit configuration `<runs>/credential_renewal_policy.json`, keyed by handle or
provider: {"cycle": DAILY|WEEKLY|MONTHLY|UNKNOWN, "reset_at": epoch of the next known reset, "source": evidence}; default UNKNOWN = non-renewing, never retried): once per cycle - at the known reset, else
24 h (DAILY) / 7 d (WEEKLY) after the exhaustion; MONTHLY needs a known renewal date - ONE availability probe is allowed (the first real request after the credential is seeded usable for one episode).
A successful probe (a success recorded after the claim) restores AVAILABLE; a failed probe (exhausted again) restores EXHAUSTED until the next cycle's probe; a probe that was never used is released, not spent.
An operator renewal (`python runners/ogi013_credential_health.py renew <runs> <handle>`) is also positive evidence. Persisted per credential: reason, renewal policy, next probe time, last probe result.
Inside the running process `latch_exhaustion` makes PlumMe's own finite billing window permanent the moment it is set. Failure kinds (exhausted credit / rate limit / auth / transient network) are kept
apart: only the first is sticky; the others keep PlumMe's own short, model-scoped handling.
"""
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


CYCLE_S = {"DAILY": 86400.0, "WEEKLY": 604800.0, "MONTHLY": 2592000.0}
FOREVER = 4102444800.0          # 2100-01-01: "ineligible until positive evidence", never a retry time
KINDS = {BILLING: "exhausted_credit", "RATE_LIMITED": "rate_limit", "AUTH_FAILED": "auth", "AUTH_EXPIRED": "auth", "TIMEOUT": "network", "PROVIDER_UNAVAILABLE": "network"}


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
        self.exhausted: dict[str, dict] = data.get("exhausted", {})      # handle -> {"at": failure time, "kind": "exhausted_credit"}
        self.kinds: dict[str, dict] = data.get("kinds", {})              # handle -> {kind: count}: evidence, distinguishes the failure causes
        self.seen: dict[str, float] = data.get("seen", {})               # "handle@failure time" already counted
        self.probes: dict[str, dict] = data.get("probes", {})            # handle -> last probe result (survives recovery)
        pol = self.path.with_name("credential_renewal_policy.json")
        self.policy: dict[str, dict] = json.loads(pol.read_text()) if pol.exists() else {}
        renewals = self.path.with_name("credential_renewals.json")
        self.renewals: dict[str, float] = json.loads(renewals.read_text()) if renewals.exists() else {}

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
            failed_at = float(health.get("last_failure_at") or 0)
            success_at = float(health.get("last_success_at") or 0)
            kind = KINDS.get(health.get("last_failure_class") or "")
            if kind and f"{handle}@{failed_at}" not in self.seen:
                self.seen[f"{handle}@{failed_at}"] = failed_at
                self.kinds.setdefault(handle, {})[kind] = self.kinds.get(handle, {}).get(kind, 0) + 1
                if kind == "exhausted_credit":
                    self._exhaust(handle, s.get("provider"), failed_at)
            ex = self.exhausted.get(handle)
            if ex and success_at > ex["at"]:
                self._recover(handle, success_at, "AVAILABLE")                   # a success after the exhaustion: positive evidence
            elif ex and self.renewals.get(handle, 0.0) > ex["at"]:
                self._recover(handle, self.renewals[handle], "RENEWED_BY_OPERATOR")

    def policy_for(self, handle: str, provider: str | None) -> dict:
        return self.policy.get(handle) or self.policy.get(str(provider)) or {"cycle": "UNKNOWN", "source": "none configured"}

    def next_probe(self, handle: str, provider: str | None, failed_at: float) -> float | None:
        """Earliest time of the next (single) availability probe, from the credential's verified/configured renewal cycle; None = no automatic retry."""
        pol = self.policy_for(handle, provider)
        cycle, length = pol.get("cycle", "UNKNOWN"), CYCLE_S.get(pol.get("cycle", "UNKNOWN"))
        if length is None:
            return None
        reset = pol.get("reset_at")
        if reset is None:
            return None if cycle == "MONTHLY" else failed_at + length             # a monthly renewal must be KNOWN
        reset = float(reset)
        while reset <= failed_at:
            reset += length
        return reset

    def _exhaust(self, handle: str, provider: str | None, failed_at: float) -> None:
        pol = self.policy_for(handle, provider)
        old = self.exhausted.get(handle) or {}
        if old and failed_at <= old["at"]:
            return                                                                   # an older observation of the same exhaustion
        was_probe = bool(old.get("probe_claimed_at")) and failed_at > old["probe_claimed_at"]
        if was_probe:
            self.probes[handle] = {"at": failed_at, "result": "EXHAUSTED"}       # a failed probe
        self.exhausted[handle] = {"at": failed_at, "kind": "exhausted_credit", "reason": BILLING, "policy": pol, "next_probe_at": self.next_probe(handle, provider, failed_at),
                                  "probe_claimed_at": None, "last_probe": self.probes.get(handle)}

    def _recover(self, handle: str, at: float, how: str) -> None:
        if (self.exhausted.get(handle) or {}).get("probe_claimed_at"):
            self.probes[handle] = {"at": at, "result": how}
        del self.exhausted[handle]

    def release_stale_claims(self) -> None:
        """Called when a new episode starts: any claimed probe belongs to an episode that has ended. Without a verdict (never used) the probe is not spent."""
        for handle, ex in self.exhausted.items():
            if ex.get("probe_claimed_at"):
                ex["next_probe_at"], ex["probe_claimed_at"] = ex.get("claimed_next") or ex["probe_claimed_at"], None
                ex["last_probe"] = self.probes[handle] = {"at": time.time(), "result": "PROBE_UNUSED"}

    def claim_probes(self, now: float) -> set[str]:
        """Handles whose renewal cycle allows ONE availability probe now (claimed: not offered again in this cycle)."""
        due = set()
        for handle, ex in self.exhausted.items():
            nxt = ex.get("next_probe_at")
            if nxt is not None and now >= nxt and not ex.get("probe_claimed_at"):
                ex.update(probe_claimed_at=now, claimed_next=nxt, next_probe_at=None)
                due.add(handle)
        return due

    def is_exhausted(self, handle: str) -> bool:
        return handle in self.exhausted

    def seed_rows(self) -> list[dict]:
        rows = []
        for handle, s in self.sources.items():
            s = copy.deepcopy(s)
            h = s.setdefault("health", {})
            ex = self.exhausted.get(handle)
            if ex and ex.get("probe_claimed_at"):
                h.update(disabled_until=0, disabled_reason=None, status="PROBE")                 # the single availability probe of this renewal cycle
            elif ex:
                h.update(disabled_until=FOREVER, disabled_reason="exhausted", status="EXHAUSTED")
            elif h.get("disabled_reason") in ("billing", "exhausted"):       # renewed: drop the stale marker
                h.update(disabled_until=0, disabled_reason=None, status=None)
            h["failure_kinds"] = dict(self.kinds.get(handle, {}))
            rows.append(s)
        return rows

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(prefix=".credential_health.", dir=str(self.path.parent))
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"sources": self.sources, "exhausted": self.exhausted, "kinds": self.kinds, "seen": self.seen, "probes": self.probes}, f, sort_keys=True)
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
    reg.release_stale_claims()
    reg.claim_probes(time.time())
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


def latch_exhaustion(svc) -> None:
    """In-process half of EXHAUSTED: PlumMe sets a finite billing window; make it permanent the moment it is set (PlumMe itself is not modified)."""
    broker = svc.credentials
    original = broker.mark_failure

    def mark_failure(handle=None, provider=None, model=None, failure_class=None, retry_after=None):
        original(handle, provider, model, failure_class, retry_after)
        s = broker.sources.get(handle or "")
        if s is not None and failure_class == BILLING:
            s.health.update(disabled_until=FOREVER, disabled_reason="exhausted", status="EXHAUSTED")
            broker._save_sources()
    broker.mark_failure = mark_failure


def renew(runs: Path, handle: str) -> None:
    """Operator evidence that a credential has credit again (e.g. top-up): the next episode seeds it as usable."""
    f = Path(runs) / "credential_renewals.json"
    data = json.loads(f.read_text()) if f.exists() else {}
    data[handle] = time.time()
    f.write_text(json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4 and sys.argv[1] == "renew":
        renew(Path(sys.argv[2]), sys.argv[3])
    else:
        sys.exit("usage: ogi013_credential_health.py renew <runs_dir> <handle>")
