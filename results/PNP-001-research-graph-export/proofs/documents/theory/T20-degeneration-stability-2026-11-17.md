# T20 — Degeneration stability of dual and conormal data (main question, flank 1/2) (PI, 2026-11-17)

STATUS: REVIEWED 2026-11-17 (same independent reviewer as T16, script /tmp/claude-0/review_t16/t20.m2): §1-§3 no flaw after the
fixes below; the reason originally given in §4 was wrong and is replaced (conclusion unchanged). No expensive computation was run; the only computation is the n = 2,3,4 check in §1.
Main question (ACTIVE-MISSION.md): is there a scheme-theoretic dual/conormal invariant with controlled behaviour under determinant
degenerations that beats polar counting?

## Hypothesis Gate
| Field | Entry |
|---|---|
| HYPOTHESIS | Scheme-theoretic data of the dual (H1) or of the conormal variety (H2) of a multiplicity-one component of z^{n-m}per_m obey a degeneration comparison with det_n strong enough to exclude n = ω(m³). |
| ASYMPTOTIC TARGET | border dc(per_m) = ω(m³). |
| NEW INFORMATION | Beyond polar degrees (cycle classes): Hilbert functions, syzygies, regularity, multiplicities, local structure of limits. |
| BORDER VALIDITY | Lemma D (T16) for duals; Lemma D'' (below) for conormals. |
| CHEAP FALSIFICATION | Theorem C' (below) — a universal degeneration of the Segre. |
| COMPUTATION | none needed beyond §1. |
| DECISION | H1: REFUTED (no asymptotic lever: no containment-derived invariant excludes any n >= (m²+1)/2; best certifiable floor(m²/2)+1). H2: PROCEED analytically only, open obligation O1. |

## §1 Theorem C' (dual containment carries no information beyond (m²+1)/2)
Let Seg ⊂ P^{N-1∨} (N = n²) be the rank-<=1 locus, the dual of the determinant hypersurface.
(a) Under a diagonal term order, in(I(Seg)) is the squarefree Stanley–Reisner ideal of the staircase triangulation; V(in I) is the
    union of C(2n-2, n-1) coordinate linear spaces of dimension 2n-2. It is the flat limit t -> 0 of the torus translates t^{-w}·Seg.
    (Classical: 2x2 minors are a Gröbner basis. Checked for n = 2,3,4 in `checks/t15/segre_groebner.m2`: squarefree, 2/6/20
    components, all of projective dimension 2n-2, Hilbert polynomial preserved.)
(b) Hence for every subvariety Y ⊂ P^{N-1∨} whose linear span has dimension <= 2n-2 there is g ∈ GL_N with Y ⊂ g·V(in I), and
    g·V(in I) is the flat limit of the GL-translates g t^{-w}·Seg.
(c) The dual of the cone over V(per_m) spans exactly the (m²-1)-plane Λ of hyperplanes through the vertex (per_m is concise, so its
    hypersurface is not a cone and its dual is nondegenerate in Λ). So for n >= (m²+1)/2 it lies in a flat limit of GL-translates of Seg.
Consequence. Any obstruction whose only input is "the dual of a multiplicity-one component of f_0 lies in some flat limit of
GL-translates of the Segre" — the information Lemma D provides — cannot certify border dc(per_m) > n for n >= (m²+1)/2. For the
Hilbert function (the containment-monotone datum) this is T16 Theorem C. Betti numbers, syzygies and regularity are not monotone
under containment (and the Gröbner limit already differs from Seg in its syzygies: n = 3 has extra β_{2,4} = 1, β_{3,5} = 2,
β_{4,5} = 2, same regularity 2), so a containment-only argument cannot use them at all. It also explains Borovik–Briand's warning concretely: limits of duals can acquire large extra components, and those
components (here: big linear spaces) are exactly what swallows any dual of dimension <= 2n-2.
Flank 1, dual side: CLOSED at quadratic. Not covered: arguments that use more of the degeneration than containment of the dual.

## §2 Lemma D'' (conormal varieties: the dimension matches)
For a reduced hypersurface X, Con(X) ⊂ P^{N-1} x P^{N-1∨} is the closure of {(p, T_pX)}; dim Con(X) = N-2 for EVERY hypersurface.
Let f_0 ∈ D_n, V a multiplicity-one component of V(f_0). By the curve selection lemma choose a curve in GL·det_n converging to f_0;
along it, the flat limit L of
Con(g_s·det_n) contains Con(V) (same implicit-function argument as Lemma D, at the points (p, [∇f_0(p)]), u(p) ≠ 0), and L is pure of
dimension N-2. Hence Con(V) is an irreducible COMPONENT of L, not merely a subvariety. Consequences:
- cycle level: [L] = [Con(det_n)], all components effective, so polar degrees satisfy δ_i(V) <= δ_i(det_n) slotwise;
- scheme level: with J the bidegree-wise limit ideal, I(Con V) ⊇ I(L_red) ⊇ J and H_J = H_{Con(det_n)}, so
  H_{Con(V)}(a,b) <= H_{Con(det_n)}(a,b) (Lemma D').
This is why polar-degree methods reach cubic while dual-dimension (LMR) and dual-containment methods stop at quadratic: projecting
the conormal to the dual loses the dimension match.

## §3 Proposition Q (the cycle level contains nothing beyond polar domination)
The class-level necessary condition "there is an effective Lagrangian cycle Σ c_i [Con(Z_i)] of class [Con(det_n)] with Z_1 = V,
c_1 >= 1" is equivalent to δ(V) <= δ(det_n) slotwise. Proof: necessity from effectivity; sufficiency at class level because the
conormal of a linear space P^k is P^k x P^{N-2-k}, whose class is the unit vector of slot k, so every nonnegative difference vector is
a sum of such classes. (This says nothing about realisability of the cycle as an actual limit.)
So everything numerical at the cycle level is polar-degree domination — the class covered by arXiv:2606.15970 Thm 7.7 and capped
at O(m³) (T15). Flank 2 is the same object: the kernel incidence {(ξ, u, v): A(ξ)u = 0, vᵀA(ξ) = 0} of the cubic preprint's
Prop. 8.3 is the conormal correspondence of det_n (Con(det_n) = {(X, u vᵀ) : Xu = 0, vᵀX = 0} up to the transpose convention; a
bundle over P^{n-1} x P^{n-1} with fibres P^{(n-1)²-1}, irreducible of dimension N-2). For a non-surjective A(ξ) the kernel incidence
is the pullback of this incidence, related to Con(det∘A) by a correspondence, not equal to it.

## §4 Open obligation O1 (the precise remaining gap of the main question)
Find an invariant I of an irreducible component C of a flat limit of GL_N-translates of Con(det_n) such that
  (i) I(C) <= B(n) for every such component (border validity), with I not determined by the class [C];
  (ii) I(Con(cone over V(per_m))) > B(n) for some n = ω(m³);
  (iii) I is not (nearly) maximised by conormals of forms of small dc (Fermat filter, T18).
Known facts constraining O1:
- The vacuity trick of Theorem C' does not transfer, because conormal containment is component-level (Lemma D''): Con(V) must be a
  whole (N-2)-dimensional component of the limit and cannot be absorbed into a large linear component as the dual is in §1. So O1 is
  genuinely open, not closed by §1. (Correction after review: an earlier reason — that the permanent cone is not torus-invariant — was
  false: per(D1 X D2) = det D1 det D2 per X, a (2m-2)-dimensional torus in PGL plus padding scalings; checked for m = 3.)
- Candidates for I: the bigraded Hilbert function in the mid range (leading terms are polar degrees), the multiplicity of C in L,
  the local length of L along C. For each, (i) needs an upper bound valid for all limits; none is known to us.
Next step (analytic, no computation): test candidate (i)-bounds on the simplest non-torus degenerations of Con(det_3) (e.g. the
boundary components of the det_3 orbit, Hüttenhain–Lairez), before any computation on the permanent side.

## §5 Side flank: boson/fermion interference (owner, theoretical only)
Gate: HYPOTHESIS — a property of fermionic (antisymmetric, Gaussian) interference preserved by poly-size determinantal
representations and their limits, violated by per_m. BORDER VALIDITY — BLOCKED: every polynomial with a small algebraic branching
program is an affine projection of a small determinant, and linear projections do not preserve Gaussianity of the projected
polynomial; a property preserved under all projections of det_n and their limits is a property of D_n itself, i.e. an orbit-closure
invariant — this is GCT again, not a new transfer. Checked fact (owner's computation, agrees with T13): for the k|n-k cut the
Schmidt rank of both the symmetric (permanent) and antisymmetric (determinant) states is C(n,k); ordinary entanglement does not
separate. DECISION: BLOCKED until an explicit candidate property is named; no simulation.
