# PNP-001 — Owner round F-J + source check (2026-11-21, late): K8 Range Avoidance / Constructive Refuters
Working copy for agents (authoritative text: the owner's message incl. the ChatGPT source check). Status OPEN. Never claim P != NP.
Note (director 2026-11-21): the owner later issued "Contract K8: Bridge Map" (PNP-001-K8-BRIDGE-MAP-CONTRACT-2026-11-21.md) as umbrella; the questions below are its Stage C (F+G), Stage E/K1 (H, J) and a control (I).

## Status tags (owner convention, binding from now on)
[Q] checked at the source (quote/link) - [G] from memory, source still to check - [E] own inference/idea, unpublished -
[B] proved/computed by the author (proof or script attached). Merge rules: (1) if a critic contradicts an [E] statement, the
proof book carries the weaker version until proved or refuted; (2) on source questions, whoever checked the source wins;
(3) an idea both sides consider dead is not deleted but booked as STOP with the reason (WIDEN, DO NOT PRUNE).

## K8 main strand (F + G together, T-B lane) - owner decision: one strand, not two contracts
- [Q] Chen-Jin-Santhanam-Williams, "Constructive Separations and Their Consequences" (FOCS 2021): Thm 1.3 (P^NP-constructive
  refuter vs certain uniform randomized streaming algorithms for an NP problem => EXP^NP != BPP), Thm 1.4 (uniform AC^0 refuter vs
  randomized streaming for DISJ => P != NP), Thm 1.7 (uniform refuter for MCSP vs AC^0 => P != NP), Prop 4.3 (sufficiently uniform
  quasi-poly AC^0 refuter against the ALWAYS-YES algorithm for MCSP at suitable thresholds => P != NP). Re-check exact parameters.
- [B, literature-known] A refuter against A(y)=1 outputs y with MCSP[s](y)=0, i.e. y outside Image(Eval_{n,s}): a Range-Avoidance
  witness. Decision MCSP is the right object (a refuter vs always-NO must find an ACCEPTED table - the other direction).
- Gap task: which resource bound (uniformity, refuter size, input length, unbounded parameter families) prevents our finite SAT
  counterexample generator (research/PNP-001-LEMMA-M/gate_pareto_sat.py) from being the Prop 4.3 refuter? A finite generator is NOT a
  uniform asymptotically efficient refuter.
- F (Korten 2021 APEPP completeness; Chen-Hirahara-Ren STOC 2024 iterative win-win; Li improvement) [Q]: first required theorem is a
  precise reduction between a bounded online Search-MCSP model and a Range-Avoidance task. The published win-win uses oracles,
  pseudodeterminism and several input lengths - do not silently replace them by streaming space/update bounds. [E] open.
- Do not conflate S_2E ("symmetric exponential time", alternation class) with symmetric circuits (Anderson-Dawar).

## I - control theorem (T-A lane)
[Q] Atserias-Bulatov-Dawar 2009 (linear equations over finite abelian groups incl. F_3 not FPC-definable); [Q] Anderson-Dawar
2017 Thm 1 (P-uniform poly-size symmetric majority circuits = FPC). [B, not independently checked] every polymorphism of
R = {100,010,001} is a projection (h(A)+h(B)+h(C)=1 over partitions => additive => single index). With Geiger/BKKR: every Boolean
relation pp-definable from R and =, giving an FO reduction F_3-equations -> positive 1-in-3. Claimed corollary: positive 1-in-3 not
FPC-definable, hence no such symmetric circuits. Expected: known corollary (bounded-width theory). Use as calibrated filter:
which property of 1-in-3 survives removing symmetry? Not a route to P != NP (symmetric circuits miss Gaussian elimination over GF(2)).
Entry 922 (two-value criterion) not read by the owner's checker - verify its content.

## H - tau conjecture / Binary Value Principle (K2-K6 lane) [G]
Shub-Smale (tau => P != NP over C, BSS); Alekseev-Grigoriev-Hirsch-Tzameret (tau => superpolynomial IPS lower bounds for BVP).
Question: do our exact GF(2) carry degrees (2^j, Lucas) give an UNCONDITIONAL lower bound for an IPS fragment on BVP? Check
characteristic: BVP lives over Q/Z; GF(2) degrees need not transfer.

## J - Pessiland 2026 (K1 lane) [G]
Hirahara-Nanashima 2026 (NP hard on average iff agnostic-learning MDL hard to approximate on average) - verify the source exists.
Question: does ST-MCSP already follow from average-case hardness of NP (weaker than the PRFs of Lemma C)?

Restrictions: mathematical research only; no architecture/PlumMe/orchestration/CI changes; nothing PROVED without independent review.
