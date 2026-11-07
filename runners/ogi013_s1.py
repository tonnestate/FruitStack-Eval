#!/usr/bin/env python3
"""S1 small advantage test (preregistered: evidence/ogi013-small-proof/PREREG.md, selection.json). Arms: T = Luna+nemotron duo under the Brother closed loop (qa1.run_T duo+loop), SN = nemotron alone
(qa2d.run_SN). Luna alone = recorded SL. One attempt per arm and item, no retries, RunBudget hard cap. `analyze` prints the preregistered estimates."""
import argparse
import json
import math
import sys
from pathlib import Path

import ogi013_qa1 as q1
import ogi013_qa2d as q2
from ogi013_qa1 import Context, attempt, finish, load_jsonl

POP_N, POP_LUNA_OK = 198, 149


def cp(k: int, n: int, alpha: float = 0.05) -> tuple:
    """Exact Clopper-Pearson interval by bisection on the binomial tail."""
    def cdf(x, p):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: 1 - cdf(k - 1, p) < alpha / 2)
    upper = 1.0 if k == n else solve(lambda p: cdf(k, p) > alpha / 2)
    return lower, upper


def estimate(rows: dict, sel: dict, arm: str, worst: bool) -> dict:
    def ok(qid):
        r = rows.get((qid, arm))
        return bool(r and r["status"] == "OK" and r["correct"]) if (worst or (r and r["status"] == "OK")) else None
    w_ids, r_ids = sel["W"], sel["R"]
    wk = [ok(i) for i in w_ids]; rk = [ok(i) for i in r_ids]
    wv, rv = [x for x in wk if x is not None], [x for x in rk if x is not None]
    if not wv or not rv:
        return {"arm": arm, "note": "no complete stratum"}
    res_k, res_n, har_k, har_n = sum(wv), len(wv), len(rv) - sum(rv), len(rv)
    pw = (POP_N - POP_LUNA_OK) / POP_N
    f = lambda rescue, harm: pw * rescue + (1 - pw) * (1 - harm)
    rl, ru = cp(res_k, res_n); hl, hu = cp(har_k, har_n)
    return {"arm": arm, "worst_case_missing_as_wrong": worst, "rescue": f"{res_k}/{res_n}", "harm": f"{har_k}/{har_n}", "est_accuracy": round(f(res_k / res_n, har_k / har_n), 4),
            "ci95_conservative": [round(f(rl, hu), 4), round(f(ru, hl), 4)], "luna_alone": round(POP_LUNA_OK / POP_N, 4)}


def classify_t_row(row: dict) -> dict:
    """Offline validity classification of a stored S1 T row (corrected protocol 2026-11-07; original verdict untouched).
    cooperation: INFRA_FAILED | LUNA_ONLY_DUPLICATION (no nemotron position, or one lineage twice) | GENUINE_LUNA_NEMOTRON (both lineages submitted a first answer).
    controller: CONSENSUS | VERIFIED_OBJECTION | PROVISIONAL_UNVERIFIED (weights / formal concession chose among unverified candidates) | NONE."""
    if row.get("status") != "OK":
        return {"cooperation": "INFRA_FAILED", "controller": "NONE", "valid_duo": False}
    lins = list((row.get("lineages") or {}).get("positions", {}).values())
    fin = list((row.get("final_positions") or {}).keys())
    luna_twice = sum(1 for m in fin if str(m).startswith("gpt-6-luna")) >= 2
    genuine = "luna" in lins and "nemotron" in lins and not luna_twice
    rule = (row.get("loop_closing") or {}).get("rule")
    ctl = {"CONSENSUS": "CONSENSUS", "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION": "VERIFIED_OBJECTION"}.get(rule, "PROVISIONAL_UNVERIFIED" if rule else "NONE")
    return {"cooperation": "GENUINE_LUNA_NEMOTRON" if genuine else "LUNA_ONLY_DUPLICATION", "controller": ctl, "valid_duo": genuine, "luna_twice_in_final_positions": luna_twice}


def reclassify(rows: list, sel: dict) -> dict:
    out = []
    for r in rows:
        if r["arm"] != "T":
            continue
        c = classify_t_row(r)
        out.append({"qid": r["qid"], "stratum": "W" if r["qid"] in sel["W"] else "R", "correct": r["correct"], "letter": r.get("letter"), **c})
    tally = {k: sum(1 for x in out if x["cooperation"] == k) for k in ("GENUINE_LUNA_NEMOTRON", "LUNA_ONLY_DUPLICATION", "INFRA_FAILED")}
    ctl = {k: sum(1 for x in out if x["controller"] == k) for k in ("CONSENSUS", "VERIFIED_OBJECTION", "PROVISIONAL_UNVERIFIED", "NONE")}
    return {"rows": out, "cooperation_tally": tally, "controller_tally": ctl, "luna_twice_rows": sum(1 for x in out if x.get("luna_twice_in_final_positions")),
            "valid_duo_rows": [x["qid"] for x in out if x["valid_duo"]]}


def counterfactual_t_row(row: dict) -> dict:
    """HYPOTHETICAL decision: the archived closing state of a T row replayed through the corrected CooperationControl.close(). Observed fields are never modified. Critique events were not archived
    (all 16 stored closings have 0 independently confirmed objections), so only concessions are replayed."""
    from fs_codemode.loop import CooperationControl, LoopParams
    c = row["loop_closing"]
    ctl = CooperationControl(LoopParams(), models=(q1.LUNA_KEY, q1.NEMO_KEY))
    ctl.concessions = list(c.get("concessions") or [])
    s1_first = (row.get("first_by_pos") or {}).get("S1")
    ctl.primary_first = lambda: s1_first
    new = ctl.close({"signatures": c["signatures"], "first": c["first"], "models": list(c["signatures"])})
    return {"qid": row["qid"], "key": row["key"], "initial_answer": s1_first, "observed_final": row.get("letter"), "observed_rule": c.get("rule"), "hypothetical_final": new["final_answer"],
            "hypothetical_rule": new["rule"], "independent_collaboration": new["independent_collaboration"], "verified_improvement": new["verified_improvement"],
            "unresolved_disagreement": new["unresolved_disagreement"]}


def counterfactual(rows: list, sel: dict) -> dict:
    out = []
    for r in rows:
        if r["arm"] == "T" and r.get("status") == "OK":
            out.append({**counterfactual_t_row(r), **{k: classify_t_row(r)[k] for k in ("cooperation",)}})
    def acc(group, field):
        return f"{sum(1 for x in group if x[field] == x['key'])}/{len(group)}"
    luna_only = [x for x in out if x["cooperation"] == "LUNA_ONLY_DUPLICATION"]
    genuine = [x for x in out if x["cooperation"] == "GENUINE_LUNA_NEMOTRON"]
    return {"LABEL": "observed = archived result; hypothetical = corrected rule replayed offline, NOT an experiment", "rows": out,
            "luna_only_12": {"initial": acc(luna_only, "initial_answer"), "observed_final": acc(luna_only, "observed_final"), "hypothetical_final": acc(luna_only, "hypothetical_final")},
            "genuine_4": {"initial": acc(genuine, "initial_answer"), "observed_final": acc(genuine, "observed_final"), "hypothetical_final": acc(genuine, "hypothetical_final")},
            "lost_by_observed": [x["qid"] for x in luna_only if x["initial_answer"] == x["key"] != x["observed_final"]],
            "recovered_by_observed": [x["qid"] for x in luna_only if x["initial_answer"] != x["key"] == x["observed_final"]]}


def analyze(out: Path, sel: dict) -> None:
    rows = {(r["qid"], r["arm"]): r for r in load_jsonl(out / "results.jsonl")}
    for arm in ("T", "SN"):
        for worst in (False, True):
            print(json.dumps(estimate(rows, sel, arm, worst)))
    for stratum in ("W", "R"):
        for qid in sel[stratum]:
            t, n = rows.get((qid, "T")), rows.get((qid, "SN"))
            print(json.dumps({"stratum": stratum, "qid": qid, "T": [t and t["status"], t and t.get("letter"), t and t["correct"], t and t.get("how")],
                              "SN": [n and n["status"], n and n.get("letter"), n and n["correct"]]}))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--selection", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--run-cap", type=int, default=500)
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--counterfactual", action="store_true", help="offline: replay the archived closings through the corrected controller (hypothetical, no provider call)")
    ap.add_argument("--reclassify", action="store_true", help="offline validity classification of the stored T rows (no provider call)")
    a = ap.parse_args()
    sel = json.loads(a.selection.read_text())
    if a.analyze:
        analyze(a.out, sel)
        return 0
    if a.counterfactual:
        print(json.dumps(counterfactual(load_jsonl(a.out / "results.jsonl"), sel), indent=1))
        return 0
    if a.reclassify:
        print(json.dumps(reclassify(load_jsonl(a.out / "results.jsonl"), sel), indent=1))
        return 0
    a.out.mkdir(parents=True, exist_ok=True)
    ctx = Context(a.out, None, 2)
    from plumme.budget import RunBudget
    ctx.run_budget = RunBudget(max_provider_calls=a.run_cap, max_cost_usd=0.0)
    ctx.stack.svc.set_run_budget(ctx.run_budget)
    import ogi013_vote
    ogi013_vote.TEXT_CAP_OBJECTION = ogi013_vote.TEXT_CAP_REPLY = 10 ** 6
    items = {q["id"]: q for q in load_jsonl(a.data)}
    res_path = a.out / "results.jsonl"
    done = {(r["qid"], r["arm"]) for r in load_jsonl(res_path)} if res_path.exists() else set()
    order = [x for pair in zip(sel["W"], sel["R"]) for x in pair]                  # interleaved strata
    for qid in order:
        q = items[qid]
        for arm, fn in (("T", lambda: attempt(q1.run_T, ctx, q, True, True)), ("SN", lambda: attempt(q2.run_SN, ctx, q))):
            if (qid, arm) in done:
                continue
            row = finish(q, arm, fn(), False)                                      # one attempt, no rerun
            with res_path.open("a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(json.dumps({"qid": qid, "arm": arm, "status": row["status"], "letter": row.get("letter"), "correct": row["correct"], "how": row.get("how"),
                              "detail": (row.get("infra_detail") or "")[:120], "used": ctx.run_budget.provider_attempt_count}), flush=True)
            if ctx.stop or ctx.run_budget.provider_attempt_count >= a.run_cap:
                print(json.dumps({"STOP": ctx.stop or "RUN_CAP"}), flush=True)
                return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
