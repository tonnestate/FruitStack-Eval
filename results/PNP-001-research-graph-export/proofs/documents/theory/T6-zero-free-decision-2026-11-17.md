# T6 — O2: Zero-free interpolation (Lee–Yang / Barvinok) lives below the counting threshold, far below SAT-hardness (PI, 2026-11-17)

Object O2 of PROGRAM-CHARTER-2026-11-16.md. Structural test S1/S2. Revised after independent adversarial review (§6). Status per item.
Novelty is NOT claimed for the elementary parts; the one genuinely informative statement is the **degree-threshold placement** (§3, D-threshold).

## 1. Primary text (read / checked against source)

**Gebauer–Szabó–Tardos**, *The Local Lemma is asymptotically tight for SAT*, J. ACM 2016 (arXiv:1006.0744v3). (k,s)-CNF = every clause
has exactly k distinct literals, every variable in ≤ s clauses. f(k) = largest s with every (k,s)-CNF satisfiable.
- **Thm 1.1 (verbatim):** 2^{k+1}/(e(k+1)) ≤ f(k) = (2/e + O(1/√k))·2^k/k. Lower bound via the **lopsided** LLL with non-uniform
  probabilities (the symmetric dependency-graph LLL gives only ≈ 2^k/(ek), a factor ~2 less).
- **Thm 1.2 (verbatim):** l(k) = (1/e + O(1/√k))·2^k (neighbourhood version). [Fix: earlier draft wrote k^{-1/3}; the source is k^{-1/2}.]
- Kratochvíl–Savický–Tuza: for k ≥ 3, (k, f(k)+1)-SAT is NP-complete. The neighbourhood-l(k)+2 NP-completeness is **Gebauer–Moser–
  Scheder–Welzl [15]**, not Thm 1.2.

**Bezáková–Galanis–Goldberg–Guo–Štefankovič** (SICOMP 2019, arXiv:1510.09193) + **Moitra** (JACM 2019, arXiv:1610.04317) +
**Galanis–Guo–Wang** (counting). Counting/sampling SAT assignments of (k, Δ)-CNF:
- **Tractable:** FPTAS / efficient sampling for Δ ≤ c·2^{k/2}/k (Moitra; Guo–Liao–Lu–Zhang; Jain–Pham–Vuong), derandomised Δ ≤ c·2^{k/2}/k².
- **Hard:** approximate counting is NP-hard (NP = RP would follow) for Δ ≥ c·2^{k/2}. The exponent k/2 matches hypergraph-colouring
  hardness (Galanis–Guo–Wang).

**Scott–Sokal** (J. Stat. Phys. 118, 2005): zeros of the **independence polynomial of the dependency graph** at negative weights
(Shearer region). This is the lopsided-LLL object; it is **not** Z_F(λ) below, and is not presented here as the same polynomial.

**Reading (precise).** Three thresholds on the variable/clause degree of a k-CNF, as k → ∞:
  zero-free / counting-tractable  ~ 2^{k/2}/k   ≪   approx-counting-hard  ~ 2^{k/2}   ≪   SAT-trivial boundary f(k) ~ (2/e)2^k/k.
Note f(k) ≫ 2^{k/2}: the decision problem is still "every instance YES" at degrees where counting is already NP-hard, and the
zero-free method stops a further factor ~k below even the counting-hardness threshold.

## 2. The polynomial

For CNF F (n vars, m clauses), v(x) = #clauses violated by x, Z_F(λ) = Σ_x λ^{v(x)} = Σ_j a_j λ^j. Then Z_F(1) = 2^n,
Z_F(0) = a_0 = #SAT(F), and Z_F(1+t) = Σ_j t^j Σ_{|S|=j} N(S), N(S) = #{x violating all of S} = 2^{n−|V(S)|} if S consistent else 0.
So the j-th Taylor coefficient at λ = 1 is computable in m^j·poly time; for bounded degree the cluster expansion
(Patel–Regts, SICOMP 2017) gives it in poly(n)·e^{O(j)}. [Review: VALID.]

## 3. Results

**Z1 (trivial).** Z_F(0) = #SAT, so a zero-freeness certificate on a region containing 0 certifies satisfiability of every instance of
its class — it can only apply to always-YES classes. [Review: VALID.]

**D-threshold (the informative statement; VERIFIED_KNOWN, assembled from §1).** The complex-zero interpolation method
(Barvinok; Patel–Regts; Moitra) computes #SAT, hence decides SAT, exactly on the counting-tractable region Δ ≲ 2^{k/2}/k. By §1 this
region is (i) exponentially below the SAT-hardness boundary f(k) ~ 2^k/k, and (ii) a factor ~k below the approximate-counting hardness
boundary 2^{k/2}. Therefore **zero-free interpolation cannot reach the NP-hard decision regime of k-SAT** — not because of a barrier
internal to the method, but because its region of validity ends, provably (modulo the BGGGS hardness, i.e. NP ≠ RP), far below where SAT
becomes hard. This is the correct, unconditional-in-structure answer to O2's question "can a zero-free criterion decide SAT beyond the
always-satisfiable region": no — it ends below even the counting-hard region.

**Z2 [INTERPRETATION CORRECTED 2026-11-17 — see §7; the computation below is correct, its reading as an intrinsic obstruction is withdrawn].** Let F0 be unsatisfiable, j = min{i : a_i(F0) > 0},
A0 = a_j(F0). Let F_t = F0 ∧ (t variable-disjoint satisfiable 3-clauses on fresh variables), and P_F(λ) = Z_F(λ) + c (c > 0 fixed, to
remove the forced zero: P_F(0) = #SAT + c). Then P_{F_t} has j zeros within R_t := 2(c/(A0·7^t))^{1/j} = 2^{−Ω(t)} of [0,1].

*Proof.* Z is multiplicative over variable-disjoint ∧: Z_{F_t}(λ) = Z_{F0}(λ)·(7+λ)^t. Write Z_{F_t} = Aλ^j h(λ), A = A0·7^t,
h(0) = 1, h analytic. On |λ| = R_t: |Aλ^j| = 2^j c; |h − 1| ≤ |g₁−1||g₂| + |g₂−1| with g₁ = Z_{F0}/(A0λ^j) = 1 + O(R_t),
g₂ = (1+λ/7)^t, |g₂ − 1| ≤ e^{tR_t/7} − 1 → 0 since R_t = Θ(7^{−t/j}) makes t·R_t → 0. So |h − 1| < 1/2 ≤ (2^j−1)/2^j on the circle,
and by Rouché P_{F_t} = c + Aλ^j h has the same zero count in |λ| ≤ R_t as c + Aλ^j, namely j (its zeros at radius R_t/2). ∎
The Ω constant depends on j (F0 fixed). Finite check (checks/t6_zeros.py, F0 = all 8 clauses on 3 vars, j = 1): zero-to-[0,1] distance
6.25e-2, 8.94e-3, 1.276e-3, 1.822e-4 for t = 0..3, matching 1/(16·7^t). [Review: VALID; re-run through PhysalisMe — §5.]

**Z3 (conditional; superseded as a route by D-threshold, kept for the record).** Barvinok's interpolation (Lemma 2.2.3: a disc
|z| ≤ β maps under a fixed polynomial onto a neighbourhood of [0,1]; after the reflection λ ↦ 1−λ and taking the real branch of log at
P(1) = 2^n + c > 0) determines log P(0) to error ε from P(1) and the first K = e^{O(1/δ)}·log(m/ε) Taylor coefficients, **if** P is
zero-free on the Euclidean δ-neighbourhood of [0,1]. So a class 𝒞 of ≤3-CNFs with m = O(n) and a uniform (δ, c) zero-free bound would
give SAT ∈ time m^{e^{O(1/δ)}·log m} = 2^{O(log² n)} for constant δ — contradicting ETH after sparsification (which outputs ≤3-CNFs,
m = O(n)). *But* for classes **closed under fresh-clause padding** Z2 already gives the conclusion unconditionally; ETH adds content only
for non-padded classes. For bounded-degree classes (e.g. (3,4)-CNF, Tovey) Patel–Regts gives polynomial time, so there the conclusion
follows from P ≠ NP, not ETH. [Review: VALID WITH FIXES, all applied; redundant with D-threshold, not load-bearing.]

## 4. Placement (structural test) and what would reopen O2

- **S1.** The zero-free structure sits at degree ≲ 2^{k/2}/k, inside the region where #SAT is already polynomial-time computable and
  every instance is satisfiable. It does not touch the decision-hard region (degree > f(k)). O2 in the "shift the polynomial" form is
  closed by D-threshold (route) and Z2 (padded classes).
- **S2.** The method's cost is governed by the distance of the zero set from [0,1]; that distance provably collapses before the hard
  region (Z2 on padded classes; BGGGS on general classes via D-threshold).
- **What would reopen O2 (corrected).** The δ-neighbourhood interpolation only excludes zero-free distance ≥ C/log n (since
  K = e^{O(1/δ)}·log m), NOT distance ≥ 1/polylog. A genuinely new route would need one of: (a) a zero-free region of width
  o(1/log n) that is still algorithmically usable by a *different* interpolation than Barvinok's; (b) a different polynomial/weighting
  whose zero-free region provably extends past degree 2^{k/2} on a SAT-hard class — which by BGGGS would itself imply NP = RP, so this is
  the "it would be a breakthrough" branch, to be treated like T4's PCZT; (c) a non-affine encoding of #SAT with hard-to-compute
  low-order coefficients. None is in hand.

## 5. FruitStack verification (this session)
- Exact computation re-run through PhysalisMe (the sanctioned exact-compute path), not only local NumPy — §5 log below.
- Independent mathematical criticism obtained from a FruitStack agent (adversarial referee) — §6; its objections examined, not
  auto-accepted (the disputed Thm 1.2 exponent was checked at the glyph level in the source PDF: 1/√k, referee correct).

## 6. Independent review (2026-11-17)
Adversarial referee (FruitStack agent), checked against GST, Barvinok, BGGGS/Moitra. Verdicts: §1 VALID WITH FIXES (exponent k^{-1/2};
NP-completeness attribution to GMSW [15]; lopsided LLL; Scott–Sokal ≠ Z_F) — all applied. §2 VALID. Z2 VALID (j-dependent constant).
Z3 VALID WITH FIXES (Barvinok disc→neighbourhood, reflection, real-log branch, K = e^{O(1/δ)}·log m, sparsification→≤3-CNF, padding
redundancy, drop connected gadget, bounded-degree→P≠NP) — all applied. §4 last sentence was INVALID (claimed the ETH argument reaches
1/polylog; it reaches only C/log n) — corrected. Added the decisive D-threshold placement and the missing citations (Moitra JACM 2019;
BGGGS SICOMP 2019; Galanis–Guo–Wang; Patel–Regts). The referee agreeing/ disagreeing is not itself evidence; the load-bearing D-threshold
rests on the published hardness results, read at abstract/theorem level (full theorem statements still to be pulled for VERIFIED_KNOWN).

## 7. CORRECTION (owner review, 2026-11-17): Z2 is a normalization artifact; O2 is not a universal impossibility

**New source read.** Liu, Wang, Yin, Zhang, Zhou, *A Counting and Sampling Lovász Local Lemma*, arXiv:2608.08616v3 (Oct 2026).
Counting/sampling tractable in the regime **4e·p·(D+1)² ≤ 1** (p = max constraint violation probability, D = max dependency degree) —
"tight up to constant factors under NP ≠ RP". For k-SAT, p = 2^{−k}, so D ≲ 2^{k/2}/(2√e): the **pD² regime**. Gives deterministic
approximate counting (fixed local params), randomized approximate counting (quadratic), near-linear **exact sampling**. Not exact counting.

**The five notions, kept distinct (this was conflated in §3 D-threshold):**
| notion | regime for k-CNF | status |
|---|---|---|
| existence / **decision** (Shearer, GST f(k)) | D ≲ 2^k (pD ≲ 1) → every instance YES | trivial decision in-region; NP-hard above f(k) |
| **exact counting** #SAT | — | #P-complete (Valiant) even for monotone 2-CNF; never tractable nontrivially |
| **approximate counting** (FPRAS/FPTAS) | D ≲ 2^{k/2} (pD² ≲ 1) | tractable; NP-hard above (Bezáková et al.; tight under NP≠RP, 2608.08616) |
| **zero-freeness** (Barvinok, deterministic) | ⊆ pD² regime | a *sufficient route* to deterministic approx counting |
| **randomized** (Moitra/this paper sampling) | pD² regime | exact sampling, approx counting |

The decisive relation: **pD² regime (counting/zero-free) ⊊ pD regime (decision trivial) ⊊ decision-hard region (above f(k))**. Since
2^{k/2} ≪ f(k) ~ 2^k/k, every counting/zero-free method operates strictly inside the region where the *decision* answer is already a
trivial "yes". So the counting threshold says nothing new about decision hardness; conversely a poly-time zero-free criterion deciding SAT
*above* f(k) would be a poly algorithm for an NP-hard problem, i.e. P = NP — the same "no free lunch" as O0/PCZT (T4), not a method-specific
barrier.

**Z2 re-examined for normalization (exact, PhysalisMe cm-673ff95932cb4a11).** For F0 = all 8 clauses on 3 variables, Z_{F0}(λ) = 8λ, so
Z_{F_t}(λ) = 8λ·(7+λ)^t. The zeros of the **partition polynomial itself** are λ = 0 (this *is* #SAT = 0, i.e. Z1) and λ = −7 (distance 7
from the segment [0,1], distance 8 from the evaluation point λ = 1). **Padding adds zeros only at −7, never near [0,1].** The
exponentially small distance in Z2 came solely from the additive
shift Z + c with a *fixed* c against coefficients that grow like 7^t:

| t | min\|zero of Z\|→[0,1] | d(Z+c) | d(Z/7^t + c) | d(Z/2ⁿ + c) |
|---|---|---|---|---|
| 0 | 0.000 | 6.25e-2 | 0.0625 | 0.500 |
| 2 | 0.000 | 1.28e-3 | 0.0637 | 0.845 |
| 4 | 0.000 | 2.60e-5 | 0.0649 | 1.638 |

**[RE-CORRECTED 2026-11-28: the two normalizations above do NOT restore a constant distance — the previous sentence "Dividing by 7^t (or 2ⁿ) restores a constant zero-to-[0,1] distance" is false; the table values (t ≤ 4, c = 1/2) are pre-asymptotic.]**
(N1) Normalization by 2ⁿ = 8^{t+1}: P_t(λ) = λ((7+λ)/8)^t + c. Put λ = 1 + u/t: P_t(1+u/t) = (1+u/t)(1+u/(8t))^t + c → e^{u/8} + c, locally uniformly in u (entire functions). The limit has the simple zeros u_k = 8(log c + iπ(2k+1)); by Hurwitz, for t large P_t has a zero λ_t = 1 + (8(log c + iπ) + o(1))/t. Its distance from [0,1] is ≈ 8π/t (for c < 1 the real part 1 + 8 log c/t lies in [0,1] once t > 8|log c|). **Distance Θ(1/t) = Θ(1/n), polynomially small, not constant.**
(N2) Normalization by 7^t: Q_t(λ) = 8λ(1+λ/7)^t + c. With w = (8/c)λ(1+λ/7)^t, the λ³-coefficient of log Q_t(λ) = log c + log(1+w) is (8/(49c))·t(t−1)/2 − 64t/(7c²) + 512/(3c³) = Θ(t²), so (log Q_t)‴(0) = Θ(t²). For the zeros ρ_j (j = 1..t+1; Q_t(0) = c ≠ 0): (log Q_t)‴(0) = −2Σ_j ρ_j^{−3}, hence Θ(t²) ≤ 2(t+1)/R_t³ with R_t = min|ρ_j|, i.e. **R_t = O(t^{−1/3})**; since 0 ∈ [0,1] the distance of the zero set to [0,1] is ≤ R_t → 0 (a bound, not the true rate; numerically ≈ 0.3·7 ln t / t).
*Targeted numerical confirmation of the predictions (not a new dataset; c = 1/2):* (N1) Newton from λ = 1 + u*/t, residual ≈ 1e-14: t·dist([0,1]) = 21.2, 24.1, 24.9, 25.09, 25.12 for t = 50, 200, 1000, 5000, 20000 → 8π = 25.13; (N2) numpy roots, min|root| = 0.147, 0.092, 0.057, 0.043 at t = 50, 100, 200, 300 (all ≤ t^{−1/3}).
**Reinterpretation of the earlier observation.** The table's near-constant distances (t ≤ 4) were read as asymptotics; the asymptotic regime starts only at t ≳ 8π ≈ 25 (N1). The numerical check at t ≤ 4 never saw the 1/t law.
**What the padded-class obstruction now says.** For the additive-shift polynomial with a fixed c, whichever of the three normalizations (none, 2ⁿ, 7^t) is used, the zeros of P_t approach [0,1] — exponentially fast (none), Θ(1/t) (N1), O(t^{−1/3}) at least (N2) — so a δ-neighbourhood of fixed width is never zero-free, and Barvinok interpolation with K = e^{O(1/δ)}·log m, δ = 1/poly(n), costs e^{poly(n)}. The earlier claim "the exponential collapse is a normalization artifact, not an intrinsic obstruction" is therefore *half* right: the **rate** (exponential) is an artifact of the missing normalization, the **collapse** is not.
**Exact repair (preserves the interpolation mechanism).** Z_{F_t}(λ)/(7+λ)^t = Z_{F0}(λ), so P_t/(7+λ)^t-type factor removal gives the fixed polynomial Z_{F0} + c with fixed zeros: no collapse. Algorithmically this is *factorisation over variable-disjoint components* (Z multiplicative, components found in linear time), after which Z_F(0) = ∏ Z_{comp}(0) and the interpolation is run per component with its own normalisation. It is exact and efficient but only removes disjoint (disconnected) padding; it is not a general evaluation algorithm. **Open:** padding that is connected to F0 (shared variables, Z non-multiplicative): neither the collapse nor a repair is established; T6 Z3's "drop connected gadget" remark stays an open restriction.

**What is preserved vs. what is withdrawn (scoped precisely).**
- PRESERVED in full: the identity Z_{F_t}(λ) = Z_{F0}(λ)·(7+λ)^t, the Rouché computation, and the statement it actually proves —
  *for the concrete unnormalized shifted polynomial P = Z_{F_t} + c with a fixed constant c, the j zeros nearest 0 lie within
  2(c/(A0·7^t))^{1/j} of [0,1].* That remains a correct, proven fact about that specific construction.
- [RE-SCOPED 2026-11-28: the withdrawal below is itself too strong — see the re-correction above; collapse persists under N1/N2 (polynomially), is removed only by exact component factorisation] WITHDRAWN (original 11-17 text): only the **algorithmic corollary** drawn from it — "no class closed under fresh-clause padding has a uniform-width zero-free
  neighbourhood for P", i.e. the reading of the above as an obstruction to zero-free *interpolation algorithms*. That corollary is false
  as a general claim: it holds only for the unnormalized additive-shift construction and disappears under the natural normalization
  (where the zeros of Z sit at 0 and −7, distance 7 from [0,1]). The limitation is thus restricted to that one construction, not a
  property of the method or of padded classes.

**Corrected O2 status.**
- PROVEN (kept): Z1 (Z(0) = #SAT); the Rouché identity (as a computation); the finite checks (cm-04ecd7876011417b, cm-673ff95932cb4a11).
- VERIFIED_KNOWN (refined): the pD / pD² / #P-hard / NP-hard-approx thresholds above, with 2608.08616 as the tight counting boundary.
- WITHDRAWN: "zero-free interpolation faces an intrinsic padding obstruction" and "O2 is a universal impossibility (LIMITATION_ESTABLISHED)".
- OPEN (honest): whether some *efficiently constructible, instance-dependent* zero-free or algebraic certificate decides SAT above f(k)
  is **equivalent to P vs NP in that regime** (no free lunch) — so O2 is not closed by a barrier; it is one more face of the open problem.
  It is de-prioritized (offers no leverage the general problem lacks), not refuted. Reopen if a certificate is proposed whose validity
  region provably crosses f(k) without already assuming P = NP.
