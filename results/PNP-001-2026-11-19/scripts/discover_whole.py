"""Decisive form of point 3 (discovery cost): the cheap cut family applied to the WHOLE formula, without knowing its core.
Whole formulas = an n=8 minimal GAP core + k new variables, each attached by two clauses to existing variables (keeps the LP
dimension d <= 2, so emptiness is decided by exact polygon clipping). Every such formula is UNSAT (it contains the core).
Family F_t: single-variable cuts x_j >= ceil(min x_j), x_j <= floor(max x_j) for all variables, plus covering cuts
sum_{i in S} x_i >= ceil(min_P sum_S x) for S = V(F) minus <= t variables. Question: does F_t still empty P, or does it need the core?"""
import json, itertools, math, random, collections, sys
from fractions import Fraction as Fr
src=open("cgrank_n.py").read().split('res={"n":n')[0].replace("n=int(sys.argv[1]); KMAX=int(sys.argv[2]) if len(sys.argv)>2 else 2","n=8; KMAX=1")
ns={}; exec(src, ns); setup, vertices, clip = ns["setup"], ns["vertices"], ns["clip"]
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
r=json.load(open("cgrank_n8.json"))
B=[c for c in r["cores"] if c["cert"]["kind"]=="B_cut_set"]; A=[c for c in r["cores"] if c["cert"]["kind"]=="A_single_variable"]
def family_empty(cl, t):
    s=setup(cl)
    if s is None: return "rational_infeasible"
    used,d,expr,base=s
    if d>2: return "skip_d"
    V=vertices(base,d)
    if d==0: return "point"
    def val(S, v): return sum(expr[j][0] for j in S)+sum(sum(expr[j][1][g] for j in S)*v[g] for g in range(d))
    cuts=[]
    for j in range(len(used)):
        vals=[val([j],v) for v in V]; mn,mx=min(vals),max(vals)
        if mn!=math.ceil(mn): cuts.append(([expr[j][1][g] for g in range(d)], math.ceil(mn)-expr[j][0]))
        if mx!=math.floor(mx): cuts.append(([-expr[j][1][g] for g in range(d)], expr[j][0]-math.floor(mx)))
    nu=len(used)
    for k in range(t+1):
        for drop in itertools.combinations(range(nu),k):
            S=[j for j in range(nu) if j not in drop]; mn=min(val(S,v) for v in V)
            if mn!=math.ceil(mn): cuts.append(([sum(expr[j][1][g] for j in S) for g in range(d)], math.ceil(mn)-sum(expr[j][0] for j in S)))
    if d==1:
        lo=min(v[0] for v in V); hi=max(v[0] for v in V)
        for a,b in cuts:
            if a[0]>0: lo=max(lo,b/a[0])
            elif a[0]<0: hi=min(hi,b/a[0])
            elif b>0: return "empty"
            if lo>hi: return "empty"
        return "nonempty"
    cx=sum(v[0] for v in V)/len(V); cy=sum(v[1] for v in V)/len(V)
    poly=sorted(V,key=lambda v: math.atan2(float(v[1]-cy),float(v[0]-cx)))
    for a,b in cuts:
        poly=clip(poly,a,b)
        if not poly: return "empty"
    return "nonempty"
res=collections.Counter(); fails=[]
for trial in range(int(sys.argv[2]) if len(sys.argv)>2 else 400):
    core=random.choice(B if trial%2==0 else A); cl=[tuple(x) for x in core["clauses"]]; nv=8
    for _ in range(random.randint(1,3)):           # k new variables, two clauses each, attached to existing variables
        y=nv; nv+=1
        for _ in range(2):
            a,b=random.sample(range(y),2); cl.append(tuple(sorted((y,a,b))))
    cl=sorted(set(cl))
    for t in (0,1,2,3):
        out=family_empty(cl,t)
        if out in ("skip_d","rational_infeasible","point"): res[out]+=1; break
        if out=="empty": res[("B" if trial%2==0 else "A", "t", t)]+=1; break
    else:
        res[("B" if trial%2==0 else "A","FAIL_t<=3")]+=1
        if len(fails)<20: fails.append({"core":core["clauses"],"whole":cl})
print(dict(res)); json.dump({"res":{str(k):v for k,v in res.items()},"fails":fails}, open("discover_whole.out.json","w"))
