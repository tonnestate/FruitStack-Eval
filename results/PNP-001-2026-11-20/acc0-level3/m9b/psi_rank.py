"""Sanity check of the M9b' restriction scheme on a tiny order-lifted formula Psi(phi) (director 2026-11-20).
phi: unsatisfiable 2-CNF on N = 4 variables. Psi = Phi1 /\\ Phi2 (selectors over ordered pairs of distinct indices, exactly-one,
incompatibility). Cut on v: L = {v0, v1}, R = {v2, v3}. Scheme: M = two v-disjoint Phi1 clauses straddling the cut (selectors := generic),
other straddling Phi1 selectors := 0, all remaining selectors := generic. Prediction: rank >= 2^|M| = 4. Rank = rank of the evaluation
matrix over F_p (a lower bound on the coefficient rank; exact with high probability)."""
import itertools, random
import numpy as np
P = 2**31 - 1; rng = np.random.default_rng(3); pr = random.Random(3)
phi = [[(0,1),(1,1)], [(0,0),(1,1)], [(0,1),(1,0)], [(0,0),(1,0)], [(2,1),(3,1)]]   # (var, positive); first four: unsat in v0,v1
N = 4
sel = {(ci, t): f"u{ci}_{t}" for ci, C in enumerate(phi) for t in itertools.permutations(range(N), len(C))}
Phi1 = [[(sel[(ci, t)], 0)] + [(f"v{t[j]}", phi[ci][j][1]) for j in range(len(t))] for (ci, t) in sel]
def pmap(ci, t): return {t[j]: phi[ci][j][0] for j in range(len(t))}
Phi2 = []
by = {}
for (ci, t), u in sel.items(): by.setdefault(ci, []).append((t, u))
for ci, lst in by.items():
    Phi2.append([(u, 1) for _, u in lst])
    Phi2 += [[(a, 0), (b, 0)] for (_, a), (_, b) in itertools.combinations(lst, 2)]
items = list(sel.items())
for ((c1, t1), a), ((c2, t2), b) in itertools.combinations(items, 2):
    if c1 == c2: continue
    m1, m2 = pmap(c1, t1), pmap(c2, t2)
    bad = any(k in m2 and m2[k] != v for k, v in m1.items()) or any(
        x in {v: k for k, v in m2.items()} and {v: k for k, v in m2.items()}[x] != k for k, x in m1.items())
    if bad: Phi2.append([(a, 0), (b, 0)])
clauses = Phi1 + Phi2
L, R = {"v0", "v1"}, {"v2", "v3"}
def straddles(t): return any(f"v{i}" in L for i in t) and any(f"v{i}" in R for i in t)
M = [(0, (0, 2)), (4, (1, 3))]          # v-disjoint, both straddle
fixed = {}
for (ci, t), u in sel.items():
    if (ci, t) in M: fixed[u] = int(rng.integers(2, P))
    elif straddles(t): fixed[u] = 0
    else: fixed[u] = int(rng.integers(2, P))
for ci, lst in by.items():
    assert any(fixed[u] != 0 for _, u in lst), "every original clause keeps a non-zero selector"
def rank_mod(M_):
    M_ = M_.copy() % P; r = 0
    for c in range(M_.shape[1]):
        nz = np.nonzero(M_[r:, c])[0]
        if not len(nz): continue
        i = r + nz[0]; M_[[r, i]] = M_[[i, r]]; M_[r] = (M_[r] * pow(int(M_[r, c]), P - 2, P)) % P
        f = M_[:, c].copy(); f[r] = 0; M_ = (M_ - (f[:, None] * M_[r][None, :]) % P) % P; r += 1
        if r == M_.shape[0]: break
    return r
def eval_rank(fixed, m=64):
    A = {v: rng.integers(2, P, size=m) for v in L}; B = {v: rng.integers(2, P, size=m) for v in R}
    Mx = np.ones((m, m), dtype=np.int64)
    for D in clauses:
        a = np.ones(m, dtype=np.int64); b = np.ones(m, dtype=np.int64); c = 1
        for v, pos in D:
            if v in fixed: x = fixed[v] % P; c = (c * ((1 - x) % P if pos else x)) % P
            elif v in A: a = (a * ((1 - A[v]) % P if pos else A[v])) % P
            else: b = (b * ((1 - B[v]) % P if pos else B[v])) % P
        a = (a * c) % P
        Mx = (Mx * ((1 - (a[:, None] * b[None, :]) % P) % P)) % P
    return rank_mod(Mx)
print("selectors:", len(sel), "clauses:", len(clauses), "| rank under the M9b' scheme:", eval_rank(fixed), "(prediction >= 4)")
allzero_c0 = dict(fixed); 
for _, u in by[0]: allzero_c0[u] = 0
print("control: all selectors of clause 0 set to 0 (the 'at least one' factor vanishes):", eval_rank(allzero_c0))
