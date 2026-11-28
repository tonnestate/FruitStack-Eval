# T51 — Transfer tests: the external contradiction mechanism vs. the hypothetical selector S (PI, 2026-11-27)

Status: CLAIMED (Claude family only). External works are UNVERIFIED; their Lean builds are not finished. These are symbolic derivations only.
Sources:
- OpenAI vp23.txt §1; Lean: CompressorLabelEvaluator, FiniteAlgebraEvaluator, FixedCompressedPairDiagonal, BalancedCircuit, CircuitDescent.
- Anthropic ant.txt §2.1, Fig. 1, §2.5.

Prerequisites: T48 (§3, 8.1, 9.1–9.4), T49, T50 (+ §4 correction), 17590.

## 0. Correction to T49 Lemma 4 (owner)
An argument that refutes all poly-size **circuit families** W with (*) proves NP ⊄ P/poly. An argument that uses the **uniform**
generation of S proves only P ≠ NP, and it does not have to prove the stronger statement. T49 §5 is correct only for the nonuniform variant.

## 1. Reconstruction (overview level; not yet independently checked line by line)
| Step | OpenAI | Anthropic |
|---|---|---|
| Assumption | an arithmetic circuit of size s ≤ n^c computing the formal polynomial P_n exactly (Lean: `hpoly : circuit.polynomial = map … (P n)`) | a circuit computing HC_m / PERM_m exactly |
| Object | coefficients c_x = number of accepting paths of the universal machine (program = prefix of x, input x); P_n = Σ c_x Π Z_{i,x_i} | f_{k,ℓ} (flat case) or Φ = Σ_w U_t(w) y^w (contracting case) |
| Local identities | gate equations → coefficient/label equations; common solution in a finite algebra (Macaulay/Cramer workspaces, prime chosen beforehand) | gate polynomials: block-linear part (lem_balanced) and low-degree part (lem_lowdeg) |
| Global combination | balanced product expansion: "the number of **graded** circuit states bounds every matrix rank" (BalancedCircuit; uses `homogeneousComponent`); tensor/price geometry | prices/spectral points with nonpositive curvature → dichotomy flat/contracting (thm_alt) |
| Contradiction | a fixed compressor-reader program evaluates coefficients from the compressed circuit within the clock; the coefficient is diagonalized ("this very coefficient plus one") | flat case: length comparison log L ≥ ℓk^{3/2}/16; contracting case: accelerator v^H → v^{H−16} iterates; no accelerators exist (diagonal, thm_noacc) |
| Essential prerequisites | (E1) exact formal identity; (E2) grading/homogeneous components; (E3) sums are counts (field); (E4) characteristic fixed before the threshold | (E1)–(E3); char ≠ 2 only for PERM |

Mechanism, stripped of its model: assumed small object ⇒ (graded) balanced rank decomposition ⇒ geometric dichotomy ⇒ either a rigidity bound
or an iterable speedup ⇒ contradiction with an unconditional hierarchy/diagonal theorem.

## 2. Transfer tests (each with its first failing step)
**T-A: formal → function on the whole Boolean domain (ring B_n).**
- Original implication: a small circuit for P_n gives a compressed representation of all c_x.
- In B_n: f_n at a Boolean point b is the **subcube sum** Σ_{x: b_{i,x_i} = 1 ∀i} c_x, i.e. counting.
- Owner's lemma, checked: efficient construction of arithmetic circuits for F_C ⇒ F_C(1) = ⊕SAT(C) ⇒ ⊕P = P.
- P = NP supplies no counting.
- **Fails at E3.** No PNP-001 theorem repairs this: defect and deviation propagation fix only the representative, not the sum.

**T-B: counts → canonical unique paths (parsimonious; Lemma B, functional gadgets).**
- The bare diagonal survives with 0/1 coefficients: D(x) = ¬Circ(x), where Circ is the circuit whose description is the prefix of x. It works
  only as long as the description fits into x, i.e. against size < n/log n. It relativizes and gives only linear bounds.
- The superpolynomial amplification needs a **joint** small object for exponentially many coefficients, a generating function.
- P = NP supplies only **pointwise** objects. For deterministic coefficients, pointwise circuits exist unconditionally, so no contradiction can
  come from them.
- Counterexample to "P-computable coefficients ⇒ joint object small": the support of PERM_m (σ is a permutation matrix) is decidable in P, yet
  its generating function is PERM_m. **Fails at the joint object.**

**T-C: counts → existence (idempotent sum).**
**Proposition C1 (proved).** Let K be a commutative semiring with 1 + 1 = 1. Then no polynomial p ∈ K[x] satisfies p(0) = 1 and p(1) = 0,
unless 1 = 0.
*Proof.* In an idempotent semiring, a ≤ b :⇔ a + b = b is a partial order compatible with + and ·
(a ≤ b ⇒ ac + bc = (a+b)c = bc). Hence polynomial maps are monotone. Since 0 + 1 = 1, we have 0 ≤ 1, so p(0) ≤ p(1), i.e. 1 ≤ 0, i.e. 1 = 1 + 0 = 0.
In a ring, 1 + 1 = 1 already forces 1 = 0. ∎
Consequence:
- Existential summation (OR) and non-monotone computation (NOT) cannot live together in one nontrivial commutative semiring.
- The hypothetical S, which decides existence and is non-monotone, is therefore not an object of any ring or semiring mechanism.
- Over the idempotent semiring, every circuit is monotone. Monotone barriers do not transfer: perfect matching is in P but needs superpolynomial
  monotone circuits (Razborov 1985, cited from memory).
- **Fails structurally (C1).** No transfer within commutative (semi)ring algebra.

**T-D: the contraction mechanism directly on finite Boolean functions (the owner's open question).**
- What survives:
  - Bit tensor networks have arbitrary local tables (OpenAI §2).
  - A Boolean circuit is a parsimonious bit network: functional gate tables, unique internal assignment. Its contraction gives the truth table.
    This is T48 9.1/9.4 and needs no formal coefficient.
  - The price geometry (spectral points over F2 tensors) is defined for these tensors.
- First failing step: the transition "circuit ⇒ balanced rank decomposition" (OpenAI BalancedCircuit; Anthropic lem_balanced, lem_lowdeg).
  It uses **additive degree along gate paths**: the graded states and the frontier between d/3 and 2d/3, as in VSBR.
  - In B_n, degree is not additive: x·x = x, so deg(gh) < deg g + deg h is possible (idempotence).
  - The frontier argument therefore breaks.
- What a B_n analogue would mean: a balanced decomposition with the VSBR parameters (depth O(log s·log n), size poly(s)) would yield
  P/poly ⊆ NC/poly. That is unproved and is generally considered false. This conclusion is drawn here as a sketch, not checked in detail.
- **Fails at E2 (idempotence destroys the grading).** No PNP-001 theorem supplies a degree-free progress measure.

**Owner correction (T50 §4):** MT ⇔ VP = VNP. As a bridge MT contradicts the external theorem, so it is removed.

## 3. Contradiction test (owner §7) for the whole chain
None of T-A to T-D yields a chain with all of the following:
- it uses P = NP;
- it holds for arbitrary uniform polynomial-time computations;
- it has a non-relativizing step;
- it ends in a contradiction.

Specifically:
- T-A needs ⊕P/#P.
- T-B needs a joint object that P = NP does not supply.
- T-C is impossible within commutative (semi)ring algebra (C1).
- T-D needs a degree-free balanced decomposition, which would be a depth-reduction statement.

## 4. Result
- **New and proved:** C1, the semiring incompatibility of existence and negation. It is presumably folklore; novelty is not claimed.
  It is the precise algebraic reason why ring-based contradiction mechanisms see only counting sums, never the existence sums that P = NP makes efficient.
- **First failing implications:** T-A at E3 (counting); T-B at the joint object; T-C at C1; T-D at E2 (the frontier argument without
  degree additivity).
- **Open, well posed:** is there a progress measure on B_n, or on parsimonious bit networks, that is additive along gate paths, bounded by
  poly(n), and still allows the balanced decomposition with rank bound across cuts? Any such measure would immediately face P vs NC.
  This is not a small step.
- **P ≠ NP has not been proved.**
