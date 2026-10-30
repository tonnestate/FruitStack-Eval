"""Repair order 1, R8: stable team roster. Each role (solver1, solver2, critic, specialist) is pinned to ONE model for the whole episode, chosen by PlumMe AUTO at its first use.
A pinned model is replaced only after a declared failure (FAILED_STEPS_BEFORE_CHANGE consecutive failed steps); every replacement is a ROSTER_CHANGE event with reason, written to MangoMe.
Hard check: at most MAX_MODELS distinct models per episode unless ROSTER_CHANGE events explain the excess."""
from __future__ import annotations

MAX_MODELS = 5
FAILED_STEPS_BEFORE_CHANGE = 2
STICKY_ALL = 99                      # every retry of a step stays on the pinned model (Episode.step: prefer applies while attempt < sticky_attempts)


class Roster:
    def __init__(self, emit=None, write=None):
        self.pins: dict = {}                     # role -> {"model_key", "lineage"}
        self.changes: list = []
        self.models_seen: set = set()
        self.emit, self.write = emit or (lambda *a, **k: None), write or (lambda *a, **k: None)

    def pinned(self, role: str):
        p = self.pins.get(role)
        return p["model_key"] if p else None

    def lineage(self, role: str):
        p = self.pins.get(role)
        return p["lineage"] if p else None

    def lineages(self, except_role=None) -> tuple:
        return tuple(sorted({v["lineage"] for r, v in self.pins.items() if r != except_role and v["lineage"]}))

    def pin(self, role: str, model_key: str, lineage) -> None:
        if role in self.pins:
            return
        self.pins[role] = {"model_key": model_key, "lineage": lineage}
        self.models_seen.add(model_key)
        self.emit("ROSTER_PIN", role=role, model=model_key, lineage=lineage)
        self.write("ROSTER_PIN", role, {"role": role, "model": model_key, "lineage": lineage})

    def change(self, role: str, reason: str) -> None:
        old = self.pins.pop(role, None)
        row = {"role": role, "from_model": old["model_key"] if old else None, "reason": reason, "n": len(self.changes) + 1}
        self.changes.append(row)
        self.emit("ROSTER_CHANGE", **row)
        self.write("ROSTER_CHANGE", f"{role}:{row['n']}", row)

    def note_model(self, model_key: str) -> None:
        self.models_seen.add(model_key)

    def check(self) -> dict:
        """ok iff <= MAX_MODELS distinct models, or every model beyond MAX_MODELS is explained by a ROSTER_CHANGE (distinct models <= MAX_MODELS + number of changes)."""
        n = len(self.models_seen)
        return {"distinct_models": n, "roster_changes": len(self.changes), "ok": n <= MAX_MODELS + len(self.changes), "limit": MAX_MODELS}

    def summary(self) -> dict:
        return {"roster": {r: v["model_key"] for r, v in self.pins.items()}, "changes": self.changes, "check": self.check()}


def next_solver_role(roster: Roster, positions_with_diff: dict) -> str:
    """The solver slot a new solve session fills: solver1, then solver2; if both exist, the slot whose position produced no accepted diff."""
    for slot in ("solver1", "solver2"):
        if slot not in roster.pins:
            return slot
    for slot in ("solver1", "solver2"):
        if not positions_with_diff.get(slot):
            return slot
    return "solver1"
