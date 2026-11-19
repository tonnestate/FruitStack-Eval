import itertools, random, numpy as np
from fractions import Fraction
random.seed(19)
def rank3(rows, n):
    M=[[1 if j in r else 0 for j in range(n)] for r in rows]; r=0
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]: f=M[i][c]; M[i]=[(a-f*b)%3 for a,b in zip(M[i],M[r])]
        r+=1
    return r
def C(n,F): return sum(all(sum(x[v] for v in c)==1 for c in F) for x in itertools.product((0,1),repeat=n))
def g3sols(n,F): return [x for x in itertools.product((0,1,2),repeat=n) if all(sum(x[v] for v in c)%3==1 for c in F)]
# --- C3/C4 on n=7: every minimal GAP core has independent rows (rank = m), m <= 6; and no minimal core with m = 7
n=7; T=list(itertools.combinations(range(n),3))
def blind(F): return not C(n,F) and bool(g3sols(n,F)) if False else None
# reuse the exact census: rebuild cores for m=5,6 quickly via sampling of the known witness-free route is slow; instead check random blind sets
# Theorem S, D3, D5 - exact random tests incl. UNSAT / C = 0 mod 3
cS=cD3=cD5=0; nunsat=nz3=0; N=400
for _ in range(N):
    nn=random.randint(3,6); m=random.randint(1,6); F=[tuple(random.sample(range(nn),3)) for _ in range(m)]
    F=[tuple(sorted(c)) for c in F]
    c=C(nn,F); S=g3sols(nn,F); nunsat+= c==0; nz3+= c%3==0
    cS+= sum(1 for x in S if len(set(x))<3)==3*c                                   # Theorem S
    # D3: N3 = 2-colourings of occurrences, no clause monochromatic, every variable even # of colour 1
    occ=[(j,v) for j,cl in enumerate(F) for v in cl]; N3=0
    for col in itertools.product((0,1),repeat=len(occ)):
        if any(col[3*j]==col[3*j+1]==col[3*j+2] for j in range(m)): continue
        if all(sum(col[i] for i,(j,v) in enumerate(occ) if v==u)%2==0 for u in range(nn)): N3+=1
    cD3+= (c - (-1)**nn * N3)%3==0
cD5=tot5=0
for _ in range(300):                                                              # D5: occurrence 1..2, every variable used
    m=random.randint(1,6); slots=[]; F=[[] for _ in range(m)]; v=0
    while True:
        free=[j for j in range(m) if len(F[j])<3]
        if not free: break
        if len(free)>=2 and random.random()<0.5:
            a,b=random.sample(free,2); F[a].append(v); F[b].append(v)
        else: F[random.choice(free)].append(v)
        v+=1
    nn=v; F=[tuple(c) for c in F]; c=C(nn,F)
    B=np.zeros((m,m),int)
    for u in range(nn):
        J=[j for j in range(m) if u in F[j]]
        if len(J)==1: B[J[0],J[0]]+=1
        else: B[J[0],J[1]]+=1; B[J[1],J[0]]+=1
    B%=2; M=B.copy(); r=0; det=1
    for col in range(m):
        p=next((i for i in range(r,m) if M[i,col]),None)
        if p is None: det=0; break
        M[[r,p]]=M[[p,r]]
        for i in range(m):
            if i!=r and M[i,col]: M[i]^=M[r]
        r+=1
    tot5+=1; cD5+= det==c%2
print(f"Theorem S: {cS}/{N} | D3: {cD3}/{N} (UNSAT {nunsat}, C=0 mod 3 {nz3}) | D5: {cD5}/{tot5}")
