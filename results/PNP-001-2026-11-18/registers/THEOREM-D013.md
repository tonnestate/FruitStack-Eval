# D-013: Positive 1-in-3-SAT is not a matroid port for n >= 6 (2026-11-18)

**Setting.** For n variables let U_n be the C(n,3) positive exactly-one clauses and L_n the clutter of minimal unsatisfiable
subsets of U_n (the minterms of the monotone function UNSAT_n : {0,1}^{U_n} -> {0,1}).

**Theorem.** L_5 is the port of a GF(3)-representable matroid (D-012). For every n >= 6, L_n is not the port of any matroid
(over any field, representable or not).

## Proof

**Lemma 1 (restriction).** For n > 6, deleting (clutter deletion) every clause that uses a variable outside {1..6} turns L_n
into L_6. *Proof:* clutter deletion keeps exactly the members of L_n contained in U_6. For S ⊆ U_6 the variables 7..n do not
occur, so S is satisfiable on n variables iff on 6, and the same holds for every subset of S; hence S is a minimal
unsatisfiable set in U_n iff in U_6. ∎

**Lemma 2 (certificate, finite, checked twice).** L_6 (3477 sets: 75 of size 4, 1872 of size 5, 1530 of size 6) has the minor
P4 = {{a,b},{b,c},{c,d}}: restrict to {123,124,126,134,145,156,235,236,246,346}, delete 134, 156, 236, contract 235, 246, 346.
The result is {{126,124},{124,145},{145,123}}, i.e. a = 126, b = 124, c = 145, d = 123.
Checks: lab/ports/qport6.py (exhaustive minor search, checker validated on 10 negative and 6 positive controls) and an
independent script that recomputes all MUS by direct 2^6 assignment enumeration and applies the deletion/contraction by hand.

**Lemma 3 (P4 is not a matroid port; elementary, no literature needed).** Suppose P4 is the port of M at p, i.e. the circuits
of M through p are pab, pbc, pcd. From the circuit pab, p ∈ cl(a,b); from pbc, c ∈ cl(p,b) ⊆ cl(a,b); from pcd,
d ∈ cl(p,c) ⊆ cl(a,b). So r(p,a,d) <= r(a,b,c,d,p) = 2. If p ∈ cl(a,d) there would be a circuit through p inside {p,a,d}, and
its trace would be one of {a},{d},{a,d} - none is in P4. Hence p ∉ cl(a,d), so r(a,d) = r(p,a,d) - 1 <= 1. a is not a loop
(else pab would not be a minimal dependent set), likewise d; so a and d are parallel. Parallel elements are interchangeable in
every circuit, so pdb is a circuit and {b,d} would be in the port - contradiction. ∎

**Lemma 4 (minor closure; standard).** Clutter minors of a matroid port are matroid ports (deletion of e: port of M\e;
contraction of e: port of M/e). Cited: Seymour 1976, Q. J. Math. 27 (owner-checked at secondary-source level). *Status:
cited, not re-proved here.*

**Proof of the theorem.** If L_n (n >= 6) were a port, so would be L_6 (Lemma 1 + Lemma 4) and its minor P4 (Lemma 2 +
Lemma 4), contradicting Lemma 3. ∎

## What it says about complexity - honestly

- Consequence: for every field F and n >= 6, no *ideal* monotone span program (one vector per clause) computes UNSAT_n;
  equivalently mSP_F(UNSAT_n) > C(n,3). This is a **weak** lower bound (by one row) in a **restricted** model.
- It does NOT bound general circuits and says nothing about P vs NP. It marks the exact point (n = 6) where every
  one-vector-per-clause linear representation breaks, for every field; at n = 5 GF(3) works, GF(2) never does (D-011).
- Novelty: not yet checked against the literature (matroid ports / ideal secret sharing of CSP clutters).
- Next, relevant: lower bounds on mSP_F(UNSAT_n) that grow with n (rank methods on minterms vs maxterms), each tested against
  the XOR-SAT control over the same field; a method that also bounds XOR-SAT measures monotonicity, not NP-hardness.
