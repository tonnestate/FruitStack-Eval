# T31 — Information transfer as a lower-bound invariant: formalisation, cap theorem, counterexample to the tensor transfer (PI, 2026-11-17)

STATUS: PI derivations (elementary + classical theorems cited). Independent verification: to be done through FruitStack mission
(req-pnp-iter04.json). Not in the ledger until that review. Owner mission brief 2026-11-17 ("Information Geometry, Time and Computational
Lower Bounds"). Binding target unchanged: ∃ L ∈ NP with L ∉ P, here ∀M deciding L ∀k ∃^∞ n: T_M(n) > n^k.

## 0. Formalisation of the candidate invariant
Machine model fixed for this note: deterministic TM, input on tape 1, alphabet Γ, state set Q. Partition the input positions [n] into
A = {1..i}, B = {i+1..n} (a "boundary" between cells i and i+1 of the input tape).
- Crossing sequence CS_M(x, i): the sequence of states in which the input head crosses the boundary i|i+1 on input x.
- Transfer measure of a function f at partition (A,B): D(f; A,B) = deterministic two-party communication complexity of f with Alice
  holding x_A and Bob holding x_B. Variants: N^1 (nondeterministic), N^0 (co-nondeterministic), log rank.
- Candidate invariant (owner's question in exact form): Inf_L(n) = Σ_{i=1}^{n-1} D(L_n; [1..i], [i+1..n]) — "total information that must
  cross the boundaries of the input".
- Tensor form: for a CNF F, its tensor network N_F (copy tensors + clause tensors); cw(N_F) = minimum over contraction orders of the largest
  intermediate tensor (log2 of its size); by Markov–Shi 2008, cw is Θ(treewidth of the line graph), and the rank of T_F across a cut is
  2^{D-like} — precisely rank(M_F^{A,B}) where M_F^{A,B} is the 2^|A| × 2^|B| satisfying-assignment matrix (T1, T10).

## 1. Transfer lemma that DOES hold (single-tape TMs): crossing sequences → communication
Lemma 1 (Hennie 1965; communication form as in Kushilevitz–Nisan Ch. 12; reconstructed). If a 1-tape TM M decides L_n, then for every
input boundary i:  max_x |CS_M(x,i)| ≥ (D(L_n; [1..i],[i+1..n]) − 1) / ⌈log2 |Q|⌉.
Proof. Alice simulates M while the head is in cells ≤ i, Bob while it is in cells > i. The tape left of the boundary depends only on x_A
and the states received at crossings, likewise on the right. At each crossing the simulating party sends the current state
(⌈log2|Q|⌉ bits); the party holding the head at halt sends the answer bit. Communication ≤ max_x|CS|·⌈log2|Q|⌉ + 1. ∎
Use for lower bounds: T_M(x) ≥ Σ_i |CS_M(x,i)| for each single x; Hennie's Ω(n²) for palindromes needs one input whose crossing sequences
are long at many i simultaneously (fooling-set/averaging argument). For the CAP below only the upper direction matters.

## 2. Cap Theorem (exact obstruction #1): the transfer invariant is at most quadratic for EVERY language
Theorem C1. For every language L and every n: Inf_L(n) ≤ Σ_{i=1}^{n-1} (min(i, n−i) + 1) ≤ n²/4 + n.
Proof. D(f; A,B) ≤ min(|A|,|B|) + 1 for every f: the party with the shorter part sends it, the other answers. ∎
Consequence. Every lower bound of the form T_M(n) ≥ c · Inf_L(n) (or any cut-sum of communication, rank, fooling-set or
information-complexity measures, each ≤ min(|A|,|B|)+1) is at most O(n²). It cannot give T_M(n) > n^3 for any language, in particular
not the binding superpolynomial statement. And it cannot distinguish SAT from P: PAL ∈ DTIME_1tape(n²) already ATTAINS the cap up to a
constant (Hennie). So whatever the measure gives for SAT, a language in P gets the same.
Generalisation (C1'). Same cap for any polynomial family of cuts/partitions of the input (not only contiguous boundaries): K cuts give
≤ K·(n+1). Information about the input that must "cross" anything is bounded by the input length n per crossing structure.
Model dependence (C1''). For 2-tape TMs, RAMs and circuits Lemma 1 has no analogue at all: PAL ∈ DTIME_2tape(O(n)) (copy the input to
tape 2, compare backwards). So the crossing-sequence → communication transfer is not even invariant between polynomially equivalent
models; only the (≤ quadratic) cap survives the 1-tape ↔ multitape simulation (T_1tape ≤ O(T_multi²)).

## 3. Why transport cannot give superpolynomial bounds: the input-information cap
Principle (exact form). A "transport" lower bound charges each step for moving information across a boundary. Under UNBOUNDED space a
deterministic machine can carry the whole input across any boundary once (O(n) crossings for O(n) bits on 1-tape, O(n) on multitape) and
never needs to re-transport input information. Hence any measure that counts input information that must cross is bounded by poly(n)·
(number of boundaries) — Theorem C1/C1'. A superpolynomial bound must charge for something that is NOT input information: intermediate
values that are recomputed or re-transported. That is exactly what circuit size / time counts, i.e. the transfer collapses into the
original problem.
Re-transfer (where transport DOES give bounds): if space is bounded by s, information cannot be stored and must cross repeatedly. This is
the time–space trade-off regime: Borodin–Cook (sorting, branching programs, TS = Ω(n²/log n)), Beame–Saks–Sun–Vee / Ajtai (TS-type bounds for
element distinctness / quadratic forms with space n^{1−ε}: time ≥ n·(log n/loglog n)^{1/2}-type, superlinear but tiny), and for SAT
SAT ∉ DTISP(n^c, n^{o(1)}) for c < 2cos(π/7) with the Buss–Williams ceiling for alternation trading (T27 §3). These bounds need the space
restriction; they say nothing about P.
Obligation R (the precise missing transfer, stated so it can be refuted): "there is an explicit L ∈ NP such that every deterministic
machine deciding L in time t needs Σ_i |CS(i)| ≥ t^{Ω(1)}·... superpolynomial re-transfer of NON-input information" — this is a restatement
of a time lower bound, not a reduction of it. No transport-specific lever remains. Status: OBSTRUCTION IDENTIFIED (not a theorem to prove).

## 4. Tensor contraction width does not transfer to general computation — explicit counterexample (exact obstruction #2)
Theorem C2. There is an explicit family of CNFs F_n (n variables, O(n) clauses of width ≤ 3 after splitting, or width 3 directly) such that
(a) every contraction order of the tensor network N_F has contraction width Ω(n) (so contraction costs 2^{Ω(n)}), and
(b) #F_n (hence SAT) is computable in O(n³) deterministic time.
Construction. Take an explicit 3-regular expander family G_n (e.g. Margulis / LPS; or any family with edge expansion h > 0 and degree 3).
Variables = edges of G_n; for each vertex v a parity constraint x_{e1} ⊕ x_{e2} ⊕ x_{e3} = c_v, written as 4 clauses of width 3 (Tseitin
formula). (a) The tensor network of F_n contains, for each vertex, the 4 clause tensors over its 3 edge variables; contracting each vertex's
group gives the parity tensor; the network's graph contains G_n as a minor, so tw ≥ tw(G_n) = Ω(n) for expanders (Grohe–Marx: tw of
expanders is linear), and contraction width ≥ tw of the line graph − 1 ≥ Ω(n) (Markov–Shi Prop. relating contraction complexity to tw of
the line graph, which is ≥ (tw(G)+1)/2 − 1). (b) #F_n = number of solutions of a linear system over GF(2): 0 if inconsistent, else
2^{|E| − rank} — Gaussian elimination, O(n³).
Consequence. "High contraction width ⇒ hard" is FALSE even for exact counting. A width lower bound is a lower bound for the restricted model
"contraction of this network", not for deterministic computation. This also shows the obstruction is representation dependence: a change of
basis (Hadamard on every leg turns parity tensors into delta-type tensors on the dual) or algebraic elimination removes it.
(Tseitin formulas are exactly the instances on which resolution needs exponential size (Urquhart 1987) — a third restricted model beaten
by Gaussian elimination. Same lesson as T29 Lemma R.)

## 5. Comparison of the three measures (required output)
| measure | upper cap for every L | lower bound transfers to | invariant under poly-equivalent models? | separates SAT from P? |
|---|---|---|---|---|
| crossing sequences (1-tape) | O(n²) (Thm C1) | 1-tape TMs only (Lemma 1) | no (PAL: n² vs n) | no (PAL ∈ P attains the cap) |
| communication across cuts (any fixed poly family) | O(K·n) | any model with a cut simulation (1-tape TMs, VLSI AT², read-once BPs) | no | no (EQ/PAL ∈ P attain it) |
| tensor contraction width | n (+ log of clause arity) | contraction algorithms of THIS network | no (basis change, elimination) | no (Thm C2: XOR-SAT/Tseitin) |
All three are measures of the INPUT's correlation structure across a partition, bounded by the input length; P vs NP needs a measure of
the COMPUTATION, unbounded by n.

## 6. Time, dimensions, reversibility, relativistic models
- d-dimensional tapes: simulated by 1-tape TMs with polynomial overhead (T_1 ≤ O(T_d^{O(1)})); a superpolynomial bound in one model is one
  in the other; nothing gained or lost at the polynomial level. Their crossing bounds are WEAKER (boundaries of a d-dim region of volume t
  have size t^{(d−1)/d}).
- Reversible computation: Bennett 1989: any time-t space-s computation reversible in time O(t^{1+ε}), space O(s log t) — polynomial
  equivalence; reversibility adds no lower-bound lever for P.
- Time reparametrisation: a monotone reparametrisation of physical time changes no step count; T_M(n) is a count of transitions, not a
  physical duration. Any physical speed-of-light argument gives T ≥ diameter ≈ (memory)^{1/3} — polynomial, capped by C1-type reasoning.
- Relativistic hypercomputation (Malament–Hogarth spacetimes; Hogarth 1994, Etesi–Németi 2002) decides Σ_1 / halting: NOT a polynomially
  equivalent classical model; anything proved in it says nothing about T_M(n) for TMs. Excluded as evidence (owner rule: only theorems
  about the defined model count).

## 7. Barriers checked
- Relativization: Lemma 1 / C1 are statements about one specific tape geometry; they do not relativize in an interesting way (oracle
  tapes add a boundary-free channel). The cap C1 is unconditional and model-internal — it is not a barrier argument, it is a ceiling.
- Natural proofs: Inf_L is computable from the truth table in time poly(2^n) (communication matrices; rank) and large (random f has
  D ≈ min(|A|,|B|) at all cuts) — the measure is natural; but C1 already kills it before Razborov–Rudich matters.
- Algebrization: not applicable (no arithmetisation involved).
- Restricted models: all three measures are restricted-model bounds (Section 5). T1/T10 earlier reached the same verdict for rank across cuts.

## 8. Decision
The information-transfer hypothesis, in every form formalised here, is CAPPED at O(n²)·(number of cuts) by the input-information bound
(Theorem C1) and its tensor version is REFUTED as a lower bound for general computation (Theorem C2). The only regime where transport
forces re-transfer is bounded space (known time–space trade-offs, Buss–Williams ceiling). The missing transfer theorem would have to bound
re-transport of non-input information for unbounded-space machines — equivalent to a time lower bound itself (Obligation R): no lever.
Next justified direction (evidence-based): the transfer must count COMPUTATION, not input transport. The only known unconditional lever of
that kind is the bounded-space/alternation-trading line (T27 Lemma S as the precise open statement). Candidate next question: can a
crossing-sequence argument be combined with the PPST log* speed-up for multitape TMs (DTIME(t) ⊆ Σ_4 TIME(t/log* t)) to get any polynomial
fixed-alternation speed-up? — known to be open; to be checked against Buss–Williams-type limitation results before any work.

## Verification plan (FruitStack)
Mission req-pnp-iter04.json: CherryMe critics attack C1, C1'', C2 (in particular the Markov–Shi / treewidth chain in C2(a) and the
claim that PAL attains the cap); PhysalisMe computes for C2 exact #F by Gaussian elimination AND by tensor contraction / brute force on
small Tseitin instances (n ≤ 20 edges) — sanity only, the asymptotic statement rests on the cited theorems; literature location for
whether C1 is stated as such (folklore; Kushilevitz–Nisan Ch. 12 for 1-tape TM via communication).
