"""lambda_eff of the DIRECT holographic translation of circuits (director 2026-11-20).
Signature grid: one vertex per gate (relation [c = g(a,b)], arity 3), one wire vertex EQ_d per wire (d = 1 + number of consumers;
circuit output wire gets an extra unary [=1] constraint port). Constructed drawing: all vertices on a line in topological order (each
wire vertex right after its driver), edges as arcs on one page - crossings = interleaving arc pairs (a < c < b < d). Exact counts.
lambda_std (standard basis): gates AND/NAND 2 bits each (|supp| = 4), EQ_d (d >= 3) 1 bit, crossover 2 bits per crossing.
lambda_LB (every single GL2 basis, gates_groebner.py + matchgate_miner): >= number of nonlinear gates (crossings not even counted)."""
import random, itertools
def circuit(n, s, rnd, maxfan=3):
    fan = [0]*(n+s); gates = []
    for j in range(s):
        cand = [w for w in range(n+j) if fan[w] < maxfan]
        u, v = rnd.sample(cand, 2); fan[u] += 1; fan[v] += 1; gates.append((u, v))
    return gates, fan
def measure(n, s, rnd):
    gates, fan = circuit(n, s, rnd)
    pos = {}; k = 0
    for i in range(n): pos[("w", i)] = k; k += 1
    for j in range(s): pos[("g", j)] = k; pos[("w", n+j)] = k+1; k += 2
    arcs = []
    for j, (u, v) in enumerate(gates):
        g = pos[("g", j)]
        arcs += [(pos[("w", u)], g), (pos[("w", v)], g), (g, pos[("w", n+j)])]
    arcs = [tuple(sorted(x)) for x in arcs]
    cr = sum(1 for (a, b), (c, d) in itertools.combinations(arcs, 2) if a < c < b < d or c < a < d < b)
    eq3 = sum(1 for w in range(n+s) if 1 + fan[w] + (w == n+s-1) >= 3)   # wire vertex arity: driver/input side + consumers (+ output)
    lam_std = 2*s + eq3 + 2*cr
    return lam_std, s, cr, eq3          # lambda_LB = s (all gates NAND = nonlinear)
rnd = random.Random(20261120)
print(f"{'n':>4} {'s':>5} {'crossings':>9} {'EQ>=3':>6} {'lambda_std':>10} {'lambda_LB(any GL2)':>18}  vs n")
for n in (8, 16, 32, 64):
    for mult in (1, 2, 4, 8):
        s = mult*n; lam, lb, cr, eq3 = measure(n, s, rnd)
        print(f"{n:>4} {s:>5} {cr:>9} {eq3:>6} {lam:>10} {lb:>18}  {'>= n' if lb >= n else '< n'}")
