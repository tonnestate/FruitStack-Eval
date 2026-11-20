"""Summarise out_t*.txt: per function f on n = 3, 4 inputs: k_min, best rank surplus Delta = n - min dim V (all k <= 7-n), unique-witness
variant, and the Theorem H bound n - dim aff_GF3(f^{-1}(1)) (no representation can exceed it)."""
import itertools, collections, json
def rank3(rows):
    M=[list(r) for r in rows]; r=0
    for c in range(len(M[0]) if M else 0):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%3: f=M[i][c]; M[i]=[(u-f*v)%3 for u,v in zip(M[i],M[r])]
        r+=1
    return r
def pts(n,f): return [tuple((x>>j)&1 for j in range(n)) for x in range(2**n) if f>>x&1]
def daff(P): return -1 if not P else rank3([[(a-b)%3 for a,b in zip(p,P[0])] for p in P[1:]] or [[0]*len(P[0])])
data=collections.defaultdict(dict)   # (n,f) -> k -> (dim, dimu)
for t in range(3,8):
    for line in open(f"out_t{t}.txt"):
        T,n,k,f,d,du=map(int,line.split()); data[(n,f)][k]=(d,du)
named={3:{"OR":lambda x:any(x),"AND":lambda x:all(x),"NAND":lambda x:not all(x),"MAJ":lambda x:sum(x)>=2,"PARITY":lambda x:sum(x)%2==1,
          "NAE":lambda x:0<sum(x)<3,"1-in-3":lambda x:sum(x)==1,"EQ(x0,x1)":lambda x:x[0]==x[1]},
       4:{"OR":lambda x:any(x),"MAJ(>=2)":lambda x:sum(x)>=2,"MAJ(>=3)":lambda x:sum(x)>=3,"PARITY":lambda x:sum(x)%2==1,"NAE":lambda x:0<sum(x)<4,
          "EQ2(x0x1=x2x3)":lambda x:x[0]==x[2] and x[1]==x[3],"exactly-1":lambda x:sum(x)==1}}
out={}
for n in (3,4):
    kmax=7-n; nf=2**(2**n); rep=collections.Counter(); viol=0; atbound=0; pos=0; posnotC0=0
    for f in range(1,nf):
        ks=data.get((n,f),{})
        if not ks: rep["none<=%d"%kmax]+=1; continue
        km=min(ks); rep["k_min=%d"%km]+=1
        bestd=min(d for d,_ in ks.values()); bound=n-daff(pts(n,f)); D=n-bestd
        viol+= D>bound; atbound+= D==bound; pos+= D>0; posnotC0+= (D>0 and km>0)
    print(f"n={n}: functions f != 0 by minimal k: {dict(sorted(rep.items()))}")
    print(f"     best Delta > Theorem-H bound (must be 0): {viol}; best Delta = bound: {atbound}; Delta > 0: {pos}, of these needing aux (not in C0): {posnotC0}")
    for name,g in named[n].items():
        f=sum(1<<x for x in range(2**n) if g(tuple((x>>j)&1 for j in range(n))))
        ks=data.get((n,f),{}); bound=n-daff(pts(n,f))
        row={k:(n-d, (n-du) if du>=0 else None) for k,(d,du) in sorted(ks.items())}
        print(f"   {name:16s} k_min={min(ks) if ks else '>'+str(kmax)}  Delta by k (all, unique-witness): {row}  H-bound {bound}")
        out[f"n{n}:{name}"]={"k_min":min(ks) if ks else None,"delta_by_k":{str(k):v for k,v in row.items()},"H_bound":bound}
json.dump(out,open("summary.json","w"),indent=1)
