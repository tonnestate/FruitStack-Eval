"""Discovery-cost probe on the 216 type-B cores at n = 8: (1) structure of the certifying covering cuts (complement sizes);
(2) does a POLYNOMIAL candidate family find a certificate: covering cuts sum_{S} x_i >= ceil(min_P sum_S x) for S = V minus <= t variables
(O(n^t) candidates)? Exact rational arithmetic; emptiness by exact polygon clipping."""
import json, itertools, math, collections, sys
from fractions import Fraction as Fr
sys.path.insert(0,"."); import importlib.util
spec=importlib.util.spec_from_file_location("cg","cgrank_n.py")
src=open("cgrank_n.py").read().split("res={\"n\":n")[0].replace("n=int(sys.argv[1]); KMAX=int(sys.argv[2]) if len(sys.argv)>2 else 2","n=8; KMAX=1")
ns={}; exec(src, ns)
setup, vertices, clip = ns["setup"], ns["vertices"], ns["clip"]
r=json.load(open("cgrank_n8.json")); B=[c for c in r["cores"] if c["cert"]["kind"]=="B_cut_set"]
comp=collections.Counter()
for c in B:
    vs=c["cert"]["vars"]; comp[tuple(sorted(len([i for i in range(len(vs)) if cut["c"][i]==0]) for cut in c["cert"]["cuts"]))]+=1
print("complement sizes of the two certifying cuts (|V\\S1|,|V\\S2|):", dict(comp))
def found_with(cl, t):
    used,d,expr,base=setup(cl); V=vertices(base,d); nu=len(used)
    cx=sum(v[0] for v in V)/len(V); cy=sum(v[1] for v in V)/len(V)
    poly=sorted(V,key=lambda v: math.atan2(float(v[1]-cy),float(v[0]-cx)))
    cands=0
    for k in range(t+1):
        for drop in itertools.combinations(range(nu),k):
            cands+=1
            S=[j for j in range(nu) if j not in drop]
            c0=sum(expr[j][0] for j in S); ca=[sum(expr[j][1][g] for j in S) for g in range(d)]
            mn=min(c0+ca[0]*v[0]+ca[1]*v[1] for v in V)
            if mn!=math.ceil(mn):                      # covering cut sum_S x >= ceil(mn):  ca.t >= ceil(mn) - c0
                poly=clip(poly, ca, math.ceil(mn)-c0)
                if not poly: return True, cands
    return False, cands
for t in (0,1,2,3):
    ok=0; maxc=0
    for c in B:
        f,cands=found_with([tuple(x) for x in c["clauses"]], t); ok+=f; maxc=max(maxc,cands)
    print(f"candidate family 'V minus <= {t} variables' (<= {maxc} covering cuts per core): certificate found for {ok}/{len(B)}")
