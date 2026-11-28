# Independent MG-3 check: own tensor, own MGI (Cai-Gorenstein Thm 2.1), Groebner over Q.
import itertools, sys, sympy as sp
a,b,c,e,t = sp.symbols('a b c e t')
def apply(M, vec, k):  # vec: dict bitstring-tuple -> value; M acts as column-vector map M[i][j]: |j> -> sum_i M[i][j]|i>
    out = {}
    for x in itertools.product((0,1), repeat=k):
        out[x] = sp.expand(sum(v*sp.prod([M[x[p]][y[p]] for p in range(k)]) for y,v in vec.items() if v != 0))
    return out
def sym(ws, k): return {x: (1 if sum(x) in ws else 0) for x in itertools.product((0,1), repeat=k)}
def mgi(G, k):
    eqs = set()
    for al in itertools.product((0,1), repeat=k):
        for be in itertools.product((0,1), repeat=k):
            P = [p for p in range(k) if al[p] != be[p]]
            s = 0
            for i,p in enumerate(P, 1):
                fa = tuple(v ^ (q == p) for q,v in enumerate(al)); fb = tuple(v ^ (q == p) for q,v in enumerate(be))
                s += (-1)**i * G[fa]*G[fb]
            s = sp.expand(s)
            if s != 0: eqs.add(s)
    return list(eqs)
# --- director 2026-11-20: gate relations [c = g(a,b)] (clause side, T^{x3}) with wire equality EQ_d (variable side, adj(T)^T^{xd})
TM = sp.Matrix([[a,b],[c,e]]); T = TM.tolist(); A = TM.adjugate().T.tolist()
gates = {"AND": lambda x,y: x&y, "OR": lambda x,y: x|y, "NAND": lambda x,y: 1-(x&y), "XOR": lambda x,y: x^y, "NOT": None}
for name, g in gates.items():
    if name == "NOT": sig, k = {x: int(x[1] == 1-x[0]) for x in itertools.product((0,1), repeat=2)}, 2
    else: sig, k = {x: int(x[2] == g(x[0], x[1])) for x in itertools.product((0,1), repeat=3)}, 3
    for d in (2, 3, 4):
        eqs = mgi(apply(T, sig, k), k) + mgi(apply(A, sym({0, d}, d), d), d) + [t*TM.det() - 1]
        gb = sp.groebner(eqs, a, b, c, e, t, order="grevlex", domain="QQ")
        print(f"{name} with EQ_{d}: {'NO common basis (GB = {1})' if list(gb.exprs) == [1] else 'basis exists (proper ideal)'}")
