# T28 — What the evaluator requires, and a lemma excluding all gate-value encodings (PI, 2026-11-17)

STATUS: Lemma G proved here; an earlier, weaker version (minimal-circuit form) checked through FruitStack/PlumMe (gpt-oss-120b,
receipt_6709dc47aef144898c6db1a5a30d68b1: all five items CORRECT); the strengthened proof in §2 is a direct simplification, not yet
reviewed separately. No computation. Not in the ledger.
Main line: T24 encoding question. Scope: algorithms-to-lower-bounds route; even full success gives lower bounds of the
NEXP/E^NP type, not the binding obligation ∃ L ∈ NP \ P (owner, 2026-11-17).

## Cost inequality (owner)
For every fixed k and every circuit C with n inputs and size <= n^k:
    T_encode(C) + T_evaluate(E(C)) + T_decode(C) <= 2^n / n^{ω(1)},
including auxiliary variables, representation size, arithmetic precision and reconstruction. Satisfiability preservation alone is
insufficient; the advantage is measured against the original n.

## §1 What the claimed evaluator requires from outside (OpenAI manuscript, Thm 1.1 and §2, read in source)
- Input: an arbitrary k-CNF (fixed k) on N variables with m clauses; exact count in (N+m)^{O_k(1)} 2^{O_k(N log log N/sqrt(log N))}
  bit operations, polynomial space (formal bound: (log log N)^2 in place of log log N).
- Bounded occurrence (each variable in <= 3 clauses) is NOT required of the input: the algorithm produces it internally by disjoint
  sparsification and variable copying, and the stated bound already includes those costs. (Owner's qualification adopted: fixed
  width does not by itself give bounded occurrence; here the transformation supplies it, at a cost inside the theorem.)
- Exactness: counts are integers of <= N bits; arithmetic cost is inside the bit-operation bound.
- Hence the ONLY structural requirements an encoding must meet are: (R1) fixed clause width w = w(k);
  (R2) variable count N <= n·sqrt(log n)/(C_w (log log n)^2)·(1 − o(1)) (formal bound) so that T_evaluate <= 2^{n − ω(log n)};
  (R3) m = 2^{o(n)} clauses and T_encode, T_decode <= 2^n/n^{ω(1)}; (R4) correctness of the decoded answer (decision or count).
  T24: (R1)+(R2) for all size-n^k circuits force w >= k−1 (counting) / w >= k (poly-time, unless coNP ⊆ NP/poly).

## §2 Lemma G (gate-value encodings are excluded)
A gate-value encoding of f: a circuit C' for f and a set S of its gates; auxiliary variables = values of the gates in S; the CNF
asserts, for each g ∈ S ∪ {output}, that g equals the function of the <= w−1 variables of X ∪ S feeding g through gates outside S.
Lemma G. For every gate-value encoding of width w: |S| >= CircuitSize(f)/2^w − 1, for ANY circuit C' (minimality not needed).
Proof. The constraints define each S-variable (and the output) as a function h_g of <= w−1 variables of X ∪ S that come earlier in
C' (acyclic). Every Boolean function of <= w−1 inputs has a circuit of size < 2^w. Composing these in topological order gives a circuit
for f of size < (|S| + 1)·2^w. Hence CircuitSize(f) < (|S|+1)·2^w. ∎
(Reviewed earlier form: with C' minimal, every cone has <= 2^{2^{w−1}} gates, |S| >= (size(C') − 2^{2^{w−1}})/(2^{2^{w−1}}+1).)
Consequence. For every fixed w and every f with CircuitSize(f) >= n^{1+ε}, every gate-value encoding has N − n = Ω_w(n^{1+ε}) auxiliary
variables, violating (R2): T_evaluate = 2^{Ω(n^{1+ε}/sqrt(log n))} > 2^n. This excludes Tseitin and every grouped/clustered variant
of it (any choice of which gate values to guess, any constant width) — for all functions of superlinear circuit complexity.
Functions of circuit complexity between n^{1+ε}/2 and n^{1+ε} exist (counting), so the exclusion is not vacuous at size n^{1+ε}.

## §3 What remains open (the precise class not covered)
Encodings whose auxiliary variables are NOT gate values of any circuit for f: proof-like witnesses y with f(x) = 1 ⇔ ∃y φ(x,y),
φ of constant width, |y| <= n·sqrt(log n)/polyloglog. Lemma G does not apply (the witness bits need not be computable from x by a small
circuit). Known constraints: counting (T24 K1) allows them only for w >= k−1; Dell–van Melkebeek forbids poly-time
satisfiability-preserving versions with w < k unless coNP ⊆ NP/poly. Standard short PCPs give length >= s = n^k, far too long.
Precise open question: does every f ∈ SIZE(n^k) admit a perfectly sound, perfectly complete, constant-width (w = w(k)) existential
CNF verifier with witness length n·sqrt(log n)/polyloglog, constructible within the cost inequality? No construction and no
impossibility proof are known to us.
