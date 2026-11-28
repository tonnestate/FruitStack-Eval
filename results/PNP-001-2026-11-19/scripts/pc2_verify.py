"""Independent degree-2 polynomial calculus check over GF(2) mod x^2 = x (director, 2026-11-19).
V_0 = span{L_j, q_i}; V_{t+1} = span(V_t u {x_k * p : p in V_t of degree <= 1}); refuted iff 1 in the fixpoint. Dense numpy elimination with
quadratic columns first, so rows of the echelon form without quadratic entries span V_t intersected with the degree<=1 space."""
import itertools, json, sys, numpy as np
core=json.loads(sys.argv[1]); n=1+max(v for c in core for v in c)
quad=list(itertools.combinations(range(n),2)); lin=[(i,) for i in range(n)]; cols=quad+lin+[()]; ix={m:i for i,m in enumerate(cols)}
def vec(terms):
    v=np.zeros(len(cols),dtype=np.uint8)
    for t in terms: v[ix[tuple(sorted(set(t)))]]^=1
    return v
def echelon(M):
    M=M.copy(); r=0
    for c in range(M.shape[1]):
        p=np.nonzero(M[r:,c])[0]
        if len(p)==0: continue
        p=p[0]+r; M[[r,p]]=M[[p,r]]; rows=np.nonzero(M[:,c])[0]; rows=rows[rows!=r]; M[rows]^=M[r]; r+=1
        if r==M.shape[0]: break
    return M[:r]
V=np.array([vec([(),(a,),(b,),(c,)]) for a,b,c in core]+[vec([(a,b),(a,c),(b,c)]) for a,b,c in core])
for it in range(50):
    E=echelon(V); low=[row for row in E if not row[:len(quad)].any()]
    new=[]
    for row in low:
        terms=[cols[i] for i in np.nonzero(row)[0]]
        for k in range(n): new.append(vec([t+(k,) for t in terms]))
    W=echelon(np.vstack([E]+new)) if new else E
    if W.shape[0]==E.shape[0]: break
    V=W
one=vec([()]); refuted=echelon(np.vstack([E,one])).shape[0]==E.shape[0]
print(f"vars {n}, clauses {len(core)}: degree-2 PC (mod x^2=x) refutes: {refuted} (fixpoint after {it} rounds, dim {E.shape[0]} of {len(cols)})")
