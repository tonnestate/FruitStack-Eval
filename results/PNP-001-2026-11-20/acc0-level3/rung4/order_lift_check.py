"""Mechanical check of the K-width generalisation of the order lift (TR26-070 Sec. 4, Prop. 17 / Thm. 18), director 2026-11-20.
For an unsatisfiable CNF phi with clauses of MIXED widths (up to K), build Psi = Phi1 /\\ Phi2 with selectors u_{C,t} for every tuple t of
|C| distinct v-indices. For random orders of ALL variables of Psi: take the induced v-order, relabel the r-th v as x_r (the hard order),
set the selectors accordingly, and check (a) Phi2 is satisfied, (b) every Phi1 clause with selector 0 is satisfied, (c) the remaining
clauses are EXACTLY phi (signs preserved), and (d) Psi is unsatisfiable (SAT solver)."""
import itertools, random
from pysat.solvers import Minisat22
def lift(phi, N):
    sel = {}                                      # (clause index, tuple) -> u variable id
    nid = N
    for ci, C in enumerate(phi):
        for t in itertools.permutations(range(N), len(C)):
            nid += 1; sel[(ci, t)] = nid
    Phi1 = [[-u] + [(t[j] + 1) * (1 if C[j] > 0 else -1) for j in range(len(C))] for (ci, t), u in sel.items() for C in [phi[ci]]]
    Phi2 = []
    byc = {}
    for (ci, t), u in sel.items(): byc.setdefault(ci, []).append((t, u))
    for ci, lst in byc.items():
        Phi2.append([u for _, u in lst])
        Phi2 += [[-a, -b] for (_, a), (_, b) in itertools.combinations(lst, 2)]
    def pmap(ci, t): return {t[j]: abs(phi[ci][j]) - 1 for j in range(len(t))}
    items = list(sel.items())
    for ((c1, t1), a), ((c2, t2), b) in itertools.combinations(items, 2):
        if c1 == c2: continue
        m1, m2 = pmap(c1, t1), pmap(c2, t2)
        bad = any(k in m2 and m2[k] != v for k, v in m1.items())
        inv1 = {v: k for k, v in m1.items()}; inv2 = {v: k for k, v in m2.items()}
        bad = bad or any(k in inv2 and inv2[k] != v for k, v in inv1.items())
        if bad: Phi2.append([-a, -b])
    return sel, Phi1, Phi2, nid
def check(phi, N, rnd, orders=20):
    sel, Phi1, Phi2, nvars = lift(phi, N)
    with Minisat22(bootstrap_with=Phi1 + Phi2) as s: unsat = not s.solve()
    ok = unsat
    for _ in range(orders):
        order = list(range(1, nvars + 1)); rnd.shuffle(order)
        vord = [x for x in order if x <= N]                       # induced order on v-variables (ids 1..N)
        relabel = {v - 1: r for r, v in enumerate(vord)}           # v index -> x_r (r-th in the hard order)
        inv = {r: vi for vi, r in relabel.items()}
        alpha = {}
        for (ci, t), u in sel.items():
            want = tuple(inv[abs(l) - 1] for l in phi[ci])
            alpha[u] = 1 if t == want else 0
        sat_lit = lambda l: abs(l) in alpha and (alpha[abs(l)] == 1) == (l > 0)
        ok &= all(any(sat_lit(l) for l in c) for c in Phi2)        # (a)
        rest = []
        for c in Phi1:
            if any(sat_lit(l) for l in c): continue                # (b) selector 0 -> satisfied
            rest.append(sorted((relabel[abs(l) - 1] + 1) * (1 if l > 0 else -1) for l in c if abs(l) <= N))
        ok &= sorted(map(tuple, rest)) == sorted(tuple(sorted(c)) for c in phi)   # (c) exactly phi in x_1 < ... < x_N
    return ok, unsat, len(sel)
rnd = random.Random(42); res = []
phis = [
  [[1], [-1, 2], [-2, 3], [-3]],                                   # widths 1,2,2,1
  [[1, 2], [1, -2], [-1, 3], [-1, -3]],                            # 2-CNF
  [[1, 2, 3], [-1], [-2], [-3, 4], [-4]],                          # mixed 1..3
  [[1, 2, 3, 4], [-1], [-2], [-3], [-4]],                          # width 4 (K = 4)
  [[1, -2, 3, 4], [2], [-1, 4], [-3], [-4, 1], [-1]],              # width 4 mixed signs
]
for phi in phis:
    N = max(abs(l) for c in phi for l in c)
    with Minisat22(bootstrap_with=phi) as s: assert not s.solve()
    ok, unsat, ns = check(phi, N, rnd)
    print(f"phi widths {sorted(set(len(c) for c in phi))}, N={N}, selectors={ns}: Psi unsat={unsat}, restriction == phi in hard order for 20 random orders: {ok}")
