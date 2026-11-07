"""OGI study analysis: exact paired tests, Holm, token control, harm, EVAL-003, power.

Input: JSONL, one row per (task, arm[, attempt]) with fields
  task_id, family, arm, correct (bool), member_first_correct (list[bool]|dict, team arm),
  tokens_in, tokens_out, calls, lineages (list), valid (bool; false = identity mismatch).
Arm roles are configurable; defaults: team "T", same-mix control "E", generic
multi-agent control "G", single members "S_*".

Statistics engine: scipy/statsmodels. PhysalisMe (448a3b1) exposes no library API for
these (only a private `_holm_adjust` over exploration rows, no McNemar/binomial/power,
MCP-only surface), so Holm is re-implemented here with identical semantics.
Run: python analysis/ogi_analyze.py rows.jsonl [--best-single S_x]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from functools import lru_cache

import numpy as np
from scipy.stats import beta, binomtest

ROLES = {"team": "T", "same_mix": "E", "generic": "G", "single_prefix": "S_",
         "mono": "R_mono", "gmas": "G_mas"}
# Arm names of the real study rows (runners/fs_org_driver.py); see ogi_rows_adapter.py.
STUDY_ROLES = {"team": "T", "same_mix": "E_div", "mono": "R_mono", "gmas": "G_mas"}
# One Holm family per task family holds every contrast below. PRIMARY (the single confirmatory
# hypothesis) is "primary:T_vs_E" = team vs E_div (same-mix diversity control); all others are secondary.
TOKEN_BAND = 0.10


# ---------- primitives ----------
def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    lo = 0.0 if k == 0 else beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha / 2, k + 1, n - k)
    return (float(lo), float(hi))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p from discordant counts (b = A-only right, c = B-only right)."""
    n = b + c
    return 1.0 if n == 0 else float(binomtest(min(b, c), n, 0.5).pvalue)


def holm(pvals: dict[str, float]) -> dict[str, float]:
    """Holm step-down adjusted p-values (same semantics as PhysalisMe._holm_adjust)."""
    out, largest, m = {}, 0.0, len(pvals)
    for rank, (k, p) in enumerate(sorted(pvals.items(), key=lambda kv: kv[1])):
        largest = max(largest, min(1.0, p * (m - rank)))
        out[k] = largest
    return out


# ---------- data ----------
def load_rows(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def split_valid(rows: list[dict]) -> tuple[list[dict], dict]:
    ok = [r for r in rows if r.get("valid", True)]
    bad = [r for r in rows if not r.get("valid", True)]
    by_arm: dict[str, int] = defaultdict(int)
    reasons: dict[str, int] = defaultdict(int)
    for r in bad:
        by_arm[r["arm"]] += 1
        reasons[r.get("exclusion") or "UNSPECIFIED"] += 1
    return ok, {"n_excluded": len(bad), "by_arm": dict(by_arm), "by_reason": dict(reasons),
                "task_ids": sorted({r["task_id"] for r in bad})}


def _tokens(r: dict) -> float:
    return float(r.get("tokens_in", 0) + r.get("tokens_out", 0))


def _index(rows: list[dict], family: str | None = None) -> dict[str, dict[str, dict]]:
    """arm -> task_id -> first row (solo arms may have repeats; see eval003)."""
    idx: dict[str, dict[str, dict]] = defaultdict(dict)
    for r in rows:
        if family is None or r.get("family") == family:
            idx[r["arm"]].setdefault(r["task_id"], r)
    return idx


def paired(idx: dict, a: str, b: str, band: float | None = None) -> dict:
    """Exact McNemar on tasks present (valid) in both arms. band: keep only pairs whose
    token totals are within +-band of each other (matched-token stratum)."""
    ta, tb = idx.get(a, {}), idx.get(b, {})
    both = sorted(set(ta) & set(tb))
    if band is not None:
        both = [t for t in both if _tokens(ta[t]) > 0 and _tokens(tb[t]) > 0
                and abs(_tokens(ta[t]) / _tokens(tb[t]) - 1) <= band]
    n11 = sum(ta[t]["correct"] and tb[t]["correct"] for t in both)
    b_ = sum(ta[t]["correct"] and not tb[t]["correct"] for t in both)
    c_ = sum(tb[t]["correct"] and not ta[t]["correct"] for t in both)
    n00 = len(both) - n11 - b_ - c_
    return {"a": a, "b": b, "n_pairs": len(both), "a_only": b_, "b_only": c_, "both": n11,
            "neither": n00, "acc_a": (n11 + b_) / len(both) if both else None,
            "acc_b": (n11 + c_) / len(both) if both else None,
            "p_exact": mcnemar_exact(b_, c_), "direction": "a" if b_ > c_ else "b" if c_ > b_ else "tie"}


# ---------- contrasts per family ----------
def contrasts(idx: dict, roles: dict, best_single: str | None, band: float | None = None) -> dict:
    T, E, G = roles["team"], roles["same_mix"], roles["generic"]
    R, M = roles["mono"], roles["gmas"]
    singles = sorted(a for a in idx if a.startswith(roles["single_prefix"]))
    tests: dict[str, dict] = {}
    if singles and best_single is None:  # post hoc: optimistic for the comparator, flagged below
        best_single = max(singles, key=lambda s: sum(r["correct"] for r in idx[s].values()) / max(1, len(idx[s])))
        posthoc = True
    else:
        posthoc = False
    if E in idx:
        tests["primary:T_vs_E"] = paired(idx, T, E, band)
    if G in idx and E in idx:
        tests["secondary:G_vs_E"] = paired(idx, G, E, band)
    if G in idx:
        tests["secondary:T_vs_G"] = paired(idx, T, G, band)
    if R in idx and E in idx:  # H3: does diversity beat repeated sampling at matched compute?
        tests["secondary:H3_E_vs_R_mono"] = paired(idx, E, R, band)
    if R in idx and singles:   # H3: does repeated sampling beat the best single member?
        tests["secondary:H3_R_mono_vs_best_single"] = {**paired(idx, R, best_single, band),
                                                      "best_single": best_single, "best_single_posthoc": posthoc}
    if M in idx and E in idx:
        tests["secondary:G_mas_vs_E"] = paired(idx, M, E, band)
    if M in idx:
        tests["secondary:T_vs_G_mas"] = paired(idx, T, M, band)
    if singles:
        tests["secondary:T_vs_best_single"] = {**paired(idx, T, best_single, band),
                                               "best_single": best_single, "best_single_posthoc": posthoc}
        # intersection-union: reject only if every T-vs-single test rejects in T's favour
        per = {s: paired(idx, T, s, band) for s in singles}
        tests["secondary:T_vs_every_single(IUT)"] = {
            "per_member": per,
            "p_iut": max(v["p_exact"] if v["direction"] == "a" else 1.0 for v in per.values())}
    return tests


def holm_family(tests: dict, alpha: float = 0.05) -> dict:
    p = {k: (v["p_iut"] if "p_iut" in v else v["p_exact"]) for k, v in tests.items()}
    adj = holm(p)
    for k, v in tests.items():
        v["p_raw"], v["p_holm"], v["reject"] = p[k], adj[k], adj[k] <= alpha
    return tests


def two_family_rule(results: dict[str, dict], alpha: float = 0.05) -> dict:
    """A hypothesis is confirmed only if rejected, in the same direction, in every family
    (requires >= 2 families)."""
    fams = sorted(results)
    out = {}
    names = set.intersection(*(set(results[f]) for f in fams)) if fams else set()
    for h in sorted(names):
        dirs = []
        for f in fams:
            t = results[f][h]
            d = t.get("direction") if "p_iut" not in t else ("a" if t["p_iut"] < 1 else "none")
            dirs.append(d if t["reject"] else None)
        out[h] = {"confirmed": len(fams) >= 2 and None not in dirs and len(set(dirs)) == 1,
                  "families": fams, "per_family_reject_direction": dirs}
    return out


# ---------- harm / correction ----------
def harm(rows: list[dict], team: str, alpha: float = 0.05) -> dict:
    n = k_cor = k_dam = held = lost = 0
    for r in rows:
        if r["arm"] != team or r.get("member_first_correct") is None:
            continue
        m = r["member_first_correct"]
        any_first = any(m.values() if isinstance(m, dict) else m)
        n += 1
        if r["correct"] and not any_first: k_cor += 1
        elif not r["correct"] and any_first: k_dam += 1
        elif r["correct"]: held += 1
        else: lost += 1
    d = k_cor + k_dam
    return {"n": n, "corrected": k_cor, "damaged": k_dam, "held": held, "lost_both": lost,
            "corrected_ci": clopper_pearson(k_cor, n, alpha), "damaged_ci": clopper_pearson(k_dam, n, alpha),
            "damage_share": k_dam / d if d else None,
            "damage_share_ci": clopper_pearson(k_dam, d, alpha) if d else None,
            "p_harm_lt_half": float(binomtest(k_dam, d, 0.5, alternative="less").pvalue) if d else None}


# ---------- tokens as covariate ----------
def token_summary(rows: list[dict]) -> dict:
    s: dict[str, dict] = defaultdict(lambda: {"rows": 0, "correct": 0, "tokens": 0.0, "calls": 0})
    for r in rows:
        a = s[r["arm"]]
        a["rows"] += 1; a["correct"] += bool(r["correct"]); a["tokens"] += _tokens(r); a["calls"] += r.get("calls", 0)
    return {k: {**v, "tokens_per_row": v["tokens"] / v["rows"],
                "tokens_per_correct": v["tokens"] / v["correct"] if v["correct"] else None} for k, v in s.items()}


def logistic_tokens(rows: list[dict], reference: str) -> dict:
    """correct ~ arm + z(log tokens), cluster-robust by task. Coefficients are log-odds vs `reference`."""
    import statsmodels.api as sm
    rows = [r for r in rows if _tokens(r) > 0]
    arms = sorted({r["arm"] for r in rows} - {reference})
    if not arms or len({r["correct"] for r in rows}) < 2:
        return {"error": "insufficient variation"}
    lt = np.log([_tokens(r) for r in rows]); lt = (lt - lt.mean()) / (lt.std() or 1.0)
    X = np.column_stack([np.ones(len(rows))] + [[float(r["arm"] == a) for r in rows] for a in arms] + [lt])
    y = np.array([float(r["correct"]) for r in rows])
    groups = np.unique([r["task_id"] for r in rows], return_inverse=True)[1]
    try:
        res = sm.Logit(y, X).fit(disp=0, cov_type="cluster", cov_kwds={"groups": groups})
    except Exception as e:  # separation / singular
        return {"error": f"{type(e).__name__}: {e}"}
    names = ["intercept"] + arms + ["log_tokens_z"]
    return {"reference": reference, "coef": {n: {"b": float(res.params[i]), "p": float(res.pvalues[i])}
                                              for i, n in enumerate(names)}}


# ---------- EVAL-003 ----------
def eval003(rows: list[dict], roles: dict, r_attempts: int = 3, family: str | None = None) -> dict:
    """U = tasks where every single member failed all >= r_attempts solo attempts."""
    solo = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["arm"].startswith(roles["single_prefix"]) and (family is None or r.get("family") == family):
            solo[r["task_id"]][r["arm"]].append(bool(r["correct"]))
    members = {r["arm"] for r in rows if r["arm"].startswith(roles["single_prefix"])}
    U = sorted(t for t, m in solo.items()
               if set(m) == members and all(len(v) >= r_attempts and not any(v) for v in m.values()))
    idx = _index(rows, family)
    res = {"n_U": len(U), "U_rate_of_solo_tasks": len(U) / len(solo) if solo else None}
    for arm_key in ("team", "same_mix", "generic"):
        a = roles[arm_key]; done = [t for t in U if t in idx.get(a, {})]
        k = sum(idx[a][t]["correct"] for t in done) if a in idx else 0
        res[arm_key] = {"n": len(done), "solved": k, "rate": k / len(done) if done else None,
                        "ci": clopper_pearson(k, len(done))}
    sub = {a: {t: v for t, v in idx.get(a, {}).items() if t in set(U)} for a in (roles["team"], roles["same_mix"], roles["generic"])}
    tests = {}
    for k in ("same_mix", "generic"):
        if sub[roles[k]]:
            tests[f"T_vs_{roles[k]}_on_U"] = paired(sub, roles["team"], roles[k])
    res["tests"] = holm_family(tests) if tests else {}
    return res


# ---------- power ----------
@lru_cache(maxsize=None)
def _crit(d: int, alpha: float) -> int:
    """Largest x with exact two-sided McNemar p(x, d-x) <= alpha, or -1."""
    c = -1
    while c + 1 <= d // 2 and mcnemar_exact(c + 1, d - c - 1) <= alpha:
        c += 1
    return c


def mcnemar_power(n: int, p_d: float, pi: float, alpha: float = 0.05) -> float:
    """Exact power: D ~ Bin(n, p_d) discordant pairs, each T-only w.p. pi; reject if exact p <= alpha."""
    from scipy.stats import binom
    pw = 0.0
    for d in range(1, n + 1):
        w = binom.pmf(d, n, p_d)
        if w < 1e-12:
            continue
        k = np.arange(d + 1)
        c = _crit(d, alpha)
        rej = (k <= c) | (k >= d - c)  # both tails
        pw += w * float(binom.pmf(k, d, pi)[rej].sum())
    return pw


def n_for_power(p_d: float, pi: float, power: float = 0.8, alpha: float = 0.05, n_max: int = 5000) -> int | None:
    """Smallest n whose exact power stays >= target for the next 10 sizes (exact power is sawtooth)."""
    ok = 0
    for n in range(10, n_max + 1):
        ok = ok + 1 if mcnemar_power(n, p_d, pi, alpha) >= power else 0
        if ok == 10:
            return n - 9
    return None


def power_from_pilot(b: int, c: int, n_pilot: int, power: float = 0.8, alpha: float = 0.05) -> dict:
    """b = team-only right, c = comparator-only right in a pilot of n_pilot paired tasks."""
    d = b + c
    if d == 0 or b <= c:
        return {"p_d": d / n_pilot, "pi": None, "n": None, "note": "no positive effect in pilot"}
    p_d, pi = d / n_pilot, b / d
    return {"p_d": p_d, "pi": pi, "n": n_for_power(p_d, pi, power, alpha)}


# ---------- driver ----------
def analyze(rows: list[dict], roles: dict | None = None, best_single: str | None = None,
            alpha: float = 0.05, r_attempts: int = 3) -> dict:
    roles = {**ROLES, **(roles or {})}
    rows, excluded = split_valid(rows)
    families = sorted({r["family"] for r in rows if r.get("family")})
    rep: dict = {"excluded_invalid": excluded, "families": {}}
    for f in families:
        idx = _index(rows, f)
        frows = [r for r in rows if r.get("family") == f]
        full = holm_family(contrasts(idx, roles, best_single), alpha)
        matched = holm_family(contrasts(idx, roles, best_single, TOKEN_BAND), alpha)
        rep["families"][f] = {"contrasts": full, "matched_token_10pct": matched,
                              "tokens": token_summary(frows), "logistic_tokens": logistic_tokens(frows, roles["same_mix"]),
                              "harm": harm(frows, roles["team"], alpha),
                              "eval003": eval003(rows, roles, r_attempts, f)}
    if len(families) >= 2:
        rep["two_family_rule"] = two_family_rule({f: v["contrasts"] for f, v in rep["families"].items()}, alpha)
    return rep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("rows"); ap.add_argument("--best-single"); ap.add_argument("--alpha", type=float, default=0.05)
    a = ap.parse_args()
    print(json.dumps(analyze(load_rows(a.rows), best_single=a.best_single, alpha=a.alpha), indent=1, default=str))
