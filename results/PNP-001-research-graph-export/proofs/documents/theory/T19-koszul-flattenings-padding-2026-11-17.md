# T19 — Koszul flattenings in the padded model: reduction, a cubic cap for partial derivatives, and a failed cap (PI, 2026-11-17)

STATUS: PAUSED 2026-11-17 by the Hypothesis Gate (NO ASYMPTOTIC LEVER: the target is a no-go, not a route to ω(m³)). Lemma K proved and checked numerically; Proposition R proved (uses Reznick's theorem as stated by
Gesmundo–Landsberg); Section 3 is a documented FALSIFICATION of one proof route; Section 4 data partial (run stopped at the pause). No review yet.
Question (from T18): is the one numerical family not yet classified — Koszul/Young flattenings of the padded permanent — padding
robust (property P), or capped like everything else?

## Definitions
f ∈ S^n W, W = C^N. Koszul flattening KF_{p,a}(f): Λ^p W ⊗ S^a W* -> Λ^{p+1} W ⊗ S^{n-a-1} W, ω ⊗ D -> Σ_i (ω ∧ e_i) ⊗ ∂_i(D f).
Its image is the image of the de Rham differential d on Λ^p W ⊗ P_a(f), P_a(f) = span of the a-th partials of f.
Ranks are lower semicontinuous and do not increase under linear substitution, so rank KF(g) <= rank KF(det_n) for every g ∈ D_n.
Duality: rank KF_{p,a}(f) = rank KF_{N-1-p, n-1-a}(f).

## Lemma K (padding decomposition)
If f involves only the variables of a subspace E (dim e) — e.g. f = z^{n-m} g with E = <z> + span of g's variables — then
    rank KF_{p,a}(f) = Σ_q C(N-e, p-q) · rank KF^E_{q,a}(f),
where KF^E is the Koszul flattening computed inside E. Proof: W = E ⊕ C; Λ^p W = ⊕_q Λ^{p-q} C ⊗ Λ^q E; since every h ∈ P_a(f)
lies in C[E], d(η ⊗ ω ⊗ h) = ±η ⊗ d_E(ω ⊗ h); the map is block diagonal with C(N-e, p-q) copies of d_E on Λ^q E ⊗ P_a(f). ∎
Checked against direct computation in 30 cases (N = 6, e = 4, n = 5, all p, a; `checks/t19/check_decomp.py`).
Consequence (cap lemma of T18, specialised): if some ψ of degree m in m² variables has r_q(z^{n-m}ψ) >= r_q(z^{n-m}per_m) for all
q, a (ranks inside E), then for every p no Koszul flattening separates z^{n-m}per_m from D_n whenever border dc(ψ) <= n.

## Proposition R (cubic cap for partial-derivative dimensions)
P_a(z^{n-m}ψ) = ⊕_j z^{n-m-a+j} P_j(ψ) (j between max(0, a-n+m) and min(a, m)), a direct sum by z-degree, so
dim P_a(z^{n-m}ψ) = Σ_j dim P_j(ψ). Reznick's forms φ_m = (Σ x_i²)^{m/2} (m even) or (Σ x_i)(Σ x_i²)^{(m-1)/2} (m odd) have maximal
dim P_j for every j (Gesmundo–Landsberg, Thms 2.2/2.5), hence dim P_a(z^{n-m}φ_m) >= dim P_a(z^{n-m}per_m) for all a, n.
dc(φ_m) <= 1 + ((m-1)/2 or m/2) · dc(Σ_{i<=m²} x_i²) = O(m³) (block-diagonal powers). By the cap lemma, any argument that uses only
the dimensions of the partial-derivative spaces of the padded permanent certifies at most dc(φ_m) = O(m³). (Shifted partials are
already capped at O(m²) by ELSW; this covers all invariants that are functions of the sequence dim P_a.)

## Section 3 — FALSIFIED route: the Reznick form does not cap Koszul flattenings
m = 3, e = 10, n = 4, a = 1, q = 3: r_q(z·per_3) = 1155 = r_q(z·generic cubic) > r_q(z·φ_3) = 1120 (`checks/t19/compare_m3.py`,
partial output `compare_m3_partial.out`). Partial-derivative dimensions agree there; the difference is in the Koszul structure.
So Proposition R does not extend to Koszul flattenings via φ_m. (This is the open Question 6.7 of Gesmundo–Landsberg in a
padded setting: Koszul ranks of explicit maximal-partials forms are not maximal.)

## Section 4 — which easy forms dominate per_3 in every Koszul slot? (computing)
`checks/t19/compare_m3b.py`: r_q(z^{n-3}ψ), q <= 4, all a, n = 4, 5, for ψ ∈ {per_3, φ_3, det_3, sum of 2 or 3 random products of
linear forms, generic cubic}. If det_3 (dc 3) dominates per_3 in all slots, Koszul flattenings cannot separate z^{n-3}per_3 from
D_n at those n — strictly weaker than LMR at (3,4).
Partial data at the pause (`compare_m3b.out`, `compare_m3c.out`, 66 slots: n = 4 complete, n = 5 a <= 1 (partial), n = 6 complete,
n = 7 a <= 1 (partial)): r_q(z^{n-3}det_3) >= r_q(z^{n-3}per_3) in every computed slot; equality everywhere except n=6, a=4, q=4
(per 2194 < det 2210). per_3 never exceeded det_3. phi_3 and sums of 2 or 3 products of linear forms fall below per_3 in many slots.
Unproved beyond these slots; no conclusion drawn.
