# T15 — First audit of the cubic border bound and of what limits it (PI, 2026-11-17)

Object: OpenAI preprint dated 2026-09-24, "A cubic lower bound for border determinantal complexity of the permanent"
(github.com/openai/math, CONTENTS.md entry 108). Read from the PDF text; local copy in the session scratchpad.
STATUS: first pass. Sections 2, 8, 9 read and partly tested; Sections 3–7 (the construction of the smooth form) NOT audited;
the Lean files not compiled. Nothing here is in the ledger beyond entry 215 (EXTERNAL_UNAUDITED_BENCHMARK).

## 1. The proof chain as read
1. Prop. 2.2: coefficientwise limits of n x n affine determinants = padded orbit-closure model.
2. Thm 2.3: a smooth form G of degree r in d variables has border dc(G) >= (r-1)(d-1)/(4e).
   Mechanism (Prop. 8.3): if P is a limit of n x n affine determinants and the system {P = 0, h first polars = 0} on an affine
   (h+1)-space has mu distinct simple zeros, then the zeros persist for one nearby determinant, lift to left/right kernel lines,
   and a multihomogeneous Bezout count gives
       mu <= K(n,h) := [H^(h+1) U^(n-1) V^(n-1)] (H+U)^n (H+V)^(n-1) (U+V)^h <= 2^h C(2n-1, h+1).
   For smooth G: mu = r(r-1)^(d-2) at h = d-2.
3. Prop. 7.3 (not audited here): for k >= 128 there is a smooth form G of degree r >= k/4+1 in d >= k^2/200+1 variables with
   G = per_m composed with an affine map, for all m >= 11k - 2q. Built from a coefficient of per_k(X + sI + tD) and a
   characteristic-2 plane-curve argument, then transferred to characteristic 0.
4. Hence border dc(per_m) >= (r-1)(d-1)/(4e) >= k^3/(3200e) >= m^3/(5 529 600 e) for m >= 1408.

## 2. What was checked here (`checks/t15/polar_count.py`, `polar_degrees.m2`)
- Closed form K(n,h) = sum_{a+b=h+1} C(n,a) C(n-1,b) C(h,b); equals the expansion for n <= 5; K <= 2^h C(2n-1,h+1);
  K(n,h) = 0 exactly when h+1 > 2n-1 (checked n <= 7).
- The inequality on real data, with polar degrees computed by Macaulay2 (Cremona `projectiveDegrees`, over Z/32003,
  probabilistic): for the hypersurface det_3 = 0 in P^8, mu_h = 3, 6, 12, 12, 6, 0, 0, 0 (h = 0..7) against
  K(3,h) = 3, 9, 16, 15, 6, 0, 0, 0. The inequality holds for every h and is an EQUALITY at the top (h = 4) and at the vanishing
  threshold. So on the determinant side this count has no slack to give away.
- For per_3 = 0 in P^8: mu_h = 3, 6, 12, 24, 48, 48, 30, 6. Against K(4,h) = 4, 18, 52, 95, 108, 70, 20, 0 this excludes n = 4
  (h = 6: 30 > 20; h = 7: 6 > 0). Against K(5,h) = 5, 30, 120, 325, 606, 770, 640, 315 nothing is excluded. So the polar count,
  applied to per_3 itself with its true polar degrees, gives border dc(per_3) >= 5 — the same as the quadratic bound, not more.
  Consistent with the known z*per_3 not in D_4; no contradiction with dc(per_3) = 7.

- Scope of these two tests (owner's caveat, correct): det_3 = 0 and per_3 = 0 are SINGULAR hypersurfaces, so they test Prop. 8.3
  (which assumes only simple zeros of the polar system), not the smoothness hypothesis of Thm 2.3.
- Thm 2.3 on an explicit smooth form (`interface.m2`, part A): a random 4-variable linear section of det_3 over Z/32003 is a smooth
  cubic surface (Jacobian ideal supported at the origin) with polar degrees 3, 6, 12 = r(r-1)^h, against K(3,h) = 3, 9, 16.
  For sections of det_n in at most 4 variables one has in general K(n,2) = n(n-1)^2 + C(n,3) + n(n-1)(n-2)/2 >= n(n-1)^2.
  These are consistency checks only: a smooth form with a determinantal representation of its own degree has at most 4 variables,
  so no small example can put the inequality under real stress.

## 3. Relation to the quadratic bound
K(n,h) vanishes iff h+1 > 2n-1. Using only THAT (some polar degree of per_m with h+1 = m^2-1 is nonzero) gives n >= m^2/2: the
Mignon–Ressayre / LMR bound is the vanishing threshold of the same count (the dual of the determinant hypersurface is the rank-one
locus, of dimension 2n-2). The cubic bound uses the SIZE of a polar degree instead of its nonvanishing.

## 4. Bottlenecks
B1. Hard cap by Bezout (elementary, proved here). For any affine restriction of per_m, a system {P = 0, h first polars = 0} on an
    affine (h+1)-space has at most m(m-1)^h isolated simple zeros, and h <= m^2-2 (for h+1 >= m^2 the zeros of the homogeneous
    system are not simple). So Prop. 8.3 can never exclude an n with K(n,h) >= m(m-1)^h for all h <= m^2-2. Largest n it could
    exclude even if Bezout were attained:

        m          3    4    5    6    7    8    9    10    11    12
        cap        5   10   17   28   43   61   85   113   148   189
        m^2/2     4.5   8  12.5  18  24.5  32  40.5   50   60.5   72
        Grenet     7   15   31   63  127  255  511  1023  2047  4095

    cap/m^3 is about 0.11 at m = 12. Whatever is done on the permanent side, first-polar counts stop at cubic order. The preprint's
    constant 1/(5 529 600 e) ~ 6.7e-8 is far below this cap, so the CONSTANT can improve by many orders of magnitude; the EXPONENT
    cannot, with this invariant. (Independent of, and much cruder than, the method ceiling of arXiv:2606.15970 Cor. 7.11.)
B2. Singularities. The cap is not attained by per_m itself: for per_3 the top polar degree is 6, not 384. codim Sing(per_m) <= 2m
    limits smooth linear sections of per_m to O(m) variables, which is why the preprint replaces per_m by a coefficient polynomial
    with smooth sections in ~k^2/100 variables at the price m >= 11k.
B3. No slack on the determinant side (equality for det_3 above).

## 5. Where an exponent above 3 would have to come from (HYPOTHESES, nothing verified)
H1. Second-order conditions. Counts of points where, in addition to first polars, minors of the Hessian restricted to a subspace
    vanish have Bezout numbers with factors of size ~ w(m-2) instead of m-1. Needed: a determinant-side lift of such conditions
    to kernel data with a controlled multidegree count. Obstacle to check first: the Hessian of det_n has rank <= 2n everywhere on
    the hypersurface, so many such conditions are automatically satisfied there and count nothing.
    TESTED 2026-11-17 (`fermat_filter.m2`): the count {f = 0, N-3 general first polars = 0, det(Hess f | W) = 0} attains its
    Bezout number d(d-1)^(N-3) w(d-2) with reduced points on the Fermat form sum x_i^d, exactly as on a random form, in the cases
    (N,d,w) = (4,3,2), (4,4,2), (5,3,2), (5,3,3). The Fermat form has determinantal complexity O(dN) (formula of size O(dN)).
    So this second-order count falls under the same barrier as the top polar degree (arXiv:2606.15970, Remark 7.13): an argument
    "count(f) > max of the count over forms of dc <= n" cannot certify more than dc(Fermat) = O(dN), i.e. O(m^3) for per_m.
    H1 in this form is therefore NOT a route past cubic. (Four parameter cases, not a general proof that Fermat attains Bezout.)
H2. Any invariant equivalent to polar degrees (Chern–Mather / CSM classes of the hypersurface) inherits B1. So "more refined
    first-order characteristic classes" is not a route.
H3. Constant improvement inside the method: better smooth sections (larger d relative to m^2, r closer to m). Worth doing only
    as a calibration of the method, not as a route past cubic.

## 6. What the ceiling of arXiv:2606.15970 covers (read: Def. 7.1, 7.5, Thm 7.7, Rem. 7.8, 7.13, 7.14)
- Covered: every Z-linear combination of "profile numbers" (aggregated multidegrees of the characteristic cycles of 1_X, Eu_X and
  the Milnor function; includes all polar degrees, Chern–Mather, CSM and Milnor class degrees) read through corank-one kernel
  systems with a count bound uniform over all matrices of a given size. Result: at most 3K dN, K = max(48, 7 C_nu).
- Not complete: corank >= 2 (Rem. 7.8); one constant conditional (Rem. 6.9).
- Explicitly outside (Rem. 7.14): scheme-theoretic invariants of the conormal or dual variety (Hilbert function, regularity of
  the dual), and mechanisms that do not factor through solution counts of kernel systems.
- Rem. 7.13 gives the simplest form of the barrier, independent of kernel systems: the Fermat form has the maximal top polar
  degree d(d-1)^(N-2) and dc = O(dN).

## 7. Working criterion derived from this ("easy-maximiser filter")
A numerical invariant I can only support a bound beyond O(dN) if it is NOT (nearly) maximal on forms of small determinantal
complexity: Fermat forms / power sums, products of linear forms, small formulas. Checking a candidate on the Fermat form is a
cheap first test; point counts bounded by a Bezout number tend to fail it (Section 5, H1). Rank-type measures (partial
derivatives, shifted partials) pass this filter — the Fermat form has tiny derivative spaces — but for padded permanent vs
determinant they are capped at quadratic by ELSW (T10). So far every known family fails one of the two filters.

## 8. Next steps
- Audit Sections 3–7 (the construction of G), which carry all of the difficulty; or compile the Lean development.
- Started, not finished at the time of writing: polar degrees of per_4 = 0 in P^15 (`checks/t15/polar_degrees_4.m2` ->
  `polar_degrees_4.out`), and the largest smooth random section of the coefficient polynomial G_D for small (k,q)
  (`interface.m2` part B -> `interface.out`; so far only k=3, q=0, i.e. per_3 itself: smooth up to 6 variables).
- Candidates outside the ceiling's scope, per Rem. 7.14: Hilbert function / regularity of the dual variety of per_m versus that of
  the determinant (the dual of det_n = 0 is the rank-one locus, whose ideal and Hilbert function are completely known).
