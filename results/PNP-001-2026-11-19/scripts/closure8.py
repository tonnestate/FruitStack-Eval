"""First Chvatal-Gomory closure of the n=8 cores WITHOUT a single-variable certificate (cgrank8.out.json 'fails').
For a rational polytope P and integral c, c.x <= floor(max_P c.x) is a rank-1 CG cut. P' (first closure) = P intersected with all of them.
Here P lies in a 2-dim affine plane x = x0 + N t; we collect cuts for all integral c with |c_i| <= K and decide emptiness of the 2-dim region exactly.
P' empty with these cuts  => CG rank 1 (certificate: the cuts used). Nonempty => rank >= 2 is possible only if larger c cannot empty it (report)."""
import json, itertools, sys
from fractions import Fraction as Fr
from math import floor, ceil
K=int(sys.argv[1]) if len(sys.argv)>1 else 1
data=json.load(open("cgrank8.out.json")); fails=data["fails"]
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
def polygon(cons):                 # vertices of {t in Q^2 : a.t >= b for (a,b) in cons}
    V=[]
    for (a1,b1),(a2,b2) in itertools.combinations(cons,2):
        det=a1[0]*a2[1]-a1[1]*a2[0]
        if det==0: continue
        t=[(b1*a2[1]-a1[1]*b2)/det, (a1[0]*b2-b1*a2[0])/det]
        if all(a[0]*t[0]+a[1]*t[1]>=b for a,b in cons): V.append(t)
    return V
def analyse(cl):
    used=sorted({v for c in cl for v in c}); nu=len(used)
    R,piv=rref([[Fr(1 if u in c else 0) for u in used]+[Fr(1)] for c in cl])
    freev=[j for j in range(nu) if j not in piv]; assert len(freev)==2
    expr={p:(row[nu],[-row[fv] for fv in freev]) for row,p in zip(R,piv)}
    for i,fv in enumerate(freev): expr[fv]=(Fr(0),[Fr(int(g==i)) for g in range(2)])
    base=[]
    for j in range(nu):
        c0,a=expr[j]; base.append((a,-c0)); base.append(([-a[0],-a[1]],c0-1))
    V=polygon(base)
    cuts=[]
    for c in itertools.product(range(-K,K+1),repeat=nu):
        if not any(c): continue
        cc0=sum(ci*expr[j][0] for j,ci in enumerate(c)); ca=[sum(ci*expr[j][1][g] for j,ci in enumerate(c)) for g in range(2)]
        mx=max(cc0+ca[0]*t[0]+ca[1]*t[1] for t in V)
        if mx!=floor(mx):          # cut c.x <= floor(mx) is violated by part of P
            cuts.append(([-ca[0],-ca[1]], cc0-floor(mx)))   # -(cc0+ca.t) >= -floor(mx)  <=>  ca.t >= ... ; written as a.t >= b
    # the cut c.x <= f means cc0 + ca.t <= f, i.e. (-ca).t >= cc0 - f
    # exact half-plane clipping of the polygon V (convex, counter-clockwise order not needed: clip a vertex list sorted by angle)
    import math
    cx=sum(t[0] for t in V)/len(V); cy=sum(t[1] for t in V)/len(V)
    poly=sorted(V, key=lambda t: math.atan2(float(t[1]-cy), float(t[0]-cx)))
    for a,b in cuts:
        out=[]; m=len(poly)
        for i in range(m):
            P,Q=poly[i],poly[(i+1)%m]; fp=a[0]*P[0]+a[1]*P[1]-b; fq=a[0]*Q[0]+a[1]*Q[1]-b
            if fp>=0: out.append(P)
            if (fp>=0)!=(fq>=0) and fp!=fq:
                s_=fp/(fp-fq); out.append([P[0]+s_*(Q[0]-P[0]), P[1]+s_*(Q[1]-P[1])])
        poly=out
        if not poly: break
    return len(V), len(cuts), (len(poly)==0)
res=[]; 
for cl in fails:
    nv,nc,empty=analyse(cl); res.append(empty)
print(f"K={K}: {len(fails)} cores without single-variable certificate; first closure EMPTY (rank 1) for {sum(res)}, nonempty for {len(res)-sum(res)}")
json.dump({"K":K,"rank1":sum(res),"open":len(res)-sum(res)}, open(f"closure8_K{K}.out.json","w"))
