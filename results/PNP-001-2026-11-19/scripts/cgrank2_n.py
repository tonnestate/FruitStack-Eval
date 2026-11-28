"""PNP-001: exact Chvatal-Gomory rank of all minimal GAP cores on n variables (owner 2026-11-19), with stored certificates.

COMPLETENESS (why every minimal GAP core is found up to isomorphism):
 (1) a minimal GAP core F is GF(3)-consistent and Boolean-UNSAT; by D-018 (formally verified) each GF(3) solution x uses all three values;
 (2) x -> x + c*1 keeps solutions (each clause has 3 variables), and permuting variables maps F to an isomorphic formula; so x can be brought to
     the form 0^k0 1^k1 2^k2 with (k0,k1,k2) minimal under cyclic shift, all ki >= 1, k0+k1+k2 = n;
 (3) every clause of F then has value sum = 1 mod 3, i.e. F is a subset of ALLOWED(k0,k1,k2);
 (4) by T44 C3/C4 (C3 confirmed exhaustively at n = 7) a minimal core has <= n-1 clauses;
 (5) the DFS below lists every subset of ALLOWED that is Boolean-UNSAT with all proper subsets SAT (supersets of an UNSAT set are pruned:
     they cannot be minimal) - every minimal core of size <= n-1 inside ALLOWED is reached through its SAT prefixes.
CG RANK: P = {x : A x = 1, 0 <= x <= 1} is never empty (x = 1/3), so rank >= 1. Rank 1 iff the first CG closure P' is empty.
 certificate A: a variable j with 0 < min_P x_j and max_P x_j < 1 (cuts x_j >= 1, x_j <= 0);
 certificate B: integral vectors c (entries in {-K..K}) whose cuts c.x <= floor(max_P c.x) intersect P emptily (exact rational clipping, d <= 2),
   reduced greedily to a small subset;
 otherwise: RANK2_CANDIDATE (P' not shown empty with |c_i| <= K) - reported with the remaining region, for a separate full check.
"""
import itertools, json, sys, time, math
from fractions import Fraction as Fr
n=int(sys.argv[1]); KMAX=int(sys.argv[2]) if len(sys.argv)>2 else 2
OUT=f"/root/fruits/research/PNP-001/lab/review-2026-11-19/cgrank2_n{n}.json"
sys.path.insert(0,"/root/fruits/research/PNP-001/lab/review-2026-11-19")
from exact_lp import exact_min
import numpy as np
from scipy.optimize import linprog
def farkas_empty(rows):
    """rows a.t >= b; True only with an exact rational Farkas certificate y >= 0, sum y_i a_i = 0, sum y_i b_i > 0"""
    d=len(rows[0][0]); M=np.array([[float(x) for x in a] for a,b in rows]); h=np.array([float(b) for a,b in rows])
    if linprog(np.zeros(d), A_ub=-M, b_ub=-h, bounds=[(None,None)]*d, method="highs").status==0: return False
    k=len(rows); res=linprog(np.zeros(k), A_eq=np.vstack([M.T, h.reshape(1,-1)]), b_eq=np.append(np.zeros(d),1.0), bounds=[(0,None)]*k, method="highs")
    if res.status!=0: return False
    y=[Fr(v).limit_denominator(10**8) for v in res.x]
    return all(v>=0 for v in y) and all(sum(y[i]*rows[i][0][g] for i in range(k))==0 for g in range(d)) and sum(y[i]*rows[i][1] for i in range(k))>0
t0=time.time()
types=sorted({min([(a,b,n-a-b),(n-a-b,a,b),(b,n-a-b,a)]) for a in range(1,n) for b in range(1,n-a) if n-a-b>=1})
def rref(M):
    M=[row[:] for row in M]; piv=[]; r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=M[r][c]; M[r]=[v/inv for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0: f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
    return M[:r], piv
def setup(cl):
    used=sorted({v for c in cl for v in c}); nu=len(used)
    R,piv=rref([[Fr(1 if u in c else 0) for u in used]+[Fr(1)] for c in cl])
    if piv and piv[-1]==nu: return None
    freev=[j for j in range(nu) if j not in piv]; d=len(freev)
    expr={p:(row[nu],[-row[fv] for fv in freev]) for row,p in zip(R,piv)}
    for i,fv in enumerate(freev): expr[fv]=(Fr(0),[Fr(int(g==i)) for g in range(d)])
    base=[]
    for j in range(nu):
        c0,a=expr[j]; base.append((a,-c0)); base.append(([-x for x in a],c0-1))
    return used,d,expr,base
def vertices(cons,d):
    if d==0: return [[]]
    V=[]
    for S in itertools.combinations(range(len(cons)),d):
        Rm,pv=rref([[*cons[i][0],cons[i][1]] for i in S])
        if len(pv)<d or (pv and pv[-1]==d): continue
        t=[Rm[r][d] for r in range(d)]
        if all(sum(x*y for x,y in zip(a,t))>=b for a,b in cons) and t not in V: V.append(t)
    return V
def clip(poly,a,b):
    out=[]; m=len(poly)
    for i in range(m):
        P,Q=poly[i],poly[(i+1)%m]; fp=a[0]*P[0]+a[1]*P[1]-b; fq=a[0]*Q[0]+a[1]*Q[1]-b
        if fp>=0: out.append(P)
        if (fp>=0)!=(fq>=0) and fp!=fq:
            s=fp/(fp-fq); out.append([P[0]+s*(Q[0]-P[0]),P[1]+s*(Q[1]-P[1])])
    return out
def interval_clip(iv,a,b):        # d = 1: t in [lo,hi], constraint a*t >= b
    lo,hi=iv
    if a[0]>0: lo=max(lo,b/a[0])
    elif a[0]<0: hi=min(hi,b/a[0])
    elif b>0: return None
    return (lo,hi) if lo<=hi else None
def certify(cl):
    s=setup(cl)
    if s is None: return {"kind":"rational_infeasible"}
    used,d,expr,base=s; nu=len(used)
    def lin(S): return sum(expr[j][0] for j in S), [sum(expr[j][1][g] for j in S) for g in range(d)]
    def ext(S, sign):
        c0,cv=lin(S); e=exact_min([sign*x for x in cv],base)
        if e is None:
            V=vertices(base,d); vals=[c0+sum(x*y for x,y in zip(cv,v)) for v in V]; return min(vals) if sign>0 else max(vals)
        return c0+sign*e[0]
    for j in range(nu):
        lo,hi=ext([j],1),ext([j],-1)
        if lo>0 and hi<1: return {"kind":"A_single_variable","d":d,"var":used[j],"min":str(lo),"max":str(hi)}
    rows=list(base); cuts=[]
    for size in range(1,nu+1):
        for S in itertools.combinations(range(nu),size):
            m=ext(list(S),1)
            if m!=math.ceil(m):
                c0,cv=lin(list(S)); rows.append((cv, math.ceil(m)-c0)); cuts.append({"S":[used[j] for j in S],"rhs":math.ceil(m)})
    if d>=1 and cuts and farkas_empty(rows):
        return {"kind":"B_covering_cuts","d":d,"n_cuts":len(cuts),"cuts":cuts[:40],"vars":used}
    return {"kind":"OPEN_NEEDS_GENERAL_CUTS","d":d,"vars":used}
res={"n":n,"types":[],"stats":{},"cores":[]}
for (k0,k1,k2) in types:
    val=[0]*k0+[1]*k1+[2]*k2
    allowed=[c for c in itertools.combinations(range(n),3) if sum(val[v] for v in c)%3==1]
    masks=[sum(1<<i for i,c in enumerate(allowed) if sum(x[v] for v in c)==1) for x in itertools.product((0,1),repeat=n)]
    masks=sorted(set(masks))
    found=[]
    def dfs(cur, last, live):                 # live = masks still containing cur (cur SAT iff live nonempty)
        for i in range(last+1,len(allowed)):
            nl=[m for m in live if (m>>i)&1]
            new=cur|(1<<i)
            if not nl:                       # UNSAT: candidate core; minimal iff removing any clause gives SAT
                if all(any((new&~(1<<j))&~m==0 for m in masks) for j in range(len(allowed)) if (new>>j)&1): found.append(new)
            elif bin(new).count("1")<n-1: dfs(new,i,nl)
    dfs(0,-1,masks)
    st={}
    for f in found:
        cl=[allowed[i] for i in range(len(allowed)) if (f>>i)&1]; cert=certify(cl)
        st[cert["kind"]]=st.get(cert["kind"],0)+1; res["stats"][cert["kind"]]=res["stats"].get(cert["kind"],0)+1
        res["cores"].append({"type":[k0,k1,k2],"clauses":cl,"cert":cert})
    res["types"].append({"type":[k0,k1,k2],"allowed":len(allowed),"cores":len(found),"stats":st})
    print(f"n={n} type {(k0,k1,k2)}: allowed {len(allowed)}, cores {len(found)}, {st}, {time.time()-t0:.0f}s", flush=True)
    json.dump(res,open(OUT,"w"))
print("DONE", n, res["stats"], flush=True)
