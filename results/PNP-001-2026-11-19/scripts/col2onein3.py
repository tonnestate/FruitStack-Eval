"""3-colouring -> positive 1-in-3 (director, 2026-11-19): vertex clause (x_v1,x_v2,x_v3); per edge uw and colour c clause (x_uc, x_wc, y_uwc).
Checks on small non-3-colourable graphs: GF(3) consistency, UNSAT (CaDiCaL), degree-2 PC in the XOR/carry encoding (pc2_verify closure)."""
import itertools, json, subprocess, sys
from pysat.solvers import Cadical153
def translate(V, E):
    x={(v,c): i for i,(v,c) in enumerate(itertools.product(V,range(3)))}; nxt=len(x); cl=[]
    for v in V: cl.append(tuple(x[v,c] for c in range(3)))
    for (u,w) in E:
        for c in range(3): cl.append((x[u,c],x[w,c],nxt)); nxt+=1
    return [tuple(sorted(c)) for c in cl], nxt
def gf3_consistent(cl,n):
    rows=[[1 if v in c else 0 for v in range(n)]+[1] for c in cl]; r=0
    for col in range(n):
        p=next((i for i in range(r,len(rows)) if rows[i][col]%3),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]; inv=1 if rows[r][col]==1 else 2; rows[r]=[(a*inv)%3 for a in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][col]%3: f=rows[i][col]; rows[i]=[(a-f*b)%3 for a,b in zip(rows[i],rows[r])]
        r+=1
    return all(any(a for a in row[:n]) or row[n]==0 for row in rows)
def sat(cl):
    with Cadical153() as s:
        for a,b,c in cl: s.add_clause([a+1,b+1,c+1]); s.add_clause([-a-1,-b-1]); s.add_clause([-a-1,-c-1]); s.add_clause([-b-1,-c-1])
        return s.solve()
graphs={"K4":(range(4),list(itertools.combinations(range(4),2))),
        "W5 (wheel, odd rim)":(range(6),[(0,i) for i in range(1,6)]+[(i,i%5+1) for i in range(1,6)])}
for name,(V,E) in graphs.items():
    cl,n=translate(list(V),E)
    out=subprocess.run([sys.executable,"pc2_verify.py",json.dumps([list(c) for c in cl])],capture_output=True,text=True).stdout.strip()
    print(f"{name}: {n} vars, {len(cl)} clauses | GF(3)-consistent {gf3_consistent(cl,n)} | UNSAT {not sat(cl)} | {out}")
