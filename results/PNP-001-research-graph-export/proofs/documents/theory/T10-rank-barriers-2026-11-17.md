# T10 — Weg 1: Shifted Partial Derivatives and the rank-method barriers (PI, 2026-11-17)

Goal: can a linear rank measure (shifted partial derivatives, SPD) break the polynomial ceiling for perm_m vs det_n (VP_ws vs VNP)? Answer:
NO for SPD in the padded perm-vs-det model (ELSW 2016), capped at O(m²); and specific other rank measures are barred (EGOW 2018). But NOT a
universal prohibition of all rank / representation-theoretic methods. char 0. Two separate VERIFIED_KNOWN results; precise conditions below.

## T10-A — the SPD barrier (Efremenko–Landsberg–Schenck–Weyman, arXiv:1609.02103, 2016)
SPD dimension: Γ_{r,ℓ}(P) = dim span{ x^α · ∂^r P/∂x_{i1}…∂x_{ir} : |α|=ℓ } (Kayal 2012; GKKS CCC 2013; gives the 2^{Ω(√m)} depth-4 lower bound).
**Theorem 1.5 (verbatim):** "There exists a constant M such that for all m > M and every n > 2m²+2m, any τ and any k < n,
rank((ℓ^{n−m} perm_m)_{(k,n−k)[τ]}) < rank((det_n)_{(k,n−k)[τ]})." Proof in four cases C1–C4:
- **C1 (k > n − n/(m+1)) [corrected]:** the det's k-th partials degenerate to span the WHOLE space of degree-(n−k) polynomials in m²+1
  variables — achieved by a specialization of det_n with **repeated identical determinant blocks** (e.g. diag(Y,…,Y,zI)), NOT a product of
  distinct general permanents. The padded permanent's partials cannot fill that space.
- **C2 (2m ≤ k ≤ n−2m):** the padded Jacobian ideal sits in (ℓ^{n−m−k}), of slowest Macaulay growth; det's Jacobian ideal is larger in
  degree n−k, hence (Macaulay) in all higher degrees.
- **C3 (k<2m, τ > 3n²m/2):** compare the padded ideal with the 2-generated ideal from det → ℓ₁ⁿ+ℓ₂ⁿ (complete intersection).
- **C4 (k<2m, τ < 6n³/m):** GKKS lower bound for det vs. a crude upper bound for the padded permanent (leading-monomial count).
C1,C2 overlap for n>2m²+2m and C3,C4 for n>m⁴, so n>2m²+2m suffices.
**Precise scope (owner-sharpened, confirmed in the source):** (i) holds for **m > M** (sufficiently large, NOT all m); (ii) for the SPD
measure (k-th Jacobian ideal) of the **padded** permanent ℓ^{n−m}perm_m vs det_n. The paper EXPLICITLY leaves open (line 133): "a more
general Young flattening [may] prove a ω(m²) lower bound" (companion paper on minimal free resolutions of Jacobian ideals). So SPD cannot
beat dc(perm_m)=Ω(m²) in this model, but the method is not universally dead.
**Exact computational witness (the degeneration mechanism, verified):** D = det-degeneration (ad−bc)²z² (5 vars a,b,c,d,z) has span{∂⁴D} of
dimension **15** = dim Sym²(ℂ⁵) (fills the whole quadric space); the padded permanent P = z⁴(ad+bc) has span{∂⁴P} of dimension **6**. So
Γ(det) > Γ(padded perm) — the determinant dominates. (The owner's broader table m=2,3,n=3,4,5 shows Γ(padded perm) ≤ Γ(det) in every case,
but these are BELOW the asymptotic threshold n>2m²+2m, so they illustrate, not prove, Thm 1.5.)

## T10-B — the EGOW rank-method barrier (Efremenko–Garg–Oliveira–Wigderson, ITCS 2018, arXiv:1710.09502)
A meta-barrier for rank-based lower-bound methods whose rank is subadditive under rank-1 additions. **Precise scope:** the quantitative
no-go theorems are proven for **tensor rank** and **Waring rank** (model-specific). This is NOT a proof that every rank method fails to
separate perm from det. Keep as a separate, model-specific result; do NOT inflate to ALL_RANK_METHODS_IMPOSSIBLE.

## Consequence for the program map (precise, not overgeneralized)
Two large method-classes are now mapped as polynomial-capped for VP_ws vs VNP:
- Local differential geometry (Hessian rank / tangency / singular-locus, T8/T9): capped at quadratic/cubic.
- Linear rank flattenings in the specific models above (SPD padded perm-vs-det; tensor/Waring rank): SPD capped at O(m²); EGOW bars tensor/Waring.
**NOT excluded (genuinely open):** general Young flattenings / Landsberg–Ottaviani (ELSW's own open question), GCT **multiplicity**
obstructions (BIP 2019 ruled out *occurrence* only — Kronecker/plethysm coefficients are not matrix ranks, so they evade EGOW), and the
Boolean routes (hardness magnification / uniformity gap, T5). A blanket "all rank/representation methods impossible" is unjustified.

## Next (Weg 2): GCT multiplicity obstructions
The multiplicity gap — mult_λ on the padded-permanent side vs. the Kronecker coefficient g(λ,(dⁿ),(dⁿ)) on the determinant side — is where
the padding does not force a linear rank collapse. The obligation: identify an explicitly formulated multiplicity obstruction not already
excluded by a known no-go (BIP occurrence-obstruction exclusion; the "no highest-weight / small-support" obstructions). To be pursued next.
