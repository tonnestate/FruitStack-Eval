"""Random test of the completeness PREMISES (independent of both enumerators): for random minimal GF(3)-blind cores,
(1) |clauses| <= |vars| - 1 (T44 C4); (2) some GF(3) solution uses all three values (D-018);
(3) normalising that solution (translation + sorting variables by value, type = rotation-minimal) puts every clause into ALLOWED."""
import random, itertools, sys, collections
from pysat.solvers import Cadical153
def sat(cl):
    with Cadical153() as s:
        for a,b,c in cl: s.add_clause([a+1,b+1,c+1]); s.add_clause([-a-1,-b-1]); s.add_clause([-a-1,-c-1]); s.add_clause([-b-1,-c-1])
        return s.solve()
def gf3_solutions(cl, vs):
    ix={v:i for i,v in enumerate(vs)}; n=len(vs)
    rows=[[0]*n+[1] for _ in cl]
    for r,(a,b,c) in zip(rows,cl): r[ix[a]]=r[ix[b]]=r[ix[c]]=1
    piv=[]; r=0
    for col in range(n):
        p=next((i for i in range(r,len(rows)) if rows[i][col]%3),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]; inv=1 if rows[r][col]==1 else 2; rows[r]=[(x*inv)%3 for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][col]: f=rows[i][col]; rows[i]=[(x-f*y)%3 for x,y in zip(rows[i],rows[r])]
        piv.append(col); r+=1
    if any(not any(row[:n]) and row[n] for row in rows): return []
    free=[c for c in range(n) if c not in piv]; out=[]
    for fv in itertools.product(range(3),repeat=len(free)):
        x=[0]*n
        for c,v in zip(free,fv): x[c]=v
        for i,c in enumerate(piv): x[c]=(rows[i][n]-sum(rows[i][f]*x[f] for f in free))%3
        out.append(x)
    return out
def core(cl):
    cl=list(cl); i=0
    while i<len(cl):
        t=cl[:i]+cl[i+1:]
        if not sat(t): cl=t
        else: i+=1
    return cl
random.seed(int(sys.argv[1])); stats=collections.Counter(); bad=[]
for trial in range(int(sys.argv[2])):
    n=random.randint(8,14); m=random.randint(int(0.6*n),n)
    cl=sorted({tuple(sorted(random.sample(range(n),3))) for _ in range(m)})
    vs=sorted({v for c in cl for v in c})
    if sat(cl) or not gf3_solutions(cl,vs): continue
    c=core(cl); cv=sorted({v for t in c for v in t})
    sols=gf3_solutions(c,cv)
    if not sols: stats["core_gf3_inconsistent(not blind)"]+=1; continue
    stats["blind_cores"]+=1
    ok1=len(c)<=len(cv)-1
    three=[x for x in sols if len(set(x))==3]
    ok2=bool(three)
    ok3=False
    if three:
        x=three[0]
        for shift in range(3):
            y=[(v+shift)%3 for v in x]; cnt=[y.count(0),y.count(1),y.count(2)]
            if all(sum(y[cv.index(a)] for a in t)%3==1 for t in c): ok3=True
        k=tuple(min([(cnt[0],cnt[1],cnt[2]),(cnt[2],cnt[0],cnt[1]),(cnt[1],cnt[2],cnt[0])]))
        stats[("size",len(cv))]+=1
    for name,ok in (("C4",ok1),("D018_three_values",ok2),("ALLOWED",ok3)):
        stats[name+("_ok" if ok else "_VIOLATED")]+=1
        if not ok and len(bad)<5: bad.append((name,c))
print(dict(stats)); print("violations:", bad)
