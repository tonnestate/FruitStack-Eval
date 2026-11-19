"""CG rank of minimal GAP cores at n = 8 via the D-018 witness generator (owner 2026-11-19).
Every minimal GAP core F has a GF(3) solution using all three values; permuting variables and shifting values maps it into the clauses allowed by
one of the 7 value-count types (k0,k1,k2) (all >= 1, sum 8, up to cyclic shift). So enumerating subsets (size <= 7, by T44 C4) of each type's
allowed set finds every core up to isomorphism. For each core: exact rational vertex enumeration of P = {Ax = 1, 0 <= x <= 1}; simple rank-1
certificate = a variable strictly inside (0,1) on P. Cores without it are written out for a full first-closure check."""
import itertools, json, collections, sys, time
from fractions import Fraction as Fr
n=8; t0=time.time(); OUT="/root/fruits/research/PNP-001/lab/review-2026-11-19/cgrank8.out.json"
types=set()
for k0 in range(1,n):
    for k1 in range(1,n-k0):
        k2=n-k0-k1
        if k2>=1: types.add(min([(k0,k1,k2),(k2,k0,k1),(k1,k2,k0)]))
types=sorted(types)
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
def certificate(cl):
    used=sorted({v for c in cl for v in c}); nu=len(used)
    R,piv=rref([[Fr(1 if u in c else 0) for u in used]+[Fr(1)] for c in cl])
    if piv and piv[-1]==nu: return "rational_infeasible"
    freev=[j for j in range(nu) if j not in piv]; d=len(freev)
    expr={p:(row[nu],[-row[fv] for fv in freev]) for row,p in zip(R,piv)}
    for i,fv in enumerate(freev): expr[fv]=(Fr(0),[Fr(1) if g==i else Fr(0) for g in range(d)])
    cons=[]
    for j in range(nu):
        c0,a=expr[j]; cons.append((a,-c0)); cons.append(([-x for x in a],c0-1))
    verts=[]
    if d==0: verts=[[]]
    for S in itertools.combinations(range(len(cons)),d):
        if d==0: break
        Rm,pv=rref([[*cons[i][0],cons[i][1]] for i in S])
        if len(pv)<d or (pv and pv[-1]==d): continue
        t=[Rm[r][d] for r in range(d)]
        if all(sum(x*y for x,y in zip(av,t))>=bb for av,bb in cons): verts.append(t)
    for j in range(nu):
        c0,a=expr[j]; vals=[c0+sum(x*y for x,y in zip(a,t)) for t in verts]
        if min(vals)>0 and max(vals)<1: return f"cert_d{d}"
    return f"NO_simple_cert_d{d}"
stats=collections.Counter(); fails=[]; ncores=0
for (k0,k1,k2) in types:
    val=[0]*k0+[1]*k1+[2]*k2
    allowed=[c for c in itertools.combinations(range(n),3) if sum(val[v] for v in c)%3==1]
    X=list(itertools.product((0,1),repeat=n))
    satmask=[sum(1<<i for i,c in enumerate(allowed) if sum(x[v] for v in c)==1) for x in X]
    def is_sat(mask): return any(mask & ~s == 0 for s in satmask)
    nt=0
    for m in range(1,min(7,len(allowed))+1):
        for comb in itertools.combinations(range(len(allowed)),m):
            mask=sum(1<<i for i in comb)
            if is_sat(mask): continue
            if any(not is_sat(mask & ~(1<<i)) for i in comb): continue      # not minimal
            ncores+=1; nt+=1
            res=certificate([allowed[i] for i in comb]); stats[res]+=1
            if res.startswith("NO_"): fails.append([allowed[i] for i in comb])
    print(f"type {(k0,k1,k2)}: allowed {len(allowed)}, cores {nt}, elapsed {time.time()-t0:.0f}s, stats {dict(stats)}", flush=True)
    json.dump({"n":n,"types_done":types[:types.index((k0,k1,k2))+1],"cores_found":ncores,"stats":stats,"fails":fails}, open(OUT,"w"))
print("DONE", ncores, dict(stats), flush=True)
