# QE-STAR-REPORT.md - independent critic review (2026-11-21)

Scope: every status-tagged bullet of QE-STAR-REPORT.md (R = report line). Sources checked by bounded line reads.
Abbrev: MMW = literature/sources/mmw19/paper.txt; LS = /root/contracts/PNP-001-STREAMING-LAMBDA-S-CHECK-2026-11-21.md (46 lines only);
SR = /root/contracts/STATE-RECODING-BOUNDS-CHECK-2026-11-21.md; OE = /root/contracts/PNP-001-ORACLE-ELIMINATION-CONTRACT-2026-11-21.md.

## Substantive findings (logic / quantifiers)
- R60 F-3 conclusion, "does not establish the uniform MMW premise and does not imply P!=NP on its own": ERROR. (a) Its own first
  sentence gives NP not in P/poly, and P is in P/poly, so P!=NP follows immediately. (b) Nonuniform QE* is the STRONGER statement:
  any uniform poly(s)-space, poly(s)-update algorithm (MMW L115-124) unrolls into poly(s)-size fan-in-2 F_t plus poly(s) decoder
  (TM time T, space S gives a circuit of size poly(T,S)), so nonuniform QE* implies the uniform MMW premise, hence P!=NP via Thm 1.3.
  The direction is inverted: the uniform premise does not imply nonuniform QE*, not the other way round.
- R58-59 F-3 derivation (NP in P/poly => NP/poly in P/poly => PH in P/poly; Sigma_3SAT^A in PH for A in PH; O~(s) query lengths
  give poly(s)-size circuits; O~(s^2)-step update with O~(s) space gives poly(s)-size F_t): CONFIRMED. Sketch only: the induction step
  NP^{Sigma_k} in NP/poly (oracle answered by advice circuits) is implicit, and R58 carries no citation (standard Karp-Lipton-type fact).
- R56/R76 F-2: CONFIRMED in substance (MMW L110-114 "Applying P=NP to the oracle calls in Thm 1.2"; L100-105 query length O~(s)).
  OVERSTATED wording: "query answers available at polynomial cost relative to B" presupposes the conclusion; the relativised task is not
  pinned (A in PH^B? B-oracle streaming machine?) and no witness B (e.g. a PSPACE-complete set) is named.
- R57 [REFUTED] over-reading of F-2: CONFIRMED in substance; cites Thm 4.1/B_n (MMW L561-565) although F-2 rests on Thm 1.2 Sigma_3SAT^A
  queries; ordinary-QE* cite LS 20-25 is wrong (QE* is LS L39).
- R66 smallest missing statement: CONFIRMED quantifiers (exists time-constructible s>=n, exists A in PH; MMW L115-118) and the
  "space AND update" polynomial pair negated correctly as "space OR update not poly". Wording: "requires super-polynomial" should read
  "for every pair of polynomials (p,q) no algorithm has space <= p(s) and update <= q(s)" (failure infinitely often suffices; "super-
  polynomial" can be read as an almost-everywhere bound, i.e. stronger than needed). "Deterministic" comes from the abstract
  (MMW L35-37), not the Thm 1.3 text.
- R18 vs LS L39: inconsistency. The recorded QE*/QE(2,3) are for ORDINARY Search-MCSP[s]; the report fixes A=SAT and never reconciles.
  Harmless logically (trivial oracle is in PH, so F-1/F-3 hold for both), but R57/R60/R79 mix "ordinary QE*" with the MCSP^SAT target.
- R45 CJSW: OVERSTATED/ERROR. A refuter finds counterexamples for EVERY C-algorithm (arXiv-2203.14379 L17-20), so a refuter does give a
  lower bound against the whole class. The valid distinction is counterexample-to-one-algorithm vs class lower bound; "blocks inferring a
  universal lower bound from one refuter" misstates the source.
- R32 Thm 4.1: ERROR (misquote). MMW L561-565: the ORACLE B_n has output bits computable in PH; the algorithm does not "output bits of a
  truth table computable in PH". Parameter t=200 s log s and O(2^n) time / O(t) space: CONFIRMED.

## Citation checks (claim content vs cited lines)
- R7 MMW L30-36 total search with "report none": CONFIRMED. R8 Thm 1.2 L100-105: CONFIRMED. R9-R10 Thm 1.3 L115-124: CONFIRMED.
- R11 LS 20-31: OVERSTATED cite. Counting lemma is LS L28-32, cell-probe LS L34-36, QE*/QE(2,3)/property P LS L38-44.
- R12/R21 LS 4-6: CONFIRMED content; "NON-UNIFORM" is LS L8 (outside the cited range).
- R13, R79: ERROR cite. LS 48-57 does not exist (file has 46 lines); content (conjectures open) is LS L38-44.
- R14 QE-STAR contract L31-32: CONFIRMED.
- R19, R20 MMW L115-124: CONFIRMED (work between reads, L121-124). "Refuting only one exponent pair" should be "proving".
- R22-R23 future-equivalence / live-dead: content CONFIRMED (I re-derived: same state + same continuation => same output; one circuit
  cannot compute two tables). Cite ERROR: LS 12-17 is Satz A (promise version); Satz B is LS L19-23.
- R24, R64, R75 unrolling: CONFIRMED (SR L68-73); re-derived: compose F_1..F_N then D_N; only the S state bits cross cut t|t+1.
  The label "INDEPENDENTLY PROVED" is fair for this trivial direction; "strongest ... theorem" (R64) overstates a one-line observation.
- R25 OE 50-69: CONFIRMED (Lemma B/E split also in QE-STAR contract L27-28).
- R31 Stream-Merge t=100 s log s, lexicographically first min-size circuit or 0^t (MMW L517-533): CONFIRMED.
- R33 O(t) Sigma_3 calls of length O~(t) per Stream-Merge call, update O~(t^2), space O~(t), time 2^n O~(t) (MMW L536-551): CONFIRMED.
- R34, R35, R39, R40: CONFIRMED.
- R41 5.3 [OPEN]: CONFIRMED (no derivation exists locally).
- R42 5.4: content CONFIRMED (MMW L121-124); cite LS 48-55 does not exist (amortisation remark is LS L11).
- R43 CHOPRS Thm 2 (chops-locality L470-489): CONFIRMED (B1O is an UPPER bound for gap-MCSP with fan-in <= N^eps oracles above XOR leaves;
  B3O InnerProduct, B4O SIZE_3 formulas; L423-424 only "believe applies more broadly").
- R44 Pich Thm 1 / Thm 3 (L163-170, L640-669): CONFIRMED.
- R46 CHMY Thm 1-2 (L121-160), Lemma 9 simulation (L488-507): CONFIRMED; note the source labels the simulation Lemma 9.
- R47 [OPEN]: CONFIRMED.
- R48 AM Thm 11 (L239-241), R49 Thm 27 (L795-815), R50 Thm 17 strongly explicit distinguisher (L482-493): CONFIRMED.
- R51 [OPEN]: CONFIRMED.
- R55 F-1: CONFIRMED (MMW L115-118 instantiated with A=SAT in NP in PH).
- R65, R73, R74 PUBLISHED THEOREM: CONFIRMED. R77 PH in P/poly: CONFIRMED (see R58). R78 [REFUTED] inference: CONFIRMED.
- R67 [OPEN] online cut-width route: CONFIRMED (SR L74-78). R68 counting: content CONFIRMED, cite ERROR (LS L28-32, not 20-24).
- R69 cell-probe: content CONFIRMED, cite ERROR (LS L34-36, not 25-26).
- R80 no P!=NP conclusion: CONFIRMED.

## Status inflation
No OPEN premise is labelled PROVED, and no PUBLISHED THEOREM is materially misquoted, except the Thm 4.1 detail (R32).
The INDEPENDENTLY PROVED unrolling (SR) is valid and re-derived here. F-3 ledger entry (R77) is sound; the error is R60's
downstream inference, which UNDERSTATES what nonuniform QE* implies.

## Overall verdict
Main conclusion stands: no proof of QE* exists locally, P!=NP is not established, and the smallest missing statement (R66) is the MMW
Thm 1.3 premise with correct quantifiers (exists s, exists A in PH; poly space AND poly update; wording "super-polynomial" to be
replaced by "not polynomially bounded"). Required repairs: R60 (inverted strength; nonuniform QE* implies the uniform premise and
P!=NP), R45 (refuter), R32 (B_n), and the eight LS line citations (R11, R13, R22-23, R42, R57, R68, R69, R79).
