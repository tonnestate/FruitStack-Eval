"""MangoMe as the work ledger of a team episode (final order C.2/C.3, AMENDMENT-MANGO-1).

Uses only the existing API `MangoWorkAdapter.checkpoint` -> `checkpoint_work` with an idempotency key per record.
  * granular records (audit trail): TEAM_GOAL, TEAM_POSITION (diff + sha256), TEAM_OBJECTION (every state change), TEAM_DECISION, TEAM_VOTE, TEAM_RELEASE;
  * after every persist one TEAM_STATE_FULL checkpoint holds the complete structured state, so `work_context(work_ref)["progressive"]["latest_checkpoint"]` alone
    rebuilds team_state.md byte-identically (work_context returns only the latest checkpoint).
Fail-closed (C.2): a failed write raises InfraMangoFailed (a BaseException so no `except Exception` in the driver can swallow it); the episode ends INFRA_MANGOME_FAILED, which is
infrastructure, never a result. The fail-soft `checkpoint_continuity` of the tau2 path is unchanged."""
from __future__ import annotations

import hashlib
import json
import threading


class InfraMangoFailed(BaseException):
    pass


def _digest(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


class MangoLedger:
    def __init__(self, adapter, work_ref: str, actor_id: str, turn_id: str, run_id: str):
        self.adapter, self.work_ref, self.actor_id, self.turn_id, self.run_id = adapter, work_ref, actor_id, turn_id, run_id
        self.seq = 0
        self.writes = 0
        self.lock = threading.RLock()                 # parallel organisation P3: writes are serialised and versioned (gap-free sequence numbers; the latest checkpoint is the latest state)

    def write(self, kind: str, key: str, payload: dict) -> None:
        with self.lock:
            self.seq += 1
            body = {**payload, "run_id": self.run_id, "key": key, "seq": self.seq}
            body["idempotency_key"] = f"{self.run_id}:{kind}:{key}:{_digest(payload)[:24]}"
            try:
                self.adapter.checkpoint(self.work_ref, self.actor_id, kind, body, turn_id=self.turn_id)
            except Exception as exc:  # noqa: BLE001 - a MangoMe write failure is infrastructure: fail closed
                raise InfraMangoFailed(f"{kind}/{key}: {type(exc).__name__}: {str(exc)[:300]}") from exc
            self.writes += 1

    def latest(self) -> dict | None:
        """The latest checkpoint payload of this work, read back through MangoMe's own work_context."""
        ctx = self.adapter.service.work_context(self.work_ref)
        cp = (ctx.get("progressive") or {}).get("latest_checkpoint") or {}
        return cp.get("payload")
