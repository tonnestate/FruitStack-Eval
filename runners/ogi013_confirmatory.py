#!/usr/bin/env python3
"""OGI-013 registered confirmatory analysis (PROTOCOL.md "Primary endpoint and inference"): exact two-sided McNemar on the discordant pairs of each exported condition pair,
paired risk difference with an exact Clopper-Pearson interval on the discordant proportion, Holm correction over the confirmatory family.

usage: ogi013_confirmatory.py --out result.json NAME=rows.jsonl [NAME=rows.jsonl ...]   (NAME e.g. H1, H1c, H2, H3, H4; rows from export_pair_rows.py, condition A -> role FIXED, B -> ADAPTIVE)
Outcome = official success (grade 1.0 with grade_status VERIFIED); anything else is a NON-success and is counted as `non_verified_as_nonsuccess`. A positive risk difference means condition A is better.
Only the pairs present in the rows are analysed; tasks missing from a pair (see mapping `unmatched`) are reported by the exporter and never silently dropped here.
Stdlib only. No network.
"""
import argparse
import json
import math
import sys


def _binom_cdf(k: int, n: int, p: float = 0.5) -> float:
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p: 2 * P(X <= min(b, c)), X ~ Bin(b + c, 0.5), capped at 1."""
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2.0 * _binom_cdf(min(b, c), n))


def clopper_pearson(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Exact two-sided (1 - alpha) interval for a binomial proportion, by bisection on the binomial tails (no scipy)."""
    if n == 0:
        return (0.0, 1.0)

    def solve(target, upper_tail):          # find p with P(X >= x | p) = target  (lower bound)  or  P(X <= x | p) = target  (upper bound)
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            val = (1 - _binom_cdf(x - 1, n, mid)) if upper_tail else _binom_cdf(x, n, mid)
            if upper_tail:
                lo, hi = (mid, hi) if val < target else (lo, mid)
            else:
                lo, hi = (lo, mid) if val < target else (mid, hi)
        return (lo + hi) / 2
    lower = 0.0 if x == 0 else solve(alpha / 2, True)
    upper = 1.0 if x == n else solve(alpha / 2, False)
    return (lower, upper)


def holm(pvalues: dict[str, float]) -> dict[str, float]:
    """Holm step-down adjusted p-values (monotone, capped at 1)."""
    order = sorted(pvalues, key=lambda k: pvalues[k])
    m, running, out = len(order), 0.0, {}
    for i, key in enumerate(order):
        running = max(running, min(1.0, (m - i) * pvalues[key]))
        out[key] = running
    return out


def analyse_pair(rows: list[dict]) -> dict:
    by_task: dict[str, dict[str, bool]] = {}
    non_verified = 0
    for r in rows:
        if r.get("pair_excluded"):
            continue
        success = r.get("grade") == 1.0 and r.get("grade_status") == "VERIFIED"
        if not success and r.get("grade_status") != "VERIFIED":
            non_verified += 1
        by_task.setdefault(str(r["task_id"]), {})[r["arm"]] = success
    pairs = {t: a for t, a in by_task.items() if "FIXED" in a and "ADAPTIVE" in a}
    b = sum(1 for a in pairs.values() if a["FIXED"] and not a["ADAPTIVE"])          # A (role FIXED) succeeded, B failed
    c = sum(1 for a in pairs.values() if a["ADAPTIVE"] and not a["FIXED"])
    both = sum(1 for a in pairs.values() if a["FIXED"] and a["ADAPTIVE"])
    n = len(pairs)
    lo, hi = clopper_pearson(b, b + c)
    d = b + c
    scale = d / n if n else 0.0
    return {"pairs": n, "both_success": both, "a_only": b, "b_only": c, "neither": n - both - b - c, "discordant": d,
            "p_exact_mcnemar": mcnemar_exact(b, c), "risk_difference": (b - c) / n if n else None,
            "risk_difference_ci95_exact": [scale * (2 * lo - 1), scale * (2 * hi - 1)] if d else [None, None],
            "non_verified_as_nonsuccess": non_verified}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("pairs", nargs="+", help="NAME=rows.jsonl")
    args = ap.parse_args()
    results = {}
    for spec in args.pairs:
        name, _, path = spec.partition("=")
        with open(path, encoding="utf-8") as fh:
            results[name] = analyse_pair([json.loads(line) for line in fh if line.strip()])
    adj = holm({k: v["p_exact_mcnemar"] for k, v in results.items()})
    for k in results:
        results[k]["p_holm"] = adj[k]
        results[k]["significant_alpha_0_05_after_holm"] = adj[k] < 0.05
    out = {"protocol": "OGI-013 PROTOCOL.md, primary endpoint and inference", "alpha": 0.05, "family": sorted(results), "results": results,
           "note": "A non-significant result is a null result at this n, not evidence of equivalence. No causal claim is made from a significance test alone."}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({k: {"pairs": v["pairs"], "a_only": v["a_only"], "b_only": v["b_only"], "p": round(v["p_exact_mcnemar"], 6), "p_holm": round(v["p_holm"], 6)} for k, v in results.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
