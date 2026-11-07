"""Offline analysis on the recorded QA-2D v2 T rows (no model call). Descriptive; selected sample (OK rows only). usage: python3 audit_analysis.py  (needs the repo runners on PYTHONPATH)"""
import json
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runners"))
from fs_codemode.evc import evaluate, normalize  # noqa: E402
from fs_codemode.shapley import ASSUMPTION, shapley  # noqa: E402


def cp(k, n, a=0.05):
    def cdf(x, p):
        return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, x + 1))
    lo, hi = 0.0, 1.0
    if k > 0:
        l, h = 0.0, k / n
        for _ in range(80):
            m = (l + h) / 2
            h, l = (m, l) if 1 - cdf(k - 1, m) > a / 2 else (h, m)
        lo = h
    if k < n:
        l, h = k / n, 1.0
        for _ in range(80):
            m = (l + h) / 2
            l, h = (m, h) if cdf(k, m) > a / 2 else (l, m)
        hi = l
    return round(lo, 4), round(hi, 4)


rows = [json.loads(l) for l in (ROOT / "evidence/ogi013-qa2d-v2-closure/inputs/results.jsonl").read_text().splitlines()]
t_ok = [r for r in rows if r["arm"] == "T" and r["status"] == "OK" and not r.get("reused_from")]
norm = [normalize(r) for r in t_ok]
n = len(norm)
acc = {name: sum(1 for r in norm if r[f] == r["key"]) for name, f in (("luna_first", "luna"), ("nemotron_first", "nemo"), ("team_final", "final"))}
out = {"label": "descriptive; selected sample (the 40 OK T rows of 53 questions; infrastructure-failed rows excluded)", "n": n,
       "correct": {k: {"k": v, "n": n, "ci95": cp(v, n)} for k, v in acc.items()}}
dis = [r for r in norm if r["luna"] != r["nemo"]]
out["disagreement_rows"] = {"n": len(dis), "qids": [r["qid"] for r in dis], "luna_first_correct": sum(1 for r in dis if r["luna"] == r["key"]),
                            "nemo_first_correct": sum(1 for r in dis if r["nemo"] == r["key"]), "team_final_correct": sum(1 for r in dis if r["final"] == r["key"])}


def game(ref):
    """duo_game with the no-critique coalition {luna, nemo} valued by ref ('luna' = the QA-2D rule, 'nemo' = the alternative)."""
    a = lambda f: sum(1 for r in norm if r[f] == r["key"]) / n  # noqa: E731
    v = {frozenset(): 0.0, frozenset({"luna"}): a("luna"), frozenset({"nemo"}): a("nemo"), frozenset({"link"}): 0.0, frozenset({"luna", "nemo"}): a(ref), frozenset({"luna", "nemo", "link"}): a("final")}
    v[frozenset({"luna", "link"})], v[frozenset({"nemo", "link"})] = v[frozenset({"luna"})], v[frozenset({"nemo"})]
    phi = shapley(("luna", "nemo", "link"), lambda s: v[frozenset(s)])
    return {"shapley_points": {k: round(100 * x, 2) for k, x in phi.items()}, "coalition_values_points": {",".join(sorted(k)) or "{}": round(100 * x, 2) for k, x in v.items()}}


from fs_codemode.shapley import duo_game  # noqa: E402
ref_luna, ref_nemo = game("luna"), game("nemo")
assert ref_luna["shapley_points"] == duo_game(norm)["shapley"], "own recomputation must equal duo_game with Luna as the reference"
out["shapley"] = {"assumption": ASSUMPTION, "reference_luna (duo_game as shipped)": ref_luna, "reference_nemotron (alternative)": ref_nemo,
                  "note": "the contribution of the link depends on this stated assumption: it is the difference between the final accuracy and the chosen no-critique reference, split by symmetry"}
ev = evaluate(t_ok)
out["evc_replay"] = {"recorded_disagreement_rows": len(dis), "n_fit": ev["n_fit"], "n_eval": ev["n_eval"], "fit_disagreements": ev["fit_disagreements"],
                     "statement": "EVC is not calibrated or evaluated on these rows: the fit half has too few disagreement rows (the table needs min_n per cell). No policy comparison is reported."}
(Path(__file__).parent / "audit_analysis.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
