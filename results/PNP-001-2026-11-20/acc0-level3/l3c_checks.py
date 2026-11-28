"""ACC0 level 3c (director, 2026-11-20): exact finite checks for the constructive/negative split.
D  = AND of GF(3)-linear equalities l(x)=c and dis-equalities l(x)!=c over Boolean x
     (= C0 plus LINEARLY DETERMINED Boolean existential auxiliaries: l!=c  <=>  exists y in {0,1}: y = l - c - 1).
(1) D-closure: f is in D iff the intersection of all equalities/dis-equalities containing f^{-1}(1) equals f^{-1}(1).
(2) Delta identity for D in canonical form: rank([E 0; N I]) - |N| = rank(E).
(3) NAND gadget search (Boolean-functional, unique witness) and its rank deficit; circuits of gadgets: Delta <= c - rho."""
import itertools, random
P=lambda n: list(itertools.product((0,1),repeat=n))
def rank3(rows):
    M=[list(r) for r in rows]; r=0; nc=len(M[0]) if M else 0
    for c in range(nc):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]%3==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%3: f=M[i][c]; M[i]=[(u-f*v)%3 for u,v in zip(M[i],M[r])]
        r+=1
    return r
def in_D(ones,n):
    pts=P(n); acc=set(pts)
    for a in itertools.product(range(3),repeat=n):
        for c in range(3):
            val=lambda x: (sum(ai*xi for ai,xi in zip(a,x))-c)%3
            if all(val(x)==0 for x in ones): acc&={x for x in pts if val(x)==0}
            if all(val(x)!=0 for x in ones): acc&={x for x in pts if val(x)!=0}
    return acc==set(ones)
for n in (2,3,4):
    OR=[x for x in P(n) if any(x)]; NAE=[x for x in P(n) if 0<sum(x)<n]
    print(f"(1) n={n}: OR_n in D: {in_D(OR,n)} | NAND_n in D: {in_D([x for x in P(n) if not all(x)],n)} | NAE_n in D: {in_D(NAE,n)}")
cnt=sum(in_D([x for x,b in zip(P(3),bits) if b],3) for bits in itertools.product((0,1),repeat=8))
print(f"(1) number of the 256 Boolean functions on 3 inputs in D: {cnt}")
random.seed(5); bad=0
for _ in range(300):
    n=random.randint(2,8); E=[[random.randint(0,2) for _ in range(n)] for _ in range(random.randint(0,4))]; N=[[random.randint(0,2) for _ in range(n)] for _ in range(random.randint(0,5))]
    full=[e+[0]*len(N) for e in E]+[N[j]+[1 if i==j else 0 for i in range(len(N))] for j in range(len(N))]
    bad+= (rank3(full)-len(N)) != (rank3(E) if E else 0)
print(f"(2) Delta identity rank(full)-|N| = rank(E): {bad} violations in 300 random D-systems")
# (3) gadget over (u,v,z,w1,w2): u+v+2z-w1 = 2 and u+v+z-w2 = 1 (two dis-equalities u+v+2z!=1, u+v+z!=0 made linear by
#     linearly determined aux w1, w2). Boolean solutions must be exactly {(u,v,NAND(u,v),w1,w2)} with unique witnesses.
gad=[((1,1,2,2,0),2),((1,1,1,0,2),1)]   # -w = +2w mod 3
S=[p for p in P(5) if all(sum(ai*pi for ai,pi in zip(a,p))%3==c for a,c in gad)]
assert sorted((u,v) for u,v,*_ in S)==P(2) and all(z==1-u*v for u,v,z,*_ in S), S
print("(3) NAND gadget exact (unique witnesses); rows 2, aux (z,w1,w2) 3 -> local Delta", rank3([list(a) for a,_ in gad])-3)
def sols(sys_): return [p for p in P(5) if all(sum(ai*pi for ai,pi in zip(a,p))%3==c for a,c in sys_)]
# random circuits of NAND gadgets on n inputs, output constraint z_out = 0 (c = 1 row); compare Delta with c - rho
def circuit(n,s):
    wires=list(range(n)); nv=n; R=[]; gates=[]
    for _ in range(s):
        u,v=random.sample(wires,2); z,w,w2=nv,nv+1,nv+2; nv+=3
        for a,c in gad:
            row={}; 
            for var,co in zip((u,v,z,w,w2),a):
                if co: row[var]=(row.get(var,0)+co)%3
            R.append((row,c))
        gates.append((u,v,z,w,w2)); wires.append(z)
    return R,gates,nv
def evalg(x,gates,nv):
    val=list(x)+[0]*(nv-len(x))
    for u,v,z,w,w2 in gates:
        p=next(p for p in sols(gad) if p[0]==val[u] and p[1]==val[v]); val[z],val[w],val[w2]=p[2],p[3],p[4]
    return val
bad=0
for _ in range(40):
    n=random.randint(3,6); s=random.randint(1,6); R,gates,nv=circuit(n,s); k=nv-n
    R2=R+[({gates[-1][2]:1},0)]                           # output constraint: c = 1
    r=rank3([[row.get(i,0) for i in range(nv)] for row,_ in R2])
    G=[[1]*2**n]+[[x[i] for x in P(n)] for i in range(n)]+[[evalg(x,gates,nv)[j] for x in P(n)] for j in range(n,nv)]
    rho=rank3(G)-(n+1)
    bad+= (r-k) > 1-rho
print(f"(3) gadget circuits: Delta = r-k <= c - rho violated in {bad} of 40 random circuits")
