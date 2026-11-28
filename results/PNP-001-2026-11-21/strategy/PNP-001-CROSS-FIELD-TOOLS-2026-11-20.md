# PNP-001 cross-field tools (owner brainstorm 2026-11-20) - for the DIVERGENT LANE and every enriched idea
Status: pointers, NOT verified results. Source-check every item before relying on it; mark SOURCE only after reading the paper.

## Objects that bound ALL methods of a model (the "Galois pattern": a normal form for all methods + an invariant no step moves enough)
- Galois group (radicals), field degree + transcendence (ruler/compass), arithmetisation + diagonalisation (Goedel, Turing).
- Extended formulations: no polynomial-size LP for the TSP polytope (Fiorini et al. 2012) - invariant: nonnegative rank of the slack matrix.
- General adversary bound: characterises bounded-error quantum query complexity up to constants (Reichardt 2011) - a dual SDP certificate.
- Information complexity: equals amortised communication (Braverman et al.); can be exponentially below communication (Ganor-Kol-Raz).
- Cell-probe lower bounds for dynamic data structures (Patrascu-Demaine) - free computation, counted memory access.
- GCT (Mulmuley-Sohoni): representation-theoretic obstructions; occurrence obstructions provably insufficient (Buergisser-Ikenmeyer-Panova
  2016); multiplicity obstructions open.

## Quantities "present but expensive to access"
- Pseudoentropy / HILL entropy; inaccessible entropy (Haitner-Reingold-Vadhan-Wee 2009).
- Logical depth with slow-growth law (Bennett 1988).
- Time-bounded Kolmogorov complexity: Liu-Pass - one-way functions exist iff (variants of) time-bounded Kolmogorov complexity are hard;
  ITCS 2026 boundary-MINrK equivalence (Thm 1.2) - TO BE SOURCE-CHECKED (exact quantifiers, ioBPP).
- Statistical-computational gaps, overlap gap property (Gamarnik); Harlow-Hayden decoding, "Python's lunch" (conjectural).
- Sheaf-theoretic contextuality: locally consistent data without a global section (Abramsky-Brandenburger).
- KRW conjecture: depth(f o g) ~ depth(f) + depth(g) - would separate P from NC1; precise form of "non-recyclable cost".
- Nielsen complexity geometry (gate count as geodesic length).

## Five circumvention tests - any proposed unavoidable cost of computation must survive them
1. Reversible computing (Bennett): logical operations without erasure cost.
2. Strassen: algebraic cancellation beats the "obvious" operation count.
3. Barrington: width-5 branching programs = NC1 (tiny memory, full power).
4. Catalytic space: a full borrowed memory helps although it must be restored.
5. Uhlig mass production: many copies of a function cost barely more than one.

## Barrier labels (record for every enriched idea BEFORE it enters the proof book; a label, not a filter)
relativizing? natural (constructive + large)? algebrizing? localizing (survives small fan-in oracle gates)?

## Deep research 2026-11-20 (web, abstracts/summaries read; papers themselves not yet read line by line)
- GCT: occurrence obstructions cannot separate padded permanent from determinant (Buergisser-Ikenmeyer-Panova, FOCS 2016 / JAMS 32 (2019)
  163-193, arXiv 1604.06431); multiplicity obstructions strictly stronger in a model setting (Doerfler-Ikenmeyer-Panova, ICALP 2019,
  arXiv 1901.04576); general multiplicity route open. GCT targets permanent vs determinant (algebraic, VP vs VNP type), not P vs NP directly.
- KRW: monotone/semi-monotone composition theorems via lifting (de Rezende-Meir-Nordstroem-Pitassi-Robere, FOCS 2020, arXiv 2007.02740;
  Comput. Complexity 2024); KRW-like theorem for STRONG composition (arXiv 2306.00615, FOCS 2023) - would give depth 3.04 log n if it held
  for standard composition; KW_XOR strong-composed with KW_f needs n^{3-o(1)} leaves (STACS 2025). Lifting via Karchmer-Wigderson only
  gives monotone formula bounds (Mertz survey). KRW itself would separate P from NC1 (not P from NP).
- Meta-complexity: MCSP in P => no pseudorandom functions (Razborov-Rudich / Kabanets-Cai 2000: a natural property is essentially an
  efficient algorithm for an MCSP-like problem); one-way functions exist <=> approximating distributional Kolmogorov complexity is
  NP-hard under randomized reductions AND NP is worst-case hard (Hirahara STOC 2023, ECCC TR23-037); partial MCSP NP-hard (Hirahara
  FOCS 2022); constant-factor MCSP NP-hard under deterministic quasi-polynomial reductions under stated hypotheses (Hirahara-Ilango
  FOCS 2025, per secondary source); total MCSP NP-hard only under assumptions.
- Range avoidance -> new lower-bound technique: S2E/1 has a language of circuit complexity >= 2^n/n via an FZPP^NP/1 algorithm for range
  avoidance (Chen-Hirahara-Ren STOC 2024, arXiv 2309.12912; ECCC TR23-144); advice removed: S2E not in i.o.-SIZE[2^n/n] (Zeyong Li,
  arXiv 2310.17762, ECCC TR23-156).
- SOURCE-CONFIRMED 2026-11-20 (existence + abstract): Loff-Sherif-Talebanfard-Ugazio, "The Switching Lemma shows what the Switching Lemma
  cannot prove: an unconditional natural-proofs barrier", arXiv 2606.12631 (June 2026): most constant-depth lower-bound techniques are
  AC0-natural; no AC0-natural proof gives a lower bound beyond 2^(n^(7/(d-5))) against depth-d circuits (switching-lemma frontier
  2^(n^(1/(d-1)))); the Trevisan-Xue generator's security is proved WITH the switching lemma - the method bounds itself.
- SOURCE-CONFIRMED: van den Berg-Dutta-Gesmundo-Ikenmeyer-Lysikov, "Algebraic Metacomplexity and Representation Theory", CCC 2025
  (LIPIcs 339, 26:1-26:35), arXiv 2411.03444: isotypic decomposition of metapolynomials is efficient; algebraic natural proofs may be
  assumed isotypic; metapolynomials in one irreducible representation have equal circuit complexity up to quasipolynomial blowup.
- Known and correct: P = NP => MCSP[N^beta] in P => the property CC(x) > N^beta is constructive, large and useful against P/poly;
  hence "no such natural property" => P != NP.
- NOT yet checked: Grochow-Urisman (ECCC TR26-106, graph isomorphism and representation theory); Garlik-Gryaznov-Lu-Santhanam-Tzameret
  (meta-mathematics of algebraic complexity, Oct 2026). Correction: Raz-McKenzie (1997/99) separated the monotone NC hierarchy; monotone
  KRW theorems are de Rezende-Meir-Nordstroem-Pitassi-Robere (2020/2024).
