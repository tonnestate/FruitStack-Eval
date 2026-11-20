"""Exact multilinear Nullstellensatz degree over F_p (director 2026-11-20; cross-check of the Singular degBound measure).
NS_d holds iff 1 is in span_F{ ML(m * p_i) : m multilinear monomial, deg m + deg p_i <= d } (ML = multilinearisation, i.e. the Boolean
axioms; it never increases degree, so all vectors live in the monomials of degree <= d). Dense elimination mod p."""
import itertools, sys, json
import numpy as np
sys.path.insert(0, ".")
import sympy as sp
def to_ml(poly_str, n, p):
    xs = sp.symbols(f"x1:{n+1}")
    import re
    expr = sp.expand(sp.sympify(re.sub(r"x\((\d+)\)", lambda m: f"x{m.group(1)}", poly_str), locals={f"x{i+1}": xs[i] for i in range(n)}))
    terms = {}
    for mon, c in sp.Poly(expr, *xs).terms():
        key = frozenset(i for i, e in enumerate(mon) if e > 0)
        terms[key] = (terms.get(key, 0) + int(c)) % p
    return {k: v for k, v in terms.items() if v}
def ns_degree(n, polys, p, dmax):
    P = [to_ml(s, n, p) for s in polys]
    for d in range(1, dmax + 1):
        cols = [frozenset(c) for k in range(d + 1) for c in itertools.combinations(range(n), k)]
        ci = {c: i for i, c in enumerate(cols)}
        rows = []
        for q in P:
            dq = max(len(k) for k in q)
            for k in range(0, d - dq + 1):
                for m in itertools.combinations(range(n), k):
                    m = frozenset(m); r = np.zeros(len(cols), dtype=np.int64)
                    for mono, c in q.items(): r[ci[mono | m]] = (r[ci[mono | m]] + c) % p
                    rows.append(r)
        if not rows: continue
        A = np.array(rows) % p
        target = np.zeros(len(cols), dtype=np.int64); target[ci[frozenset()]] = 1
        def rank(M):
            M = M.copy() % p; r = 0
            for c in range(M.shape[1]):
                piv = np.nonzero(M[r:, c])[0]
                if len(piv) == 0: continue
                i = r + piv[0]; M[[r, i]] = M[[i, r]]
                M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
                nz = np.nonzero(M[:, c])[0]
                for j in nz:
                    if j != r: M[j] = (M[j] - M[j, c] * M[r]) % p
                r += 1
                if r == M.shape[0]: break
            return r
        if rank(np.vstack([A, target])) == rank(A): return d
    return f">{dmax}"
from gdeg import tseitin, colouring, subset, K4, K33, PRISM
out = []
for name, E, nv in (("K4", K4, 4), ("K33", K33, 6), ("prism", PRISM, 6)):
    n, P = tseitin(E, nv)
    for p in (2, 3): out.append(("Tseitin", name, n, f"F{p}", ns_degree(n, P, p, n + 1))); print(*out[-1], flush=True)
for n in range(2, 9):
    out.append(("SubsetSum n+1", f"n={n}", n, "F101", ns_degree(*subset(n), 101, n + 1))); print(*out[-1], flush=True)
n, P = colouring(4, K4)
for p in (2, 3): out.append(("Col(G)", "K4", n, f"F{p}", ns_degree(n, P, p, 5))); print(*out[-1], flush=True)
json.dump(out, open("nsdeg_results.json", "w"), indent=1)
