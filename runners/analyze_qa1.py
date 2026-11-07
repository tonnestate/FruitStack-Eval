#!/usr/bin/env python3
"""QA-1 analysis (pre-registered; sealed in QA1_LOCK.txt before the first study call). usage: analyze_qa1.py RESULTS.jsonl [--out report.md]
Pure python (no scipy). Row format (one per question x arm, final attempt): {"qid","arm","letter","correct","status","calls","tokens","seconds", ...T trace fields}.
Primary: an arm that failed on infrastructure after its one rerun counts as incorrect. Sensitivity: questions with an infrastructure failure in ANY arm are excluded from all arms.
Tests: exact McNemar on the discordant pairs, Holm over H1 (T-S), H1c (T-E), HL (T-L). Effect size: paired risk difference with the exact conditional CI given the number of discordant pairs."""
import json
import sys
from collections import Counter
from math import comb

ARMS = ("T", "E", "S", "L")
HYPOTHESES = (("H1", "S"), ("H1c", "E"), ("HL", "L"))
ALPHA = 0.05


def binom_cdf(k: int, n: int, p: float) -> float:
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def mcnemar_exact(b: int, c: int) -> float:
    m = b + c
    if m == 0:
        return 1.0
    return min(1.0, 2 * binom_cdf(min(b, c), m, 0.5))


def clopper_pearson(x: int, n: int, alpha: float = ALPHA) -> tuple:
    if n == 0:
        return (0.0, 1.0)

    def solve(f, lo=0.0, hi=1.0):
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if x == 0 else solve(lambda p: 1 - binom_cdf(x - 1, n, p) < alpha / 2)          # P(X >= x | p) rises with p
    upper = 1.0 if x == n else solve(lambda p: binom_cdf(x, n, p) > alpha / 2) if False else 1.0 - (0.0 if x == n else solve(lambda q: 1 - binom_cdf(n - x - 1, n, q) < alpha / 2))
    return (lower, upper)


def paired(t: list, o: list) -> dict:
    n = len(t)
    b = sum(1 for x, y in zip(t, o) if x and not y)
    c = sum(1 for x, y in zip(t, o) if y and not x)
    m = b + c
    lo, hi = clopper_pearson(b, m) if m else (0.5, 0.5)
    return {"n": n, "b_T_only": b, "c_other_only": c, "diff": (b - c) / n if n else 0.0, "ci_low": (m / n) * (2 * lo - 1) if m else 0.0, "ci_high": (m / n) * (2 * hi - 1) if m else 0.0, "p": mcnemar_exact(b, c)}


def holm(ps: list) -> list:
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


def table(rows: dict, qids: list) -> list:
    out = []
    for arm in ARMS:
        rs = [rows[(q, arm)] for q in qids if (q, arm) in rows]
        out.append({"arm": arm, "n": len(rs), "correct": sum(1 for r in rs if r["correct"]), "tokens": sum(r.get("tokens") or 0 for r in rs), "calls": sum(r.get("calls") or 0 for r in rs),
                    "seconds": round(sum(r.get("seconds") or 0 for r in rs), 1), "infra_failed": sum(1 for r in rs if r["status"] != "OK")})
    return out


def comparisons(rows: dict, qids: list) -> list:
    res = []
    for name, other in HYPOTHESES:
        pr = paired([bool(rows[(q, "T")]["correct"]) for q in qids], [bool(rows[(q, other)]["correct"]) for q in qids])
        res.append({"hypothesis": name, "pair": f"T vs {other}", **pr})
    for r, a in zip(res, holm([r["p"] for r in res])):
        r["p_holm"] = a
    return res


def t_trace(rows: dict, qids: list) -> dict:
    cats = Counter()
    tot = Counter()
    for q in qids:
        r = rows[(q, "T")]
        first = r.get("first_letters") or {}
        key = r.get("key")
        any_first_right = any(l == key for l in first.values() if l)
        if r["correct"] and not any_first_right:
            cats["wrong_to_right"] += 1
        elif not r["correct"] and any_first_right:
            cats["right_to_wrong"] += 1
        elif r["correct"]:
            cats["unchanged_right"] += 1
        else:
            cats["unchanged_wrong"] += 1
        for k in ("grounded_objections", "objections", "replies", "answer_changes", "mango_reads", "mango_writes"):
            tot[k] += int(r.get(k) or 0)
    return {"categories": dict(cats), "totals": dict(tot)}


def analyze(path: str) -> dict:
    raw = [json.loads(l) for l in open(path) if l.strip()]
    rows = {}
    for r in raw:                                                # the last attempt per (question, arm) is the final one
        rows[(r["qid"], r["arm"])] = r
    qids = sorted({q for q, _ in rows if all((q, a) in rows for a in ARMS)})
    clean = [q for q in qids if all(rows[(q, a)]["status"] == "OK" for a in ARMS)]
    return {"n_questions": len(qids), "primary": {"table": table(rows, qids), "comparisons": comparisons(rows, qids)},
            "sensitivity": {"n_questions": len(clean), "table": table(rows, clean), "comparisons": comparisons(rows, clean) if clean else []}, "t_trace": t_trace(rows, qids)}


def render(res: dict) -> str:
    out = [f"# QA-1 analysis ({res['n_questions']} questions)", "", "## Arm table (primary)", "| arm | correct | n | % | tokens | calls | wall s | infra failures |", "|---|---|---|---|---|---|---|---|"]
    for t in res["primary"]["table"]:
        out.append(f"| {t['arm']} | {t['correct']} | {t['n']} | {100 * t['correct'] / max(t['n'], 1):.1f} | {t['tokens']} | {t['calls']} | {t['seconds']} | {t['infra_failed']} |")
    for title, comp in (("Confirmatory (primary), Holm over 3", res["primary"]["comparisons"]), (f"Sensitivity (questions without infrastructure failure: {res['sensitivity']['n_questions']})", res["sensitivity"]["comparisons"])):
        out += ["", f"## {title}", "| hypothesis | pair | T-only | other-only | paired diff | 95% CI (exact, conditional) | p (exact McNemar) | p (Holm) |", "|---|---|---|---|---|---|---|---|"]
        for c in comp:
            out.append(f"| {c['hypothesis']} | {c['pair']} | {c['b_T_only']} | {c['c_other_only']} | {100 * c['diff']:+.1f} pts | [{100 * c['ci_low']:+.1f}, {100 * c['ci_high']:+.1f}] | {c['p']:.4f} | {c['p_holm']:.4f} |")
    out += ["", "## T trace (descriptive)", f"- categories: {res['t_trace']['categories']}", f"- totals: {res['t_trace']['totals']}"]
    return "\n".join(out)


if __name__ == "__main__":
    res = analyze(sys.argv[1])
    text = render(res)
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(text + "\n")
        open(sys.argv[sys.argv.index("--out") + 1] + ".json", "w").write(json.dumps(res, indent=1))
    print(text)
