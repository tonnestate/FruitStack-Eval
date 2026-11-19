"""ALG-BIT-001 search for a GF(3)-blind formula WITHOUT a degree-2 GF(2) refutation (director, 2026-11-19, owner request).
Random positive 1-in-3 formulas (n, m), kept iff GF(3)-consistent and Boolean-UNSAT (CaDiCaL via pysat). Degree test = run() of
xorcarry_degree.py (NS2 without Boolean axioms; then NS2 mod x^2=x and full degree-2 PC mod x^2=x). A formula failing all three is a
counterexample: every subset fails too, so its minimal cores need degree >= 3; the script shrinks it to a minimal UNSAT core and re-tests.
Usage: deg2_search.py SEED N_LO N_HI TRIALS_PER_POINT"""
import sys, random, json, itertools, time
from pysat.solvers import Cadical153
seed, nlo, nhi, T = map(int, sys.argv[1:5]); random.seed(seed)
src=open("/root/fruits/research/PNP-001/lab/review-2026-11-19/xorcarry_degree.py").read().split("classes={}")[0]
def degree2(cl, n):
    ns={}; sys.argv=["x",str(n),"/dev/null"]
    exec(src.replace('cores=[[tuple(c) for c in x["clauses"]] for x in json.load(open(src))["cores"]]','cores=[]'), ns)
    a,_=ns["run"](cl,False)
    if a: return "NS2"
    b,c=ns["run"](cl,True)
    return "NS2_bool" if b else "PC2_bool" if c else "FAIL"
def gf3_consistent(cl, n):
    rows=[[1 if v in c else 0 for v in range(n)]+[1] for c in cl]; r=0
    for col in range(n):
        p=next((i for i in range(r,len(rows)) if rows[i][col]%3),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]; inv=1 if rows[r][col]%3==1 else 2
        rows[r]=[(x*inv)%3 for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][col]%3: f=rows[i][col]; rows[i]=[(x-f*y)%3 for x,y in zip(rows[i],rows[r])]
        r+=1
    return all(any(x%3 for x in row[:n]) or row[n]%3==0 for row in rows)
def sat(cl):
    with Cadical153() as s:
        for a,b,c in cl:
            s.add_clause([a+1,b+1,c+1]); s.add_clause([-a-1,-b-1]); s.add_clause([-a-1,-c-1]); s.add_clause([-b-1,-c-1])
        return s.solve()
def shrink(cl):
    core=list(cl); i=0
    while i<len(core):
        t=core[:i]+core[i+1:]
        if not sat(t): core=t
        else: i+=1
    return core
stats={}; t0=time.time(); hits=[]
for n in range(nlo, nhi+1):
    for ratio in (0.70,0.75,0.80,0.85,0.90,0.95):
        m=round(ratio*n); key=f"n{n}_m{m}"; st=stats.setdefault(key,{"tried":0,"blind":0})
        for _ in range(T):
            cl=sorted({tuple(sorted(random.sample(range(n),3))) for _ in range(m)})
            st["tried"]+=1
            if not gf3_consistent(cl,n) or sat(cl): continue
            st["blind"]+=1; d=degree2(cl,n); st[d]=st.get(d,0)+1
            if d=="FAIL":
                core=shrink(cl); dc=degree2(core,n)
                hits.append({"n":n,"formula":cl,"core":core,"core_vars":len({v for c in core for v in c}),"core_degree2":dc})
                print("HIT", json.dumps(hits[-1]), flush=True)
        print(key, st, f"{time.time()-t0:.0f}s", flush=True)
json.dump({"seed":seed,"stats":stats,"hits":hits}, open(f"deg2_search_s{seed}_n{nlo}-{nhi}.json","w"))
print("DONE", len(hits), "hits")
