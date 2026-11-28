# T43 — What do T40/T41 imply about ALL polynomial-time algorithms, and what is the missing bridge? (PI, 2026-11-18)

Owner's proof obligation (2026-11-18): "Which statement about ALL polynomial-time algorithms follows from our algebraic results?
If none, identify the exact missing mathematical bridge, without replacing it by more special-case tests."
No new computation; this document is a proof-structure analysis.

## 0. Corrections and precisions (owner)
- SAT ∉ P/poly ⇒ P ≠ NP; the converse is not known. A non-uniform circuit lower bound is STRONGER than the goal. The exact
  equivalent form of P ≠ NP is the uniform one: SAT has no P-uniform polynomial-size circuits (T36 Lemma N). The phrase "an
  invariant exists iff P ≠ NP" does not occur in this proofbook; it came from an external text.
- Best explicit B₂ lower bound: T39/T3 cite ≈ 3.1n (Li–Yang 2022). The owner reports a 2026 ECCC revision by Mishra–Santhanam
  with 4n − O(log n) over B₂ (improved gate elimination). The PI could not locate it (search 2026-11-18: B₂ 3.1n Li–Yang; 4n only
  for the basis U₂, Zwick 1991). Status: owner-reported, unverified; T39/T3 left unchanged until the source is identified.

## 1. What follows UNCONDITIONALLY about all polynomial-time algorithms: nothing
- T40 and T41 consist of (a) exact identities (count/parity representations), (b) polynomial algorithms for restricted
  classes (D5, twin class, AUT-2 → D5, small rank), and (c) completeness results (Theorem P, R3, Theorem H).
- (a) and (b) are upper bounds. (c) are reductions, and reductions relativise and give only relative statements.
- An unconditional statement "no polynomial-time algorithm computes X" for any X in NP would separate P from NP (or P from ⊕P,
  #P). None of (a)–(c) contains a step that bounds an arbitrary algorithm. This is the precise reason, not a barrier citation.

## 2. What follows CONDITIONALLY (proved, all from T41)
- C1 (Theorem P, R3). If some deterministic polynomial-time algorithm computes the parity of positive 1-in-3-SAT with ≤ 3
  occurrences, then ⊕P = P. Hence NP ⊆ RP (Valiant–Vazirani) and PH ⊆ BPP (Toda).
- C2 (Theorem P, exact counting version). If it computes the count, then FP = #P.
- C3 (D5 / Björklund Lemma 4.2). The boundary between occurrence 2 (polynomial) and occurrence 3 (complete) is sharp.
  ~~A polynomial algorithm must therefore fail exactly on what the read-3 gadgets create: variables shared by three clauses that are functionally determined by others.~~ **[Withdrawn 2026-11-28: only the different complexity classification of read-2 and read-3 families is proved. It does not localize the algorithmic difficulty on particular variables; a structural correlation was read as a causal statement.]**
These are statements about all polynomial-time algorithms, but only relative to the collapse of a class.

## 3. The only known theorem-type bridge from ALGORITHMS to LOWER BOUNDS: Williams' algorithmic method
Statement used (to be checked verbatim at the source before ledger use): Williams (STOC 2010 / SICOMP 2013, "Improving exhaustive
search implies superpolynomial lower bounds"). If Circuit-SAT for circuits with n inputs and n^k gates is solvable in time
2^n / n^{ω(1)} for every k, then NEXP ⊄ P/poly. Restricted-class versions give NEXP ⊄ ACC⁰ (2011) and NQP ⊄ ACC⁰
(Murray–Williams 2018).
Lemma B (PI, follows from T41 §6/§10b gadgets; proved). For every fan-in-2 circuit C with n inputs and s gates there is a positive
1-in-3 formula φ_C, computable in time poly(s), with:
- every variable in ≤ 3 clauses;
- O(s) variables;
- a designated set X of the n input variables;
- every assignment of X has exactly one extension if C(x) = 1 and none otherwise.
So #φ_C = #SAT(C), and SAT(φ_C) ⇔ C satisfiable.
Proof: the functional AND/OR/NOT gadgets of §6 (each completion unique), output forced to 1 by E(v, a, b), and the read-≤3 copy
chains of §10b (count-preserving). ∎ (The gadget correctness is computationally checked in §6/§10b. The general statement is
a direct composition.)
THE BRIDGE (precise, open). An algorithm that decides satisfiability of positive 1-in-3 formulas with ≤ 3 occurrences, given a
functional backdoor X (a set of n variables that determines all others), in time 2^n / n^{ω(1)} · poly(|φ|), applied to the
images φ_C of Lemma B, would decide Circuit-SAT in 2^n / n^{ω(1)} and give NEXP ⊄ P/poly by Williams.
Assessment:
- Existing T41 algorithms do not provide this. D5/twin/AUT-2 are polynomial only on classes the gadget images avoid. All other
  methods are exponential in the TOTAL number of variables O(s), not in |X| = n. The exponent must be in the backdoor size.
- Even full success gives NEXP ⊄ P/poly, not P ≠ NP (NEXP lower bounds do not scale down to NP; T34 J5).
- A ⊕-only algorithm is not assumed to suffice for Williams' theorem; the decision or counting version is required.

## 4. The bridge that P ≠ NP itself would need (for completeness)
Uniform form (T36 Lemma N): show that no P-uniform polynomial-size circuit family decides SAT. A route via Williams would need a
"P-uniform analogue": a non-trivial SAT algorithm against P-uniform circuits combined with a diagonalisation inside NP rather than
NEXP. No such scaled-down version of the algorithmic method is known. Its absence is the precise missing mathematical bridge
between algorithms like those in T40/T41 and P ≠ NP.

## 5. Next mathematical step (not a benchmark)
Question Q-BD (narrow, open, mathematically defined): for positive 1-in-3 formulas with ≤ 3 occurrences and a given functional
backdoor X with |X| = n, is satisfiability decidable in 2^n / n^{ω(1)} · poly(|φ|)?
- Known: trivially 2^n · poly by enumerating X and propagating, since every completion is forced.
- Any ω(1) saving in the exponent's base factor is the bridge to Williams.
- The algebraic tools of T41 (D5 on the read-2 part, FP on symmetric parts, the equality rule) are the candidates to ATTEMPT a
  saving. Each attempt must be proved, not tested.
