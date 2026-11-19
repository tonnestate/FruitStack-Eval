import itertools, numpy as np, random
n=7; T=list(itertools.combinations(range(n),3)); k=len(T)
def masks(vals, ok): return np.array(sorted({sum(1<<i for i,t in enumerate(T) if ok(sum(x[j] for j in t))) for x in itertools.product(vals,repeat=n)}),dtype=np.int64)
B=masks((0,1),lambda s:s==1); G=masks((0,1,2),lambda s:s%3==1)
def cov(F,M):
    o=np.zeros(F.size,bool)
    for m in M: o|=(F&~m)==0
    return o
def rank3(idx):
    M=[[1 if j in T[i] else 0 for j in range(n)] for i in idx]; r=0
    for c in range(n):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(v*inv)%3 for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]: f=M[i][c]; M[i]=[(a-f*b)%3 for a,b in zip(M[i],M[r])]
        r+=1
    return r
bad=0; tot=0
for m in (5,6,7):
    F=np.array([sum(1<<i for i in c) for c in itertools.combinations(range(k),m)],dtype=np.int64)
    bl=F[cov(F,G)&~cov(F,B)]
    mn=np.ones(bl.size,bool)
    for i in range(k):
        bit=np.int64(1<<i); h=(bl&bit)!=0
        if h.any(): mn[np.where(h)[0][~cov(bl[h]&~bit,B)]]=False
    cores=bl[mn]; print("m",m,"minimal cores",cores.size, flush=True)
    for f in cores:
        idx=[i for i in range(k) if (int(f)>>i)&1]; tot+=1; bad+= rank3(idx)!=m
print("C3 independence violations:",bad,"of",tot)
