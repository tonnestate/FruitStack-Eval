# T44 — Slice transfer and the characteristic-3 decomposition of positive 1-in-3-SAT (director, 2026-11-18)

Owner order 2026-11-18: the director's OWN mathematical investigation (not a campaign). Scripts: `lab/slice/` (gf3_gap.py,
gap_structure.py, check_char3_lemma.py, gap_n7.py). Independent critique: PlumMe work W-c2126626f88449ca (claude-haiku-5-5, gemma-4-31b),
assessed in §6.

Notation. n variables, N = C(n,3) clause bits, f_n(S) = 1 iff the positive 1-in-3 instance S is UNSAT (monotone, coNP-complete).
j = all-ones vector. Sol_3(S) = affine solution set of {sum_{i in C} x_i = 1 (mod 3) : C in S}.

## 1. What the existing evidence actually is (assessment)
- Restricted-model theorems: D-011..D-013 (matroid ports = IDEAL monotone span programs; D-013 gives mSP_F(f_n) >= N+1, a one-row
  bound), D-014/D-014f (Gal rank: every explicit construction so far has ratio about 2 or is provably capped at N).
- Problem-structure theorems: D-015 (LP point 1/3 in every char != 3), D-012 (at n=5, UNSAT = GF(3)-inconsistency), T41 (Fourier dual,
  char-3 count identity, parity hardness).
- Finite computations: D-010/D-010e (exact circuit sizes: no 1-in-3-specific effect at k=6), D-016a-j (linear/cheap invariants do not
  determine the count; all negative).
- Reading: none of these bounds a general model; the only items that describe the PROBLEM rather than a model are D-012/D-015/T41, and
  they all point to characteristic 3. That is the starting point chosen in §3.

## 2. The route: slices (the only known exact monotone-to-general bridge)
A slice function at level m: g(x)=0 for |x|<m, 1 for |x|>m, arbitrary on |x|=m. g_{n,m} := level-m slice of f_n.

Lemma S1 (padding; elementary, proved). For n >= n' + 3m the weight-m inputs of g_{n,m} contain every positive 1-in-3 instance with
<= m clauses on n' variables: add m-m' pairwise disjoint clauses on fresh variables (each is satisfiable, satisfiability unchanged).
So {g_{n,m}} is coNP-hard; a superpolynomial general circuit lower bound for it gives NP not in P/poly, hence P != NP.

Theorem S2 (Berkowitz 1982; KNOWN, cited, not re-proved). For slice functions, monotone and general circuit size are polynomially
related. Hence: a superpolynomial MONOTONE circuit lower bound for g_{n,m} would prove P != NP. This route is an EQUIVALENT
reformulation (no loss, no gain in difficulty): it moves the problem into the monotone world, where lower-bound methods exist
(approximation method, rank measures), but those methods must work on slices.

Lemma S3 (span-program analogue; derived here, novelty unchecked, likely folklore). For a slice g at level m and any field F:
mSP_F(g) <= SP_F(g) * T + 2T', T, T' = mSP_F sizes of threshold functions on <= N variables (T = N-1, T' = N if |F| > N by Shamir;
poly(N) for every F via monotone threshold formulas).
Proof. A span program with literal-labelled rows is a monotone span program in the 2N variables x_i, y_i (y_i read as not x_i).
On |x| = m, theta_i(x) := [sum_{j != i} x_j >= m] equals 1 - x_i (x_i = 1 gives m-1, x_i = 0 gives m). Substitute y_i := theta_i(x):
monotone span programs (= linear secret-sharing schemes, Karchmer-Wigderson) are closed under substitution of monotone sub-schemes
(share each row value with the scheme of the substituted function; the composite is linear; authorised sets are exactly those making
the outer row set authorised). Size: sum over rows labelled y_i of size(theta_i) plus the x_i rows. The result h' is monotone and
equals g on |x| = m; then g = T_{m+1} OR (T_m AND h'), and OR / AND add sizes. QED.
Corollary. For slices, mSP_F and SP_F are polynomially related; a superpolynomial mSP_GF(p) bound for g_{n,m} gives
coNP (equivalently NP, Mod_pL is closed under complement for prime p) not in Mod_pL/poly - a major separation, but WEAKER than P != NP.

Lemma S4 (loss; proved). Over |F| > N: SP_F(g) >= (mSP_F(g) - 2N)/(N-1). So any mSP bound O(N) - all PNP-001 bounds (D-013: N+1;
D-014f: ratio <= N for |v\u| = 1 supports) - is annihilated by the transfer. Only bounds >> N^2 carry over. (Consequence for D-014:
the explicit Gal programme is irrelevant to general computation unless it reaches ratio omega(N^2) on SLICES.)

Lemma S5 (natural proofs applied to the Gal programme; conditional). Let A(g) be a Gal-matrix construction computable in time
2^{O(N)} from the truth table (e.g. critical-pair support, D-014). The Gal ratio is always a valid lower bound, so if A gave ratio
>= s(N) superpolynomial on a >= 2^{-O(N)} fraction of slice functions, this would be a natural property useful against SP size s(N);
slices embed every function (dual rail x -> (x, not x) at level N/2), so - assuming pseudorandom functions COMPUTABLE in NC^1 (hence
in Mod_pL/poly) with 2^{N^eps} security (standard, e.g. Naor-Reingold) - no such construction exists. Hence a Gal-type proof on
slices must use structure specific to the function (non-large). The characteristic-3 structure below is exactly such structure.

## 3. Own derivation: the characteristic-3 decomposition
Lemma C1 (two-value criterion; proved, checked exhaustively: n=5 all 1024 instances, 3000 random n=6, 1500 random n=7, 0 mismatches).
[2026-11-19: FORMALLY VERIFIED - Lean 4.35 kernel, theorem one_in_three_two_value, axioms propext + Quot.sound, lab run 454de9fe-13ee-42a6-ae75-e3cb730c1c42, file sha256 8ae41a9d24fac990fca3435cde7f87c05a09b01dec8c808b950410a600ec5d5e, fidelity MATCH (claim:28014452c616).]
j lies in the kernel of every 3-uniform clause matrix over GF(3). Hence S is SAT iff Sol_3(S) contains a vector with at most two
distinct values.
Proof. (=>) a Boolean solution. (<=) values in {a, a+1} (every 2-subset of GF(3) has this form): y - a j is in Sol_3(S), 0/1-valued,
and a 0/1 vector with clause sums = 1 (mod 3) has clause sums exactly 1 (sums lie in {0,..,3}). QED.

Corollary C2 (decomposition; proved). f_n = INCONS_n OR M_n, where INCONS_n = GF(3)-inconsistency (ideal monotone span program of size
N: rows (1_C, 1), target (0,..,0,1); polynomial time by Gaussian elimination) and M_n = monotone function generated by the minimal
GAP cores (Boolean-UNSAT but GF(3)-consistent, every proper subset SAT). Since INCONS has size N:
   mSP_GF(3)(M_n) >= mSP_GF(3)(f_n) - N        (the hardness of f_n is LOCALISED in M_n).
The reverse direction is NOT claimed (referee correction, §6): a lower bound for M_n does not by itself bound f_n.

Lemma C3 (independence of minimal cores; proved). The clause rows of a minimal GAP core S are linearly independent over GF(3).
Proof. If row C is a combination of the others, consistency makes its equation implied: Sol_3(S) = Sol_3(S\C). By minimality S\C is SAT;
its Boolean solution lies in Sol_3(S\C) = Sol_3(S), so S is SAT by C1 - contradiction. QED.
Corollary C4. A minimal GAP core has at most n-1 clauses (rank <= n-1 because j is in the kernel), and dim Sol_3(S) = n - |S| >= 1.
So M_n is a monotone function whose minterms are independent clause sets of size <= n-1; f_n minus its linear part is exactly the
question "does this affine GF(3) space (direction space contains j) avoid all two-valued vectors".

Exact data (lab/slice; recomputed independently of D-012/D-013).
| n | GAP instances | minimal GAP cores | sizes | affine dim | orbits |
| 5 | 0 | 0 | - | - | - (= D-012) |
| 6 | 1350 of 988,837 UNSAT | 900 | all 5 | all 1 (one line, every point uses 0,1,2) | 3 orbits under S_6: 360, 360, 180 |
| 7 | (not enumerated) | 62,370 (complete by C4: sizes 1..6 searched) | 8,190 of size 5, 54,180 of size 6 | 7 - size | - |
The D-013 obstruction is the statement GAP_n != {} for n >= 6 (for GF(3)); C1-C4 say WHAT the obstruction is.

Hypothesis tested and refuted: "every minimal core has a 1-dimensional solution set (a rigid line)". False at n=7: all 8,190 cores of
size 5 have dimension 2. What survives is C3/C4 (independence, dim = n - |S|), which is proved. Lesson: rigidity was an artefact of n=6.

## 4. What this does and does not reduce
- Proved: (i) exact reformulation of the target through slices (S1, S2), and the span-program version (S3) with its exact loss (S4);
  (ii) the problem splits into a polynomial linear part and a residual M_n with small independent minterms (C1-C4); (iii) every
  PNP-001 lower bound is O(N) and is annihilated by the transfer (S4); (iv) generic Gal constructions are barrier-blocked on slices (S5,
  conditional on standard PRFs).
- Not proved: any superpolynomial bound. The gap is unchanged in size: P != NP <=> (via S2) a superpolynomial monotone circuit bound for
  g_{n,m}; and by C2 any such bound must already hold for the residual M_n-part (localisation).
- Does anything reduce the gap? Only in the sense of LOCATING it: the linear-algebra part of 1-in-3-SAT is now proved irrelevant
  (ideal, size N), and the remaining object (M_n: independent cores, affine spaces avoiding two-valued vectors) is the specific,
  non-large structure that S5 says a successful method must exploit. No reduction of the asymptotic difficulty is claimed.

**Analytic re-derivation 2026-11-28 (no new enumeration) [DED].** Re-proved by hand, each step against its stated hypotheses: S1 (needs n >= n'+3m,
fresh single clauses are satisfiable, UNSAT preserved); S3 (theta_i = 1 - x_i on |x| = m checked for x_i = 1 -> m-1 < m and x_i = 0 -> m;
cost s*T counts every row occurrence; Shamir needs |F| > N, GF(3) uses monotone threshold formulas, size poly(N)); S4 follows from S3 by
rearrangement; C1 (shift y - a j keeps clause sums, 0/1 values force sum exactly 1 since sums <= 3); C2 (a Boolean-UNSAT, GF(3)-consistent set contains a
minimal such subset, and subsets of consistent sets are consistent); C3/C4 (rank <= n-1 because j is in the kernel; dim Sol = n - |S|).
Arithmetic of the table: 360+360+180 = 900; 8,190+54,180 = 62,370. The counts 1350 / 988,837 / 62,370 are STORED enumeration values
(lab/slice, previously verified), not recomputed in this round. No premise of T44 depended on the corrected e*, T6, T29 or T52 statements:
nothing stale. Scope reminder: S3's corollary gives only coNP not in Mod_pL/poly, strictly weaker than P != NP (Mod_pL is inside P).

## 5. Next decisive mathematical question (commissioned to the D-014 campaign via the proofbook)
Q-T44: Does a Gal matrix with columns = minimal GAP cores (M_n minterms) and rows = maxterms of M_n (or of the slice g_{n,m} restricted to
the M part) reach ratio > N at n = 6, 7, and how does the best ratio grow from n=6 to n=7? Why decisive: D-014f caps every
single-difference construction at N, and S4 says only omega(N^2) on slices matters; the cores are the first FUNCTION-SPECIFIC column
family (independent sets with |v \ u| typically >= 2, outside the D-014f cap, and not large in the sense of S5). If the ratio stays
O(1) as for every natural family so far, the Gal programme has no f-specific lever left and should be abandoned for this function;
if it grows with n, it is the first candidate method that is neither capped (D-014f) nor barrier-blocked (S5).

## 6. Independent criticism (PlumMe W-c2126626f88449ca) and my assessment
- Haiku: S1 valid (corrected wording: UNSAT is coNP-complete; P/poly conclusion unaffected). S3 composition step needed an explicit
  proof (added above via secret-sharing composition). S5 "INVALID": objection rests on reading "PRFs in NC^1" as security against NC^1;
  meant is computability in NC^1 with exponential security - the standard Razborov-Rudich hypothesis; wording made explicit; S5 stays
  CONDITIONAL. C1/C2 valid; correctly flagged that only mSP(M) >= mSP(f) - N holds, not the reverse (my first draft said "differ by at
  most N" - corrected). Also: no theorem makes the SPAN-PROGRAM route equivalent to NP not in P/poly (only to Mod_pL/poly) - agreed (S3 corollary).
- Gemma: called S3 invalid (substitution "disrupts linear dependencies") - rejected: substitution in linear secret sharing is standard and
  the cost s*T already counts every occurrence. Called C1 invalid with a {0,2}-valued "counterexample" - rejected: y - 2j is then {1,0}
  valued and Boolean; C1 is also verified exhaustively. Confirmed S2 (Berkowitz) and that the circuit route is exactly as hard as
  NP not in P/poly - agreed; that is why S2 is a reformulation, not progress.
