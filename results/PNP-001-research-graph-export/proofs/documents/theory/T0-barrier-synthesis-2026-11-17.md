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

## Comparison baseline update (2026-11-17) — EXTERNAL_UNAUDITED_BENCHMARK
Sources read (by a research agent, not re-derived by us; the Lean files were inspected, not compiled):
- OpenAI preprint dated 2026-09-24 (github.com/openai/math, CONTENTS.md entry 108), Theorem 1.1: over C, for m >= 1408,
  border dc(per_m) >= m^3 / (5 529 600 e). Unpadded affine-linear model; Prop. 2.2 there shows equivalence with the padded
  orbit-closure model. Method: top polar degree of a smooth linear section vs. a multihomogeneous count on the determinant side
  (an enumerative degree count, not the Hessian-rank / dual-degeneracy dimension argument of Mignon–Ressayre / LMR).
  A Lean 4 formalization is in the repository. No peer-reviewed publication or independent confirmation found.
- arXiv:2606.15970 (Sheshadri), Cor. 7.11: every bound on dc(per_n) derivable as in its Theorem 7.7 is O(n^3). METHOD-SPECIFIC
  (corank-one kernel systems; one constant conditional); not a ceiling for determinantal-complexity methods in general.
- arXiv:2610.40484: extension to odd characteristic, Pfaffian representations, polynomial entries ("submitted to IMRN").
- arXiv:2611.06658 (Sheshadri): dc(per_4) = 15 over C, exact dc only; says nothing about border dc or about per_3.
Consequence for this project: the quadratic bound is no longer the comparison frontier for border dc; the claimed frontier is cubic.
Still polynomial — the asymptotic separation (n superpolynomial in m) is untouched. None of these texts contains equation degrees
or representation-theoretic multiplicities, so T11 (bracket 6 <= d_min^sep(3,4) <= 24) is unaffected.
