"""Supply funnel for one PlumMe state: discovered -> role-eligible -> executable (credential + health + circuit) -> actually dispatched / succeeded.
Catalog entries are not working models. Discovery lists provider catalogs only; it sends no inference request. Dispatch counts come from existing receipts (read-only).
usage: supply_counts.py STATE_DIR [RECEIPT_GLOB ...]"""
import asyncio, collections, glob, json, os, sys
os.environ["PLUMME_STATE_DIR"] = sys.argv[1]
from plumme.config import Settings
from plumme.service import PlumMeService, default_adapters
from cherryme.plumme_bridge import _runtime_offer_state

s = Settings.load()
svc = PlumMeService(s, adapters=default_adapters(s))
rows = asyncio.run(svc.discover())
out = {"cost_policy": s.cost_policy, "zero_charge_dispatch": getattr(s, "zero_charge_dispatch", None), "credit_entitlements": list(s.credit_entitlements)}
disc = rows
elig = [r for r in rows if r.get("worker_eligible")]
exe, why = [], collections.Counter()
for r in elig:
    ok, reason, _ = _runtime_offer_state(svc, r)
    (exe.append(r) if ok else why.update([reason or "NOT_EXECUTABLE"]))
cc = lambda rs: dict(collections.Counter(str(r.get("cost_class")) for r in rs))
out["discovered"] = {"offers": len(disc), "models": len({r.get("model_key") or r.get("model") for r in disc}), "by_cost_class": cc(disc)}
out["role_eligible"] = {"offers": len(elig), "models": len({r.get("model_key") or r.get("model") for r in elig}), "by_cost_class": cc(elig)}
out["executable_now"] = {"offers": len(exe), "models": len({r.get("model_key") or r.get("model") for r in exe}), "providers": len({r.get("provider") for r in exe}), "by_cost_class": cc(exe),
                         "excluded_by_reason": dict(why)}
att, succ, mods = 0, 0, collections.Counter()
for pat in sys.argv[2:]:
    for f in glob.glob(pat, recursive=True):
        for l in open(f):
            try: r = json.loads(l)
            except ValueError: continue
            att += 1
            if r.get("success"):
                succ += 1; mods[(r.get("provider"), r.get("model"), r.get("cost_class"))] += 1
out["dispatched_in_receipts"] = {"attempts": att, "successful": succ, "distinct_working_routes": len(mods), "distinct_working_models": len({m[1] for m in mods})}
print(json.dumps(out, indent=1))
