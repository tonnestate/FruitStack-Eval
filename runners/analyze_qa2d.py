"""QA-2D analysis (sealed in QA2D_LOCK.txt before the first study call). usage: analyze_qa2d.py RESULTS.jsonl [--out report.md]
Confirmatory (exact McNemar, Holm over 2, two-sided alpha 0.05): H1L T vs SL, H1c T vs E. Primary: an infrastructure failure counts as incorrect. Sensitivity: questions without any infra failure.
Descriptive: T vs SN, disagreement rate, chains with their three labels, HARMFUL changes, formal/verified counts, tokens and calls per arm, MangoMe reads/writes."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from analyze_qa1 import holm, paired
from ogi013_qa1 import chain_class, chain_labels, chain_stages

ARMS = ("T", "E", "SL", "SN")
CONFIRMATORY = (("H1L", "SL"), ("H1c", "E"))


def load(path) -> dict:
    return {(r["qid"], r["arm"]): r for r in (json.loads(l) for l in Path(path).read_text().splitlines() if l.strip())}


def complete_qids(rows: dict) -> list:
    qids = sorted({q for q, _a in rows})
    return [q for q in qids if all((q, a) in rows for a in ARMS)]


def compare(rows: dict, qids: list, other: str) -> dict:
    return paired([bool(rows[(q, "T")]["correct"]) for q in qids], [bool(rows[(q, other)]["correct"]) for q in qids])


def confirmatory(rows: dict, qids: list) -> list:
    res = [{"hypothesis": h, "pair": f"T vs {o}", **compare(rows, qids, o)} for h, o in CONFIRMATORY]
    for r, a in zip(res, holm([r["p"] for r in res])):
        r["p_holm"] = a
    return res


def pct(xs: list, p: float):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return round(xs[lo] + (xs[hi] - xs[lo]) * (k - lo), 2)


def arm_table(rows: dict, qids: list) -> list:
    out = []
    for a in ARMS:
        rs = [rows[(q, a)] for q in qids]
        ok = sum(bool(r["correct"]) for r in rs)
        tokens, calls, secs = (sum(r.get(k) or 0 for r in rs) for k in ("tokens", "calls", "seconds"))
        lat = [r.get("seconds") for r in rs if r["status"] == "OK"]
        out.append({"arm": a, "n": len(rs), "correct": ok, "infra_failures": sum(r["status"] != "OK" for r in rs), "tokens": tokens, "calls": calls, "reused": sum(1 for r in rs if r.get("reused_from")),
                    "latency_p50_s": pct(lat, 0.5), "latency_p95_s": pct(lat, 0.95), "tokens_per_success": (tokens / ok) if ok else None, "calls_per_success": (calls / ok) if ok else None,
                    "seconds_per_success": (secs / ok) if ok else None})
    return out


def t_descriptive(rows: dict, qids: list) -> dict:
    t = [rows[(q, "T")] for q in qids if rows[(q, "T")]["status"] == "OK"]
    dis = [r for r in t if r.get("stop") != "AGREED_FIRST"]
    chains = [r for r in dis if chain_stages(r)["complete"]]
    harmful = [r for r in dis if chain_class(r) == "HARMFUL"]
    lab = Counter(k for r in chains for k, v in chain_labels(r).items() if v)
    return {"t_ok": len(t), "disagreed_first": len(dis), "disagreement_rate": (len(dis) / len(t)) if t else None, "stops": dict(Counter(r.get("stop") for r in t)),
            "complete_chains": len(chains), "chain_labels": dict(lab), "chain_classes": dict(Counter(chain_class(r) for r in chains)), "classes_all_disagreements": dict(Counter(chain_class(r) for r in dis)),
            "harmful_changes": len(harmful), "formal_objections": sum(r.get("formal_objections") or 0 for r in t), "verified_objections": sum(r.get("verified_objections") or 0 for r in t),
            "formal_replies": sum(r.get("formal_replies") or 0 for r in t), "verified_replies": sum(r.get("verified_replies") or 0 for r in t), "accepted_concessions": sum(r.get("accepted_concessions") or 0 for r in t),
            "mango_reads": sum(r.get("mango_reads") or 0 for r in t), "mango_writes": sum(r.get("mango_writes") or 0 for r in t)}


def analyze(path) -> dict:
    rows = load(path)
    qids = complete_qids(rows)
    clean = [q for q in qids if all(rows[(q, a)]["status"] == "OK" for a in ARMS)]
    return {"n_questions": len(qids), "arms": arm_table(rows, qids), "confirmatory": confirmatory(rows, qids), "sensitivity_n": len(clean), "sensitivity": confirmatory(rows, clean) if clean else [],
            "descriptive_T_vs_SN": compare(rows, qids, "SN"), "trace": t_descriptive(rows, qids)}


def render(res: dict) -> str:
    L = [f"# QA-2D analysis ({res['n_questions']} questions)", "", "## Arm table (primary)", "| arm | correct | n | infra failures | tokens | calls | reused | latency P50/P95 s | tokens / calls / s per correct answer |", "|---|---|---|---|---|---|---|---|---|"]
    f = lambda v: "-" if v is None else f"{v:.1f}"  # noqa: E731
    L += [f"| {a['arm']} | {a['correct']} | {a['n']} | {a['infra_failures']} | {a['tokens']} | {a['calls']} | {a['reused']} | {f(a['latency_p50_s'])} / {f(a['latency_p95_s'])} | {f(a['tokens_per_success'])} / {f(a['calls_per_success'])} / {f(a['seconds_per_success'])} |" for a in res["arms"]]
    for title, block in (("Confirmatory (primary), Holm over 2", res["confirmatory"]), (f"Sensitivity (questions without infrastructure failure: {res['sensitivity_n']})", res["sensitivity"])):
        L += ["", f"## {title}", "| hypothesis | pair | T-only | other-only | paired diff | 95% CI | p (exact McNemar) | p (Holm) |", "|---|---|---|---|---|---|---|---|"]
        L += [f"| {r['hypothesis']} | {r['pair']} | {r['b_T_only']} | {r['c_other_only']} | {100 * r['diff']:+.1f} pts | [{100 * r['ci_low']:+.1f}, {100 * r['ci_high']:+.1f}] | {r['p']:.4f} | {r['p_holm']:.4f} |" for r in block]
    d = res["descriptive_T_vs_SN"]
    L += ["", "## Descriptive", f"- T vs SN: T-only {d['b_T_only']}, SN-only {d['c_other_only']}, paired diff {100 * d['diff']:+.1f} pts, p {d['p']:.4f} (not part of the confirmatory family)", "- T trace: " + json.dumps(res["trace"])]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    out = analyze(sys.argv[1])
    text = render(out)
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(text)
        Path(sys.argv[sys.argv.index("--out") + 1] + ".json").write_text(json.dumps(out, indent=1))
    print(text)
