"""Host-side typed execution facade (Code Mode level D1).

All model work goes through one injected `call(member, prompt) -> {"success", "output", "tokens"?, "failure_class"?}` (in production: luna_step / nemo_step,
which charge PlumMe's RunBudget and PeachMe's governance). The facade adds no retries. Every operation is written to `provenance` (outside any model
context) and, if given, to `on_event` (MangoMe ledger). A `budget_ok()` check runs before every model call; False stops the facade."""
from __future__ import annotations

import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .contract import Resources, sha


class BudgetStop(RuntimeError):
    pass


class Facade:
    def __init__(self, call: Callable[[str, str], dict], *, verifier: Optional[Callable[[str], dict]] = None,
                 on_event: Optional[Callable[[dict], None]] = None, budget_ok: Optional[Callable[[], bool]] = None,
                 max_parallel: int = 2, clock: Callable[[], float] = time.monotonic):
        self._call, self._verifier, self._on_event, self._budget_ok = call, verifier, on_event, budget_ok
        self.max_parallel, self.clock = max(1, int(max_parallel)), clock
        self.provenance: List[dict] = []
        self.totals = Resources()
        self._lock = threading.Lock()

    # -- recording --------------------------------------------------------------------------------------------------------------------------------
    def _record(self, op: str, **data) -> dict:
        ev = {"op": op, "seq": None, **data}
        with self._lock:
            ev["seq"] = len(self.provenance) + 1
            self.provenance.append(ev)
        if self._on_event is not None:
            self._on_event(ev)
        return ev

    # -- model calls --------------------------------------------------------------------------------------------------------------------------------
    def call(self, member: str, prompt: str, tag: str = "") -> dict:
        if self._budget_ok is not None and not self._budget_ok():
            self._record("budget_stop", member=member, tag=tag)
            raise BudgetStop(f"budget refused a call for {member} ({tag})")
        t0 = self.clock()
        d = self._call(member, prompt)
        dt = round(self.clock() - t0, 3)
        tokens = int(d.get("tokens") or 0)
        with self._lock:
            self.totals = self.totals.add(Resources(1, tokens, dt))
        self._record("call", member=member, tag=tag, prompt_sha=sha(prompt), prompt_chars=len(prompt or ""), output_sha=sha(d.get("output")),
                     success=bool(d.get("success")), failure_class=d.get("failure_class"), tokens=tokens, seconds=dt)
        return d

    def parallel(self, jobs: Sequence[Tuple[str, str, str]]) -> List[dict]:
        """Independent calls [(member, prompt, tag)] at the same time (bounded by max_parallel); results in input order."""
        if not jobs:
            return []
        with ThreadPoolExecutor(min(self.max_parallel, len(jobs))) as tp:
            futs = [tp.submit(self.call, m, p, t) for m, p, t in jobs]
            return [f.result() for f in futs]

    def chain(self, steps: Sequence[Callable[[object], object]], seed: object = None, stop: Optional[Callable[[object], bool]] = None) -> object:
        """Dependent steps in a fixed order; each step gets the previous result. `stop(result)` ends the chain early (recorded)."""
        value = seed
        for i, step in enumerate(steps):
            value = step(value)
            self._record("chain_step", index=i, name=getattr(step, "__name__", str(i)))
            if stop is not None and stop(value):
                self._record("chain_stop", index=i)
                break
        return value

    # -- deterministic operations (no model) ---------------------------------------------------------------------------------------------------
    def compare(self, letters: Dict[str, Optional[str]]) -> dict:
        valid = {m: l for m, l in letters.items() if l}
        counts = Counter(valid.values())
        agree = len(valid) == len(letters) and len(counts) == 1
        res = {"agree": agree, "letters": dict(letters), "counts": dict(counts), "conflict": [] if agree else sorted(letters)}
        self._record("compare", **{k: v for k, v in res.items() if k != "letters"}, letters=dict(letters))
        return res

    def verify(self, text: str) -> dict:
        """Deterministic evidence check through the injected verifier (production: ogi013_argument.classify_argument, bubblewrap sandbox).
        Without a verifier nothing is executed and the result is 'none' (fail closed)."""
        if self._verifier is None:
            res = {"kind": "suggestion", "argument": {"reason": "no verifier", "executed": False}}
        else:
            res = self._verifier(text)
        self._record("verify", text_sha=sha(text), kind=res.get("kind"), executed=bool((res.get("argument") or {}).get("executed")))
        return res

    def conflicts(self, letters: Dict[str, Optional[str]], objections: Sequence[dict]) -> List[dict]:
        """The conflicts that still need CherryMe: members disagree, and no verified objection already settles the point. An objection settles it only
        if it is verified AND no verified objection exists against the answer it supports (no automatic decision on contested verified evidence)."""
        cmp = self.compare(letters)
        if cmp["agree"]:
            return []
        verified = [o for o in objections if o.get("level") == "verified"]
        open_points = []
        for m in sorted(letters):
            against = [o for o in verified if o.get("target") == m]
            open_points.append({"member": m, "letter": letters[m], "verified_against": len(against)})
        self._record("conflicts", points=open_points)
        return open_points
