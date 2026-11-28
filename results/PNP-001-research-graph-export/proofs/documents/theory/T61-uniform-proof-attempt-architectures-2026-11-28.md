# T61 — Connected proof attempt from uniform P = NP: architectures, closures, first unproved implication (2026-11-28)

Status: ATTEMPT. No contradiction derived; P != NP is not claimed. Labels: [U] unconditional, [H] consequence of H, [?] unproved,
[R] recalled from memory, not opened in this session, [V] verified in this session (Proofbook row).

Hypothesis H: there is a deterministic algorithm A with SAT-search in time n^kappa (kappa unknown constant). Uniform, explicit code.

## 0. What uniformity gives (and does not)
- [U] Levin search A* finds a witness on every satisfiable instance (time exponential in general); poly time on satisfiable instances iff H. Soundness of any
  returned witness is checkable per instance. Unsatisfiable instances need a clock c n^kappa, correct only for the unknown pair (kappa,c). (18325)
- [U] Global correctness of poly-time search programs is undecidable (W_M construction, 18324); this blocks certificates, not the use of H as a hypothesis.
- [H] Per length n, correctness of a given circuit/program on all inputs of length n is Pi_2 hence in P (pre-check); cost exponent kappa_2 > kappa.

## 1. Architecture A: manufacture hardness with A, then contradict a hierarchy/size theorem
Chain: [H] Sigma_2 cap Pi_2 = P; [U,R] Kannan: Sigma_2 cap Pi_2 not in SIZE(n^k); [U,R] Pippenger-Fischer: DTIME(t) in SIZE(t log t).
Result: for the Kannan language L_k, time(L_k) >= n^{k-o(1)}. Upper bound from A: the Sigma_2 search runs on an instance of size >= 2^m = truth-table size
>= n^k, so time >= n^k * (instance-reading) and exponent kappa_2 k. A contradiction needs time(L_k) < circuit complexity(L_k), i.e. producing a hard object faster
than its size. The instance written for the solver has size >= the hardness it certifies. CLOSED: with explicit instances no kappa makes it work; with succinct
instances P=NP only yields EXP (succinct SAT in NEXP = EXP under H), exponential time. [V-type reasoning; no new row]

## 2. Architecture B: pre-check + compact tableau (Meyer)
18301 [V]: poly-size circuits for the whole computation table of one EXP-complete problem would give EXP in Sigma_2 = P (contradiction), so under H such compact
tableaux do NOT exist for all inputs. The route needs the compactness it refutes. CLOSED.

## 3. Architecture C: self-certification
To certify a size-s solver at length n one solves a Sigma_2 instance of size ~s, costing s^{kappa_2} > s; the certifier is again a size-s^{kappa_2} circuit whose
certification needs the next level. No grounding; accounting inequality only (no contradiction). [H], consistent with Pich-Santhanam provability gap [R].

## 4. Architecture D: per-length adaptive selection of (kappa,c)
Selecting the best pair per length costs a pre-check of exponent kappa_2 > kappa; it cannot beat the optimum exponent (Levin optimality) and yields no gain. CLOSED.

## 5. Architecture E: algebraic (this session's toolkit)
18308-18325: all identities are semantic (truth-table ring), valid in every oracle world; admissible as links, not as a whole chain (algebrization barrier
concerns the proof, 18321). Cost content: lexicographic choice indicators O(s+m) [U]; formal certificate that some indicator is active = zero test of D, coNP-type.
No size statement about certificates under H is derived. OPEN link, no mechanism.

## 6. Architecture F: non-relativizing theorems applied to H
[R] IKW: NEXP in P/poly => NEXP = MA; under H, BPP = P so MA = P, hence NEXP in P/poly => NEXP = P, contradicting the time hierarchy. So H => NEXP not in P/poly
(non-relativizing step used). This is a consequence of H consistent with all known theorems (it is the believed state of affairs). A contradiction needs an
unconditional proof of NEXP in P/poly or of EXP in P/poly: none exists.

## 7. First unproved implication (exact)
Every architecture above ends at one of two statements, neither provable today:
(i) an unconditional theorem asserting compact (poly-size) description of an EXP/NEXP computation for all inputs [B, F]; or
(ii) a way to invoke A on an instance of size strictly smaller than the hardness being contradicted, i.e. a succinct SAT instance solved below its output size [A].
(ii) is NP vs NEXP-type: succinct SAT is NEXP-complete and H only gives EXP. (i) is the open EXP in P/poly question in the direction opposite to the believed one.

## 8. What would count as progress
[CORRECTED 2026-11-28, see T62 §7: o(T) is insufficient for an unknown solver exponent; the requirement is instance size T^{o(1)} with reduction time o(T/log T), all recomputation charged.]  A mechanism that makes the Cook-Levin instance for a simulated T-step computation of size o(T) while keeping the problem in NP (not NEXP): a "locally checkable
compression" of computations. The algebraic cancellation tools (D, E, composition law eta_12 = eta_1 + D_1 eta_2) act on a given system; none shrinks the
encoding of a simulated computation. Not available.
