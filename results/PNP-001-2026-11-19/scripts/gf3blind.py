import itertools, numpy as np
for n in (5, 6):
    T = list(itertools.combinations(range(n), 3)); k = len(T)
    def masks(vals, ok):
        return np.array(sorted({sum(1 << i for i, t in enumerate(T) if ok(sum(x[j] for j in t))) for x in itertools.product(vals, repeat=n)}), dtype=np.int64)
    B = masks((0, 1), lambda s: s == 1); G = masks((0, 1, 2), lambda s: s % 3 == 1)
    F = np.arange(1 << k, dtype=np.int64)
    sat = np.zeros(F.size, bool); con = np.zeros(F.size, bool)
    for m_ in B: sat |= (F & ~m_) == 0
    for m_ in G: con |= (F & ~m_) == 0
    blind = con & ~sat
    pc = np.array([bin(f).count("1") for f in range(1 << k)])
    print(f"n={n}: {F.size} clause sets, UNSAT {(~sat).sum()}, GF(3)-blind {blind.sum()}; by m:", {int(m): int(blind[pc == m].sum()) for m in range(k + 1) if blind[pc == m].sum()})
    if n == 6:
        ex = [(0,1,2),(0,1,3),(0,2,3),(0,4,5),(1,2,4)]; f = sum(1 << T.index(t) for t in ex)
        print("owner example: sat", bool(sat[f]), "gf3-consistent", bool(con[f]))
