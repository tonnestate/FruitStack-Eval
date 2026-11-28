"""Shrink a degree-2-PC-resistant blind core from above (owner recommendation 2026-11-19, director implementation).
Moves: identify two variables; replace one clause by another triple on the current variables. A variant is kept iff it is Boolean-UNSAT and
GF(3)-consistent; it is cut down to a minimal UNSAT core (deletion, CaDiCaL), relabelled to 0..k-1 and tested with the iterated degree-2 PC
closure (XOR/carry, GF(2), mod x^2=x). Resistant cores with fewer variables than the current best are logged and expanded first.
Usage: shrink_pc2.py SEED SECONDS"""
import sys, json, random, itertools, time
from pysat.solvers import Cadical153
seed, limit = int(sys.argv[1]), float(sys.argv[2]); random.seed(seed)
F16=[(0,1,9),(0,4,15),(1,2,7),(2,9,10),(3,6,9),(3,8,11),(4,9,11),(5,6,14),(5,7,9),(9,12,15),(10,12,13)]
def sat(cl):
    with Cadical153() as s:
        for a,b,c in cl: s.add_clause([a+1,b+1,c+1]); s.add_clause([-a-1,-b-1]); s.add_clause([-a-1,-c-1]); s.add_clause([-b-1,-c-1])
        return s.solve()
def gf3(cl):
    vs=sorted({v for c in cl for v in c}); ix={v:i for i,v in enumerate(vs)}; n=len(vs)
    rows=[[sum(1 for v in c if ix[v]==j) for j in range(n)]+[1] for c in cl]; r=0
    for col in range(n):
        p=next((i for i in range(r,len(rows)) if rows[i][col]%3),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]; inv=1 if rows[r][col]%3==1 else 2; rows[r]=[(a*inv)%3 for a in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][col]%3: f=rows[i][col]; rows[i]=[(a-f*b)%3 for a,b in zip(rows[i],rows[r])]
        r+=1
    return all(any(a%3 for a in row[:n]) or row[n]%3==0 for row in rows)
def core(cl):
    cl=list(cl); i=0
    while i<len(cl):
        t=cl[:i]+cl[i+1:]
        if not sat(t): cl=t
        else: i+=1
    vs=sorted({v for c in cl for v in c}); ix={v:i for i,v in enumerate(vs)}
    return sorted(tuple(sorted(ix[v] for v in c)) for c in cl), len(vs)
def pc2_refutes(cl, n):
    mons={(): 0}
    for i in range(n): mons[(i,)]=len(mons)
    for i,j in itertools.combinations(range(n),2): mons[(i,j)]=len(mons)
    inv={v:k for k,v in mons.items()}; Q=sum(1<<mons[m] for m in mons if len(m)==2)
    def P(ts):
        b=0
        for t in ts: b^=1<<mons[tuple(sorted(set(t)))]
        return b
    basis={}
    def add(v):
        while v:
            h=v.bit_length()-1
            if h in basis: v^=basis[h]
            else: basis[h]=v; return True
        return False
    for a,b,c in cl:
        add(P([(),(a,),(b,),(c,)])); add(P([(a,b),(a,c),(b,c)]))
    seen=set()
    while True:
        # degree<=1 part of the span: reduce with quadratic-leading basis vectors (quadratic monomials have the highest indices)
        low=[v for v in basis.values() if not v & Q and v not in seen]
        if not low: break
        for v in low:
            seen.add(v); terms=[inv[i] for i in range(v.bit_length()) if v>>i&1]
            for k in range(n): add(P([t+(k,) for t in terms]))
    return 0 in basis and basis[0]==1
best=(16,F16); frontier=[F16]; seen=set(); t0=time.time(); tested=0
print("start: F16 resistant =", not pc2_refutes(F16,16), flush=True)
while frontier and time.time()-t0<limit:
    frontier.sort(key=lambda c: len({v for x in c for v in x})); cur=frontier.pop(0)
    vs=sorted({v for c in cur for v in c}); moves=[]
    for u,v in itertools.combinations(vs,2): moves.append(("merge",u,v))
    for i in range(len(cur)):
        for t in random.sample(list(itertools.combinations(vs,3)), min(150, len(vs)*(len(vs)-1)*(len(vs)-2)//6)): moves.append(("swap",i,t))
    random.shuffle(moves)
    for mv in moves:
        if time.time()-t0>limit: break
        if mv[0]=="merge":
            _,u,v=mv; new=[tuple(sorted(u if x==v else x for x in c)) for c in cur]
            if any(len(set(c))<3 for c in new): continue
        else:
            _,i,t=mv; new=cur[:i]+[t]+cur[i+1:]
        new=sorted(set(new)); key=tuple(new)
        if key in seen: continue
        seen.add(key)
        if sat(new) or not gf3(new): continue
        c,k=core(new); ck=tuple(c)
        if ck in seen and ck!=key: continue
        seen.add(ck); tested+=1
        if k<=best[0] and gf3(c) and not pc2_refutes(c,k):
            if k<best[0] or len(frontier)<50:
                frontier.append(c)
            if k<best[0]:
                best=(k,c); print(f"{time.time()-t0:.0f}s NEW BEST {k} vars, {len(c)} clauses: {c}", flush=True)
print("DONE best", best[0], "vars:", best[1], "| cores tested", tested, flush=True)
json.dump({"best_vars":best[0],"core":best[1]}, open(f"shrink_pc2_s{seed}.json","w"))
