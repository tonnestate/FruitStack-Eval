import itertools, random, sys
sys.setrecursionlimit(10000); random.seed(7)
def count(nv, cl):
    """exact #solutions of positive 1-in-3 clauses over nv variables (unused variables count x2), DPLL with 1-in-3 propagation"""
    cl=[tuple(c) for c in cl]; occ=[[] for _ in range(nv)]
    for i,c in enumerate(cl):
        for v in c: occ[v].append(i)
    used=[v for v in range(nv) if occ[v]]; free=nv-len(used)
    def prop(x, stack):
        while stack:
            v=stack.pop()
            for i in occ[v]:
                c=cl[i]; vals=[x.get(u) for u in c]
                ones=vals.count(1); none=[u for u,val in zip(c,vals) if val is None]
                if ones>1 or (ones==0 and not none): return False
                if ones==1:
                    for u in none: x[u]=0; stack.append(u)
                elif len(none)==1: x[none[0]]=1; stack.append(none[0])
        return True
    def rec(x):
        un=next((v for v in used if v not in x), None)
        if un is None: return 1
        tot=0
        for b in (1,0):
            y=dict(x); y[un]=b
            if prop(y,[un]): tot+=rec(y)
        return tot
    return rec({}) * (2**free)
# read-3 construction (precise)
def read3(n, F):
    occ={}
    for j,c in enumerate(F):
        for p,v in enumerate(c): occ.setdefault(v,[]).append((j,p))
    new=[list(c) for c in F]; extra=[]; nv=[n]
    def fresh(): nv[0]+=1; return nv[0]-1
    def zero():
        T,a,b,c=fresh(),fresh(),fresh(),fresh(); extra.extend([(T,a,b),(T,b,c),(T,c,a)]); return a
    for v,os in occ.items():
        d=len(os); xs=[v]+[fresh() for _ in range(d)]
        for idx,(j,p) in enumerate(os): new[j][p]=xs[idx]
        for j in range(d):
            t=fresh(); extra.append((xs[j],t,zero())); extra.append((t,xs[j+1],zero()))
    return nv[0], [tuple(c) for c in new]+extra
ok=okr=okN=okK=0; R=300
for _ in range(R):
    n=random.randint(3,6); F=[tuple(random.sample(range(n),3)) for _ in range(random.randint(1,4))]
    used=sorted({v for c in F for v in c}); ren={v:i for i,v in enumerate(used)}; F=[tuple(ren[v] for v in c) for c in F]; n=len(used)
    D=3*len(F); nv,G=read3(n,F); reads={}
    for c in G:
        for v in c: reads[v]=reads.get(v,0)+1
    ok+= count(nv,G)==count(n,F); okr+= max(reads.values())<=3; okN+= len(reads)==10*D+n; okK+= sum(1 for r in reads.values() if r==3)==5*D-n
print(f"read-3 (T41 10b): count preserved {ok}/{R}, max occ<=3 {okr}/{R}, N=10D+n {okN}/{R}, K=5D-n {okK}/{R}", flush=True)
# section 6 reduction (precise: forcing with the constant gadget's zeros)
def reduce3cnf(n, phi):
    cl=[]; nv=[n]
    def fresh(): nv[0]+=1; return nv[0]-1
    T,a,b,c=fresh(),fresh(),fresh(),fresh(); cl+=[(T,a,b),(T,b,c),(T,c,a)]; comp={}
    def neg(x):
        if x not in comp: y=fresh(); cl.append((x,y,a)); comp[x]=y; comp[y]=x
        return comp[x]
    def lit(l): return l-1 if l>0 else neg(-l-1)
    def OR(p,q):
        w=fresh(); wb=neg(w); s,r,t=fresh(),fresh(),fresh(); cl.extend([(p,wb,s),(q,wb,r),(neg(p),r,t)]); return w
    for C3 in phi:
        u=OR(lit(C3[0]),lit(C3[1])); v=OR(u,lit(C3[2])); cl.append((v,a,b))
    return nv[0], cl
def sat3(n,phi): return sum(all(any((x[abs(l)-1]==1) if l>0 else (x[abs(l)-1]==0) for l in C3) for C3 in phi) for x in itertools.product((0,1),repeat=n))
ok6=tot6=0
lits3=[l for v in range(1,4) for l in (v,-v)]
for C3 in itertools.product(lits3, repeat=3):                       # every single clause over 3 variables (exhaustive)
    nv,cl=reduce3cnf(3,[C3]); tot6+=1; ok6+= count(nv,cl)==sat3(3,[C3])
for _ in range(400):
    n=random.randint(1,7); phi=[tuple(random.choice([1,-1])*random.randint(1,n) for _ in range(3)) for _ in range(random.randint(1,6))]
    nv,cl=reduce3cnf(n,phi); tot6+=1; ok6+= count(nv,cl)==sat3(n,phi)
print(f"section 6 reduction (T41 6): #SAT preserved {ok6}/{tot6}", flush=True)
