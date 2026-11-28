# T50 — Contradiction mechanism of the external VP≠VNP proofs and where it meets the Boolean world (PI, 2026-11-27)

Status: analysis of UNVERIFIED external work. It is kept strictly separate from established proofbook results.
- OpenAI, "VP and VNP are different", Nov 23 2026 edition: `dl_oai/vp23.txt`; its Lean build is running.
- Anthropic (Claude), "VP ≠ VNP over every field": `ant_paper/ant.txt`; its Lean build has not been started yet.

Only the overviews have been read (OpenAI §1; Anthropic §2.1, Figure 1, §2.5). The appendices have not been read.
Owner's directive, 2026-11-27: extract the mechanism, do not adopt the result, and do not assume the mechanism transfers to the Boolean setting.

## 1. The common mechanism: a win-win dichotomy on a geometric hypothesis
Both papers have the same skeleton.
- **Object.** Tensors over the field k. Wires are identity tensors ⟨q⟩. A price assigns lengths to wires: Anthropic uses spectral points φ after
  Strassen, OpenAI uses Euclidean wire lengths. Both papers derive a nonpositive-curvature structure of prices.
- **Dichotomy.** At least one of two hypotheses holds (Anthropic thm_alt; OpenAI's "strict shortening" or its negation). Neither paper
  knows which one holds.
  - **Flat / no shortening ⇒ rigidity.** A small circuit for the clause-sum polynomial f_{k,ℓ} (Anthropic (2.1)) splits into balanced parts
    with small rank across every balanced cut. A length comparison then gives log L ≥ ℓ·k^{3/2}/16. This is a direct lower bound.
  - **Contracting / shortening ⇒ diagonalization.** A wire saving lets one replay a hypothetical small circuit for the program polynomial
    Φ = Σ_w U_t(w) y^w more cheaply than gate by gate. That yields an "accelerator": sums over v^H steps in v^{H−16} steps. The saving iterates
    across scales. A diagonal / hierarchy argument shows that no such accelerators exist (thm_noacc). OpenAI: "if geometry fails to prove
    hardness directly, its failure powers a hierarchy theorem."
- **The law the owner asked for has, there, this form:**
  "small algebraic circuit" + (geometry) ⇒ "rank bound" (rigidity) **or** "iterable speedup", and an iterable speedup contradicts a
  hierarchy theorem that is proved unconditionally.
  - Where the circuit is used: in only two steps (Anthropic Figure 1, arrows C), namely lem_balanced and lem_lowdeg.
  - What those steps look at: the polynomial computed at every gate, specifically its **block-multilinear part** and its **low-degree part**.

## 2. Exactly where the transfer to Boolean computation breaks (connection to T48/T49)
**B1: the grading.** The arrows C use graded parts of the gate polynomials: homogeneous parts, block-multilinear parts, and low-degree parts.
- A Boolean circuit is correct only modulo the Boolean ideal I = (x_i² − x_i). It computes some g = f + Σ_i (x_i² − x_i)·h_i
  (Anthropic §2.5 says this explicitly).
- This is exactly T49 Lemma 3 (correctness is never formal) and T48 §3 (Boolean vs. formal cancellation).
- The ring F[x]/I has only a filtration, not a grading: x² ↦ x lowers the degree. Graded parts are not invariant mod I.
  Anthropic's example: (x_{1,1}² − x_{1,1})·x_{2,1}⋯x_{k,1} ∈ I, yet its block-linear part is −x_{1,1}⋯x_{k,1}.
- Our defect/deviation propagation (T48 8.1/9.1) does NOT construct g − f = Σ h_i(x_i² − x_i) for two circuits (correction 2026-11-28).
  T48 Thm 8.1 gives a compact representation of g² − g = Σ Q_i(x_i² − x_i), i.e. Booleanness of ONE circuit function; T48 Thm 9.1 relates a circuit to its OWN
  gate equations. Neither yields an equivalence certificate for two different circuits g, f computing the same Boolean function (that is an IPS/ideal-membership certificate,
  its existence and size are open, T48 9.5(c), and its verification is PIT/coNP-type). Even if such h_i were given, the graded parts of g are not those of f.

**What a Boolean transfer would need (precisely).** Call it MT, the multilinearization transfer:
"every Boolean circuit of size s for a multilinear f ∈ F2[x] (correct on {0,1}^n) yields an arithmetic F2-circuit of size poly(s) for f itself."
- NF(g) = Σ_{b∈{0,1}^n} g(b)·Π_i(x_ib_i + (1+x_i)(1+b_i)) always lies in VNP_2. So MT is a VNP → VP statement for this particular family.
- **B2: even MT does not reach NP.** HC_m over F2 is multilinear. Its Boolean function is ⊕#HC, and by Valiant's criterion and projection
  completeness (cited from memory; the papers' substitutions send 0/1 to 0/1) that function is ⊕P/poly-complete. MT plus the external theorem
  would therefore give only ⊕P ⊄ P/poly.
  - P = NP is not known to imply ⊕P ⊆ P/poly (Toda gives only PH ⊆ BPP^⊕P), so this is no contradiction with P = NP.
  - In characteristic ≠ 2, Boolean circuits compute 0/1 values, not counts. In general the algebraic objects are sums (counting) and NP is an OR (existence).
- **B3: the contracting case.** In the Boolean world the accelerator diagonal needs a fixed exponent saving that iterates (v^H → v^{H−16}).
  - P = NP gives only simulations NTIME(t) ⊆ DTIME(t^c) with c ≥ 1, so the saving goes the wrong way.
  - Known Boolean results of the type "speedup + slowdown ⇒ contradiction with hierarchy" are the alternation-trading proofs (time-space bounds
    for SAT; Fortnow, Williams; cited from memory). That is the T27 route, which the owner has closed.
  - Anthropic §2.5 states this too: "Nor can a large Boolean circuit take the place of the program … no way to run it faster than gate by gate."

## 3. Result
- The external mechanism is a dichotomy: geometric rigidity, or a speedup forced by the failure of rigidity, which then contradicts a hierarchy.
  It is exactly the kind of "law" the owner is looking for, but it is formulated for formal polynomials.
- It breaks on our Boolean correctness relation at a precisely identified point: the arrows C need a grading, and F[x]/I has none.
- The first unproved implication on this route is MT, Boolean size ⇒ arithmetic size for the multilinear representative.
  - Together with the external theorem, MT would be a Boolean lower bound (⊕P ⊄ P/poly). MT is therefore not a small step.
  - Even then the target would be ⊕P, not NP. A route to P ≠ NP would additionally need the step "counting → existence", for which no tool is known.
- Before any further use: complete both Lean builds, run `#print axioms`, and read the appendices (lem_balanced, lem_lowdeg, thm_noacc).
  Until then nothing goes into the proofbook as a result.

## 4. Correction (owner, 2026-11-27; checked by the PI)
**MT ⇔ VP = VNP (nonuniform, over F2).**
- (⇒) The HC check is in P. Its multilinear extension is f_m = Σ_{H∈𝓗_m} Π_{e∈H}X_e Π_{e∉H}(1 − X_e). Each summand has minimal degree m, so
  the homogeneous component of degree m is exactly HC_m, in every characteristic. A homogeneous component can be extracted from a circuit with
  polynomial overhead (Strassen homogenization). So MT ⇒ HC ∈ VP ⇒ VP = VNP, because HC is VNP-complete in every characteristic.
- (⇐) NF(C) = Σ_b C(b)·Π_i(x_ib_i + (1+x_i)(1+b_i)) lies in VNP (via the unique gate assignments).

Literature: Hrubeš, "On hardness of multilinearization, and VNP completeness in characteristics two", ECCC TR15-067 (2015). The owner found
this reference; the PI has not yet read it.
**Consequence.** The conditional in §2/§3, "MT + external theorem ⇒ ⊕P ⊄ P/poly", is logically correct but useless: if the external theorem
holds, MT is false, so the premises are incompatible. MT is removed as a bridge. No P = NP assumption is needed for this.
