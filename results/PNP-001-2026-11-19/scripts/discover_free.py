"""Point 3, meaningful form: core (n=8, minimal GAP) + k 'free' attachments: each new clause (y1, y2, a) with fresh y1, y2 and a core variable a.
This adds one LP degree of freedom per attachment (y1 + y2 = 1 - x_a always satisfiable) without constraining the core, but shifts every
covering sum that contains y1, y2. Cheap family F_t on the WHOLE formula: single-variable cuts on all variables + covering cuts over
V(F) minus <= t variables. Emptiness of P cap cuts decided exactly: an LP solver proposes a Farkas certificate y >= 0, y^T M = 0, y^T h < 0
for the system M t <= h in the free coordinates; it is rationalised and VERIFIED in exact arithmetic (otherwise 'undecided').
Cut right-hand sides need exact min over P: vertices of P in free coordinates are enumerated exactly (d small)."""
import json, itertools, math, random, collections, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
src=open("cgrank_n.py").read().split('res={"n":n')[0].replace("n=int(sys.argv[1]); KMAX=int(sys.argv[2]) if len(sys.argv)>2 else 2","n=8; KMAX=1")
ns={}; exec(src, ns); setup, vertices = ns["setup"], ns["vertices"]
seed=int(sys.argv[1]); N=int(sys.argv[2]); KATT=int(sys.argv[3]); random.seed(seed)
r=json.load(open("cgrank_n8.json")); cores=r["cores"]
def exact_empty(rows):                 # rows: list of (a(list Fr), b Fr) meaning a.t >= b ; returns True (verified empty) / False (feasible) / None
    d=len(rows[0][0]); M=np.array([[-float(x) for x in a] for a,b in rows]); h=np.array([-float(b) for a,b in rows])   # -a.t <= -b
    feas=linprog(np.zeros(d), A_ub=M, b_ub=h, bounds=[(None,None)]*d, method="highs")
    if feas.status==0: return False
    k=len(rows); res=linprog(np.zeros(k), A_eq=np.vstack([M.T, h.reshape(1,-1)]), b_eq=np.append(np.zeros(d), -1.0), bounds=[(0,None)]*k, method="highs")
    if res.status!=0: return None
    y=[Fr(v).limit_denominator(10**6) for v in res.x]
    if all(sum(y[i]*(-rows[i][0][g]) for i in range(k))==0 for g in range(d)) and sum(y[i]*(-rows[i][1]) for i in range(k))<0 and all(v>=0 for v in y):
        return True
    # repair: exact nullspace on the support
    sup=[i for i in range(k) if res.x[i]>1e-9]
    Rm,pv=ns["rref"]([[ -rows[i][0][g] for i in sup] for g in range(d)])
    return None
def family(cl,t):
    s=setup(cl)
    if s is None: return "rational_infeasible", None
    used,d,expr,base=s
    if d>8: return "skip_d", d
    V=vertices(base,d)
    def val(S,v): return sum(expr[j][0] for j in S)+sum(sum(expr[j][1][g] for j in S)*v[g] for g in range(d))
    rows=list(base)
    for j in range(len(used)):
        vals=[val([j],v) for v in V]; mn,mx=min(vals),max(vals)
        if mn!=math.ceil(mn): rows.append(([expr[j][1][g] for g in range(d)], math.ceil(mn)-expr[j][0]))
        if mx!=math.floor(mx): rows.append(([-expr[j][1][g] for g in range(d)], expr[j][0]-math.floor(mx)))
    nu=len(used)
    for k in range(t+1):
        for drop in itertools.combinations(range(nu),k):
            S=[j for j in range(nu) if j not in drop]; mn=min(val(S,v) for v in V)
            if mn!=math.ceil(mn): rows.append(([sum(expr[j][1][g] for j in S) for g in range(d)], math.ceil(mn)-sum(expr[j][0] for j in S)))
    return exact_empty(rows), d
out=collections.Counter(); examples=[]
for trial in range(N):
    core=random.choice([c for c in cores if c["cert"]["kind"]=="B_cut_set"] if len(sys.argv)>4 else cores); cl=[tuple(x) for x in core["clauses"]]; nv=8; kind=core["cert"]["kind"][0]
    corevars=sorted({v for c in cl for v in c})
    for _ in range(KATT):
        a=random.choice(corevars); cl.append((a,nv,nv+1)); nv+=2
    for t in (0,1,2):
        e,d=family(cl,t)
        if e is True: out[(kind,KATT,"t",t)]+=1; break
        if e in ("skip_d","rational_infeasible") or e is None: out[(kind,KATT,str(e))]+=1; break
    else:
        out[(kind,KATT,"FAIL_t<=2")]+=1
        if len(examples)<10: examples.append(cl)
print(dict(out)); json.dump({"seed":seed,"KATT":KATT,"res":{str(k):v for k,v in out.items()},"fail_examples":examples}, open(f"discover_free_k{KATT}.out.json","w"))
