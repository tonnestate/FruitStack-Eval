# T33 — OpenAI Cross-Theorem Proof Audit: Navier–Stokes blowup × forced-fluid computation × ETH refutation vs P ≠ NP (PI, 2026-11-17)

STATUS: primary sources read by the PI (theorem statements, Lean comparator signatures); cross-implications derived by the PI.
Independent adversarial review: FruitStack mission req-pnp-iter06.json (queued after iterations 4, 5). Not in the ledger before that.
Sources (local copies, /root/fruits/research/PNP-001/literature/sources/openai-math/):
- repo/ = github.com/openai/math at commit 4eaee87548250b2682affda7d05d947c05554bae (2026-10-29); CONTENTS.md entries 376, 378;
  lean/docs/376.md, 378.md; lean/ComparatorChallenges/ForcedNavierStokesComputation.lean, SubexponentialSAT.lean.
- navier-stokes-blowup.pdf (+ ns-blowup.txt) = https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf
  (NOT in openai/math at that commit; 165 pp.).
- Fluid manuscripts extracted to *.txt: Universal-Computation-with-Eventually-Stationary-..., Computation-under-Rapidly-Vanishing-...
Not checked: Lean proofs compiled by us (comparator files contain `sorry` by design; the proofs live elsewhere in lean/); the NS
blowup Lean development (location not found in the repo); independent expert reviews (only press reports on a priority dispute).

## 1. Verified theorem inventory (statements read in source)
(F1) NS blowup, Thm 1.1 (ns-blowup.txt l.36): ∀ν>0 ∃ f ∈ C_c^∞(R³×(0,∞)), compact K, smooth u,p on R³×[0,1), u(·,0)=0, forced NS,
  supports in K, sup_t ||u(t)||_{L²} < ∞, limsup_{t↑1} ||u(t)||_{L∞} = ∞. Claims alternatives (C) and (D) of Fefferman's statement
  (Cor. 10.6 for T³). Mechanism (§2): prescribed self-similar vortex; force := momentum residual, made smooth by oscillatory pulses
  whose fluxes cancel the singular residual. A single existence statement; no parameter that encodes an input.
(F2) Forced-fluid computation (entry 376, 9+ manuscripts). Representative: "Universal Computation with Eventually Stationary NS
  Forcing", Thm 1.1: for computable ν>0 an EFFECTIVE PROCEDURE maps (TM M, input w) to a smooth mean-zero force on T³, stationary for
  t ≥ 1, global smooth solution from rest, bounded energy, and the particle from P=(1/4,1/4,0) enters 𝒪={1/32<Y<1/8} at a finite
  time ⇔ M halts on w. Explicit: "There is no efficiency requirement" (l.67); "the theorem supplies no uniform finite-precision
  tolerance" (after Thm 1.1). "Computation under Rapidly Vanishing Forcing": "Each machine step takes one unit of physical time";
  "Our results supply no uniform finite-precision detection tolerance" (l.76); "No efficiency estimate is asserted" (l.155).
  Lean comparator `balanced_three_stack_realization` (ForcedNavierStokesComputation.lean): `EffectiveFamily` = Computable evaluator,
  bound and radius functions — NO complexity bound; halting ⇔ ∃ t ≥ 0, X(t, fixedLabel) ∈ observer — NO relation between t and the
  number of machine steps. Mechanism: tape as positional expansion of a real coordinate (Moore generalized shifts), Bennett-style
  history recording for invertibility, area-preserving realizations; force := residual of the prescribed velocity.
(F3) ETH refutation (entry 378; paper.pdf; my reconstruction T23, T28 §1): deterministic exact #k-CNF in (n+m)^{O_k(1)}
  2^{n/(log n)^{1/2+o(1)}}, polynomial space. Lean comparator `exact_count_and_sat`: one fixed machine, exact count + SAT bit, time ≤
  runtimeBound (formal bound (L+1)^{O_k(1)} 2^{O_k(n (loglog n)²/√log n)}, weaker than the manuscript), visited space ≤ S(L+1)^e at every
  prefix. Complexity consequence (paper; T23): a language in E^NP without circuits of size c·n·√log n on infinitely many lengths.

## 2. Dependency graph (theorem level)
F1 and F2 share ONE technique and no lemma: the inverse-design identity "prescribe a smooth divergence-free u, define f as the
residual" (F1 §2: "we can always define the external force f to be the residual"; F2 intro: "the force identity itself is elementary").
F2 does not use F1, F1 does not use F2, F3 uses neither. Consequence of the shared identity: for FORCED NS, every smooth
incompressible velocity field with smooth residual is a solution; F2's content is a theorem about effective smooth volume-preserving
flows realizing generalized shifts (Moore 1990; Cardona–Miranda–Peralta-Salas), F1's content is smoothness of one residual.
No composition edge exists in the published proofs.

## 3. Exact simulation and resource bounds of F2 (what the sources establish)
| resource | established | source |
|---|---|---|
| compiler (M,w) ↦ force description | computable; no complexity bound | Thm 1.1 "effective procedure", l.67; Lean EffectiveFamily |
| physical time per machine step | 1 unit (rapidly-vanishing construction); slow clocks are slower | abstract l.12; Scalar-potential paper |
| spatial precision | records at geometrically finer scales; no uniform tolerance | l.13, l.76, §6 |
| readout | exact continuous-time entry into an open set; late signals arbitrarily small | l.73–76 |
| time ↔ steps in Lean | none (∃ t) | comparator theorem |
So F2 is a COMPUTABILITY equivalence (halting ⇔ reachability), not a complexity-preserving simulation. The forward direction can
only be at least as slow as the machine (≥ one time unit per step).

## 4. Candidate cross-implications (Steps A–F)
(I1) Bounded fluid reachability is hard. A: F2 Thm 1.1 + unit-time steps. B: requires a POLY-TIME compiler and an exact time ↔ step
  relation — neither is established (§3). C: FR = {(M,w,t): particle enters 𝒪 by time t} would be EXP-hard for t in binary (time-bounded
  halting). D: lands in EXP; by T27 Lemma E, FR ∈ NP ⇔ NP = EXP. F: CONDITIONAL (missing: poly-time compiler + time–step bound) for the
  hardness itself; INAPPLICABLE to P ≠ NP (hierarchy hardness lives outside NP — T27 §4 translation problem).
(I2) Blowup + computation ⇒ Zeno machine (infinitely many machine steps before a finite time, deciding halting). A: no published lemma
  makes F1's singularity programmable or composes it with F2's recorder. C: not derivable from F1+F2 as stated. F: OPEN at the PDE level
  (missing: a programmable accumulation lemma); INAPPLICABLE to P vs NP — a hypercomputing PDE solution is not a classical algorithm, and
  physical time is not a step count (T31 §6).
(I3) ETH refutation + fluid ⇒ a fluid solves SAT in physical time 2^{n/(log n)^{1/2+o(1)}}. C: compile F3's machine with F2 (unit time
  per step). D: valid only under the I1 conditions; it is an UPPER bound and not polynomial. F: CONDITIONAL, trivial, no consequence for
  P vs NP (neither direction).
(I4) ETH false ⇒ P ≠ NP or P = NP? F3 is consistent with both (P = NP makes ETH false; P ≠ NP with 2^{n/polylog} SAT is consistent as
  far as known). Established consequence only: E^NP ⊄ SIZE(c n √log n) i.o. (T23). F: REFUTED as an implication to either side.
(I5) Undecidability (F2) ⇒ hardness inside NP. The only computational premises such a derivation can draw from F2 are halting
  undecidability and step-by-step simulation; both hold relative to every oracle (relativized halting is undecidable for oracle
  machines, simulation relativizes), while P^A = NP^A for some A (Baker–Gill–Solovay). (The fluid itself realizes finite tables only;
  the point is the logical form of the premises, not an oracle fluid.) Hence any derivation of P ≠ NP whose only complexity input is F2-type undecidability relativizes and cannot
  succeed. F: REFUTED as a route (relativization barrier); undecidability ≠ hardness.
(I6) Robust fluid computation. If a fluid construction HAD a uniform 1/poly tolerance, poly-time compiler and poly physical time, T29
  Lemma A (Grönwall) makes it classically simulable in polynomial time: it could only reproduce classical upper bounds (P direction),
  never a lower bound. F: INAPPLICABLE for lower bounds (proved, T29).

## 5. Answer to the mission question
The published OpenAI results (F1, F2, F3), alone or composed, do NOT imply P ≠ NP. Exact reasons:
- F1 is an existence theorem for one force; it has no input parameter and no complexity content.
- F2 is computability-level by its own statements (no efficiency, no tolerance, no time–step relation in Lean); any complexity reading
  needs the missing compiler/time lemmas, and even then yields EXP-hardness (outside NP, T27 Lemma E) or relativizing statements (I5).
- F3 is an upper bound; its proved lower-bound corollary is for E^NP against linear-size circuits.
Strongest remaining open lemma (precise): "complexity-preserving fluid simulation" — a poly-time compiler with physical time poly(T)
and readout tolerance 2^{-poly(T)} — and it would only give EXP-hardness of fluid prediction, not P ≠ NP. For P ≠ NP no lemma from
these papers is on the path; the open obligation remains the original statement (T21 target map; T27 Lemma S; T30 composition lemma).
New results: none claimed. Verified negative results: I4, I5 (proof sketches above), I6 (T29 Lemma A).
