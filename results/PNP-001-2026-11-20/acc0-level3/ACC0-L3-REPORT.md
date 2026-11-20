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
R(S) decides SAT and computes #SAT exactly. Its cost is exactly poly(t, m) * [2^{|S|} + sum over GF(3)-consistent sigma of 2^{t-|S|-r(sigma)}]
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
- Consequences: (i) #SAT by R costs >= sum_sigma 2^{dim aff Sol_sigma} >= #SAT. (ii) On UNSAT inputs R costs the sum of 2^{free} over
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
