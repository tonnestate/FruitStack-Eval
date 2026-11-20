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
