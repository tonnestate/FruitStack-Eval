# T32 — Identity, recoverability and emergent information: model, trichotomy, transfer to PNP-001 (PI, 2026-11-17)

STATUS: PI derivations; classical theorems cited (Grollmann–Selman, Schäffer–Yannakakis, IKKM/Achlioptas–Molloy confirmed in abstracts /
secondary sources 2026-11-17; Bennett 1973, Hopfield 1982, MPZ 2002, MMZ 2005 to be read in source by the verification mission).
Independent verification: FruitStack mission req-pnp-iter05.json. Not in the ledger until that review.
Owner brief 2026-11-17 "Identity, Phase Transitions and Emergent Information" (PNP-HYP-EMERGENT-INFORMATION).

## 1. Model of the water-drop identity problem (WP1)
Finite model, exact. Microstate space Ω (finite), dynamics U: Ω → Ω a BIJECTION (microscopic reversibility, Bennett 1973 in the
computational form: logically reversible = injective transition function). Label ℓ: Ω → {A, B} ("drop came from region A or B"), initial
ensembles μ_A, μ_B on Ω (initial microstate uncertain, label fixed). Coarse observation π: Ω → Y (e.g. block densities, tags invisible).
Three levels, exactly defined:
- (P) physical preservation: the label is a function of the microstate at time t: since U^t is a bijection, x_0 = U^{-t}(x_t), so
  ℓ(x_0) is determined by x_t. Quantitatively d_TV(U^t_*μ_A, U^t_*μ_B) = d_TV(μ_A, μ_B) for all t (bijections preserve total variation).
- (O) observational distinguishability through π: δ_π(t) = d_TV(π_*U^t_*μ_A, π_*U^t_*μ_B) ≤ d_TV(μ_A, μ_B) (data processing).
  Bayes error of the best label guess from π(x_t) = (1 − δ_π(t))/2 (equal priors). Non-identifiability = δ_π(t) = 0.
- (C) computational recoverability: there is an algorithm of time τ that outputs ℓ from the observation it has access to.
Lemma W1 (reversible micro / irreversible macro coexist). If (Ω, U, uniform measure) is mixing in the sense
|ν(U^{-t}E ∩ F) − ν(E)ν(F)| → 0 for all E, F, and μ_A, μ_B are uniform on sets S_A, S_B of positive measure, then for every finite
coarse-graining π: δ_π(t) → 0 while d_TV(U^t_*μ_A, U^t_*μ_B) stays constant. Proof: π_*U^t_*μ_A(y) = ν(U^{-t}π^{-1}(y) ∩ S_A)/ν(S_A)
→ ν(π^{-1}(y)) for each of the finitely many y, same for B; the micro statement is bijectivity. ∎ (Finite Ω has no strict mixing; there
the statement is "δ_π(t) small for t in a range", computable exactly — this is the planned PhysalisMe model: discrete cat map on Z_p².)
Tracers (WP3): a tracer is an enlargement of π (a finer observation π' with π = h∘π'): δ_{π'}(t) ≥ δ_π(t) by data processing; a tracer
"fails" exactly when the tracer coordinates themselves become mixed (δ_{π'}(t) → 0), e.g. tracers that redistribute in phase changes.

## 2. The recoverability trichotomy and its exact computational content
Separation 1 (O without P is impossible; P without O is generic): (O) ⇒ (P) for deterministic dynamics; W1 shows (P) ∧ ¬(O).
Separation 2 (information present but computationally hidden): the observation is the full microstate x_t = g(x_0), g = U^t.
Theorem W2 (exact transfer, classical). Let g be polynomial-time computable, injective and honest (|x| ≤ poly(|g(x)|)).
 (a) If P = NP, then g^{-1} is computable in polynomial time (prefix search for x with g(x) = y, each step one NP query).
 (b) Grollmann–Selman 1988 (SIAM J. Comput. 17): honest injective polynomial-time functions that are not invertible in polynomial time
     ("worst-case one-way functions") exist IF AND ONLY IF P ≠ UP.
Consequence. "Physical information is preserved (reversible dynamics, simulable in polynomial time) but computationally unrecoverable" is
EXACTLY the statement P ≠ UP (for worst-case inversion). P ≠ UP ⇒ P ≠ NP (UP ⊆ NP); the converse is not known. So the identity route, in
its precise computational form, is a STRONGER-OR-EQUAL target than P ≠ NP, not a reduction of it. Relativization: there are oracles with
P^O = UP^O and with P^O ≠ UP^O (standard), so no relativizing argument settles it.
Separation 3 (fast-forwarding). If t is part of the input in binary, predicting/inverting U^t for a universal reversible machine is
EXP-hard by the time hierarchy (unconditional) — but outside NP: the same translation problem as T27 §4 (a hierarchy-hard language
reduces to SAT iff its class ⊆ NP).

## 3. Collective invariants and phase transitions cannot create information (WP2, WP4)
Lemma W3 (data processing for computation). For a decision problem L and any transformation Φ: if L = O∘Φ then Φ preserves L-information
(I(L(X); Φ(X)) = H(L(X)) for every input distribution). A collective invariant never contains information the input lacks; for a decision
problem the input determines the answer, so non-identifiability never occurs — the only obstacle is cost. (Owner WP1 distinction "genuine
non-identifiability vs computational intractability": for SAT only the second exists.)
Theorem W4 (direction). (i) Uniform Φ_n, O_n both poly-time with SAT_n = O_n∘Φ_n for all inputs ⇒ SAT ∈ P (P = NP direction).
(ii) "For all poly-time Φ and all poly-time O: SAT ≠ O∘Φ" is literally SAT ∉ P (take Φ = id). So any lower-bound use of collective
invariants must RESTRICT Φ or O (a restricted model); the unrestricted version restates the target.
Counterexample E1 (clustering does not imply hardness for general algorithms). Random k-XORSAT (k ≥ 3) has a sharp clustering
threshold equal to the 2-core threshold, below the satisfiability threshold, with frozen variables in each cluster (Mézard–Ricci-Tersenghi–
Zecchina 2003; proved by Ibrahimi–Kanoria–Kraning–Montanari, Ann. Appl. Probab. 25 (2015), and Achlioptas–Molloy 2015) — the same
solution-space geometry as random k-SAT (Mézard–Mora–Zecchina 2005) — yet XORSAT is decided and counted exactly by Gaussian elimination
over GF(2) in O(n³). Hence "solution-space clustering / frozen variables / overlap gap ⇒ hard for every algorithm" is FALSE; such
phenomena bound restricted classes (local, sequential-local, low-degree, stable algorithms; e.g. arXiv:2404.17775 for sequential local
algorithms on k-XORSAT). The global algebraic invariant (linearity) is precisely an emergent-information mechanism — and it yields an
ALGORITHM (upper bound), not a lower bound. Same mechanism as T31 Theorem C2 (Tseitin) and T29 Lemma R.
Random vs worst case: everything in MPZ 2002 / MMZ 2005 concerns random formulas at fixed density; no worst-case transfer is claimed here.

## 4. Attractor networks, tracers, quantum correlations — the shared mechanism (WP3)
- Hopfield 1982: asynchronous dynamics decrease E(s) = −½ sᵀWs (W symmetric, zero diagonal) and converge to a LOCAL minimum.
  Schäffer–Yannakakis 1991 (SIAM J. Comput. 20:56–87): finding a stable configuration of such a network is PLS-complete (weighted);
  unweighted P-complete. Global minimum (ground state) of Ising spin glasses is NP-hard (Barahona 1982). So attractor recall computes
  PLS objects; global properties are NP-hard — the network does not evade complexity, it lives in PLS.
- Associative recall = decoding: reconstructing a stored pattern from a corrupted one is decoding a code (patterns = codewords); the
  information-theoretic limit is mutual information (Fano), the computational question is decoding complexity; maximum-likelihood
  decoding of general linear codes is NP-hard (Berlekamp–McEliece–van Tilborg 1978).
- Quantum correlations: n qubits yield at most n classical bits (Holevo 1973); black-box search needs Ω(√N) queries (BBBV 1997);
  no-signalling forbids using entanglement alone to transmit information. NP ⊆ BQP is open; nothing here touches it.
Shared mechanism (precise): REDUNDANT ENCODING + DECODING. Recoverability = (information-theoretic) channel capacity question
(data processing, Fano), solved; cost = decoding complexity question, which in general is NP-hard or PLS-hard. The "drop" analogy splits
exactly into these two parts; only the second is about complexity, and there it reproduces known hardness, it does not prove any.

## 5. Obstruction analysis (WP5) — exact missing theorems
| candidate | what it would need | status |
|---|---|---|
| identity preserved but unrecoverable | unconditional worst-case one-way function = P ≠ UP (Thm W2b) | equivalent to an open separation ⊇ P≠NP; relativization-neutral (both oracles) |
| collective invariant lower bound | restrict Φ/O to a class 𝒞; prove SAT ≠ O∘Φ for Φ,O ∈ 𝒞; then a transfer 𝒞 ⊇ P | transfer = restatement (Thm W4 ii) |
| phase-transition hardness | worst-case statement from random-ensemble geometry | refuted as a general principle (E1: XORSAT) |
| attractor / associative computation | global optimum by local dynamics | PLS vs NP-hard ground state; no lower bound |
| fast-forwarding hardness | hierarchy hardness inside NP | translation problem T27 §4: needs X ⊆ NP for a class X ⊋ P |
Bypass routes found (WP5 list): algebraic compression / global inference (Gaussian elimination: E1, T31 C2), change of model (attractor
dynamics vs exact solver), change of representation (Φ = id in W4 ii).

## 6. Decision
PNP-HYP-EMERGENT-INFORMATION, in its exact computational form, splits into: (a) information-theoretic recoverability — fully decided by
data processing / mixing (W1, W3), contains no complexity content for decision problems; (b) computational recoverability of preserved
information — equivalent to P ≠ UP (W2), a target at least as strong as P ≠ NP; (c) collective invariants and phase transitions — give
algorithms (P direction) when they exist; as lower bounds they hold only for restricted algorithm classes and the unrestricted transfer
restates SAT ∉ P (W4); clustering-based hardness is refuted for general algorithms (E1).
No new lever for ∃L ∈ NP \ P. The route fails for an exactly identified reason: emergent information is a property of a REPRESENTATION;
lower bounds must quantify over all representations, and at that point the invariant is the decision problem itself.
Retained, verifiable small results: W1 (finite exact model to be computed), W2 (classical, cited), W4 (elementary), E1 (classical, cited).
