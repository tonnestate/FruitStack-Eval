# T7 — O1: Global / instance-dependent Pfaffian representations of permanent-like sums (PI, 2026-11-17)

Object O1 of PROGRAM-CHARTER-2026-11-16.md (fermion/boson = determinant/permanent). Structural test S1–S3. Status per item. The one
load-bearing new statement for this program is **Lemma O1-B** (a clean no-free-lunch dichotomy); the rest is assembled from known results
and verified exactly on base cases.

## 1. Primary text (read / checked)

- **Valiant 1979:** perm of 0/1 matrices is #P-complete; perm = Σ_{perfect matchings} of a weighted bipartite graph.
- **FKT (Kasteleyn; Fisher–Temperley):** #perfect-matchings of a **planar** graph = |Pf(signed Tutte matrix)|, poly time.
- **Robertson–Seymour–Thomas, Annals 150 (1999), 929–975 (arXiv:math/9911268):** a bipartite graph has a Pfaffian orientation iff it
  is obtained from planar bipartite graphs and one sporadic nonplanar brace — the **Heawood graph** (the point/line incidence graph of
  the Fano plane, 14 vertices) — by **4-sums**; **poly-time recognizable.** Little: a bipartite graph is non-Pfaffian iff it contains a
  matching-covered ("nice") even subdivision of K_{3,3} (Little, *A characterization of convertible (0,1)-matrices*, JCTB 1975).
- **Mignon–Ressayre 2004:** dc(perm_n) ≥ n²/2 (char 0, Hessian-rank); Cai–Chen–Li extend to char ≠ 2; Yabe (n−1)²+1 over ℝ. **These
  quadratic bounds are NO LONGER the frontier (corrected 2026-11-17, §1a).** superpolynomial dc(perm) is open and is
  **VP_ws ≠ VNP** (dc ↔ determinant ↔ VP_ws = algebraic branching programs; Valiant, Toda, Mahajan–Vinay), **implied by** VP ≠ VNP
  (VP_ws ⊆ VP) but **not implying it**: a superpolynomial dc(perm) bound separates VNP from VP_ws only; VP_ws ≠ VP-type separations are a different open question
  (corrected 2026-11-28; earlier text in §S2/S3 and the conclusions wrongly read "VP_ws ≠ VNP, hence VP ≠ VNP"). **Characteristic:** in char 2 perm_n = det_n, so dc(perm_n) ≤ n and no
  dc/pc lower bound of any growth exists there; all bounds on perm quoted in this file are for char 0 (Mignon–Ressayre) / char ≠ 2 (Cai–Chen–Li) / odd char (Sheshadri).
- **Cai–Chen (Holant dichotomy, JACM 2017):** #CSP/Holant is tractable iff affine, product-type, or (planar) matchgate-realizable;
  else #P-hard. Matchgates = exactly the Pfaffian-computable local gadgets.

## 1a. The 2026 cubic frontier (read verbatim; supersedes the quadratic bounds above)

Three directly relevant 2026 primary sources, with their models kept distinct:

- **[OpenAI, 24 Sep 2026]** *A cubic lower bound for border determinantal complexity of the permanent.* Over ℂ, **dc̄(perm_n) = Ω(n³)**
  where dc̄ is **border** determinantal complexity (perm a coefficient-wise limit of determinants of affine m×m matrices; dc̄ ≤ dc, so
  this is the *stronger* statement). Method: restrict perm_n to a linear subspace where it becomes a **smooth** hypersurface of degree
  ≈ n/3 in ≈ n²/100 variables, then use: a smooth degree-d hypersurface in N variables has dc̄ ≥ (N−1)(d−1)/(4e).
- **[Sheshadri, arXiv:2610.40484, 29 Oct 2026]** extends the cubic bound to (a) every algebraically closed field of **odd characteristic**
  p (constant depends on p), and (b) **Pfaffian representations** — pc(perm_n) = Ω(n³) [Thm 1.1: pc_ℂ(perm_n) ≥ n³/(8.8·10⁶ e),
  n ≥ 1408; exact AND border], and (c) **degree-a entries** — dc_a(perm_n), pc_a(perm_n) = Ω(n³/a) for a ≤ n/72 [Thm 1.2], with the bound
  on a necessary (the 1×1 matrix [perm_n] is a degree-n representation). All from one smooth-hypersurface theorem [Thm 3.1,
  dc ≥ (N−1)(d−1)/(4e), pc ≥ (N−1)(d−1)/(8e), every characteristic], proved by intersecting V(F) with N−2 general first derivatives and
  counting intersection points **with multiplicities** (sum d(d−1)^{N−2}) through the border limit. "Lower bounds for Pfaffians imply the
  same for determinants."
- **[Pant–Singh, arXiv:2605.21077, 2026]** a **different, restricted model** — the **Pfaffian number pf(G)**: the least k such that the
  perfect-matching polynomial of G is a linear combination of k Pfaffians of **signings of G's own (fixed) support** (k-Pfaffian;
  pf(G)=1 ⟺ G Pfaffian). Result: **exponential** — for genus ≤ g, some G needs ≥ (8/3)^g Pfaffians; pf(G) ≥ (8/3)^{⌊n/6⌋} on n vertices,
  even for cubic bipartite matching-covered G (improving Galluccio–Loebl–Tesler's 4^g upper bound and the linear Junchaya–Miranda–
  Lucchesi lower bound). Proof: expressing perm of a matrix of **distinct variables** as a linear combination of sign-changed
  determinants needs exponentially many. **This is NOT the affine pc model** (fixed support, no auxiliary variables, but a sum of several
  signings), so it does not lower-bound pc(perm_n).

**§1a correction of §1.** The strongest current lower bounds are **cubic, not quadratic**, and hold for exact, **border**, and **Pfaffian**
representations, in characteristic 0 and every odd characteristic, and degrade as Ω(n³/a) for degree-a entries. The quadratic
Mignon–Ressayre bound is superseded (but its Hessian method is the ancestor of the smooth-hypersurface/polar-intersection argument).

## 2. Models (made precise — the question "beyond local basis change" needs them separated)

Target: perm_w(G) = Σ_{perfect matchings M of G} ∏_{e∈M} w_e, G bipartite, |U|=|V|=n.

- **(L) Local / edge-signing Pfaffian (FKT model):** Pf of the Tutte matrix **of G itself** with a ± signing of its edges. Exists iff G
  is Pfaffian (RST). Preserves the instance graph; most restrictive.
- **(H) Holographic / matchgate (Valiant; Cai–Chen):** local gadget substitution + a global linear basis change. Classified by the
  Holant dichotomy.
- **(S) Symbolic / affine determinantal or Pfaffian (Valiant VP/VNP):** a **fixed** matrix M(x) whose entries are affine-linear forms in
  the variables x_{uv}, with det M = perm_n (dc) or Pf M = perm_n (pf-dc). The instance enters only by substituting values; the matrix is
  instance-independent. Size = complexity measure.
- **(I) Instance-dependent poly-time Pfaffian:** a poly-time algorithm G ↦ B(G) skew-symmetric with Pf(B(G)) = perm_w(G), entries any
  poly-time-computed numbers.

## 3. Results

**Counterexample (L fails at the smallest obstruction; exact, PhysalisMe cm-699ff19e0d48490b).** Exhaustive search over all 2⁹ edge
signings of the Tutte matrix of K_{3,3}: **no** signing makes all 6 perfect matchings agree in sign, so K_{3,3} has no Pfaffian
orientation (while K_{2,2} does). By RST the local model (L) computes perm exactly on the "planar + one sporadic" family and fails off it.
So (L) cannot reach general perm — this is what motivates asking about (H), (S), (I).

**Lemma O1-A (PROVEN — Pfaffian affine ⟹ determinantal affine of the square; exact base case cm-d55440f1d9d84caf).** If Pf(M(x)) =
perm_n(x) for a skew-symmetric M of affine forms of size 2m, then det(M(x)) = Pf(M(x))² = perm_n(x)² — an affine determinantal
representation of perm_n² of size 2m, so pf-dc(perm_n) ≥ ½·dc(perm_n²). *Verified:* K_{2,2}, signing (+,+,+,−): Pf(M)=ad+bc=perm,
det(M)=(ad+bc)²=perm². Moreover dc and pf-dc are **polynomially equivalent** (determinant and Pfaffian are both VP_ws-complete [R, not re-verified here: the direction pc ≤ 2·dc is the elementary det = Pf([[0,M],[−Mᵀ,0]]); the converse needs a polynomial-size ABP for Pfaffians]), so a
superpolynomial lower bound for one transfers to the other (same class VP_ws, not VP) — though the polynomial blow-up does not preserve the exact quadratic constant.

**[RESOLVED by the literature, 2026-11-17 — my Ω(n²) conjecture is superseded by a proven cubic bound.]**
- My earlier "pf-dc(perm_n) = Ω(n²) via Mignon–Ressayre on perm²" route was already **withdrawn as unproven** (the MR method needs a
  smooth point, but {perm²=0}={perm=0} is everywhere non-reduced: at a perm-zero, Hess(perm²) = 2∇perm·∇permᵀ has rank ≤ 1, a trivial
  bound). The owner's precise note confirms this: det(B)=perm² is a valid identity, but a determinant lower bound for perm does **not**
  transfer to perm², and conversely the perm²-detour cannot produce the Pfaffian bound. **The ½·dc(perm²) inequality is correct but
  useless here** (dc(perm²) is not independently known to be large).
- **Now proven, and stronger:** Sheshadri (Thm 1.1) establishes **pc(perm_n) = Ω(n³)** directly — exact and border, char 0 and every odd
  characteristic — by the smooth-hypersurface/polar-intersection method, bypassing the perm² detour entirely. So pf-dc(perm_n) = Ω(n²)
  is not merely CONJECTURED but **PROVEN and improved to Ω(n³)**. I withdraw my planned Hessian investigation as **already done, better**:
  the right tool was intersecting {Pf=0} with N−2 general first derivatives and counting multiplicities (Sheshadri Thm 3.1), not a bare
  Hessian-rank count — my instinct (second-order local geometry of the reduced Pfaffian hypersurface) was the correct direction, the
  polar-intersection realization is the correct method.

**Lemma O1-B (the sharp no-free-lunch dichotomy; PROVEN).** If there is a poly-time algorithm G ↦ B(G) (model (I)) with
Pf(B(G)) = #PM(G) for all bipartite G, then **FP = #P** (hence P = P^#P ⊇ PH, collapse).
*Proof.* The Pfaffian of an integer skew-symmetric matrix is computable **exactly** (value and sign, as a signed integer) in polynomial
time by the fraction-free algorithm of Mahajan–Subramanya–Vinay (and Bareiss-type eliminations) — not merely up to sign via √det.
Composing the poly-time construction G ↦ B(G) with this exact poly-time Pfaffian evaluation computes #PM(G) in FP. #PM of bipartite
graphs = perm of 0/1 matrices = #P-complete (Valiant). Hence FP = #P. ∎ (No vacuity: a B(G) that "encodes the answer" would already
require #PM ∈ FP, which is the conclusion.)
*Consequence.* The instance-dependent global-Pfaffian idea, taken at full generality, **is** the statement FP = #P — it offers no attack
surface the counting world does not already have. The only non-vacuous escape is to restrict G to a family where #PM is already in FP
(planar, Pfaffian braces), i.e. where there is nothing new to gain.

## 4. Placement (structural test S1–S3) and the one genuine open lever

- **S1.** (L) and (H) are classified: (L) = RST planar+sporadic; (H) = Cai–Chen dichotomy, with general (non-planar) #PM on the #P-hard
  side. (I) collapses to FP = #P (O1-B). None reaches general perm without proving FP = #P.
- **S2 (computation vs representation).** (S) is the only model where the instance-independent **representation size** is the open
  quantity. There the cost is genuine: a superpolynomial size lower bound is not excluded by any #P-hardness obstruction — it is
  a superpolynomial size lower bound for dc(perm_n) (char ≠ 2) is equivalent to **VP_ws ≠ VNP** (perm is VNP-complete in char ≠ 2 [R]; dc ~ VP_ws), which is
  implied by VP ≠ VNP but weaker; it is NOT literally VP ≠ VNP.
- **S3 (real room).** The only lever with upside is **(S): dc(perm_n) / pc(perm_n)**. Proven bounds are now **cubic** (OpenAI/Sheshadri,
  §1a), for exact, border and Pfaffian representations in char 0 and odd characteristic (NOT char 2, where perm = det; the generic smooth-hypersurface Thm 3.1 holds in every characteristic but is not applicable to perm there); the target is superpolynomial (= VP_ws ≠ VNP, a consequence of VP ≠ VNP, not a proof of it). The known barriers are representation-theoretic (GCT **occurrence** obstructions — not multiplicity obstructions — were ruled
  out by Bürgisser–Ikenmeyer–Panova, JAMS 32 (2019)), not #P-hardness.

## 4a. My own result: the smooth-restriction / polar-intersection method is capped at n³ for the permanent (Proposition O1-E)

**Proposition O1-E (PROVEN; I claim it is folklore-implicit in the 2026 proofs but state it explicitly as the precise limit of the
method).** Let 𝓜 be the lower-bound method "restrict F to an affine subspace so that the restriction F' is a smooth hypersurface, then
apply dc(F') ≥ (N'−1)(d'−1)/(4e) (resp. pc ≥ …/(8e)), N' = #variables of F', d' = deg F' (Sheshadri Thm 3.1 / OpenAI)". For F = perm_n,
every bound 𝓜 can output satisfies
  dc(perm_n) ≥ dc(F') ≥ (N'−1)(d'−1)/(4e) ≤ (n²−1)(n−1)/(4e) < n³/(4e),
because any affine restriction F' of perm_n has **d' = deg F' ≤ deg perm_n = n** and **N' ≤ n²** — the latter because if the affine map L
had image of dimension > n² it could not be injective into the n²-variable space, so F' would factor through a ≤ n²-dimensional image and its
projective zero locus would be a **cone**, hence singular, contradicting the smoothness 𝓜 requires (reviewer-sharpened, 2026-11-17). The cap
is thus **exactly (n²−1)(n−1)/(4e) < n³/(4e)** (and n³/(8e) for Pfaffians). Hence 𝓜 cannot
prove any bound above n³/(4e) for the permanent (resp. n³/(8e) for Pfaffians). *Proof.* dc(F') ≤ dc(perm_n) since a determinantal
representation of perm_n restricts to one of F' = perm_n∘(affine); deg and variable count of a restriction cannot exceed those of
perm_n. ∎
**Consequence (answers "what is open beyond cubic").** A superpolynomial lower bound for perm cannot come from this method at all: it is
*intrinsically* capped at the product (degree)·(#variables) = n·n² = n³. Any route past n³ must either (i) use a non-linear restriction
(then smoothness and the restriction inequality must be re-established), or (ii) replace the polar-intersection count by an invariant not
bounded by d·N. This is a concrete, method-specific barrier — **not** a claim that superpolynomial bounds are impossible.

## 4b. Model relations I derived (Lemma O1-C)

**Lemma O1-C (PROVEN).** For every polynomial F: **pc(F) ≤ 2·dc(F)** via the alternating embedding det(A) = ±Pf(B), B = [[0, A],[−Aᵀ, 0]]
(B alternating of order 2·order(A); the raw sign is **Pf B = (−1)^{m(m−1)/2} det A**, m = order(A) — verified m=1: Pf=a=det; m=2:
Pf=bc−ad=−det — and is forced to +F by conjugating B with a single transposition, which flips the Pfaffian; reviewer-confirmed 2026-11-17).
Conversely det(M) = Pf(M)² gives
dc(F²) ≤ pc(F). *Verified on K_{2,2}:* dc(perm_2)=2 ⟹ pc(perm_2) ≤ 4, and we exhibited a Pfaffian representation of order 4
(cm-d55440f1d9d84caf). **Open (my selected extension):** is **dc(F) ≤ C·pc(F)** (a *linear* reverse bound)? Polynomial equivalence holds
(both VP_ws-complete), but no linear reverse is known; Sheshadri's pc ≥ …/(8e) vs dc ≥ …/(4e) is consistent with pc ≈ dc/2 but does not
establish dc = O(pc). Settling this would say whether the Pfaffian and determinantal models are the *same* up to constants or genuinely
differ — a precise, bounded question the cubic bounds leave open.

**Honest relation to P vs NP.** perm is #P-complete; VP ≠ VNP is the algebraic analogue of P ≠ NP but does **not** directly imply it
(Boolean vs algebraic; the known transfer, Bürgisser, needs GRH and concerns P vs NP over ℂ). So O1 is a legitimate deep direction toward
VP vs VNP, a recognized intermediate target, but a result here would not by itself settle the Millennium problem. I will not claim
otherwise.

## 5. Self-challenge (before independent review)
- *Am I discovering new mathematics?* Mostly no: O1-A is a one-line classical reduction; O1-B is folklore in spirit (Pfaffian is in FP,
  perm is #P-hard). The new-for-this-program content is the **model taxonomy** that pins down which "global/instance-dependent Pfaffian"
  readings are vacuous (I, collapses to FP=#P) vs. genuinely open (S, = VP/VNP). I state this, not a breakthrough.
- *Am I confusing a limitation of one method with universal impossibility?* Checked against the O2 mistake: O1-B is not a method-specific
  barrier — it is an exact equivalence (poly Pfaffian construction ⟺ FP=#P), with the escape (restricted families) named. (S)'s quadratic
  bound is explicitly flagged as a known limit of current techniques, not an impossibility.
- *Representation vs computation?* Central here and kept distinct: (I) is a computation claim (collapses), (S) is a representation-size
  claim (open).
- *What would change the conclusion?* A superpolynomial lower bound on dc(perm) in char ≠ 2 (= VP_ws ≠ VNP; this separates VNP from VP_ws and by itself does not give VP ≠ VNP); or a poly-constructible (I) on a
  #P-hard family (would give FP = #P). Either is a major theorem.
- *Still P vs NP?* Via the algebraic analogue, with the honest caveat above.

## 6. Verification
Independent adversarial review DONE (2026-11-17, FruitStack agent): O1-B VALID (sign-computation phrasing fixed to the exact
Mahajan–Subramanya–Vinay Pfaffian algorithm); O1-A equalities VALID, its Ω(n²) corollary found UNPROVEN and downgraded to CONJECTURED
(the perm²-route gives Hessian rank ≤ 1); §1 citation fixes applied (Heawood/Fano sporadic brace, 4-sums, Little 1975, VP_ws). Objections
examined, not auto-accepted (the Hessian-rank-1 point verified by hand). Exact computations recorded: cm-699ff19e0d48490b (K_{3,3} non-Pfaffian),
cm-d55440f1d9d84caf (O1-A base case). Ledger entries only after review.

## 1b. Mechanism of the 1/(4e) factor (model-reconstructed, PI-verified against Sheshadri A.3)

Produced by a reasoning model (gpt-oss-120b, PINNED, ovhcloud) and **corrected by me against the primary text** (Sheshadri A.3, lines
~135, 472, 700-715):
- Smooth+reduced V(F): the polar intersection with N-2 general first derivatives is a proper/transverse 0-dimensional complete
  intersection, so by **Bézout** its length = d(d-1)^{N-2} (multiplicities counted; Kleiman genericity for transversality).
- **Upper bound by the representation (the source of 1/(4e)):** Sheshadri "bound[s] it from above by a Bézout count on a larger space,
  which also records the kernel vectors of the matrix" — the intersection points pull back into the locus where the representing matrix
  drops rank (a **corank-one kernel system**, Sheshadri line 472). That count is a **single binomial coefficient** β_1(2m-1) (A.3), of
  central-binomial size ~ 4^m/√m. Solving d(d-1)^{N-2} ≤ β·(…) for the order m gives m ≥ (N-1)(d-1)/(4e): the **4 from the binomial
  base 4^m, the e from Stirling**.
- **{perm²=0} breakdown:** ∂_i(perm²) = 2·perm·∂_i(perm), so vanishing of all first partials forces perm=0, NOT the matrix corank
  drop — the inclusion into the rank-drop locus fails, and the bound cannot start. (Confirms §O1-A: the perm² route is blocked.)
- **PI corrections to the model:** it named the rank-drop locus degree a *Catalan number* of *codimension 4* (corank 2); Sheshadri's
  actual object is a *binomial coefficient* via a *corank-one* kernel system. The 4^m growth and the 4e constant are right; the exact
  combinatorial label and corank were the model's error. Its citations (Harris-Tu dates, "Sheshadri Lemma 3.4") are unreliable; the real
  lemmas are A.2, A.7, Prop A.8.
