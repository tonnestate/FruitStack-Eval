# PNP-001 — Contract K1: Streaming-to-Formula Depth Reduction for MCSP
Owner contract 2026-11-21 (~21:35; authoritative text: the owner's message; this file is its working copy for agents).
Programme P2 (meta-complexity lower bounds). Target status: OPEN. Nothing here is proved unless a section says so explicitly.
Related (do not duplicate): Q-9540547936 (reuse bound from CJW Thm 1.6 + REUSE note), Q-2dc43864bc (proof-chain check backwards),
REUSE-MCSP-NOTE.md (R-MCSP, the broader obligation for arbitrary circuits).

## 0. Why
- CJW20 (Chen-Jin-Williams, STOC 2020, ECCC TR20-065) Theorem 1.6: for every beta in (0,1) and eta > 0, MCSP[N^beta] has no
  probabilistic De Morgan formulas of size N^{2+beta-eta}. PUBLISHED THEOREM - copy the exact statement, basis and leaf-count
  convention from the paper before using it.
- MMW19 (McKay-Murray-Williams, STOC 2019) Theorem 1.3: if search-MCSP^A[s] has no deterministic one-pass streaming algorithm with
  poly(s) space and poly(s) update time (A in PH), then P != NP. PUBLISHED THEOREM.
If every such streaming algorithm (A trivial, Boolean update circuits) converts into a De Morgan formula below N^{2+beta-eta} leaves, CJW20
proves the MMW19 hypothesis and so P != NP. K1 investigates that simulation - narrower than R-MCSP (only streaming circuits).

## 1. Exact target (fix before any proof attempt)
K1(beta, k): for all large n, N = 2^n, s = N^beta: every deterministic one-pass algorithm deciding MCSP[s] on truth tables in
lexicographic order, with state size S <= s^k, every update map F_t a Boolean circuit of size <= s^k and decoder circuit of size <= s^k, is
equivalent to a De Morgan formula with at most N^{2+beta-eta} leaves, for some eta > 0 independent of beta.
Tasks: (1) does the DECISION version suffice for MMW19 Thm 1.3 (search gives decision; state the direction precisely); (2) fix circuit
basis, leaf convention, whether F_t may depend on t (nonuniform), aligned with CJW20 Thm 1.6 and MMW19; (3) quantifier order: one eta for
all small beta, every fixed k - one prescribed (beta, k) is not enough; (4) the full chain K1 => MMW19 hypothesis => P != NP, each premise
labelled PUBLISHED THEOREM / INDEPENDENTLY PROVED / OPEN.

## 2. Mandatory negative tests (BEFORE any positive attempt)
A Oracle test: MMW19 Thm 1.2 gives a streaming algorithm with PH-oracle updates and poly(s) cost. From the locality paper (Chen, Hirahara,
  Oliveira, Pich, Rajgopal, Santhanam, ITCS 2020) decide whether the CJW20 formula bound still holds for formulas with small fan-in oracle
  leaves. If it does, a simulation treating update circuits as black boxes would turn the oracle algorithm into a too-small oracle
  formula - impossible. Record as a lemma: "a valid simulation must use the internal gate structure of F_t".
B Generic-simulation test: prove or refute that divide-and-conquer conversion of a width-2^S read-once program of length N gives formulas
  of size N^{Theta(S)} or N^{O(log 2^S)}, hence misses the target for S = N^{Theta(beta)}. Give the exact recursion.
C Function-independence test: a simulation valid for every function computed by poly(s)-streaming algorithms would give such (sequential
  depth ~N) algorithms formulas of size N^{2+o(1)} - a depth reduction for a large class. Does it contradict known results or plausible
  conjectures? Controls: iterated composition of a fixed permutation (Barrington-type), parity, inner product, prefix sums. If a control is
  poly(s)-streaming computable but needs formulas above the target, the simulation cannot be generic and must use MCSP-specific structure -
  record which property of MCSP is then required.
D Labels: per proof step, does it relativise, does it localise.

## 3. Exact small-instance evidence (only to test a stated lemma)
n = 2, 3 (N = 4, 8), small thresholds s: (i) minimum De Morgan formula size of MCSP[s] (exact, SAT or exhaustive); (ii) minimum total cost
of a one-pass realisation (sum of update circuit sizes + decoder) for S = 1, 2, ... using the EXISTING SAT synthesizer
(research/PNP-001-LEMMA-M/gate_pareto_sat.py - do not restart or disturb its running Pareto computation; new runs only after it
finishes or as separate small jobs); (iii) minimum formula size of the function computed by the cheapest one-pass realisations. Purpose:
test "formulas derived from optimal streaming circuits are not larger than optimal formulas" on exact instances. No large campaigns;
every number reproducible by a script in the repository and checked by a second independent method.

## 4. Output
One report K1-REPORT.md: (1) exact K1 + chain to P != NP with labelled premises; (2) tests A-D each as proved lemma, counterexample, or OPEN
with the precise missing step; (3) small-instance tables with scripts; (4) verdict PROVED (only if every premise established and
independently checked) / REFUTED (counterexample) / OPEN (smallest missing lemma).

## 5. Restrictions
Mathematical research only. No changes to FruitStack architecture, PlumMe, agent management or running PNP-001 sessions. No CI.
Proof-book conventions. Nothing PROVED without independent review. P != NP is not claimed unless every link is established.
