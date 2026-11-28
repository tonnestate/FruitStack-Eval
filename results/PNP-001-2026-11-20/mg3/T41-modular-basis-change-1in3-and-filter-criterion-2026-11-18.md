# T41 — Modulus and basis change for positive 1-in-3-SAT filters; colour-filter criterion (PI, 2026-11-18)

STATUS: owner handover 2026-11-18, §12 next step, plus the colour-filter brief of the same day. PI proofs; exact computational checks
in lab/onein3/onein3.py (onein3.out.json) and scratchpad filter.py. Not in the ledger; no FruitStack mission started (owner rule:
queue unchanged).

## 1. Colour-filter criterion (closes the colour-filter brief)
Theorem CF. Let V, W be vector spaces over a field, C : V → W and D : V → V linear.
(a) There is M : W → W with CD = MC iff ker C ⊆ ker(CD).
(b) For a family {D_a}, C is exact for every filter word (CD_w = M_w C for all w) iff ker C is D_a-invariant for every a.
(c) For a final readout c^T, the smallest exact linear compression has rank d = dim span{c^T D_w}. Its kernel is the unobservable
    subspace ∩_w ker(c^T D_w).
Proof.
- (a) (⇒) Cx = 0 ⇒ CDx = MCx = 0. (⇐) Define M(Cx) := CDx on im C. It is well defined because Cx = Cx' ⇒ x − x' ∈ ker C ⊆ ker CD.
  Extend M linearly to W by any complement of im C.
- (b) If D_a(ker C) ⊆ ker C for all a, then D_w(ker C) ⊆ ker C ⊆ ker C. So C D_w kills ker C, and (a) applies to every word.
  Conversely, U = ∩_w ker(C D_w) is D_a-invariant and lies inside ker C. Exactness for all w means ker C ⊆ U, hence ker C = U.
- (c) is T38 Finding E and O7, in dual form. ∎
Verified: over 𝔽₂, all C of size 2×3, 1×3 and 2×2 and all square D (37 120 cases), existence of M ⇔ the kernel criterion: 0 mismatches.
Metamerism means exactly that ker C is not D-invariant.
Relation to T38. CF is linear observability (Kalman / T38 Finding E, O7) in measurement language. It provides NO property beyond
O1–O8: no new invariant, and no statement about cost.
Transfer to SAT. The linear (Koopman) lifting of a circuit acts on ℝ^{2^n} (2^n "channels"). The gates are cheap as tensor-product
operators, but extracting the decision is a full contraction. By O7 the minimal exact channel count is d, and O2 shows d = 2^{n−1}+1
for the binary counter, a problem in P. So an exponential channel lower bound holds for easy problems and cannot imply hardness.
Any lower bound obtained this way excludes linear-channel representations only.
DECISION: NO. Colour filters reproduce T38 (Finding E, O7) and give no polynomial transfer. The hypothesis is CLOSED as a separate
direction. Its content stays in T38 as mechanism A (projection).

## 2. Positive 1-in-3-SAT under basis and modulus change (handover §12)
Setting. Positive clauses (a, b, c), satisfied iff x_a + x_b + x_c = 1. n variables, m clauses, one coordinate of ω ∈ 𝔽₂^{3m} per
occurrence. B : 𝔽₂^{3m} → 𝔽₂^n sums each occurrence coordinate into its variable. C(φ) = number of satisfying assignments.
Signature: f̂(ω) = (3 − 2|ω|)/8, weights {3, 1, −1, −3} (owner §8, re-derived).
Theorem D1 (Fourier dual, exact). C(φ) = 2^{n−3m} Σ_{ω ∈ ker B} Π_j (3 − 2|ω_j|).
Proof. Write f_j(x) = Σ_{ω_j} f̂(ω_j)(−1)^{ω_j·x_{S_j}}. Multiply and sum over x. Σ_x (−1)^{(Bω)·x} = 2^n [Bω = 0]. ∎
In Holant language, the Hadamard transform maps Holant(=, ExactOne₃) to Holant(EVEN, f̂). The equalities become parity constraints.
Theorem D3 (characteristic 3: 1-in-3 becomes NAE with parity). C(φ) ≡ (−1)^n · N₃(φ) (mod 3), where N₃ is the number of 2-colourings
of the occurrences such that (i) no clause has all three occurrences the same colour (NAE), and (ii) every variable has an even
number of occurrences of colour 1.
Proof. Mod 3 the weights are 0 for |ω_j| ∈ {0, 3} and ±1 for |ω_j| = 1 or 2. So only NAE blocks survive, each with sign
(−1)^{[|ω_j| = 2]}. On ker B the total weight Σ|ω_j| is even, since it is the sum of the even per-variable parities. With every
block of weight 1 or 2, the number of weight-2 blocks is ≡ m (mod 2), so every surviving term is (−1)^m. Finally 2 ≡ −1 is a unit
mod 3, and (−1)^{3m−n}(−1)^m = (−1)^n. ∎
Characteristics 5 and 7 give no simplification: the weights stay nonzero and distinct (mod 5: 3, 1, 4, 2; mod 7: 3, 1, 6, 4).
Characteristic 2 has no Fourier transform (1/8 is not invertible), so see D4.
Theorem D4 (read-twice: matchings; mod 2 is polynomial). If every variable occurs exactly twice, in two different clauses, then
C(φ) = #PM(G_φ). Here G_φ is the multigraph whose vertices are the clauses and whose edges are the variables; "exactly one true
variable per clause" is a perfect matching. Hence:
- C mod 2 = det over 𝔽₂ of the multiplicity adjacency matrix with zero diagonal. Reason: Pf² = det for the skew-symmetrised
  matrix, and x² ≡ x mod 2.
- For planar G_φ, C is exact in polynomial time (FKT / Pfaffian orientation).
Verified (onein3.py, exact):
- D1 on 400 random instances (n ≤ 9, m ≤ 4): 0 mismatches.
- D3 on the same 400: 0 mismatches.
- D4: 300 random read-twice instances, #PM = C and C mod 2 = det_𝔽₂: 0 mismatches.
- Caveat: 398 of the 400 random instances were satisfiable, so D1/D3 were checked almost only on instances with C > 0. They rest
  on the proofs; a check that includes unsatisfiable and C ≡ 0 (mod 3) instances is still to do.

## 3. Answers to handover §12 questions 1–5
1. Does the characteristic change the filter? YES, in characteristic 3: the dual signature collapses to NAE₃ with a global sign
   (D3). In characteristics 5 and 7: no. In characteristic 2: only through the primal Pfaffian structure (D4).
2. Does a basis change simplify the couplings? The coupling becomes AFFINE (parity, EVEN). The local constraint changes from
   ExactOne to f̂, or to NAE mod 3. Both are non-affine. The number of dual states is |ker B| = 2^{3m − rank B} = 2^{3m−n} when
   every variable occurs. That is smaller than 2^n only if the average occurrence is below 2. For read-k formulas it is 2^{(k−1)n}.
   No general state reduction.
3. Do the identities survive arbitrary composition? YES. D1, D3 and D4 hold instance-wise for every m.
4. Which modular information is preserved exactly? C mod 3 for every instance (D3). C mod 2 for read-twice instances (D4).
5. CRT? For n-variable formulas one needs C mod p for primes with product > 2^n: about n/ln n primes ≤ O(n).
   - Read-twice instances: mod 2 is easy, but every odd p asks for #PM mod p of a general graph, which contains the permanent
     mod p. That is hard for odd p (Valiant 1979; from memory, check at source).
   - The decision for read-twice is perfect matching, already in P (Edmonds), so this class is no route to NP-hard SAT.
   - General instances: no odd prime is known for which C mod p is easy. If C mod p were polynomial for all primes p ≤ O(n), CRT
     would give C exactly, and #P-completeness of counting positive 1-in-3-SAT (Creignou–Hermann: non-affine) would give FP = #P.
   - Precedent for "easy only at one modulus": Valiant 2006, "Accidental Algorithms" (#₇ planar read-twice monotone 3-CNF in P,
     the mod-2 version ⊕P-hard; from memory, check at source). Planarity is essential there, as in D4.

## 4. Precise missing step and decision
- Established (PI, exact checks): CF, D1, D3, D4.
- Missing step for the owner's architecture (filter → basis change → modular evaluation → CRT): a polynomial algorithm for
  C mod p for ≈ n/ln n distinct primes on GENERAL (non-planar, read ≥ 3) instances. D3 does not provide it for p = 3: it turns
  #1-in-3 mod 3 into #(NAE + parity) mod 3, another non-affine Boolean #CSP mod 3. Whether that has a known dichotomy status
  (Faben 2008, counting mod k for Boolean CSPs) must be checked at the source before any claim.
- Direction status: RETAIN, narrowly. The concrete next question, small and checkable: is N₃ (NAE₃ blocks + even parity per
  variable) computable mod 3 in polynomial time on any natural non-planar class where C mod 3 is not already known to be easy?
  A positive answer would be a genuine modulus-specific algorithm. A negative answer comes from the mod-k counting dichotomy.
- No statement about P vs NP follows from §1–§3.

## 5. Owner refinement (2026-11-18): top ANF coefficient over 𝔽₂
- Checked: ANF of the 1-in-3 indicator = x + y + z + xyz (monomials {1, 2, 4, 7}). #SAT mod 2 = [x_1⋯x_n] Π_j f_j: 300/300 random
  instances (lab/onein3/anf_top.py, Möbius transform).
- Exact combinatorial form: [x_1⋯x_n] Π f_j = #{(σ_j) : σ_j ∈ {{a}, {b}, {c}, {a, b, c}} for clause j = (a, b, c), ∪_j σ_j = [n]}
  mod 2. The covering count tracks exactly the "information contributing to the top coefficient". In general its state is the
  covered set.
- Known easy case inside the class: read-twice instances (D4: Pfaffian over 𝔽₂). Eliminating a private variable gives a NAND
  constraint (Σ_x f = 1 + yz), which leaves the 1-in-3 class.
- Hardness status for general positive 1-in-3: OPEN in this proofbook. The search for an OR-gadget (inputs, complements, constants
  T/Z, ≤ 3 auxiliary variables, ≤ 3 clauses, plus k = 2 with 4 clauses; count = c·OR with any constant c ≥ 1) found NONE
  (lab/onein3/gadget_search.py). Whether ⊕(positive 1-in-3-SAT) is ⊕P-complete must be settled by a larger gadget or at the
  source (Faben 2008, mod-k Boolean #CSP dichotomy).
- Owner's chain (VV isolation → parity → top coefficient): correct as stated. Note that VV adds XOR constraints. In ANF these are
  linear factors (1 + Σ x_i + c), so the product stays inside "1-in-3 ANFs × affine factors". A deterministic polynomial top-
  coefficient algorithm for that class would give NP ⊆ RP. That is a consequence, not an impossibility statement.

## 6. Parsimonious reduction 3-CNF → positive 1-in-3-SAT (PI, 2026-11-18) — settles §5 "hardness status"
Gadgets (E(x,y,z) :⇔ x + y + z = 1). Each is checked exhaustively in lab/onein3/gates.py:
- Constants: E(T,a,b), E(T,b,c), E(T,c,a) has exactly one solution, T = 1 and a = b = c = 0. (Owner, independently: 16
  assignments.) Z := a.
- Complement: E(x, x̄, Z), with exactly one x̄ = 1 − x.
- Implication: E(x, ȳ, a), with a = y − x; count = [x ≤ y] (1, 1, 0, 1 for xy = 00, 01, 10, 11). Hence #Impl-2SAT → positive 1-in-3
  is parsimonious, consistent with Creignou–Hermann (owner's source, Thm 4.3).
- Functional AND: E(l₁,a,b), E(l₂,a,c), E(u,l̄₁,c), with exactly one completion iff u = l₁ ∧ l₂.
- Functional OR: E(l₁,ū,a), E(l₂,ū,b), E(l̄₁,b,c) (ū = complement of the output), with exactly one completion iff u = l₁ ∨ l₂. [Corrected 2026-11-18: an earlier transcription wrote l̄₂ for ū.]
  (Found by exhaustive gadget search, 3 auxiliary variables; complements via the complement gadget.)
Reduction. For each clause (l₁ ∨ l₂ ∨ l₃): v = OR(OR(l₁, l₂), l₃) and E(v, a, b) with a, b THE ZERO variables of the constant gadget (a = b = 0), which forces v = 1. [Clarified 2026-11-19: with fresh a, b the gadget has two completions at v = 0.] Every auxiliary variable is a
function of the original variables, so the count is preserved: #3SAT(φ) = #1in3(φ'). Size: O(n + m) variables and clauses (at most
108 variables for n = m = 8).
Verified: lab/onein3/parsimonious.py, 300 random 3-CNF formulas (n ≤ 8, m ≤ 8), exact propagating model counter: 300/300 equal.
Theorem P. Counting positive 1-in-3-SAT mod 2 is ⊕P-complete under parsimonious reductions. Equivalently, extracting the top
coefficient [x₁⋯x_n] Π_j (x_a + x_b + x_c + x_a x_b x_c) over 𝔽₂ (with x² = x) is ⊕P-complete. The same holds for every prime p:
#3SAT mod p ≤ #1in3 mod p.
Proof. ⊕3SAT is ⊕P-complete (parsimonious Cook–Levin). Compose with the reduction above. ∎
Consequences (no impossibility claim):
- A deterministic polynomial top-coefficient algorithm for this class gives ⊕P = P. Hence NP ⊆ RP (Valiant–Vazirani) and
  PH ⊆ BPP (Toda).
- The class is closed under the owner's isolation step. VV's XOR constraints compile through the functional gates into positive
  1-in-3 clauses parsimoniously, so "isolation → parity → top coefficient" never leaves positive 1-in-3.
Remaining frontier inside the class (precise, small): read-twice is polynomial (D4, Pfaffian mod 2). The reduction above reads the
constants T and Z unboundedly. Which occurrence bound k makes ⊕ positive 1-in-3 ⊕P-complete (k = 3 with fresh constant gadgets per
use?) is the next checkable question. It locates exactly where the Pfaffian structure is lost.

## 7. Owner's mod-3 / mod-7 observation (2026-11-18): verified; exact structure = affine ternary code + MacWilliams
Checked in lab/onein3/ternary.py (ternary.out.json), 250 random instances (n ≤ 9, m ≤ 6):
- Integer indicator x+y+z−2(xy+xz+yz)+3xyz, and mod 3 x+y+z+xy+xz+yz: correct.
- Owner's formula C ≡ 5^m Σ_{y∈𝔽₃^m} 2^{−Σy} Π_i (1 + 2^{(Aᵀy)_i}) (mod 7): 250/250. The same formula with a primitive cube root
  ζ holds mod 13 (ζ = 3) and mod 19 (ζ = 7): 250/250 each. It holds for every p ≡ 1 (mod 3) and over ℂ (ζ = ω, exact integer
  identity). Nothing is specific to 7: 𝔽₇ just carries the characters of 𝔽₃.
Theorem T (ternary code form, PI). C(φ) = #{x ∈ 𝔽₃^n : Ax = 𝟙 over 𝔽₃, and x_i ≠ 2 for all i}.
Proof. For Boolean x the clause sums lie in {0,…,3}, and ≡ 1 (mod 3) only at 1. Conversely, words without a coordinate equal to 2
are Boolean. ∎
So C is ONE coefficient of the complete weight enumerator of the affine ternary code {x : Ax = 𝟙}: the words with zero 2s. The
owner's 3^m formula is exactly its MacWilliams transform onto the code generated by the clause incidence vectors (the characters of
𝔽₃ realised in 𝔽_p, p ≡ 1 mod 3). The two computation spaces "2^n vs 3^m" are a MacWilliams pair.
Cost (exact algorithms read off the structure; r = rank_𝔽₃ A):
- Primal: enumerate the 3^{n−r} words of the affine space and keep those without a 2. Checked: 250/250 equal to C.
- Dual: Σ_y depends on y only through c = Aᵀy, plus the factor Σ_{k∈ker Aᵀ} ζ^{−Σk} (= |ker| or 0). So only 3^r distinct terms
  are needed, not 3^m. (This reduction is proved; it was not computed separately.)
- Hence C is computable in time poly · 3^{min(r, n−r)} ≤ poly · 3^{n/2} ≈ 1.732^n. That is correct, but still exponential and
  weaker than the known specialised exact-cover counters. No complexity claim.
Answer to the owner's question (can a further transformation make the dual sum non-exponential in m?):
- In general, such a transformation is exactly as hard as the whole problem. By Theorem P (§6) the reduction is parsimonious, so
  #3SAT mod 7 = #1in3(φ') mod 7. A polynomial evaluation of the mod-7 dual for all instances would decide Mod₇P. With isolation
  (VV) that gives NP ⊆ RP. This is a consequence, not an impossibility.
- Provably polynomial cases: r = O(log n) (dual), n − r = O(log n) (primal), and read-twice planar (FKT, §2 D4).
- The precise open object: the complete weight enumerator coefficient "no 2s" of affine ternary codes coming from 0/1 incidence
  matrices with three ones per row, between these poly cases. For general linear codes, weight-enumerator evaluation is #P-hard
  (classical; check the exact citation before ledger use).

## 8. Owner's multilinearisation formulation (2026-11-18): verified; exact placement
Checked in lab/onein3/multilin.py (multilin.out.json):
- C = 2^n · ML(F)(½,…,½), with ML via the integer Möbius transform: 200/200.
- The same identity mod 3, 5, 7, 11 (½ ∈ 𝔽_p; for p = 3, ½ = −1): 200/200.
- Characteristic 2: ½ does not exist, and the statement degenerates to the top-ANF-coefficient identity (§5).
Placement (PI):
- M1 (where the difficulty sits). If no variable is shared, F = Π f_j is SYNTACTICALLY multilinear, and C = Π_j 3 for disjoint
  clauses, trivially. Multilinearisation is needed exactly because of shared variables, i.e. the coupling. ML(F) is the multilinear
  extension used in sum-check (LFKN). Evaluating it at ½ is the count itself, so an efficiently constructible small circuit for
  ML(Π f_j), for all positive 1-in-3 F, gives FP = #P via Theorem P. This is a consequence, not an impossibility.
- M2 (the read-twice case lands exactly on determinant vs permanent). For read-twice instances, ML(F)(r) = Σ_{perfect matchings M}
  Π_{e∈M} r_e Π_{e∉M} (1 − r_e), the weighted perfect-matching polynomial of the clause graph. Checked: 100/100 with random
  rational weights.
  - Planar clause graph: a Pfaffian (Kasteleyn), so a determinant-type circuit (VP).
  - General graph: the perfect-matching polynomial, which contains the permanent (bipartite case). VNP-complete in characteristic
    ≠ 2 (Valiant). Classical; check the exact statement at the source.
  - So "the algebraic cost of the Boolean sum" (owner's source: Orzel–Srinivasan–Tavenas–Yehudayoff, FSTTCS 2025) separates
    planar from non-planar read-twice 1-in-3 exactly along determinant vs permanent.
- M3 (Mahajan–Saurabh–Tavenas). Their VNP = VP statement concerns MULTILINEAR circuit classes. Π f_j with shared variables is not
  syntactically multilinear, so their theorem does not apply without a multilinearisation step. That step is what Hrubeš (owner's
  source, ECCC TR15-067) studies. Exact theorem statements are to be checked at the sources before ledger use; this proofbook claims
  only M1, M2 and the verified identities.
Open object (sharpened): for which coupling structures of 1-in-3 clauses does ML(Π f_j) have a polynomial-size, polynomially
constructible arithmetic circuit? Known yes: read-once (trivial), read-twice planar (Pfaffian). Known VNP-type: read-twice general.
Read ≥ 3: Theorem P (counting complete).

## 9. Owner's integer primal–dual (2026-11-18): verified; what W₀ − W₁ is
Checked in lab/onein3/intdual.py (intdual.out.json), 300 random instances (n ≤ 10, m ≤ 7):
- Primal with 2^{n−r} Boolean free-variable assignments (pivots computed, then checked ∈ {0, 1}): 300/300.
- Product identity Π_i(1 + ω^{u_i}) = (−1)^{n−z(u)} 2^{z(u)} for every u in the row space, exact in ℤ[ω]: 300/300. Reason:
  Σ_i u_i = 3Σ_j y_j ≡ 0 forces n₁ ≡ n₂ (mod 3), so ω^{2n₁+n₂} = 1.
- C = (W₀ − W₁)/3^r with W_j = Σ_{u∈U, u·x₀=j} w(u): 300/300. Integer arithmetic only, with no p ≡ 1 (mod 3) and no CRT.
- Cost: poly · min(2^{n−r}, 3^r). The worst case is at r/n = ln2/ln6 ≈ 0.3869, giving O*(1.5296^n). This improves the PI's
  1.732^n. It is not competitive with specialised exact-cover counters; no complexity claim.
Theorem S (translation symmetry, PI). Every row of A has three ones, so A𝟙 = 0 over 𝔽₃, and x ↦ x + c𝟙 permutes the coset
{Ax = 𝟙}. Hence #{coset words without 2} = #{without 0} = #{without 1} = C. There are no constant coset words (A(c𝟙) = 0 ≠ 𝟙), so
#{coset words missing at least one symbol} = 3C. Checked: lab/onein3/symmetry.py, 200/200.
What W₀ − W₁ is. g(0) = 2 and g(±1) = −1 has 𝔽₃-Fourier transform ĝ(0) = 0 and ĝ(±1) = 3. By Poisson summation (MacWilliams),
3^{−r}(W₀ − W₁) counts coset words with NO ZERO coordinate. By Theorem S that is C again. So the integer dual sum is the exact
MacWilliams image of the primal count. Evaluating it directly over subspaces or symmetry classes is the same task as counting C:
#P-complete in general by Theorem P, and polynomial on the classes in §8. This explains the formula and closes no gap.
The sharpened open object stays: the weight enumerator of U = rowspace_𝔽₃(A) at the point (2, −1, −1), twisted by the character
x₀, for codes generated by 0/1 rows of weight 3, in the region where neither r nor n − r is O(log n).

## 10. Owner's determinant identities (2026-11-18): proved by the owner, independently re-checked by the PI
Source: owner derivation and proof (own check: 700 + 1280 instances). Independent PI check: lab/onein3/minors.py (minors.out.json),
separate code: 700/700 and 700/700.
Theorem D5 (owner; occurrences ≤ 2, no planarity). Let every variable occur in at most two distinct clauses, and let every variable
in the count actually occur in a clause. B ∈ 𝔽₂^{m×m}: B_ij = #(variables shared by clauses i and j) mod 2 for i ≠ j;
B_ii = #(variables only in clause i) mod 2. Then #SAT(φ) mod 2 = det B.
Proof (owner). B is symmetric. Over 𝔽₂, every permutation that contains a cycle of length ≥ 3 is paired with the permutation that
reverses its first such cycle, so all such terms cancel. The remaining permutations consist of fixed points (private variables)
and transpositions (shared variables): exactly the exact covers of the clauses, with multiplicities mod 2. ∎
Caveat (PI): a variable that occurs in no clause doubles the count, so the parity is 0. The matrix does not see such variables.
D5 generalises D4 (read-twice) by the diagonal.
Theorem D6 (owner; principal-minor decomposition). Let H be the variables with ≥ 3 occurrences, E_h their clause sets, and B built
from the variables with 1–2 occurrences only. Then #SAT(φ) mod 2 = Σ_{S ⊆ H, E_h pairwise disjoint} det B[V∖U(S)] (det ∅ = 1),
with U(S) = ∪_{h∈S} E_h.
Proof (owner). Fix the true H-variables S. Their clauses are covered. Every other H-variable is false. A 1–2-occurrence variable
touching U(S) must be false, and it is absent from the principal submatrix. Apply D5 to the rest. ∎
Cost: poly · 2^{|H|} for the parity, and for the decision with |H| fixed (matching on the rest).
Status of the owner's open question ("can the sum over compatible hyperedge selections be evaluated jointly?"):
- In general this is the full ⊕(positive 1-in-3) problem, ⊕P-complete by Theorem P. A joint evaluation for all instances
  would give ⊕P = P.
- Whether it stays ⊕P-complete when every H-variable occurs EXACTLY 3 times and |H| = Θ(n) depends on a read-≤3 parsimonious
  reduction (copy chains through complements, with fresh zeros from constant gadgets). The PI's check of that reduction was
  interrupted by the owner (lab/onein3/read3.py written, not run to completion, no result). Status: UNVERIFIED.

### §10b. Read-≤3 hardness (owner's proof, 2026-11-18; PI re-check)
Construction (owner). A variable x with d occurrences becomes copies x_1..x_{d+1}, with x_1 = x itself (d NEW variables), x_j in the j-th original occurrence. [Clarified 2026-11-19: d+1 new copies would leave x orphaned and double the count.]
Links: E(x_j, t_j, 0), E(t_j, x_{j+1}, 0). Every 0 is the variable a of its own constant gadget E(T,a,b), E(T,b,c), E(T,c,a). The
links force t_j = 1 − x_j and x_{j+1} = x_j, so every original assignment has exactly one extension (parsimonious). Occurrences:
- middle copies 3, end copies ≤ 2;
- t_j: 2;
- T: 3; a: 2 + 1 use; b, c: 2.
Counts: N = 10D + n variables, K = 5D − n of them exactly 3 times (D = total occurrences, n = used variables), so 4/11 ≤ K/N < 1/2.
Theorem R3 (owner). Counting positive 1-in-3-SAT with every variable in ≤ 3 clauses is #P-complete, and its parity is ⊕P-complete.
This holds even with at least 4/11 of the variables occurring exactly 3 times. Proof: compose Theorem P (§6) with the construction. ∎
Verified (PI, lab/onein3/owner_read3.py, owner_read3.out.json; 150 random formulas): count preserved 150/150, max occurrence ≤ 3
150/150, N = 10D + n 150/150, K = 5D − n 150/150. A second, independent construction by the PI (shared zeros, three per gadget;
lab/onein3/read3.py) is running as a regression test; its result is recorded when available.
The sharp boundary inside positive 1-in-3: ≤ 2 occurrences → ⊕ in P (D5, det over 𝔽₂; decision by Edmonds); ≤ 3 occurrences →
⊕P-complete (R3). The owner reports a matching literature statement (TCS Stack Exchange, Creignou–Hermann); not re-checked at the
source by the PI.

### §10c. Differential-filter identity (owner, 2026-11-18; PI re-check)
P(z) = det(B + diag z) is multilinear in z, and its coefficient of Π_{i∈U} z_i is det B[V∖U]. With D_h = Π_{i∈E_h} ∂/∂z_i:
  C mod 2 = (Π_{h∈H} (1 + D_h)) P(z) |_{z=0}.
Overlapping selections differentiate some z_i twice and vanish by multilinearity, so the identity equals D6 in one expression.
Verified (PI, symbolic with sympy, 120 random formulas): 120/120.
Open constructive question (owner's formulation, retained): for which classes of 3-uniform incidence structures can the
hypergraph differential filter Π(1 + D_h) on a determinant polynomial be evaluated in polynomial time? The general class is
⊕P-complete (R3). Example (owner): for B = 0 the expression is the parity of exact covers of the 3-hypergraph; det(I + B) = 1
cannot see it.

## 11. Owner's product identity and the characteristic-2 obstruction to Waring decompositions (2026-11-18)
Source: owner derivation (own check 1470/1470). Independent PI re-check: lab/onein3/product_identity.py (sympy, M(z) as a symbolic
determinant, not via principal minors): 150/150.
Theorem PI (owner). If every counted variable occurs in some clause:
  #SAT(φ) mod 2 = [z₁⋯z_m] det(I + diag(z)B) · Π_{h∈H} (1 + Π_{i∈E_h} z_i)   over 𝔽₂.
Proof (owner). det(I + diag(z)B) = Σ_S det B[S,S] z^S. Overlapping hyperedges, and hyperedges overlapping S, create a z_i²
and cannot reach the square-free full monomial. What remains is D6. ∎
Equivalently, the computation happens in R = 𝔽₂[z]/(z₁², …, z_m²), where multiplication is disjoint-union (subset) convolution.
Characteristic-2 remark (owner, verified):
- Over 𝔽₂, ∂_i² = 0, so every directional derivative D_v = Σ a_i ∂_i has D_v² = 0. The hyperedge operator ∂₁∂₂∂₃ is nonzero
  (it maps z₁z₂z₃ ↦ 1). Checked symbolically.
- So Waring-type decompositions into powers of linear derivations (characteristic-0 apolarity) cannot represent D_h over 𝔽₂.
  Hasse derivatives / divided powers are the right tool.
- The owner's source check: arXiv:2512.13805 is "Waring decompositions of special binomials", over ℂ. It is not applicable as
  claimed by the external report.
PI structural addition (proved here, elementary). With g_i := 1 + z_i, R ≅ 𝔽₂[(ℤ/2)^m] (g_i² = 1 + z_i² = 1). The top coefficient
[z₁⋯z_m] f is the coefficient of g₁⋯g_m in the group basis, since z^{[m]} = Π(1 + g_i) = Σ_T g^T and the triangular change of
basis has a unit diagonal. 𝔽₂[(ℤ/2)^m] is a LOCAL ring (char 2 divides |G|; Maschke fails), so no character transform
diagonalises it. This is the same obstruction as the non-invertible 1/8 of §2 and the missing ½ of §8: in characteristic 2 the
Fourier route is closed for structural reasons, not for lack of a trick. Methods that do work in characteristic 2 are
Pfaffian / determinant structure (D4, D5) and subset convolution (O*(2^m)).
Rejected from the external report (owner's assessment, PI agrees):
- A Waring-rank lower bound for a general determinant gives no bound for these specific filters.
- Failure of four evaluation methods is no hardness certificate.
- Gurvits capacity approximates permanents of nonnegative matrices; it does not apply to exact parity with cancellations.
- Matchgate dichotomies concern planar Holant / #CSP. A matchgate-compatible local signature does not make non-planar networks
  tractable.
Open object (owner's formulation): for which non-trivial hypergraph structures (H, E_h) does [z₁⋯z_m] det(I + diag(z)B) Π(1 + z_{E_h})
admit a compact, directly evaluable representation, without the 2^m coefficients? The general class is ⊕P-complete (R3, §10b).

## 12. Which basis changes keep the determinant form? (PI lemma, 2026-11-18)
Lemma L. Let P, Q ∈ GL_m(𝔽₂) satisfy P(B + diag z)Q = B′ + diag(σz) for all z ∈ 𝔽₂^m. Then P is a permutation matrix, Q = Pᵀ,
and B′ = PBPᵀ.
Proof. For z = e_i, P e_i e_iᵀ Q = (P e_i)(e_iᵀ Q) must be diagonal. A rank-1 diagonal matrix has exactly one nonzero entry, so
P e_i and e_iᵀ Q are both supported on the same single index σ(i). P is invertible, so σ is a permutation. Over 𝔽₂ the nonzero
entries are 1. Then PQ restricted to the diagonal gives Q = Pᵀ. ∎
Consequence for the owner's question ("which transformations simplify the hyperedge operator without destroying the determinant
structure?"): same-size linear changes that preserve the form det(B + diag z) are clause relabellings only. A simplification
must therefore enlarge the matrix (Pfaffian or gadget extensions with extra rows) or transform the operator Π(1 + D_h) itself.
No experiment needed. Status: proved, elementary, not in the ledger.

## 13. Symmetry: Reynolds projection rejected; 2-group fixed-point reduction (owner, 2026-11-18; PI completion and check)
Rejected (owner's counterexample, PI agrees). The sign-character Reynolds projection (F − σF)/2 annihilates F = x+y+z+xyz (σ = x↔y,
σF = F), although the parity is [xyz]F = 1. Over 𝔽₂ it does not even exist (½ is missing, and +1 = −1). It is unusable as an
"annihilation operator" for T41.
The external modules, as reported by the owner, are not available to the PI and were not re-run here. The reported defects are:
- non-simultaneous sympy subs for permutations, which maps x₀x₁ to x₀²;
- float64 eigenvalue/PSD "certificates" for 𝔽₂ parities;
- an ALMA harness with fixed action probabilities, so its OPE claims do not hold.
None of these modules enters the stack.
Theorem FP (owner). Let G be a group of variable permutations that maps the clause set onto itself, with |G| = 2^k. Then
#SAT(φ) ≡ #Fix_G(Sol φ) ≡ #SAT(φ/G) (mod 2).
Proof (owner). The non-trivial G-orbits on solutions have size 2^a with a ≥ 1, so they vanish mod 2. Fixed solutions are exactly the
assignments that are constant on variable orbits. ∎
Completion (PI). Identifying variables of one orbit can turn a clause into Σ c_v u_v = 1 with c_v ∈ {1, 2, 3}. Exact preprocessing:
- c_v = 3: unsatisfiable, so the parity is 0;
- c_v = 2: u_v = 0, propagated;
- identical constraints are merged;
- an orbit variable left in no constraint doubles the count, so the parity is 0.
The remaining constraints are exactly-one constraints of size 1–3 on distinct variables. D5 applies whenever every remaining
variable lies in ≤ 2 constraints: the D5 proof uses only "each variable covers ≤ 2 clauses", not the clause size.
Verified (lab/onein3/fixpoint.py, fixpoint.out.json; 151 random instances closed under an involution σ, every variable used):
- #SAT(φ) mod 2 = #SAT(φ/G) mod 2: 151/151.
- The quotient → preprocessing → D5 path was applicable in 124 cases, all correct (124/124).
- 87 of these were read-≥3 in the original. So the chain Read-Three → symmetry quotient → Read-≤2 → det(B) mod 2 really
  decides the parity of instances outside D5.
Scope and caveats:
- G must be given (generators). Finding a 2-group of automorphisms is a separate problem (graph-isomorphism type), and the
  computation cost assumes it is known.
- The class is not automatically easy. φ ∪ σφ on disjoint copies has parity = parity(φ), so symmetric instances contain
  ⊕P-complete ones. The open question (owner) is which non-trivial read-three classes have a 2-group whose quotient is read ≤ 2.
  That is a structural property of (φ, G), now precisely stated.

### §13b. Incidence twins: a polynomially recognisable read-three class (owner, 2026-11-18; PI completion and check)
Lemma TW (owner). If two used variables x ≠ y have identical incidence columns (A_{·,x} = A_{·,y}), then x ↔ y is an automorphism.
By FP: #SAT(φ) ≡ #SAT(φ | x = y) (mod 2). Every clause of x has the form E(x, y, z), and with x = y = u it becomes 2u + z = 1. So
u = 0 and z = 1: set both twins to 0 and every third variable of their clauses to 1. Parity is preserved; satisfiability in general
is not. ∎
Procedure (owner; PI completion of the edge cases). Repeat:
- exactly-one unit propagation (exact: forced values, no branching);
- the twin rule.
Edge cases:
- a conflict gives parity 0;
- a remaining two-element clause E(x, y) of twins means 2u = 1, so no fixed point and parity 0;
- an unassigned variable that is in no remaining clause doubles the count, so parity 0;
- once every remaining variable lies in ≤ 2 clauses, use D5 (clause sizes 1–3 allowed).
Each twin step removes variables, so the procedure is polynomial. Twin detection is column comparison, O(nm).
Theorem TW-class (owner). Every positive 1-in-3 instance on which this procedure ends in D5, or decides the parity earlier, has
its parity computed in deterministic polynomial time, without computing an automorphism group.
Verified (lab/onein3/twins.py, twins.out.json; 231 random instances, 60% with planted twins):
- finished 178, correct 178/178, stuck (no twins, still read ≥ 3) 53;
- 106 of the finished instances were read ≥ 3 originally, and twin reductions were needed in exactly those 106;
- owner's example E(a,b,c), E(a,b,d), E(a,b,e): count 3, procedure parity 1 after one twin step.
Caveats (PI):
- The class is defined by this deterministic procedure. Independence of the order of twin steps (confluence) is NOT proved, so
  "reducible by SOME order" may be larger than what the greedy run recognises.
- The class is a parity class. Combined with VV isolation it would need closure under the isolation constraints, which is not
  examined.
- R3 (⊕P-completeness at read ≤ 3) is untouched. TW-class instances are a polynomially recognisable easy subclass, of the same
  kind as D5.

## Priority note (2026-11-18)
D4/D5 coincide with Björklund, "Exact Covers via Determinants" (STACS 2010), Lemma 4.2, specialised to unit weights: symmetric
matrix over characteristic 2, loops on the diagonal, cycle-reversal cancellation. D6/§10c/§11 is a close variant of Björklund's
inclusion–exclusion + determinant scheme. The full audit is in protocol/NOVELTY-AUDIT-T41.md. All T41 results remain correct as
stated; only the novelty assessment changes.

## 14. Planarity, holographic signatures, and the extended quotient class (owner review 2026-11-18; PI check)
- Clarification. T41 claims Pfaffian / FKT tractability ONLY for read-twice instances (graph perfect matching: §2 D4, §8 M2).
  The bracket "(non-planar, read ≥ 3)" in §4 does not mean that planar read-three is easier.
- Planar read-three is hard (owner's sources, not re-checked by the PI). Moore–Robson: positive planar 1-in-3-SAT is NP-complete
  even with every variable occurring exactly three times. Cai–Fan 2023: counting for planar cubic exact cover is #P-hard.
  #P-completeness of exactly the Moore–Robson class does not follow from NP-completeness alone (owner's precision). The genus-g
  Pfaffian method (4^g terms) concerns graph matchings, not hypergraph matchings. The relevant boundary is graph matching vs
  hypergraph exact cover, not planar vs non-planar.
- Hadamard signatures (PI recomputation). EQ₃ ↦ [2, 0, 2, 0] ∝ [1, 0, 1, 0] (even weights only: the matchgate parity condition holds).
  EXACT1₃ ↦ [3, 1, −1, −3] (all weights nonzero: the parity condition fails). So the Hadamard basis simplifies equality but does
  not make exactly-one matchgate-realisable. This does not exclude other bases; the full question is the simultaneous-
  realisability classification of Cai–Lu–Xia. Over 𝔽₂, H itself is singular (det H = −2 = 0), so any holographic computation must
  run over a field of characteristic ≠ 2 and be reduced mod 2 at the end.
- Rejected heuristic (owner). "Coefficients cancel mod 2 in the quotient" is false for exactly-one. E(u,u,v), i.e. 2u + v = 1,
  has exactly one solution (0, 1). Dropping the 2 gives v = 1 with two solutions, so parity 1 becomes 0. The exact quotient
  preprocessing of §13 (coefficient 2 forces u = 0) is the correct rule.
- Extended quotient class (owner's proposal, retained as a research object): φ → exact fixed-point quotient φ/G (a Boolean
  constraint system with coefficients 1–3) → test whether its constraint signatures are simultaneously realisable by matchgates
  under one basis, over a field of characteristic ≠ 2 → Pfaffian → value mod 2. A success needs every equality in this chain to be
  proved per instance. Unsolved residual instances are NOT labelled #P-hard.

### §14b. Counterexamples to an automatic quotient → Pfaffian step (owner, 2026-11-18; PI re-check)
- EQ₄ = [1, 0, 0, 0, 1] satisfies the even-weight parity condition but violates the 4-ary Grassmann–Plücker identity
  f₀₀₀₀f₁₁₁₁ = f₁₁₀₀f₀₀₁₁ − f₁₀₁₀f₀₁₀₁ + f₁₀₀₁f₀₁₁₀ (it gives 1 = 0). So EQ₄ is not a standard-basis matchgate signature, and
  "even orbit multiplicity ⇒ matchgate" is false. A basis that works for a particular family must be proved separately. PI check:
  identity fails.
- Cube example: E(a,b,c), E(a,b,d), E(a,c,d), E(b,c,d). Every variable occurs 3 times; summing gives 3(a+b+c+d) = 4, so
  #SAT = 0. The clause–variable incidence graph is K₄,₄ minus a perfect matching = the 3-cube (planar, cubic), with 9 perfect
  matchings. PI check: 0 solutions, 9 matchings, degrees (3,3,3,3). A Kasteleyn matrix of the incidence graph counts
  graph matchings, not exact covers. With two disjoint copies swapped by an involution, the fixed-point quotient is again this
  system. An exact orbit reduction + a planar quotient + a naive matching translation is wrong.
- External 18-variable prototype (owner's independent recomputation; the prototype was not available to the PI):
  - non-planar original and quotient;
  - 9 variable orbits instead of the claimed 6;
  - 3 fixed solutions vs 42 perfect matchings of the quotient incidence graph;
  - `range(M_bar.shape)` makes it non-executable;
  - no certified Kasteleyn orientation.
  It is not evidence for a quotient-Pfaffian identity and is not used.
- Valid form (owner). C(φ) ≡ C(φ/G) ≡ Holant(𝓕_{φ/G}) (mod 2):
  - the first step needs a formula-preserving 2-group (FP);
  - the second needs an exactly constructed Holant representation of the quotient;
  - a Pfaffian evaluation then needs a certified invertible basis change mapping ALL signatures to matchgates, plus a planar
    network.
  A given basis can be verified by exact tensor computation and Grassmann–Plücker identities. Existence is a separate theorem.
  Failure of a search proves no hardness. Claims such as "affine supports with arbitrary weights are solvable by Gaussian
  elimination" or a general "Cai–Lu eigenvalue condition" are not used without an exact theorem reference.
- Research object (sharpened). Which fixed-point quotients, still containing variables with ≥ 3 occurrences after propagation,
  admit a certified matchgate realisation? (Read ≤ 2 is already covered by D5 / Björklund Lemma 4.2.)

### §13c. AUT-2 and MOD-P (owner, 2026-11-18; PI exact check on small instances)
Statements (owner):
- AUT-2: for read ≤ 3 the incidence graph has maximum degree 3. Aut is computable in polynomial time (Luks 1982, bounded valence),
  a Sylow 2-subgroup G₂ in polynomial time (Kantor 1985), so φ/G₂ is constructible and #SAT(φ) ≡ #SAT(φ/G₂) mod 2 (FP).
- Uniqueness: all Sylow 2-subgroups are conjugate in Aut(φ), so their quotients are isomorphic.
- MOD-P: for a p-subgroup G_p, C(φ) ≡ C(φ/G_p) mod p. Different primes may use different quotients of the SAME global count,
  which is exactly the CRT-compatible form.
- Class 𝒞_{AUT2→D5} = {φ read ≤ 3 : φ/G₂ is read ≤ 2 after exact preprocessing}: polynomially recognisable, parity polynomial.
PI check (lab/onein3/aut2.py, aut2.log; Aut by brute force over variable permutations, n ≤ 7, greedy Sylow 2-subgroup plus all
conjugates; the polynomial-time claims of Luks / Kantor are literature results and are NOT exercised here):
- owner's 8-variable example: 0 twins, σ ∈ Aut (|Aut| = 2), count 3, fixed solutions 1 ✓.
- E(a,b,c): fixed points mod 2 = 1, mod 3 = 0, so C ≡ 3 mod 6 ✓.
- 285 random read ≤ 3 instances with a planted involution:
  - parity via the Sylow-2 quotient 285/285;
  - MOD-P with a 3-subgroup 81/81;
  - quotient → preprocessing → D5 applicable in 283 cases, correct 283/283;
  - instances with several Sylow 2-subgroups: quotients pairwise isomorphic 83/83;
  - instances without twins: 115, decided by the D5 path 113.
Caveats:
- Small instances make "quotient becomes read ≤ 2" very likely (283/285). This says nothing about the size of the class for large n.
- Novelty: see protocol/NOVELTY-AUDIT-T41.md. AUT-2 → D5 is a composition of known results (Luks, Kantor, FP, Björklund
  Lemma 4.2).
- MOD-P is only useful where instances have nontrivial p-symmetries. Generic instances have none, and then the reduction is the
  identity.

### §14c. External HolographicMatchgateVerifier (owner's review, 2026-11-18; prototype not available to the PI)
- Orbit contraction with port_groups = [[0, 1]] drops port 2 of a 3-ary clause (implicitly set to 0). That yields a unary zero
  signature instead of 2u + v = 1. The correct grouping is [[0, 1], [2]].
- The demo certifies EQ₄ as a standard-basis matchgate, but EQ₄ violates the 4-ary Grassmann–Plücker identity (1 ≠ 0, §14b).
- Not accepted as evidence. These defects concern only the external prototype, not FP, the quotient, or the possibility of
  another holographic basis.

### §14d. Overlap fusion, an exact equality rule, and a GL₂ no-go (owner, 2026-11-18; PI check)
- Fusion: F = E(x₁,x₂,x₃)·E(x₁,x₂,x₄) has support exactly {1000, 0100, 0011} (PI check ✓).
- Equality rule (owner): E(a,b,c) ∧ E(a,b,d) ⇔ E(a,b,c) ∧ (c = d). Proof: subtract the two equations. PI check: all 16
  assignments ✓. Unlike the twin rule, it preserves the EXACT count, not only the parity. It is a polynomial, lossless
  preprocessing step: identify c and d; the two clauses become identical and are merged. It may raise the occurrence count of
  the merged variable, so its interaction with the read bound must be tracked.
- Theorem GL2-NoGo (owner). No T ∈ GL₂(ℂ) makes T^{⊗4}F supported on only even or only odd Hamming weights. Since every matchgate
  signature satisfies the parity condition, no common GL₂ basis change maps F to a matchgate signature. Proof (owner): T^{⊗4}F is
  parity-supported iff K^{⊗4}F = ±F for K = T⁻¹ diag(1,−1) T = [[a, b], [c, −a]] with a² + bc = 1; a case analysis gives a
  contradiction. Independent PI check (lab/onein3/gl2_nogo.py): a Gröbner basis over ℚ of all 16 component equations plus
  a² + bc − 1 is {1} for both signs, so there is no complex solution ✓.
  Scope: this super-signature and one common GL₂ change only. Other super-signatures, other gadgets, or different transforms on
  the two sides of a bipartite Holant are not excluded.
- External "Cayley miner" / GL₂ certifier (owner's review; code not available to the PI). Defects reported:
  - both blocks fail to parse (`if list(gb) !=:`);
  - group generation uses the number of generators instead of the permutation length;
  - matchgate identities are only complete up to arity 4;
  - a failed sympy solve is treated as non-existence (false negatives possible);
  - Z₃ is mixed with 2-groups (its fixed-point count is valid mod 3, not mod 2; cf. MOD-P §13c).
  Not integrated into ALMA or FruitStack.
- Net gain for T41: the exact equality propagation rule and the GL2-NoGo theorem for this super-signature.

### §14e. MG-3: no common GL₂ basis makes EXACT1₃ and EQ_d (d ≥ 3) matchgates (owner, 2026-11-18; PI check)
Correction to an external draft (owner). "No basis satisfies even the PARITY conditions for EXACT1₃ and EQ₄" is false: T = I gives
EXACT1₃ = [0,1,0,0] (odd only) and EQ₄ = [1,0,0,0,1] (even only). Parity compatibility is weaker than matchgate realisability;
EQ₄ fails Grassmann–Plücker (§14b).
Theorem MG-3 (owner; statement made precise 2026-11-20 after independent review). In the bipartite holographic setting
Holant(EXACT1₃ | EQ_d) with ONE basis T ∈ GL₂(ℂ) applied to every clause node and (T⁻¹)ᵀ to every variable node, there is no T such
that T^{⊗3}·EXACT1₃ and ((T⁻¹)ᵀ)^{⊗d}·EQ_d (d ≥ 3) are both PLANAR matchgate signatures (Cai–Gorenstein). Not covered: higher-
dimensional bases, gadgets/super-signatures, non-planar matchgates, other transform pairings, tractability by other means.
Proof (owner):
- T = [[a, b], [c, e]] gives weight entries f₀′ = 3a²b, f₁′ = a²e + 2abc, f₂′ = bc² + 2ace, f₃′ = 3c²e.
- The parity condition (f₀′ = f₂′ = 0 or f₁′ = f₃′ = 0) with ae − bc ≠ 0 forces T diagonal or antidiagonal (monomial).
- Then the inverse transpose is monomial too, and EQ_d becomes α|0…0⟩ + β|1…1⟩ (or the swap), with αβ ≠ 0.
- d odd: mixed parity, so not a matchgate.
- d even: a matchgate signature with a nonzero weight-0 entry is f₀·Pf of the principal submatrices of a skew matrix (Cai–
  Gorenstein, "Matchgates Revisited"). All weight-2 entries vanish, so the matrix is 0, so the weight-d entry would be 0 ≠ β. ∎
PI check (lab/onein3/mg3.py, mg3.out.json):
- the four f′ formulas and symmetry of T^{⊗3}·EXACT1₃: symbolic ✓;
- with the invertibility variable t, b and c lie in the radical of ⟨f₀′, f₂′, (ae − bc)t − 1⟩, and a and e lie in the radical of
  ⟨f₁′, f₃′, (ae − bc)t − 1⟩ (Gröbner reduction): "parity ⇒ T monomial" ✓;
- the EQ_d step rests on the Pfaffian characterisation (literature; not re-derived).
Scope: one common GL₂ transform for these two unchanged signatures. It does not say that the instances are not polynomially
solvable by other means, and it says nothing about gadgets, super-signatures or other Holant formulations.
Propagation is sound, not complete (owner's counterexample, PI check ✓). E(x₀,x₁,x₂), E(x₀,x₃,x₄), E(x₀,x₅,x₆), E(x₁,x₃,x₅)
(read ≤ 3): no clause pair shares two variables, and there is no unit clause, yet x₀ = 0 in all 3 solutions. Local rules
(multiplicity ≥ 2 ⇒ 0, the equality rule of §14d, unit propagation) are SOUND but INCOMPLETE. No completeness, O(mk) bound or
uniqueness of the final state is claimed for them in T41.
External super_signature_certifier.py (owner's review; not available to the PI): `if list(gb) !=:`, identities only up to arity
4, failed candidate search reported as non-existence, no Pfaffian end-to-end evaluation. Not accepted as a certificate.
Reference for the last MG-3 step (PI, checked at the source, local copy literature/sources/cai-gorenstein-matchgates-revisited/):
Cai & Gorenstein, "Matchgates Revisited", Theory of Computing 10(7):167–197, 2014.
- Thm 2.1: every planar matchgate signature satisfies the MGI.
- Thm 5.1: over any field, every vector satisfying the MGI is a planar matchgate signature.
- Thm 2.2: the MGI imply the Parity Condition.
- Thm 7.1 (symmetric signatures): [z₀,…,z_k] is an even symmetric matchgate signature iff z_i = 0 for odd i and there are
  (r₁, r₂) ≠ (0, 0) with r₁ z_{i−2} = r₂ z_i for all even i ≥ 2. Analogously for odd signatures. Equivalently: alternate entries
  are zero, and the others form a geometric progression.
MG-3, even d ≥ 4, via Thm 7.1 (replaces the Pfaffian sketch). After a monomial T the image of EQ_d is the symmetric
[α, 0, …, 0, β] or its reverse, with αβ ≠ 0. For i = 2: r₁α = r₂·z₂ = 0, so r₁ = 0 and r₂ ≠ 0. For i = d: 0 = r₁z_{d−2} = r₂β,
so β = 0. Contradiction. ∎
Sharpness at d = 2 (Thm 7.1). EXACT1₃ = [0, 1, 0, 0] is odd symmetric with odd-position entries (1, 0): geometric with r₁ = 0.
EQ₂ = [1, 0, 1] is even symmetric with (1, 1): r₁ = r₂. Both are standard-basis matchgates, so MG-3 is sharp in d.
Status: MG-3 is a candidate for the proof register (owner's proof; PI symbolic check of steps 1–2; step 3 by the exact
literature theorem). Ledger only after iteration 11 or an independent review.

### §14f. Exact GL₂ matchgate solver (owner's tool, 2026-11-18; PI review and run)
Tool: lab/onein3/matchgate_miner.py (owner's code, stored verbatim; sympy 1.14, /opt/fruitstack/venv-host/bin/python).
PI code review:
- full MGI per Cai–Gorenstein Thm 2.1 (summing from j = 0 only flips the global sign);
- the reductions in the branch equations are exact (only opposite-parity α, β contribute; |α⊕β| = 2 vanishes identically);
- the dual side adj(T)ᵀ = det(T)·(T⁻¹)ᵀ is valid, because all equations are homogeneous;
- the gauges a = 1 and (a = 0, c = 1) cover GL₂;
- invertibility is enforced through z(ad − bc) − 1;
- PROVED_NO_BASIS only if every branch has Gröbner basis {1};
- a proper ideal is reported as EXISTS_NO_WITNESS (Nullstellensatz), not as FOUND;
- every FOUND is re-verified forward against all MGI.
Runs (PI):
- self-test 10/10;
- read2 (EXACT1₃, EQ₂): FOUND by the identity;
- mg3 (EQ₃) and eq4 (EQ₄): PROVED_NO_BASIS (8/8 branches inconsistent);
- super4 (fused F + EQ₃): PROVED_NO_BASIS (8/8).
All agree with the independent results (D5 / MG-3 sharpness d = 2; MG-3 odd and even; GL2-NoGo §14d).
PI hidden-basis test (lab/onein3/hidden_basis.json): EXACT1₃ and EQ₂ disguised by T₀ = [[1,1],[−2,−1]] (clause side T₀⁻¹,
variable side T₀ᵀ). The solver returned FOUND with T = [[1, ½], [2, 2]], forward-verified. The basis is not unique; a different
valid T was found.
Scope (owner and PI): certifies LOCAL matchgate compatibility of signature families (arity ≤ 6) under one bipartite holographic
basis. It does not reduce SAT to a Pfaffian, check planarity or global contraction, or prove hardness on PROVED_NO_BASIS. A
research instrument for T41. It is an exact CERTIFIER for given signature families, NOT an automatic Cayley/hypergraph miner: it searches no automorphisms and builds no quotients. Not integrated into FruitStack or CherryMe until an interface for independent certificate re-verification is defined (owner, 2026-11-18). A timeout gives INCONCLUSIVE, which is neither a counter-proof nor a fault in MG-3.
Machine-readable certificates (PI, 2026-11-18). Status of §14f: SOLVER-VALIDATED and CERTIFIED.
- lab/onein3/mg_certify.py writes certs/<demo>.json.
  - PROVED_NO_BASIS: for each of the 8 parity-profile × gauge branches, the exact branch generators (including z(ad − bc) − 1
    after the gauge) and Nullstellensatz cofactors c_i with Σ c_i f_i = 1, computed by SINGULAR `lift` (a CAS independent of
    sympy and of the solver's Gröbner run).
  - FOUND: the matrix T.
- lab/onein3/mg_verify.py is the independent verifier, in pure Python with exact Fractions: no sympy, no Gröbner, no solver code.
  - It re-derives every branch system from the instance definitions with its own tensor and MGI code, and requires equality with
    the certificate's generators up to sign, so a certificate for a weaker system is rejected.
  - It expands Σ c_i f_i and checks equality with 1.
  - It checks that all 8 branches are present.
  - For FOUND it recomputes T^{⊗k}·clauses and ((T⁻¹)ᵀ)^{⊗k}·variables and checks parity and ALL MGI.
- Results: mg3, eq4, super4 OK (8 branches each, 1 ∈ I verified by expansion); read2 and hidden_basis OK (T verified).
- Tamper tests, all rejected with the right reason: wrong cofactor, dropped generator (weaker system), missing branch, wrong T.
- Remaining assumption: the MGI system is the complete characterisation (Cai–Gorenstein Thm 2.1 + 5.1). This is a literature
  theorem, not re-proved here.
- Not integrated into CherryMe/FruitStack. The certificate format plus the verifier is the candidate interface for that decision
  (owner).

### §14g. Independent review of MG-3 (2026-11-20)
Separate reviewer (own code, no reuse of mg3.py / matchgate_miner.py; script lab/onein3/mg3_independent_review.py):
transformed entries CORRECT (also under the transposed convention); "parity + det ≠ 0 ⇒ T monomial" CORRECT (hand proof, both cases);
EQ_d step via Cai–Gorenstein Thm 2.1/2.2/7.1 CORRECT (theorems checked in the local paper copy; d odd by parity, d even ≥ 4 by Thm 7.1);
sharpness at d = 2 CORRECT; exact Gröbner check of all MGI with t·det − 1 over ℚ: basis {1} for d = 3, 4, 5 under both conventions,
proper ideal at d = 2 (T = I). Only defect: scope assumptions were in the note, not in the statement - fixed above. Verdict: MG-3
proved as now stated.
