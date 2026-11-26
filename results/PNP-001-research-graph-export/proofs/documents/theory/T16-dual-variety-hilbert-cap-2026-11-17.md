# T16 — Dual-variety invariants and determinant degenerations: a rigorous link, and why it stops at m²/2 (PI, 2026-11-17)

STATUS: REVIEWED (independent adversarial review 2026-11-17, /tmp/claude-0/review_t16/): Lemma D no flaw; Theorem C algebra correct,
headline corrected by one (below); no counterexample in 5 computed cases (det_3, two boundary points of D_3, a D_5 point, a D_4 point).
Question (owner, item 1 of the autonomous mandate): do Hilbert-function or regularity invariants of the dual variety have a
RIGOROUS relationship to determinant degenerations, before anything is inferred from numerical differences?
Answer: Hilbert function — yes (Lemma D), but the resulting obstruction provably cannot certify border dc(per_m) >= (m²+1)/2
(Theorem C): it cannot exclude any n >= (m²+1)/2, so the best it can certify is border dc(per_m) >= floor(m²/2)+1 —
equal to LMR for odd m, +1 over LMR for even m. Regularity — no usable relationship (Section 4). Route closed.

## Setup
N = n², W = C^N, D_n = closure of GL_N · det_n in Sym^n W. For a reduced hypersurface V ⊂ P^{N-1}, V^∨ ⊂ P^{N-1∨} is the closure of
the tangent hyperplanes at smooth points. For f = g·det_n (g in GL_N), V(f)^∨ is projectively equivalent to the rank-<=1 locus
Seg = P^{n-1} x P^{n-1}, with Hilbert function H_Seg(t) = C(n-1+t, t)^2 (coordinate ring of rank-<=1 matrices).

## Lemma D (Hilbert function of duals under determinant degeneration)
Let f_0 ∈ D_n and let V = V(h) with h an irreducible factor of f_0 of multiplicity one (f_0 = h·u, h ∤ u). Then for every t >= 0
    dim I(V^∨)_t >= dim I(Seg)_t,   equivalently   H_{V^∨}(t) <= C(n-1+t, t)^2.

Proof. Orbit closures are Euclidean closures, so f_0 = lim f_s with f_s = g_s·det_n, g_s ∈ GL_N. Put X_s = V(f_s); X_s^∨ = g_s^{-T}·Seg,
so dim I(X_s^∨)_t = dim I(Seg)_t =: e for all s. Fix t. The Grassmannian Gr(e, Sym^t W) is compact; pass to a subsequence with
I(X_s^∨)_t -> J_t. Every element of J_t is a limit of elements h_s ∈ I(X_s^∨)_t.
Points: let p ∈ V be a smooth point of V not on V(u); such p are dense in V, and their tangent hyperplanes are dense in V^∨.
Then f_0(p) = 0 and ∇f_0(p) = u(p)∇h(p) ≠ 0. By the implicit function theorem, for s large there are p_s -> p with f_s(p_s) = 0 and
∇f_s(p_s) -> ∇f_0(p) ≠ 0; p_s is a smooth point of X_s (reduced), so y_s := [∇f_s(p_s)] ∈ X_s^∨ and y_s -> y := [∇f_0(p)] = T_pV.
For j ∈ J_t, j = lim h_s, so j(y) = lim h_s(y_s) = 0 (joint continuity; normalised representatives). Hence J_t vanishes on a dense
subset of V^∨, so J_t ⊆ I(V^∨)_t and dim I(V^∨)_t >= e. ∎
Remarks. (i) Only multiplicity-one components are controlled; e.g. the padding hyperplane z = 0 of z^{n-m}per_m is not.
(ii) The proof gives more than dimensions: I(V^∨)_t contains a point of the GL-orbit closure of I(Seg)_t in the Grassmannian.
(iii) Lemma D contains the LMR dimension argument: Hilbert polynomials give dim V^∨ <= 2n-2.

## Application to the padded permanent
f_0 = z^{n-m} per_m; V = cone over V(per_m) (per_m irreducible, multiplicity one; generic points have z ≠ 0).
V^∨ = (V(per_m) ⊂ P^{m²-1})^∨ embedded linearly in the hyperplanes through the vertex; Hilbert function unchanged by the embedding.
Obstruction: if H_{V(per_m)^∨}(t) > C(n-1+t, t)^2 for some t, then z^{n-m}per_m ∉ D_n, i.e. border dc(per_m) > n.

## Theorem C (the obstruction is capped at quadratic)
For n >= (m²+1)/2, H_{V^∨}(t) <= C(n-1+t,t)^2 for ALL t and for EVERY subvariety V^∨ of P^{m²-1}. Hence the Lemma-D obstruction
cannot exclude any n >= (m²+1)/2, whatever the dual of the permanent turns out to be; the best certifiable bound is
floor(m²/2)+1. (Correction after review: an earlier wording claimed it can never certify (m²+1)/2; for odd m it does,
e.g. m=3, n=4: dim V(per_3)^dual = 7 > 6 = 2n-2 gives border dc(per_3) >= 5.)
Proof. H_{V^∨}(t) <= C(a+t, t) with a = m²-1 (ambient). For real x >= 0, C(x+t,t) = prod_{i=1..t} (x+i)/i is increasing in x, and
    C(a/2+t, t)^2 / C(a+t, t) = prod_{i=1..t} (a/2+i)^2 / (i(a+i)) >= 1,   since (a/2+i)^2 - i(a+i) = a²/4 >= 0.
With n-1 >= a/2: C(n-1+t,t)^2 >= C(a/2+t,t)^2 >= C(a+t,t) >= H_{V^∨}(t). ∎
Checked numerically with exact rationals for a ∈ [0,200) in steps 1/2, t < 60 (`dual_hilbert_cap.py`, part 1).
Room left below the cap: only at the dimension boundary 2n-2 = m²-2 (m even, n = m²/2) can H_{V(per_m)^∨}(t) exceed H_Seg(t)
for some finite t (not only asymptotically via the degree) and exclude one more value of n than LMR. At most +1 over LMR; not pursued.

## Section 4 — regularity: no usable relationship
Lemma D yields a containment V^∨ ⊆ V(J) with J a degeneration of the Segre ideal. Castelnuovo–Mumford regularity is not monotone
under containment (a degree-D hypersurface inside a linear space has regularity D, the linear space 1), and no bound on the
regularity of V(f)^∨ for f ∈ D_n in terms of n alone is known to us. Without such a bound no inequality "reg small for dc <= n"
exists, so nothing may be inferred from regularity values. Recorded as an UNRESOLVED OBSTRUCTION (no theorem relates them), not as
evidence in either direction.

## Consequence for the research map
The "scheme-theoretic invariants of the dual" gap left by the ceiling of arXiv:2606.15970 (its Remark 7.14) is closed for the
Hilbert function at the quadratic level by Theorem C. What survives of the dual-variety route is the non-numerical containment of
Remark (ii): I(V^∨) must contain a degeneration of the 2x2-minor ideal. That is an orbit-closure containment problem for ideals,
i.e. a GCT-type question again, not a new numerical invariant.
