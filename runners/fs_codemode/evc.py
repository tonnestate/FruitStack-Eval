"""Expected Value of Computation for the duo's activation decision.

  EVC(a | S) = E[dU | a, S] - lambda_T * E[dT] - lambda_C * E[dC]        (lambda_R = 0: harm, right -> wrong, is already inside E[dU])

U = 1 per correct final answer. Actions at a disagreement: CRITIQUE (one cross-critique exchange) or FINISH (current rule: Luna's answer when no
objection exists). Probabilities and costs are estimated ONLY from recorded runs (counting tables with Laplace smoothing and back-off), never set by hand.
Fitting and evaluation use disjoint halves (hash split of the question id). Weights are not chosen here: `pareto()` reports every point of a fixed grid
and the owner picks the operating point. Until per-exchange records exist, later exchanges keep the baseline decision (CRITIQUE)."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from math import comb
from typing import Dict, Iterable, List, Optional, Tuple

LAMBDA_C = (0.0, 0.001, 0.003, 0.01)     # utility per 1,000 tokens
LAMBDA_T = (0.0, 0.0005, 0.002)          # utility per second
CRITIQUE, FINISH = "CRITIQUE", "FINISH"


def split_half(qid: str, salt: str = "QA2D-EVC") -> int:
    return int(hashlib.sha256(f"{salt}|{qid}".encode()).hexdigest(), 16) % 2


def normalize(row: dict) -> Optional[dict]:
    """A QA-2D T row (or a duo() result plus key) -> the fields EVC needs; None for rows without a usable answer pair (infra)."""
    first = row.get("first_by_member") or {}
    if not first and row.get("first_by_pos"):
        fb = row["first_by_pos"]
        first = {"luna": fb.get("S1"), "nemo": fb.get("S2")}
    if not first or row.get("key") is None or row.get("status") not in (None, "OK", "ok"):
        return None
    calls = max(int(row.get("calls") or 2), 2)
    tokens, seconds = float(row.get("tokens") or 0), float(row.get("seconds") or 0)
    ph_t, ph_s = row.get("phase_tokens") or {}, row.get("phase_seconds") or {}
    first_tokens = float(ph_t["first"]) if "first" in ph_t else tokens * 2.0 / calls
    first_seconds = float(ph_s["first"]) if "first" in ph_s else seconds * 2.0 / calls
    return {"qid": str(row.get("qid") or row.get("id")), "category": row.get("category") or "all", "key": row["key"],
            "luna": first.get("luna"), "nemo": first.get("nemo"), "final": row.get("letter"),
            "tokens": tokens, "seconds": seconds, "first_tokens": first_tokens, "first_seconds": first_seconds}


@dataclass
class Stats:
    n: int = 0
    finish_correct: int = 0
    critique_correct: int = 0
    extra_tokens: float = 0.0
    extra_seconds: float = 0.0

    def p_finish(self) -> float:
        return (self.finish_correct + 1) / (self.n + 2)

    def p_critique(self) -> float:
        return (self.critique_correct + 1) / (self.n + 2)

    def d_tokens(self) -> float:
        return self.extra_tokens / self.n if self.n else 0.0

    def d_seconds(self) -> float:
        return self.extra_seconds / self.n if self.n else 0.0


class EVCTable:
    def __init__(self, min_n: int = 5):
        self.min_n = min_n
        self.by_cat: Dict[str, Stats] = {}
        self.all = Stats()

    @classmethod
    def fit(cls, rows: Iterable[dict], min_n: int = 5) -> "EVCTable":
        t = cls(min_n)
        for r in rows:
            if r["luna"] == r["nemo"] and r["luna"]:
                continue                                    # only disagreements are decision points
            for s in (t.by_cat.setdefault(r["category"], Stats()), t.all):
                s.n += 1
                s.finish_correct += int(r["luna"] == r["key"])
                s.critique_correct += int(r["final"] == r["key"])
                s.extra_tokens += max(0.0, r["tokens"] - r["first_tokens"])
                s.extra_seconds += max(0.0, r["seconds"] - r["first_seconds"])
        return t

    def stats(self, category: str) -> Stats:
        s = self.by_cat.get(category)
        return s if s is not None and s.n >= self.min_n else self.all

    def evc(self, category: str, lam_c: float, lam_t: float) -> float:
        s = self.stats(category)
        return (s.p_critique() - s.p_finish()) - lam_c * s.d_tokens() / 1000.0 - lam_t * s.d_seconds()


class AlwaysCritique:
    name = "baseline_always_critique"

    def decide(self, state: dict) -> str:
        return CRITIQUE


class NeverCritique:
    name = "never_critique"

    def decide(self, state: dict) -> str:
        return FINISH


class EVCPolicy:
    def __init__(self, table: EVCTable, lam_c: float, lam_t: float):
        self.table, self.lam_c, self.lam_t = table, lam_c, lam_t
        self.name = f"evc_c{lam_c}_t{lam_t}"

    def decide(self, state: dict) -> str:
        if state.get("exchange", 0) >= 1:
            return CRITIQUE                                   # no per-exchange data yet: keep the validated rule
        return CRITIQUE if self.table.evc(state.get("category") or "all", self.lam_c, self.lam_t) > 0 else FINISH


def replay(rows: Iterable[dict], policy) -> dict:
    """Score a policy on recorded rows without model calls. Agreement: the agreed letter at first-answer cost. Disagreement: CRITIQUE -> the recorded
    final at the recorded cost; FINISH -> Luna's first letter at first-answer cost."""
    out = []
    for r in rows:
        if r["luna"] and r["luna"] == r["nemo"]:
            letter, tok, sec, act = r["luna"], r["first_tokens"], r["first_seconds"], "AGREED"
        else:
            act = policy.decide({"exchange": 0, "category": r["category"]})
            if act == CRITIQUE:
                letter, tok, sec = r["final"], r["tokens"], r["seconds"]
            else:
                letter, tok, sec = r["luna"], r["first_tokens"], r["first_seconds"]
        out.append({"qid": r["qid"], "action": act, "correct": letter is not None and letter == r["key"], "tokens": tok, "seconds": sec})
    n = len(out)
    return {"policy": getattr(policy, "name", str(policy)), "n": n, "correct": sum(o["correct"] for o in out),
            "accuracy": (sum(o["correct"] for o in out) / n) if n else 0.0, "tokens": sum(o["tokens"] for o in out),
            "seconds": round(sum(o["seconds"] for o in out), 1), "critiques": sum(o["action"] == CRITIQUE for o in out), "rows": out}


def mcnemar_exact(a_only: int, b_only: int) -> float:
    n = a_only + b_only
    if n == 0:
        return 1.0
    k = min(a_only, b_only)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def paired(policy_res: dict, base_res: dict) -> dict:
    a = {o["qid"]: o["correct"] for o in policy_res["rows"]}
    b = {o["qid"]: o["correct"] for o in base_res["rows"]}
    a_only = sum(1 for q in a if a[q] and not b.get(q))
    b_only = sum(1 for q in a if b.get(q) and not a[q])
    n = len(a)
    return {"diff_points": round(100.0 * (a_only - b_only) / n, 2) if n else 0.0, "policy_only": a_only, "baseline_only": b_only,
            "p_mcnemar": mcnemar_exact(a_only, b_only)}


def evaluate(rows: Iterable[dict], min_n: int = 5) -> dict:
    """Fit on half 0, evaluate on half 1; every grid point plus the baseline and never-critique. Non-dominated points are marked."""
    norm = [r for r in (normalize(x) for x in rows) if r]
    fit_rows = [r for r in norm if split_half(r["qid"]) == 0]
    eval_rows = [r for r in norm if split_half(r["qid"]) == 1]
    table = EVCTable.fit(fit_rows, min_n)
    base = replay(eval_rows, AlwaysCritique())
    points = [base, replay(eval_rows, NeverCritique())]
    for lc in LAMBDA_C:
        for lt in LAMBDA_T:
            points.append(replay(eval_rows, EVCPolicy(table, lc, lt)))
    for p in points:
        p["vs_baseline"] = paired(p, base)
    for p in points:
        p["pareto"] = not any(q is not p and q["accuracy"] >= p["accuracy"] and q["tokens"] <= p["tokens"] and q["seconds"] <= p["seconds"]
                              and (q["accuracy"] > p["accuracy"] or q["tokens"] < p["tokens"] or q["seconds"] < p["seconds"]) for q in points)
    return {"n_fit": len(fit_rows), "n_eval": len(eval_rows), "fit_disagreements": table.all.n,
            "points": [{k: v for k, v in p.items() if k != "rows"} for p in points]}
