"""Fast exhaustive enumeration of minimal GF(3)-blind cores on n variables (director, 2026-11-19), without CG certificates.
Same completeness argument as cgrank_n.py (witness types (k0,k1,k2) up to cyclic shift, ALLOWED clauses = value sum 1 mod 3, minimal cores
have <= n-1 clauses by T44 C3/C4), but Boolean solution sets are 2^n-bit integers: AND per clause, UNSAT = 0, minimality by prefix/suffix
ANDs. Output: distinct clause sets; isomorphism classes and orbit sums are computed separately (isoclasses.py).
Usage: cores_fast.py n [type k0,k1,k2]"""
import sys, json, itertools, time
n=int(sys.argv[1]); only=tuple(map(int,sys.argv[2].split(","))) if len(sys.argv)>2 else None
FULL=(1<<(1<<n))-1
def cmask(c):
    m=0
    for x in range(1<<n):
        if ((x>>c[0])&1)+((x>>c[1])&1)+((x>>c[2])&1)==1: m|=1<<x
    return m
types=sorted({min([(a,b,n-a-b),(n-a-b,a,b),(b,n-a-b,a)]) for a in range(1,n) for b in range(1,n-a) if n-a-b>=1})
found=set(); t0=time.time()
for ty in types:
    if only and ty!=only: continue
    val=[0]*ty[0]+[1]*ty[1]+[2]*ty[2]
    allowed=[c for c in itertools.combinations(range(n),3) if sum(val[v] for v in c)%3==1]
    masks=[cmask(c) for c in allowed]; A=len(allowed); cnt=0; nodes=0
    def dfs(start, chosen, sol):
        global cnt, nodes
        for j in range(start, A):
            nodes+=1; new=sol & masks[j]
            if new==0:
                ch=chosen+[j]; k=len(ch)
                pre=[FULL]*(k+1); suf=[FULL]*(k+1)
                for i in range(k): pre[i+1]=pre[i]&masks[ch[i]]
                for i in range(k-1,-1,-1): suf[i]=suf[i+1]&masks[ch[i]]
                if all(pre[i]&suf[i+1] for i in range(k)):
                    found.add(tuple(sorted(allowed[i] for i in ch))); cnt+=1
            elif len(chosen)+1 < n-1:
                dfs(j+1, chosen+[j], new)
    dfs(0, [], FULL)
    print(f"n={n} type {ty}: allowed {A}, minimal cores {cnt}, DFS nodes {nodes}, {time.time()-t0:.0f}s", flush=True)
json.dump({"n":n,"cores":[{"clauses":[list(c) for c in cl],"cert":{"kind":"-"}} for cl in sorted(found)]}, open(f"cores_fast_n{n}{'_'+'-'.join(map(str,only)) if only else ''}.json","w"))
print("DONE distinct", len(found))
