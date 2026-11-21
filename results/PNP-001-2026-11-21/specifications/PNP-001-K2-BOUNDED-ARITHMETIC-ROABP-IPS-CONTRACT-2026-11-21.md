# PNP-001 — Contract K2: A Bounded-Arithmetic Theory for roABP-IPS
Owner contract 2026-11-21 (~21:30; authoritative text: the owner's message; this file is its working copy for agents).
Programme P3 (proof systems and algebra). Status OPEN. Literature and theory contract with one concrete theorem as its goal.

## 0. Why
Proof-book entry 3562 records the known correspondence: if correctness of a polynomial-time algorithm is provable in PV (or S^1_2), its
UNSAT answers translate into polynomial-size Extended Frege proofs (Cook 1975; Krajicek-Pudlak). Analogous correspondences exist for weaker
systems (V^0 and AC^0-Frege, VNC^1 and Frege, theories for Resolution and Res(log)).
PNP-001 holds Theorem 12 (THEOREM-12.md, building on Hakoniemi-Limaye-Tzameret, ECCC TR26-070): an explicit CNF family Psi_n needs
exponential-width roABP-IPS_LIN refutations in every variable order over every field.
If a theory T exists whose provably correct algorithms (or provable universal statements "for all x, phi(x)") translate into
polynomial-size roABP-IPS_LIN refutations, Theorem 12 gives unconditionally:
  No polynomial-time algorithm for SAT has correctness provable in T, and T does not prove that Psi_n is unsatisfiable (propositional
  translation).
This is NOT P != NP; it is an unprovability theorem about SAT algorithms built on a result PNP-001 already has.

## 1. Literature (check at the source, cite exact theorem numbers)
1. Known theory/proof-system correspondences (Cook-Nguyen, Krajicek): which theory <-> which propositional system, exact translation
   theorem (Paris-Wilkie style or Cook style).
2. Any known theory or translation for ALGEBRAIC proof systems: IPS, roABP-IPS, polynomial calculus, Nullstellensatz, "algebraic bounded
   arithmetic", theories over finite fields, Buss-Kolodziejczyk-Zdanowski, Tzameret-Cook work on algebraic/arithmetic theories for IPS
   fragments. Exact titles, venues, systems covered.
3. Is roABP-IPS_LIN (fixed or arbitrary order) known to simulate or be simulated by a propositional system that already has a theory? If
   roABP-IPS_LIN polynomially simulates Q with theory T_Q, Theorem 12 applies to T_Q only if Psi_n is hard for Q - check separately;
   record the direction carefully.

## 2. Theory task (if no theory is known)
- Define a two-sorted or algebraic theory T_roABP whose comprehension or induction is restricted to objects representable by read-once
  oblivious ABPs of polynomial width in a fixed order.
- Prove a translation theorem: every Sigma^b_0-type (or appropriate class of) consequence of T_roABP translates into a polynomial-width
  roABP-IPS_LIN refutation family.
- Test against TR26-070's upper bounds: Tseitin formulas and the functional pigeonhole principle have small roABP-IPS_LIN refutations
  (Propositions 20, 21). T_roABP must prove the corresponding principles; if it cannot, the translation is too weak and the theory is
  mis-specified.

## 3. Mandatory checks
- Apply Theorem 12 with its exact hypotheses: width measure, variable orders, field, the LIN restriction on placeholders incl. Boolean
  axioms.
- If the translation reaches roABP-IPS only in a fixed order, use the all-order Theorem 12 only if the translation produces every order,
  else restrict the conclusion.
- "T does not prove correctness of any poly-time SAT algorithm" != "SAT is not in P"; the second is NOT a consequence.

## 4. Output
One report K2-REPORT.md: (1) literature table: theory, proof system, translation theorem, source; (2) an existing theory to which Theorem
12 applies (full derivation of the unprovability theorem) OR a proposed T_roABP with the translation theorem proved or the precise failing
step; (3) labels PUBLISHED THEOREM / INDEPENDENTLY PROVED / OPEN / REFUTED; (4) novelty check: is such an unprovability statement for
algebraic proof systems already published?

## 5. Restrictions
Mathematical research only. No changes to FruitStack architecture, PlumMe, agent management or running PNP-001 sessions. No CI. Nothing
PROVED without independent review.
