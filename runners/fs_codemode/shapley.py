"""Exact Shapley values for a small player set (post-hoc attribution only; never used to decide truth).

Duo game on recorded T rows, players {luna, nemo, link} (link = the critique exchange):
  v({})        = 0
  v({luna})    = accuracy of Luna's first answers          v({nemo}) = accuracy of nemotron's first answers
  v({link})    = 0                                           (a critique link without members produces nothing)
  v({m, link}) = v({m})                                      ASSUMPTION: a link with one member is inert (no partner to criticise)
  v({luna, nemo}) = accuracy of the no-critique rule (agreement -> that answer; disagreement -> Luna's answer)
  v(all)       = accuracy of the recorded duo final
The assumption is reported with every result."""
from __future__ import annotations

from itertools import combinations
from math import factorial
from typing import Callable, Dict, FrozenSet, Iterable, Sequence

ASSUMPTION = "a critique link with a single member is inert: v({m, link}) = v({m})"


def shapley(players: Sequence[str], v: Callable[[FrozenSet[str]], float]) -> Dict[str, float]:
    n = len(players)
    out = {}
    for p in players:
        others = [q for q in players if q != p]
        total = 0.0
        for k in range(len(others) + 1):
            w = factorial(k) * factorial(n - k - 1) / factorial(n)
            for s in combinations(others, k):
                s = frozenset(s)
                total += w * (v(s | {p}) - v(s))
        out[p] = total
    return out


def duo_game(rows: Iterable[dict]) -> Dict[str, object]:
    """rows: normalized EVC rows (evc.normalize). Returns Shapley values (accuracy points) and the coalition values."""
    rows = list(rows)
    n = len(rows) or 1
    acc = lambda f: sum(1 for r in rows if f(r) is not None and f(r) == r["key"]) / n  # noqa: E731
    vals = {
        frozenset(): 0.0,
        frozenset({"luna"}): acc(lambda r: r["luna"]),
        frozenset({"nemo"}): acc(lambda r: r["nemo"]),
        frozenset({"link"}): 0.0,
        frozenset({"luna", "nemo"}): acc(lambda r: r["luna"]),
        frozenset({"luna", "nemo", "link"}): acc(lambda r: r["final"]),
    }
    vals[frozenset({"luna", "link"})] = vals[frozenset({"luna"})]
    vals[frozenset({"nemo", "link"})] = vals[frozenset({"nemo"})]
    phi = shapley(("luna", "nemo", "link"), lambda s: vals[frozenset(s)])
    return {"shapley": {k: round(100 * v, 2) for k, v in phi.items()}, "coalitions": {",".join(sorted(k)) or "{}": round(100 * v, 2) for k, v in vals.items()},
            "assumption": ASSUMPTION, "n": len(rows)}
