"""ACC0 level 3d (director, 2026-11-20): Theorem L (degree-1 projection identity) and the branch-sum criterion.
For a linear system M z = b over GF(3) (Boolean variables z, t of them), V = GF(3) solution space, S a subset of variables:
 (i)  the residual matrix of every branch sigma in {0,1}^S is the same (rank r_S constant over consistent branches);
 (ii) branch sigma is consistent iff sigma lies in pi_S(V);
 (iii) free dimension per consistent branch = t-|S|-r_S = dim V - dim pi_S(V);
 (iv) hence cost(S) = 2^|S| + |{0,1}^S cap pi_S(V)| * 2^(dim V - dim pi_S V) <= 2^|S| + 2^dim V.
Checked exactly by enumerating V (t <= 9)."""
import itertools, random
def rref(rows,nc):
    M=[list(r) for r in rows]; piv=[]; r=0
    for c in range(nc):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%3: f=M[i][c]; M[i]=[(u-f*v)%3 for u,v in zip(M[i],M[r])]
        piv.append(c); r+=1
    cons=not any(len(row)>nc and not any(row[:nc]) and row[nc]%3 for row in M)
    return r,cons
def dim_affine(pts):
    if not pts: return -1
    p0=pts[0]; return rref([[(a-b)%3 for a,b in zip(p,p0)] for p in pts[1:]] or [[0]*len(p0)],len(p0))[0]
random.seed(3); bad=0; runs=0
for _ in range(300):
    t=random.randint(3,9); m=random.randint(1,t); M=[[random.randint(0,2) for _ in range(t)] for _ in range(m)]
    b=[random.randint(0,2) for _ in range(m)]
    V=[z for z in itertools.product(range(3),repeat=t) if all(sum(a*x for a,x in zip(row,z))%3==bb for row,bb in zip(M,b))]
    if not V: continue
    S=sorted(random.sample(range(t),random.randint(0,t))); U=[i for i in range(t) if i not in S]
    ranks=set(); cost=2**len(S); ncons=0
    for sig in itertools.product((0,1),repeat=len(S)):
        rows=[[row[i] for i in U]+[(bb-sum(row[s]*v for s,v in zip(S,sig)))%3] for row,bb in zip(M,b)]
        r,cons=rref(rows,len(U)) if U else (0, all(x[-1]==0 for x in rows))
        if cons: ranks.add(r); ncons+=1; cost+=2**(len(U)-r)
    proj={tuple(z[i] for i in S) for z in V}; dV=dim_affine(V); dP=dim_affine(sorted(proj)) if S else 0
    Bool=sum(1 for p in proj if all(v in (0,1) for v in p))
    ok = len(ranks)<=1 and ncons==Bool and all(len(U)-r==dV-dP for r in ranks) and cost==2**len(S)+Bool*2**(dV-dP) and cost<=2**len(S)+2**dV
    bad+= not ok; runs+=1
print(f"Theorem L (i)-(iv): {bad} violations in {runs} random systems with nonempty V")
# branch-sum: average surplus large, one bad branch dominates (degree 2): x0*(x1+...+x_k)-style system, S={x0}
n=12
k=n-1; cost_good=2**(k-k); cost_bad=2**k     # branch x0=1: k independent equations; branch x0=0: none
print(f"branch-sum example n={n}: Delta_a = {k} and 0 (average {k/2}), cost {cost_good+cost_bad} vs 2^(n-|S|-avg)={2**(n-1-k//2)}: the worst branch decides")
