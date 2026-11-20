# Theorem 12 — roABP-IPS_LIN lower bound for a doubly lifted colouring family (PNP-001, 2026-11-20)

Status: PROVED (paper proof), independently reviewed twice (sections 11 and 12 of ACC0-L3-REPORT.md: Lemma T, Lemma N; then the full
chain incl. Lemma O). Machine formalisation of Lemma N pending. Scope: roABP-IPS_LIN only; says nothing about stronger proof systems,
algorithms, or P vs NP.

## Statement
Let G_n be the Lauria-Nordstrom non-3-colourable graphs (arXiv 2306.00125, Thm 3.7: O(n) vertices of degree O(1)), F(G_n) the 3-CNF of
the 3-colouring translation into positive 1-in-3 (vertex clauses (x_v1,x_v2,x_v3), edge clauses (x_uc,x_wc,y_uwc), each 1-in-3 clause as
(a v b v c), (-a v -b), (-a v -c), (-b v -c)), g = h_{2^p - 1} (Pitassi-Robere Def. 4.1) on {0,1}^p x {0,1}^p with a constant p such that
2^p - 1 > 2^{1/eps}, phi_n = F(G_n) o g, and Psi_n the order lift of phi_n (Lemma O, selectors over K-tuples, K = 6p).
For every field F and every variable order, every roABP-IPS_LIN refutation of Psi_n over F has width 2^{Omega(n)}; Psi_n has poly(n) size.

## Proof (chain; full text in ACC0-L3-REPORT.md sections 11-12)
1. Lemma N (ours): deg_NS(Col(G)) <= deg_NS(F(G)) over every field (affine slack substitution; image axioms in the Boolean ideal plus
   multiples of x_uc x_wc, no degree increase). With Lauria-Nordstrom Thm 3.7 / Thm 1.1 (PC degree Omega(n), field-independent;
   NS >= PC): deg_NS(F(G_n)) >= eps * #vars(F(G_n)).
2. Lemma T (ours): a width-w roABP-IPS_LIN refutation of C o g with all x-bits before all y-bits gives an algebraic tiling of KW+(f_{C,g})
   of size <= w * m * 2^{k(p+q)} (cut rank <= w; clause indicators split as R(x) S(y); supports inside the canonical rectangles of PR18).
3. Pitassi-Robere STOC'18 Thm 1.1 / 3.4 / 3.5 / 2.4: for NS >= eps n and a good gadget of rank > 2^{1/eps}, chi_F >= mu_F >= 2^{Omega(n)};
   h_lambda is good over every field with rank lambda (Lemma 4.2). Hence width >= 2^{Omega(n)}/poly in the order sigma (x-bits first).
4. Lemma O (ours; TR26-070 Prop. 17 / Thm. 18 with tuples instead of triples): any order of Psi_n restricts, without width increase, to
   phi_n in sigma; Psi_n is unsatisfiable.

## Sources (local copies, not redistributed)
- Hakoniemi, Limaye, Tzameret, "Hard CNF Instances for Ideal Proof Systems", ECCC TR26-070 (2026): eq. (0.2), Thm 9, Sec. 4 (Def. 15/16,
  Prop. 17, Thm. 18), Sec. 5, Sec. 1.4.
- Pitassi, Robere, "Lifting Nullstellensatz to Monotone Span Programs over Any Field", STOC 2018 / ECCC TR17-165: Def. 2.1, 2.11, 3.1,
  4.1; Thm 1.1, 2.4, 3.4 (proof deferred to the full version), 3.5; Lemma 4.2.
- Lauria, Nordstrom, "Graph Colouring is Hard for Algorithms Based on Hilbert's Nullstellensatz and Groebner Bases", CCC 2017 /
  arXiv 2306.00125: Thm 1.1, encoding (2.2a)-(2.2c), Thm 3.7.

## Novelty (honest; sharpened 2026-11-20 after an external review)
The MAIN theorem of TR26-070 (Thm 1 / Thm 18) already gives exponential roABP-IPS_LIN lower bounds for an explicit CNF family, in every
variable order and over every field (GEN-based, via feasible interpolation). The degree route used here is remarked in TR26-070 Sec. 1.4
and attributed to Dmitry Sokolov. Our difference is therefore at most: a different explicit family (3-colouring / positive 1-in-3, via
Nullstellensatz degree instead of interpolation), the written proof of the degree lift (Lemma T), the instantiation (Lemma N), the
constant-width order lift (Lemma O), and constants. Any preprint must state it exactly so. Full (non-linear) roABP-IPS is not treated in
TR26-070; our partial results there are Theorem 14 and Lemma 15 (report sec. 14-15).

## Reproducibility
- rung4/order_lift_check.py: selector combinatorics of Lemma O (5 unsatisfiable CNFs, clause widths 1-4, 20 random orders each).
  A sanity check of the combinatorics, not of the polynomial identities.
- Reviews: ledger VERIFICATION entries of 2026-11-20 (Lemma T / Lemma N; Theorem 12).

## Caveats
Polynomial size of degree O(p) with p ~ 1/eps (Lauria-Nordstrom constants): astronomically large in practice. Pitassi-Robere Thm 3.4 is
used through its published statement.
