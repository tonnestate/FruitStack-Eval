# T22 — One-way functions via meta-complexity: bounded primary-source check (PI, 2026-11-17)

STATUS: literature check only (independent agent read the theorem texts; extracts in /tmp/claude-0/owf_check/). No ledger entry.
Owner question: name the unproved statement, its known obstacles and the strongest available partial theorem.

## The exact unproved statement (Liu–Pass FOCS 2020, arXiv 2009.11514, Thm 1.1 and following remark — read in source)
There are polynomials t(n) >= (1+ε)n and p such that every uniform PPT algorithm (two-sided error) fails to compute K^t(x) on at
least a 1/p(n) fraction of uniformly random x ∈ {0,1}^n, for all large n.  [mild average-case hardness of K^t; NOT errorless]
LP20 prove: this ⇔ one-way functions exist — an equivalence between two hardness statements, neither of which is proved.
Security notion matters (owner correction 2026-11-17): OWF secure against UNIFORM PPT ⇒ NP ⊄ BPP ⇒ P ≠ NP; the stronger
NP ⊄ P/poly needs security against NON-UNIFORM polynomial-size circuits. LP20's equivalence is for uniform PPT adversaries.
Strength: implies P ≠ NP; the converse is not known (Heuristica and Pessiland are not excluded), so as far as is known the target is
STRICTLY STRONGER than P ≠ NP. The chain relocates the difficulty; it does not reduce it.

## Refinements read in source
- Liu–Pass CCC 2022 (LIPIcs CCC.2022.36): conditional McK^tP[ζ] (RAM programs): mild average-case hardness ⇔ OWF (Thm 1.1);
  NP-complete for t >= n², some ζ, under RANDOMIZED reductions only (Thm 1.2). "OWF from NP ⊄ BPP" ⇔ a worst-to-average reduction
  for this problem — which is reframed, not provided.
- Hirahara STOC 2023 (ECCC TR23-037, Thm 1.2 informal): under NP ⊄ i.o.P/poly, OWF secure against circuits ⇔ NP-hardness (parametric
  honest, randomized, nonadaptive) of (1+ε)-approximating distributional Kolmogorov complexity dK^{τ,A}.
- Liu–Pass ITCS 2026 (LIPIcs ITCS.2026.97): unconditionally OWF ⇔ boundary-MINrK^poly ∉ ioBPP (randomised K^t, Thm 1.2); for plain
  K^t (Thm 1.1) only under E ⊄ ioSIZE[2^{εn}]. Owner's correction confirmed.
- Goldberg–Hu–Lu–Lyu–Oliveira, arXiv:2610.19162: isolates a missing worst-case reduction (mild-gap to standard-gap pKT) for the
  DistPH-vs-PH question, with an oracle where it fails (relativization barrier for that step). About Heuristica, not OWF.
- Couteau–Melissaris–Sajith, arXiv:2611.04680: fine-grained, CONDITIONAL one-way functions from linear-algebra hardness. Not a
  cryptographic OWF, no bearing on P vs NP. Owner's warning confirmed.

## Known obstacles
- Every barrier for P ≠ NP applies (the target implies it).
- Natural proofs (scope corrected, owner 2026-11-17): if PRFs secure against non-uniform circuits (of size 2^{n^ε}) exist, no
  P/poly-natural property is useful against P/poly (Razborov–Rudich). This blocks only NATURAL proofs of non-uniform lower bounds;
  it is not a blanket ban on proving the existence of one-way functions (e.g. by non-natural or uniform arguments).
- Relativization: oracles realising Heuristica (Impagliazzo CCC 2011) and Pessiland (Wee TCC 2006) [search snippets, not re-read];
  Thm 1.3 of arXiv:2610.19162 [read].
- Limits on reductions proving NP-hardness of MCSP/K^t: Murray–Williams (no NP-hardness under small projections; poly-time NP-hardness
  would give EXP ≠ NP ∩ P/poly); Hirahara–Watanabe (oracle-independent reductions); Saks–Santhanam CCC 2020 [snippet].

## Strongest unconditional partial results (none reaches exact K^t on the uniform distribution with two-sided error)
- Hirahara FOCS 2022: partial MCSP, MINKT*, MKTP* NP-hard under randomized reductions (worst case, partial functions; non-relativizing).
- Hirahara FOCS 2018: non-black-box reduction from approximate MINKT (worst case) to errorless average-case MINKT.
- Huang–Ilango–Ren STOC 2023: NP-hardness of approximating the oracle version MOCSP [snippet].
- Golovnev et al. ICALP 2019: MCSP needs AC^0[p] circuits of size exp(N^{0.49/d}) (restricted model) [snippet].

## Comparison with the algebraic route (owner's question: two chains side by side)
| | Algebraic route (border dc / GCT) | Meta-complexity route |
|---|---|---|
| Final implication to P ≠ NP | none known | proved (OWF ⇒ P ≠ NP) |
| Open step | superpolynomial border dc(per_m) | mild average-case hardness of K^t |
| Strength of the open step | not known to imply P ≠ NP | at least as strong as P ≠ NP, strictly stronger as far as known |
| Specific barrier | polynomial caps on all known numerical invariants (T15–T20) | natural proofs self-reference; relativization (Heuristica/Pessiland oracles) |
DECISION (gate): NO NEW MISSION (owner); kept as the reference formulation of the classical target.
