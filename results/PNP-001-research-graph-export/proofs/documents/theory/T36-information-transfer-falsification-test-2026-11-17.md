# T36 — Information-Transfer Falsification Test (PI, 2026-11-17)

STATUS: owner's narrowed obligation (2026-11-17, after the Grok report): define an information measure that is (i) non-trivial for
deterministic computations, (ii) controlled under admissible changes of memory organisation, (iii) an unavoidable resource rather than
the cost of one simulation — or exclude the proposed definitions by counterexample. PI proofs below; verification by FruitStack
iteration 7 (request narrowed to this test). Not in the ledger.
Facts checked in source (arXiv:2611.11832 pp. 2–3): one-tape chain NTIME₁[t] ⊆ NSPACE₁[O(√t)] ⊆ DTIME[2^{O(√t)}] ⊆ DTIME₁[2^{O(√t)}]
(first step Hopcroft–Ullman, needs t ≥ n²); "our proof, by necessity, does not relativize" (Lipton's conjecture fails relative to some
oracle and relative to a random oracle). Lemma 2.1: the 2^{O(t/b)} patterns enumerate only BLOCK MOVES of the heads; tape contents are
variables, not enumerated (owner's precision adopted; T35 §2 step 2–3 says the same).

## Setting
M deterministic multitape, inputs {0,1}^n, a partition 𝓑 of the space–time history fixed by (M, n) (e.g. HPV blocks × epochs; input-tape
boundaries), boundary set E (|E| = K), transcript τ_e(M, x) = everything crossing boundary e on input x.

## The candidate definitions and their fate
μ1 (realised patterns, Grok): log2 |{π(M,x)}| for fixed x. For deterministic M exactly one history ⇒ μ1 = 0. FAILS (i). (owner)
μ2 (variety over inputs): V_e(M,n) = log2 |{τ_e(M,x) : x ∈ {0,1}^n}|.
  Lemma E1. V_e ≤ n for every e, hence Σ_e V_e ≤ K·n. Proof: the map x ↦ τ_e(M,x) has a domain of size 2^n. ∎
  Consequence: a lower bound Σ_e V_e ≥ g(n) gives at most K ≥ g(n)/n boundaries, i.e. T ≥ g(n)/n only if boundaries are time-indexed —
  and a lower bound on V at a TIME boundary is not forced by L: the future of the computation needs at most x (n bits) and at least the
  answer bit; anything in between depends on the machine's progress, not on L. Forced variety exists only at INPUT cuts, where
  V_e ≥ log2 (largest fooling set of L at the cut A|B) (distinct inputs of a fooling set need distinct crossing transcripts, Hennie/
  Yao), and that fooling-set bound is itself ≤ min(|A|,|B|) + 1 — the communication cap (T31 C1). FAILS (iii) beyond O(K n).
μ3 (transcript length): Σ_e |τ_e| = Θ(T) for block-respecting machines (T35 U1, B1). Satisfies (i), (ii) up to HPV/PF factors, but
  is TIME ITSELF: a lower bound on min_M μ3 is a time lower bound. FAILS (iii) as an independent resource.
μ4 (communication at input cuts): Σ_i D(L; [1..i],[i+1..n]) ≤ n²/4 + n for every L; palindromes ∈ P attain it. FAILS (iii) for
  superpolynomial bounds; it is non-trivial only up to n².

Theorem F (falsification, PI). No measure of the forms μ1–μ4, and no measure bounded by a function of the variety maps {x ↦ τ_e(M,x)}
over polynomially many boundaries, yields a lower bound above O(K·n); measures that are not so bounded and satisfy (i)–(ii) are
length-type and equal time up to the normal-form overhead (B1). Proof: E1, C1, B1. ∎
**Scope correction 2026-11-28:** what is proved is the exclusion of the four concrete measures μ1–μ4 in their stated form (V_e ≤ n, E1). "Bounded by a function of the variety maps" must mean a function that is itself O(poly)·V_e-type; a function such as 2^{V_e} is not bounded by K·n (V_e ≤ n gives only 2^{V_e} ≤ 2^n), and whether such a measure yields an algorithmic bound is a separate unproved question. The classification of ALL other measures as length-type/time-equal is NOT proved by E1, C1, B1; no general exclusion of information-based methods follows.

## The owner's reformulated obligation (a lower-bound theorem whose premises capture every poly-time SAT algorithm)
Lemma N (normal forms are free and therefore neutral). For each normal form 𝒩 ∈ {b-block-respecting (HPV 1977), oblivious (Pippenger–
Fischer 1979), reversible (Bennett 1989)} every machine M has an 𝒩-machine M_𝒩 for the same language with T_{M_𝒩} ≤ poly(T_M).
Hence SAT ∉ P ⇔ no 𝒩-machine decides SAT in polynomial time. A premise "M is in normal form 𝒩" captures all polynomial-time algorithms
at no cost — and therefore cannot make the lower bound easier. For 𝒩 = oblivious, an O(T log T)-step oblivious machine IS a uniform
circuit family of size O(T log T) (PF), so the normalised obligation is exactly: SAT has no P-uniform polynomial-size circuits — the
known equivalent form of P ≠ NP. ∎ (classical facts assembled; the equivalence P ≠ NP ⇔ SAT ∉ P-uniform-SIZE(poly) is standard.)
So every information-transfer route, once normalised, lands on uniform circuit lower bounds for SAT; the measure then carries no
information beyond circuit size (μ3 ≈ size).

## Where the non-relativizing ingredient sits (owner's point 4)
In 2611.11832 the reduction (HPV + generalized Cook–Levin) is local and explicit; the algorithm (Lemma 1.3, i.e. the OpenAI/Anthropic
counting engines) is WHITE-BOX: it reads the constraint circuits. Relative to an oracle the epoch constraints would contain oracle gates
that the engine cannot inspect, so the composition fails — the same mechanism as Williams' algorithmic method (Cook–Levin local
checkability + white-box SAT algorithm). This identifies the non-relativizing technique available today: algorithms on explicit
local encodings. Its lower-bound use is Williams' method, which yields NEXP / E^NP circuit lower bounds (T23, T34 J5), not P ≠ NP.
(Algebrization status of 2611.11832: not examined; no claim.)

## Decision
PNP-TRANSFER-001 as proposed (Grok) is NOT accepted: μ1 trivial, μ2 capped (E1 + C1), μ3 = time (B1), μ4 capped (C1). Classified as an
open hypothesis with a definitional defect, now excluded in the forms μ1–μ4 by Theorem F. The remaining exact obligation is the
normalised one (Lemma N): uniform circuit lower bounds for SAT. No new large mission; one narrow verification (iteration 7).

## Addendum — owner's worked instance (2026-11-17), checked by the PI
Instance W_m = (1,2,…,2^{m−1}, 1,2,…,2^{m−1}), T_m = 2^m − 1. Claim: Σ 2^i (x_i + y_i) = 2^m − 1 ⇔ y_i = 1 − x_i ∀i.
Proof (owner): parity forces x_0 + y_0 = 1; subtract, halve, induct. CHECKED, correct. Myhill–Nerode (owner's Satz 1, classical):
after x the continuation sets L_m(x) = {x̄} are pairwise distinct ⇒ 2^m classes at the cut x | y.
PI computation (scratchpad knap.py, exhaustive, m = 1..6): order x…x y…y: 2^m classes at cut m; paired order x_i y_i: ≤ 3 classes at
every level (2 live + 1 dead). Solution count 2^m, all with y = x̄. Agrees with the owner's enumeration.
Placement: a concrete instance of μ2/E1 and T31 C1 — 2^m classes = m bits of information at the cut, ≤ input length; a TM stores them
in m cells; the class count depends on the variable order (Bryant OBDD ordering phenomenon) and on what is to be preserved. Same lesson
as the equality example in T30. It refutes the general principle "exponentially many distinguishable future states ⇒ exponential time";
that principle is not a ledger claim of PNP-001, but T36 now carries this explicit counterexample for it.
Next obligation (owner): lower bounds for knapsack/subset-sum against a PRECISELY defined class of representations. For the class of
all polynomial-time algorithms this is P ≠ NP (subset sum is NP-complete); meaningful intermediate classes are OBDDs under every order,
read-once/k-times branching programs — known lower-bound territory (restricted models), with no transfer to general algorithms.

## Addendum 2 — owner's review of the Grok / Gemini reports (2026-11-17), checked by the PI
- Grok C(S) = min_π max_i |reachable partial sums after i| on W_m: the last stage reaches every integer 0..2^{m+1}−2 for every order,
  and every stage is a subset of that range ⇒ C(S) = 2^{m+1} − 1 exactly. Claimed Θ(2^{m/2}) REFUTED. (checked)
- Gemini "universal information collapse": (N_0,+) ↪ (Z,+) is an epimorphism of commutative monoids without being surjective, and a
  monoid homomorphism is determined by its kernel CONGRUENCE, not by the preimage of the identity ⇒ the quotient argument is invalid.
  Proof REJECTED. (checked; standard facts)
- Grok block-Nerode N_b ≤ N ≤ N_b 2^{O(b)}: under the natural reading (only complete b-blocks) L_m = {uu1 : |u| = 2m}, b = 2: block
  language empty (odd lengths) ⇒ N_b = 1, while the 2^{2m} prefixes u are pairwise Nerode-inequivalent ⇒ N ≥ 2^{2m}. REFUTED for that
  formalisation; any other formalisation must be stated and proved. (checked)
- Optimality of pattern enumeration (2611.11832 gives an upper bound only), reversible < irreversible (reversible algorithms are
  deterministic algorithms, so min over all ≤ min over reversible), rank ≤ #columns (vacuous), generating function Π(1+z^{w_i}) (classical;
  difficulty is coefficient extraction): all owner objections CORRECT.
- Parity sharing (owner): B uniform, X uniform on {x : ⊕x = B} ⇒ I(B; X_S) = 0 for every proper S, H(B | X) = 0; permutation invariant.
  CORRECT and classical (n-out-of-n XOR secret sharing). It is the exact finite form of T32 W1 (preserved but locally invisible). PI
  remark: parity is also the standard example where local invisibility DOES give restricted-model lower bounds (AC^0: Håstad 1986;
  low-degree correlation) while parity is linear-time on a TM — again restricted vs general (T31, T32 W4).

## Lemma S-cap (PI) — the proposed measure B(F) is bounded by the number of solutions
B(F) = min_π max_i |{L_{π,i}(p) : p a prefix of length i}| (L = set of successful continuations; the empty set counts once).
Lemma. For every instance F (CNF, subset sum, any Boolean f) and every order π and level i: the number of distinct NONEMPTY continuation
sets is ≤ |Sol(F)|; hence B(F) ≤ |Sol(F)| + 1.
Proof. Each nonempty L_{π,i}(p) contains a suffix y with p·y ∈ Sol(F); different prefixes p give disjoint sets {p·y}, so the number of
prefixes with a nonempty continuation set is ≤ |Sol(F)|, and distinct sets need distinct prefixes. ∎
Consequence. B ≤ 2 on every uniquely satisfiable instance. Unique-SAT carries the full difficulty of SAT under randomized reductions
(Valiant–Vazirani 1986). So B cannot be a hardness measure for the DECISION problem: it measures the size of a representation of the
solution SET (small when the set is small), not the cost of finding or deciding it — the OBDD of a unique-solution instance is a single
path, i.e. the solution itself. Lower bounds on B can only come from instances with many solutions and say nothing about deciding them.
The meaningful object for P vs NP is the function of the INSTANCE (W, T) ↦ [∃ solution]; OBDD/branching-program lower bounds for that
function are restricted-model results (no transfer: T36 Lemma N).
