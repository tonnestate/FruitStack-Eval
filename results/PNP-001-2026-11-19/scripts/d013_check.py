import itertools
U = ["123","124","126","134","145","156","235","236","246","346"]
cl = [tuple(int(c)-1 for c in s) for s in U]
def sat(idx):
    return any(all(sum(x[v] for v in cl[i]) == 1 for i in idx) for x in itertools.product((0,1), repeat=6))
subsets = [frozenset(s) for r in range(len(U)+1) for s in itertools.combinations(range(len(U)), r)]
unsat = {s for s in subsets if not sat(s)}
mus = [s for s in unsat if all((s - {i}) not in unsat for i in s)]          # minimal unsatisfiable subsets of U = L_6 restricted to U
print("|MUS within U| =", len(mus))
name = {i: U[i] for i in range(len(U))}
D = {U.index(c) for c in ("134","156","236")}; C = {U.index(c) for c in ("235","246","346")}
dele = [s for s in mus if not (s & D)]                                       # deletion: members avoiding D
con = {frozenset(s - C) for s in dele}                                       # contraction: remove C, keep minimal sets
con = [s for s in con if not any(t < s for t in con)]
print("minor:", sorted(sorted(name[i] for i in s) for s in con))
target = [{"126","124"}, {"124","145"}, {"145","123"}]
print("equals P4 as stated:", sorted(map(sorted, target)) == sorted(sorted(name[i] for i in s) for s in con))
# Lemma 1 sanity: is the restriction clutter well-defined independent of n? satisfiability of clauses on vars 1..6 does not depend on extra variables
