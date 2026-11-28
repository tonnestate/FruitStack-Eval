"""K_{3,3} control for the matchgate-excess measure (owner 2026-11-20). One variable per edge, one positive 1-in-3 clause per vertex.
Checks: n, m, read-twice, #SAT = number of perfect matchings = 3! = 6, parity via T41 D5 (det over F2) = 0, local signatures
EXACT1_3 / EQ_2 are standard-basis matchgates, crossover signature X(a,b,c,d) = [a=c][b=d] (a..d in cyclic order) is NOT a planar
matchgate in the standard basis (MGI of the independent review script)."""
import itertools, sys
sys.path.insert(0, "/root/fruits/research/PNP-001/lab/onein3")
import sympy
import mg3_independent_review as R
L, Rt = range(3), range(3)
edges = [(u, v) for u in L for v in Rt]                      # variable i = edge
clauses = [[i for i, (u, v) in enumerate(edges) if u == a] for a in L] + [[i for i, (u, v) in enumerate(edges) if v == b] for b in Rt]
n, m = len(edges), len(clauses)
occ = [sum(i in c for c in clauses) for i in range(n)]
sat = sum(all(sum(x[i] for i in c) == 1 for c in clauses) for x in itertools.product((0, 1), repeat=n))
B = sympy.zeros(m, m)
for i in range(m):
    for j in range(m):
        B[i, j] = len(set(clauses[i]) & set(clauses[j])) % 2 if i != j else sum(1 for v in clauses[i] if occ[v] == 1) % 2
print(f"K33: n={n}, m={m}, occurrences={set(occ)}, #SAT={sat}, #SAT mod 2={sat % 2}, det B mod 2 (D5)={int(B.det()) % 2}")
def is_mg(sig, k): return all(sympy.simplify(e) == 0 for e in R.mgi(sig, k))
print("EXACT1_3 matchgate:", is_mg(R.sym({1}, 3), 3), "| EQ_2 matchgate:", is_mg(R.sym({0, 2}, 2), 2))
X = {x: int(x[0] == x[2] and x[1] == x[3]) for x in itertools.product((0, 1), repeat=4)}
print("crossover [a=c][b=d] planar matchgate (standard basis):", is_mg(X, 4), "| |supp| =", sum(X.values()))
