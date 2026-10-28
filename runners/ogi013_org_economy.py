"""OGI-013 economy mode (opt-in, OGI013_ORG_ECONOMY=1; default OFF, so the frozen experimental conditions are unchanged).

Why: measured on the archived airline:2 trace, 64 of 79 provider dispatches were organisational overhead that influenced no decision (every one of 13 decisions was escalated, 15 atomic
claims re-asked the same values, 74 failed worker attempts were retried against known supply failures). The correction keeps the full eligible model pool and only decides WHEN cooperation is bought:

 * a task starts with ONE model (the agent's draft); the organisation is recruited only for a stated purpose:
     consequential_effect  - a WRITE or TRANSFER action (cooperation is justified by what the action can change)
     draft_uncertainty     - the draft needed a format retry (observed uncertainty)
     observed_uncertainty  - an earlier dissent / verified contradiction in this episode (alert)
   plain reads and messages without any of these are not escalated ("simple_task");
 * delegation stops when it produces nothing new: after UNPRODUCTIVE_LIMIT consecutive uncertainty-triggered escalations without a decision-relevant contribution (dissent, verified
   contradiction/confirmation, changed action) further uncertainty escalations are skipped until a new signal ("no_new_information"); consequential actions are never skipped by this rule;
 * retry amplification stops once a failure is known: after SUPPLY_FAIL_LIMIT consecutive escalations in which no worker delivered anything, non-consequential escalations and atomic
   verification are skipped ("known_supply_failure"); every escalation runs under an ACTUAL-dispatch allowance (engine.run call_budget: workers, verifiers, reselections), a resource-safety
   control, not an output-token cap;
 * the same value is never re-verified within an episode ("duplicate_evidence_request").
Every decision records its purpose (or the reason it was skipped) and its measured yield, so the marginal cost per contribution is computable from the trace.
"""
from __future__ import annotations

import os

CONSEQUENTIAL = ("WRITE", "TRANSFER")
DEFAULTS = {"unproductive_limit": 2, "supply_fail_limit": 2, "primary_calls": 6, "atom_calls": 4}


class EconomyGate:
    def __init__(self, **overrides):
        cfg = {**DEFAULTS, **{k: int(v) for k, v in overrides.items()}}
        self.unproductive_limit, self.supply_fail_limit = cfg["unproductive_limit"], cfg["supply_fail_limit"]
        self.primary_calls, self.atom_calls = cfg["primary_calls"], cfg["atom_calls"]
        self.unproductive_streak = 0
        self.supply_fail_streak = 0
        self.asked_values: set[str] = set()
        self.skipped: dict[str, int] = {}
        self.escalations = self.productive = self.dispatches = 0

    @classmethod
    def from_env(cls):
        if os.environ.get("OGI013_ORG_ECONOMY") != "1":
            return None
        return cls(**{k: os.environ[f"OGI013_ORG_{k.upper()}"] for k in DEFAULTS if f"OGI013_ORG_{k.upper()}" in os.environ})

    def should_escalate(self, *, kind: str, alert: int = 0, prior_dissents: int = 0, uncertain: bool = False) -> tuple[bool, str]:
        if kind in CONSEQUENTIAL:
            return True, "consequential_effect"
        if self.supply_fail_streak >= self.supply_fail_limit:
            return self._skip("known_supply_failure")
        if self.unproductive_streak >= self.unproductive_limit:
            return self._skip("no_new_information")
        if uncertain:
            return True, "draft_uncertainty"
        if alert > 0 or prior_dissents > 0:
            return True, "observed_uncertainty"
        return self._skip("simple_task")

    def _skip(self, reason: str) -> tuple[bool, str]:
        self.skipped[reason] = self.skipped.get(reason, 0) + 1
        return False, reason

    def plan_atoms(self, atoms: list[dict], *, kind: str, alert: int = 0) -> list[dict]:
        """Atomic provenance claims are bought only for consequential actions or under an alert, only for values not yet asked in this episode, and not while supply is known to fail."""
        if not atoms or not (kind in CONSEQUENTIAL or alert > 0):
            return []
        if self.supply_fail_streak >= self.supply_fail_limit:
            self.skipped["known_supply_failure"] = self.skipped.get("known_supply_failure", 0) + len(atoms)
            return []
        fresh = []
        for atom in atoms:
            if atom["value"] in self.asked_values:
                self.skipped["duplicate_evidence_request"] = self.skipped.get("duplicate_evidence_request", 0) + 1
                continue
            self.asked_values.add(atom["value"])
            fresh.append(atom)
        return fresh

    def note_outcome(self, rec: dict, reason: str) -> bool:
        """Record the yield of one escalation. Productive = a decision-relevant contribution: worker dissent, a verified contradiction/confirmation, or a REFUTED/CONFLICT status."""
        productive = bool(rec.get("dissent")) or rec.get("status") in ("REFUTED", "CONFLICT") or any(
            a.get("status") in ("SUPPORTED", "REFUTED", "CONFLICT") for a in rec.get("atoms", []))
        self.escalations += 1
        self.productive += 1 if productive else 0
        self.dispatches += int(rec.get("dispatch_total") or 0)
        self.supply_fail_streak = 0 if rec.get("delivered") else self.supply_fail_streak + 1
        if reason != "consequential_effect":
            self.unproductive_streak = 0 if productive else self.unproductive_streak + 1
        elif productive:
            self.unproductive_streak = 0
        return productive

    def summary(self) -> dict:
        return {"escalations": self.escalations, "productive": self.productive, "skipped": dict(self.skipped), "dispatches": self.dispatches,
                "dispatches_per_productive": (self.dispatches / self.productive) if self.productive else None,
                "unproductive_streak": self.unproductive_streak, "supply_fail_streak": self.supply_fail_streak}
