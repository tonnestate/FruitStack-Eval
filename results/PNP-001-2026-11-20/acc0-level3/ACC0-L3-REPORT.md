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
CNFs. Their Thm 5 (Thm 49): the functional method cannot give non-placeholder roABP-IPS_LIN' bounds over finite fields - the same
phenomenon as our breaking point B1. Use for R4b: technique anchor (finite fields, lower bound by multiples, set-multilinearisation),
not a solution.
