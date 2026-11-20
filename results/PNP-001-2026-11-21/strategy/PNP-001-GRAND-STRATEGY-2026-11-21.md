# PNP-001 grand strategy (director, 2026-11-21, owner: "think big")

## 1 The one object we are missing
The transfer theorems already exist: MMW19 / CHMY Thm 1 (MCSP[2^{mu n}] not in one-tape time N^1.01 => P != NP), Theorem R
(R-MCSP + CJW20 => NP not in P/poly), Liu-Pass (time-bounded Kolmogorov hardness <=> one-way functions => P != NP), Williams
(fast Circuit-SAT for C => NEXP not in C). P != NP is therefore reduced to WEAK-LOOKING lower bounds for meta-complexity problems.
Every known lower-bound technique fails there for the same reasons. The missing object is ONE lower-bound technique that is
simultaneously:
- non-localizing (breaks when small fan-in oracle gates are allowed - MCSP has near-linear oracle circuits; CHOPRS),
- non-relativizing (MMW19 holds for MCSP^A for every oracle A, so a relativizing argument would separate P^A from NP^A for all A -
  impossible by Baker-Gill-Solovay; pure diagonalization is out),
- non-natural (Razborov-Rudich; and the barrier is itself a statement about MCSP),
- aimed at a meta-complexity problem.

## 2 Where barrier-breaking techniques have actually come from (last 15 years)
- ALGORITHMS => LOWER BOUNDS: Williams 2011/2014 (faster ACC0-SAT => NEXP not in ACC0), Chen-Hirahara-Ren / Li 2024 (range-avoidance
  algorithms => S2E needs near-maximum circuits). Both are non-natural and non-relativizing in essential steps. This is the only family
  that has produced new unconditional circuit lower bounds against strong classes recently.
- SELF-REFERENCE / META-COMPLEXITY: non-black-box reductions (Hirahara), Liu-Pass equivalences, Loff et al. 2026 (a method bounds itself).
- ALGEBRA / SYMMETRY: GCT multiplicities, algebraic metacomplexity (van den Berg et al. 2025) - long horizon.

## 3 Three programmes, each with a milestone ladder (milestones are real theorems, not activity)
P1 ALGORITHMIC METHOD - FruitStack's comparative advantage (algorithm discovery + exact evaluation).
  M1.1 A Circuit-SAT (or #SAT) algorithm beating 2^n by a superpolynomial factor for a class where no such algorithm is known - the
       named target is depth-2 threshold circuits THR o THR with superlinear wires (=> NEXP not in THR o THR via Williams' framework,
       a famous open problem). Algorithms are searched with the evolution engine, proved by the formal lane.
  M1.2 Push the range-avoidance pipeline (Korten reduction, win-win) towards classes inside NP / towards MCSP at the magnification
       threshold; state exactly which algorithmic speed-up would be needed.
  M1.3 The self-referential win-win: use a hypothetical fast MCSP algorithm itself as the algorithm in an algorithms-to-lower-bounds
       pipeline; either case yields a lower bound. Find the first case split that closes.
P2 META-COMPLEXITY LOWER BOUNDS - our own chain.
  M2.1 Second lever: raise the fixed-threshold formula exponent a(beta) above 2+beta (composition / KRW tools) - relaxes R-MCSP to c < a-1.
  M2.2 Settle the shrinkage self-barrier (does Loff et al. transfer to formulas?) - tells whether M2.1 needs a non-natural method.
  M2.3 One-tape route: local generator with seed below sqrt(t) (CHMY), with the log q oracle-absorption check.
  M2.4 Property P for MCSP (Theorem R hypothesis) and the elimination calculus.
P3 PROOF SYSTEMS AND ALGEBRA - the Cook-Reckhow line and GCT.
  M3.1 IPS line (Theorems 12/14/16 extended towards general IPS), ZH rewriting as a proof system.
  M3.2 GCT multiplicity obstructions in small cases as a source of conjectures (computation guides, proofs decide).

## 4 Rules of the programme
Breadth: the divergent lane stays open (WIDEN, DO NOT PRUNE). Rigour: claims go through the discovery contract; computation refutes or
suggests, proofs decide; every milestone states its exact consequence. A milestone short of P != NP that is a genuine new theorem
(e.g. NEXP not in THR o THR) counts as progress and is published as such - never as P != NP.
