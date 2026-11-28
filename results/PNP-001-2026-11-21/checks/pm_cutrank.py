"""Cut rank of the perfect-matching indicator PM_G (variables = edges) for cubic graphs.
d-SDNNF size >= rank_Q of the cut matrix at every vtree node; rank over GF(p) <= rank_Q.
Test: does rank grow like 2^(#crossing structures) on balanced edge cuts?"""
import itertools, random, sys
import numpy as np
random.seed(3)
P = 1000003

def rank_mod(M, p=P):
    M = M.copy() % p; r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if not len(nz): continue
        piv = r + nz[0]; M[[r, piv]] = M[[piv, r]]
        M[r] = M[r] * pow(int(M[r, c]), p - 2, p) % p
        f = M[:, c].copy(); f[r] = 0
        M = (M - f[:, None] * M[r][None, :]) % p
        r += 1
        if r == rows: break
    return r

def random_cubic(nv):
    while True:
        stubs = [v for v in range(nv) for _ in range(3)]; random.shuffle(stubs)
        E = [tuple(sorted(stubs[i:i+2])) for i in range(0, len(stubs), 2)]
        if all(a != b for a, b in E) and len(set(E)) == len(E): return E

def pm_matrix(E, nv, L):
    R = [i for i in range(len(E)) if i not in L]
    rows = {}; cols = {}
    def ok_partial(sel):   # no vertex covered twice
        seen = set()
        for i in sel:
            for v in E[i]:
                if v in seen: return None
                seen.add(v)
        return frozenset(seen)
    lv = [ (a, ok_partial([L[j] for j in range(len(L)) if a >> j & 1])) for a in range(1 << len(L))]
    rv = [ (b, ok_partial([R[j] for j in range(len(R)) if b >> j & 1])) for b in range(1 << len(R))]
    lv = [x for x in lv if x[1] is not None]; rv = [x for x in rv if x[1] is not None]
    M = np.zeros((len(lv), len(rv)), dtype=np.int64)
    full = frozenset(range(nv))
    for i, (_, sa) in enumerate(lv):
        for j, (_, sb) in enumerate(rv):
            if not (sa & sb) and (sa | sb) == full: M[i, j] = 1
    return M

for nv in (8, 10, 12, 14):
    E = random_cubic(nv); m = len(E)
    best = 0; ranks = []
    for trial in range(6):
        L = sorted(random.sample(range(m), m // 2))
        M = pm_matrix(E, nv, L)
        ranks.append(rank_mod(M))
    print(f"nv={nv} edges={m}: ranks on random balanced edge cuts = {ranks}  (#PM total = {int(pm_matrix(E,nv,[]).sum())})", flush=True)
