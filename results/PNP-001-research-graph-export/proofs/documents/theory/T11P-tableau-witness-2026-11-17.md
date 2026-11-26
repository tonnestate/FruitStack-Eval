# T11-P — delta_(6,6,6,4,2)(D_4) = 1 by a direct tableau highest-weight witness (PI, 2026-11-17)

STATUS: VERIFIED. Independent adversarial review (separate agent, own code in /tmp/claude-0/review_t11p/) found no flaw:
it recomputed the k=0 value with its own C evaluator over all 298,598,400 assignments, with the tensor built as mixed discriminants of
the five coefficient matrices, modulo 2^61-1 and 2305843009213693921, and recovered -37673274855121317888 by CRT; it confirmed the
normalisation (the tests fail with raw coefficients), the weight and raising behaviour by substitution on f, the reduction to five
variables, and p_lambda = 1 by a direct multiset-counting DP (sum of mult*dim over all dominant lambda = C(75,6)).
Convention: multiplicity of S_lambda(V*) in Sym^6(Sym^4 V*), i.e. in the degree-6 functions. The reviewer rechecked section k=0 only.

## Result
For lambda = (6,6,6,4,2) |- 24, degree d = 6, quartics (n = 4):
    p_lambda = 1,  delta_lambda(D_4) = 1,  and also gamma_lambda(Y_{3,4}) = 1.
So E_D is injective at this lambda: it contributes NO equation of D_4 and no separating equation. One of the two open degree-6
five-row candidates with lambda_1 = 6 is closed. (6,6,4,4,4) is untouched. The degree-6 front is NOT complete: five-row partitions
with lambda_1 > 6 and partitions with more than five rows remain open. d_min^sep(3,4) stays in [6,24].

## Construction (Breiding–Ikenmeyer–Michalek–Hodges, arXiv:2110.06608, Section 4, formula (dagger))
Isobaric semistandard tableau, each symbol 1..6 exactly four times:

    1 1 1 1 2 2
    2 2 3 3 3 3
    4 4 4 4 5 5
    5 5 6 6
    6 6

Columns (symbols top to bottom): [1,2,4,5,6] [1,2,4,5,6] [1,3,4,6] [1,3,4,6] [2,3,5] [2,3,5]; heights 5,5,4,4,3,3.
P(F) = sum over column permutation assignments T of sgn(T) * prod_{symbol s} F(multiset of the four numbers on the boxes of s),
where a column of height h receives each of 1..h once and F(i,j,k,l) is the symmetric-tensor entry of the quartic, i.e.
raw coefficient of x^alpha divided by the multinomial 4!/prod(alpha_i!). The code uses 24*F (integers); P(24F) = 24^6 P(F).
The literal sum has 5!^2 4!^2 3!^2 = 298,598,400 terms.

## Tensor network and contraction (planned before the computation, `plan.py`)
Six symbol nodes (symmetric order-4 tensors F) and six column nodes; one edge per box. Column tensors are supported on the
permutations of 1..h only: 120, 120, 24, 24, 6, 6 nonzero entries. Because F is symmetric, a partial assignment matters only through
the multiset of numbers each still-open symbol has received; states with equal multisets are merged, and a symbol is closed
(multiplied in as F) when its fourth box is assigned.
Column order chosen: (2,3,0,1,4,5) (0-based). Merged states after each column: 24, 282, 26 864, 1 800, 8 533, then 1.
Total transitions 3,320,118 (3,268,920 before the last column + 8 533*6). Peak 26 864 states.
Measured: 5 s per evaluation in pure Python with exact integers, peak RSS 71 MB (mostly sympy). No weight-space matrix is built.

## Validation (`crosscheck.py`, `gates.py`, outputs in `checks/t11p/`)
1. Paper's worked example c = d = 2: 2*F11*F22 - 2*F12^2 reproduced.
2. Contraction equals the literal permutation sum (Python) on shapes (4,4,4), (6,3,3), (5,4,3), (4,4,4,4), (6,4,4,2).
3. For lambda = (6,6,6,4,2): contraction equals an independent C implementation of the literal 298,598,400-term sum modulo
   p = 2147483647, on a random integer tensor (230016686) and on the determinant witness (1496438837).
4. Generic quartic: P = -4064950608 != 0 (random symmetric tensor, entries in [-9,9], seed 20261117).
5. Torus weight: P(t.F) = t^lambda P(F) for t = (2,3,5,7,11).
6. Raising operators, EXACT (`expand.c`, `raising.py`): all 298,598,400 assignments grouped into the monomial basis give 73,100
   nonzero monomials (weight space: 76,288), stored in `P_66642_monomials.json`; every monomial has weight lambda; and
   R_k P_T = 0 identically for k = 1..4 (69,628 / 69,628 / 54,837 / 41,358 monomials touched, all coefficients cancel), where
   (R_k A)(m) = #(k+1 in m) * A(m with one k+1 -> k). So P_T is a highest weight vector by direct computation, not only by the
   paper's theorem. The monomial form equals the contraction on a random tensor.
   Numerical side check: P(g.F) = P(F) for g: e_{i+1} -> e_{i+1} + 2 e_i, i = 1..4; the opposite direction holds for i = 1,2 and
   fails for i = 3,4, as lambda_1 = lambda_2 = lambda_3 > lambda_4 > lambda_5 predicts.
7. Veronese control: P(l^4) = 0 for l = (3,-2,5,1,-4).
8. Vanishing control with a different HWV (`witness.py control`): lambda = (4,4,4,4,4), d = 5. The engine returns 0 on l*perm_3
   sections k = 0,1 (as the rectangular null-cone lemma T11-N requires) and nonzero values on det_4 sections. So the engine does
   detect vanishing on the padded permanent when it must occur; nothing is inferred from the padding-floor bound alone.

## The witness (`witness.py target`, `witness_target.json`)
Section k: the 4x4 matrix X_k(y) with entry (a,b) = sum_{t=0..4} c y_{t+1},
    c = (((a+1)(b+2)(t+1) + (a+2b+3t)(k+1) + a^2 t + k t^2) mod 7) - 3,   a,b in 0..3.
f_k = det X_k(y), a quartic in y_1..y_5. Exact integer values of P(24*F_{f_k}):
    k=0: -37673274855121317888     k=1: 25236302950396446720
    k=2:  38385066924993159168     k=3: -653825577592413198336
Modulo p = 2305843009213693967 (next prime after 2^61): k=0: 1526056301511479551, k=1: 2177872858259507050 — identical from the
contraction run mod p, from the stored monomial form, and from the exact integer. The tensor 24*F equals the fourth partial
derivatives of f_k on all 70 index multisets (i.e. all 625 index tuples by symmetry).
Any one of them proves P does not vanish on D_4 (f_k = det_4 composed with a linear map C^5 -> C^16 lies in D_4, and a weight-lambda
highest weight function with five rows only reads the coefficients of monomials in the first five variables). With p_lambda = 1 this
gives delta_lambda(D_4) = 1.
Same P on l*perm_3 sections (3x3 matrix and l from the same formula, l = entry (3,3)): -104090023121043456, 569258564910637056,
-2214767837184000, 331048203633939456 — all nonzero, so gamma_lambda(Y_{3,4}) = 1 as well.

## p_lambda (`pleth.py`)
Weight multiplicities of h_6[h_4] in five variables via exp(sum_k h_4(x^k)/k); N(lambda) = 76288 and 133366 reproduce the earlier
weight-space dimensions. Weyl alternating sum gives p_(6,6,6,4,2) = 1 and p_(6,6,4,4,4) = 1.
Owner's Kronecker prefilter (ordinary and symmetric Kronecker coefficients, both positive for both candidates) excludes neither.

## Original software
The authors' code (tableau database generator `PlethysmDBcode.zip`, Julia code `highest_weights_in_julia.zip`) is linked from
https://www.dcs.warwick.ac.uk/~u2270030/GL-paper/GL-paper.html . Located after our engine was written; NOT downloaded or run (no Julia
here). Our engine was instead checked against the paper's definition, its worked example and an independent literal summation.
The paper's algorithm expands (dagger) into monomials; the merged-state contraction used here is our adaptation of it.

## Not done
(6,6,4,4,4) was not evaluated (owner: report first). No claim about any other degree-6 partition.

## Cross-check with the owner's independent run and regression against T11-J/L (`regression.py`, `regression.out`)
- Shape (6,6,6,4,2), content (4^6) has exactly 135 semistandard tableaux (owner's count confirmed).
- Owner's tableau 111144 / 222255 / 333366 / 4466 / 55 is ours up to renaming the symbols (same columns as sets after the renaming
  1,4,6 -> 1,2,3; 2,5 -> 4,5; 3 -> 6), so it defines the SAME polynomial: ratio exactly 1 at two random tensors, two det_4 sections and
  one l*perm_3 section; it vanishes on l^4. The owner's value 519 mod 1009 could not be reproduced here because the embedding matrices of
  that run are not on this machine.
- Regression: for the five p=2 partitions of T11-J/L at degree 4, (12,4), (10,6), (10,4,2), (8,6,2), (8,4,4), the tableau engine
  evaluates all semistandard tableaux (15, 16, 27, 24, 15) and finds rank 2 on generic tensors, rank 2 on det_4 sections and rank 2
  on l*perm_3 sections — the same gamma = delta = p = 2 as the earlier raising-kernel engine.

# Second certificate: lambda = (6,6,4,4,4)  (`cert.py 6,6,4,4,4`, `cert_66444.out`, `cert_66444.json`)
STATUS: VERIFIED. Independent adversarial review (separate agent, /tmp/claude-0/review_t11p_2/) found no flaw: with its own
tensors and the first reviewer's literal-sum evaluator it recovered both exact values (det_4 and l*perm_3, k=0) by CRT from two
61-bit primes; confirmed weight, raising behaviour and Veronese vanishing by substitution on the quartic (random-point tests),
p_lambda = 1 by direct multiset counting, the five-variable reduction for both orbit closures, and the twin-colour lemma
(proof checked; `evaluate_sym` matched the literal sum on 150 random column systems; mutation tests detect a wrong sign).

## Result
p_lambda = 1, delta_lambda(D_4) = 1, gamma_lambda(Y_{3,4}) = 1. Same conclusion as for (6,6,6,4,2): no equation of D_4 and no
separating equation from this lambda. With both candidates closed: among five-row partitions of 24 with lambda_1 = 6, degree 6
contributes nothing to I(D_4). Still open at degree 6: five-row partitions with lambda_1 > 6 and partitions with more than five rows.

## Tableau and network
50 semistandard isobaric tableaux exist; the cheapest by a-priori bound is nonzero on a random tensor and was used:

    1 1 1 1 2 2
    2 2 3 3 3 3
    4 4 4 4
    5 5 5 5
    6 6 6 6

Columns (symbols top to bottom): [1,2,4,5,6] [1,2,4,5,6] [1,3,4,5,6] [1,3,4,5,6] [2,3] [2,3]; heights 5,5,5,5,2,2; every column has
distinct symbols; column tensors have 120,120,120,120,2,2 nonzero entries. Literal sum: 5!^4 2!^2 = 829,440,000 terms.

## Performance (measured)
| engine | column order | transitions | states after each column | peak | time per evaluation |
|---|---|---|---|---|---|
| merged states (`hwv_dp.evaluate`, validated in the first certificate) | (3,1,0,2,4,5) | 43,644,220 | 120, 11 010, 352 560, 225, 425, 1 | 352 560 | 57 s |
| + twin-colour merging (`sym.evaluate_sym`) | same | 1,488,798 | 5, 545, 13 765, 225, 425, 1 | 13 765 | 3 s |
| literal sum in C (`literal.c`) | — | 829,440,000 terms | — | — | 88 s |
| monomial expansion in C (`expand.c`) | — | 829,440,000 terms | — | 129 616 monomials | 84 s |
Pure Python, exact integers. Peak memory of the whole certificate run: 220 MB.
For comparison, twin merging on the first candidate: 3,320,118 -> 293,250 transitions, peak 26,864 -> 4,227, 4.5 s -> 0.8 s;
on the control (4^5), d=5: 19,124,520 -> 135,840 transitions.

## Twin-colour lemma (new, used only for the faster engine; `sym.py`)
If two symbols occupy exactly the same set of columns, exchanging their partial multisets in a partial assignment multiplies the
sum over all completions by (-1)^r, r = number of their common columns still unprocessed (exchange the two values in each such
column: one transposition per column, same final multisets). Hence states can be stored with twin multisets sorted, and a state
with two equal twin multisets and r odd contributes 0. Corollary: if a tableau has two symbols in exactly the same columns and the
form degree c is odd, its polynomial is identically zero. Tested: `evaluate_sym` equals `evaluate` on 13 tableaux of 7 shapes.
Here the twins are {1,4,5,6} (all four height-5 columns); in the first tableau {1,4,6} and {2,5}.

## Validation
- Exact expansion: 129,616 nonzero monomials (weight space 133,366), all of weight lambda; R_k P_T = 0 exactly for k = 1..4
  (122,318 / 96,084 / 114,058 / 114,058 monomials touched, every coefficient cancels). Stored in `P_66444_monomials.json`.
- Monomial form = contraction on a random tensor; generic value -47259365424; Veronese P(l^4) = 0.
- Tensor 24*F equals the fourth partial derivatives on all 70 index multisets, for the det and the perm section k=0.

## Witnesses (same deterministic sections as in the first certificate)
det_4: all four sections nonzero. k=0: P(24F) = -1367122445633475772416 exactly. Identical modulo p = 2305843009213693967 (= 242458830244750015) from the
contraction run mod p, the stored monomial form and the exact integer; identical modulo 2147483647 (= 1210041570) from the literal
829,440,000-term sum in C. The twin-merging engine returns the same integer. k=1: 54763449225221936640, k=2: 14193491044892479488, k=3: 2296387253838099684864.
l*perm_3, k=0: -3327819268605124608 (mod p: 1283866749822263326, same three-way and C agreement). k=1: -155182123591262208, k=2: 6113910707509248, k=3: 470788311517558272.
All sections k=0..3 are in `cert_66444.json`.

## Comparison of the two constructions (observations, not theorems)
- Both partitions have all parts even and both chosen tableaux are column-doubled: each column occurs twice (A,A,B,B,C,C).
- Both highest weight functions are nonzero on det_4 AND on l*perm_3, so neither separates.
- Tried as a possible common witness: forms l*(a1 a2 a3 + b1 b2 b3), which lie in both orbit closures (det and perm of
  [[a1,b1,0],[0,a2,b2],[b3,0,a3]] coincide). Both functions gave 0 on two such forms each, and 0 on products of four linear forms
  (the latter must vanish: at most four essential variables). So this simple common subvariety explains neither nonvanishing;
  no vanishing statement is claimed for the first family from two samples.
