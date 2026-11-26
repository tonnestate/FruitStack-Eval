# T45 — Exact transfer lemma, D-013 transfer verdict, conditions on a lower-bound invariant (director, 2026-11-18)

Owner order 2026-11-18 (Tasks 1-5). Scripts: `lab/transfer/p4_control.py`. Builds on T44. Critique: PlumMe (§7).
F_n : {0,1}^N -> {0,1}, N = C(n,3), bit = presence of a positive exactly-one clause on 3 DISTINCT variables, F_n = 1 iff UNSAT.
S(f) = minimum number of fan-in-2 gates (any of the 16 binary functions; NOT is free or costs 1 - irrelevant up to factor 2).

## 1. Task 1 — Transfer lemma (proved, standard ingredients cited)
Lemma T1 (encoding). L = {positive 1-in-3 instances that are satisfiable} is NP-complete (Schaefer 1978; Garey-Johnson LO4). Clauses
with repeated variables are eliminated in polynomial time (x,x,y forces x=0, y=1; x,x,x is unsatisfiable), duplicate clauses are
irrelevant, so distinct-variable instances remain NP-complete. An instance with m clauses mentions <= 3m variables; renaming them
1..n (n <= 3m) gives the input x in {0,1}^N of F_n with N = C(n,3) <= (3m)^3: a polynomial-time map, and F_n(x) = 1 - [x in L].
Lemma T2 (uniform). P = NP  =>  L in P  =>  {F_n} computed in time poly(N). Conversely a poly(N)-time algorithm for F_n decides L in
polynomial time, so P = NP. Hence: P != NP  <=>  no polynomial-time algorithm computes F_n.
Lemma T3 (circuits). A time-t(N) TM yields circuits of size O(t log t) (Pippenger-Fischer). So P = NP => exists c: S(F_n) <= N^c + c
for all n. Contrapositive (the exact sufficient condition): if for every c there is n with S(F_n) > N^c + c (superpolynomial
INFINITELY OFTEN), then P != NP. The owner's "for all n >= n_0: S(F_n) >= n^{log2 n}" implies this (n^{log n} is superpolynomial and
N = Theta(n^3)), so it is sufficient, and stronger than needed (infinitely often suffices).
Lemma T4 (non-uniform strength). Such a bound gives coNP not in P/poly, equivalently NP not in P/poly (P/poly is closed under
complement; F_n is coNP-complete). Since P is in P/poly this is at least as strong as P != NP; it is NOT necessary - P != NP with
NP in P/poly is not excluded by any known theorem (Karp-Lipton only collapses PH to Sigma_2).
Lemma T5 (the weaker uniform target). L in P <=> L has P-uniform polynomial-size circuits. So a superpolynomial lower bound for F_n
against P-UNIFORM (or logspace-uniform) circuits is EQUIVALENT to P != NP - the exact uniform statement, weaker than T3/T4.

## 2. Owner's formula: S(f) >= log2 D_k(f) - 1 (verified true; proved capped)
Let R = relevant variables of f, r = |R|. Fixing a set T (|T| = k) of variables to 1 gives a function determined by T ∩ R
(irrelevant variables change nothing). So D_k(f) <= 2^r. A circuit computing a function of r relevant variables needs >= r - 1
gates. Hence D_k(f) <= 2^r <= 2^{S(f)+1}: the formula holds. But log2 D_k(f) - 1 <= r - 1 <= N - 1 for EVERY f and k: the method
cannot exceed a linear bound, i.e. O(n^3) for F_n - never n^{log n}. This is a theorem, not a numerical shortfall: the number of
subfunctions of a function of N variables under restrictions to a single fixed value class is at most 2^N. (The formula-size analogue,
Nechiporuk, is capped at O(N^2 / log N) for the same reason.)

## 3. Task 2 — D-013 transfer verdict
(a) What D-013 excludes. "Matroid port" = access structure of an IDEAL secret-sharing scheme (Brickell-Davenport); ideal LINEAR
schemes = monotone span programs with exactly one row per input. D-013 excludes those (over every field, and non-linear ideal
schemes too), i.e. it proves mSP_F(F_n) >= N + 1. Nothing about circuits.
(b) Why P4 is small. P4 = ab | bc | cd has S = 4 (owner's circuit) and mSP = 5 (monotone formula (a&b)|(c&(b|d)) has 5 leaves; any
MSP with 4 rows would be ideal, excluded). The obstruction is QUALITATIVE (ideal vs non-ideal), worth exactly one row.
(c) Restriction transfer is valid but weak. Minors are restrictions; S(f|rho) <= S(f), so S(F_n) >= S(H) for every minor H. With H = P4:
S(F_n) >= 4. Constant.
(d) Amplification by direct sums is provably linear. Variable-disjoint sub-instances: UNSAT(S1 ∪ S2) = UNSAT(S1) OR UNSAT(S2). For any
minor of the form h(g_1, ..., g_t): S <= S(h) + sum S(g_i). t disjoint P4's (t <= N/4) give a minor of size <= 5t - 1 = O(N). More
generally composition of a fixed obstruction with an outer function only yields what the outer function already has (circular).
(e) DECISIVE CONTROL (computed, lab/transfer/p4_control.py): the D-013 obstruction occurs in 2-SAT, a polynomial-time problem.
2-SAT on 3 variables, clauses (x_u = s_u) OR (x_v = s_v): fix PRESENT (x0 | ~x1), (x0 | x1), (~x1 | x2); fix ABSENT all others except
a = (~x0 | ~x1), b = (~x0 | x1), c = (~x0 | ~x2), d = (~x0 | x2). Then UNSAT = ab | bc | cd (hand check: the two fixed clauses force
x0 = 1, so a,b,c,d become ~x1, x1, ~x2, x2 with x1 -> x2; ab, bc, cd are contradictory, ac, ad, bd are satisfiable). By the D-013
Lemma 1 argument (restriction to a variable subset), 2-SAT's UNSAT clutter is not a matroid port for every n >= 3. Calibrations of the
same search: 1-in-3 n=5 no P4 (D-012 GF(3) port), XOR-SAT n=4 no P4 (binary port for all n), P4 found in P4.
VERDICT. "Not a matroid port" holds for an NL-complete problem with linear-size circuits; so it cannot imply any superpolynomial - or
even super-linear - circuit lower bound. D-013 is a correct theorem about ideal secret sharing / ideal monotone span programs and is
NOT a route to a general lower bound. Its specificity is only versus XOR-SAT (a GF(2) port), i.e. it measures field-linearity, not
hardness. D-013 is retired as a proof route (kept as a theorem).
(f) Survival under NOT/AND/OR/sharing: the only property that survives arbitrary gates is restriction-monotonicity of S (c); all
port/ideality properties are about one-row-per-input representations and are destroyed by any non-ideal encoding; open obligation
none - the transfer is refuted by (e).

## 4. Task 3 — Conditions any invariant Phi must satisfy (derived), and the candidates tested against them
R1 Soundness: Phi(f) <= poly(S(f)) for all f (e.g. Phi(f op g) <= Phi(f) + Phi(g) + 1 on a circuit's set of computed functions).
R2 Beyond counting: Phi must not be bounded by a function of subfunction counts under restrictions (§2: capped at N for circuits).
R3 Beyond minors of fixed size: Phi must not be obtained from fixed-size obstructions by composition (§3d: capped at O(N)).
R4 Controls: Phi(2-SAT_n), Phi(XOR-SAT_n) polynomial - IMPLIED by R1; any candidate giving superpolynomial values there is unsound.
   Field-relative measures (span programs over GF(p)): XOR-SAT is a valid control only over GF(2); 2-SAT (NL/poly = UL/poly, in
   Mod_pL/poly) is valid over every field.
R5 Barriers: if Phi is computable in time 2^{O(N)} from the truth table and large on a 2^{-O(N)} fraction of functions, it is a
   natural property (blocked under standard PRFs in NC^1, T44 S5). Phi must be function-specific or non-constructive.
Candidates from PNP-001 evidence:
| candidate | R1 | R2 | R3 | R4 | R5 | verdict |
| subfunction count D_k (owner) | yes | FAILS (cap N) | - | yes | - | dead (theorem §2) |
| non-port / D-013 | no (monotone, ideal only) | - | FAILS | FAILS (2-SAT has P4) | - | dead as hardness signal (§3e) |
| Gal rank on F_n (D-014) | only for mSP, not circuits | - | single-difference families capped at N (D-014f) | - | generic constructions natural | not a circuit route |
| exact small circuit sizes (D-010e) | yes (exact) | finite | - | XOR control harder than 1in3 at k=6 | - | finite data, no asymptotics |
| linear/rank/count invariants (D-016a-j) | - | - | - | fail (do not even determine C) | - | dead |
| mSP of SLICES (T44 S3) | yes for SP_F (=> NP not in Mod_pL/poly), loss factor N (T44 S4) | open | open | must be checked with 2-SAT | generic: blocked | open; weaker target |
| monotone circuit size of SLICES (Berkowitz) | yes for P/poly (poly loss) | open | open | automatic | method-dependent | open = equivalent to the problem |
ML/feature engineering: any feature computed from finite truth tables is constructive; if it separates 1-in-3 from random functions it
is large and hence (R5) cannot be the invariant; if it separates 1-in-3 from 2-SAT/XOR-SAT only on finite data it says nothing about
R1. ML can propose function-specific structure (as the campaigns did: D-016 series), not certify an invariant.

## 5. Task 4 — the decisive test (executed)
Conjecture K (the implicit premise of the matroid route since D-011): "failure to be a matroid port (the D-013 obstruction) indicates
computational hardness of the UNSAT function". Supporting argument at the time: 1-in-3 fails from n=6 on, XOR-SAT (in P) never fails.
Weakest step: the control set contained only XOR-SAT, which is a GF(2) port by construction - a field-specific control. Finite test:
exhaustive P4-minor search in the UNSAT function of 2-SAT (in P, NL-complete) - executed: P4 found at n=3 (explicit witness §3e).
Agents: PlumMe critique W (see §7) asked to break the witness. Result: K REFUTED. What is ruled out: every implication of the form
"non-port (or any excluded-minor property of the MUS clutter shared with 2-SAT) => super-linear circuit size".

## 6. Next mathematical step (single most important lemma)
Everything PNP-001 proved so far is either sound-but-capped (counting, minors, D-014f) or unsound for circuits (monotone/ideal
properties). The only candidates meeting R1 are the slice measures, and for them R2-R5 are open. The next lemma is therefore not a
new measure but a CONTROL lemma for the one function-specific structure we have (T44 cores):
  Lemma L* (to prove or refute): the T44 decomposition F_n = INCONS_n OR M_n has no analogue for 2-SAT with an exponentially growing
  residual - i.e. for 2-SAT the analogous "linear part" (implication-graph reachability) already captures UNSAT with polynomial
  overhead, while for 1-in-3 the minimal residual cores grow (900 at n=6, 62,370 at n=7). If L* holds, the residual M_n is a
  function-specific (non-natural) object that separates 1-in-3 from 2-SAT, and lower bounds for monotone circuits on SLICES of M_n
  are the precise target (sound via Berkowitz). If L* fails (2-SAT has an equally growing residual), the T44 decomposition does not
  carry hardness and the Gal/core programme (Q-T44) loses its last justification.
No unproved circuit lower bound is claimed anywhere in this document.

## 7. Independent criticism
PlumMe W-83465c2ba7394d3e (claude-haiku-5-5, gemma-4-31b), both independent families:
- Claim A (T1-T5): VALID (both). Haiku re-derived T5 including hard-coding finitely many lengths; only "as far as known" wording loose.
- Claim B (owner formula capped at N): VALID (both); Haiku re-proved S >= r-1 by the cone/edge count. Nechiporuk cap: not re-checked by
  Haiku, asserted by Gemma - kept as cited, not re-proved here.
- Claim C (2-SAT has P4): VALID - Haiku checked all 16 subsets of {a,b,c,d} by hand against the three remaining points (00, 01, 11).
- Claim D (direct sums linear): VALID (both); Haiku found the 4-gate circuit b(a|c) | cd.
- Claim E (field-relative controls): XOR GF(2) part valid; 2-SAT control valid via NL/poly = UL/poly and UL in Mod_pL (Haiku checked the
  latter directly). Gemma's alternative justification "NL in DET in Mod_pL" is REJECTED (DET in Mod_pL is not known); the UL argument stands.
- Final question (both): no super-linear lower bound for an explicit function is known for unrestricted fan-in-2 circuits (best ~3n);
  super-linear/superpolynomial bounds exist only for restricted models (formulas: Khrapchenko, Andreev/Hastad n^{3-o(1)}; AC^0, AC^0[p];
  monotone: Razborov). Consistent with R2/R3: both of our capped methods are of the kind that stays linear for circuits.

## 8. Self-correction (director, after delivery)
L* (§6) is WITHDRAWN as the "next decisive lemma". Reason: the number or growth of minimal residual cores is a count of minterms of a
monotone function, and minterm counts are not a complexity measure (2-SAT, in P, has exponentially many MUS; any count fails R1).
Relative to its own polynomial algorithm 2-SAT has no residual at all, and relative to a foreign linear part the residual size says
nothing about hardness. So L* would not change the proof strategy whichever way it came out. Corrected next step: there is no
PNP-001 candidate satisfying R1-R5; the only sound target remains a lower bound for monotone circuits on slices of F_n (Berkowitz),
which is equivalent to the original problem. Q-T44 (Gal on cores) stays a question about monotone span programs only.
