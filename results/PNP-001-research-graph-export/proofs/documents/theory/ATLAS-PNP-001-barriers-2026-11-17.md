# PNP-001 — Barrier Atlas (T0, T7–T13) — consolidated 2026-11-17

Principal Investigator export. Each node: PROVEN | NO-GO barrier | OPEN obligation. All arXiv IDs verified. No new separation claimed.

---


---

# T0 — Barrier synthesis for P vs NP / VP_ws vs VNP (T5, T11, T12, T13) (PI, 2026-11-17)

Strict separation throughout: PROVEN implications/theorems | known NO-GO barriers | remaining OPEN proof obligations. No claim that any
new lower bound or obstruction has been found. All citations arXiv-verified. char 0 for the algebraic side.

## T12 — Boolean hardness magnification (source-verified barrier map)
Magnification converts WEAK (near-linear) circuit lower bounds for meta-computational problems into global NON-UNIFORM separations.
Truth-table encoding N=2ⁿ; MCSP[s]/MKtP[s] ask if the length-N table has circuit size / time-bounded Kolmogorov complexity ≤ s(n).
PROVEN conditional theorems (the weak premises themselves are OPEN):
- **Oliveira–Santhanam, FOCS 2018:** an N^{1+o(1)}-size lower bound for (Gap)MKtP magnifies to EXP⊄P/poly (NP⊄P/poly under gap variants).
- **McKay–Murray–Williams, STOC 2019:** near-linear AC⁰-with-few-XOR/THR-oracle lower bounds for MCSP/MKtP magnify to NP⊄P/poly.
- **Chen–Jin–Williams, FOCS 2019:** all sparse NP languages — e.g. De Morgan formulas N^{3+ε} for Search-MCSP → ⊕P⊄NC¹; AC⁰[6] N^{1+ε} → NEXP⊄P/poly / NP⊄NC¹.
NO-GO — **Locality Barrier (Chen–Hirahara–Oliveira–Pich–Rajgopal–Santhanam, ITCS 2020 / JACM):** a lower-bound technique is "local" if it
still works against the class augmented with oracle gates of fan-in N^δ. A sparse language (MCSP[2^{o(n)}] has only 2^{2^{o(n)}} ≪ 2^N
small circuits) is trivially decided by AC⁰ + such oracles, so every local technique (random restrictions, polynomial approximation,
discriminators) CANNOT cross the magnification threshold. Magnification evades Natural Proofs (sparse, not dense) but hits Locality.
OBLIGATION **T12-A:** a NON-local lower bound (e.g. N^{1+ε} for AC⁰, N^{3+ε} for De Morgan formulas) using global truth-table structure,
failing under N^δ-fan-in oracles. **T12-B:** even then the result is only non-uniform (NP⊄P/poly); the step to P≠NP goes through T5.

## T5 — uniformity gap / Karp–Lipton bridge (source-verified)
PROVEN: P ⊆ P/poly, so **NP⊄P/poly ⟹ P≠NP immediately and unconditionally** (this is the easy direction; T12 feeds it).
PROVEN: **Karp–Lipton (STOC 1980):** NP⊆P/poly ⟹ PH collapses to Σ₂ᵖ (= S₂ᵖ, Sengupta). So proving PH ≠ Σ₂ᵖ gives NP⊄P/poly (contrapositive).
PROVEN: **Williams' algorithmic method (STOC 2011/JACM 2014):** a non-trivial (2ⁿ/n^{ω(1)}) SAT algorithm for a circuit class C + IKW-style
collapse ⟹ NEXP⊄C; executed for C=ACC⁰. OBLIGATION **T5-A:** a Circuit-SAT algorithm at 2ⁿ/n^{ω(1)} would give NEXP⊄P/poly (open).
**T5-B:** descending NEXP→NP needs a non-relativizing witness-compression theorem for NP under NP⊆P/poly beyond Σ₂ᵖ (missing).

## T13 — algebraic natural proofs & succinct hitting sets (source-verified; bridges back to T11)
Setup: C_{n,d} ⊆ 𝔽[x]_{≤d}, N=C(n+d,n). A proof polynomial P_N(Z) vanishes on coeff(f) for all f∈C (soundness), is ≢0 (largeness), and is
itself computable in an efficient algebraic class 𝒟 (constructivity). These P_N are exactly the defining equations of the GCT orbit closure
(T11) — T13 isolates their CIRCUIT complexity 𝒟 where GCT uses their symmetry.
PROVEN EQUIVALENCE — **Grochow–Kumar–Saks–Saraf (arXiv:1701.01717) & Forbes–Shpilka–Volk (arXiv:1701.05328, ToC 2018):** no 𝒟-natural proof
against C EXISTS ⟺ C is a 𝒟-succinct hitting set (extreme PIT derandomization). So the algebraic natural-proofs barrier is EQUIVALENT to a
PIT statement.
- **FSV 2018:** explicit C-succinct hitting sets for restricted C (sparse, ROABP, multilinear) ⇒ natural proofs against those are impossible.
- **Chatterjee–Kumar–Ramya–Saptharishi–Tengse, FOCS 2020:** VP-natural proofs DO exist for VP with bounded coefficients / over 𝔽_q — no
  blanket barrier there. **Kumar–Ramya–Saptharishi–Tengse 2023 (GRH):** win-win — either natural proofs for VP exist, or succinct hitting
  sets for VP exist (themselves giving strong lower bounds).
OBLIGATION **T13-A (char-0 gap):** over ℂ/ℚ without coefficient bounds, whether VP-natural proofs against VP exist is OPEN. **T13-B:** to
dodge the char-0 barrier, the equations P_N for the det orbit closure (T11) must themselves lie OUTSIDE VP (e.g. use multiplicities γ_λ,
not matrix ranks) — directly linking T13 back to T11-B's lower-bound-on-closure obligation.

## T0 — dependency graph and consolidated critical-path obligations
```
[T11 GCT & orbit closures] --(no-go: BIP n≥m²⁵, IP n>3m⁴, ELSW n>2m²+2m, EGOW tensor/Waring)--> [OBL T11-B: L≤γ_λ on Y_{m,n}, ∀ n=poly(m)]
     |--(equation complexity 𝒟)--> [T13 algebraic natural proofs] --(equivalence)--> [succinct hitting sets / PIT]
[T12 hardness magnification] --(no-go: CHOPRS locality)--> [OBL T12-A: non-local N^{1+ε} bound]
     |--(NP⊄P/poly)--> [T5 uniformity / Karp–Lipton] --(P⊆P/poly)--> [GOAL: P≠NP]
```
| Path | Proven mechanism | Blocking barrier | Exact open obligation |
|---|---|---|---|
| T11 algebraic | γ_λ>δ_λ ⟹ perm_m ∉ closure(GL·det_n) | BIP, IP, ELSW, EGOW | certified L≤γ_λ on CLOSURE Y_{m,n}, δ_λ≤U, L>U, ∀ n=poly(m) (not open-orbit a_λ) |
| T13 meta-algebraic | no 𝒟-natural proof ⟺ 𝒟-succinct hitting set | most rank/derivative methods are VP-natural | over ℂ: equations outside VP (T11) or succinct hitting sets for VP |
| T12 Boolean | near-linear MCSP/MKtP bound ⟹ NP⊄P/poly | CHOPRS locality | a non-local circuit lower bound using global table structure |
| T5 uniformity | NP⊄P/poly ⟹ P≠NP; NP⊆P/poly ⟹ PH=Σ₂ᵖ | relativization; missing NP witness-compression | NP⊄P/poly via T12-A, or Williams NEXP→NP |

**Net:** every known method on P vs NP / VP_ws vs VNP is mapped to a PROVEN barrier and a PRECISE surviving obligation. No barrier is a
universal impossibility; none of the obligations is discharged. This is negative/structural knowledge, not progress on the separation.

---

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
  **VP_ws ≠ VNP** (dc ↔ determinant ↔ VP_ws = algebraic branching programs; Valiant, Toda, Mahajan–Vinay), a necessary milestone toward
  VP ≠ VNP, not literally VP ≠ VNP.
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
det(M)=(ad+bc)²=perm². Moreover dc and pf-dc are **polynomially equivalent** (determinant and Pfaffian are both VP_ws-complete), so a
superpolynomial lower bound for one transfers to the other — though the polynomial blow-up does not preserve the exact quadratic constant.

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
  VP ≠ VNP.
- **S3 (real room).** The only lever with upside is **(S): dc(perm_n) / pc(perm_n)**. Proven bounds are now **cubic** (OpenAI/Sheshadri,
  §1a), for exact, border and Pfaffian representations and all characteristics; the target is superpolynomial (= VP_ws ≠ VNP, hence
  VP ≠ VNP). The known barriers are representation-theoretic (GCT **occurrence** obstructions — not multiplicity obstructions — were ruled
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
- *What would change the conclusion?* A superpolynomial lower bound on dc(perm) (= VP_ws ≠ VNP, hence VP ≠ VNP); or a poly-constructible (I) on a
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

---

# T8 — O1: Tangency, the Pfaffian singular criterion, and a Hessian-rank bound for affine Pfaffian representations (PI, 2026-11-17)

Directive "Pfaffian Singularities, Tangency and Algebraic Lower Bounds". Continues T7. char ≠ 2. All claims carry their status. The useful
content is **Lemma T8-B** (rank Hess ≤ 4m−4 at a tangency point) — an **elementary corollary** of the classical Pfaffian Schur-complement
identity, not a deep new theorem — together with a **proved limitation** on what local tangency geometry can give, and the precise open
question it isolates. Verified by independent reasoning model (gpt-oss-120b) + exact computation + adversarial review.

## 1. The exact singular criterion (owner-sharpened; established mathematics)

For F(x) = Pf(A(x)), A(x) = A_0 + Σ_i x_i A_i alternating of order 2m:
  **x ∈ Sing(V(F))  ⟺  F(x)=0 AND D F_x = 0  ⟺  corank A(x) ≥ 4,  OR  ( corank A(x) = 2 AND u^T A_i v = 0 ∀i )**,
where u,v span the 2-dim kernel of A(x). The second clause is **tangency-induced**.

Reasoning (chain rule DF_x = D(Pf)_{A(x)} ∘ L, L the linear part): F(x)=0 means corank A(x) ≥ 2 (on the Pfaffian hypersurface). At a
corank-2 matrix M the differential D(Pf)_M(H) = c_M·u^T H v with c_M = Pf(A') ≠ 0 (A' = invertible complement block), because the
Pfaffian adjugate ∇Pf(M) ∝ uv^T − vu^T is nonzero; its kernel is the tangent hyperplane T_M Pf_{2m}. So DF_x = 0 at a corank-2 point
⟺ im(L) ⊆ T_{A(x)}Pf_{2m} ⟺ u^T A_i v = 0 ∀i. At corank ≥ 4, D(Pf)=0 (intrinsic singular locus of Pf_{2m}, codim 6). **The owner's
precision over the model's answer:** DF_x=0 alone is a *critical point of the polynomial*; a *singular point of the hypersurface* also
needs F(x)=0, i.e. corank ≥ 2 — included above.

**Owner's note on codimension.** The codim-6 intrinsic Pfaffian singular locus is a fact in the *full* space of alternating matrices; it
does NOT transfer automatically to the *parameter* space of an affine representation. Tangency is exactly the phenomenon that breaks the
naive transfer. (Sheshadri therefore converts Pf→det via Lemma A.2 and uses the determinant's codim-4 geometry, not the Pfaffian's.)

## 2. The counterexample (exact, PhysalisMe cm-bc3b5742be854b39)

A(x,y) = [[0,1,x,0],[-1,0,0,-y],[-x,0,0,0],[0,y,0,0]] has **Pf(A)=xy**; A(0,0) has **corank 2** (kernel u=e_3, v=e_4); ∇Pf|_{A(0,0)} is
dual to the (3,4)-entry, so T_{A(0,0)}Pf_4 = {N : N_{34}=0}; and (A_1)_{34}=(A_2)_{34}=0, i.e. u^T A_i v = 0 — **im(L) ⊆ tangent
hyperplane**. Hence the origin is a **tangency-induced** singular point of {xy=0} (corank 2, not corank 4). Confirms §1 and the owner's
point that the codim-6 locus does not drive the singularities after affine restriction.

## 3. Lemma T8-B (PROVEN; elementary corollary of the Pfaffian Schur-complement identity; verified three ways)

**Lemma.** Let p be a tangency-induced singular point of F = Pf(A(x)) (A(p) corank 2, kernel u,v, u^T A_i v = 0 ∀i). Then
  **rank Hess_F(p) ≤ 4m − 4.**

**Proof.** Put A(p) = diag(0_2, A'), A' invertible of order 2m−2 (kernel = first two coordinates). For H = Σ(x_i−p_i)A_i written in
blocks [[H_11, H_12],[−H_12^T, H_22]], the **Pfaffian Schur-complement identity** (Z = A'+H_22 invertible) gives
  F(x) = Pf(A'+H_22) · [ (H_11)_{12} + ( H_12 (A'+H_22)^{-1} H_12^T )_{12} ]   (sign **+**, verified exactly: Pf([[X,Y],[−Yᵀ,Z]]) =
  Pf(Z)·Pf(X + Y Z^{-1} Yᵀ)).
Under tangency (H_11)_{12} = u^T H v = Σ(x_i−p_i) u^T A_i v ≡ 0 **identically**. So to second order
  F(x) = Pf(A')·( H_12 (A')^{-1} H_12^T )_{12} + O(|x−p|^3).
The prefactor's linear part (in H_22) multiplies the now-identically-zero (H_11)_{12}, contributing only at order ≥ 3. Hence Hess_F(p)
is the quadratic form x ↦ Pf(A')·( H_12(x) (A')^{-1} H_12(x)^T )_{12}, which factors through the linear map x ↦ H_12(x) into the
2×(2m−2) block, of dimension 2(2m−2) = 4m−4. Therefore rank Hess_F(p) ≤ 4m−4. ∎

**Verification.**
- Independent reasoning model (gpt-oss-120b, PINNED, ovhcloud, success/finish=stop): confirmed (a) the Schur identity, (b) the factoring
  through H_12 and the ≤ 4m−4 bound, (c) that H_22 enters only at order ≥ 3. (It gave the sign as minus; the adversarial review then showed
  the correct sign is **plus**, verified exactly — rank-irrelevant either way.)
- Exact computation (sympy, 6×6, m=3, N=10 variables, all A_i with (1,2)-entry 0 so tangency holds): all first derivatives of F vanish at
  0 (singular point) and **rank Hess_F(0) = 8 = 4m−4** — the bound is attained (tight). Control without tangency: 0 is not singular.

## 4. Consequence and the PROVED LIMITATION (exact scope)

**Conditional consequence.** If a singular point p of V(perm_n) with rank Hess(perm_n)(p) = R is realized **tangency-induced** (corank 2)
in an affine Pfaffian representation F = perm_n, then (since Hess_F = Hess(perm_n) there) R ≤ 4m−4, so
  **pc(perm_n) = 2m ≥ (R+4)/2.**

**Proved limitation (scope).** The local tangency–Hessian method yields, per singular point, at most pc ≥ (R+4)/2 with R ≤ 4m−4, i.e. its
strength is capped by the Hessian rank attainable at a tangency-realizable singular point. It is a *local* (single-point, second-order)
method and **cannot reach Sheshadri's cubic bound**, which is *global* (polar intersection + the corank-one binomial/Catalan count over the
whole hypersurface, T7 §1b). At corank ≥ 4 (intrinsic) points the Hessian plausibly factors through a larger block (4-dim kernel → block
4×(2m−4) plus the 4×4 kernel Pfaffian), suggesting a *weaker* per-point bound so routing through intrinsic points does not help; this is
asserted, not rigorously derived here (the corank-4 Hessian also carries intrinsic-singular terms not analysed) — flagged as a sub-question.

**The precise open question (the owner's "simultaneous tangency" problem).** Whether this gives a *quadratic* (Ω(n²)) or only a *linear*
(Ω(n)) Pfaffian bound hinges on the **maximal Hessian rank R at a singular point of perm_n that is forced to be corank-2 in the
representation**:
- Mignon–Ressayre attain Hessian rank ~n² for perm (giving dc ≥ n²/2) — but at a point with perm=0, not necessarily ∇perm=0 (a
  *singular* point) and not necessarily corank-2 in a Pfaffian representation.
- The gpt-oss-120b model asserted R = 2n at the realizable point (→ only pc ≥ n+2, linear). **I do NOT adopt this**: it was unverified and
  conflicts with the MR-order; the true value of R at a *singular* point of perm realizable as a *tangency* is OPEN. Resolving it — by
  (i) pinning the Hessian rank of perm at its singular locus, and (ii) deciding whether a representation can force all high-rank singular
  points to corank ≥ 4 (codim-6, a strong simultaneous constraint) — would turn Lemma T8-B into a quadratic Pfaffian bound or prove it
  cannot exceed linear. This is the next proof obligation.

## 5. n = 4 (established reference, status)

dc(perm_4) = 15 (Nov 2026 result; to be checked against its proof). This does NOT determine pc(perm_4). From T7: pc(perm_4) ≤ 2·dc = 30;
and the degree constraint (Pf of order 2m has degree m, need m ≥ 4) gives pc(perm_4) ≥ 8. So pc(perm_4) ∈ [8, 30], exact value OPEN; the
dc=15 result gives no new pc bound. Lemma T8-B at n=4 needs R = rank Hess(perm_4) at a tangency-realizable singular point — small-case,
but governed by the same open R question; no uncontrolled numerical search performed.

## 6. Verification log
Exact: cm-bc3b5742be854b39 (counterexample), local sympy (Lemma T8-B, rank=8=4m−4 tight). Independent model: gpt-oss-120b (criterion §1
and Lemma §3, sign-corrected). Adversarial review: §7 (pending). Ledger entries only after review.

## 7. The singular-locus Hessian-rank analysis (owner-driven, PI-verified 2026-11-17)

Normalization (owner precision): T8-B gives, for an alternating representation of order 2m, M ≤ 4m−4 ⟹ **m ≥ (M+4)/4**; equivalently the
full order **pc = 2m ≥ (M+4)/2**. (My earlier "pc=2m ≥ (M+4)/2" was for the full order and is consistent; m is half the order.)

**Corank-stratified Hessian bounds (exact, verified).** At a singular point p of F = Pf(A(x)):
| corank A(p) | bound on rank Hess_F(p) | reason | verified (exact) |
|---|---|---|---|
| 2 (tangency) | ≤ 4m−4 | Lemma T8-B (Schur complement, factors through the 2×(2m−2) block) | rank = 8 = 4m−4, m=3 |
| 4 | ≤ 6 | split off invertible skew block; the residual 4×4 kernel-Pfaffian is quadratic in its 6 entries | rank = 6, m=4 (tight) |
| ≥ 6 | = 0 | the kernel-block Pfaffian expansion starts at order ≥ 3 | rank = 0, m=4 |

**Corollary (owner; UNCONDITIONALIZES the bound).** rank Hess_F(p) > 6 ⟹ corank A(p) = 2. So a Pfaffian representation **cannot** route a
singular point with Hessian rank > 6 into the intrinsic (corank-4, codim-6) locus; every such point is corank-2, where Lemma T8-B applies.
Hence, with M_n := max over Sing(V(perm_n)) of rank Hess(perm_n), **pc(perm_n) = 2m ≥ (M_n+4)/2 unconditionally** (any witness with rank>6).

**M_n grows at least quadratically (owner's construction, PI-reproduced exactly).** For blocks B (k×k), C (ℓ×ℓ), k+ℓ=n, k,ℓ≥2, with
perm(B)=perm(C)=0 and full-rank gradient matrices, X = diag(B,C) is a singular point of perm_n with
  **rank Hess(perm_n)(X) = 2kℓ + 2**  (mixed second derivatives across the two blocks and the two off-diagonal blocks).
Taking k=⌊n/2⌋, ℓ=⌈n/2⌉: **M_n ≥ 2⌊n/2⌋⌈n/2⌉ + 2 = ⌊n²/2⌋ + 2** for n ≥ 4. Verified exactly (rational blocks, e.g. B = [[1,1],[1,−1]],
perm=0, gradient full rank):
| n | old X_n (2 zero rows) | diag(B,C) = 2kℓ+2 |
|---|---|---|
| 4 | 8 | **10** |
| 5 | 10 | **14** |
| 6 | 12 | **20** |
Owner's exact X_4 = diag([[1,1],[1,−1]],[[1,1],[1,−1]]) → rank 10, reproduced. **Search for a larger M_4:** 167,408 matrices over {−1,0,1},
873 singular, **max rank = 10** — the block-diagonal construction appears optimal at n=4 (tested, not proven). So M_n = Θ(n²) (between
⌊n²/2⌋+2 and the trivial n²).

**Consequence.** pc(perm_n) = 2m ≥ (M_n+4)/2 ≥ (⌊n²/2⌋+6)/2, i.e. m ≥ (⌊n²/2⌋+6)/4 — a **quadratic** Pfaffian lower bound from local
singular-locus geometry, UNCONDITIONAL. It does **not** surpass Sheshadri's cubic pc = Ω(n³) (global). **Status/novelty:** a derived
algebraic corollary; whether the 2kℓ+2 rank formula / the quadratic M_n bound already exist in the literature is NOT settled, so this is
NOT claimed as a published-new result. The exact geometry (and codimension) of Sing(V(perm_n)) remains a hard open problem (2024 literature).

**Net scientific progress (over the earlier T8 finding).** The max Hessian rank on the permanent's singular locus grows **at least
quadratically, not merely linearly** (the earlier X_n family's 2n was not optimal). This resolves the direction of the §4 open question:
the tangency method yields a quadratic (not linear) unconditional Pfaffian bound — still below cubic. Remaining open: the exact value of
M_n (is it ⌊n²/2⌋+2, or larger up to n²?) and whether any global Pfaffian method beats cubic.

**Verification.** Exact computation (sympy): corank-2/4/≥6 bounds (rank 8/6/0), the 2kℓ+2 formula (n=4,5,6 → 10,14,20), owner's X_4,
M_4 search (max 10). Independent adversarial review of the 2kℓ+2 derivation: §8 (pending).

## 8. Algebraic proofs of the corank-4 and corank-≥6 bounds (normal form — NOT a finite search)

Methodological note (owner): a finite search ("not refuted in 40 instances") does NOT prove a bound. The corank-stratified bounds are
provable via the local Pfaffian normal form; here are the proofs. Put A(p) = diag(0_{2r}, A'), A' invertible alternating of order 2m−2r
(2r = corank), kernel = first 2r coordinates; H = Σ(x_i−p_i)A_i in blocks [[H_11, H_12],[−H_12^T, H_22]] (H_11 = 2r×2r kernel block, linear
in x; H_12 = 2r×(2m−2r)). Pfaffian Schur complement (A'+H_22 invertible):
  F(x) = Pf(A'+H_22) · Pf( H_11 + H_12 (A'+H_22)^{-1} H_12^T ).
Write G = Pf(H_11 + W), W := H_12(A'+H_22)^{-1}H_12^T (quadratic-leading in x, since H_12 is linear).

**Corank 4 ⟹ rank Hess_F(p) ≤ 6 (PROVEN).** Here 2r = 4. At corank 4, D(Pf)_{A(p)} = 0 (gradient of Pf vanishes on corank ≥ 4), so p is
singular and F has no linear term. Pf of a 4×4 alternating matrix is the **homogeneous quadratic** Q = af − be + cd in its 6 entries.
Expanding G = Q(H_11 + W) = Q(H_11) + B(H_11, W) + Q(W) with B the polar bilinear form: orders in x are 2, 3, 4 respectively (H_11 linear,
W quadratic). The prefactor Pf(A'+H_22) = Pf(A') + O(x). Hence the degree-2 (Hessian) part of F is exactly Pf(A')·Q(H_11) = Pf(A')·Pf(H_11),
which factors through the linear map x ↦ (the 6 entries of H_11) ∈ k^6. Therefore rank Hess_F(p) ≤ 6. ∎ (Tight: verified = 6.)

**Corank ≥ 6 ⟹ Hess_F(p) = 0 (PROVEN).** Here 2r ≥ 6. The Pfaffian of a 2r×2r alternating matrix is **homogeneous of degree r ≥ 3** in
its entries. H_11 is linear in x, so Pf(H_11) has degree r ≥ 3 in x; the W-terms only raise the order. Thus the lowest-order term of F at
p has degree ≥ 3, so all first and second derivatives vanish: Hess_F(p) = 0 (indeed all derivatives up to order r−1 vanish). ∎

These two, with Lemma T8-B (corank 2, proven in §3), give the full corank-stratified table **by proof**, hence the corollary
rank Hess_F(p) > 6 ⟹ corank A(p) = 2 is a **theorem**, not a numerical observation.

**The X_n corollary, stated honestly.** For X_n (two zero rows) rank Hess(perm_n)(X_n) = 2n > 6, so in any affine Pfaffian representation
X_n is corank-2, and T8-B gives 2n ≤ 4m−4, i.e. **m ≥ (n+2)/2**. This is UNCONDITIONAL but **weaker than the degree bound** m ≥ n (perm_n
degree n = Pf-degree m) — so the X_n point ALONE is not progress on complexity lower bounds; it is a structural illustration. The
block-diagonal construction (§7), with M_n ≥ ⌊n²/2⌋+2, gives the stronger **quadratic** m ≥ (⌊n²/2⌋+6)/4 — which does exceed the degree
bound, but stays below Sheshadri's cubic.

**The extremal question (where new mathematics may lie — OPEN).** Two results would be genuinely valuable:
(i) an *exact singular point* with Hessian rank > ⌊n²/2⌋+2 (would show the two-block construction is not extremal);
(ii) a *proven upper bound* on rank Hess(perm_n) over the whole singular locus (would settle M_n).
Current status: M_n ≥ ⌊n²/2⌋+2 (proven by construction); M_4 = 10 only *tested* (167k matrices over {−1,0,1}, max 10), NOT proven maximal;
no proven upper bound below the trivial n² is known, consistent with the singular-locus geometry of perm being an open problem (2024).

---

# T9 — O1: The extremal Hessian rank on the permanent's singular locus (torus bound; M_4 = 10) (PI, 2026-11-17)

Owner-driven; PI-verified (exact). Continues T8. The extremal quantity is M_n := max over X ∈ Sing(V(perm_n)) of rank Hess(perm_n)(X),
Sing = {perm_n(X)=0 AND ∇perm_n(X)=0}. Result: **M_n = Θ(n²)**, tightly bracketed; **M_4 = 10 exactly**. char 0 / exact field arithmetic.

## 0. Admissibility gate (binding rule for every candidate, before any rank computation)
A candidate X ∈ 𝔽^{n×n} is a singular point ONLY if, in **exact** field arithmetic (cyclotomic field for roots of unity — never
floating-point zero tolerances), **perm_n(X) = 0 AND all n² first derivatives ∂perm_n/∂x_ij (X) = 0** (the (n−1)-sub-permanents). Fourier
matrices are a cautionary case: F_4, F_5 have perm = 0 but ∇perm ≠ 0 (e.g. ∂perm_4/∂x_00(F_4) = −2) — NOT singular; only F_6 is singular,
with rank Hess(perm_6)(F_6) = 16 < 20 (below the block construction). (Owner, exact in cyclotomic fields.)

## 1. Torus-kernel Lemma (owner; PI-verified exactly) — the upper bound

**Lemma T9-A.** For X ∈ Sing(V(perm_n)) let c = number of connected components of the bipartite graph of X (rows ∪ cols, edge iff
X_ij ≠ 0), counting only non-isolated vertices. Then **rank Hess(perm_n)(X) ≤ n² − 2n + c.**

**Derivation.** perm is torus-invariant: perm(D_L X D_R) = (∏_i α_i)(∏_j β_j)·perm(X), D_L=diag(α), D_R=diag(β). Differentiate in x_kl:
perm'_{kl}(D_L X D_R) = (∏_{s≠k}α_s)(∏_{t≠l}β_t)·perm'_{kl}(X). Differentiate again in α_i at α=β=1: the left side gives
[Hess·vec(E_ii X)]_{(k,l)} (where E_ii X = the matrix carrying only row i of X); the right side is a multiple of perm'_{kl}(X) = 0 at a
singular point. Hence **Hess(perm_n)(X)·vec(E_ii X) = 0** for every row i, and likewise **Hess·vec(X E_jj) = 0** for every column j. The 2n
vectors {vec(E_ii X)}, {vec(X E_jj)} satisfy Σ_i E_ii X = X = Σ_j X E_jj per connected component, i.e. c independent relations, so they span
a subspace of ker Hess of dimension 2n − c. Therefore rank Hess ≤ n² − (2n − c) = n² − 2n + c. ∎
*Verified exactly* (sympy): at X = diag([[1,1],[1,−1]],[[1,1],[1,−1]]) (n=4, c=2) the 8 identities Hess·vec(E_ii X)=0, Hess·vec(X E_jj)=0
hold, ker dim = 6 = 2n − c, rank = 10 = n²−2n+c (tight).

## 2. Satz T9-B: M_4 = 10 (PROVEN — full case analysis; owner, PI-verified exactly)

**Upper bound.** Let X be a singular point of perm_4.
- **Case A: X has a zero row (or column).** Say row i = 0. Then the second derivative ∂²perm/∂x_{ab}∂x_{cd} vanishes whenever both index
  pairs avoid row i, and whenever both lie in row i; only cross terms (one variable in row i, one outside) survive, giving the block form
  Hess = [[0, B],[Bᵀ, 0]] with B ∈ ℂ^{4×12}. Hence rank Hess ≤ 2·4 = **8**. (Verified: max rank over zero-row singular points = 8.)
- **Case B: X has no zero row and no zero column.** Every connected component of the bipartite graph has ≥1 row and ≥1 col node. A singular
  point must have c(X) ≤ 2. **[Clean argument, review-supplied — covers non-square components too.]** In any pattern with c ≥ 3 components and
  no zero row/col, there is a 3×3 sub-permanent (delete two rows and two columns suitably) that reduces to a **single uncancellable transversal
  term** — a product of 3 nonzero entries, hence ≠ 0. Concretely: c = 4 ⟹ generalized permutation matrix, perm ≠ 0; c = 3 with the square
  partition (2,2)+(1,1)+(1,1) ⟹ ∂perm/∂(2×2 entry) = (opposite entry)·e·f, a single term, whose vanishing forces a zero row; c = 3 with a
  non-square partition such as (2,1)+(1,2)+(1,1) ⟹ the 3×3 sub-permanent deleting the extra row and extra column is a single product a·c·e ≠ 0.
  In every case some first derivative is nonzero, so X is not singular. Hence c ≤ 2, and Lemma T9-A gives rank Hess ≤ 4²−2·4+2 = **10**.
  (Independently re-verified: adversarial search found max rank 10, 0 singular points among the non-square c=3 family.)
Maximum over both cases is 10.

**Lower bound.** X_4 = diag(B,B), B = [[1,1],[1,−1]] (perm B = 0), is singular with rank Hess(perm_4)(X_4) = 10 (T8 §7; c=2, torus bound
tight). Hence **M_4 = 10.** ∎ (C_4 over ℚ(i) also achieves 10 but is row/col-permutation-equivalent to diag(B,B).)

**[Correction of an auxiliary claim.]** An intermediate argument asserted that for a *rectangular* c=2 structure like (1,3)+(3,1) the Hessian
vanishes. That is FALSE. Owner counterexample, verified exactly: X = [[1,1,1,0],[0,0,0,1],[0,0,0,1],[0,0,0,1]] is singular with rank Hess = 9
(e.g. ∂²perm/∂x₂₁∂x₃₂ = 1, 0-based). This does NOT affect Satz T9-B: X has c=2, so Lemma T9-A already gives rank ≤ 10; its actual rank 9 is
below the balanced diag(B,B) value 10. Rectangular (unbalanced-component) c=2 singular points exist and must be handled by the torus bound,
not by any "H=0" claim. M_4=10 is additionally confirmed EXHAUSTIVELY (all 3¹⁶ {−1,0,1} matrices: 220,737 singular points, max rank 10).

## 3. M_n = Θ(n²) — the general upper bound WITHDRAWN; asymptotics still hold

**[CORRECTION, owner 2026-11-17.]** My earlier general bound "M_n ≤ n²−⌈3n/2⌉" via "c ≤ ⌊n/2⌋" is **FALSE and withdrawn**: a 1×1 block
with a *nonzero* entry is a valid component, so c is not bounded by ⌊n/2⌋. Counterexample (owner, verified exactly): for n=5,
X = diag(1, B, B) has no zero row/column, is singular, but c = 3 > ⌊5/2⌋ = 2, with rank Hess(perm_5)(X) = 10. The n=4 proof (Satz T9-B)
does NOT use that false step — it uses the complete case analysis above, valid because at n=4 a c=3 no-zero-row/col point cannot be singular
(the second singular 2×2 block that kills the derivative at n=5 has no analogue at n=4). 

**Corrected general bound (owner, PI-verified): M_n ≤ n²−n−2 (n ≥ 4).** Proof via Lemma T9-A: if X has a zero row/column its Hessian has the
block form [[0,B],[Bᵀ,0]], rank ≤ 2n ≤ n²−n−2 (n ≥ 4). Otherwise the nonzero graph has no isolated node, and a singular point must have
c ≤ n−2: c = n is a generalized permutation matrix (perm ≠ 0, not singular); c = n−1 forces either a 2×2 component (⟹ a nonzero first
derivative inside it, as in §2 Case B) or a pair of unbalanced complementary components of sizes k and n−k (an unbalanced bipartite
component has no perfect matching, and yields a nonzero sub-permanent derivative) — neither is singular. So c ≤ n−2 and T9-A gives
rank ≤ n²−2n+(n−2) = n²−n−2. ∎ Combined with the construction:
  **⌊n²/2⌋ + 2 ≤ M_n ≤ n²−n−2** (n ≥ 4) — Θ(n²) (lower ½, upper 1); the upper bound is not claimed optimal.

**n=5: M_5 ∈ [14, 18] (PROVEN bracket); exact value OPEN.** What is and is NOT established:
- **Square two-block family (PROVEN = 14):** rank Hess(diag(B_k,C_ℓ)) = 2kℓ+2 (T8 §7, structural derivation independently verified),
  maximized over k+ℓ=5 at (2,3) → 14. This is ONLY the square two-block family.
- **NOT yet bounded ≤14 (open):** rectangular (unbalanced-component) c=2 points — T9-A gives only ≤ 17 — and c=3 points — T9-A gives only
  ≤ 18. So the earlier inference "only a connected point can exceed 14" is **WITHDRAWN**: decomposable points with rectangular components
  or three components are a priori allowed up to 17/18 and must be bounded algebraically, not assumed. Tested exactly: rectangular c=2
  (owner's X = [[0,1,−1,0,0],[1,−1,−1,0,0],[0,−1,−1,0,0],[−1,−1,−1,0,0],[0,0,0,1,1]], sizes (4,3)+(1,2)) → rank 8; c=3 diag(1,B,B) → 10;
  connected c=1 → ≤12 found. Nothing exceeds 14 yet, but no proof for the rectangular/c=3/connected cases.
- **The connected case (Fall D) — the key tool.** Σ(perm_n) = {∇perm_n = 0} is the critical (singular) locus; the Hessian H is the Jacobian
  of ∇perm_n, so the Zariski tangent space satisfies T_X Σ = ker H, giving **dim ker H ≥ dim_X Σ**, i.e. **rank H ≤ n² − dim_X Σ**. The
  torus orbit of X has dimension ≤ 2n−1 = 9 (and lies in Σ), recovering rank ≤ 16 for connected X. A PROOF of M_5 = 14 would follow if
  every connected singular point lies in a component of Σ(perm_5) of dimension ≥ 11 (⟹ rank ≤ 14). Whether dim Σ(perm_5) ≥ 11 on every
  connected component is the exact open obligation (ties to the open singular-locus geometry of the permanent, 2024 literature).
- **Next task:** bound the rectangular-c=2, c=3, and connected-c=1 cases algebraically (not by random matrices); or construct a singular
  point with rank ≥ 15.

## 4. Consequence for pc, and the real next lever (T9 obligation)
**Conditional bound.** If a block singular point (rank Hess = ⌊n²/2⌋+2 > 6) is realized as a **corank-2** point of a Pfaffian representation
F = perm_n, then by T8-B 4m−4 ≥ ⌊n²/2⌋+2, so pc(perm_n) = 2m ≥ ⌊n²/4⌋ + 3 — **quadratic**, below Sheshadri's cubic.

**The blind spot (the genuine open frontier — Satz T9).** A representation A(X) could try to push every point of Sing(V(perm_n)) into the
**intrinsic corank-≥4 locus** {rank A(X) ≤ 2m−4} (codim 6 in alternating matrices), where T8-B does NOT apply (there rank Hess ≤ 6 by T8 §8).
Whether it CAN is a **dimension/incidence** question: a component Z ⊆ Sing(V(perm_n)) (e.g. the block-diagonal variety, codim 4n−6 for the
k=2 family) would have to pull back entirely into the codim-6 locus. Linearizing rank A(X) ≤ 2m−4 along Z couples dim Z (a component of the
permanent's singular locus — whose geometry/codimension is itself open, 2024 literature) to the minimal corank of the bundle A(X) on Z.
**This is the next proof obligation:** does such an embedding exist, or is it obstructed (giving the quadratic pc bound unconditionally)?

## 5. Status
PROVEN & verified THREE ways (PI derivation + exact sympy + independent reasoning model gpt-oss-120b): **Lemma T9-A** (torus-kernel bound
rank ≤ n²−2n+c, including isolated nodes) and **Satz T9-B** (M_4 = 10, full case analysis). The admissibility gate. M_n = Θ(n²) (lower ½,
upper ≤ n²−n−1). **WITHDRAWN (false):** the general upper bound M_n ≤ n²−⌈3n/2⌉ and the step c ≤ ⌊n/2⌋ (owner's n=5 counterexample
diag(1,B,B): c=3, rank 10). OPEN: exact M_5 ∈ [14,17] (needs the correct c-stratification incl. decomposable c=3 points); the
component-incidence obstruction (T8 §7 / the next Satz). Novelty of T9-A / 2kℓ+2 vs. literature: not settled — NOT claimed as published-new.
Independent adversarial review of T9-A and T9-B (separately): pending.

## 3a. Non-equidimensionality of Σ(perm_5) — cleaned theorem, witnesses, literature (2026-11-17)

**Theorem.** The critical scheme Σ(perm_5) ⊂ 𝔸²⁵_ℂ is **NOT equidimensional over ℂ**: it has smooth irreducible components of dimension 11
and 15. Verified three ways (PI exact sympy; gpt-oss-120b reasoning; CherryMe adversarial exact).

**11-dim component V_{2,3} (new).** V_{2,3} = {diag(B,C) : perm_2(B)=0, perm_3(C)=0}, with perm_2, perm_3 irreducible over ℂ, is irreducible
of dim (4−1)+(9−1)=11 and ⊆ Σ (every 4×4 submatrix of a block-diagonal contains all of B or all of C ⟹ all 4-sub-permanents vanish).
Witness X_A = diag(B_0, C_0), B_0=[[1,1],[1,−1]], C_0=[[−2,−2,2],[−2,0,−1],[0,2,1]]. **Corrected gradient matrices** (exact):
G(B_0) = [[−1,1],[1,1]], det −2; **G(C_0) = [[−2,−2,−4],[2,−2,−4],[2,−2,4]], det 64** (both ≠ 0). rank Hess(perm_5)(X_A) = 2·2·3+2 = 14,
so 11 = dim V_{2,3} ≤ dim_{X_A}Σ ≤ dim T_{X_A}Σ = 25−14 = 11 ⟹ dim_{X_A}Σ = 11, smooth point of the unique 11-dim component.
(Local dimension of an irreducible variety is constant at every point, smooth or not — no gap.)

**15-dim components (two types, both KNOWN in the literature).**
- Type B: two zero rows (or two zero cols); linear, dim 15. Witness X_B (rows 0,1 zero, rows 2–4 ones): rank Hess = 10, dim T = 15.
- Type C (1×4 block split, complementary permanent): W_{1,4} = {diag(0,D) : D∈ℂ^{4×4}, perm_4(D)=0}, dim 16−1 = 15, ⊆ Σ. Witness
  X_C = diag(0, D_0), D_0 = [[−1,−1,1,−1],[−1,0,0,1],[1,0,−1,−1],[1,−1,0,−1]]: perm_4(D_0)=0, det G(D_0)=−32 (≠0),
  rank Hess(perm_5)(X_C) = 10, dim T = 15 — a separate smooth 15-dim component (one zero row + one zero col + perm_4(D)=0), NOT a
  two-zero-rows component.

**Literature / novelty (owner survey, to double-check).** The 15-dim components are known: the Type-C family (vanishing row + vanishing col
+ vanishing complementary permanent) appears in Bläser–Ikenmeyer–Jindal–Lysikov, *Ulrich complexity* (2017), used for the codim-2n lower
bound; the two-zero-rows family is the trivial lower-bound family in Xie (arXiv:2609.27320). What is **not** in the surveyed literature
(Bläser et al. 2017; Kirkup 2005; Boralevi–Carlini–Michałek–Ventura arXiv:2402.17839; Xie 2026): the **11-dim block component V_{2,3}** and
the resulting **non-equidimensionality of Σ(perm_5)**. Those references study only the global/maximal dimension (codim 2n) or minimal
primes for 2×2, 3×3 sub-permanents; none constructs multi-block diag(B,C) components or addresses equidimensionality for n=5. So the 11-dim
component and the non-equidimensionality conclusion are the standalone new contribution; full-literature novelty remains to be confirmed.

**Generalization (next step).** For any k+ℓ=n, k,ℓ≥2: V_{k,ℓ} = {diag(B,C): perm_k(B)=perm_ℓ(C)=0} is irreducible of dim (k²−1)+(ℓ²−1)
= k²+ℓ²−2; the block formula rank Hess(diag(B,C)) = 2kℓ+2 gives dim T = n²−2kℓ−2 = (k+ℓ)²−2kℓ−2 = k²+ℓ²−2 = dim V_{k,ℓ} — EQUAL, so
every V_{k,ℓ} is a smooth component. Since k²+ℓ²−2 < n(n−2) whenever kℓ > n (true for k,ℓ≥2, n≥5), V_{k,ℓ} is strictly below the maximal
dimension ⟹ **Σ(perm_n) is non-equidimensional for every n ≥ 5** (indeed n ≥ 4), ONCE the general 2kℓ+2 formula is proven for all
k,ℓ≥2 (verified for (2,2),(2,3),(3,3); general proof is the pending obligation).

---

# T10 — Weg 1: Shifted Partial Derivatives and the rank-method barriers (PI, 2026-11-17)

Goal: can a linear rank measure (shifted partial derivatives, SPD) break the polynomial ceiling for perm_m vs det_n (VP_ws vs VNP)? Answer:
NO for SPD in the padded perm-vs-det model (ELSW 2016), capped at O(m²); and specific other rank measures are barred (EGOW 2018). But NOT a
universal prohibition of all rank / representation-theoretic methods. char 0. Two separate VERIFIED_KNOWN results; precise conditions below.

## T10-A — the SPD barrier (Efremenko–Landsberg–Schenck–Weyman, arXiv:1609.02103, 2016)
SPD dimension: Γ_{r,ℓ}(P) = dim span{ x^α · ∂^r P/∂x_{i1}…∂x_{ir} : |α|=ℓ } (Kayal 2012; GKKS CCC 2013; gives the 2^{Ω(√m)} depth-4 lower bound).
**Theorem 1.5 (verbatim):** "There exists a constant M such that for all m > M and every n > 2m²+2m, any τ and any k < n,
rank((ℓ^{n−m} perm_m)_{(k,n−k)[τ]}) < rank((det_n)_{(k,n−k)[τ]})." Proof in four cases C1–C4:
- **C1 (k > n − n/(m+1)) [corrected]:** the det's k-th partials degenerate to span the WHOLE space of degree-(n−k) polynomials in m²+1
  variables — achieved by a specialization of det_n with **repeated identical determinant blocks** (e.g. diag(Y,…,Y,zI)), NOT a product of
  distinct general permanents. The padded permanent's partials cannot fill that space.
- **C2 (2m ≤ k ≤ n−2m):** the padded Jacobian ideal sits in (ℓ^{n−m−k}), of slowest Macaulay growth; det's Jacobian ideal is larger in
  degree n−k, hence (Macaulay) in all higher degrees.
- **C3 (k<2m, τ > 3n²m/2):** compare the padded ideal with the 2-generated ideal from det → ℓ₁ⁿ+ℓ₂ⁿ (complete intersection).
- **C4 (k<2m, τ < 6n³/m):** GKKS lower bound for det vs. a crude upper bound for the padded permanent (leading-monomial count).
C1,C2 overlap for n>2m²+2m and C3,C4 for n>m⁴, so n>2m²+2m suffices.
**Precise scope (owner-sharpened, confirmed in the source):** (i) holds for **m > M** (sufficiently large, NOT all m); (ii) for the SPD
measure (k-th Jacobian ideal) of the **padded** permanent ℓ^{n−m}perm_m vs det_n. The paper EXPLICITLY leaves open (line 133): "a more
general Young flattening [may] prove a ω(m²) lower bound" (companion paper on minimal free resolutions of Jacobian ideals). So SPD cannot
beat dc(perm_m)=Ω(m²) in this model, but the method is not universally dead.
**Exact computational witness (the degeneration mechanism, verified):** D = det-degeneration (ad−bc)²z² (5 vars a,b,c,d,z) has span{∂⁴D} of
dimension **15** = dim Sym²(ℂ⁵) (fills the whole quadric space); the padded permanent P = z⁴(ad+bc) has span{∂⁴P} of dimension **6**. So
Γ(det) > Γ(padded perm) — the determinant dominates. (The owner's broader table m=2,3,n=3,4,5 shows Γ(padded perm) ≤ Γ(det) in every case,
but these are BELOW the asymptotic threshold n>2m²+2m, so they illustrate, not prove, Thm 1.5.)

## T10-B — the EGOW rank-method barrier (Efremenko–Garg–Oliveira–Wigderson, ITCS 2018, arXiv:1710.09502)
A meta-barrier for rank-based lower-bound methods whose rank is subadditive under rank-1 additions. **Precise scope:** the quantitative
no-go theorems are proven for **tensor rank** and **Waring rank** (model-specific). This is NOT a proof that every rank method fails to
separate perm from det. Keep as a separate, model-specific result; do NOT inflate to ALL_RANK_METHODS_IMPOSSIBLE.

## Consequence for the program map (precise, not overgeneralized)
Two large method-classes are now mapped as polynomial-capped for VP_ws vs VNP:
- Local differential geometry (Hessian rank / tangency / singular-locus, T8/T9): capped at quadratic/cubic.
- Linear rank flattenings in the specific models above (SPD padded perm-vs-det; tensor/Waring rank): SPD capped at O(m²); EGOW bars tensor/Waring.
**NOT excluded (genuinely open):** general Young flattenings / Landsberg–Ottaviani (ELSW's own open question), GCT **multiplicity**
obstructions (BIP 2019 ruled out *occurrence* only — Kronecker/plethysm coefficients are not matrix ranks, so they evade EGOW), and the
Boolean routes (hardness magnification / uniformity gap, T5). A blanket "all rank/representation methods impossible" is unjustified.

## Next (Weg 2): GCT multiplicity obstructions
The multiplicity gap — mult_λ on the padded-permanent side vs. the Kronecker coefficient g(λ,(dⁿ),(dⁿ)) on the determinant side — is where
the padding does not force a linear rank collapse. The obligation: identify an explicitly formulated multiplicity obstruction not already
excluded by a known no-go (BIP occurrence-obstruction exclusion; the "no highest-weight / small-support" obstructions). To be pursued next.

---

# T11 — Weg 2: GCT multiplicity obstructions (permanent vs determinant) (PI, 2026-11-17)

Research objective (owner): find + independently validate a concrete representation-theoretic multiplicity inequality separating the orbit
closures of det_n and the padded permanent ℓ^{n−m}perm_m. Method: two independent researchers (gpt-oss-120b PINNED; adversarial reviewer
w/ web), substance-agreed, citations corrected by the reviewer. Outcome = owner's Option 3: a PRECISELY BOUNDED OPEN PROBLEM, not a
certified obstruction (which would be a breakthrough). char 0.

## The two sides — orbit vs CLOSURE (the critical distinction; owner-sharpened 2026-11-17)
Write Y_{m,n} = closure of GL·(ℓ^{n−m}perm_m), D_n = closure of GL·det_n. For λ ⊢ nd set γ_λ = mult_λ ℂ[Y_{m,n}]_d (closure, padded
perm) and δ_λ = mult_λ ℂ[D_n]_d (closure, det). The OPEN-orbit multiplicities are a_λ (padded perm) and k_n(λ) = g(λ,(dⁿ),(dⁿ)) (det,
Kronecker; plethysm p_{λ,m,d} = ⟨s_λ, h_d[h_m]⟩ is a_λ). **Direction (verified, standard AG):** the orbit O is open dense in its closure
Ȳ, so ℂ[Ȳ] ↪ ℂ[O] (a regular function vanishing on the dense O vanishes), hence **closure multiplicity ≤ orbit multiplicity**:
    **γ_λ ≤ a_λ   and   δ_λ ≤ k_n(λ)  — both are UPPER bounds.**
A certified multiplicity obstruction is **γ_λ > δ_λ**. Therefore a_λ > k_n(λ) (comparing the two UPPER bounds) is **NOT** a certified
obstruction — it bounds nothing about γ_λ vs δ_λ. (My first recording of T11-B compared these two upper bounds; corrected below.)

## T11-A — the GCT obstruction landscape (VERIFIED_KNOWN; two-model + primary-source)
1. **Occurrence obstructions — EXCLUDED.** Bürgisser–Ikenmeyer–Panova, "No occurrence obstructions in GCT", JAMS 32 (2019) 163–193,
   arXiv:1604.06431, **Theorem 1.4**: for n ≥ m²⁵ and λ ⊢ nd, if λ occurs in ℂ[orbit-closure(padded perm)] then it occurs in
   ℂ[orbit-closure(det_n)]. I.e. a_λ(perm)>0 ⟹ a_λ(det)>0. The polynomial padding range (n ≥ m²⁵) comfortably covers any
   superpolynomial-lower-bound attempt, so occurrence obstructions provably CANNOT prove perm≠det. (Exponent 25 loose/improvable.
   Precursor: Ikenmeyer–Panova, Adv. Math. 319 (2017), rectangular-Kronecker positivity.)
2. **Positivity-hardness — bars EFFICIENTLY-VERIFIABLE obstructions (not obstructions per se).** Plethysm: Fischer–Ikenmeyer, Comput.
   Complexity 29 (2020), arXiv:2002.00788 — computing is #P-hard, deciding POSITIVITY is NP-hard. Kronecker: Ikenmeyer–Mulmuley–Walter,
   Comput. Complexity 26 (2017) — positivity NP-hard (and C_=P-hard); computing #P-hard (Bürgisser–Ikenmeyer FPSAC 2008). These are exactly
   the multiplicities governing GCT obstructions ⇒ an explicit, poly-time-verifiable obstruction is not obtainable by generic positivity
   computation. (Also: these coefficients are NOT matrix ranks, so Weg 2 genuinely evades the EGOW/T10 rank barrier — the padding survives
   as a plethysm, not a collapsed linear rank.)
3. **Multiplicity obstructions — OPEN (not excluded).** BIP state explicitly (§1(c), abstract): they do NOT rule out the approach via
   multiplicity obstructions; comparing multiplicities may still succeed. No published no-go excludes them for det vs padded perm.

## T11-A extra barriers (owner-added, verified)
- **Ikenmeyer–Panova, Adv. Math. 319 (2017)** (rectangular Kronecker): for n > 3m⁴, a λ occurring on the padded-perm side cannot yield an
  obstruction merely through VANISHING of the rectangular Kronecker coefficient k_n(λ) — reinforces that occurrence/vanishing routes die.
- **Dörfler–Ikenmeyer–Panova, arXiv:1901.04576 (ICALP 2019)**: "Multiplicity obstructions are stronger than occurrence obstructions" —
  multiplicity obstructions provably SUCCEED where occurrence obstructions fail, but in a DIFFERENT geometric setting. A proof of concept
  that the multiplicity route is not vacuous; NOT a permanent–determinant separation.

## T11-B — the precisely bounded open problem (the frontier; CORRECTED to lower-bound-on-closure form)
A certified obstruction requires γ_λ > δ_λ on the CLOSURES. Since γ_λ ≤ a_λ and δ_λ ≤ k_n(λ) are both upper bounds, the obligation is:
    **find a specified (m,n,d,λ) and certified bounds L, U with  L ≤ γ_λ,  δ_λ ≤ U,  and  L > U.**
The hard half is the **lower bound L ≤ γ_λ on the orbit-CLOSURE coordinate ring ℂ[Y_{m,n}]_d** (not the open-orbit plethysm a_λ, which is
only an upper bound for γ_λ). All known explicit families give EQUALITY a_λ = k_n(λ); a gap could only open at the BOUNDARY of the Kronecker
polytope, where no λ is known. Coupled obstacles: (a) existence of such (λ) with γ_λ > δ_λ is OPEN; (b) exhibiting/verifying one without
solving a #P-/NP-hard positivity instance (T11-A.2) is the SHARPER obstacle. **Asymptotic criterion:** a VP_ws≠VNP-relevant separation
needs L > U to hold for n beyond EVERY fixed polynomial bound in m, not merely one fixed exponent. Post-2019 pivots (data): finer
multiplicity/asymptotics; unpadded + symmetry formulations (Landsberg–Ressayre; Grochow–Mulmuley–Qiao); border-rank/matrix-mult GCT.

## Honest status vs the ultimate objective (P vs NP)
Weg 2 is the genuine superpolynomial-candidate route (unlike T8/T9/T10, all polynomial-capped) AND evades the rank barrier — but it meets
its own double barrier (occurrence dead + positivity #P/NP-hard). No certified obstruction; no refuted construction either. Deliverable =
bounded open problem T11-B. This does NOT prove anything about P vs NP; it maps precisely where the GCT route is stuck and why.
