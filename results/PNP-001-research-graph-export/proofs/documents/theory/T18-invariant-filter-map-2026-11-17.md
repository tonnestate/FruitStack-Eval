# T18 — Which invariants could go past the cubic order? A three-property filter (PI, 2026-11-17)

STATUS: working map. The lemma is elementary (proved below); the table cites T10/T15/T16/T17 and the literature.
Nothing here is a new lower bound. Purpose: decide where research effort can still change the exponent.

## Lemma (monotone-invariant cap; general form of arXiv:2606.15970 Remark 7.13)
Let I be a real invariant of forms and B a nondecreasing function with I(g) <= B(n) whenever border dc(g) <= n. An argument
"I(f) > B(n) => border dc(f) > n" certifies at most n* = max{n : B(n) < I(f)}, and
    n* < min{ border dc(g) : g of the same degree and number of variables, I(g) >= I(f) }.
Proof: if I(g) >= I(f) then B(border dc(g)) >= I(g) >= I(f) > B(n*), so border dc(g) > n*. ∎
For f = per_m (degree m, m² variables): if a Fermat form x_1^m + ... + x_{m²}^m (formula size O(m³), so dc = O(m³)) or any other
form of dc O(m³) has I >= I(per_m), the argument is capped at O(m³).

## Three properties an invariant needs to beat cubic in the padded model
(P) padding robust: comparable between z^{n-m} per_m and det_n in degree n (e.g. depends only on multiplicity-one components);
(M) controlled on all of D_n (bound B(n) valid for limits, not only for the orbit);
(F) not (nearly) maximised by any form of determinantal complexity O(m³) of degree m in m² variables (Lemma above).

| Family | P | M | F | Status / evidence |
|---|---|---|---|---|
| Polar degrees, Chern–Mather / CSM / Milnor classes, read through corank-1 kernel systems (cubic preprint, Sheshadri) | yes | yes | NO — Fermat attains the maximum d(d-1)^(N-2) | capped O(m³): arXiv:2606.15970 Thm 7.7 / Cor 7.11; T15 Bezout cap ~0.11 m³ |
| Second-order point counts (Hessian minor conditions) | yes | not established | NO — Fermat attains Bezout in 4 tested cases (`checks/t15/fermat_filter.m2`) | T15 H1 refuted as a route |
| Hilbert function of the dual variety | yes | yes (T16 Lemma D) | — | capped at (m²+1)/2: T16 Theorem C (review pending) |
| Regularity of the dual | ? | no relation known | ? | T16 §4: unresolved, nothing may be inferred |
| Hessian rank / dual dimension (Mignon–Ressayre, LMR) | yes | yes | — | quadratic m²/2 |
| Shifted partials / Jacobian-ideal Hilbert function | NO | yes | yes (power sums have small derivative spaces) | capped O(m²) by ELSW arXiv:1609.02103; Hilbert functions arXiv:1504.05171 |
| Iterated-matrix Koszul flattenings, unpadded model | — | yes | yes | no-go: Gesmundo–Landsberg (Theory of Computing 15, 2019) |
| General Young / Koszul flattenings, padded model | UNKNOWN | yes (rank is lower semicontinuous) | yes (rank bounded by border Waring rank, small for power sums) | OPEN — ELSW explicitly leave it open; nothing newer found |
| Singular-locus invariants (codim Sing etc.) | partly | NO — limits only enlarge singular loci (l^n ∈ D_n) | yes | exact dc only (Alper–Bogart–Velasco), linear for per_m |
| GCT multiplicities / separating equations (T11) | yes | yes | not numeric | no small-case separator found up to degree 6 at (3,4); occurrence obstructions dead (BIP) |

## Consequence
Every family with a known status fails at least one of P, M, F, or is non-numerical (GCT). The only numerical family not yet
classified is general Young/Koszul flattenings in the padded model, where (P) is the open question.
Next investigation (T19): padding behaviour of Koszul flattenings — compare ranks of Koszul flattenings of z^{n-m} g and det_n as n
grows for fixed g, first numerically for small parameters to find the trend, then attempt an ELSW-style comparison proof.
