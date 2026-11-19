"""Independent check of one core (director, 2026-11-19): brute-force UNSAT/minimality, GF(3) consistency by enumeration of a solution,
and Nullstellensatz degree d over GF(2) (with and without x^2=x) via an independent dense-rank implementation (numpy, mod 2).
NS_d: 1 = sum g_i q_i + sum h_j L_j (+ sum b_k (x_k^2 - x_k) if boolean), deg g_i <= d-2, deg h_j <= d-1, deg b_k <= d-2."""
import itertools, sys, json, numpy as np
core=json.loads(sys.argv[1]); n=1+max(v for c in core for v in c)
sols=[x for x in itertools.product((0,1),repeat=n) if all(sum(x[i] for i in c)==1 for c in core)]
minimal=all(any(all(sum(x[i] for i in c)==1 for c in core[:j]+core[j+1:]) for x in itertools.product((0,1),repeat=n)) for j in range(len(core)))
def gf3():
    import itertools as it
    for x in it.product(range(3),repeat=n):
        if all(sum(x[i] for i in c)%3==1 for c in core): return x
print("vars",n,"clauses",len(core),"| Boolean solutions",len(sols),"| minimal UNSAT",minimal,"| GF(3) solution",gf3())
def monos(deg, boolean):
    out=[]
    for d in range(deg+1):
        for m in (itertools.combinations(range(n),d) if boolean else itertools.combinations_with_replacement(range(n),d)): out.append(m)
    return out
def mul(p,m,boolean):   # p: dict mono->1, m: mono tuple
    r={}
    for t in p:
        u=tuple(sorted(set(t)|set(m))) if boolean else tuple(sorted(t+m))
        r[u]=r.get(u,0)^1
    return {k for k,v in r.items() if v}
def ns(d, boolean):
    L=[{(),(a,),(b,),(c,)} for a,b,c in core]; Q=[{(a,b),(a,c),(b,c)} for a,b,c in core]
    gens=[mul(q,m,boolean) for q in Q for m in monos(d-2,boolean)]+[mul(l,m,boolean) for l in L for m in monos(d-1,boolean)]
    if not boolean: gens+=[ {tuple(sorted(m+(k,k))),tuple(sorted(m+(k,)))} for k in range(n) for m in monos(d-2,False)] if False else []
    allm=sorted({t for g in gens for t in g}|{()}); ix={t:i for i,t in enumerate(allm)}
    M=np.zeros((len(gens),len(allm)),dtype=np.uint8)
    for r,g in enumerate(gens):
        for t in g: M[r,ix[t]]=1
    def rank2(A):
        A=A.copy(); r=0
        for c in range(A.shape[1]):
            p=np.nonzero(A[r:,c])[0]
            if len(p)==0: continue
            p=p[0]+r; A[[r,p]]=A[[p,r]]
            rows=np.nonzero(A[:,c])[0]; rows=rows[rows!=r]; A[rows]^=A[r]; r+=1
            if r==A.shape[0]: break
        return r
    e=np.zeros((1,len(allm)),dtype=np.uint8); e[0,ix[()]]=1
    return rank2(np.vstack([M,e]))==rank2(M)
for d in (2,3):
    print(f"NS degree {d}: without Boolean axioms {ns(d,False)}, modulo x^2=x {ns(d,True)}")
