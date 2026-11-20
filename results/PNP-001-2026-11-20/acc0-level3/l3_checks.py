"""ACC0 level 3 (director, 2026-11-20): exact checks of three elementary statements.
(E) positive 1-in-3 clause (a,b,c) over Boolean x  <=>  x_a+x_b+x_c = 1 (mod 3)   [sum in {0..3}; = 1 mod 3 iff sum = 1]
(M) GF(3)-Lin-01-SAT (A x = b mod 3, x in {0,1}^n) is decided exactly by meet-in-the-middle on syndromes in O*(2^{n/2})
(F) ... and exactly by enumerating Boolean values of the n-rank free columns, computing pivots mod 3, checking pivots in {0,1}: O*(2^{n-rank})
(O) the Boolean set {x != 0} (OR_n) is not Boolean-cube intersect GF(3)-affine subspace for any n >= 2 (affine hull of OR's ones contains 0)"""
import itertools, random
def brute(A,b,n): return any(all(sum(r[i]*x[i] for i in range(n))%3==bb for r,bb in zip(A,b)) for x in itertools.product((0,1),repeat=n))
def mitm(A,b,n):
    h=n//2; L={}
    for xl in itertools.product((0,1),repeat=h): L.setdefault(tuple(sum(r[i]*xl[i] for i in range(h))%3 for r in A),xl)
    for xr in itertools.product((0,1),repeat=n-h):
        need=tuple((bb-sum(r[h+i]*xr[i] for i in range(n-h)))%3 for r,bb in zip(A,b))
        if need in L: return True
    return False
def rref3(A,b,n):
    M=[list(r)+[bb] for r,bb in zip(A,b)]; piv=[]; r=0
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%3: f=M[i][c]; M[i]=[(u-f*v)%3 for u,v in zip(M[i],M[r])]
        piv.append(c); r+=1
    if any(not any(row[:n]) and row[n] for row in M): return None
    return M[:r],piv
def freeenum(A,b,n):
    R=rref3(A,b,n)
    if R is None: return False
    M,piv=R; free=[c for c in range(n) if c not in piv]
    for u in itertools.product((0,1),repeat=len(free)):
        x=dict(zip(free,u)); ok=True
        for row,p in zip(M,piv):
            v=(row[n]-sum(row[f]*x[f] for f in free))%3
            if v not in (0,1): ok=False; break
        if ok: return True
    return False
random.seed(7); bad=0; tot=0; sat=0
for _ in range(1500):
    n=random.randint(3,11); r=random.randint(1,n+2)
    if random.random()<0.5:   # positive 1-in-3 instances via (E)
        cl=[random.sample(range(n),3) for _ in range(r)]; A=[[1 if i in c else 0 for i in range(n)] for c in cl]; b=[1]*r
        assert brute(A,b,n)==any(all(sum(x[i] for i in c)==1 for c in cl) for x in itertools.product((0,1),repeat=n))   # (E)
    else:
        A=[[random.randint(0,2) for _ in range(n)] for _ in range(r)]; b=[random.randint(0,2) for _ in range(r)]
    t=brute(A,b,n); sat+=t; tot+=1; bad+= (mitm(A,b,n)!=t) + (freeenum(A,b,n)!=t)
print(f"(E) exact on all 1-in-3 instances; (M),(F) disagreements with brute force: {bad} of {2*tot} runs ({sat} SAT, {tot-sat} UNSAT)")
def affine_hull_contains_zero(S,n):
    # GF(3) affine hull of S contains 0 iff 0 = sum c_i s_i with sum c_i = 1 (mod 3): linear system over GF(3)
    A=[[s[i] for s in S] for i in range(n)]+[[1]*len(S)]; b=[0]*n+[1]
    return rref3(A,b,len(S)) is not None
for n in range(2,8):
    S=[x for x in itertools.product((0,1),repeat=n) if any(x)]
    print(f"(O) n={n}: affine hull over GF(3) of OR_n's ones contains 0: {affine_hull_contains_zero(S,n)}")
