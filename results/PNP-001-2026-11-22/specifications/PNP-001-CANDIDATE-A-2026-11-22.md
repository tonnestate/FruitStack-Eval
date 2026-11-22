# PNP-001 — Candidate A: adversarial test (owner priority 2026-11-22)

Owner: "Priorität: Q-9c4d56f01f – Candidate A adversarial prüfen." Source: FruitStack-Eval cc/pnp001-results-20261118 commit 57021bb,
results/PNP-001-2026-11-22/papers/PNP-001-UNIFIED-RESEARCH-SYNTHESIS-v0.3.md, Appendix A (verbatim below). Background: Basis-Blowup paper v4.0
(spec_read PNP-001-PAPER-BASIS-BLOWUP-v4.0.md: Thm 4.1 R/L/E, Thm 5.4, Cor 6.2, Remark 6.4, Prop 6.5).

**Candidate A (OPEN, not a proven theorem).** Fix the exact MMW Search-MCSP model with \(s=s(m)\) meeting all theorem hypotheses. There exist uniformly constructible graphs \(G_{m,s}\), linear spaces \(K_{m,s}\) with block structure and a computable transformation \(\mathcal A\mapsto B_\mathcal A\), defined for every admissible exact deterministic one-pass algorithm \(\mathcal A\), such that:

1. \(K_{m,s}\) satisfies (R), (L), (E) with fixed \(d\ge1\).
2. \(B_\mathcal A\) spans \(K_{m,s}\).
3. \(\operatorname{tw}(H_{B_\mathcal A})\le F(m,s,S_\mathcal A,U_\mathcal A)\), with all construction work, output processing and decoder cost accounted for.
4. The lower bound \(d(\operatorname{tw}(G_{m,s})+1)-1\) exceeds \(F\) for every resource bound allowed by MMW for sufficiently large parameters.
5. A precisely identified premise fails in the known MMW oracle-assisted construction.

Only if all five clauses are proved does Candidate A provide the desired width-based entry to QE*. Clause 4 must be asymptotic and uniform across the relevant exponent choices. Clause 5 cannot be satisfied by an informal assertion of nonrelativisation.

The immediate falsification task is to test Clause 3 against nonlinear state encodings, arbitrary DAG reuse, time-dependent recoding, deferred decoding, and easy high-width examples.

## Appendix B. The requested union theorem

## Task (adversarial, not supportive)
For EACH clause 1-5, try to break it first: a smallest counterexample, an admissible algorithm A whose B_A violates clause 2/3,
or a parameter regime where clause 4 fails. Priority is Clause 3 against: nonlinear state encodings, arbitrary DAG reuse/fan-out,
time-dependent recoding, deferred decoding/decoder work, alternative witnesses, and easy high-width functions (Prop 6.5, K_n).
Also check: is there ANY definition of A -> B_A for non-linear algorithms (Thm 4.1 is linear) - if none exists, say so precisely.
Clause 5: name the exact premise/inequality that fails for the MMW oracle construction, or show none does.
Clause 4: check exponents for every MMW-admissible s(n) (incl. s=2^{n/log* n}) and every poly(s) resource bound.
Record: per clause one of REFUTED (counterexample, lab ids) / SURVIVED this attack (what was tried) / OPEN (smallest missing lemma).
Finite checks are evidence, not proofs. Never call Candidate A proved; a survived attack is not a proof.
