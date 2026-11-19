"""Exhaustive minimal GF(3)-blind cores on n variables with an INLINE degree test (director, 2026-11-19): enumeration as cores_fast.py,
every core tested at once for a degree-2 Nullstellensatz refutation (XOR/carry encoding, GF(2), no Boolean axioms); only failures are
kept and then tested for NS2 mod x^2=x and degree-2 PC. Counts are over labelled-within-type clause sets (duplicates across types possible;
the NS2 property is isomorphism-invariant, so failures are complete). Usage: cores_deg.py n [k0,k1,k2]"""
import sys, json, itertools, time
n=int(sys.argv[1]); only=tuple(map(int,sys.argv[2].split(","))) if len(sys.argv)>2 else None
FULL=(1<<(1<<n))-1
def cmask(c):
    m=0
    for x in range(1<<n):
        if ((x>>c[0])&1)+((x>>c[1])&1)+((x>>c[2])&1)==1: m|=1<<x
    return m
# monomial bits for NS2 without Boolean axioms: const, x_i, x_i*x_j (i<=j)
mon={(): 0}
for i in range(n): mon[(i,)]=len(mon)
for i in range(n):
    for j in range(i,n): mon[(i,j)]=len(mon)
def P(*ts):
    b=0
    for t in ts: b^=1<<mon[tuple(sorted(t))]
    return b
LG={}; QG={}
for c in itertools.combinations(range(n),3):
    a,b,d=c
    QG[c]=P((a,b),(a,d),(b,d))
    LG[c]=[P((),(a,),(b,),(d,))]+[P((k,),(a,k),(b,k),(d,k)) for k in range(n)]
ONE=1
def ns2(cl):
    basis={}
    for v in [QG[c] for c in cl]+[g for c in cl for g in LG[c]]:
        while v:
            h=v.bit_length()-1
            if h in basis: v^=basis[h]
            else: basis[h]=v; break
    v=ONE
    while v:
        h=v.bit_length()-1
        if h not in basis: return False
        v^=basis[h]
    return True
types=sorted({min([(a,b,n-a-b),(n-a-b,a,b),(b,n-a-b,a)]) for a in range(1,n) for b in range(1,n-a) if n-a-b>=1})
tot={"cores":0,"ns2":0}; fails=[]; t0=time.time()
for ty in types:
    if only and ty!=only: continue
    val=[0]*ty[0]+[1]*ty[1]+[2]*ty[2]
    allowed=[c for c in itertools.combinations(range(n),3) if sum(val[v] for v in c)%3==1]
    masks=[cmask(c) for c in allowed]; A=len(allowed); st={"cores":0,"ns2":0}
    def dfs(start, chosen, sol):
        for j in range(start, A):
            new=sol & masks[j]
            if new==0:
                ch=chosen+[j]; k=len(ch); pre=[FULL]*(k+1); suf=[FULL]*(k+1)
                for i in range(k): pre[i+1]=pre[i]&masks[ch[i]]
                for i in range(k-1,-1,-1): suf[i]=suf[i+1]&masks[ch[i]]
                if all(pre[i]&suf[i+1] for i in range(k)):
                    cl=[allowed[i] for i in ch]; st["cores"]+=1
                    if ns2(cl): st["ns2"]+=1
                    else: fails.append(sorted(cl))
            elif len(chosen)+1 < n-1:
                dfs(j+1, chosen+[j], new)
    dfs(0, [], FULL)
    for k in tot: tot[k]+=st[k]
    print(f"n={n} type {ty}: cores {st['cores']}, NS2 {st['ns2']}, NS2-failures so far {len(fails)}, {time.time()-t0:.0f}s", flush=True)
json.dump({"n":n,"totals":tot,"ns2_failures":fails}, open(f"cores_deg_n{n}{'_'+'-'.join(map(str,only)) if only else ''}.json","w"))
print("DONE", tot, "NS2 failures:", len(fails))
