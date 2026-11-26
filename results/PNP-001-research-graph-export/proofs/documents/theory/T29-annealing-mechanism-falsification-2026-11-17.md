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
  threshold detector of this kind is equivalent in strength to a poly-time SAT algorithm (P = NP direction). Linear quantum dynamics
  with H_F as a black box needs time ~2^{n/2} (Farhi–Gutmann, Hamiltonian search; not re-checked); exploiting F's structure is the
  NP ⊆ BQP question. Neither bears on the binding objective ∃ L ∈ NP \ P.
