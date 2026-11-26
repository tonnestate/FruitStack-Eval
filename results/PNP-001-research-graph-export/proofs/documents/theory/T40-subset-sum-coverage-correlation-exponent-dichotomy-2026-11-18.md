# T40 — Single-use reachability in finite abelian groups: coverage recurrence, exact correlation law, exponent dichotomy (PI, 2026-11-18)

STATUS: owner mission "Algebraic Reachability, Subset-Sum Saturation and Exact Compression" (2026-11-18). PI proofs below, each checked
by exhaustive computation in lab/exp5x/ (exact.py, cert.py, dichotomy.py; sim.py = extended Experiment 5, seed 20261118).
Not in the ledger. Adversarial verification via FruitStack is queued (see protocol/ACTIVE-MISSION.md).
Builds on T36 Addendum (owner knapsack W_m), T37 (alias/character sums), T38 (observable spaces O1–O8), T39 (natural-proofs placement).

## 0. Phase 1 audit (sources)
- Experiments 1–5 are NOT in the PNP-001 tree. They come from the owner's external agent investigations; their original code is not
  on this host. The re-implementation here (lab/exp5x/sim.py) follows the owner's description: groups, k-range, Poisson comparison.
  The owner's statements about them are classified below.
- Ma–Tang, arXiv:2602.05768v2 (local copy literature/sources/arXiv-2602.05768/), checked in the source:
  - Model: a uniformly random k-ELEMENT SUBSET A ⊆ G (distinct elements), not i.i.d. generators.
  - f(N) is the least k with P(Σ(A) = G) ≥ 1/2 for EVERY abelian G of order N.
  - Erdős–Rényi 1965: f(N) ≤ log₂N + (1/log 2 + o(1)) log log N.
  - Theorem 1.2 (p prime only): for fixed 0 < c < 1/(2 log 2) and k = ⌊log₂p + c log log p⌋, P(Σ(A) = 𝔽_p) → 0.
  - Corollary 1.3: f(p) ≥ log₂p + (1/(2 log 2) + o(1)) log log p for large p.
  - Scope: answers Erdős Problem #543 negatively. It says nothing about other group families, and nothing about worst-case decisions.
- Classification of the owner's earlier statements:
  - "Leftover Hash Lemma ⇒ Poisson law": INCORRECT (owner's own correction is confirmed). See §2, §4.
  - "Threshold k ≈ log₂|H| is universal": INCORRECT. Exponent 2 has full coverage at log₂N + ω(1), while for primes log₂p +
    Ω(log log p) is necessary (§4 Theorem E, Ma–Tang).
  - Experiment 5 transition near k ≈ log₂|H|: computational observation, reproduced in §5.
  - Exp 4 property 5 ("use at most once") is the decisive one: §6 Lemma G and Theorem H make this exact.
  - The other four properties: invertibility and commutativity hold throughout (abelian translations). Solvability and variety
    statements were not re-derived here; no claim.

## 1. Setting
G is a FIXED finite abelian group, n = |G|. g_1, g_2, … are i.i.d. uniform on G (unless stated otherwise).
R_0 = {0}, R_{k+1} = R_k ∪ (R_k + g_{k+1}), q_k = 1 − |R_k|/n. H_k = ⟨g_1..g_k⟩.
S_v = Σ v_i g_i for v ∈ {0,1}^k.
All coverage statements use the denominator G unless "/H" is written.

## 2. Theorem A (exact one-step recurrence) — PROVED
For every set R ⊆ G and g uniform on G: E|R ∩ (R+g)| = |R|²/n. Hence E[q_{k+1} | g_1..g_k] = q_k².
Proof. E_g|R ∩ (R+g)| = (1/n) Σ_g Σ_x 1[x∈R]·1[x−g∈R] = (1/n) Σ_{x∈R} Σ_{y∈R} 1 = |R|²/n, because for fixed x the map g ↦ x−g is a
bijection of G. Then |R ∪ (R+g)| = 2|R| − |R ∩ (R+g)|, so E[1 − |R_{k+1}|/n | R_k] = 1 − 2(1−q) + (1−q)² = q². Here g_{k+1} is
independent of R_k = R_k(g_1..g_k). ∎
Corollary A1. E q_{k+1} = E[q_k²] = (E q_k)² + Var(q_k).
Corollary A2. E q_k ≥ (1 − 1/n)^{2^k}, i.e. E[|R_k|/|G|] ≤ 1 − (1 − 1/n)^{2^k}. By induction with q_0 = 1 − 1/n and Var ≥ 0. ∎
- Equality holds only if every Var(q_j) = 0 for j < k. For n ≥ 3 and k ≥ 2 the inequality is strict, because q_1 takes two values.
- (1 − 1/n)^{2^k} ≤ e^{−2^k/n}. So A2 is NOT the statement "coverage ≤ Poisson". Exact data show E q_k slightly BELOW e^{−2^k/n}
  at small k, e.g. (Z/2)^3, k = 3: 0.3606 < 0.3679.
- Why the fixed ambient G matters: conditioned on H_k, g_{k+1} is not uniform on H_k (it leaves H_k with probability 1 − |H_k|/n).
  The recurrence with H in place of G is false in general. Example: (Z/2)^r, where |R_k|/|H_k| ≡ 1 for every sequence.
Verified: exact.py checks E[q'|R] = q² exactly (rational arithmetic) for EVERY subset R of G, in G ∈ {Z/2², Z/4, Z/6, Z/2×Z/4,
(Z/3)², Z/5}. A2 is checked by full enumeration of all generator tuples in 11 groups for k ≤ 5 (n^k ≤ 2·10⁶): all pass.

## 3. Theorem C (exact joint law of subset sums) — PROVED; answers Phase 5 Q1–Q3
Let v_1..v_m ∈ {0,1}^k and V the m×k integer matrix with these rows. Then (S_{v_1}, …, S_{v_m}) is uniform on the subgroup
V(G^k) ≤ G^m. It is uniform on all of G^m iff, for every prime p | exp(G), the rows of V are linearly independent over 𝔽_p
(equivalently: all m Smith invariants of V are prime to exp(G)).
Proof. The map (g_i) ↦ (Σ_i V_{ji} g_i)_j is a homomorphism φ : G^k → G^m. The push-forward of the uniform law is uniform on im φ,
since its fibres are cosets of ker φ and so have equal size. Write G = ⊕ (Z/p^a). φ is surjective iff it is surjective on each
summand (Z/p^a)^k → (Z/p^a)^m. By Nakayama's lemma (reduction mod p) that holds iff V mod p has rank m. ∎
Consequences:
- C1 (universal pairwise independence). Any two DISTINCT NONEMPTY subsets give independent uniform sums, in EVERY finite abelian
  group: two distinct nonzero 0/1 vectors are independent over every 𝔽_p.
- C2 (relations of characteristic 0). Z-linear relations (A, B disjoint: S_{A∪B} = S_A + S_B) bind in every group.
- C3 (torsion relations). In exponent 2, S_A + S_B = S_{A△B} always: three sums are deterministic. For A, B, C = {1,2}, {2,3}, {1,3}
  (det = 2) the three sums are dependent exactly when 2 | exp(G), and independent uniform in groups of odd order.
- So the correlation structure of random subset sums is EXACTLY the family of 𝔽_p-matroids of the 0/1 indicator vectors, for the
  primes p | exp(G). Invariant factors enter only through their prime supports.
- C4 (generic primes). If p exceeds every minor of every 0/1 matrix with k columns (Hadamard: p > (k+1)^{(k+1)/2}/2^k suffices),
  the 𝔽_p-matroid equals the ℚ-matroid. All such primes then have the same correlation structure. In the threshold regime
  k ≈ log₂p this condition FAILS (k^{k/2} ≫ p), so C4 gives no Poisson theorem there. Recorded as a precise gap.
Verified: exact.py checks all pairs and triples of nonempty subsets of [3] in Z/2, Z/3, Z/4, Z/6, (Z/2)², Z/5 (336 cases):
uniform ⇔ Smith criterion, 0 mismatches.

## 4. Theorems D, E (two-sided coverage bounds; non-universality) — PROVED
Theorem D (universal second-moment bound). For every finite abelian G and k ≥ 1:
  E q_k ≤ (n−1)² / (n(2^k − 1)),  and  P(R_k ≠ G) ≤ (n−1)² / (2^k − 1).
Proof. Fix x ≠ 0 and let X = #{v ≠ 0 : S_v = x}, with N = 2^k − 1 summands of probability 1/n each. By C1 the indicators are
pairwise independent, so Var X = N(1/n)(1 − 1/n). Chebyshev: P(X = 0) ≤ Var X / (EX)² = (n−1)/N. The element x = 0 is always
covered. Average over x for the first bound; take a union bound over the n−1 nonzero x for the second. ∎
So full coverage holds w.h.p. once k ≥ 2 log₂n + ω(1), in every group. This is weaker than Erdős–Rényi (log₂N + O(log log N)),
but fully proved here from Theorem C alone.
Theorem E (exponent 2: exact law, and tightness of D). G = (Z/2)^r, n = 2^r. R_k = span_{𝔽₂}(g_1..g_k) = H_k for EVERY sequence.
  P(R_k = G) = Π_{j=0}^{r−1} (1 − 2^{j−k})  (k ≥ r), the standard count of full-rank r×k matrices over 𝔽₂.
  With s = (2^r − 1)/2^k:  ½(s − s²/2) ≤ E q_k ≤ (n−1)²/(n(2^k−1)) ≈ s.
Proof of the lower bound. If rank < r then |R_k| ≤ n/2, so q_k ≥ ½. Hence E q_k ≥ ½(1 − Π(1 − x_j)) with x_j = 2^{j−k}, and
1 − Π(1 − x_j) ≥ Σx_j − Σ_{i<j} x_i x_j ≥ s − s²/2. ∎
Consequences:
- E1. D is tight up to a factor 2 + o(1) (as s → 0) on the family (Z/2)^r. No universal improvement of D in its 2^{−k} order
  is possible.
- E2 (Poisson fails decisively in exponent 2). Poisson predicts E q ≈ e^{−2^k/n}, the truth is Θ(n/2^k). The ratio is unbounded
  as k − r → ∞.
- E3 (the threshold is not universal, and the two effects point opposite ways). In (Z/2)^r, P(R_k = G) → 1 already for
  k = log₂n + ω(1). For primes, Ma–Tang require k ≥ log₂p + (1/(2 log 2) − ε) log log p. Exponent 2 has WORSE mean coverage than
  Poisson but a SHARPER full-coverage threshold. The cause is the same: the large variance from C3 (whole subspaces are
  covered or missed together).
Verified: exact.py confirms the rank formula exactly for r = 2, 3 and k ≤ 5 (e.g. 0.794677734375 = 0.794677734375). The bounds
D and A2 are confirmed exactly in all enumerated rows (see exact.out.json).

## 5. Corrected Experiment 5 (sim.py, seed 20261118) — COMPUTATIONAL OBSERVATIONS
Run: lab/exp5x/sim.py, seed 20261118, 972 rows (sim.out.json). Groups: Z/2^10, Z/2^14, Z/2^18, (Z/4)^5, (Z/4)^7, (Z/4)^9,
(Z/2)^10, (Z/2)^14, (Z/2)^18, Z/1021, Z/16381, Z/262139. Trials: 300 per (group, distribution), except n = 2^18: 100 uniform and
50 otherwise. Distributions: uniform; small (coordinates in {0,1,2}); digit basis (2^j per coordinate, then uniform). Wilson 95% CIs.
These are observations, not proofs; no asymptotic claim is drawn from them.
- T40 bounds (A2, D): 0 of the uniform rows lie outside [lower, upper] (sampling slack ±0.03).
- (Z/2)^r, exact law (E): P(R_k = G) matches Π(1 − 2^{j−k}). 77 of 81 rows have the exact value inside the 95% CI, about what 5%
  coverage error predicts. The rows of one group share the same trial runs, so the misses cluster ((Z/2)^18, k = 19, 20: 100 trials).
- Mean coverage vs Poisson, uniform generators:
  - Z/p, Z/2^m, (Z/4)^r: close to 1 − e^{−2^k/n} near the threshold (e.g. Z/16381, k = 14: 0.633 vs 0.632).
  - (Z/2)^r: clearly BELOW Poisson (k = L+1: 0.775 vs 0.865 for r = 10, 14; 0.703 for r = 18), as E2 predicts.
  - Coverage of H: identically 1 in (Z/2)^r (Lemma G); equal to coverage of G in cyclic groups once H = G.
- Full coverage vs mean coverage, uniform:
  - At k = L+3 the Poisson mean coverage is 1.000, but P(R = G) is 0.00 for Z/16381 and Z/262139, 0.28 for Z/2^14 and 0.33 for
    (Z/4)^7. The full-coverage threshold lies above log₂n, consistent with Ma–Tang's log log term (primes) and Erdős–Rényi.
  - (Z/2)^r reaches P(R = G) ≈ 0.88 already at k = r+3. Non-universality (E3) is visible.
- Small-magnitude generators:
  - In cyclic groups the coverage collapses (Z/2^14: 0.002 at k = 20), because subset sums are bounded by 2k.
  - In (Z/4)^r and (Z/2)^r small coordinates are not restrictive, and coverage stays near the uniform values.
  The generator distribution, not the group order, decides here.
- Digit basis: full coverage exactly once the 2^j-digits of every coordinate are present (k = Σ_c ⌈log₂ m_c⌉, e.g. Z/2^14 at
  k = 14, (Z/4)^5 at k = 10), constructive by the §7 greedy certificate. Before that, coverage is 2^{k}/n (e.g. 0.5 at one digit
  short).

## 6. Lemma G and Theorem H (exponent dichotomy: the algebraic structure behind efficient exact decisions) — PROVED
Lemma G. R_k(S) = ⟨S⟩ for EVERY finite sequence S in G ⇔ exp(G) ≤ 2.
Proof. (⇐) In exponent 2, ⟨S⟩ = {Σ z_i g_i : z_i ∈ Z/2} and z_i ∈ {0,1} = Z/2. (⇒) If g has order ≥ 3, take S = (g):
R_1 = {0, g} ≠ ⟨g⟩. ∎
Interpretation: the single-use restriction is vacuous exactly when the coefficient ring of G is 𝔽₂. Then b_i ∈ {0,1} IS the full
ring and R_k is a group, i.e. closed under addition. This is the closure property whose failure Phase 8 asks for.
Theorem H (dichotomy for (Z/m)^r, r part of the input; generators and target as vectors of digits).
- m = 2: subset-sum reachability is in P (Gaussian elimination over 𝔽₂; by Lemma G it is subgroup membership).
- m ≥ 3 fixed: subset-sum reachability is NP-complete.
- For every m, unrestricted membership t ∈ ⟨S⟩ is in P (linear algebra over Z/m via Howell/Smith form).
Proof (m ≥ 3). Membership in NP is clear. Reduce from X3C restricted to instances in which every element lies in at most 3 triples,
which stays NP-complete (Garey–Johnson [SP2]; Gonzalez 1985). Let the elements be coordinates 1..r, each triple its characteristic
vector in (Z/m)^r, and the target the all-ones vector. A subfamily sums to the target iff every coordinate count c_e ∈ {0,1,2,3}
satisfies c_e ≡ 1 (mod m). For m ≥ 3 this holds iff c_e = 1, i.e. iff the subfamily is an exact cover. ∎
Verified: dichotomy.py checks Lemma G exhaustively in 9 small groups (k ≤ 3), and the reduction by brute force on 450 random
instances (m = 3, 4, 5; 293 with a cover): 0 mismatches.
Placement:
- For every m ≥ 3, random coverage in (Z/m)^r is high once k is a little above log₂n (Theorem D and §5), yet the worst-case
  decision is NP-complete. "High coverage probability" and "easy decision or witness" are different properties (owner's Phase 8
  warning, now with a proof).
- For fixed G, DP over the reachable set decides in O(k·n) time. That is T38's exact abstraction: the state is R_j, of size ≤ n,
  and for translations the observable space of 1_t is the coset space, of dimension |H|. Hardness needs n exponential in the input.

## 7. Exact coverage certificates (Phase 6) — PROVED, constructive
Binary (single use), Z/n. Sort the representatives a_1 ≤ … ≤ a_k in [1, n−1]. The Brown condition is a_{i+1} ≤ 1 + Σ_{j≤i} a_j
(so a_1 = 1). If it holds and Σ a ≥ n − 1, every integer in [0, n−1] is a subset sum, so R_k = Z/n. The greedy decoder (largest
first, take a_i if a_i ≤ remainder) constructs the witness in O(k). Checking costs O(k log k).
Proof: induction on the prefix sums. If t ≥ a_i, take a_i and t − a_i ≤ S_{i−1}; otherwise t < a_i ≤ 1 + S_{i−1}. ∎
- The certificate is sufficient, not necessary (cert.py: 2507 of 6670 fully covering random instances certified, 0 false
  certificates, 11032 targets decoded correctly).
- Products: generators supported on single coordinates certify ⊕ Z/n_c coordinatewise.
- Digit bases are the extreme case (a_i = 2^{i−1}).
Signed, length-bounded. Λ = {z ∈ Z^k : Σ z_i g_i = 0}. The signed Cayley distance of t equals min{‖z‖₁ : Σ z_i g_i = t}, i.e. the
ℓ₁-distance from a particular solution z_0 to Λ. For any basis b_1..b_k of Λ, Babai rounding (z = z_0 − Σ round(c_i) b_i) returns an
integral representation with ‖z‖₁ ≤ ½ Σ‖b_i‖₁. This is a polynomially checkable, constructive upper bound on the ℓ₁ covering radius
of the cosets.
Verified: cert.py, LLL basis, 300 instances and 30305 targets: 0 violations; true radius / certificate ≤ 0.965 (mean 0.53).
The signed certificate does NOT transfer to binary sums: among 1196 random instances with signed radius ≤ k, 1069 have R_k ≠ Z/n.

## 8. Answer to the mandatory question
"Can the group-theoretic correlation structure of random subset sums be characterised precisely enough to predict exact
reachability and complete coverage without enumeration?"
- YES for the correlation structure itself. Theorem C gives it exactly: 𝔽_p-matroids of the indicator vectors, for p | exp(G).
- YES for the first two moments and full-coverage bounds valid in every G: Theorem A (exact one-step law), A2 and D (two-sided
  bounds, D tight up to factor 2).
- YES exactly for exponent 2 (Theorem E).
- NO universal law: Poisson fails by an unbounded factor in exponent 2 (E2), and the full-coverage threshold differs between
  exponent 2 and primes (E3, Ma–Tang).
- For a SPECIFIC instance, exact reachability without enumeration is NP-complete as soon as exp(G) ≥ 3 and the group is part of
  the input (Theorem H). It is polynomial in exponent 2 (Lemma G), for certified generator structure (§7), and for fixed G (DP).
  Averages give no worst-case statement.
- Open (precise): an explicit Poisson error term for Z/p in the window k = log₂p + O(log log p). It needs control of 𝔽_p-relations
  among 0/1 vectors at k ≈ log₂p, where C4 does not apply. Ma–Tang's second-moment analysis is the relevant tool.

## 9. PNP-001 implications
- Established (PI, pending adversarial verification): A, A2, C (C1–C4), D, E, G, H, §7 certificates.
- Classical ingredients: Chebyshev, Nakayama, full-rank count over 𝔽₂, X3C-3 NP-completeness, Brown's criterion, Babai rounding.
- New as assembled statements here (no literature search for priority yet): A2 in this form, C as the exact correlation law, E1–E3
  as the explicit non-universality, H as the exponent dichotomy for (Z/m)^r.
- Not established: anything about P vs NP. Theorem H is an NP-completeness result plus a polynomial case. It locates the efficient
  structure (exponent 2 = closure of the single-use set under addition), but gives no lower bound for general algorithms. Any such
  bound would face T36 Lemma N and the T39 barrier.
- T38 link: exponent 2 is the case where the exact abstraction (the reachable set) is a subgroup, i.e. linear, as in Finding E /
  O6. For exp ≥ 3 the reachable sets are not closed, and the exact abstraction is the DP state of size ≤ n.

## Verification record — FruitStack iteration 10 (mission 80b3922a, 2026-11-18, COMPLETED, CherryMe UNVERIFIED, claims UNKNOWN)
- The mission reported "(A) refuted" and "(D) refuted", and "(C) supported". Its own synthesis states that no claim rests on
  checkable evidence.
- PI examination of the recorded code (mission_record.json events 36–42, research_computations). The objections are NOT
  binding, because none of them rests on a computation of the stated quantity:
  - (Z/2)^3 was modelled as the list [0,1,0,1,0,1].
  - The first E q_k code added group elements without reduction mod n.
  - The "independence" test applied S_A + S_B = S_{A△B} to Z/4 and Z/6, where T40 states it ONLY for exponent 2.
  - No code computed E|R ∩ (R+g)|.
  - The recorded outputs are "results_DE: 0.0", "results_E: 0.0" and unrelated "quantum states".
- T40 A, C, D, E, G, H stand as PI results with their exact checks in lab/exp5x (exact rational enumeration). They are not in the
  ledger: there is still no independent adversarial confirmation.
