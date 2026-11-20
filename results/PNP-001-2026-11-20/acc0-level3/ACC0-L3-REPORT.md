# PNP-001 ACC0 Level 3 — GF(3) Boolean intersection and algorithmic lower-bound transfer (director, 2026-11-20)

Spec: /root/contracts/PNP-001-ACC0-MOD6-2026-11-19.md (active state contains Level 3 + precisions; the GitHub copy on
cc/pnp001-results-20261118 predates them - reconciliation = push of the active file, pending owner approval). No duplicate assignment.
Checks: lab/acc0-level3/l3_checks.py (exact; 3,000 runs, 0 disagreements). Existing results (Theorem 30 w*(F(G)) = 2tw+1 Lean,
Theorem 44, F16, n <= 10 classification) untouched.

## 1 Model and exact encoding
GF(3)-Lin-01-SAT: given A in GF(3)^{r x n}, b in GF(3)^r, decide whether some x in {0,1}^n satisfies Ax = b (mod 3).
Here t = n, m = 0 (NO auxiliary variables), d = n - rank(A).
Lemma E (exact encoding). A positive 1-in-3 clause (a,b,c) holds for Boolean x iff x_a+x_b+x_c = 1 (mod 3).
Proof: the integer sum lies in {0,1,2,3}; it is 1 mod 3 iff it equals 1. QED. Hence positive 1-in-3-SAT = GF(3)-Lin-01-SAT with 0/1
rows of weight 3 and b = 1, i.e. SAT of circuits AND o MOD3[=1] over input LITERAL-FREE linear forms (fan-in 3).
Circuit class C0 := AND o MOD3^lin: top AND of arbitrary fan-in; each MOD3 gate outputs 1 iff sum_i a_i x_i = b (mod 3), a_i in GF(3),
constants allowed, no bottom AND gates; size s = number of MOD3 gates + wires; non-uniform. C0-SAT = GF(3)-Lin-01-SAT (exact, no blow-up).
Note on F(G): there the slack variables y are BOOLEAN inputs of the same system (they are among the n variables), not GF(3)-free;
treating them as unrestricted over GF(3) would change the Boolean problem - in this report every variable is Boolean.

## 2 Algorithms (exact, worst case, measured in the circuit inputs n)
Lemma M (meet in the middle = the forward/backward identity with interface = partial syndrome). Split x = (x_L, x_R), |x_L| = n/2.
Ax = b iff A_L x_L = b - A_R x_R. Tabulate A_L x_L over {0,1}^{n/2} in a hash table (<= min(2^{n/2}, 3^r) keys), then look up each
b - A_R x_R. Correct on SAT and UNSAT; time O(2^{n/2} r n), space O(2^{n/2} r).
Lemma F (free-variable enumeration). Gaussian elimination mod 3 (O(r n min(r,n))) gives pivot columns P (|P| = rank) and free columns
U (|U| = d); every GF(3) solution is determined by its free values. Enumerate x_U in {0,1}^d, compute pivots mod 3, accept iff all
pivots lie in {0,1}. Correct (every Boolean solution has Boolean free values and is reached); time O(2^d r n) + elimination.
Theorem A. C0-SAT on n inputs is decidable in time poly(n,s) * min(2^{n/2}, 2^{n - rank A}). In particular T_C0(n,s) <= 2^n / n^{omega(1)}.
Control C (Boolean restriction): Gaussian elimination solves the affine problem in poly time; ALL remaining cost is the Boolean test of the
pivots (Lemma F) resp. matching of Boolean halves (Lemma M). 3^d GF(3) points are never enumerated, only 2^d Boolean free values.
Control B (expanders F(G)): rank = M = |V|+3|E| (proved earlier), d = 2|V|, n = 3|V|+3|E|; for 3-regular G, n = 7.5|V| and Lemma F runs in
2^{(4/15) n} poly; correct on the K4-plus-expander family (worst-case bound, constant core irrelevant for correctness).
Control A (Equality): Lemma M's interface has up to 2^{n/2} states, yet the matching step is a hash equality test - a large interface
does not imply large cost; no lower bound is inferred from interface size anywhere in this report.

## 3 Why this does NOT transfer to a new lower bound
Theorem O (C0 is too weak). Every function computed by a C0 circuit has 1-set V intersect {0,1}^n for a GF(3)-affine subspace V
(intersection of the gates' affine hyperplanes). OR_n (n >= 2) is not of this form: any affine V containing e_1, e_2 and e_1+e_2 contains
e_1 + e_2 - (e_1+e_2) = 0 (coefficients 1+1-1 = 1 mod 3), so it accepts 0. Hence OR_n has NO C0 circuit of ANY size (checked n = 2..7).
Consequence: lower bounds against C0 are trivial; a Williams-type transfer (which in addition needs closure of the class under the
AND/OR compositions used in its proof - C0 is not closed under OR) yields nothing new from Theorem A.
Richer classes. With bottom ANDs (C1 = AND o MOD3 o AND_k, degree-k polynomial systems over GF(3) with Boolean domain), Gaussian
elimination no longer applies; Lemma M survives only for splits that cut no monomial (cut monomials enlarge the interface by the cut
variables, Theta(n) in the worst case), so the GF(3) structure gives no provable 2^n/n^omega(1) saving by itself. Such classes lie in
ACC0, where SAT savings are already known (Williams' ACC0-SAT; algorithms for systems of low-degree polynomial equations over finite
fields beating brute force, Lokshtanov-Paturi-Tamaki-Williams-Yu), and the transfer consequences are at most the known NEXP / NQP not in
ACC0 (Murray-Williams). Exact hypotheses of the transfer theorems (circuit size, closure, deterministic vs randomized, exact vs
approximate counting) must be quoted from the papers before any further claim; this report claims no new separation.

## 4 Outcome (negative, precise)
- Proven: Lemma E, Lemma M, Lemma F, Theorem A, Theorem O (elementary; finite checks agree).
- Obstruction for THIS representation: GF(3) linearity gives a provable worst-case saving exactly on C0 (Theorem A), and C0 cannot
  compute OR (Theorem O), so no lower-bound transfer is new; adding bottom ANDs destroys the linearity the saving uses, and the remaining
  savings are those already known for ACC0. This is not a no-go theorem for all algorithms; it is a statement about the GF(3)-linear
  representation.
- First unproved step: a SAT/#SAT algorithm with savings 2^n / n^omega(1) (or the size/savings regime required by the invoked transfer)
  for a class that is NOT contained in ACC0 (e.g. with threshold gates) or strong enough for an NP-level consequence, in which the GF(3)
  kernel structure is actually used. No such algorithm or even a mechanism is known from our results.
- Novelty: Lemmas M/F are standard (meet-in-the-middle / elimination for Boolean solutions of linear systems mod p); Theorem O is an
  elementary observation. The contribution is the exact placement: where PNP-001's GF(3) structure helps algorithmically (C0) and why that
  place is below every open lower-bound frontier.
- Significance for P != NP: none directly. Polynomial calculus (degree Omega(n), Theorem 30), communication and ACC0 frontiers unchanged.
