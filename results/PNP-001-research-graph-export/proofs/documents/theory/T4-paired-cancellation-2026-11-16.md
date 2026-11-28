# T4 — Paired cancellation (SOSA 2026, Bannach–Demaine–Gomez–Hecher): first-stage claim refuted, two-stage mechanism RECOVERED (Claude PI 2026-11-16; repaired 2026-11-28)

Source read in full (easy_sharp2sat.pdf). Facts: ψ1=ψ∧e_0∧e_m∧C, ψ2=ψ∧e_0∧¬e_m∧C (C = parity counter w/o the red size-4 clauses);
Thm 3.8: #(φ)=#(ψ1)−#(ψ2); Lemmata 3.2/3.6/3.7 (rogue bijection).

## Lemma A (VALID; NOT novel — the paper states it)
ψ1,ψ2 differ in exactly one unit clause (e_m vs ¬e_m). So Δ(F)=Σ_{β⊨Φ}(−1)^{1⊕e_m(β)}, a single-variable signed count over one 2-CNF
Φ=ψ∧e_0∧C. The paper itself: "both ψ1 and ψ2 are almost identical and differ only in a single clause (a single literal)."
**Exact check (running example φ=c1∧c2∧c3): #(ψ1)=232, #(ψ2)=227, Δ=5=#(φ). Confirms Lemma A and Thm 3.8.**

## REPAIR 2026-11-28 (owner reconstruction, independently re-derived and re-computed; paper text read: Def. 3.1, 3.3–3.4, Lemma 3.6–3.7, Thm 3.8, Ex. 3.5)
**What row 91 refuted, exactly:** "after the FIRST (rogue) cancellation the survivors all carry sign +1 and biject with SAT(φ)". False: after rogue cancellation 11 positive / 6 negative non-rogue models remain. That statement stays refuted. **What was not refuted and was abandoned too early:** a second, explicit sign-reversing involution.
**Setting (paper Prop. 2.1, Def. 3.1).** ψ = ⋀_i ⋀_{ℓ∈c_i}(ĉ_i → ¬ℓ); a model of ψ over x is (x,S), S ⊆ V(x) = clauses violated by x, sign (−1)^{|S|}. ψ1 = ψ ∧ ξ (even |S|-parity counter), ψ2 = ψ ∧ ξ′ (odd), counters without the red size-4 clauses.
**Stage 1 (rogue cancellation, paper Lemma 3.7):** removes the models violating a red clause; the non-rogue models are exactly the pairs (x,S), counted 11 (|S| even, ψ1) and 6 (|S| odd, ψ2).
**Stage 2 (new here):** for V(x) ≠ ∅ let j(x) = min V(x) and ι(x,S) = (x, S △ {j(x)}). ι is an involution, reverses |S| parity (hence swaps ψ1-type and ψ2-type models and the sign), has no fixed point, and is defined for every unsatisfying x. The only unmatched pairs are (x,∅) with x ⊨ φ: positive survivors, sign +1, in bijection with SAT(φ). Counts: 232/227 → 11/6 → 5/0, difference 5 at each stage.
**Direct verification (this session, brute force over x, ĉ, e_0..e_p and all four auxiliary variables per step, exact):** without red clauses #ψ1 = 232, #ψ2 = 227; with red clauses 11 and 6; the pairs (x,S) number 11 even / 6 odd.
**Per-assignment transfer-matrix identity.** For fixed x with k violated clauses among m, the number of counter completions of all S ⊆ V(x) is e_aᵀ M e_a (ψ1) resp. e_aᵀ M e_b (ψ2), where the step matrix on the parity state (rows e_{i−1}, columns e_i) is T_0 = [[2,1],[1,2]] for ĉ_i = 0 (one rogue completion in each of the 4 positions + the case aux), T_1 = [[1,2],[2,1]] for ĉ_i = 1 (derived from the clauses of Def. 3.1: ĉ_i = 1 admits o-case for (1→0), e-case for (0→1), plus the rogue 'no case' completion), and T_0 + T_1 = 3J for a violated clause (S free). All commute; common eigenvectors (1,1) (eigenvalues 3, 3, 6) and (1,−1) (eigenvalues 1, −1, 0). Hence for k ≥ 1 the antisymmetric part is multiplied by 0, and
 **N_+(x) = (3^m 2^k + [k=0])/2, N_−(x) = (3^m 2^k − [k=0])/2, N_+(x) − N_−(x) = [x ⊨ φ].**
Checked exactly: all 8 assignments of the example (e.g. satisfying x: 14/13; unsatisfying: 27·2^{k−1} each) and 12 random small CNFs (0 violations); totals 70+162 = 232 and 65+162 = 227. Consequence: the cancellation is per assignment, not only global.
**What this is, and is not.** (i) The involution ι is Prop. 2.1's own inclusion–exclusion sign reversal written on the model set of ψ; its survivor set is SAT(φ) itself. The "sign-free core" therefore exists (the earlier "no sign-free core exists" is withdrawn), but it is SAT(φ), so it is not an independent shortcut: ι is cheap to evaluate, finding an unmatched pair is the search problem. (ii) The antisymmetric projection of the transfer matrix equals ∏_i [c_i satisfied] = φ(x): Σ_x of the antisymmetric eigenvalue is #φ by definition — no computation is saved. Novelty vs. the paper is not established (the identity is implicit in its Thm 3.8 argument). The correct reading of the symmetry: Z/2 parity swap acts on counter completions, 3J annihilates its sign character exactly at a violated clause.
**Class correction (replaces the PP argument below).** Δ(F) = #ψ1 − #ψ2 = #φ ≥ 0 for this family. "Δ > 0" is SAT (NP-complete), "Δ = 0" is UNSAT (coNP-complete). The PP-completeness of sign testing refers to arbitrary GapP functions and does not transfer to this nonnegative difference: P = PP is NOT implied by a poly-time zero test here; P = NP is (restatement of SAT).

## (superseded by the repair above where marked) Candidate obstruction (my Claim B/C)
I claimed: rogue models cancel (sign-reversing involution), the non-rogue survivors biject with SAT(φ) and all carry sign +1, hence
Δ=|SAT(φ)| is a sign-free core and no involution-based ⋆ beats #SAT. Two independent checks killed it:

1. **Independent adversarial review** (subagent, verbatim points): Claim C is circular — "Δ=|SAT(φ)|" is just Thm 3.8 restated, so "Δ>0 is
   NP-complete" is only "SAT is NP-complete", not an obstruction; "no sub-#SAT test unless NP⊆P" is a non sequitur (a test may be
   exponential); the all-+1 premise was unproven.
2. **Exact computation** on the example: non-rogue(ψ1)=11, non-rogue(ψ2)=**6 (≠0)**, rogue(ψ1)=rogue(ψ2)=221.
   - So the survivors do NOT all have sign +1: there are 6 non-rogue models of ψ2 with sign −1.
   - non-rogue(ψ1)=11 ≠ 5=#φ either. The clean "survivors = SAT" picture is false.
   - Correct structure: non-rogue(ψ1) = #φ (5, the E-set, all c_i=0) + X extra (6, with ≥2 clauses falsified, even c-parity);
     non-rogue(ψ2) = X (6, odd c-parity); Δ = 0 (rogue) + (#φ + X) − X = #φ. There is a SECOND signed cancellation among non-rogue models,
     which I had missed.

## Honest status of the direction
- **PCZT ≡ SAT, identically.** By Thm 3.8, Δ(F)=#(φ); "decide the sign of the paired difference" is literally "decide SAT". It is not a new
  problem with a new attack surface. A uniform poly-time zero-test ⟺ P=NP — restated, not advanced.
- **[WITHDRAWN 2026-11-28 — see REPAIR]** ~~No sign-free core exists~~ (a sign-free core exists after the second cancellation ι; it equals SAT(φ)); original text: No sign-free core exists in this reduction (refuted above): the difference is genuinely signed at every layer (rogue AND non-rogue).
  Consistent with the authors' companion result (LICS/ESA 2025): #SAT ∈ [#2SAT−#2SAT], and this difference structure is GapP-complete.
  [Scope corrected 2026-11-28: deciding >0 for a *general* GapP function is PP-complete; for this nonnegative family Δ>0 is SAT, i.e. NP-complete, so the PP wall does not apply.]
- **Conclusion (corrected):** for this family the operation is exactly as hard as SAT (not PP); no mechanism for efficient global evaluation is known. [Earlier: the "new operation A⋆B deciding existence without counting" cannot, in general, be easier than deciding PP — not supported.] I have NO
  mechanism that escapes GapP/PP. Claiming otherwise would be false.

## Negative knowledge (recorded, do not re-explore without a new idea)
- NK-T4-1 (corrected 2026-11-28): after the FIRST (rogue) cancellation the survivors are mixed-sign (11/6); after the second involution ι the survivors are exactly SAT(φ) with sign +1. A sign-free core exists; it is SAT(φ), so it gives no shortcut by itself.
- NK-T4-2 (corrected): the PP classification applies to general GapP sign tests only; for Δ = #φ the sign test is NP-complete. Efficient global evaluation of the local annihilation (3J kills the antisymmetric character) is OPEN, not excluded; it requires evaluating Σ_x ∏_i[c_i(x)].

## Next justified step (only if a genuine new idea)
A non-vacuous contribution would need a RESTRICTED input family (e.g. bounded incidence treewidth k, where #SAT is already 2^k·poly) on
which the paired difference has special structure usable for a sign test faster than counting — but there #SAT is already easy, so it proves
nothing about P vs NP. For general CNF the direction is PP-equivalent and closed. Honest recommendation: this direction does not advance
P vs NP; return to the §13 uniformity-gap / non-algebrization thread, which at least isolates a real barrier rather than restating SAT.

## Link to algebraic masking (T62/T63) — analogy, not a theorem (2026-11-28)
Both mechanisms are character sums over a small group: Williams' ADD identity Σ_{i=1}^m P(ω^i x̂+v) = P(v) (deg P < m) kills every nontrivial character of Z_m; here Σ_{ĉ_i∈{0,1}} (−1)^{ĉ_i}(…) = 0 kills the sign character of Z/2 exactly at a violated clause (step matrix 3J has antisymmetric eigenvalue 0). The cost question is identical in kind to T62 Theorem W2: the local annihilation is exact and cheap, but what survives is Σ_x ∏_i [c_i(x) satisfied], a sum over all 2^n assignments of a product of clause indicators — #SAT. The mechanism removes the *unwanted* mass (the symmetric part, size 3^m 2^k, which dwarfs #φ ≤ 2^n) without enumerating the S-sets per x, but does not reduce the sum over x. Open (not excluded): a global evaluation of Σ_x ∏_i [c_i(x)] that exploits the transfer structure — it would have to use structure of φ (bounded incidence treewidth gives it, see T25), since for general φ this is #SAT. The recovered mechanism is therefore a *local, exact, sign-character annihilator*; whether it composes with a sublinear-in-2^n summation is the unresolved obligation.
