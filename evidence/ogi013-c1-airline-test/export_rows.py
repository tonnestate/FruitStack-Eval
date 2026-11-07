#!/usr/bin/env python3
"""Export an OGI-013 campaign directory to FSE-OGI13-PAIR/1 JSONL rows.

usage: export_rows.py CAMPAIGN_DIR [--out FILE] [--benchmark-id ID]
Stdlib only. Writes rows to stdout (or --out) and a summary to stderr.
Unknown values are JSON null; a missing outcome is never a success.
# ponytail: digests are derived from observed files, not a frozen manifest; skills/budget have no source, so they are constant-per-arm.
"""
import argparse, collections, glob, hashlib, json, os, subprocess, sys

TREAT = {"fixed": "FIXED", "adaptive": "ADAPTIVE"}
ENV = "/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013"
TAU2 = os.path.join(ENV, "benchmarks", "tau2-bench")


def sha(data):
    if not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode()
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_jsonl(path):
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    out.append({"event": "CORRUPT_LINE"})
    return out


FREE_CLASSES = {"ANONYMOUS_FREE", "FREE_TIER"}
RECEIPT_CACHE = {}


def load_receipts(arm_dir):
    if arm_dir not in RECEIPT_CACHE:
        recs = read_jsonl(os.path.join(arm_dir, "fruitstack", "plumme-state", "receipts.jsonl"))
        RECEIPT_CACHE[arm_dir] = {r["receipt_id"]: r for r in recs if isinstance(r.get("receipt_id"), str)}
    return RECEIPT_CACHE[arm_dir]


def _num(v):
    return float(v) if type(v) in (int, float) else None


def summarize_receipts(ids, recs):
    """ids: receipt ids as referenced by events (may repeat). Unknown is never 0.
    cost_usd: sum only if every distinct receipt has a non-null cost, else None.
    cost_unknown_receipts: unresolved ids + null-cost receipts + invalid ids.
    quota_units: sum only if receipts carry a quota field, else None."""
    valid = {i for i in ids if isinstance(i, str) and i}
    invalid = len(ids) - sum(1 for i in ids if isinstance(i, str) and i)
    found = [recs[i] for i in sorted(valid) if i in recs]
    unresolved = len(valid) - len(found)
    usage = [r.get("usage") or {} for r in found]
    costs = [_num(u.get("cost_usd")) for u in usage]
    unknown = unresolved + invalid + sum(c is None for c in costs)
    quotas = [_num(u.get("quota_units")) for u in usage]
    return {
        "cost_usd": round(sum(costs), 10) if unknown == 0 else None,
        "cost_unknown_receipts": unknown,
        "quota_units": round(sum(quotas), 10) if found and all(q is not None for q in quotas) else None,
        "classes": {r.get("cost_class") for r in found},
        "tokens_in": sum(u.get("input_tokens") or 0 for u in usage),
        "tokens_out": sum(u.get("output_tokens") or 0 for u in usage),
    }


def tau2_revision():
    try:
        return subprocess.run(["git", "-C", TAU2, "rev-parse", "HEAD"], capture_output=True,
                              text=True, timeout=10, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "UNKNOWN"


def work_ref_default():
    try:
        with open(os.path.join(ENV, "runs", "work.env"), encoding="utf-8") as fh:
            for tok in fh.read().split():
                if tok.startswith("OGI013_WORK_REF="):
                    return tok.split("=", 1)[1]
    except OSError:
        pass
    return "UNKNOWN"


def int_or_none(v):
    return v if type(v) is int else None


def export_arm(arm_dir, task, arm, benchmark_id, revision, work_default):
    tdir = os.path.join(arm_dir, "tasks", task)
    events = read_jsonl(os.path.join(tdir, "fruitstack-events.jsonl"))
    sim = read_jsonl(os.path.join(arm_dir, "sim-usage.jsonl"))
    res_path = os.path.join(tdir, "official-result.json")
    notes = []

    opened = next((e for e in events if e.get("event") == "EPISODE_OPENED"), {})
    closed = next((e for e in events if e.get("event") == "EPISODE_CLOSED"), None)
    steps = [e for e in events if e.get("event") == "STEP"]
    abandoned = [e for e in events if e.get("event") == "STEP_ABANDONED"]
    refused = [e for e in events if e.get("event") == "STEP_REFUSED"]

    # Outcome: official tau2 reward only. Missing file/reward => non-success.
    grade_status, grade, grader_ref, verifier, duration = "UNKNOWN", None, None, None, None
    if os.path.isfile(res_path):
        with open(res_path, "rb") as fh:
            raw = fh.read()
        try:
            res = json.loads(raw)
        except json.JSONDecodeError:
            res = {}
        duration = res.get("duration") if type(res.get("duration")) in (int, float) else None
        rw = ((res.get("reward_info") or {}).get("reward"))
        if type(rw) in (int, float) and 0 <= rw <= 1:
            grade_status, grade = "VERIFIED", float(rw)
            grader_ref = "tau2-official:" + hashlib.sha256(raw).hexdigest()
            verifier = "tau2-official-grader"
        else:
            grade_status = "INCOMPLETE"
            notes.append("reward missing or invalid")
        policy_src = (res.get("policy") or "") + "|" + task
    else:
        policy_src = task
        notes.append("no official-result.json (running or crashed)")

    # Resources: worker side from STEP events; simulator side kept as extra fields.
    calls = len(steps)
    if abandoned or any(not str(e.get("code", "")).startswith("EXECUTION_NOT_PERFORMED")
                        for e in refused):
        calls = None  # attempts whose provider execution is unknown
        notes.append("unknown provider attempt (abandoned or unclassified refusal)")
    refs = [e.get("receipt") for e in steps]
    if not all(isinstance(r, str) and r for r in refs) or len(refs) != len(set(refs)):
        refs = [r for r in refs if isinstance(r, str) and r]
        notes.append("missing or duplicate worker receipt")
    tokens = None
    if steps and all(type(e.get("tokens_in")) is int and type(e.get("tokens_out")) is int for e in steps):
        tokens = sum(e["tokens_in"] + e["tokens_out"] for e in steps)
    if calls is None:
        tokens = None

    # Cost/quota: joined to PlumMe receipt records (receipts.jsonl), never assumed 0.
    recs = load_receipts(arm_dir)
    wsum = summarize_receipts([e.get("receipt") for e in steps], recs)
    wcost = None if calls is None else wsum["cost_usd"]
    wquota = None if calls is None else wsum["quota_units"]

    # Simulator: shared per pair by model_key; cost_usd null stays null.
    ok_sim = [s for s in sim if s.get("success") is True and s.get("model_key")]
    model_keys = sorted({s["model_key"] for s in ok_sim})
    sim_ids = [s["receipt_id"] for s in sim if s.get("receipt_id")]
    ssum = summarize_receipts(sim_ids, recs)
    sim_cost = None if not sim_ids else ssum["cost_usd"]
    sim_tokens = sum((s.get("input_tokens") or 0) + (s.get("output_tokens") or 0) for s in sim if s.get("receipt_id"))

    edges = sorted({f"competence:{a.get('tag')}>{b.get('tag')}" for a, b in zip(steps, steps[1:])})
    models = sorted({e.get("model") for e in steps if e.get("model")})
    write_tools = opened.get("write_tools")
    row = {
        "task_id": task, "arm": arm,
        "benchmark_id": benchmark_id, "benchmark_revision": revision,
        "task_manifest_digest": sha(policy_src), "grader_digest": sha("tau2-evaluator:" + revision),
        "model_pool_digest": None,  # filled per pair
        "skills_digest": sha("no-skill-registry-recorded"),
        "tools_digest": sha(sorted(write_tools)) if write_tools is not None else None,
        "budget_digest": sha((closed or {}).get("budget")),
        "supply_regime_id": sha(model_keys),
        "work_ref": opened.get("work") or work_default,
        "trace_ref": ("fruitstack-sid:" + opened["sid"]) if opened.get("sid") else f"export:{os.path.basename(arm_dir)}",
        "grade_status": grade_status, "grade": grade,
        "grader_receipt_ref": grader_ref, "independent_verifier": verifier,
        "competence_edges": edges,
        "provider_calls": int_or_none(calls), "provider_receipt_refs": refs,
        "total_tokens": int_or_none(tokens), "quota_units": wquota,
        "cost_usd": wcost, "cost_unknown_receipts": wsum["cost_unknown_receipts"],
        "cost_classes": sorted(c for c in wsum["classes"] | ssum["classes"] if c),
        "wall_seconds": duration, "human_minutes": None,
        "sim_calls": len(sim_ids), "sim_tokens": sim_tokens,
        "sim_cost_usd": sim_cost, "sim_cost_unknown_receipts": ssum["cost_unknown_receipts"],
        "sim_model_keys": model_keys,
        "worker_models": models, "arm_dir": os.path.basename(arm_dir),
        "export_notes": notes,
    }
    return row, models, write_tools


def export(campaign, benchmark_id):
    revision, work_default = tau2_revision(), work_ref_default()
    dirs = {}
    for path in sorted(glob.glob(os.path.join(campaign, "*-fixed")) + glob.glob(os.path.join(campaign, "*-adaptive"))):
        if not os.path.isdir(path):
            continue
        name = os.path.basename(path)
        task, arm = name.rsplit("-", 1)[0], TREAT[name.rsplit("-", 1)[1]]
        dirs.setdefault(task, {})[arm] = path
    rows, excluded = [], []
    for task in sorted(dirs):
        arms = {arm: export_arm(path, task, arm, benchmark_id, revision, work_default)
                for arm, path in dirs[task].items()}
        if len(arms) == 2:
            (fr, fm, ft), (ar, am, _) = arms["FIXED"], arms["ADAPTIVE"]
            pool = sha(sorted(set(fm) | set(am)))
            tools = fr["tools_digest"] or ar["tools_digest"]
            if fr["sim_model_keys"] != ar["sim_model_keys"] or not fr["sim_model_keys"]:
                reason = f"simulator model_key mismatch or missing: {fr['sim_model_keys']} vs {ar['sim_model_keys']}"
                excluded.append((task, reason))
            else:
                reason = None
            for r in (fr, ar):
                r["model_pool_digest"], r["tools_digest"] = pool, tools
                r["pair_excluded"], r["exclusion_reason"] = reason is not None, reason
                if reason:  # distinct digest per arm so the evaluator reports the pair as confounded
                    r["supply_regime_id"] = sha(["EXCLUDED", r["arm"], task])
        else:
            (only, _, _), = arms.values()
            reason = "unpaired (other arm missing)"
            excluded.append((task, reason))
            only["pair_excluded"], only["exclusion_reason"] = True, reason
            only["model_pool_digest"] = sha([])
        for r, _, _ in arms.values():
            rows.append(r)
    discarded_dirs = [p for p in glob.glob(os.path.join(campaign, "discarded", "*")) if os.path.isdir(p)]
    return rows, excluded, len(discarded_dirs), dirs


def cost_report(dirs):
    """Markdown per arm dir, worker + simulator, grouped by (provider, model, cost_class)."""
    head = ["| arm | side | provider | model | cost_class | calls | tokens in/out | cost_usd | known/unknown |",
            "|---|---|---|---|---|---|---|---|---|"]
    body, routes, charged = [], {}, set()
    for task in sorted(dirs):
        for arm, path in sorted(dirs[task].items()):
            recs = load_receipts(path)
            steps = [e for e in read_jsonl(os.path.join(path, "tasks", task, "fruitstack-events.jsonl"))
                     if e.get("event") == "STEP"]
            sim = [s["receipt_id"] for s in read_jsonl(os.path.join(path, "sim-usage.jsonl")) if s.get("receipt_id")]
            for side, ids in (("worker", [e.get("receipt") for e in steps]), ("sim", sim)):
                groups = {}
                for i in ids:
                    rec = recs.get(i) if isinstance(i, str) else None
                    key = (rec.get("provider"), rec.get("model"), rec.get("cost_class")) if rec else \
                        ("UNRESOLVED", "UNRESOLVED", "UNRESOLVED")
                    g = groups.setdefault(key, {"calls": 0, "tin": 0, "tout": 0, "cost": 0.0, "known": 0, "unk": 0})
                    g["calls"] += 1
                    u = (rec or {}).get("usage") or {}
                    g["tin"] += u.get("input_tokens") or 0
                    g["tout"] += u.get("output_tokens") or 0
                    c = _num(u.get("cost_usd"))
                    if c is None:
                        g["unk"] += 1
                    else:
                        g["known"] += 1
                        g["cost"] += c
                for (prov, model, cls), g in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
                    cost = f"{g['cost']:.6f}" if g["unk"] == 0 else "null"
                    body.append(f"| {task}/{arm} | {side} | {prov} | {model} | {cls} | {g['calls']} | "
                                f"{g['tin']}/{g['tout']} | {cost} | {g['known']}/{g['unk']} |")
                    routes[(prov, model, cls)] = routes.get((prov, model, cls), 0) + g["calls"]
                    if g["cost"] > 0:  # a known positive charge disqualifies a free-class label
                        charged.add((prov, model, cls))
    bad = sorted({k for k in routes if k[0] == "UNRESOLVED" or k[2] not in FREE_CLASSES} | charged)
    total = sum(routes.values())
    if bad:
        verdict = ("VERDICT: NOT ALL ROUTES PROVABLY FREE. Not provably free: "
                   + ", ".join(f"{p}/{m} [{c}]" for p, m, c in bad) + f" ({total} calls total).")
    else:
        verdict = (f"VERDICT: all {len(routes)} routes ({total} calls) carry FREE cost_class "
                   "(ANONYMOUS_FREE/FREE_TIER) per receipts; cost_usd null on some receipts, so the charge is "
                   "label-based, not measured.")
    return "\n".join(["## Cost evidence (PlumMe receipts)", ""] + head + body + ["", verdict]) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("campaign")
    ap.add_argument("--out")
    ap.add_argument("--benchmark-id", default="tau2-bench:airline")
    ap.add_argument("--cost-report", action="store_true",
                    help="print markdown cost evidence per arm to stdout (rows go to --out only)")
    a = ap.parse_args(argv)
    rows, excluded, n_disc, dirs = export(os.path.abspath(a.campaign), a.benchmark_id)
    text = "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    elif not a.cost_report:
        sys.stdout.write(text)
    if a.cost_report:
        sys.stdout.write(cost_report(dirs))
    pairs = [t for t, arms in dirs.items() if len(arms) == 2]
    excl = {t for t, _ in excluded}
    complete = [t for t in pairs if t not in excl and all(
        r["grade_status"] == "VERIFIED" and not r["export_notes"] for r in rows if r["task_id"] == t)]
    print(f"tasks={len(dirs)} pairs_both_arms={len(pairs)} complete_pairs={len(complete)} "
          f"excluded={len(excluded)} discarded_attempts={n_disc} rows={len(rows)}", file=sys.stderr)
    for arm in ("FIXED", "ADAPTIVE"):
        mine = [r for r in rows if r["arm"] == arm]
        print(f"  {arm}: rows={len(mine)} verified_success={sum(r['grade'] == 1 for r in mine)} "
              f"non_success={sum(r['grade'] != 1 for r in mine)}", file=sys.stderr)
    for t, reason in excluded:
        print(f"  excluded task {t}: {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
