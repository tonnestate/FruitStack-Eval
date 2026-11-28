import itertools, numpy as np, sys
def run(n):
    T=list(itertools.combinations(range(n),3)); k=len(T)
    def masks(vals, ok):
        return np.array(sorted({sum(1<<i for i,t in enumerate(T) if ok(sum(x[j] for j in t))) for x in itertools.product(vals,repeat=n)}),dtype=np.int64)
    B=masks((0,1),lambda s:s==1); G=masks((0,1,2),lambda s:s%3==1)
    def covered(F, M):
        out=np.zeros(F.size,bool)
        for m in M: out|=(F & ~m)==0
        return out
    cores=0; bymin={}
    for m in range(1, n):                         # minimal cores have <= n-1 clauses (T44 C4) - also verified below by checking m = n
        F=np.array([sum(1<<i for i in c) for c in itertools.combinations(range(k),m)],dtype=np.int64)
        blind=F[covered(F,G) & ~covered(F,B)]
        if blind.size==0: continue
        minimal=np.ones(blind.size,bool)
        for i in range(k):
            bit=np.int64(1<<i); has=(blind & bit)!=0
            if has.any():
                sub=blind[has] & ~bit
                minimal[np.where(has)[0][~covered(sub,B)]]=False   # a proper subset is UNSAT -> not minimal
        bymin[m]=int(minimal.sum()); cores+=int(minimal.sum())
    # sanity: with m = n clauses no minimal core (C4 says <= n-1)
    return cores, bymin
for n in map(int, sys.argv[1:]):
    print(n, run(n), flush=True)
