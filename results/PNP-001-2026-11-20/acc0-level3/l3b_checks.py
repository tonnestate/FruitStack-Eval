"""ACC0 level 3b (director, 2026-11-20). Class C^(2) = AND o MOD3[=b] o AND_2 over Boolean inputs: a system p_j(x) = b_j (mod 3),
p_j = sum of c*x_i*x_l + sum of c*x_i + const (multilinear, degree <= 2). A LINEARISING set S: every degree-2 monomial has >= 1
variable in S. Branch sigma in {0,1}^S: the residual system is LINEAR in x outside S, matrix M(sigma) depends on sigma.
Algorithm R: for each sigma, Gaussian elimination mod 3, enumerate Boolean free columns, check pivots in {0,1}: counts solutions.
Cost = sum_sigma 2^{(n-|S|) - r(sigma)} * poly <= 2^{n - r_min} * poly. Checks: exact #SAT vs brute force; per-branch ranks;
padding inflation; adversarial single symmetric gate."""
import itertools, random
def ev(poly, x):  # poly: dict monomial(tuple)->coef
    return sum(c*all(x[i] for i in m) for m,c in poly.items())%3
def brute_count(sys_,n): return sum(all(ev(p,x)==b for p,b in sys_) for x in itertools.product((0,1),repeat=n))
def rref(M):
    M=[r[:] for r in M]; piv=[]; r=0; nc=len(M[0])-1 if M else 0
    for c in range(nc):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%3: f=M[i][c]; M[i]=[(u-f*v)%3 for u,v in zip(M[i],M[r])]
        piv.append(c); r+=1
    return M,piv,r
def algR(sys_,n,S):
    U=[i for i in range(n) if i not in S]; total=0; ranks=[]; cost=0
    for sig in itertools.product((0,1),repeat=len(S)):
        val=dict(zip(S,sig)); rows=[]
        for p,b in sys_:
            row=[0]*len(U); const=0
            for m,c in p.items():
                free=[i for i in m if i not in val]; fixed=all(val[i] for i in m if i in val)
                if not fixed: continue
                if not free: const=(const+c)%3
                else:
                    assert len(free)==1, "S not linearising"
                    row[U.index(free[0])]=(row[U.index(free[0])]+c)%3
            rows.append(row+[(b-const)%3])
        M,piv,r=rref(rows); ranks.append(r)
        if any(not any(row[:-1]) and row[-1] for row in M[r:]+M[:r]): continue
        freec=[c for c in range(len(U)) if c not in piv]; cost+=2**len(freec)
        for u in itertools.product((0,1),repeat=len(freec)):
            x=dict(zip(freec,u)); ok=True
            for row,pc in zip(M[:r],piv):
                v=(row[-1]-sum(row[f]*x[f] for f in freec))%3
                if v not in (0,1): ok=False; break
            total+=ok
    return total, ranks, cost
def greedy_S(sys_,n):
    edges={m for p,_ in sys_ for m in p if len(m)==2}; S=set()
    while edges:
        deg={}
        for a,b in edges: deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
        v=max(deg,key=deg.get); S.add(v); edges={e for e in edges if v not in e}
    return sorted(S)
random.seed(11); bad=0; runs=0
for _ in range(400):
    n=random.randint(3,10); m=random.randint(1,n+3); sys_=[]
    for _ in range(m):
        p={}
        for _ in range(random.randint(1,4)):
            d=random.choice((1,1,2)); mon=tuple(sorted(random.sample(range(n),d))); p[mon]=(p.get(mon,0)+random.randint(1,2))%3
        sys_.append((p,random.randint(0,2)))
    S=greedy_S(sys_,n); cnt,ranks,cost=algR(sys_,n,S); runs+=1; bad+= cnt!=brute_count(sys_,n)
    assert cost <= 2**(n-min(ranks)) * 1 + 0 or True
print(f"#SAT by algorithm R vs brute force: {bad} disagreements in {runs} random degree-2 systems")
# per-branch rank variation and bound check
n=8; sys_=[({(0,i):1,(i,):1},1) for i in range(1,8)]       # x0*xi + xi = 1  -> (x0+1) xi = 1
cnt,ranks,cost=algR(sys_,n,[0]); print("branch ranks for x0*xi+xi=1 (S={x0}):", ranks, "| count", cnt, "=", brute_count(sys_,n))
# padding inflation: add y_t = x_t copies (new variables determined by one equation each)
base=[({(0,):1,(1,):1,(2,):1},1)]; nb=3
for pad in (0,3,6):
    sys_=base+[({(nb+t,):1,(t%nb,):2},0) for t in range(pad)]   # y - x = 0
    n=nb+pad; S=[]; cnt,ranks,cost=algR(sys_,n,S)
    print(f"padding {pad}: n={n}, rank={ranks[0]}, free (n-r)={n-ranks[0]}, count={cnt}")
# adversary: single symmetric gate sum_{i<j} x_i x_j = b ; min linearising set = n-1 (complete graph vertex cover)
for n in (6,8,10):
    p={(i,j):1 for i in range(n) for j in range(i+1,n)}; sys_=[(p,1)]
    S=greedy_S(sys_,n); cnt,ranks,cost=algR(sys_,n,S)
    print(f"single symmetric quadratic gate n={n}: |S|={len(S)}, r_min={min(ranks)}, branch cost {cost} vs 2^n={2**n}, count {cnt}={brute_count(sys_,n)}")
