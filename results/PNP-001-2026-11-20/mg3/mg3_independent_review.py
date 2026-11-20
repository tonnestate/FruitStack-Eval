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
# sanity of own MGI: EQ4 fails, EQ2/EXACT1_3/[1,0,1,0,1] pass, EQ3 fails
assert mgi(sym({0,4},4),4); assert not mgi(sym({0,2},2),2); assert not mgi(sym({1},3),3)
assert not mgi(sym({0,2,4},4),4); assert mgi(sym({0,3},3),3)
for conv in ('T','T^T'):
    T = [[a,b],[c,e]] if conv=='T' else [[a,c],[b,e]]
    adjT = [[T[1][1],-T[1][0]],[-T[0][1],T[0][0]]]  # det*(T^-1)^T
    det = T[0][0]*T[1][1]-T[0][1]*T[1][0]
    X = apply(T, sym({1},3), 3)
    print(conv, 'weights', [X[(0,0,0)], X[(1,0,0)], X[(1,1,0)], X[(1,1,1)]])
    for d in (2,3,4,5):
        Y = apply(adjT, sym({0,d},d), d)
        eqs = mgi(X,3) + mgi(Y,d) + [t*det-1]
        gb = sp.groebner(eqs, a,b,c,e,t, order='grevlex')
        print(conv, 'd=%d'%d, '#eqs', len(eqs), 'GB=={1}:', list(gb.exprs)==[1]); sys.stdout.flush()
