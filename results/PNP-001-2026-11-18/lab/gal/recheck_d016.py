import itertools, random
def rank(rows, p):
    rows=[r[:] for r in rows]; r=0; ncol=len(rows[0]) if rows else 0
    for c in range(ncol):
        piv=next((i for i in range(r,len(rows)) if rows[i][c]%p),None)
        if piv is None: continue
        rows[r],rows[piv]=rows[piv],rows[r]; inv=pow(rows[r][c],p-2,p)
        rows[r]=[x*inv%p for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][c]%p:
                f=rows[i][c]; rows[i]=[(a-f*b)%p for a,b in zip(rows[i],rows[r])]
        r+=1
    return r
random.seed(1); groups={}
for _ in range(3000):
    n=random.randint(4,7); T=list(itertools.combinations(range(n),3)); m=random.randint(1,min(6,len(T)))
    cl=random.sample(T,m)
    A=[[int(i in c) for i in range(n)] for c in cl]; Ab=[r+[1] for r in A]
    C=sum(all(sum(a>>i&1 for i in c)==1 for c in cl) for a in range(1<<n))
    key=(n,m,rank(A,2),rank(Ab,2),rank(A,3),rank(Ab,3))
    groups.setdefault(key,set()).add(C%2)
mixed=[k for k,v in groups.items() if len(v)>1]
print(len(groups),"groups",len(mixed),"mixed parity; example",mixed[:3])
