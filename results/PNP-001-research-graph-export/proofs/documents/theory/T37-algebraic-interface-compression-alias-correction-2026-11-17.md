# T37 — Algebraic interface compression with alias correction: checks, reduction, exact question (PI, 2026-11-17)

STATUS: owner's direction (2026-11-17, from the Grok/Gemini reports). Checks below executed by the PI (scratchpad charsum.py).
Verification: FruitStack iteration 8 (req-pnp-iter08.json, chained after 7). Not in the ledger.

## 1. Checked facts
- Owner's counterexample: W = (1,1,1,1,2,2,2,2,2), t = 4: c_t = 41 solutions; −Σ_{x∈F_41^*} x^{36} P(x) ≡ 0 (mod 41). CONFIRMED.
  Grok's "exact decision by one character sum" is REFUTED: the sum yields c_t mod p, which vanishes for p | c_t.
- Identity (character orthogonality): −Σ_{x=1}^{p−1} x^{p−1−t} P(x) ≡ c_t (mod p) REQUIRES p − 1 > D = Σ w_i (else exponents wrap mod
  p−1 and residues of other sums s ≡ t (mod p−1) are added — these are exactly ALIASES).
- Multi-prime theorem (owner): distinct primes p_j > D + 1 with Π p_j > 2^n ⇒ [solution exists] ⇔ some residue ≠ 0 (c_t ≤ 2^n, CRT).
  CONFIRMED in 300 random instances (n ≤ 9, w ≤ 12), 0 errors. Cost: about n / log D primes of size ≈ D, each sum p·n operations ⇒
  Θ̃(n² D) — pseudo-polynomial, the same regime as dynamic programming; exponential when weights have n bits. Not a new complexity bound.
- OpenAI "Subset Sum in Time 2^{0.49n}" (openai/math preprints/Subset-Sum-in-Time-2-power-0-49n-October-4-2026): "a subset is an alias if
  its sum is t′ modulo P but not over the integers" (l.110); "We estimate the modular sum and subtract the phases of a COMPLETE LIST of
  aliases" (l.121). Alias correction needs the aliases to be listable cheaply (distinct-sum / representation structure). CONFIRMED.
- Gemini's matrix power M^T: configuration graph N = 2^{O(S)}; Savitch is recursive reachability (O(S²) space), not repeated squaring.
  Owner's correction CORRECT.

## 2. Reduction: the Turing-machine layer adds nothing
Strassle–Subercaseaux Thm 2 transfers circuit-CSP algorithms to NTIME LOSSLESSLY (2^{O(t/k)}·2^{O(t/s)}). Hence "alias correction on TM
block transitions" is equivalent to: improve exact counting/deciding for density-O(1) circuit-CSPs of arity ≤ n^{9/10} beyond
2^{O(n/√log n)} (Lemma 1.3). Work at the CSP level; the TM version follows automatically.

## 3. Consequences of success (both directions, exact)
- Algorithmic: NTIME[t] ⊆ DTIME[2^{t^{1−ε}}] would give 3-SAT (n variables, O(n) clauses, in NTIME[O(n log n)]) in 2^{n^{1−ε′}}, refuting
  Weak ETH ⇔ SH (arXiv:2611.02650). Still not P = NP (needs polynomial).
- Lower bounds (Williams' method): larger savings s(n) for circuit-CSP enlarge the circuit classes against which E^NP / NEXP lower bounds
  follow (T23 cost inequality, T34 C1). Not P ≠ NP.

## 4. Already present in the ETH engines?
OpenAI's ETH algorithm fixes "a few integer linear measurements" and recovers the exact count by Hermite interpolation (§1.1.5, §2):
an EXACT treatment of what single projections confuse. Anthropic's signed edge factorizations do the same for consistency constraints.
Whether this is literally alias correction in the subset-sum sense is to be checked (iteration 8), not assumed.

## 5. Exact open question (narrow)
For the density-2 circuit-CSP of a block-respecting history (2611.11832 Lemma 2.1), take a modular projection h of each interface
(b bits → Z_P). Alias = a family of interface values consistent under h but not exactly. A1: bound the number/structure of aliases
for explicit families. A2: give an algorithm subtracting their contribution in time 2^{o(n/√log n)}. Without A1 (few, listable aliases)
the subset-sum mechanism does not transfer. Status: OPEN; no claim.
