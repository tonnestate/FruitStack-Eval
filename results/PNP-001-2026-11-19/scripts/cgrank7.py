"""Exact (rational) CG-rank-1 certificate for every minimal GAP core on n<=7 variables.
Certificate: a variable j with 0 < min_P x_j and max_P x_j < 1 on P = {x : A x = 1, 0 <= x <= 1} (CG cuts x_j >= 1 and x_j <= 0 then clash)."""
import itertools, numpy as np, json, collections
from fractions import Fraction as Fr
n=7; T=list(itertools.combinations(range(n),3)); k=len(T)
def masks(vals, ok): return np.array(sorted({sum(1<<i for i,t in enumerate(T) if ok(sum(x[j] for j in t))) for x in itertools.product(vals,repeat=n)}),dtype=np.int64)
B=masks((0,1),lambda s:s==1); G=masks((0,1,2),lambda s:s%3==1)
def cov(F,M):
    o=np.zeros(F.size,bool)
    for m in M: o|=(F&~m)==0
    return o
cores=[]
for m in (5,6):
    F=np.array([sum(1<<i for i in c) for c in itertools.combinations(range(k),m)],dtype=np.int64)
    bl=F[cov(F,G)&~cov(F,B)]; mn=np.ones(bl.size,bool)
    for i in range(k):
        bit=np.int64(1<<i); h=(bl&bit)!=0
        if h.any(): mn[np.where(h)[0][~cov(bl[h]&~bit,B)]]=False
    cores+= [int(f) for f in bl[mn]]
def rref(M):                                  # exact RREF over Q, returns (R, pivots)
    M=[row[:] for row in M]; piv=[]; r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=M[r][c]; M[r]=[v/inv for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0: f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
    return M[:r], piv
stats=collections.Counter(); fails=[]
for f in cores:
    cl=[T[i] for i in range(k) if (f>>i)&1]
    used=sorted({v for c in cl for v in c}); nu=len(used)
    Aug=[[Fr(1 if u in c else 0) for u in used]+[Fr(1)] for c in cl]
    R,piv=rref(Aug)
    if len(piv) and piv[-1]==nu: stats["rational_infeasible"]+=1; continue
    freev=[j for j in range(nu) if j not in piv]; d=len(freev)
    # x_piv = rhs - sum coeff * x_free ; x_free = t
    expr={}
    for row,p in zip(R,piv): expr[p]=(row[nu], {fv:-row[fv] for fv in freev})
    for fv in freev: expr[fv]=(Fr(0),{g:(Fr(1) if g==fv else Fr(0)) for g in freev})
    # constraints 0 <= c0 + sum a_g t_g <= 1  as list of (a_vec, b): a.t >= b
    cons=[]
    for j in range(nu):
        c0,a=expr[j]; av=[a[g] for g in freev]
        cons.append((av, -c0)); cons.append(([-x for x in av], c0-1))
    # vertices of the polytope in t-space (d <= 2): intersect d constraints, keep feasible
    verts=[]
    for S in itertools.combinations(range(len(cons)), d):
        if d==0: verts=[[]]; break
        M=[ [*cons[i][0], cons[i][1]] for i in S]
        Rm,pv=rref(M)
        if len(pv)<d or (pv and pv[-1]==d): continue
        t=[Rm[r][d] for r in range(d)]
        if all(sum(a*b for a,b in zip(av,t))>=bb for av,bb in cons): verts.append(t)
    if not verts: stats["empty_P"]+=1; continue
    cert=None
    for j in range(nu):
        c0,a=expr[j]; vals=[c0+sum(a[g]*t[i] for i,g in enumerate(freev)) for t in verts]
        if min(vals)>0 and max(vals)<1: cert=(used[j],min(vals),max(vals)); break
    if cert: stats[f"rank1_cert_d{d}"]+=1
    else: stats[f"NO_simple_cert_d{d}"]+=1; fails.append(cl)
print(len(cores),"cores", dict(stats)); print("examples without simple certificate:", fails[:3])
json.dump({"cores":len(cores),"stats":stats,"fails":fails[:50]}, open("cgrank7.out.json","w"))
