# T29 — Energy-minimising dynamics (p-bits, Ising chips, annealing): proved bounds and a falsified universal claim (2026-11-17)

STATUS: elementary proofs + exact small-n computations (scratchpad: .../scratchpad/anneal/check.py, schedule.py). No independent
review yet; not in the ledger. Scope: statements about a MECHANISM class, not about P vs NP.

## Model (Pervaiz et al., Sci. Rep. 7 (2017), Eq. 1-2, read in source)
p-bit update m_i <- sgn(rand(-1,1) + tanh(I_i)), I_i = I0 (h_i + Σ_j J_ij m_j): Gibbs sampling of exp(-I0·E), E = -Σ h m - ½ Σ J m m.
Invertible logic = clamping outputs = conditioning; SAT via E_F(x) = #violated clauses (F satisfiable ⇔ min E_F = 0).
Operation performed: FIND with a checkable certificate; never certifies UNSAT.
Lemma P: poly-size dynamics with poly-precision couplings are classically simulable per step; reaching E = 0 with probability
>= 1/poly in poly time on all satisfiable 3-CNF would give NP ⊆ RP. (Quantum annealers: not classically simulable in general;
the analogue would be NP ⊆ BQP.)

## Result 1 (PI, proved): fixed temperature, start in the decoy basin
F_n (n even): clauses (¬x_i ∨ x_j), i ≠ j, plus (x_1). E = k(n-k) for 0<k<n, E(0^n) = 1, E(1^n) = 0 (unique solution).
Single-flip Metropolis at fixed β, start π_S, S = {|x| < n/2}, L = {|x| = n/2}:
  P(hit 1^n within t steps) <= (t+1) π(L)/π(S) <= (t+1) 2^n e^{-β(n²/4 - 1)}.
Proof: π_S <= π/π(S); ν <= Cπ is preserved by any nonnegative kernel with πP = π; every path S -> 1^n meets L; union bound.
Exact check n = 8, 10, β ∈ {0.5, 1}: bound holds (n=10, β=1: exact 2.8e-7 <= 2.0e-6). Uniform start instead: success ≈ 0.5.
F_n is 2-SAT (linear time): a mechanism statement, not a hardness statement.

## Result 2 (owner, proved; verified by PI): a universal annealing-exclusion claim is FALSE
Claim refuted (forwarded text): "every admissible cooling schedule fails with exponentially small probability" on landscape H_n
(n = 2m+1, H_n = 2n(n - w) right of the barrier, start uniform on L = {w <= m-1}).
Schedule β_1 = β_2 = 0, β_t = n (3 <= t <= n²+2): P(success) >= C(n,m-1)/|L| · (m+2)(m+1)/n² · (1 - n² e^{-2n²} - n e^{-n})
= Ω(n^{-1/2}). Reproduced exactly: n = 101 gives lower bound 0.0468 in 10 203 steps.
Also correct (owner): that text's CNF (all unit clauses (x_i) plus (¬x_1 ∨ … ∨ ¬x_n)) is unsatisfiable, so it cannot encode a
landscape with a zero-energy solution at 1^n.

## Result 3 (PI, retraction): my "open" extension of Result 1 to cooling schedules is FALSE
Exact on F_10 (start π_S at β=1, then 300 cold steps at β=1): 0 hot steps (β=0) -> success ≈ 0.000; 10 -> 0.407; 30 -> 0.522;
60 -> 0.535. Hot-then-cold behaves like random restart + descent: success ≈ volume of the solution's basin under cold descent.
Remaining narrower open question: does Result 1 survive schedules never hotter than the start temperature (β_j >= β_0 for all j)?

## Falsification rule (owner, adopted)
A universal claim is refuted by one valid counterexample; the counterexample refutes exactly the claim whose quantifiers it meets.
Failure of one algorithm does not refute P = NP; a fast single case does not prove it — "no poly-time algorithm decides SAT" is
refuted only by an algorithm with a general correctness and running-time proof.

## Physical SAT encodings and the robust threshold detector (owner + PI, 2026-11-17)
- Owner (verified): Π_r = Π_{j∈C_r} (I + s_rj Z_j)/2 projects onto the clause-violating assignments; H_F|x> = λ·#violated(x)|x>;
  <+|^{⊗n} Π_0 |+>^{⊗n} = #F/2^n is the probability of one specific measurement — NOT derived for scattering/ringdown; a classical
  field superposition of n modes is not the n-qubit tensor product; Kerr-matter initial data with back-reaction not constructed.
- Owner (verified): ż = κz amplifies 2^{-n} to O(1) in time n ln2/κ, but distinguishability still needs 2ε < 2^{-n}; Choptuik
  scaling with p - p* = 2^{-n} gives M_BH ~ C 2^{-γn} (smaller, not macroscopic).
- PI: the 2^{-n} smallness is an artefact of the counting readout; encodings of a satisfiable F and an unsatisfiable F' (one more
  clause) differ by O(1), so robust detection is not excluded information-theoretically — the obstacle is computational.
- Lemma A (PI, standard Grönwall argument): classical dynamics ż = f(z;F), N = poly(n) dimensions, f computable to precision 2^{-b}
  in poly(n,b), Lipschitz K = poly(n), run time T = poly(n), readout correct for all initial states within η = 1/poly of the
  encoding ⇒ numerical integration with b = O(KT + log(1/η)) bits and poly steps decides SAT in polynomial time. Hence a robust
  threshold detector of this kind is equivalent in strength to a poly-time SAT algorithm (P = NP direction).
  **[LEMMA A AS STATED IS NOT PROVED — repaired 2026-11-28.]** Gap: the Grönwall factor e^{KT} is absorbed by b = O(KT + log 1/η) *bits*, but not by the *number of steps*. For Euler with step h and a Lipschitz-in-(t,z) vector field
  (|f_t| ≤ M), the global error is ≤ (M h /(2K))·(e^{KT} − 1); requiring ≤ η forces N = T/h ≥ T M (e^{KT}−1)/(2Kη) steps — exponential in KT when KT = poly(n). Polynomial precision does not give a polynomial step count.
  **Kawamura (Computational Complexity 19 (2010), arXiv:1004.4622; abs + §§1–4.2 read 2026-11-28, §4.3 onward only via a model summary):** setting h(0)=0, h' = g(t,h), t ∈ [0,1], scalar h, g Lipschitz in its second argument with some constant Z independent of y,t, g polynomial-time computable
  (cost polynomial in the output precision m); Thm 3.2: there exist such g with h PSPACE-hard (upper bound PSPACE). Hypotheses that differ from ours: scalar unknown; horizon 1; the hard instance reads out h(1) = 2^{−ρ(|u|)}L(u), an exponentially small quantity (margin 2^{−poly}, not η = 1/poly);
  complexity measured in output precision m plus |u|; g only Lipschitz (no smoothness/analyticity: Lemma 2.2 gives a polynomial modulus of continuity, nothing more). **It is therefore not a counterexample to a robust (η = 1/poly) readout, and it does not exclude Lemma A's conclusion; it shows why "Lipschitz + poly-time f" alone cannot give polynomial-time integration**
  (without a margin, precision grows to poly bits and the Lipschitz-only step count is not controlled). Whether a PSPACE-hard instance exists with margin 1/poly and KT = poly is not answered by the paper.
  **Sufficient conditions for the intended simulation theorem (each gives polynomially many steps; derived/standard, not new):**
  (S1) KT = O(log n) and f Lipschitz in (t,z) with polynomial constants: Euler with N = poly(n,1/η) steps (from the bound above).
  (S2) Dissipative phase: one-sided Lipschitz constant ⟨f(t,z)−f(t,z'), z−z'⟩ ≤ μ|z−z'|² with μ ≤ 0 (logarithmic norm ≤ 0): errors do not grow, global Euler error ≤ T·h·M/2, N = T²M/(2η) steps, independent of K; truncation, stability and time dependence are then controlled by the f_t bound M.
  (S3) f polynomial/analytic in z with polynomial-length trajectory ∫|ż|dt: polynomial-time computability of the solution (Bournez–Graça–Pouly) [R, recalled, not re-read]; time dependence of the schedule must be analytic with polynomially bounded derivatives.
  **[CORRECTION 2026-11-28 — time regularity was missing from S1–S3.]** Counterexample (owner; verified numerically, n = 4, 6, 8): y′ = cos(2π·2^n t), y(0) = 0. Analytic, Lipschitz constant in y is 0, ∫|y′| ≤ 1, exact y(1) = 0 (y = sin(2π2^n t)/(2π2^n)); explicit Euler with 2^k uniform steps returns exactly 1 for every k ≤ n (all sample points t_j = j2^{−k} give cos = 1) and 0 only from k = n+1: error 1 until exponentially many steps. Not a lower bound for all algorithms (the integral is known in closed form; other schemes can do better), but S1–S3 as written do not give an Euler guarantee. Missing quantity: the second derivative along the trajectory, M₂ = sup‖z″‖ ≤ sup(‖f_t‖ + ‖f_z‖·‖f‖) (here 2π2^n). Corrected error bound (Euler, step h, derived): ‖e_N‖ ≤ (h·M₂/(2K))(e^{KT}−1) for K > 0, ≤ T·h·M₂/2 for K = 0 or one-sided Lipschitz μ ≤ 0; with |rounding per step| ≤ ε the extra term is ≤ (ε/h)(e^{KT}−1)/K. **Corrected sufficient condition (Euler): M₂ ≤ poly(n) AND (KT = O(log n) or μ ≤ 0), then N = poly(n,1/η) steps suffice.** Order-p one-step methods: replace M₂ by M_{p+1} = sup‖z^{(p+1)}‖ and h^1 by h^p: N ≈ T·(M_{p+1} T e^{KT}/η)^{1/p}; polynomial iff the derivative growth M_{p+1}^{1/p} (the inverse fastest time scale) is polynomial. (S3) must be read for the autonomous extension (t and every periodic driver as state variables): the driver (cos ωt, sin ωt) has curve length ≈ 2πω T = exponential here, so the Bournez–Graça–Pouly criterion [R] is not met either — consistent. Open: whether the annealing schedule has M_{p+1}^{1/p} polynomial; this is a property of the schedule (rate of change of the Hamiltonian), to be derived for the specific dynamics.
  **[STABILITY CORRECTION 2026-11-28.]** Two earlier statements are wrong for EXPLICIT Euler: (i) "one-sided Lipschitz μ ≤ 0 ⇒ error ≤ T·h·M₂/2, independent of K" — non-expansiveness of the exact flow does not carry over to the explicit scheme; (ii) hence "N = T²M₂/(2η)" for μ ≤ 0. Derivation: with d_j = ẑ_j − z(t_j), ‖d_j + h(f(ẑ_j) − f(z_j))‖² = ‖d_j‖² + 2h⟨d_j, f(ẑ_j) − f(z_j)⟩ + h²‖f(ẑ_j) − f(z_j)‖² ≤ (1 + 2μh + K²h²)‖d_j‖². With the local error ≤ h²M₂/2: E_{j+1} ≤ √(1 + 2μh + K²h²)·E_j + h²M₂/2. For μ ≤ 0: factor ≤ e^{K²h²/2}, so E_N ≤ (h²M₂/2)·N·e^{NK²h²/2} = **(T h M₂/2)·exp(T K² h /2)**. With h ≤ 1/(T K²) the exponential is ≤ e^{1/2}: **N = max(T²K², e^{1/2}T²M₂/(2η)) steps suffice** — polynomial when T, K, M₂, 1/η are (also K = 0 gives no restriction on h). For general μ > 0 the factor is ≤ exp(μh + K²h²/2) and E_N ≤ (hM₂/2)·T·exp(μT + TK²h/2): exponential in μT as before, polynomial iff μT = O(log n). Per-step rounding error ε adds ≤ (ε/h)·N·e^{…} (same factor), so ε ≤ η·h/(2T)·e^{−1/2} suffices. **Higher-order methods:** the one-step convergence theory gives E_N ≤ (C_p h^p M_{p+1}/K)(e^{C′KT} − 1) with method constants C_p, C′ [R]; under μ ≤ 0 explicit Runge–Kutta methods are NOT in general contractive (stability region bounded, non-normal dissipative systems) — one needs h·K ≤ h₀(method) and then an amplification factor 1 + O(K²h²)-type bound must be proved per method; algebraically stable implicit RK methods (e.g. Gauss, Radau IIA) are B-stable [R] (contractive for μ ≤ 0 at every h), with the stage equations solvable by fixed-point iteration when hK < 1 at polynomial cost. So the recoverable theorem is: under (a) one-sided Lipschitz μ ≤ 0 and Lipschitz K, (b) polynomial T, K, M₂ (or M_{p+1}^{1/p}), 1/η, (c) h ≤ 1/(TK²) (Euler) / h ≤ 1/(2K) (implicit RK), and (d) controlled evaluation error, the simulation uses polynomially many steps and the readout is correct.
  Readout robustness (η = 1/poly) is required in all three; trajectory bounds ‖z(t)‖ ≤ R = poly are needed to bound f_t and the Lipschitz constant on the region visited by the numerical scheme.
  **Consequence (scope):** "a robust threshold detector of this kind decides SAT in polynomial time" holds under (S1)–(S3) only; for general Lipschitz dynamics with KT = poly it is unproved and the physical-computation exclusion based on it is withdrawn. The dynamical approach is not excluded: its viability is now a question of which of S1–S3 (or a different stability mechanism) the annealing dynamics satisfy, with a computational cost of at least that of the numerical scheme. Linear quantum dynamics
  with H_F as a black box needs time ~2^{n/2} (Farhi–Gutmann, Hamiltonian search; not re-checked); exploiting F's structure is the
  NP ⊆ BQP question. Neither bears on the binding objective ∃ L ∈ NP \ P.
