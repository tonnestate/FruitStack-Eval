# T5 — The uniformity gap: uniform magnification (MMW) and the reach of known uniform techniques (PI, 2026-11-16)

Continues T3 §13 ("the uniformity-gap question stays open"). Lower-bound side of the program (see protocol/PROGRAM-CHARTER-2026-11-16.md).
Nothing here is a new separation. The propositions are elementary and are recorded for routing. Revised after independent review (§6).

## 1. Sources read (primary text)

- **[MMW19]** McKay, Murray, Williams, *Weak lower bounds on resource-bounded compression imply strong separations of complexity
  classes*, STOC 2019, pp. 1215–1225 (https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf). Notation: N = 2^n is the input length,
  s = s(n) is a function of n = log N.
  - **Theorem 1.2 (verbatim):** "Let s(n) ≥ n for all n, where s(n) is time constructible. Let A : {0,1}⋆ → {0,1} be an arbitrary
    oracle. There is a (one-pass) streaming algorithm for search-MCSP^A[s(n)] on 2^n-bit inputs running in 2^n·Õ(s(n)) time with
    Õ(s(n)²) update time and Õ(s(n)) space, using an oracle for Σ3SAT^A with queries of length Õ(s(n))."
  - **Theorem 1.3 (verbatim):** "If there is some time-constructible s(n) ≥ n and an A ∈ PH such that search-MCSP^A[s(n)] is not
    solvable by a poly(s(n))-space streaming algorithm with poly(s(n)) update time, then P ≠ NP."
  - Authors' remark: "there is no information-theoretic barrier to such a streaming algorithm, only a computational one".
  - Other uniform routes to P ≠ NP exist: [OS18] (cited in MMW) — an Ω(N) randomized lower bound for approximate MCSP[2^√n] gives
    RP ≠ NP, hence P ≠ NP; MMW Theorem 1.7 gives the analogue for MKTP streaming. MMW Thm 1.3 is the one analysed here, not the only one.
- **[Oli19]** Oliveira, *Randomness and intractability in Kolmogorov complexity*, ICALP 2019 (ECCC TR19-064).
  - Thm 3(ii): for every 0 < γ < 1, Gap-MrKtP[n^γ, n/2] ∉ Promise-BPTIME[n^{poly(log n)}] — unconditional, uniform, LARGE gap.
  - Thm 3(iii): if ∃ε such that for every 0 < γ < 1, Gap-MrKtP[n^γ, n^γ + C·log n] ∉ SIZE[n^{1+ε}], then Promise-BPEXP ⊄ SIZE[poly].
  - Thm 23 (body): same with "every small enough β", gap d·log n.
  - The magnification is stated non-uniformly; a uniform randomized version exists but its algorithm uses small-fan-in oracle gates
    ([CHOPRS] footnote 12), and the unconditional lower bound "does not extend to algorithms with such oracle gates". Conclusion class:
    BPEXP vs P/poly, not P vs NP.

**Consequence.** [Oli19] is the one place where a real unconditional uniform lower bound sits next to a magnification frontier; it fails
on the gap parameter and on small-fan-in oracles, and it concerns BPEXP. It is evidence of the gap, not a bridge to P vs NP.

## 2. Proposition U1 — the space bound of the MMW premise is achievable unconditionally

**Claim.** For every A ∈ PH and every time-constructible s(n) ≥ n, search-MCSP^A[s(n)] is solvable by a one-pass streaming algorithm
with poly(s) space and update time 2^{poly(s)}.

**Proof.** In MMW's streaming model the working storage between bit reads counts against the space bound. Take the algorithm of
Thm 1.2 (Õ(s) space). Each oracle query is a Σ3SAT^A instance of length q = Õ(s); Σ3SAT^A ∈ PH ⊆ PSPACE, so it is answered in poly(q)
space, reused between queries. Total space poly(s). ∎

**Corollary U1.** U1 makes the MMW premise *non-vacuous only through update time*: the premise says that every poly(s)-space streaming
algorithm needs super-poly(s) update time on infinitely many input lengths (the premise is ∃s ∃A, and "not solvable" is infinitely
often). Hence a method that bounds only space or communication and ignores per-step computation time (one-way communication complexity,
information-theoretic streaming bounds) cannot establish it. *Status:* formalizes the MMW remark; not new.

## 3. Time-sensitive uniform technique and the transfer question

Alternation trading gives SAT ∉ DTISP[n^c, n^{o(1)}] for every c < 2cos(π/7) ≈ 1.8019 (Williams, CCC 2007); Buss–Williams show that
alternation-trading proofs cannot go beyond this exponent.

**Threshold, by regime.**
- s = N^{o(1)} (e.g. s = n^c): the MMW premise is against total time N·poly(s) = N^{1+o(1)} and space N^{o(1)}. The SAT bound lies
  above this threshold in a stronger model (random access). The question is transfer.
- s = N^β, β fixed: the premise must hold against every polynomial p(s). Taking p(s) = s^{1/β} = N, it becomes a full polynomial-time
  lower bound for a PH problem — not a weak lower bound. The regime is not "magnification" in the useful sense.

**Proposition U3 (witness-compression obstruction).** Let A ∈ DTIME[2^{m^k}] (holds for every A ∈ PH, since PH ⊆ PSPACE ⊆ ∪_k
DTIME[2^{m^k}]). Suppose R is a polynomial-time many-one reduction from SAT (instance length L) to MCSP^A[s] whose outputs have length
N ≤ L^c; write σ(L) = s(log N) ≤ s(c·log L). Then SAT ∈ DTIME[2^{O(σ log σ)}·L^c·σ·2^{O(σ^k)}].

**Proof.** Enumerate all A-oracle circuits of size ≤ σ (2^{O(σ log σ)}) and evaluate each on all N inputs; each A-gate has fan-in ≤ σ
and costs 2^{O(σ^k)}. ∎

**Corollary U3.** If σ(L) ≤ L^{δ} with δ·k < 1 (in particular s = N^{o(1)}, or s = N^β with c·β·k < 1), SAT is solvable in time
2^{L^{1-Ω(1)}} in instance length L; by the sparsification lemma (Impagliazzo–Paturi–Zane) this refutes ETH. Hence, under ETH, the
alternation-trading bounds for SAT cannot be carried to the MMW regime by polynomial-time many-one reductions with polynomial blow-up.
*Status:* folklore brute force (Kabanets–Cai 2000; Murray–Williams CCC 2015); recorded for routing only.

**What U3 does not show.** It does not exclude a *direct* alternation-trading argument for the target problem itself. For A ∈ P
(e.g. A = ∅), MCSP^A[s] is in NTIME[N·poly(s)] with poly(s) witness bits; for general A ∈ PH evaluating A-gates already needs PH, so
the guess-bounded NTIME placement holds only for A ∈ P.

## 4. Next proof obligation (restated after review)

**PO-U.** Regime s = N^{o(1)}, A ∈ P. Is there ε > 0 such that search-MCSP^A[s] (or another MMW-magnifiable problem) provably has no
streaming algorithm with N^{ε} space and N^{1+ε} total time, by a time-sensitive (alternation-trading type) argument?

**Locality constraint (decisive).** MMW Thm 1.2 unconditionally gives a streaming algorithm with N·Õ(s) time, Õ(s) space and short
Σ3SAT^A oracle queries. Any lower-bound argument that remains valid for streaming machines with small-fan-in oracle access is therefore
refuted by Thm 1.2 itself. A positive answer to PO-U must use a step that breaks under such oracles. Whether the speed-up and hierarchy
steps of alternation trading survive small-fan-in oracles is NOT yet checked; if they do, the positive branch of PO-U is closed by
Thm 1.2.

**H-U (heuristic, NOT a proof).** The standard speed-up DTISP[T, S] ⊆ Σ2TIME[~√(T·S)] guesses ~√(T/S) configurations, a witness of
length ~√(T·S) ≈ N^{1/2+o(1)} for T = N^{1+ε}, S = N^{ε}. This exceeds the poly(s) = N^{o(1)} witness budget of the target, so a
hypothesis about guess-bounded problems cannot remove the new ∃ quantifier; padding to make the guess relatively small raises the time
far above T. This explains why the standard argument fails; it does not exclude a different speed-up.

## 5. Status

- U1: VALID (review). Corollary U1: VALID after fixes (non-vacuity, infinitely-often quantifier).
- U3: VALID after fixes (notation, sparsification, A ∈ P restriction). Folklore.
- Uniform route: OPEN. Next check: does alternation trading survive small-fan-in oracles (locality constraint in §4)?

## 6. Independent review (2026-11-16)

Adversarial referee subagent, checked against the MMW, Oli19 and CHOPRS texts. Verdicts: §1 VALID WITH FIXES ("only route" overclaim
removed; Oli19 uniform/non-uniform and theorem split corrected); U1 VALID, Cor. U1 VALID WITH FIXES; §3 VALID WITH FIXES (c < 2cos(π/7),
Buss–Williams; threshold only for s = N^{o(1)}; s = N^β premise is a full polynomial lower bound, so the earlier PO-U was wrongly
posed); U3 VALID WITH FIXES; added the locality constraint. All fixes applied above.
