#!/usr/bin/env python3
"""Independent COLLAB-1 evaluator. Reads ONLY recorded evidence (episode records, official tau2 results, events, PlumMe receipts) and, here and only here, the official reference actions of each task.
Deterministic: same evidence -> byte-identical report.json / report.md (no timestamps, sorted keys, seeded bootstrap).
Confirmatory (write-opportunity stratum, exact two-sided McNemar on discordant pairs, Holm over three; reuses the registered C3 functions of runners/ogi013_confirmatory.py):
  E1 official success COLLAB vs SINGLE; E2 official success COLLAB vs SINGLE-E; E3 no state-changing deviation (AMENDMENT-1) COLLAB vs SINGLE.
Missing / incomplete episodes are non-success for E1/E2 (as in C3); for E3 a pair with a missing episode is excluded and counted. Everything else is descriptive.
usage: analyze_study.py CAMPAIGN_DIR MANIFEST BUDGET TAU2_DATA_DIR"""
import importlib.util
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


guard = _load("pilot_guard", CODE / "evidence/ogi013-pilot/pilot_guard.py")
dm = _load("decision_metrics", CODE / "evidence/ogi013-phase2/decision_metrics.py")
conf = _load("ogi013_confirmatory", CODE / "runners/ogi013_confirmatory.py")
COMPLETED = {"DONE", "BUDGET_STOP", "TIMEOUT"}


def _jsonl(p: Path):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.is_file() else []


def _round(x):
    return round(x, 6) if isinstance(x, float) else x


def episode(C: Path, R: Path, t: dict, cond: str, reference: dict, reserve: int) -> dict:
    ref = t["task_ref"]
    dirname = ref.replace(":", "_")
    rec_p = C / dirname / f"{cond}.episode.json"
    rec = json.loads(rec_p.read_text()) if rec_p.is_file() else {}
    arm = f"{C.name}/{dirname}/{cond}"
    out = {"task": ref, "condition": cond, "status": rec.get("status", "MISSING"), "official": False, "success": False, "decision": None}
    off_p = C / dirname / cond / "tasks" / t["task_id"] / "official-result.json"
    if off_p.is_file():
        official = json.loads(off_p.read_text())
        events = _jsonl(off_p.with_name("fruitstack-events.jsonl"))
        out["official"] = "reward_info" in official
        out["success"] = out["official"] and (official["reward_info"] or {}).get("reward") == 1.0
        out["decision"] = dm.summarize(official, events, reference.get(ref, []))
    u = guard.usage(str(R), [arm], reserve)
    rows = guard.dispatches(str(R), arm)
    started, ended = rec.get("started_at"), rec.get("ended_at")
    out["resources"] = {"requests": u["dispatches"], "tokens": u["tokens"], "receipts": len(rows), "cash_usd": _round(u["cash_usd"]), "entitlement": u["entitlement"], "rejected_unprocessed": u["rejected_unprocessed"],
                        "wall_s": _round(ended - started) if started and ended else None}
    out["lineages"] = sorted({r["lineage"] for r in rows if r["lineage"]})
    out["providers"] = sorted({r["provider"] for r in rows if r["provider"]})
    out["lineage_providers"] = {l: sorted({r["provider"] for r in rows if r["lineage"] == l and r["provider"]}) for l in out["lineages"]}
    return out


def _pair_rows(eps, tasks, a_cond, b_cond, outcome, require_both=False):
    rows, excluded = [], 0
    for t in tasks:
        a, b = eps[(t["task_ref"], a_cond)], eps[(t["task_ref"], b_cond)]
        if require_both and not (a["official"] and b["official"]):
            excluded += 1
            continue
        for arm, e in (("FIXED", a), ("ADAPTIVE", b)):
            ok = outcome(e)
            rows.append({"task_id": t["task_ref"], "arm": arm, "grade": 1.0 if ok else 0.0, "grade_status": "VERIFIED"})
    return rows, excluded


def _boot(values, seed=4242, n=2000):
    if not values:
        return [None, None]
    rng, m = random.Random(seed), len(values)
    means = sorted(sum(values[rng.randrange(m)] for _ in range(m)) / m for _ in range(n))
    return [_round(means[int(0.025 * n)]), _round(means[int(0.975 * n)])]


def evaluate(C: Path, manifest: dict, budget: dict, data_dir: Path) -> dict:
    R = C.parent
    reference = {}
    for domain in sorted({t["domain"] for t in manifest["tasks"]}):
        for task in json.loads((data_dir / "domains" / domain / "tasks.json").read_text()):
            reference[f"{domain}:{task['id']}"] = (task.get("evaluation_criteria") or {}).get("actions") or []
    reserve = budget["reserve_tokens_per_dispatch"]
    conds = manifest["conditions"]
    eps = {(t["task_ref"], c): episode(C, R, t, c, reference, reserve) for t in manifest["tasks"] for c in conds}
    wr = [t for t in manifest["tasks"] if t["stratum"] == "write-opportunity"]
    nowrite = [t for t in manifest["tasks"] if t["stratum"] != "write-opportunity"]
    success = lambda e: e["success"]  # noqa: E731
    clean = lambda e: e["official"] and not e["decision"]["state_changing_deviations"]  # noqa: E731
    tests, raw = {}, {}
    for name, (a, b, outcome, both, label) in {"E1": ("COLLAB", "SINGLE", success, False, "official success"), "E2": ("COLLAB", "SINGLE-E", success, False, "official success"),
                                              "E3": ("COLLAB", "SINGLE", clean, True, "no state-changing deviation")}.items():
        rows, excluded = _pair_rows(eps, wr, a, b, outcome, both)
        r = conf.analyse_pair(rows)
        tests[name] = {"comparison": f"{a} vs {b}", "outcome": label, "pairs": r["pairs"], "excluded_pairs": excluded, "a_only": r["a_only"], "b_only": r["b_only"], "both": r["both_success"], "neither": r["neither"],
                       "discordant": r["discordant"], "p_exact_mcnemar_two_sided": _round(r["p_exact_mcnemar"]), "risk_difference_a_minus_b": _round(r["risk_difference"]) if r["risk_difference"] is not None else None,
                       "risk_difference_ci95": [_round(x) if x is not None else None for x in r["risk_difference_ci95_exact"]]}
        raw[name] = r["p_exact_mcnemar"]
    adj = conf.holm(raw)
    for name in tests:
        tests[name]["p_holm"] = _round(adj[name])
        tests[name]["significant_at_0.05"] = adj[name] < 0.05
    # ---- descriptive --------------------------------------------------------------------------------------------------------------------------------------------
    def rate(tasks, cond):
        n = len(tasks)
        s = sum(eps[(t["task_ref"], cond)]["success"] for t in tasks)
        return {"n": n, "success": s, "rate": _round(s / n) if n else None}
    success_rates = {c: {"write-opportunity": rate(wr, c), "no-write-control": rate(nowrite, c), **{d: rate([t for t in wr if t["domain"] == d], c) for d in ("airline", "retail")}} for c in conds}
    outcomes = Counter()
    helped, worse = [], []
    for t in manifest["tasks"]:
        e = eps[(t["task_ref"], "COLLAB")]
        for r in (e["decision"] or {}).get("reviews", []):
            outcomes[r["outcome"]] += 1
            if r["outcome"] == "PREVENTED_WRITE_ERROR":
                helped.append({"task": t["task_ref"], "episode_success": e["success"]})
            if r["outcome"] in ("CORRECT_BLOCKED", "ERROR_REPLACED_BY_DIFFERENT_ERROR", "UNNECESSARY_CHANGE", "ERROR_NOT_FIXED"):
                worse.append({"task": t["task_ref"], "outcome": r["outcome"]})
    quality = {}
    for c in conds:
        ds = [eps[(t["task_ref"], c)]["decision"] for t in manifest["tasks"] if eps[(t["task_ref"], c)]["decision"]]
        quality[c] = {"episodes_with_official_result": len(ds), "state_changing_deviation_episodes": sum(1 for d in ds if d["state_changing_deviations"]), "unnecessary_transfer_episodes": sum(1 for d in ds if d["unnecessary_transfer"]),
                      "objectives_abandoned": dict(sorted(Counter(d["abandon_cause"] for d in ds if d["objectives_abandoned"]).items())),
                      "expected_actions_completed": sum(len(d["expected_actions_completed"]) for d in ds), "expected_actions_total": sum(len(d["expected_actions"]) for d in ds),
                      "policy_evidence": dict(sorted(Counter(str(d["policy_evidence"]) for d in ds).items()))}
    resources = {}
    for c in conds:
        es = [eps[(t["task_ref"], c)] for t in manifest["tasks"]]
        resources[c] = {"requests": sum(e["resources"]["requests"] for e in es), "tokens": sum(e["resources"]["tokens"] for e in es), "cash_usd": _round(sum(e["resources"]["cash_usd"] for e in es)),
                        "wall_s": _round(sum(e["resources"]["wall_s"] or 0 for e in es)), "rejected_unprocessed": sum(e["resources"]["rejected_unprocessed"] for e in es),
                        "entitlement": {k: sum(e["resources"]["entitlement"].get(k, {}).get(f, 0) for e in es) for k in ("TRIAL_CREDIT", "INCLUDED") for f in ("dispatches",)}}
    paired = {}
    for other in ("SINGLE", "SINGLE-E"):
        for field in ("requests", "tokens"):
            d = [eps[(t["task_ref"], "COLLAB")]["resources"][field] - eps[(t["task_ref"], other)]["resources"][field] for t in manifest["tasks"]
                 if eps[(t["task_ref"], "COLLAB")]["status"] in COMPLETED and eps[(t["task_ref"], other)]["status"] in COMPLETED]
            paired[f"COLLAB-{other}:{field}"] = {"n": len(d), "mean": _round(statistics.fmean(d)) if d else None, "median": _round(statistics.median(d)) if d else None, "bootstrap_ci95_mean": _boot(d)}
    matched = [t for t in wr if eps[(t["task_ref"], "SINGLE-E")]["resources"]["requests"] and eps[(t["task_ref"], "COLLAB")]["resources"]["requests"] <= 1.25 * eps[(t["task_ref"], "SINGLE-E")]["resources"]["requests"]]
    rows, _ = _pair_rows(eps, matched, "COLLAB", "SINGLE-E", success)
    effort_matched = conf.analyse_pair(rows) if rows else {}
    sensitivity = {"E2_effort_matched_subset": {"rule": "pairs where COLLAB requests <= 1.25 x SINGLE-E requests (descriptive)", "pairs": len(matched),
                                                "a_only": effort_matched.get("a_only"), "b_only": effort_matched.get("b_only"), "p_exact_mcnemar_two_sided": _round(effort_matched["p_exact_mcnemar"]) if effort_matched else None}}
    reviews = [(t, r) for t in manifest["tasks"] for r in ((eps[(t["task_ref"], "COLLAB")]["decision"] or {}).get("reviews", []))]
    independence = {"reviews": len(reviews), "independent_reviews": sum(1 for _, r in reviews if r["independent_review"]), "final_reviewed": sum(1 for _, r in reviews if r["final_reviewed"]),
                    "lineages_per_condition": {c: dict(sorted(Counter(l for t in manifest["tasks"] for l in eps[(t["task_ref"], c)]["lineages"]).items())) for c in conds},
                    "providers_per_condition": {c: dict(sorted(Counter(p for t in manifest["tasks"] for p in eps[(t["task_ref"], c)]["providers"]).items())) for c in conds}}
    discarded = {"episodes": 0, "requests": 0, "tokens": 0}
    for rec in sorted((C / "discarded").rglob("*.episode.json")) if (C / "discarded").is_dir() else []:
        arm = str(rec.with_name(rec.name[: -len(".episode.json")]).relative_to(R))
        u = guard.usage(str(R), [arm], reserve)
        discarded["episodes"] += 1
        discarded["requests"] += u["dispatches"]
        discarded["tokens"] += u["tokens"]
    status = Counter(e["status"] for e in eps.values())
    return {"study": manifest["study"], "episodes_planned": len(eps), "episode_status": dict(sorted(status.items())),
            "infra_incomplete_blocks": sorted(p.name[: -len("-INFRA_INCOMPLETE.txt")] for p in (C / "discarded").glob("*-INFRA_INCOMPLETE.txt")) if (C / "discarded").is_dir() else [],
            "confirmatory": tests, "success_rates": success_rates, "decision_outcomes": dict(sorted(outcomes.items())), "critique_helped": helped, "critique_made_worse": worse, "decision_quality": quality,
            "resources": resources, "paired_resource_differences": paired, "sensitivity": sensitivity, "independence": independence, "discarded_usage": discarded,
            "premature_stop_episodes": {c: sum(1 for t in manifest["tasks"] if (eps[(t["task_ref"], c)]["decision"] or {}).get("abandon_cause") == "PREMATURE_STOP_PENDING") for c in conds},
            "interpretation": "Technical completion is not organisational advantage. A confirmatory endpoint counts only if its Holm-adjusted p < 0.05; with 40 pairs most outcomes are inconclusive and that is a valid result. No effect size or "
                              "'organisational intelligence' claim follows from this report. Descriptive sections are exploratory."}


def render(rep: dict) -> str:
    L = [f"# {rep['study']} - evaluation report", "", f"Episodes planned {rep['episodes_planned']}; status {rep['episode_status']}; INFRA_INCOMPLETE blocks {rep['infra_incomplete_blocks']}.", "",
         "## Confirmatory (write-opportunity stratum; exact two-sided McNemar; Holm over E1-E3)", "| endpoint | comparison | pairs | A only | B only | p | p Holm | significant |", "|---|---|---|---|---|---|---|---|"]
    for k, v in rep["confirmatory"].items():
        L.append(f"| {k} {v['outcome']} | {v['comparison']} | {v['pairs']} | {v['a_only']} | {v['b_only']} | {v['p_exact_mcnemar_two_sided']} | {v['p_holm']} | {v['significant_at_0.05']} |")
    L += ["", "## Official success", "| condition | write-opportunity | no-write control |", "|---|---|---|"]
    for c, v in rep["success_rates"].items():
        L.append(f"| {c} | {v['write-opportunity']['success']}/{v['write-opportunity']['n']} | {v['no-write-control']['success']}/{v['no-write-control']['n']} |")
    L += ["", f"## Decision outcomes of COLLAB reviews\n{rep['decision_outcomes']}", f"Critique helped: {rep['critique_helped']}", f"Critique made decisions worse: {rep['critique_made_worse']}", "", "## Decision quality by condition"]
    for c, v in rep["decision_quality"].items():
        L.append(f"- {c}: {v}")
    L += ["", "## Resources (all attempts counted in discarded_usage separately)"]
    for c, v in rep["resources"].items():
        L.append(f"- {c}: {v}")
    L += [f"- paired differences: {rep['paired_resource_differences']}", f"- sensitivity: {rep['sensitivity']}", f"- discarded attempts: {rep['discarded_usage']}", "", f"## Independence and diversity\n{rep['independence']}",
          f"Premature stops with a pending action: {rep['premature_stop_episodes']}", "", rep["interpretation"], ""]
    return "\n".join(L)


def write_report(C: Path, manifest: dict, budget: dict, data_dir: Path) -> dict:
    rep = evaluate(Path(C), manifest, budget, Path(data_dir))
    (Path(C) / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True) + "\n")
    (Path(C) / "report.md").write_text(render(rep))
    return rep


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    rep = write_report(Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), json.loads(Path(sys.argv[3]).read_text()), Path(sys.argv[4]))
    print(json.dumps(rep["confirmatory"], indent=1, sort_keys=True))
