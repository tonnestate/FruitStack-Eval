# T42 — CRT for Subset Sum: separate vs joint vs exact feasibility, and the role of idempotents (PI, 2026-11-18)

STATUS: owner instruction 2026-11-18 (continue the CRT experiment; no new mission). PI proofs plus exact computation in
lab/crt/crt.py (crt.out.json, seed 20261118). Not in the ledger. T40/T41 untouched; FruitStack queue untouched.

## 1. Definitions (same instance w ∈ ℕ^n, target t with 0 ≤ t ≤ Σw, primes p_1..p_s, M = Π p_j)
- SEP: for every j there is b^{(j)} ∈ {0,1}^n with Σ b^{(j)}_i w_i ≡ t (mod p_j).
- JOINT: there is one b ∈ {0,1}^n with Σ b_i w_i ≡ t (mod p_j) for all j. By CRT this is ⇔ Σ b_i w_i ≡ t (mod M).
- EXACT: there is b ∈ {0,1}^n with Σ b_i w_i = t.
Hierarchy (immediate): EXACT ⇒ JOINT ⇒ SEP.

## 2. Theorems
Theorem J (exact threshold for JOINT). If M > max(t, Σw − t), then JOINT ⇔ EXACT; in particular whenever M > Σw.
For every instance: JOINT accepts iff some subset sum s satisfies M | (s − t). *(Corrected 2026-11-28:)* a JOINT false positive (accepts although no exact solution exists) exists iff t is not a subset sum AND some subset sum s ≠ t satisfies M | (s − t). A modular collision alone is not a wrong decision: w = (1,2), t = 1, M = 2 has sums {0,1,2,3}, the collision 3 ≡ 1 (mod 2), yet the answer is correct because the exact sum 1 exists.
Proof. s − t ∈ [−t, Σw − t]. A nonzero multiple of M in that range needs M ≤ max(t, Σw − t). ∎
Theorem I (SEP = solvability over the idempotents). Let E = {e ∈ ℤ/M : e² = e}. Since M is squarefree, E ≅ {0,1}^s, and e
corresponds to the set {j : e ≡ 1 mod p_j}; |E| = 2^s. Then
  SEP ⇔ ∃ x ∈ E^n with Σ x_i w_i ≡ t (mod M),
  JOINT ⇔ the same with x ∈ {0,1}^n = {0,1} ⊂ E (the two trivial idempotents).
Proof. Given the b^{(j)}, put x_i := the CRT lift of (b^{(1)}_i, …, b^{(s)}_i). Each component is 0 or 1, so x_i² = x_i, and the
congruence holds mod every p_j, hence mod M. Conversely, reduce x mod p_j: idempotents of 𝔽_p are 0 and 1, which gives b^{(j)}. ∎
Consequence. The gap SEP \ JOINT is exactly the set of instances that are solvable only with at least one NONTRIVIAL idempotent
coefficient, i.e. with per-prime solutions that disagree on some coordinate. M > Σw closes the JOINT gap (Theorem J), but it does
nothing against the idempotent gap. So no size condition on M makes SEP correct.
Smallest counterexample (found by exhaustive search): w = (1, 4), t = 2, primes {2, 3}, M = 6 > Σw = 5.
- Mod 2: t ≡ 0, reached by {} (and by {4}).
- Mod 3: t ≡ 2, reached only by {1, 4} (sum 5).
- Mod 6: the subset sums are {0, 1, 4, 5}, and 2 is not among them. So SEP holds, JOINT fails, EXACT fails.
- Idempotents mod 6: {0, 1, 3, 4}, with 3 = (1 mod 2, 0 mod 3) and 4 = (0 mod 2, 1 mod 3). Lifting b^{(2)} = (0, 1) (mod 2) and
  b^{(3)} = (1, 1) (mod 3) gives x = (4, 1): 4·1 + 1·4 = 8 ≡ 2 (mod 6). The witness needs the nontrivial idempotent 4, as
  Theorem I says.
Theorem K (cost). By bitset DP, SEP costs Θ(n Σ_j p_j) time and Σ_j p_j bits. JOINT costs Θ(nM) and M bits. EXACT costs Θ(n Σw)
and Σw + 1 bits. When JOINT is guaranteed correct by Theorem J (M > max(t, Σw − t) ≥ Σw/2), JOINT is no cheaper than EXACT up to a
factor 2. JOINT mod M is itself Subset Sum mod M, NP-complete with M in binary. So CRT recombination does not reduce the cost of
exact pseudo-polynomial DP. The cheap quantity (SEP) is the incorrect one, by Theorem I.

## 3. Computation (crt.py; 7200 instance/modulus pairs; n ∈ {8, 12, 16, 20}; weights ≤ 2^8 or 2^12; half the targets feasible)
- Theorem I: 60 random instances, exhaustive over E^n: 0 mismatches.
- Hierarchy violations: 0 (24 rows with M > 2^24 skipped the JOINT DP and are excluded).
- False positives among infeasible targets, by ρ = M/Σw:

| ρ | SEP false positives | JOINT false positives |
|---|---|---|
| 0.01 | 259/285 | 175/285 |
| 0.1 | 266/285 | 80/285 |
| 0.5 | 258/285 | 10/285 |
| 1 | 260/285 | 0/285 |
| 2 | 262/285 | 0/285 |
| 10 | 250/285 | 0/280 |

- With M > Σw: JOINT false positives 0 (as Theorem J requires), SEP false positives 1097 of 1221 infeasible instances. With
  M > max(t, Σw − t): JOINT false positives 0.
- Mean cost with M > Σw (bits / ms):
  - n = 8: SEP 205 / 0.011, JOINT 458 336 / 0.041, EXACT 8 715 / 0.005.
  - n = 20: SEP 219 / 0.024, JOINT 1 251 683 / 0.094, EXACT 20 911 / 0.021.
  JOINT is larger than EXACT here because the moduli overshoot Σw. These are measurements of this implementation, not lower
  bounds.
- No threshold at 2^n is assumed. The relevant scale is Σw (Theorem J), and measured percentages are not used to infer asymptotics.

## 4. Placement
The owner's correct distinction (T41 discussion: recombining solution SETS vs recombining the one global COUNT) is made exact:
- per-modulus feasibility = Boolean algebra of idempotents (Theorem I);
- the global count C mod p_j recombined by CRT is exact once Π p_j > C_max;
- a common witness b is exact once M > max(t, Σw − t).
The open quantity is the same as in T41: an efficient way to obtain the global count (or one consistent witness) modulo each
p_j. Nothing here bears on P vs NP.
