# PNP-001 Lemma M - systematic computational attack (owner 2026-11-21: "systematisch per Brute Force"; run IN PHYSALISME)
Exploration level: finite data can REFUTE naive versions and MEASURE trends; it never proves Lemma M (asymptotic, all c,d).
All runs via the lab (physalis_code_run / physalis_dataset_from_code / desk_submit code_run, sandbox has pysat) so each result
has a lab experiment id. Lemma M: proof state Q-156fa9c912 G0015; candidate analysis theory/oracle-elimination/QE-STAR-CANDIDATE-FIRST-FALSE-LINE.md.

## Objects
- Family F subset {0,1}^N (N = 2^n): SC_{n,s} = truth tables of n-input B2 circuits (16 binary ops, inputs = variables) with <= s gates,
  bit t = f(t). Director size check (reproduce in the lab first): n=3: |SC_s| = 3, 38, 152, 232, 256 for s = 0..4;
  live-prefix counts |P_t| n=3,s=2: 1,2,4,8,16,32,60,108,152; n=4,s=2: |SC| = 526, max |P_t| = 526.
- Controls of the SAME sizes |P_t|: (a) AFFINE family (all affine functions of the right size / a linear code) - cheap updates expected;
  (b) uniformly random family with the same |F| - expensive expected by counting; (c) small decision trees / read-once formulas.
- Separating streaming system with S state bits: codes c_t(p) in {0,1}^S for live prefixes p in P_t (injective) and dead codes
  disjoint from live ones; transitions F_t(c_t(p), b) = c_{t+1}(pb) on every reachable (code, b); unreachable inputs are don't-care.
  Cost: G_max = max_t CC(F_t) (B2 gates, multi-output, shared gates counted once). S = ceil(log2(max_t |P_t| + 1)) first, then S+1, S+2
  (redundancy allowed: several dead codes, free don't-cares).

## Measurements (exact where feasible)
1. Exact minimum G_max over ALL encodings: joint SAT (code bits per class per t as variables + exact-synthesis circuit per step,
   Kojevnikov-Kulikov-Yaroslavtsev encoding) for increasing G; report UNSAT certificates for G-1. Start with n=3, s=1,2 (N=8).
2. Same for controls (a)-(c) with identical |P_t| profiles.
3. Upper bounds by local search over encodings (annealing) where exact SAT times out - labelled UPPER BOUND only.
4. Growth: n=3 -> n=4 (N=16) for s=1,2 where feasible.

## What a result means
- SC behaves like AFFINE (small G_max): evidence AGAINST naive "separation forces work" - a refutation of the naive toy version.
- SC behaves like RANDOM (G_max near counting bound) while AFFINE stays small: evidence (not proof) for an M-type mechanism; then
  extract the structure of optimal encodings and try to PROVE a toy theorem.
- Every claim: exact statement, lab id, status OBSERVED (finite) - never PROVED for an asymptotic statement.

## SUPERSEDING OWNER CONTRACT 2026-11-21: "BRUTE-FORCE LEMMA M" (authoritative text: owner message; working copy of the binding points)
Start state: theory/oracle-elimination/QE-STAR-CANDIDATE-FIRST-FALSE-LINE.md; S0011, G0015 (Q-156fa9c912). Do NOT retry C5.
Classes C_{n,s}: constants+literals; depth-2 decision trees; read-once formulas; general B2 DAG circuits with few gates (unrestricted
fan-out). Deterministic truth-table order. Transducer q_{t+1} = F_t(q_t, x_{t+1}), q_t in {0,1}^S, final decoder D outputs a valid
witness circuit (in a fixed encoding) or a correct rejection; correctness checked on EVERY one of the 2^N inputs (valid and invalid).
No canonical encoding imposed: redundant states, arbitrary recoding, time-dependent F_t.
Synthesis: basis AND, XOR, NOT, constants; count every non-constant gate; shared gates/fan-out free. Complete bounded synthesis
(SAT/SMT; CEGIS allowed for discovery, every impossibility by a complete bounded check with checkable UNSAT certificate, e.g. DRAT).
Pareto frontier (S, G, D); timeouts are never UNSAT; report explored bounds.
Reproduce first (constants+literals): n=2: 16 streams, min state 3 bits, simple nonlinear mask 6 bits; n=3: 256, 4, 8; n=4: 65536, 4, 10.
Verify the depth-2 decision tree claim for n=3: 62 distinct functions, min state 6 bits.
Then: state-width vs gate-count trade-off; does redundancy lower G; recurrent computation within an update is counted as gates.
For every proposed invariant: smallest machine that could violate it, exhaustive search, minimise any counterexample, record the failed
implication. Oracle stress test for every lemma (exact inference that fails with small-input oracle gates; fan-out != oracle power).
Then the smallest provable structural lemma for an infinite family (restricted class kept in the conclusion).
Artifacts: instances, circuits, counterexamples, CNFs, models or UNSAT certificates, verification logs, limits.
Report ends with A smallest synthesized nonlinear exact streaming algorithm, B strongest certified finite lower bound, C smallest
counterexample to a proposed general lemma, D most promising surviving invariant, E exact unresolved asymptotic implication,
F independent verification verdict. Brute-force the mechanism, not P != NP.

## Owner addendum 2026-11-21 (binding for the evaluation)
1. Full SEARCH semantics: all distinct live prefixes at the same t must have distinct states (plus >= 1 dead code), so
   S_t >= ceil(log2(L_t + 1)). Live/dead separation alone is the weaker DECISION task - report it only as a separate, labelled variant.
2. Triviality: if S >= t at every t (in particular S >= N) the transducer can store the raw table with ZERO update gates (wire the new
   bit to a free state line) and all work sits in the decoder. Required minima: SC_{3,1}: 38 fns -> 6 bits < N=8 (meaningful);
   SC_{3,2}: 152 -> 8 bits = N (TRIVIAL at S = 8); SC_{4,1}: 70 -> 7 bits < 16; SC_{4,2}: 526 -> 10 bits < 16 (meaningful).
   Report results only on a fixed (S, D) frame with S < N, as the Pareto set of (S, G_max, D); a G_max minimum without fixed S and D
   is not evidence about Lemma M. Ask explicitly: is cheap G_max achieved only by moving the work into D?
3. Progress criterion: an independently PROVED optimal time-space trade-off (S, G_max, D) for one small class would count; finite
   results otherwise stay OBSERVED.

## Owner precision + order 2026-11-21
- Bound: S_t >= ceil(log2(L_t + [L_t < 2^t])) (the +1 only when a dead prefix exists at t). End values for SC_{3,1}, SC_{3,2}, SC_{4,2} unchanged.
- Order: (1) PhysalisMe Pareto sets (S, G_max, D); (2) separate critic checks correctness and certificate completeness; (3) only then
  escalating graphs (EGC-001, Q-55c26ae71b) against the optimal transducers at IDENTICAL budgets, comparing incremental cascades with
  full recomputation and keeping apart: static hardware (configuration size), dynamic work, worst-case update time, decoder cost.
  Question for (3): does a cascade reach a better (time, space) point with ALL internal activations counted?
