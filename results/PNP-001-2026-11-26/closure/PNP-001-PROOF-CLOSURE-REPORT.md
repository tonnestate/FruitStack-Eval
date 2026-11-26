# PNP-001 Proof Closure Report

Started 2026-11-26 16:45 CET under the owner order "PNP-001 – Autonomous Proof Closure Mission".
Validation status of everything below: assessor derivations of one session and one model family unless a
Q-id:S-id with SURVIVED_REVIEW is cited. Nothing here is PROVED in the K11 sense. **P ≠ NP is not proved.**

## 1. Reverse proof graph from the target

Every edge is a mathematical implication; references are the evidence for that edge.

### Route M (MMW streaming magnification) — the only route with a published final implication

| # | Statement | Edge to the next line | Evidence | Status |
|---|---|---|---|---|
| M0 | P ≠ NP | — | — | target |
| M1 | ∃ time-constructible s(n) ≥ n, ∃ A ∈ PH: search-MCSP^A[s] has **no** uniform deterministic streaming algorithm with space poly(s) and worst-case update time poly(s) (fresh bit per step not required) | M1 ⇒ M0 | MMW19 Thm 1.3, `literature/sources/mmw19/paper.txt` l. 115–121 (quantifiers re-read 2026-11-26) | published |
| M2 | Γ^A_S lower bound: for the uniform class, max_t of the update cost is not poly(s) | M2 ⇔ M1 | Q-156fa9c912:S0037 (resource transfer, worst-case, SURVIVED_REVIEW), Q-156fa9c912:S0036 (representation completeness, SURVIVED_REVIEW), Q-0cce07fc92:S0024/S0027 (stage circuits incl. oracle slots, SURVIVED_REVIEW), Q-6ead6c935d:S0004 (class match, SURVIVED_REVIEW); assessor row R2-G0004-R1-STRENGTH (uniform QE* ⇔ (40a)) | reduction done, cross-family review pending for the assessor row |
| M3 | **OPEN CORE OBLIGATION O\***: a property of the update maps of every correct uniform algorithm for search-MCSP^A[s] that forces update time s^{ω(1)} | M3 ⇒ M2 | — | **open** |

Note (S0037): the right target is the worst case Γ_S = min max_t CC(F_t), not the sum Λ_S; Λ_S bounds imply Γ_S bounds (Λ_S ≤ N·Γ_S), not conversely.

### Routes R1, R2', W, ARITH (blocked or supporting)

| Route | Final implication | First failing inference | Repair attempted | Status |
|---|---|---|---|---|
| R1 self-diagonalisation (universal certificate verifier) | CC(W_{m,s}) ≤ C m^d s^{1-δ} ⇒ P ≠ NP | the bound is refuted under P = NP i.o. (Meyer), so proving it is proving P ≠ NP (TWENTYSEVENTH, NINETEENTH) | tensor contraction, QE arithmetisation, partial certificates (THIRTIETH–THIRTYTHIRD) | **blocked**: equivalent restatement |
| W witness-circuit / Williams | E^NP or NE lower bounds | P = NP ⇒ ∃L ∈ E with CC > c2^n/n a.e. (R1-KANNAN-UNDER-PNP): class lower bounds never contradict P = NP | — | **supporting route** (owner 2026-11-26) |
| ARITH (VP ≠ VNP, HC/permanent, tensor spectra) | — | formal → Boolean transfer; GL-invariant functionals see only |f^{-1}(1)| (R1-INVARIANCE-OBSTRUCTION) | — | **blocked** for Boolean conclusions |
| HTT magnification | HTT_{N^δ} ∉ DTIME(O(N)) ∀δ ⇒ P ≠ NP | hypothesis contradicts "E needs exponential circuits" (R1-HTT-MAGNIFICATION) | redirect to tasks whose quasi-linear hardness is the believed truth | **blocked** (wrong direction) |

## 2. Why O\* is the minimum remaining obligation and what any proof of it must avoid

Proved constraints (assessor, cross-family review pending):

1. **Information barrier.** S0006 (state O(s log s) suffices), S0010 (prefix separation), S0012 (counting), S0013 (cell-probe ceiling O(S/w)):
   every bound that depends only on states, ranks, fooling sets or cut measures is met by S0006 and cannot exceed polylog N.
2. **Oracle-locality barrier.** MMW19 Alg. 1 (blocks b = Θ(s log s), Stream-Merge) solves search-MCSP^A[s] with poly(s)
   state when each update may ask a Σ_k-oracle on poly(s)-length queries. A technique that is insensitive to what an update
   computes internally (it bounds only states or information) also "proves" a lower bound against these oracle updates, which is
   false. O\* must use the internal computation of the updates.
3. **Degree / rank controls.** OR accumulator (addendum 2026-11-21 §8 A): degree t at one gate per update; equality: rank 2^k at
   O(k) gates. Degree k d (p-1) ≥ 2^m (Q-f90dd2d84d:S0005, CLAIMED) constrains encodings, not update size.
4. **Re-encoding.** F'_t = π_{t+1} ∘ F_t ∘ π_t^{-1} (R2-COST-SHIFT): invariants must be relabelling-invariant; then they bound
   only a minimum over encodings (an MCSP-type minimisation).
5. **Quantifier order of the oracle freedom.** M1 needs ∃A ∀c. Deriving the update cost from A's own time complexity gives at
   most ∀c ∃A_c (time hierarchy inside P); a single A ∈ PH with superpolynomial time is P ≠ PH, i.e. the target. Hardness
   must come from the MCSP search structure, not from A.
6. **Strength.** The non-uniform version of M3 implies Σ_2 ⊄ P/poly, hence NP ⊄ P/poly (R2-G0004-R1-STRENGTH). Work on the
   uniform version.
7. **Unrolling.** Σ_{t<2^k} CC(F_t) ≥ CC(MCSP[s] on 2^k bits) − O(S) at aligned lengths (S0127 + S0033 unrolling,
   R2-Q-18a621cf3e-EXACT-FORM): non-uniform progress on O\* is an MCSP circuit lower bound at the magnification threshold.

## 3. Consolidated route table (mission §13 format)

| Route | Existing verified results | Remaining obligation | First failing inference | Proposed repair | Verification evidence | Status |
|---|---|---|---|---|---|---|
| M | MMW19 Thm 1.3 (published); S0036, S0037, Q-0cce07fc92:S0024/S0027, Q-6ead6c935d:S0004 (SURVIVED_REVIEW) | O\* (uniform update lower bound for search-MCSP^A[s]) | degree/rank → update cost (fails controls A, equality) | update-sensitive mechanism that survives barriers 1–7 | REVIEW lane (other family) | **active** |
| R1 | Q-filter results, partial certificates (THIRTYTHIRD) | CC(W_{m,s}) upper bound = P ≠ NP restated | Meyer step | none without new handle | assessor | blocked |
| W | OpenAI Cor. 1.4, Exact-One witness bound (THIRTYTHIRD) | — | Kannan under P = NP | supporting only | assessor | supporting |
| ARITH | VP ≠ VNP (formal), hexagon 2611.00149 barriers | formal → Boolean | GL invariance | none | assessor | blocked |

## 4. FruitStack allocation (2026-11-26 16:45)

- Peripheral lanes paused (T-B, T-A, K1, K2-K6, QW, MS-0.25, CAND-A, RECON, BINGO, QE*); backup `desk/lanes.json.bak-closure-1645`.
- Lane REVIEW: cross-family verification of the M-chain edges and the assessor rows used in §2.
- Lane CLOSURE: the core obligation O\* (counterexample-first) and the chain audit, admitted through `pnp_graph.gate`.
- Progress metric: closed critical obligations and verified edges only (`python -m pnp_graph.gate` metrics), not entry counts.
