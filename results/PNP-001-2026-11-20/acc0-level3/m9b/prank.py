"""M9b level 1 (director 2026-11-20): coefficient rank of P(x) = prod_j (1 - Q_j(x)) for F(G) across cuts.
Rank measured as rank of the evaluation matrix M[a,b] = P(a,b), a in F^L, b in F^R random over F_p, p = 2^31 - 1 (equals the
coefficient rank with high probability over a large field). Q_j = product of literal terms (1-x for a positive literal, x for a negative
one) - the CNF arithmetisation; each factor splits as 1 - QL(a) QR(b). Reported: rank (capped), #crossing clauses, k_disj = size of a
greedy family of crossing clauses with pairwise disjoint variables (the restriction route predicts rank >= 2^k_disj if its lemma holds)."""
import itertools, random, sys, json
import numpy as np
P = 2**31 - 1
def F_of_G(V, E):
    idx = {}
    def var(k):
        if k not in idx: idx[k] = len(idx)
        return idx[k]
    tri = [[var(("x", v, c)) for c in range(3)] for v in range(V)] + [[var(("x", u, c)), var(("x", w, c)), var(("y", u, w, c))] for u, w in E for c in range(3)]
    cl = []
    for a, b, c in tri:
        cl += [[(a, 1), (b, 1), (c, 1)], [(a, 0), (b, 0)], [(a, 0), (c, 0)], [(b, 0), (c, 0)]]   # (var, positive?)
    return len(idx), cl, idx
def rank_mod_p(M):
    M = M.copy() % P; r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = np.nonzero(M[r:, c])[0]
        if len(piv) == 0: continue
        i = r + piv[0]
        if i != r: M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), P - 2, P); M[r] = (M[r] * inv) % P
        below = M[r+1:, c].copy()
        nz = np.nonzero(below)[0]
        if len(nz): M[r+1+nz] = (M[r+1+nz] - (below[nz, None] * M[r][None, :]) % P) % P
        r += 1
        if r == rows: break
    return r
def cut_rank(n, cl, left, rng, cap):
    L = sorted(left); R = [v for v in range(n) if v not in left]
    k = 32
    while True:
        A = rng.integers(0, P, size=(k, n), dtype=np.int64)   # rows: left assignment varies; right part from B
        B = rng.integers(0, P, size=(k, n), dtype=np.int64)
        M = np.ones((k, k), dtype=np.int64)
        for c in cl:
            ql = np.ones(k, dtype=np.int64); qr = np.ones(k, dtype=np.int64)
            for v, pos in c:
                if v in left: col = A[:, v]; ql = (ql * ((1 - col) % P if pos else col)) % P
                else:         col = B[:, v]; qr = (qr * ((1 - col) % P if pos else col)) % P
            M = (M * ((1 - (ql[:, None] * qr[None, :]) % P) % P)) % P
        r = rank_mod_p(M)
        if r < k or k >= cap: return r, (r >= k)
        k *= 2
def crossing(cl, left):
    cr = [c for c in cl if any(v in left for v, _ in c) and any(v not in left for v, _ in c)]
    used = set(); fam = 0
    for c in sorted(cr, key=len):
        vs = {v for v, _ in c}
        if vs & used: continue
        used |= vs; fam += 1
    return len(cr), fam
def orders(n, idx, rng):
    byvert = sorted(range(n), key=lambda i: [k for k, v in idx.items() if v == i][0][1:])
    yield "grouped", byvert
    for s in range(3):
        o = list(range(n)); rng.shuffle(o); yield f"random{s}", o
G = {"K4": (4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
     "W5": (6, [(0, i) for i in range(1, 6)] + [(i, i % 5 + 1) for i in range(1, 6)]),
     "Petersen": (10, [(i, (i+1) % 5) for i in range(5)] + [(5+i, 5+(i+2) % 5) for i in range(5)] + [(i, 5+i) for i in range(5)])}
rng = np.random.default_rng(1); prng = random.Random(1); out = []
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 1024
for name, (V, E) in G.items():
    n, cl, idx = F_of_G(V, E)
    for oname, o in orders(n, idx, prng):
        for frac in (0.25, 0.5, 0.75):
            left = set(o[: int(frac * n)])
            r, capped = cut_rank(n, cl, left, rng, CAP)
            ncr, kd = crossing(cl, left)
            row = (name, n, len(cl), oname, frac, ("≥" if capped else "") + str(r), ncr, kd, 2 ** kd)
            out.append(row); print(*row, flush=True)
json.dump(out, open("prank_level1.json", "w"), indent=0)
