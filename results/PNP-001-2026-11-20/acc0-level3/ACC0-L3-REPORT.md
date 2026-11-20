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

## 5 Addendum (2026-11-20): auxiliary variables - Lemma F' and the checklist
Lemma F' (determined existential auxiliaries). Let f(x) = exists y in {0,1}^k : A_x x + A_y y = b (mod 3). If A_y has full column rank k,
Gaussian elimination can take all k auxiliary columns as pivots; the free columns then lie in x and number n + k - rank(A) <= n.
Enumerating the Boolean free x-values, computing all pivots (x-pivots and y) mod 3 and checking them in {0,1} decides f exactly in
time poly * 2^{n - (rank(A) - k)}. Saving against 2^n iff rank(A) > k (more equations than needed to determine the auxiliaries).
Checklist (owner/peer): (1) C0 has k = 0, bound in n; C0-exists bound stated in n + k in general, in n under Lemma F'; no structural
parameter is used. (2) No GF(3)->Boolean encoding (all variables Boolean, GF(3) only as arithmetic), branching only on Boolean free
columns, every branch leaves a determined linear system. (3) No channelling: x(x-1)=0 is enforced by enumeration and an O(1) pivot check
per branch, never branched again; no hidden nonlinear terms.

## 6 Level 3b (2026-11-20): constructive transfer vs formal obstruction for linearising restrictions
Checks: l3b_checks.py (algorithm R exact for #SAT on 400 random degree-2 systems; branch ranks; padding; symmetric gate),
l3c_checks.py (class D membership n<=4, Delta identity 300 systems, NAND gadget, 40 gadget circuits). All exact, 0 violations.

### 6.1 Common definitions
- Variables: inputs x in {0,1}^n, Boolean existential auxiliaries y in {0,1}^k, t = n + k. All variables Boolean; GF(3) is arithmetic only.
- C^(d)-exists: AND o MOD3[=b] o AND_{<=d}: constraints p_j(x,y) = b_j (mod 3), p_j multilinear of degree <= d; f(x) = exists y.
- Auxiliary types: LINEARLY DETERMINED (aux columns of full column rank: y affine in x on the GF(3) solution space),
  BOOLEAN-FUNCTIONALLY DETERMINED (unique Boolean witness y = g(x), not necessarily affine), FREE existential. GF(3)-valued: not used.
- Class D := C^(1)-exists with linearly determined auxiliaries. Lemma D0: D = AND of equalities l(x)=c and DIS-equalities l(x)!=c over
  Boolean x. (<=: y = l - c - 1 in {0,1} iff l != c. =>: y = affine(x), and y_j in {0,1} iff affine_j(x) != 2.)  D is strictly larger
  than C0 (OR_2, NAND_2 in D; the "collapse to the base class" in the peer text is false because Booleanity of determined auxiliaries
  adds dis-equalities).
- Linearising restriction S (subset of all t variables): every monomial of degree >= 2 has at most one variable outside S.
- Algorithm R(S): for each sigma in {0,1}^S: Gaussian elimination mod 3 on the residual linear system; if consistent, enumerate the
  Boolean values of the free columns, compute pivots, accept/count iff all pivots in {0,1}.

### 6.2 Theorem R (cost, exact over all branches) - proved, numerically confirmed
R(S) decides SAT exactly and counts the complete Boolean solutions (x,y) exactly [CORRECTED 2026-11-20, owner: this is NOT the
projected count #{x : exists y A(x,y)=b} in general; see section 8]. Its cost is exactly poly(t, m) * [2^{|S|} + sum over GF(3)-consistent sigma of 2^{t-|S|-r(sigma)}]
<= poly * 2^{|S|} + poly * 2^{t - r_min(S)} = poly * 2^{n - Delta(S)} + poly * 2^{|S|},  Delta(S) := r_min(S) - k.
|S| cancels in the second term; the bound is a uniform worst case over ALL branches (not a favourable one). Restriction selection:
any vertex cover of the monomial graph (greedy, poly time) - Delta(S) need not be computed to run R. Branch-dependent ranks are covered
by the sum. Padding invariance: a determined padding variable (y - l(x) = c) raises r and k by 1 (Delta unchanged, checked); redundant
rows do not raise r; a forced input (x_i = c) raises Delta by 1 and is exactly an input reduction (n_eff = n - 1) - Delta is measured
against n_eff to exclude this inflation.

### 6.3 Constructive results (A)
- Theorem A (C0, earlier): min(2^{n/2}, 2^{n - rank}).
- Theorem D1 (exact Delta on D): in canonical form (E equalities, N dis-equalities, one aux each), rank[E 0; N I] - |N| = rank(E), and
  for EVERY restriction S: Delta(S) <= rank(E). So R decides D-SAT/#SAT in poly * 2^{n - rank(E)}; the saving is exactly the rank of the
  GF(3) EQUALITY part. Closure: AND of D-circuits stays in D with Delta >= max(Delta_1, Delta_2) (rank of union of equality sets);
  projections/restrictions of inputs keep D (Delta drops by at most 1 per fixed input, n by exactly 1); literal substitution x -> 1-x
  keeps D; OR of m D-circuits: SAT in sum_i 2^{n-Delta_i} (run each disjunct; saving minus log2 m), but OR is not inside D.
- Strongest proved positive statement: on D with rank(E) = omega(log n) (n_eff-measured), SAT and #SAT in 2^n / n^{omega(1)}.
  This is NOT a guaranteed surplus for the class: D contains NAE-3SAT (x_a+x_b+x_c != 0) with E empty, Delta <= 0 for every S.

### 6.4 Negative results (B)
- Theorem O' (Davenport obstruction): OR_n is in D iff n <= 2. Proof for n >= 3: the ones of OR_n have GF(3)-affine hull containing 0
  (Theorem O), so 0 must be excluded by a dis-equality l(x) != c with l(0) = c; any sequence of n >= 3 coefficients in Z_3 has a
  nonempty zero-sum subsequence T (Davenport constant D(Z_3) = 3), and the nonzero Boolean point 1_T has l(1_T) = c, so it is rejected
  although OR_n(1_T) = 1. Corollary: NAND_3 not in D (literal substitution), AND_3 in D: D is not closed under negation nor under
  fan-in-3 OR. (Checked: n = 3, 4; 236 of the 256 functions on 3 inputs lie in D; NAE_3 in D, NAE_4 not.)
- Theorem G (determined gate outputs are literals): a Boolean function g on {0,1}^a that is GF(3)-affine on the cube is a constant or a
  literal (two nonzero coefficients force a value 2). Hence any auxiliary computing a non-literal gate output is NOT linearly determined.
- Theorem H (affine-hull bound, all S): in every branch sigma, the free dimension satisfies t - |S| - r(sigma) >= dim aff_GF(3)(Sol_sigma)
  (Sol_sigma = Boolean solutions in the branch; Sol is contained in the GF(3) solution space). For unique-witness systems whose
  solution set is the graph of g on the whole cube plus c extra constraint rows: Delta <= c - rho(g), rho(g) = dimension of
  span_GF(3){g_1..g_k} modulo affine functions on the cube. Each GF(3)-independent non-literal gate output costs one unit of surplus.
  Example: the exact NAND gadget u+v+2z-w1 = 2, u+v+z-w2 = 1 has 2 rows, 3 auxiliaries, local Delta = -1; 40 random gadget circuits
  satisfy Delta <= 1 - rho.
- Consequences: (i) counting by R costs >= sum_sigma 2^{dim aff Sol_sigma} >= #{(x,y)} (complete solutions, not the projected count). (ii) On UNSAT inputs R costs the sum of 2^{free} over
  GF(3)-consistent branches: the expensive instances are exactly the GF(3)-blind ones (the PNP-001 blind cores; F(G) for
  non-3-colourable G: 2^{2|V|} = 2^{(4/15)n} for cubic G). (iii) Failed conjecture recorded: "guaranteed Delta = omega(log n) for
  C^(2)" is FALSE (single symmetric quadratic gate: r_min = 0; NAE-3SAT in D: Delta <= 0).
- The universal obstruction "forall C: Delta_guaranteed = O(log n)" is TRUE for every class containing NAE-3SAT in canonical form
  (Delta <= 0) and for every gadget closure (Delta <= c - rho); it is a statement about algorithm family R and the representation,
  not about all algorithms.

### 6.5 Controls
Equality EQ_n(x,x'): x_i - x'_i = 0, rank n, N = 2n inputs: R costs 2^{N/2} (large interface, cheap) - consistent. F(G): C0, Delta = rank,
2^{2|V|}; correct on expander + K4 (bounds are worst case). Satisfiable instances: early exit only lowers SAT cost; #SAT obeys (i).

### 6.6 Boundary, transfer, remaining obligation
- Exact boundary (both directions meet): Delta = (rank of the GF(3) equalities that constrain the inputs) - rho(non-affine
  Boolean-functional auxiliaries), with equality on D (rho = 0). Every source of expressiveness beyond C0 - dis-equalities in D,
  non-literal gate outputs in gadget closures - contributes 0 or -1 per unit to the surplus. Closure under negation/OR (needed by any
  Williams-type transfer) forces non-literal gate auxiliaries (Theorems O', G) and therefore drives Delta <= c - rho. So linearising
  restrictions + GF(3) elimination cannot supply the transfer hypothesis for a class closed under the transfer's operations.
- Comparison: savings on D and C0 lie inside ACC0-SAT savings already known; implications at most NEXP/NQP not in ACC0 (known).
  No new lower bound.
- First unproved statement: a #SAT/SAT algorithm for a class closed under AND/OR/NOT composition (beyond ACC0, or with an NP-level
  consequence) whose cost is NOT lower-bounded by enumeration of a GF(3)-affine superset of the solutions (Theorem H) - i.e. one that
  exploits cancellation or counting rather than the kernel dimension. No such mechanism follows from the GF(3) kernel structure.
- P != NP relevance: none directly; restricted-model and algorithm-family theorems only. Level 3 stays OPEN.

## 7 Level 3c (2026-11-20): guaranteed surplus over ALL restriction branches; formal checks; evidence audit
Checks: l3d_checks.py (Theorem L exact on 280 random systems, branch-sum example). Lean: formal/acc0l3/ACC0L3.lean
(Mathlib, sha256 1f00ba8be8e191af..., axioms propext/Classical.choice/Quot.sound only).

### 7.1 Theorem Sigma (branch-sum criterion) - proved
For a degree-d system and a linearising S, with free_a = t - |S| - r_a =: n - |S| - Delta_a (Delta_a = r_a - k):
T(S) = poly * ( 2^{|S|} + sum over GF(3)-consistent a in {0,1}^S of 2^{n-|S|-Delta_a} ) = poly * ( 2^{|S|} + 2^n * E_a[ 1_cons(a) 2^{-Delta_a} ] ).
Assuming poly(t, m) = poly(n) (auxiliaries and rows polynomial in n), a class has saving 2^n/n^{omega(1)} by R iff for every circuit an efficiently found S has 2^{|S|} <= 2^n/n^{omega(1)} and
E_a[1_cons 2^{-Delta_a}] <= n^{-omega(1)}. Sufficient (together with the 2^{|S|} condition): min over consistent a of Delta_a = omega(log n). NOT sufficient: a large average
Delta: by Jensen E[2^{-Delta}] >= 2^{-E[Delta]}, and one consistent branch with Delta_a = 0 already costs 2^{n-|S|}
(example n = 12, S = {x0}: Delta = 11 and 0; cost 2^1 + 2^0 + 2^11 = 2051, while two branches at the average Delta 5.5 would cost 2*2^5.5 ~ 91). Lemma F' must hold per branch; branches where it
fails are charged with their actual free dimension (the formula uses r_a, not an assumed full rank).

### 7.2 Theorem L (degree 1: restriction never raises the rank surplus) - proved, checked exactly
For a linear system over GF(3) with solution space V != {} in t Boolean variables and any S:
(i) every branch has the same residual matrix, hence the same rank r_S; (ii) branch a is consistent iff a in pi_S(V);
(iii) free dimension = t - |S| - r_S = dim V - dim pi_S(V); (iv)
  T(S) = poly * ( 2^{|S|} + |{0,1}^S cap pi_S(V)| * 2^{dim V - dim pi_S V} ) <= poly * ( 2^{|S|} + 2^{dim V} ).
Proof: fixing variables only moves their columns to the right-hand side (i); (ii) is the definition of the projection; (iii) the
residual solution set of a consistent branch is a fibre of pi_S restricted to V, of dimension dim V - dim pi_S V (rank-nullity); (iv)
an affine q-dimensional subspace contains at most 2^q Boolean points (it is a graph over q coordinates).
In the owner's notation Delta_a = Delta_0 - (|S| - dim pi_S V) <= Delta_0 on every consistent branch: restriction LOWERS the per-branch
surplus and the loss is repaid exactly by the inconsistent branches. The only gain beyond the unrestricted exponent dim V = n - Delta_0
is the Boolean sparsity beta_S = |{0,1}^S cap pi_S V| / 2^{dim pi_S V} of a projected affine space - and computing it is #C0-SAT on |S|
variables (self-reduction: no free lunch). Corollary for D (canonical form): dim V = n - rank(E), so T(S) <= 2^{|S|} + 2^{n-rank E}
so the exponent of the bound is n - rank(E) for every restriction, and per branch Delta_a <= rank(E) (equality only when pi_S is onto).
### 7.3 Status of the general obligation
- Degree 1 (C0, D): the guaranteed rank surplus after restriction is DETERMINED: Delta_0 = n - dim V, independent of S; all further gain
  is Boolean sparsity of projections (an instance of the original problem).
- Degree >= 2 (where linearising restrictions are needed): Theorem Sigma is the exact criterion; Theorem H bounds every branch
  (free_a >= dim aff Sol_a); gadget closures give Delta <= c - rho. A guaranteed omega(log n) bound over all branches for a
  composition-closed class is NOT proved and is false for the canonical gadget representation; whether some other representation of a
  composition-closed class achieves it is the open part.
### 7.4 Formal checks (independent of the validator's model judgement, not yet desk-accepted)
Lean 4.35 + Mathlib, kernel-checked, standard axioms only (file sha256 1f00ba8be8e191af...): or_not_C0 (claim:53f46be7d6fc);
or_not_D + or2_in_D + or1_in_C0 (claim:03fced129264 both directions; n = 0 trivial: OR_0 = dis-equality 0 != 0);
affine_bool_is_literal + affine_bool_classified (claim:1a3685a2808b complete: constant, u_i or 1-u_i). Independent fidelity review
(reviewer saw only code and claim texts): or_not_C0 MATCH; the other two were WEAKER (missing direction / finishing step) - both gaps
closed afterwards; Theorem L CORRECT; Theorem Sigma CORRECT with the poly(t,m) = poly(n) assumption (added) and the corrected example. Not formalised: running-time claims (claim:247c31e61b92, claim:bf65731be859 rank identity,
claim:ea42f7f7fa39 affine-hull bound) - paper proofs above.
### 7.5 Evidence audit (owner request)
All 3,244 agent ledger entries checked against primary sources (lab register, run files, datasets, trace): dataset/column citations 0
failures; 12 entries with run ids unknown to the observed-id index - 10 cite real executed runs (index fixed, cc60940), seq 2895 cites a
failed run but says so and rests on real runs, seq 154 predates the trace. Fabricated evidence: only R0400 / HYPOTHESIS seq 4825 -
RETRACTED (INVALID_RESULT). R0396 recorded no evidence entry; its FINAL's "numerical evidence" has no primary source.

## 8 Correction (owner, 2026-11-20): counting semantics of algorithm R
R enumerates complete Boolean solutions of A(x,y) = b, so it counts PAIRS (x,y). The projected count #{x : exists y} is a different
quantity: the constraint x = 0 with one free auxiliary y has 2 pairs and 1 accepted input (l3e_checks.py). Corrected statements:
- SAT: exact for every representation (unchanged).
- #SAT over all variables (pairs): exact (unchanged; the earlier tests compared exactly this).
- Projected #SAT on the original inputs: exact iff every accepted x has exactly one witness y. Holds for class D (linearly determined
  auxiliaries: y is an affine function of x; 0 mismatches in 300 random D systems) and for unique-witness (Boolean-functionally
  determined) gadget representations such as the NAND gadget of section 6.4. Fails in general for free auxiliaries (122 of 300 random
  C0-exists systems differ). For free auxiliaries R gives only the upper bound #{x} <= #{(x,y)}; projected counting would need a
  per-input existence test (a C0-SAT instance on the auxiliaries), which this report does not analyse.
- Consequence for transfers: only SAT and unique-witness counting results of this report may be fed into SAT/#SAT transfer theorems
  on the original circuit inputs.
R0404 (OR_n with n-1 auxiliaries, rank n): NO evidence - its only successful lab run returned a hard-coded placeholder ("m = 4 # Example
value"), three dataset reads failed, the dataset and the cited law:acc0_c0_exists_or_* ids do not exist. It is an unsupported claim,
not k_min(OR_n) <= n-1; even a verified construction would give only an upper bound on k_min. Not part of this report's results.

## 9 Brute force (2026-11-20): every GF(3)-linear representation with Boolean existential auxiliaries, n + k <= 7
brute/repr_brute.c enumerates every affine subspace V of GF(3)^{n+k} exactly once (184 / 2,452 / 53,968 / 1,996,024 / 125,850,208
for t = 3..7, matching the Gaussian-binomial counts), takes Sol = V cap {0,1}^t, projects onto the n inputs (k Boolean existential
auxiliaries), and records per function the minimal dim V (= best rank surplus Delta = n - dim V; by Theorem L no restriction improves
this exponent) with and without the unique-witness condition. Analysis: brute/analyse.py, brute/check_tight.py, brute/summary.json.
Results (exact for the stated ranges, k <= 7 - n):
- n = 3: nonzero functions by k_min: 57 (k=0), 72 (1), 106 (2), 20 (3); all 255 representable. n = 4 (k <= 3): 473 / 1,776 / 5,770 /
  20,260; 37,256 functions (incl. OR_4, MAJ>=2, ...) need k >= 4.
- k_min(OR_3) = k_min(NAND_3) = 3 and their best surplus is -1 (dim V = 4 > n); OR_4 needs k >= 4. NAE_3: k = 1, Delta 0;
  MAJ_3, PARITY_3: k = 2, Delta 0; NAE_4: k = 3, Delta -1.
- Theorem H bound Delta <= n - dim aff_GF3(f^{-1}(1)) is never exceeded; it is attained EXACTLY for the functions in D
  (n = 3: 235 + 20; n = 4: 26,339 at the bound all in D, 1,940 below it none in D - no exception among 28,279 representable functions).
Theorem B (proved; suggested by the brute force): for every representation f(x) = exists y in {0,1}^k: A(x,y) = b,
  Delta = n - dim V <= n - dim aff_GF3(f^{-1}(1)), with equality only if the representation's auxiliaries are linearly determined,
  hence only if f is in D.
Proof: pi(V) is affine and contains f^{-1}(1), so dim V >= dim pi(V) >= dim aff f^{-1}(1). Equality forces dim V = dim pi(V), i.e.
pi is injective on V, so y is an affine function of x on V: every auxiliary is linearly determined and f is in D (Lemma D0). QED.
Corollary: every function outside D pays at least one unit below its affine-hull bound in EVERY representation, whatever the number
of auxiliaries; full-hull functions outside D (OR_n, NAND_n for n >= 3, NAE_4, ...) have Delta <= -1.
Meaning and limit: the rank surplus is a property of the function, not of a clever choice of auxiliaries - auxiliaries buy
expressiveness only by spending surplus. This concerns representations of the function computed (satisfiable side). For SAT the hard
instances are unsatisfiable ones, where Sol is empty and Theorem B says nothing; there the cost is governed by GF(3)-blind solution
spaces (PNP-001 blind cores). That remains the open part of Level 3; brute force at n <= 4 does not decide the asymptotic question.

## 10 Second route, step 1 (2026-11-20): lambda of the DIRECT holographic translation of circuits
Files: holo/gates/ (*.json inputs for lab/onein3/matchgate_miner.py, gates_groebner.py independent Groebner check with the reviewer's
MGI code, lambda_circuits.py measurement).
Setting: bipartite signature grid gates | wires; gate vertex = relation [c = g(a,b)] (arity 3) transformed by T^{x3}; wire vertex =
EQ_d transformed by (T^{-1})^T (up to scalar adj(T)^T); planar matchgates (Cai-Gorenstein MGI); one T in GL2(C) for the whole grid.
Theorem MG-C (computational proof, two independent methods agree: exact solver PROVED_NO_BASIS and Groebner basis {1} over Q):
  for g in {AND, OR, NAND}: no T makes g and EQ_d both matchgates, for d = 2, 3, 4 - even without fan-out (d = 2);
  XOR: a common basis exists with EQ_2, none with EQ_3, EQ_4; NOT: a common basis exists with EQ_2, EQ_3, EQ_4.
Lemma S: a signature with at most one nonzero entry is a planar matchgate (tensor product of unary matchgates), so every
  non-matchgate vertex contributes log2|supp| >= 1 to lambda.
Corollary (proved from MG-C + S): for circuits over {AND, OR, NAND, XOR, NOT} with fan-out <= 3 (wire arity <= 4), in the direct
  translation under ANY single GL2 basis: either every nonlinear gate (AND/OR/NAND) is a non-matchgate, or every wire vertex is
  (and there are at least as many wires as gates); hence lambda >= N_nonlinear (crossings not even counted). So the direct
  translation beats brute force (lambda <= n - omega(log n)) only for circuits with fewer than n - omega(log n) nonlinear gates -
  a weak class (few AND gates), not a new lower-bound route.
Measurement (random NAND circuits, fan-out <= 3, constructed one-page drawing, exact counts):
  n = 8..64, s = n..8n: crossings grow ~quadratically (36 at n = s = 8; 118,959 at n = 64, s = 512), lambda_std = 2s + #EQ_{>=3} +
  2 cr (93 ... 239,270), and the basis-independent lower bound lambda >= s >= n holds in every case. Crossings dominate.
Meaning: MG-3 extends from EXACT1_3 to every nonlinear gate; for the direct translation lambda grows with the circuit size s, not
with n. The holographic route can only work through GADGETS / super-signatures (several vertices fused, higher-dimensional bases)
or through drawings with few crossings - exactly the parts MG-C does not cover. That is the remaining open part of this route.

## 11 Rung 4 (2026-11-20): transfer to roABP-IPS_LIN for lifted F(G), and what stronger systems lose
Sources (local copies, not redistributed): ECCC TR26-070 (Hakoniemi-Limaye-Tzameret 2026), literature/sources/eccc-TR26-070;
Pitassi-Robere, "Lifting Nullstellensatz to monotone span programs over any field", STOC 2018 (ECCC TR17-165),
literature/sources/eccc-TR17-165. Statements used, checked in the source text:
[PR18 Def 2.1] algebraic tiling of KW+(f): matrices A_i with sum A_i = J (all-ones), A_i embedded in the coordinate rectangle X_i;
  size = sum rank_F(A_i); chi_F(f) = minimum size. [PR18 Thm 2.2, Gal] mSP_F(f) = chi_F(f).
[PR18 Def 2.11 + Sec. 3] KW+(f_{C,g}) is (up to renaming) the canonical search problem CanSearch(C,g) on X^n x Y^n with rectangles
  X_{pi,alpha} = {(x,y) : g^n(x,y) consistent with the certificate pi, x restricted to vars(pi) = alpha}.
[PR18 Thm 1.1] C unsatisfiable CNF on n variables, F any field, g good over F (Def 3.1) with rank(g) = n^2: chi_F(f_{C,g}) =
  n^{Theta(NS_F(C))}; if NS_F(C) = Theta(n), then for every good gadget of sufficiently large constant rank chi_F(f_{C,g}) = 2^{Theta(n)}.
[TR26-070 eq. (0.2)] roABP-IPS_LIN refutation: sum_i g_i f_i + sum_j h_j (x_j^2 - x_j) = 1 with g_i, h_j roABPs; width = max width.

Lemma T (proved here). Let C = C_1..C_m be an unsatisfiable k-CNF on z_1..z_n, g : {0,1}^p x {0,1}^q -> {0,1} a gadget, and C o g the
standard lifted CNF: for every clause C_j with falsifying assignment beta_j and every (u, v) in ({0,1}^p x {0,1}^q)^{vars(C_j)} with
g(u_i, v_i) = beta_j(i) for all i, the clause D = NOT(x_{vars(C_j)} = u AND y_{vars(C_j)} = v), arithmetised as Q_D = R_D(x) S_D(y)
(product of literal indicators). If C o g has an roABP-IPS_LIN refutation of width w over F in a variable order in which all x-bits
precede all y-bits, then KW+(f_{C,g}) has an algebraic tiling of size <= w * m * 2^{k(p+q)}.
Proof. On the Boolean cube the Boolean-axiom terms vanish, so sum_D a_D(x,y) R_D(x) S_D(y) = 1 for all (x,y). As an
X^n x Y^n matrix, a_D has rank <= w: at the x|y cut of an roABP of width w, a_D = sum_{t<=w} L_t(x) M_t(y), and evaluation rank on the
cube is at most this. (Renaming, PR18 Prop 2.10: x -> u^x need not be injective; keep one representative row/column per class - a
submatrix, rank does not grow, supports stay inside the rectangles, the sum stays J; X_{pi,alpha} is a combinatorial rectangle.)
B_D := diag(R_D) a_D diag(S_D) has rank <= w and support inside {x_{vars(C_j)} = u, y_{vars(C_j)} = v}, which lies
inside X_{pi_j, u} (g^n(x,y) falsifies C_j, x on vars(C_j) equals u). Grouping B_D by (j, u) gives matrices embedded in the canonical
rectangles that sum to J, of total rank <= w * #clauses(C o g) <= w m 2^{k(p+q)}. QED
Theorem 4.1 (rung 4, fixed order; from Lemma T + PR18 Thm 1.1). For C a k-CNF with k = O(1) and g as in PR18 Thm 1.1 with
Boolean-encoded domains X = {0,1}^p, Y = {0,1}^q (PR18's field-independent good gadget h_lambda lives on [lambda+1] x [lambda+1]:
take lambda + 1 = 2^p, or prove that zero-padding keeps h_lambda good - OPEN DETAIL), every roABP-IPS_LIN refutation of C o g
over F with all x-bits before all y-bits has width >= chi_F(f_{C,g}) / (m 2^{k(p+q)}): n^{Omega(NS_F(C))} / poly for rank(g) = n^2,
and 2^{Omega(n)} / poly when NS_F(C) = Theta(n) and g is a good gadget of large constant rank.
Lemma N (proved here; degree of F(G) as a CNF). Write F(G) as the 3-CNF with, per positive 1-in-3 clause (a,b,c), the clauses
(a v b v c), (-a v -b), (-a v -c), (-b v -c). Then NS_F(Col(G)) <= NS_F(F(G)) for every field F (exact, no loss - review 2026-11-20), where Col(G) is the indicator
encoding of 3-colouring used by Lauria-Nordstrom. Proof: substitute y_{uwc} := 1 - x_uc - x_wc (affine, degree does not increase). The
images of the edge-clause axioms and of y^2 - y reduce, modulo Boolean axioms in degree <= 3, to multiples of x_uc x_wc (e.g.
(1-a)(1-b)(a+b) = 0, a(1-a-b) = -ab, (1-a-b)^2-(1-a-b) = 2ab); the vertex clauses generate 1 - sum_c x_vc and x_vc x_vc' in degree 3
and conversely. QED. With Lauria-Nordstrom (arXiv 2306.00125, Thm 3.7, checked at the source: graphs with O(k^4 n) vertices of degree O(k^2), encoding
(2.2a)-(2.2c) = Col(G), PC degree Omega(n), field-independent per Thm 1.1; NS >= PC) and n_vars(F(G)) = 3|V| + 3|E| = Theta(|V|):
NS_F(F(G)) = Theta(n).
Corollary 4.2 (rung 4 for lifted F(G)). For the Lauria-Nordstrom graph families and every field F, F(G) o g (g good, large constant
rank) requires roABP-IPS_LIN refutations of width 2^{Omega(n)} in every order with x-bits before y-bits. Arbitrary orders: TR26-070
Sec. 4 lifts order-specific hardness to all orders for 3-CNFs; F(G) o g is a k(p+q)-CNF of constant width - the extension of Sec. 4
to constant-width k-CNFs (or a 3-CNF re-encoding preserving the bound) is the remaining check.
Status: Lemma T, Lemma N proved here; Theorem 4.1 = Lemma T + PR18 Thm 1.1 (cited, checked in the source). This is the transfer the
owner asked for, and matches TR26-070's attribution to Sokolov. It concerns the LIFTED formula (no longer positive 1-in-3).

What a STRONGER system loses (explicit):
(S1) roABP-IPS (non-linear in the axioms): C(x,y,f) with C(x,y,0) = 0, C(x,y,Q) = 1. Expanding in placeholder monomials gives
  sum_M c_M(x,y) prod_D Q_D^{M_D} = 1; every term is still embedded in a canonical rectangle, but the number of terms is the number of
  placeholder monomials, which an roABP of width w can make exponential. Limit of THIS argument: Lemma T's tile count needs linear
  axiom use; that linearity is necessary for every transfer is NOT proved.
(S2) multilinear-formula IPS / no fixed order: Lemma T needs ONE cut (x | y) of rank <= w. Raz's method gives only a rank DEFICIT
  under random partitions, not small rank, and e.g. prod_i (x_i + y_i) has full rank at the x|y cut. Lost property: a fixed low-rank cut.
(S3) constant-depth IPS without individual-degree bounds: simulates AC0[p]-Frege over F_p, which has no GENERAL feasible interpolation
  unless Diffie-Hellman is computable by 2^{n^eps}-size circuits (TR26-070 Sec. 1.3, citing [BDG+99]). Lost property: general feasible
  interpolation (conditional). This does NOT exclude a Lemma-T-type transfer for LIFTED formulas C o g (the Diffie-Hellman formulas
  are not of that form) - corrected after review.
(S4) Control: F(G) as a CNF contains no XOR; in the separate XOR/carry representation the XOR (Tseitin-type) part is easy for
  roABP-IPS_LIN (TR26-070 Sec. 5). The hardness of F(G) o g comes from the colouring part through NS degree (Lemma N).
Independent review 2026-11-20 (reviewer saw only this section and the two source texts): Lemma T CORRECT, Theorem 4.1 CORRECT for
constant k, Lemma N CORRECT (exact inequality), Corollary 4.2's named gap is the right one; fixes applied above (renaming line, k = O(1),
exact Lemma N, S1-S4 wording). Open: (i) gadget domain {0,1}^p for h_lambda; (ii) TR26-070 Sec. 4 for constant-width k-CNFs
(N^K selectors per clause plus a matching consistency part).

## 12 Corollary 4.2 completed (2026-11-20): all variable orders, every field, explicit family
Closes the two open checks of section 11. Mechanical check: rung4/order_lift_check.py.
Gap (i) closed - gadget domain. PR18 Def. 4.1 defines h_lambda : [lambda+1] x [lambda+1] -> {0,1} (identity with one 1 deleted) for EVERY
positive integer lambda; PR18 Lemma 4.2: h_lambda is good over every field and rank(h_lambda) = lambda. Take lambda = 2^p - 1: then
[lambda+1] = [2^p] is in bijection with {0,1}^p, so Lemma T applies verbatim with X = Y = {0,1}^p, no padding.
Gap (ii) closed - order lifting for constant width (Lemma O). Let phi be an unsatisfiable CNF on x_1..x_N with M clauses of width <= K, no clause repeating a variable,
hard for roABP-IPS_LIN in the fixed order x_1 < ... < x_N. Psi_K(u,v) = Phi1 /\ Phi2: for every clause C of phi and every tuple t of |C|
DISTINCT indices in [N], a selector u_{C,t} and the clause (NOT u_{C,t}) v OR_j v_{t_j}^{sg(l_j)}; Phi2 = "exactly one selector per clause"
+ "no two incompatible selectors" (partial maps v -> x not one-to-one), exactly as TR26-070 Def. 15/16. Size: M N^K selectors, poly for
constant K. Claim: (a) Psi_K is unsatisfiable; (b) a roABP-IPS_LIN refutation of Psi_K of width w in ANY order gives one of phi of width
<= w in x_1 < ... < x_N.
Proof: TR26-070 Prop. 17 and Thm. 18 verbatim - neither proof uses the clause width: (a) any u satisfying Phi2 selects one tuple per
clause from one global one-to-one map, the surviving Phi1 clauses are a relabelled copy of phi; (b) for an order <, relabel the r-th
v-variable (in <) as x_r, set u_{C,t} = 1 exactly for the tuple realising C under this relabelling. Then Phi2 is satisfied (its clause
polynomials, in u only, become 0), Phi1 clauses with selector 0 have the factor u_{C,t} = 0, the Boolean axioms of u vanish, and the
selected clauses become exactly phi in the order x_1 < ... < x_N. Substituting constants and renaming variables does not increase roABP
width. QED. Checked mechanically on 5 unsatisfiable CNFs with clause widths 1-4 and mixed signs, 20 random orders each: restriction
equals phi in the hard order every time, Psi unsatisfiable (SAT solver).

Theorem 12 (Corollary 4.2, complete). Fix the Lauria-Nordstrom family G_n (arXiv 2306.00125 Thm 3.7, k = 3: O(n) vertices of degree
O(1), not 3-colourable, encoding (2.2a)-(2.2c) needs PC degree Omega(n) over every field). Let F(G_n) be the 3-CNF of section 11, with
NS_F(F(G_n)) >= c n and N_0 = #vars(F(G_n)) = Theta(n), so NS_F >= eps N_0 for a constant eps > 0 (Lemma N). Choose a constant p with
2^p - 1 > 2^{1/eps}, g = h_{2^p - 1} on {0,1}^p x {0,1}^p, phi_n = F(G_n) o g (a 6p-CNF on 2pN_0 variables with at most m_0 * 2^{6p} clauses, m_0 = #clauses(F(G_n)) =
Theta(n)), sigma = any order with all x-bits before all y-bits, and Psi_n = Psi_{6p}(phi_n) built for sigma (Lemma O).
Then for EVERY field F and EVERY variable order, every roABP-IPS_LIN refutation of Psi_n over F has width 2^{Omega(n)}; Psi_n has
poly(n) variables and clauses (degree of the polynomial O(p), p constant).
Proof: Lemma O(b) reduces any order to phi_n in sigma with no width increase; Theorem 4.1 (Lemma T + PR18 Thm 1.1 for NS = Theta(N_0) and
a good gadget of constant rank > 2^{1/eps}) gives width >= chi_F(f_{F(G_n),g}) / (#clauses of phi_n) >= 2^{Omega(N_0)} / poly(n).
Lemma O(a) and unsatisfiability of phi_n (F(G_n) unsatisfiable, lifting preserves unsatisfiability) make Psi_n a valid instance. QED
Independent validation 2026-11-20 (reviewer saw only sections 11-12 and the three source texts): Theorem 12 PROVED as stated; every
link CORRECT (gadget, constant-rank case incl. mu_F <= chi_F via PR18 Thm 2.4 and NS = gap via Thm 3.5, Lemma T on phi_n, Lemma O,
unsatisfiability, size). Wording fixes applied (Omega instead of Theta; no repeated variables in Lemma O). Caveats: the proof of PR18
Thm 3.4 is deferred to the full version in the STOC text (we rely on the published statement); the polynomial size of Psi_n has degree
O(p) with p ~ 1/eps from the Lauria-Nordstrom constants - astronomically large in practice, irrelevant for correctness; the mechanical
script checks only the selector combinatorics on toy CNFs, not the polynomial identities.
Scope (unchanged): roABP-IPS_LIN only; the instance is the doubly lifted formula, not positive 1-in-3 itself; no statement about stronger
systems or algorithms.

## 13 Owner steps 2026-11-20: target statements, degree experiment, barrier test
### 13.1 Target statements (binding form: "family X needs degree/size ... in proof system Y over field(s) F" - a lower bound against a
RESTRICTED class, labelled as such)
- PROVED (paper proof, independently reviewed; formalisation of Lemma N pending): X = F(G_n) (Lauria-Nordstrom graphs), Y = Nullstellensatz
  and polynomial calculus, degree Omega(n), every field (Lemma N + Lauria-Nordstrom Thm 3.7).
- PROVED (independently validated): X = Psi_n (doubly lifted), Y = roABP-IPS_LIN, width 2^{Omega(n)}, every field, every order (Thm 12).
- KNOWN (literature, to be cited exactly before use; not ours): subset sum sum x_i = beta without Boolean root - linear degree in PC
  (Impagliazzo-Pudlak-Sgall 1999) and exponential roABP-IPS_LIN size (Forbes-Shpilka-Tzameret-Wigderson); Tseitin on expanders - linear
  degree over characteristic != 2 (Buss-Grigoriev-Impagliazzo-Pitassi), degree O(1) over F2.
- OPEN: X = Psi_n, Y = full roABP-IPS (rung 4b).
### 13.2 Experiment (groebner/gdeg.py, groebner/nsdeg.py; supports hypotheses, proves nothing)
Measure A (Singular std with degBound = d over F[x]/(x^2 - x)): NOT reliable as a degree invariant - returns degrees above n + 1
(Tseitin K4, 6 variables: 7) and is non-monotone (subset sum: ">7" at n = 5, 7 at n = 6); it counts non-multilinearised intermediate
degrees. Reported but not used. Measure B (exact multilinear Nullstellensatz degree by linear algebra mod p; CONVENTION: the smallest d such that 1 lies in the span
of the multilinearised products m * p_i with deg m + deg p_i <= d - state this convention whenever comparing with published NS/PC
theorems): Tseitin K4 / K33 / prism:
F2 = 1, 1, 1 versus F3 = 6, 7, 6 (XOR-SAT control: linear over F2, high over F3, as the literature predicts); subset sum sum x = n + 1 over
F101: exactly n + 1 for n = 2..8 (consistent with the functional argument: the coefficient equals 1/(sum x - beta) on the cube, of full
degree n; over fixed F101 the instance is unsatisfiable only for n <= 99 - for n >= 100, sum x = n - 100 is a Boolean solution mod 101,
so this is no infinite family); colouring encoding of K4: 3 over F2 and F3 (matches R0427). Small instances cannot show the asymptotic Omega(n) of F(G_n).
### 13.3 Barrier test of every open inference in this manuscript
Filter: an inference that claims a separation of complexity classes must state its quantifier structure and why it does not relativise
(Baker-Gill-Solovay), is not a natural proof (Razborov-Rudich: constructive + large property), and does not algebrise (Aaronson-
Wigderson). [CORRECTED 2026-11-20, owner:] arithmetisation and linear-algebraic techniques must be examined for algebrization under
the formal Aaronson-Wigderson definition (validity relative to oracles and their low-degree extensions); their use alone does NOT
establish that a proof algebrizes. A claimed P != NP proof must identify how it overcomes each applicable barrier; natural proofs is a
barrier only for properties that are constructive and large, under a pseudorandom-function hardness assumption.
- Theorems A, B, G, H, L, O', Lemma F' (GF(3) route): statements about the algorithm family R / representations - no class separation
  claimed; filter not triggered.
- Theorem 12, Lemmas T, N, O; MG-3, MG-C: lower bounds for fixed proof systems / fixed representations - no class separation claimed.
- Open: rung 4b (full roABP-IPS) - a proof-system statement; general IPS lower bounds imply VP != VNP (Grochow-Pitassi), the known wall.
- Open: algorithmic transfer (Williams-type) from a SAT saving - relies on cited external transfer theorems; no own saving claimed.
- NOT present and NOT claimable from these methods: any inference from a restricted-system lower bound to "no polynomial SAT algorithm".
  It fails on the quantifier gap (fixed proof system vs all algorithms); whether our arguments (degree, rank, tiling over fields)
  algebrize has NOT been examined under the formal definition - an open check, not a settled fact.

### 13.4 Literature: ECCC TR25-080 (Elbaz, Govindasamy, Lu, Tzameret, 2025; local copy literature/sources/eccc-TR25-080)
Checked at the source: lower bounds over FIXED finite fields for constant-depth multilinear IPS_LIN' (knapsack mod p) and for
roABP-IPS_LIN' in every variable order (Thm 3 / Cor. 43 functional method; Thm 4 / Thm 46 lower bound by multiples). IPS_LIN' (their
Def. 9) is linear in the AXIOM placeholders y and may be non-linear only in the Boolean-axiom placeholders z - so these are NOT bounds
for non-linear use of the axioms (our rung 4b). The roABP bounds are PLACEHOLDER bounds (instances not computable by small roABPs), not
CNFs. Their Thm 49 (main text, p. 31; the intro summary Thm 5 says LIN'): "The functional lower bound method cannot establish
non-placeholder lower bounds on the size of roABP-IPS refutations when working in finite fields" - stated for (full) roABP-IPS. Its proof
is our breaking point B1: g = ml(f^{p-2}) equals 1/f on the cube and has a small roABP in every order (roABPs are closed under
multilinearisation, FSTW Prop. 4.5 = their Prop. 48); a linear refutation is also a full roABP-IPS refutation. B1 (claim:75698fb31560)
is thereby an independently published fact. Scope: a limit of the FUNCTIONAL METHOD, not of every lower-bound technique. Use for R4b: technique anchor (finite fields, lower bound by multiples, set-multilinearisation),
not a solution.

## 14 Cell M9, partial result (director 2026-11-20): full roABP-IPS with bounded placeholder degree
Setting. C o g a lifted CNF with m' clauses and clause polynomials Q_D(x,y) = R_D(x) S_D(y) (Lemma T). A full roABP-IPS refutation is an
roABP C(x, y, z, w) of width W in some total order of all variables, z_D placeholders for the clause axioms, w_j placeholders for the
Boolean axioms, with C(x,y,0,0) = 0 and C(x, y, Q, x^2 - x) = 1 as a formal polynomial identity (formal source: TR25-080 Def. 9,
which has separate Boolean-axiom placeholders; TR26-070 Def. 3 lists the Boolean axioms among the axioms - equivalent here). Placeholder degree t(C): the
largest number of distinct z-variables in a monomial of the multilinearisation ml_z C(x,y,z,0).
Lemma T* (proved here). If all x-bits precede all y-bits in the order (z and w anywhere), then KW+(f_{C,g}) has an algebraic tiling of size
<= W * sum_{s=1}^{t(C)} binom(m', s).
Proof. (a) Set w = 0: still an roABP of width <= W, and on the Boolean cube C(x,y,Q,0) = 1 (the Boolean axioms vanish there).
(b) On the cube every z_D takes the value Q_D(x,y) in {0,1}, so C(x,y,Q,0) = C~(x,y,Q) with C~ = ml_z C(x,y,z,0) = sum_S c_S(x,y) z^S;
c_empty = C(x,y,0,0) = 0. Hence for every (x,y): sum over non-empty S contained in F(x,y) of c_S(x,y) = 1, F(x,y) = falsified clauses.
(c) Rank: at the cut between the last x-bit and the first y-bit, C = sum_{r <= W} L_r(x, z_L) R_r(y, z_R) with disjoint placeholder sets
z_L, z_R; ml_z acts separately on both factors, so c_S = sum_r [coeff of z^{S_L} in ml L_r](x) * [coeff of z^{S_R} in ml R_r](y): rank <= W.
(d) Tiles: B_S := diag-restriction of c_S to {all clauses in S falsified} = c_S o prod_{D in S} Q_D; each Q_D is a rank-1 0/1 indicator,
so rank B_S <= W, and supp B_S lies in the falsification set of every D in S, hence in the canonical rectangle of D_min(S) (as in Lemma T).
Grouping the B_S by the rectangle of their smallest clause gives matrices embedded in canonical rectangles that sum to J, of total rank
<= W * #{S : c_S != 0} <= W * sum_{s <= t} binom(m', s). QED
Theorem 14 (partial M9). For the family of Theorem 12, every field F and every variable order: every full roABP-IPS refutation of Psi_n
with placeholder degree t has width >= 2^{Omega(n)} / binom(m', <= t), m' = Theta(n) clauses of phi_n. Since binom(m', <= alpha m') <=
2^{H(alpha) m'}, the width is 2^{Omega(n)} whenever t <= c' n for a suitable constant c' > 0 (improvement by the review; the earlier
threshold c n / log n is superseded).
Proof. Lemma O extends: restricting the selectors sets the placeholders of satisfied Psi-clauses to 0 (their axioms become 0), which keeps
an roABP of width <= W and does not increase the placeholder degree; the order restricts to sigma (x-bits before y-bits). Then Lemma T*
and Pitassi-Robere Thm 1.1 as in Theorem 12. QED
Why the degree bound is essential for THIS method (not a lower-bound obstruction): C = 1 - prod_D (1 - z_D) + (Boolean-axiom part) has
placeholder degree m'; its restriction C(x,y,z,0) = 1 - prod_D (1 - z_D) has width 1 and does not depend on the formula, so NO argument
that looks only at the w = 0 restriction can give a bound for such certificates; its multilinear coefficients are c_S = (-1)^{|S|+1}, and the tiling bound becomes 2^{m'} - useless. In such
certificates all difficulty moves into the Boolean-axiom part sum_j h_j w_j, which must certify prod_D (1 - Q_D) = 0 modulo x^2 - x.
OPEN remainder of M9: full roABP-IPS refutations of unbounded placeholder degree - plausibly via a width lower bound for the
Boolean-axiom part (a roABP certificate that prod_D (1 - Q_D(x,y)) lies in the Boolean ideal).
Status: paper proof by the director; INDEPENDENTLY REVIEWED 2026-11-20 - "proved as stated": steps (a)-(d), the extension of Lemma O
and the final bound CORRECT, example correct and not overstated, no counterexample; corrections applied (formal source TR25-080 Def. 9; threshold t <= c' n; sharper example wording). Works over every field.

## 15 Lemma 15 (M9-S, owner proposal 2026-11-20): sparse-placeholder linearisation for CNF axioms
Statement. Let Phi be an unsatisfiable CNF over a field F, axioms Q_1..Q_M = clause polynomials (products of univariate factors 1 - x_i
and x_j) and Boolean axioms x_j^2 - x_j (univariate). Let C(x, z) be a full IPS refutation (C(x,0) = 0, C(x,Q) = 1 as polynomials,
TR25-080 Def. 9) computed by an roABP of width w in an arbitrary total order of x and z, with t distinct z-monomials (z^alpha, alpha != 0)
in C = sum_alpha c_alpha(x) z^alpha. Then Phi has a roABP-IPS_LIN refutation whose coefficients have width <= t w in the order induced on x.
Proof. (i) Coefficient extraction: replacing, in every z-layer, each edge label by its coefficient of z_j^{alpha_j} gives constant
matrices (alpha_j = 0: constant term; consecutive z-layers multiply into one matrix; a z-layer at either end merges into the first/last
x-matrix); multiplying them into the adjacent x-layers yields an roABP for c_alpha(x) of width <= w in the induced x-order. (ii) For each
alpha choose i(alpha) with alpha_i >= 1 and set h_alpha(x) = c_alpha(x) Q_i^{alpha_i - 1} prod_{j != i} Q_j^{alpha_j}. Every Q is a product of
univariate polynomials, so multiplying by it only multiplies edge labels layer by layer (a variable without a layer first gets a
trivial identity layer): width stays <= w. (iii) g_i = sum_{alpha: i(alpha)=i}
h_alpha has width <= t w (sum of <= t roABPs in the same order). (iv) sum_i z_i g_i(x) vanishes at z = 0 and at z = Q equals
sum_{alpha != 0} c_alpha(x) Q^alpha = C(x,Q) - c_0 = 1, since c_0 = C(x,0) = 0. Every field. QED (cf. Grochow-Pitassi, arXiv 1404.3820, Prop. 2.1: sparse IPS certificates convert
to Hilbert-like ones; the non-sparse case is their Open Question 1.13.)
Corollary (via Theorem 12). For Psi_n: t * w >= 2^{Omega(n)}.
Relation to Theorem 14 (honest): Lemma T* already gives tiling size <= W * #{S : c_S != 0} <= W * t, hence the same corollary, and the
stronger degree consequence (placeholder degree > c' n for polynomial width, counting only clause placeholders after multilinearisation).
Precisely: t and the placeholder degree are incomparable parameters; Lemma T* gives W * min(t, binom(m', <= t(C))) and covers both.
Lemma 15 is an independent second route (a direct simulation full -> LIN with width loss t, invariance-matrix style), not a new bound.
Unlike Grochow-Pitassi Prop. 2.1 it needs no bound on the individual placeholder degree and no field-size condition (coefficients are
read off the roABP exactly instead of Zippel interpolation).
Status: INDEPENDENTLY REVIEWED 2026-11-20 - proved as stated over every field (extraction, univariate products, sums, validity,
Grochow-Pitassi comparison, relation to Lemma T* all CORRECT; wording fixes applied).

## 16 Cell M9b: rank of P_Psi in every order (2026-11-20; repaired argument by an external reviewer + director's selector scheme)
Lemma M9b' (repair). Let (U,V) be a cut of the variables of a CNF F, P_F = prod_D (1 - Q_D). Let M be K pairwise variable-disjoint clauses
crossing the cut, and assume that after a substitution of field elements for ALL variables except the variables of the M-clauses that
stay free (in Theorem 16: all except M's v-variables; M's selectors are substituted too) every remaining non-M factor depends
only on U or only on V and is a non-zero polynomial. Then rank_{U|V}(P_F) >= 2^K over every field.
Proof. (1) Substituting field elements (possibly from an extension) is a linear map on each side: the coefficient rank does not increase.
(2) Multiplication by a non-zero g(U) h(V) is injective (polynomial ring = integral domain): rank unchanged. (3) Each M factor
1 - c Q_L Q_R (c != 0) has rank exactly 2 (Q_L, Q_R non-constant because the clause crosses); the factors live on disjoint variables, so
the rank of their product is the Kronecker product 2^K. QED. A Boolean restriction that makes ALL other factors non-zero constants is
impossible for unsatisfiable F (that objection is correct) - but it is not needed: generic non-Boolean values (fully restricted factors
1 - (1-s)^p s^q vanish for finitely many s only) and one-sided factors suffice.
Theorem 16 (M9b for Psi_n; director's scheme). Psi = Phi1 /\ Phi2 over phi (clause width k <= 6p, N v-variables). Assumptions: phi has a
clause of width >= 2 (so tuples can straddle a cut) and N >= 2k (so every clause has a one-sided tuple); both hold for phi_n, n large. In every
total order, some prefix cut balances the v-variables (|L| = floor(N/2)); the selectors' side is irrelevant because all are substituted.
Choose M = pairwise v-disjoint Phi1 clauses (C,t) whose tuple has v-variables on both sides (K >= floor(N/(2k)) of them), selectors := generic.
Every other Phi1 clause whose tuple straddles the cut: selector := 0 (factor 1). All remaining selectors := generic (their Phi1 factors are
one-sided). Phi2: for every C some tuple lies on one side, so its selector is generic and the "at least one" factor 1 - (1-s)^g is a non-zero
constant (precisely 1 - prod(1 - s_t) over its non-zero selectors, a non-zero polynomial); the 2-clauses not u v not u' become 1 or
1 - s s', non-zero polynomials avoided by independent transcendentals. Lemma M9b' gives rank(P_Psi) >= 2^{floor(N/(2k))} = 2^{Omega(n)} at a prefix
cut of EVERY order; hence every certificate C = 1 - prod(1 - y) + sum_i z_i h_i(x) of Psi_n has width >= 2^{Omega(n)} / N_total (cell M9b).
Check: m9b/psi_rank.py (tiny Psi, 60 selectors, 1,667 clauses): rank 4 = 2^2 as predicted; control (all selectors of one clause := 0) rank 0.
Meaning (external reviewer's caveat, confirmed): the bound uses only the selector structure of the order lift, not the hardness of phi - it
holds for Psi(phi) of every unsatisfiable phi. It excludes the canonical product certificate for structural reasons and says nothing about
general full roABP-IPS certificates (M9 remainder stays OPEN). Tseitin: roABP-IPS_LIN refutes it in polynomial width in every order (TR26-070 Prop. 20); that its P has high rank is asserted by
the external reviewer's small check, not shown here.
Precision (external, 2026-11-20): work over F(s) with s TRANSCENDENTAL over F - a fixed s need not keep all factors non-zero over small
finite fields. The restricted coefficient matrix is A M B with A, B over F[s], so its rank over F(s) is <= rank_F(M); the lower bound
therefore holds over F. Distinct generic values: independent transcendentals s_1, s_2, ... (or one s with distinct powers).
Overlap objection (external): in phi_n the strict M9b' condition fails for every non-empty M - the four-clause 1-in-3 encoding and the
gadget lift produce clauses with identical supports that cannot be switched off. Correct for phi_n, but not an obstacle for Theorem 16:
in Psi_n every Phi1 clause has its OWN selector, so overlapping straddling clauses are switched off individually (selector := 0, factor 1);
the M9b' condition is checked AFTER the substitution. Lemma O's restriction to phi brings the overlap back - Theorem 16 uses a different
restriction (any restriction is a valid lower bound). Remark (external, valid): width_pi(P_Psi) >= rank_{X|Y}(P_phi) for every pi via Lemma O;
not needed for M9b. Optional open question: rank_{X|Y}(P_phi) at the gadget cut with overlapping supports.
Status: INDEPENDENTLY REVIEWED 2026-11-20 - Lemma M9b' and Theorem 16 CORRECT (substitution and injectivity, rank 2 per crossing
factor, tensor product, field genericity, balanced prefix cut, every clause type of Psi under the substitution, deduction to certificate
width: h_i = C(x,0,e_i) has width <= w, rank(P_Psi) <= N_total w with N_total = N + #selectors = poly(n)). Fixes applied: substitution
wording, assumptions (a clause of width >= 2; N >= 2k), at-least-one factor notation. psi_rank.py is a sanity check of one cut only.

## 17 Rung 5 - hardness magnification route and the first check (2026-11-20)
Sources (local, checked): Chen-Jin-Williams, "Hardness Magnification for all Sparse NP Languages", ECCC TR19-118 (FOCS 2019),
literature/sources/eccc-TR19-118. Their main theorem (abstract): if some 2^{n^{o(1)}}-sparse L in NP is not in Circuit[n^{1+eps}], then NP
does not have n^k-size circuits for ALL k - FIXED-POLYNOMIAL lower bounds, not NP not in P/poly. This does NOT imply P != NP: if P = NP then
Sigma_2^p = P = NP, and Kannan (Sigma_2^p not in SIZE[n^k] for every k) gives NP not in SIZE[n^k] anyway. The route that reaches P != NP is
item (1) of their introduction, McKay-Murray-Williams (STOC 2019): if there is eps > 0 such that for all small enough beta > 0,
MCSP[2^{beta m}] has no n^{1+eps}-size circuits (n = 2^m), then NP not in P/poly, hence P != NP.
Target statement (rung 5, magnification): exists eps > 0, for all small beta > 0: MCSP[2^{beta m}] has no Boolean circuits of size n^{1+eps}.
Known obstacle: the locality barrier (Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam 2020): techniques valid for circuits with small
fan-in oracle gates cannot give these bounds.
First check (proved here): cut rank is NOT a circuit-size measure. IP_n(x,y) = sum x_i y_i mod 2 has Boolean circuits of size O(n), while
its +-1 communication matrix across x | y is the 2^n x 2^n Sylvester-Hadamard matrix of full rank 2^n over Q; likewise prod_i (1 + x_i y_i)
has arithmetic circuits of size O(n) and cut rank exactly 2^n (Kronecker product of n rank-2 factors). Hence every lower bound obtained in
this project from cut rank (Lemma T, T*, M9b', Theorems 12, 14, 16) is a bound for models with a FIXED cut/order (roABP, OBDD-like,
communication, IPS fragments) and cannot by itself give any superlinear general-circuit lower bound - our rank methods fail for general
circuits even before the locality barrier is reached. Consequence: none of the current PNP-001 tools addresses the rung-5 target statement;
a genuinely new circuit-lower-bound idea would be required, and it would have to pass the locality barrier and the barrier filter.

### 17.1 Precision (2026-11-20, second source check) and the connection test
Verbatim, TR19-118 lines 180-181 (after Thm 1.1): "Setting L_beta = MCSP[2^{0.99 beta n}] and C = NP in Theorem 1.1, we recover a main result of
[MMW19], although with a weaker (yet still very strong) consequence NP not in Circuit[n^k] for all k." So: CJW Thm 1.1 for ANY sparse NP
language (including MCSP[m^2]) yields only fixed-polynomial lower bounds (not P != NP); NP not in P/poly needs MMW19 with MCSP[2^{beta m}] for all
small beta. Binding wording (owner 2026-11-20): the transfer theorem exists (MMW19), the target statement is precise, the mechanism with
which FruitStack could prove it is missing.
Connection test (single obligation for rung 5): can a PNP-001 measure be strengthened so that it captures the REUSE of intermediate results in
arbitrary Boolean circuits? Mandatory controls: EQ_m (cut rank 2^m, linear circuits) and IP_n (full cut rank, linear circuits) - any claim
that fails on these is unsuitable for this route. Lead only, not yet checked at the source: Atserias-Mueller 2025, "Simple General
Magnification of Circuit Lower Bounds" (arXiv).

## 18 Rung 5, step 1 of the binding order: is there a bridge from PNP-001 measures to general circuit size? (2026-11-20)
Sources checked: Atserias-Mueller, "Simple general magnification of circuit lower bounds", arXiv 2503.24061v2 (local copy
literature/sources/arXiv-2503.24061); Chen-Jin-Williams TR19-118; Grochow-Pitassi arXiv 1404.3820.
(a) General magnification (Atserias-Mueller Thm 4, 9; CJW): for sparse NP problems the conclusions are FIXED-POLYNOMIAL
    (NP not in FML[n^c] / SIZE[n^c] for all c) - not NP not in P/poly. Atserias-Mueller state the thresholds are sharp.
(b) Uniform magnification (Atserias-Mueller Thm 11): P != NP^{(+)P} if for some eps > 0 and sigma(l) <= 2^{o(l)},
    n^{-eps}-MCSP[sigma] is not in P-uniform-SIZE[n^{1+eps+o(1)}]. "Almost known" (Santhanam-Williams: P not in P-uniform-SIZE[n^c]) and it
    seems to sidestep the localization barrier. Conclusion is P != NP^{(+)P}, which is WEAKER than P != NP (NP is contained in NP^{(+)P}).
    The best partial route found; it needs lower bounds against UNIFORM circuits, not proof-system bounds.
(c) Proof-complexity magnification (Mueller-Pich, APAL 2020; Atserias-Buss-Mueller, STOC 2023) concerns the PROVABILITY of circuit lower
    bounds in weak theories / Extended Frege - not lower bounds themselves. Listed as leads, not checked in detail.
(d) Structural finding (direction of implication), proved by inspection of our own tools: every PNP-001 lower bound flows
    COMPUTATION -> PROOFS - Lemma T / Theorem 12 derive proof-size bounds FROM monotone-span-program (tiling) lower bounds; feasible
    interpolation in general turns short proofs into small circuits/span programs, so its contrapositive yields PROOF lower bounds from
    COMPUTATIONAL lower bounds. The magnification target needs the opposite flow PROOFS/MEASURES -> COMPUTATION. The only known formal
    bridge from IPS goes to ALGEBRAIC complexity (Grochow-Pitassi: superpolynomial general-IPS lower bounds imply VP != VNP), not to
    Boolean P/poly. Together with sec. 17 (cut rank is not a circuit-size measure; EQ, IP controls): no published or PNP-001 bridge from
    our measures to general Boolean circuit size exists. Step 1 result: NEGATIVE for all current tools; step 2 (locality) is moot for them.
(e) What a bridge would have to be (precise open statement): a lemma "a Boolean circuit of size s deciding MCSP[2^{beta m}] yields a
    small refutation in a proof system Y of an explicit family Phi" - i.e. the circuit's correctness must be efficiently provable in Y.
    For weak Y (roABP-IPS_LIN, PC, ...) this is not available; for strong Y (Extended Frege) lower bounds are themselves out of reach.

## 19 Rung 5: streaming magnification (MMW19 Thm 1.3) and the communication connection test (2026-11-20)
Source checked: McKay-Murray-Williams, STOC 2019, people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf (local copy literature/sources/mmw19).
Thm 1.3: if for some time-constructible s(n) >= n and A in PH, search-MCSP^A[s(n)] is not solvable by a poly(s(n))-space streaming algorithm
with poly(s(n)) update time, then P != NP. (Owner's statement confirmed.)
Thm 1.2 (same paper): for every oracle A there is a one-pass streaming algorithm for search-MCSP^A[s(n)] with O~(s(n)) space and O~(s(n)^2)
update time using a Sigma_3 SAT^A oracle with short queries. Authors, after Thm 1.3: "Note there is no information-theoretic barrier to such
a streaming algorithm, only a computational one."
Connection test (owner proposal: transfer rank/communication methods to the information states of a streaming algorithm) - NEGATIVE,
proved: communication protocols are computationally unbounded, so Thm 1.2 yields a one-way protocol of O~(s) = poly(s) bits at every cut of
the stream; no communication or rank lower bound can exceed poly(s). The hypothesis of Thm 1.3 is a lower bound on UPDATE TIME (computation),
not on information - outside the reach of every PNP-001 tool. Status of the streaming route: OPEN; no PNP-001 connection.
Precision (owner, 2026-11-20): the bounds of Thm 1.2 hold for the ORACLE algorithm (Sigma_3 SAT^A queries of length O~(s)). For A in PH the
oracle can be simulated in space poly(s) (PH is contained in PSPACE), at possibly huge running time - so even WITHOUT oracle access there is
a deterministic one-pass streaming algorithm with poly(s) space, lacking only the update-time guarantee. Hence: a pure streaming SPACE lower
bound cannot activate Thm 1.3. Combined time-space lower bounds remain mathematically possible; the PNP-001 communication and rank results
provide none.
### Rung 5: investigation of the transfer routes COMPLETED (owner decision 2026-11-20) - direct applicability of PNP-001 tools refuted. P != NP is NOT proved; SAT not in P (or any statement implying it) remains OPEN.
- General Boolean circuits: high cut rank is compatible with small circuits (EQ_m, IP_n).
- Universal IPS simulation: no size-preserving simulation of arbitrary SAT algorithms in a fixed proof system.
- MCSP hardness magnification (MMW19): needs a general circuit lower bound; our implications run computation -> proofs.
- MCSP streaming magnification (MMW19 Thm 1.3): space lower bounds cannot suffice (Thm 1.2 + PH in PSPACE); an update-time lower bound is missing.
- Atserias-Mueller uniform magnification: conclusion only P != NP^{(+)P}; needs uniform circuit lower bounds.
What is missing is a method that captures the cost of GENERAL computation, including free reuse of intermediate results - not a higher
rank, larger degree or a stronger restricted proof system. No such method is established in the PNP-001 proof book. All existing
mathematical results are preserved; no new mission and no further experiments from this approach.

## 20 Reuse-sensitive MCSP route: lower limit for generic reuse lemmas (director 2026-11-20)
Proposition R1. Any lemma "for every De Morgan circuit of size S with r gates of fan-out > 1 computing f: L(f) <= C S (r+1)^c" that holds for
ALL Boolean functions f needs c >= 1 (exactly: for fixed C, n^2 <= C' n^{1+c} for all n forces c >= 1).
Proof. XOR_n has a De Morgan circuit of size S = Theta(n): a chain of XOR_2 gadgets x (+) y = (x v y) ^ not(x ^ y); the output of each gadget
feeds both the v- and the ^-gate of the next gadget, so it has fan-out 2, giving r >= n - 2 reused gates. Khrapchenko: L(XOR_n) >= n^2
(De Morgan formula leaf size). Hence n^2 <= C' n^{1+c} for all n, so c >= 1. QED (classical ingredients; elementary.)
Consequence. With today's provable a(beta) ~ 2 for small thresholds (MCSP[2^{sqrt l}] not in FML[n^{2-delta}]), the route needs c < 1, i.e. an
MCSP-specific reuse lemma that strictly beats the parity witness: every small circuit for MCSP[N^beta] must have reused intermediate results
that unfold into formulas more cheaply than XOR chains do. Obstacle to examine next: small circuits for MCSP may contain parity-like
sub-computations; a lemma with c < 1 must exclude this for EVERY small circuit, not only natural ones. Together with the non-locality
requirement (F2), this is the precise current state of the route. Status: OPEN; Proposition R1 elementary, independent review not yet done.
Reuse lemma, written proof (director 2026-11-20; leaf-count size). Let C be a De Morgan circuit of size S with r gates of fan-out > 1.
(1) Replace each reused gate g_i by a new variable y_i; every other gate has fan-out 1 and lies in exactly one tree (the one its unique path
leads to), giving formulas T_1..T_r, T_out over (x, y); a tree with g binary gates has g + 1 leaves (NOT gates add none), so the r + 1 trees have at
most S + r + 1 leaves together (input leaves may repeat) - corrected 2026-11-20. (2) f(x) = OR over a in {0,1}^r of
[AND_i (T_i(x,a) <-> a_i) AND T_out(x,a)], where T_i <-> a_i is T_i or not T_i (negations pushed to leaves, leaf count unchanged).
(3) Acyclicity: in topological order a consistent a equals the true gate values, so exactly one branch is consistent and yields the output.
(4) Size <= 2^r (S + r + 1) leaves = O(S 2^r) since r <= S. QED - correct for arbitrary fan-out.
Update (owner deep research, source-checked 2026-11-20): Chen-Jin-Williams, "Sharp Threshold Results for Computational Complexity", ECCC
TR20-065 / STOC 2020 (local copy literature/sources/eccc-TR20-065), Thm 1.6: for every alpha in (0,1) and eps > 0, MCSP[n^alpha] has no
probabilistic n^{2+alpha-eps}-size formulas (n = truth-table length, FIXED threshold n^alpha). So a(beta) = 2 + beta for the fixed threshold
(supersedes "a ~ 2" above).
Conditional Theorem R (owner formulation, proof checked). Hypothesis R-MCSP: there are constants C, c < 1 and beta_0 > 0 such that for every
fixed beta in (0, beta_0) every Boolean circuit of size S with r reused gates deciding MCSP[N^beta] has an equivalent De Morgan formula with
at most C S (r+1)^c leaves. Then P != NP.
Proof. r <= S, so L <= C S^{1+c}. CJW20 Thm 1.6: L >= N^{2+beta-eta}. Hence S >= N^{(2+beta-eta)/(1+c)}/O(1) >= N^{(2-eta)/(1+c)}/O(1); for
eta small and c < 1 this is >= N^{1+eps} with eps > 0 independent of beta. MMW19 (MCSP[2^{beta m}] not in SIZE(N^{1+eps}) for all small beta)
gives NP not in P/poly, hence P != NP (basis changes cost constant factors). QED.
Threshold table: c < 1 - uniform eps, MMW applies; 1 <= c < 1 + beta - eta - superlinear for each fixed beta, eps -> 0 as beta -> 0, MMW does
not apply; c >= 1 + beta - no superlinear bound.
Status: Theorem R (the implication) PROVED from published results (paper proof, review pending); hypothesis R-MCSP OPEN. By Proposition R1
any reuse lemma valid for all functions has c >= 1, so R-MCSP must be MCSP-specific, strictly beat the parity witness, and fail for small
fan-in oracle gates (F2). The exponent c < 1 lies exactly where every generic method is excluded.
Independent review (2026-11-20, adversarial reviewer, read-only, against CJW20/MMW19/CJW19 texts): lemma, R1 and the arithmetic of Theorem R
CORRECT; CJW20 Thm 1.6 citation CORRECT (line 162; n = 2^m truth-table length, size = leaf count). Nothing WRONG. Fixes adopted:
(1) NOT-gate convention: S counts binary gates; if NOT gates are free but reused NOT gates count in r, then r <= 2S + N = O(S) (S >= N-1),
so all bounds hold up to constants. (2) MMW step: the literal STOC'19 statement is Thm 1.4 (third bullet: search-MCSP^A[s] without circuits
of size N poly(s), depth poly(s) => NP not in P/poly); the "MCSP[2^{beta m}] not in SIZE(N^{1+eps}) for all small beta" form is the CJW
TR19-118 restatement (lines ~62-64). Derivation: NP in P/poly gives MCSP[2^{beta m}] circuits of size N^{1+k beta} for a fixed k; beta <
eps/k contradicts; search vs decision costs N poly(s). (3) Theorem R uses only r <= S, so R-MCSP is in effect "L(MCSP[N^beta]) <=
C S^{1+c}, 1+c < 2" - the (r+1)^c refinement plays no role in the implication. (4) R1 is weaker than the real obstacle: a generic lemma with
ANY constant c would put P/poly into poly-size formulas (NC1/poly). "Exactly where every generic method is excluded" is withdrawn: R1
excludes only lemmas valid for all functions, not lemmas for restricted circuit classes or other techniques.
Status: reuse lemma, Proposition R1, Theorem R (implication) - independently reviewed. R-MCSP OPEN.
Owner refinement (2026-11-20): restrict to size-minimal circuits. Target: L(MCSP[N^beta]) <= K_beta S*(r*+1)^{1-delta}, delta > 0 independent
of beta, S* = CC(MCSP[N^beta]). Director check: WLOG correct; arithmetic correct (S* >= N^{(2+beta-eta)/(2-delta)}, uniform > 1 for eta <
delta). Note: since r* <= S*, the implication uses only L(F) <= K_beta CC(F)^{2-delta}, a statement relating two complexity measures of
one function; minimality/decomposition is a proof device, not part of the statement.
Source check KKLMO (Kabanets-Koroth-Lu-Myrisiotis-Oliveira, CCC 2020, arXiv 2002.08533 / ECCC TR20-018, local copy
literature/sources/arXiv-2002.08533): Thm 1 item 3 / Thm 34: if MCSP in FORMULA[s] o XOR then s = Omega~(N^2) (polylog losses). MCSP there
has the threshold l as INPUT (line 230-232), and the authors note the proof "requires instances where the parameter l is n^{Omega(1)}"
(line ~277) - same quantification caveat as CKLM; not stated for fixed MCSP[N^beta]. Their magnification remark: MCSP with l <= n^{o(1)} not
in FORMULA[n^{1+eps}] o XOR would give NP not in FORMULA[n^c] for all c (formulas, not P/poly).
Observation R1' (director, elementary given Tal 2017; Tal source check pending): XOR leaves are XORs of INPUT variables, so
FORMULA[s] o XOR is contained in bipartite formulas of size O(s) (XOR(x_S) + XOR(y_T) needs 2 bipartite leaves). Inner Product IP_n has a
linear-size circuit with a chain of ~n reused gates but needs bipartite formula size n^{2-o(1)} (Tal 2017). So the parity witness is
neutralised by XOR leaves, but IP (a mandatory control) is the same witness in the FORMULA o XOR model: any generic conversion
"circuit -> FORMULA o XOR of size C S (r+1)^c" needs c >= 1 - o(1). The algebraic-unit idea must therefore also be MCSP-specific; XOR
leaves alone do not absorb reuse of COMPUTED values (XOR of intermediate results).
R1' upgraded (2026-11-20, owner check + director source check): Tal, "The Bipartite Formula Complexity of Inner-Product is Quadratic",
ECCC TR16-181 (local copy literature/sources/eccc-TR16-181), Thm 3.2 (line 148): bipartite formula complexity of IP_n is
Omega(n^2/log^2 n) (leaves = arbitrary functions of all x or all y). XOR leaf over inputs = a(x) xor b(y) = (a ^ not b) v (not a ^ b): 4
bipartite leaves. So L_{FORMULA o XOR}(IP_n) = Omega(n^2/log^2 n), while IP_n has a De Morgan circuit with S, r = O(n). Hence any universal
bound L_{FORMULA o XOR}(f) <= C S (r+1)^c needs c >= 1. Status: R1' PROVED from Tal Thm 3.2 + explicit translation (internally
checked; no novelty claim).
Elimination formulation (owner 2026-11-20). For an acyclic circuit C with reused gates g_1..g_r in topological order:
H_C(x,y) = T_out(x,y) AND AND_i (y_i <-> T_i(x, y_<i)), f_C(x) = OR_{y in {0,1}^r} H_C(x,y) exactly; H_C is a formula of size O(S) in
(x,y), consistent y is unique for every x. Naive elimination costs 2^r. Director notes: (i) this is the Tseitin/extension-variable view -
"circuit = small formula with r existentially quantified, functionally determined auxiliaries"; eliminating them IS circuit-to-formula
conversion, so the formulation makes the task concrete but not easier; uniqueness holds for every acyclic circuit (incl. IP), so it is
not MCSP-specific (owner's point). (ii) Structural analogy (not a result): Level-3 (sections 1-9) studied exactly this shape - elimination
of functionally determined auxiliary variables (class D, linearly determined auxiliaries) - over GF(3) representations; its methods
(linearising restriction + elimination) are candidates for allowed transformations, but they were representation-level, not
formula-size results.
Next obligation (owner): fix exactly which transformations are allowed for eliminating y and how their formula leaves are counted;
nested algebraic/non-algebraic dependencies must be costed (XOR of computed AND values is NOT a free XOR leaf); then attempt an
MCSP-specific bound K S^{2-delta} for minimum-size circuits, delta uniform. Controls: parity (R1), IP (R1'), MCSP semantics, small
fan-in oracle gates (locality). OPEN.
Image formulation and HIW23 (owner 2026-11-20; director source check). MCSP[s](x) = 1 iff x in Im(E_{n,s}), E_{n,s}: circuit
descriptions -> truth tables (exact). Two kinds of reuse must be separated: (a) reuse inside a candidate circuit, (b) reuse inside the
circuit that DECIDES MCSP (sharing work across many candidates). R-MCSP and the parameter r concern (b).
Hirahara-Ilango-Williams, "Beating Brute Force for Compression Problems", ECCC TR23-171 (local copy literature/sources/eccc-TR23-171),
Thm 1.3 (line 116): Search-MCSP[s] on truth tables of size 2^n has circuits of size 2^{(4/5)w+o(w)} poly(2^n), w = s log2(s+n); built from
Fiat-Naor function inversion implemented in Boolean circuits. Director assessment: (i) an UPPER bound; at s = N^beta it is
2^{Theta(N^beta log N)}, far above the N^{1+eps} regime where Theorem R needs R-MCSP, so it gives no evidence for or against R-MCSP.
(ii) It is a genuine example of type-(b) sharing (precomputed inversion tables used by all candidates). (iii) Test case for any
elimination calculus: the brute-force formula OR over descriptions d of [x = E(d)] has about 2^{w+o(w)} poly(N) leaves (tight encodings),
i.e. about S_HIW^{5/4+o(1)} poly(N) - so at the HIW scale the formula/circuit gap is at most exponent 5/4 relative to these UPPER bounds
(not a statement about the true CC). A calculus applied to HIW circuits must do at least this well.
R0522 (organisation, 2026-11-20): the 0.99 ML screen on agent_agent_numdiffs_indep_n6_v1_e83d0e55 does NOT survive removing
target-encoding columns (balanced accuracy 0.78 cons3 / 0.76 sat with rank3, m, ncoord_diff; exact law search 0 laws over 60459 rows);
leakage resolved as artefact (session did not re-run the original screen's column list - attribution from the question text).
Prefix extendability (owner 2026-11-20; director check). EXT_{n,s}(p) = 1 iff some circuit of size <= s has truth table starting with p.
Exact prefix automaton = trie of Im(Eval_{n,s}): at most 1 + N |Im| states, state index O(log N + s log(n+s)) bits (owner's count
correct). Owner's points adopted: sparsity and non-injectivity alone explain no hardness; a lower bound for this procedure is not one for
all MCSP algorithms.
Director source check: this automaton with compact states IS the MMW19 streaming algorithm - MMW19 Thm 1.2 (local copy mmw19/paper.txt
line ~100): for every oracle A, search-MCSP^A[s] has a one-pass streaming algorithm on 2^n-bit inputs with 2^n O~(s) time, O~(s^2) update
time and O~(s) space, using a Sigma3SAT^A oracle with queries of length O~(s). Consequences: (i) state count/space cannot give the bound
(already filter F2); ALL difficulty sits in the transition function. (ii) If transitions cost poly(s), MCSP[N^beta] runs in N poly(N^beta)
time; an N^{1+eps} lower bound would need transition cost N^eps = s^{eps/beta}, i.e. SUPERPOLYNOMIAL in the transition input size as beta
-> 0 - a lower bound for an NP-type search problem (find the next consistent circuit) that is itself P != NP-strength. (iii) The
construction holds for every oracle A, so any argument that counts only transition calls relativizes/localizes; the connection test must
cost transitions in real gates. Bridge to R-MCSP (owner's third obligation) remains the decisive open step.
Corrections (owner 2026-11-20, director source check of MMW19 Thm 1.3 and Stream-Merge, mmw19/paper.txt lines ~508-522):
(1) The trie automaton is NOT identical to MMW's algorithm: the trie bounds the information content; MMW's streaming state is a concrete
small circuit consistent with the prefix read so far, and the transition Stream-Merge^A[s] searches a new small circuit that also fits
the next bits (Sigma3SAT^A queries). "IS the MMW19 algorithm" above is withdrawn; read "is realised compactly by".
(2) "superpolynomial in s as beta -> 0" was imprecise: for each FIXED beta, s^{eps/beta} is a polynomial in s. The force lies in the
quantifiers. MMW19 Thm 1.3 (verbatim): "If there is some time-constructible s(n) >= n and an A in PH such that search-MCSP^A[s(n)] is not
solvable by a poly(s(n))-space streaming algorithm with poly(s(n)) update time, then P != NP." Target form: for one fixed s and A in PH,
for EVERY k no one-pass streaming algorithm with O(s^k) space and O(s^k) update time. (3) Stream-Merge is a study object, not the
universal bound: another algorithm may encode states and transitions completely differently. Core obligation (owner): derive from the
correctness of an ARBITRARY streaming algorithm an unavoidable computation and bound its cost in ordinary Boolean operations, for every
fixed polynomial budget. Two published-transfer targets now stand: (A) R-MCSP -> Theorem R (CJW20 + MMW19 Thm 1.4); (B) streaming
time-space lower bound for search-MCSP^A, all polynomial budgets -> MMW19 Thm 1.3. Both OPEN; both need a statement about arbitrary
computation methods.
