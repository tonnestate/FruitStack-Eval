# T4 — Paired cancellation (SOSA 2026, Bannach–Demaine–Gomez–Hecher): first candidate REFUTED (Claude PI, 2026-11-16)

Source read in full (easy_sharp2sat.pdf). Facts: ψ1=ψ∧e_0∧e_m∧C, ψ2=ψ∧e_0∧¬e_m∧C (C = parity counter w/o the red size-4 clauses);
Thm 3.8: #(φ)=#(ψ1)−#(ψ2); Lemmata 3.2/3.6/3.7 (rogue bijection).

## Lemma A (VALID; NOT novel — the paper states it)
ψ1,ψ2 differ in exactly one unit clause (e_m vs ¬e_m). So Δ(F)=Σ_{β⊨Φ}(−1)^{1⊕e_m(β)}, a single-variable signed count over one 2-CNF
Φ=ψ∧e_0∧C. The paper itself: "both ψ1 and ψ2 are almost identical and differ only in a single clause (a single literal)."
**Exact check (running example φ=c1∧c2∧c3): #(ψ1)=232, #(ψ2)=227, Δ=5=#(φ). Confirms Lemma A and Thm 3.8.**

## Candidate obstruction (my Claim B/C): REFUTED
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
- **No sign-free core exists** in this reduction (refuted above): the difference is genuinely signed at every layer (rogue AND non-rogue).
  Consistent with the authors' companion result (LICS/ESA 2025): #SAT ∈ [#2SAT−#2SAT], and this difference structure is GapP-complete.
  Deciding >0 for a general GapP function is PP-complete by definition, so a general cancellation zero-test gives P=PP⊇NP — the known wall.
- **Conclusion:** the "new operation A⋆B deciding existence without counting" cannot, in general, be easier than deciding PP. I have NO
  mechanism that escapes GapP/PP. Claiming otherwise would be false.

## Negative knowledge (recorded, do not re-explore without a new idea)
- NK-T4-1: the SOSA reduction exposes no sign-free survivor set; rogue-involution cancellation collapses to the full signed #φ difference.
- NK-T4-2: general paired-cancellation sign test = PP (known); no free lunch from the two-call reduction.

## Next justified step (only if a genuine new idea)
A non-vacuous contribution would need a RESTRICTED input family (e.g. bounded incidence treewidth k, where #SAT is already 2^k·poly) on
which the paired difference has special structure usable for a sign test faster than counting — but there #SAT is already easy, so it proves
nothing about P vs NP. For general CNF the direction is PP-equivalent and closed. Honest recommendation: this direction does not advance
P vs NP; return to the §13 uniformity-gap / non-algebrization thread, which at least isolates a real barrier rather than restating SAT.
