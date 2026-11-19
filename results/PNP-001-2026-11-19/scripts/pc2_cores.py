"""Collect random blind formulas with no degree-2 NS certificate (NS2 and NS2 mod x^2=x fail) but degree-2 PC success; shrink each to a
minimal UNSAT core and re-test the core (director, 2026-11-19)."""
import sys, random, json
sys.argv=[sys.argv[0]]+["21","14","14","1"]
exec(open("deg2_search.py").read().split("stats={}")[0])
random.seed(int(__import__("os").environ.get("SEED","21"))); out=[]
for n in (12,13,14,15,16):
    for _ in range(6000):
        m=random.choice(range(int(0.7*n),n)); cl=sorted({tuple(sorted(random.sample(range(n),3))) for _ in range(m)})
        if not gf3_consistent(cl,n) or sat(cl): continue
        if degree2(cl,n)!="PC2_bool": continue
        core=shrink(cl); used=sorted({v for c in core for v in c}); ren={v:i for i,v in enumerate(used)}
        core=sorted(tuple(sorted(ren[v] for v in c)) for c in core); k=len(used)
        rec={"n_formula":n,"core_vars":k,"core_clauses":len(core),"core":core,"core_gf3":gf3_consistent(core,k),"core_degree":degree2(core,k)}
        out.append(rec); print(json.dumps(rec), flush=True)
        if len(out)>=25: break
    if len(out)>=25: break
json.dump(out, open("pc2_cores.json","w"))
