# PNP-001 grand strategy - revision 2026-11-21 (owner review applied; supersedes the first version of the same day)

## Guiding principle
Every milestone is tied to a PROVED transfer theorem. Unproved win-win arguments and algorithm targets that are too weak for the
transfer are recorded as open sub-tasks, never assumed as bridges.

## P1 - algorithmic method on threshold circuits (primary line)
- State of the art: Chen-Tal-Wang, ECCC TR26-039 (2026-03-14): there is f in E^NP with Size_{THR o THR}(f) >= n^{2.5-o(1)}, via a faster
  algorithm estimating the acceptance probability of the XOR of two THR o THR circuits + Williams' algorithmic method
  (spec_read('PNP-001-LIT-7-2026-11-21.md')).
- Milestone M1: scale the non-trivial acceptance-probability estimation (or #SAT / SAT) for THR o THR (and THR o MAJ) from size
  ~n^{2.5} to ARBITRARY polynomial size n^k, closed under the combination of several circuits that Williams' transfer creates.
  The sufficient conditions are attributed to Chen-Oliveira-Santhanam (CCC 2019; e.g. a non-trivial SAT algorithm for polynomial-size
  THR o MAJ) - NOT YET SOURCE-CHECKED (2026-11-21 search did not surface the paper); the exact transfer theorem must be stated from the
  source before the evolution engine optimises against it.
- Consequence on success: NEXP (or E^NP) not in THR o THR (resp. THR o MAJ) - a historic step at the TC0 frontier, NOT P != NP.

## P2 - meta-complexity and MCSP (hardness magnification, R-MCSP)
- Parameter gap: known lower bounds hold for LARGER thresholds than magnification needs - CKLM N^{3-o(1)} De Morgan formula bound and
  CHMY N^{1.99} one-tape bound (threshold 2^{mu_2 n}, mu_2 close to 1) vs the magnification thresholds (2^{mu_1 n}, N^beta for small beta).
- M2a (structural route, R-MCSP): an MCSP-specific formula simulation L(MCSP[N^beta]) <= C S^{1+c} with 1+c < 2 (r <= S), turning the
  FIXED-threshold formula bound of CJW20 Thm 1.6 (N^{2+beta-eta}; NOT CKLM, which needs a variable threshold) via Theorem R into an
  N^{1+eps} circuit bound. Second lever: a fixed-threshold exponent a(beta) above 2+beta relaxes the requirement to c < a-1.
- M2b (a win-win only after proof): (1) MCSP[theta] efficiently solvable => an explicit lower bound for a target class; (2) MCSP[theta]
  not efficiently solvable => exactly the lower bound, in exactly the model and parameter range theta, that the chosen magnification
  theorem requires. Both implications must be proved before the case split is used.
- Consequence on success: via MMW19 (Thm 1.4) / CJW19, NP not in P/poly and hence P != NP.
- Running sub-questions: property P, elimination calculus, HIW23 sharing, one-tape seed below sqrt(t), formula-exponent lever,
  shrinkage self-barrier, Liu-Pass Kolmogorov route.

## P3 - algebraic complexity and proof systems
- Starting point: IPS (Grochow-Pitassi) and restricted variants (roABP-IPS, multilinear, constant depth); our Theorems 12/14/16;
  ZH rewriting as a proof system; GCT multiplicities.
- M3: lower bounds for stronger IPS fragments / general algebraic circuits.
- Consequence: algebraic separations (super-polynomial lower bounds for full IPS imply VP != VNP); no automatic transfer to Boolean
  P != NP without additional bridge theorems.

## Governance: barrier audit per transfer theorem, not a blanket checklist
Methods are not rejected merely because they relativize, localize or are natural (Chen-Hirahara-Ren, TR23-144: their 2024 range-avoidance
lower bounds relativize). For each candidate proof, audit against ITS transfer theorem:
1. relativization: is there an oracle that falsifies exactly the target theorem? (For the MCSP magnification route yes in effect: MMW19
   holds for MCSP^A for every oracle A, so a relativizing proof would give P^A != NP^A for all A - excluded.)
2. natural proofs: does the proof use a constructive, dense property against a class that can contain pseudorandom functions?
3. locality: can the target function, at the concrete parameters, be solved by small fan-in oracle circuits the method cannot handle?

## Slot allocation
P1 primary; P2 and P3 stay open in parallel; the divergent lane (WIDEN, DO NOT PRUNE) stays open. The four slots are never again
restricted to a single direction.

## Consequence table
| Programme | Next solid breakthrough | Consequence |
|---|---|---|
| P1 algorithms | fast circuit analysis for sufficiently large threshold classes | new NEXP / E^NP lower bounds, not yet P != NP |
| P2 MCSP | a matching lower bound or a proof of R-MCSP | P != NP through the existing transfer theorems |
| P3 algebra / proof systems | a lower bound for a stronger proof system | depends on the system; no automatic transfer |
