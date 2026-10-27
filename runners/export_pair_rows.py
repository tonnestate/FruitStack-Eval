#!/usr/bin/env python3
"""Export ONE condition pair from an OGI-013 c3-style campaign to FSE-OGI13-PAIR/1 rows.

usage: export_pair_rows.py --campaign DIR --cond-a NAME --cond-b NAME --out rows.jsonl [--mapping-out mapping.json]
Condition A -> role FIXED, condition B -> role ADAPTIVE. Only tasks where BOTH conditions have
official-result.json form a pair; the rest are listed in mapping['unmatched'] (never dropped silently).
Extraction logic (grade, usage, receipts, cost evidence) is copied from runs/export_rows.py (c1/c2).
Stdlib only. No network, no provider calls.
Digests: model_pool_digest and supply_regime_id are the digest of the string 'plumme-auto'; treatment
parity is judged on mapping['model_mix'] (sidecar), not on the digest.
"""
import argparse, hashlib, json, os, subprocess, sys

MAP_SCHEMA = "FSE-OGI13-PAIR-MAPPING/1"
SUPPLY_BASIS = "plumme-auto"
ROLES = {"A": "FIXED", "B": "ADAPTIVE"}


def raw_sha(text):
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


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




def _model_mix(arm_dir, task):
    """Successful worker receipts per (provider|model). Unresolved step refs are counted, never guessed."""
    events = read_jsonl(os.path.join(arm_dir, "tasks", task, "fruitstack-events.jsonl"))
    recs = load_receipts(arm_dir)
    mix, unresolved = {}, 0
    for e in events:
        if e.get("event") != "STEP":
            continue
        rec = recs.get(e.get("receipt")) if isinstance(e.get("receipt"), str) else None
        if rec is None:
            unresolved += 1
        elif rec.get("success") is True:
            key = f"{rec.get('provider')}|{rec.get('model')}"
            mix[key] = mix.get(key, 0) + 1
    return {"successful": dict(sorted(mix.items())), "unresolved_refs": unresolved}


def _economic(arm_dir, task):
    """receipts.metadata.economic numeric dimensions over the worker receipts of this arm.
    A dimension is a total only if every resolved receipt carries it numerically; otherwise null."""
    events = read_jsonl(os.path.join(arm_dir, "tasks", task, "fruitstack-events.jsonl"))
    recs = load_receipts(arm_dir)
    ids = {e.get("receipt") for e in events if e.get("event") == "STEP" and isinstance(e.get("receipt"), str)}
    found = [recs[i] for i in sorted(ids) if i in recs]
    econs = [(r.get("metadata") or {}).get("economic") for r in found]
    keys = sorted({k for x in econs if isinstance(x, dict) for k in x})
    dims = {}
    for k in keys:
        vals = [x.get(k) if isinstance(x, dict) else None for x in econs]
        dims[k] = round(sum(vals), 10) if all(type(v) in (int, float) for v in vals) else None
    return {"receipts": len(found), "with_economic": sum(isinstance(x, dict) for x in econs),
            "dimensions": dims}


def _sum_dims(dicts):
    keys = sorted({k for d in dicts for k in d})
    out = {}
    for k in keys:
        vals = [d.get(k) for d in dicts]
        out[k] = round(sum(vals), 10) if all(type(v) in (int, float) for v in vals) else None
    return out


def _block(campaign, task):
    path = os.path.join(campaign, task, "BLOCK.json")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"error": "unreadable BLOCK.json"}


def export(campaign, cond_a, cond_b, benchmark_id="tau2-bench:airline"):
    """Return (rows, mapping) for one condition pair. rows only contain complete, comparable pairs."""
    if cond_a == cond_b:
        raise ValueError("cond_a and cond_b must differ")
    campaign = os.path.abspath(campaign)
    revision, work_default = tau2_revision(), work_ref_default()
    pool = raw_sha(SUPPLY_BASIS)
    tasks = sorted(d for d in os.listdir(campaign)
                   if d not in ("discarded",) and not d.startswith(".")
                   and os.path.isdir(os.path.join(campaign, d)))
    rows, unmatched, excluded, paired = [], [], [], []
    mix, econ, blocks = {}, {}, {}
    for task in tasks:
        dirs = {ROLES["A"]: os.path.join(campaign, task, cond_a),
                ROLES["B"]: os.path.join(campaign, task, cond_b)}
        have = [c for c, role in ((cond_a, "FIXED"), (cond_b, "ADAPTIVE"))
                if os.path.isfile(os.path.join(campaign, task, c, "tasks", task, "official-result.json"))]
        missing = [c for c in (cond_a, cond_b) if c not in have]
        if missing:
            unmatched.append({"task_id": task, "missing_conditions": missing, "present_conditions": have})
            continue
        fr, fm, ft = export_arm(dirs["FIXED"], task, "FIXED", benchmark_id, revision, work_default)
        ar, am, at = export_arm(dirs["ADAPTIVE"], task, "ADAPTIVE", benchmark_id, revision, work_default)
        reason = None
        if fr["sim_model_keys"] != ar["sim_model_keys"] or not fr["sim_model_keys"]:
            reason = f"simulator model_key mismatch or missing: {fr['sim_model_keys']} vs {ar['sim_model_keys']}"
        elif fr["tools_digest"] is None or ar["tools_digest"] is None:
            reason = "tools digest unknown (write_tools missing) on at least one arm"
        if reason:
            excluded.append({"task_id": task, "reason": reason})
            continue
        for r in (fr, ar):
            r["model_pool_digest"] = pool
            r["supply_regime_id"] = pool
            rows.append(r)
        paired.append(task)
        mix[task] = {"FIXED": _model_mix(dirs["FIXED"], task), "ADAPTIVE": _model_mix(dirs["ADAPTIVE"], task)}
        econ[task] = {"FIXED": _economic(dirs["FIXED"], task), "ADAPTIVE": _economic(dirs["ADAPTIVE"], task)}
        blocks[task] = _block(campaign, task)
    disc = os.path.join(campaign, "discarded")
    mapping = {
        "schema": MAP_SCHEMA,
        "campaign": campaign,
        "benchmark_id": benchmark_id,
        "benchmark_revision": revision,
        "conditions": {"A": {"name": cond_a, "role": "FIXED"}, "B": {"name": cond_b, "role": "ADAPTIVE"}},
        "model_pool_digest_basis": SUPPLY_BASIS,
        "model_pool_digest_note": "digest of the string 'plumme-auto'; NOT a treatment-parity claim. "
                                  "Per-row model mix is in model_mix.",
        "tasks_seen": tasks,
        "paired": paired,
        "unmatched": unmatched,
        "excluded": excluded,
        "discarded": sorted(os.listdir(disc)) if os.path.isdir(disc) else [],
        "blocks": blocks,
        "model_mix": mix,
        "economic": econ,
        "economic_totals": {
            "FIXED": _sum_dims([econ[t]["FIXED"]["dimensions"] for t in paired]),
            "ADAPTIVE": _sum_dims([econ[t]["ADAPTIVE"]["dimensions"] for t in paired]),
        },
    }
    return rows, mapping


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--cond-a", required=True)
    ap.add_argument("--cond-b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mapping-out")
    ap.add_argument("--benchmark-id", default="tau2-bench:airline")
    a = ap.parse_args(argv)
    rows, mapping = export(a.campaign, a.cond_a, a.cond_b, a.benchmark_id)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    if a.mapping_out:
        with open(a.mapping_out, "w", encoding="utf-8") as fh:
            json.dump(mapping, fh, indent=2, sort_keys=True)
            fh.write("\n")
    print(f"paired={len(mapping['paired'])} rows={len(rows)} unmatched={len(mapping['unmatched'])} "
          f"excluded={len(mapping['excluded'])}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
