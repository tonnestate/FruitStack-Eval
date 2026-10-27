"""Experimental-integrity audit of c1 (read-only): cost classes / trial credit, agent-model composition per arm, discarded attempts, provider admission drift."""
import json, sys, glob, os, collections
base = sys.argv[1]
def receipts(d):
    f = f"{d}/fruitstack/plumme-state/receipts.jsonl"
    return [json.loads(l) for l in open(f)] if os.path.exists(f) else []
def sim(d):
    f = f"{d}/sim-usage.jsonl"
    return [json.loads(l) for l in open(f)] if os.path.exists(f) else []
out = {"kept": {}, "discarded": {}}
def audit(dirs):
    cc, prov, ok, nocost, agent_models = collections.Counter(), collections.Counter(), collections.Counter(), 0, collections.Counter()
    for d in dirs:
        for r in receipts(d):
            cc[r.get("cost_class")] += 1; prov[r.get("provider")] += 1; ok[bool(r.get("success"))] += 1
            if r.get("success"): agent_models[r.get("model")] += 1
            if r.get("success") and (r.get("usage") or {}).get("cost_usd") is None: nocost += 1
    return dict(arms=len(dirs), receipts=sum(ok.values()), cost_class=dict(cc), providers=dict(prov), success=dict(ok), success_without_cost_usd=nocost, agent_models=dict(agent_models.most_common(12)))
kept = sorted(glob.glob(f"{base}/*-fixed") + glob.glob(f"{base}/*-adaptive"))
out["kept"]["fixed"] = audit([d for d in kept if d.endswith("-fixed")]); out["kept"]["adaptive"] = audit([d for d in kept if d.endswith("-adaptive")])
disc = [d for d in glob.glob(f"{base}/discarded/*") if os.path.isdir(d)]
out["discarded"] = audit(disc)
trial = [os.path.basename(d) for d in disc + kept if any(r.get("cost_class") == "TRIAL_CREDIT" for r in receipts(d))]
out["trial_credit_arms"] = trial
out["trial_credit_in_kept"] = [t for t in trial if "attempt" not in t]
# simulator model per pair
pairs = collections.defaultdict(set)
for d in kept:
    t = os.path.basename(d).rsplit("-", 1)[0]
    for s in sim(d):
        if s.get("success"): pairs[t].add(s.get("model_key"))
out["pairs_with_multiple_sim_models"] = {t: sorted(m) for t, m in pairs.items() if len(m) > 1}
out["sim_calls_kept"] = {k: sum(len(sim(d)) for d in kept if d.endswith(k)) for k in ("-fixed", "-adaptive")}
json.dump(out, open("integrity.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str)[:3500])
