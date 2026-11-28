# T11 — Weg 2: GCT multiplicity obstructions (permanent vs determinant) (PI, 2026-11-17)

Research objective (owner): find + independently validate a concrete representation-theoretic multiplicity inequality separating the orbit
closures of det_n and the padded permanent ℓ^{n−m}perm_m. Method: two independent researchers (gpt-oss-120b PINNED; adversarial reviewer
w/ web), substance-agreed, citations corrected by the reviewer. Outcome = owner's Option 3: a PRECISELY BOUNDED OPEN PROBLEM, not a
certified obstruction (which would be a breakthrough). char 0.

## The two sides — orbit vs CLOSURE (the critical distinction; owner-sharpened 2026-11-17)
Write Y_{m,n} = closure of GL·(ℓ^{n−m}perm_m), D_n = closure of GL·det_n. For λ ⊢ nd set γ_λ = mult_λ ℂ[Y_{m,n}]_d (closure, padded
perm) and δ_λ = mult_λ ℂ[D_n]_d (closure, det). The OPEN-orbit multiplicities are a_λ (padded perm) and k_n(λ) = g(λ,(dⁿ),(dⁿ)) (det,
Kronecker; plethysm p_{λ,m,d} = ⟨s_λ, h_d[h_m]⟩ is a_λ). **[Definitions fixed 2026-11-28: |λ| = nd, so ⟨s_λ,h_d[h_m]⟩ cannot be the padded multiplicity. Three distinct upper bounds for γ_λ: A^amb = ⟨s_λ, h_d[h_n]⟩ (whole coordinate ring of Sym^n W; this is the ledger's 'p' in T11-J/L/P), A^par = ⟨s_λ, h_{d(n−m)}·h_d[h_m]⟩ (parametrization ℓ^{n−m}g, T11-O), and the open-orbit multiplicity a_λ = dim(S_λ)^{Stab} (not computed here). γ_λ ≤ min(A^amb, A^par, a_λ); δ_λ ≤ min(A^amb, k_n(λ)). Exact values (rational arithmetic): (3,4,4): A^amb = 2 for (12,4),(10,6),(10,4,2),(8,6,2),(8,4,4); A^par = 4,4,7,6,4; (3,4,6) λ=(6,6,6,4,2): A^amb = A^par = 1; (2,3,6) λ=(8,2,2,2,2,2): A^amb = 1, A^par = 2 while γ = 0 (both bounds positive, not sharp: essential-variable bound).]** **Direction (verified, standard AG):** the orbit O is open dense in its closure
Ȳ, so ℂ[Ȳ] ↪ ℂ[O] (a regular function vanishing on the dense O vanishes), hence **closure multiplicity ≤ orbit multiplicity**:
    **γ_λ ≤ a_λ   and   δ_λ ≤ k_n(λ)  — both are UPPER bounds.**
A certified multiplicity obstruction is **γ_λ > δ_λ**. Therefore a_λ > k_n(λ) (comparing the two UPPER bounds) is **NOT** a certified
obstruction — it bounds nothing about γ_λ vs δ_λ. (My first recording of T11-B compared these two upper bounds; corrected below.)

## T11-A — the GCT obstruction landscape (VERIFIED_KNOWN; two-model + primary-source)
1. **Occurrence obstructions — EXCLUDED.** Bürgisser–Ikenmeyer–Panova, "No occurrence obstructions in GCT", JAMS 32 (2019) 163–193,
   arXiv:1604.06431, **Theorem 1.4**: for n ≥ m²⁵ and λ ⊢ nd, if λ occurs in ℂ[orbit-closure(padded perm)] then it occurs in
   ℂ[orbit-closure(det_n)]. I.e. a_λ(perm)>0 ⟹ a_λ(det)>0. The polynomial padding range (n ≥ m²⁵) comfortably covers any
   superpolynomial-lower-bound attempt, so occurrence obstructions provably CANNOT prove perm≠det. (Exponent 25 loose/improvable.
   Precursor: Ikenmeyer–Panova, Adv. Math. 319 (2017), rectangular-Kronecker positivity.)
2. **Positivity-hardness — bars EFFICIENTLY-VERIFIABLE obstructions (not obstructions per se).** Plethysm: Fischer–Ikenmeyer, Comput.
   Complexity 29 (2020), arXiv:2002.00788 — computing is #P-hard, deciding POSITIVITY is NP-hard. Kronecker: Ikenmeyer–Mulmuley–Walter,
   Comput. Complexity 26 (2017) — positivity NP-hard (and C_=P-hard); computing #P-hard (Bürgisser–Ikenmeyer FPSAC 2008). These are exactly
   the multiplicities governing GCT obstructions ⇒ an explicit, poly-time-verifiable obstruction is not obtainable by generic positivity
   computation. (Also: these coefficients are NOT matrix ranks, so Weg 2 genuinely evades the EGOW/T10 rank barrier — the padding survives
   as a plethysm, not a collapsed linear rank.)
3. **Multiplicity obstructions — OPEN (not excluded).** BIP state explicitly (§1(c), abstract): they do NOT rule out the approach via
   multiplicity obstructions; comparing multiplicities may still succeed. No published no-go excludes them for det vs padded perm.

## T11-A extra barriers (owner-added, verified)
- **Ikenmeyer–Panova, Adv. Math. 319 (2017)** (rectangular Kronecker): for n > 3m⁴, a λ occurring on the padded-perm side cannot yield an
  obstruction merely through VANISHING of the rectangular Kronecker coefficient k_n(λ) — reinforces that occurrence/vanishing routes die.
- **Dörfler–Ikenmeyer–Panova, arXiv:1901.04576 (ICALP 2019)**: "Multiplicity obstructions are stronger than occurrence obstructions" —
  multiplicity obstructions provably SUCCEED where occurrence obstructions fail, but in a DIFFERENT geometric setting. A proof of concept
  that the multiplicity route is not vacuous; NOT a permanent–determinant separation.

## T11-B — the precisely bounded open problem (the frontier; CORRECTED to lower-bound-on-closure form)
A certified obstruction requires γ_λ > δ_λ on the CLOSURES. Since γ_λ ≤ a_λ and δ_λ ≤ k_n(λ) are both upper bounds, the obligation is:
    **find a specified (m,n,d,λ) and certified bounds L, U with  L ≤ γ_λ,  δ_λ ≤ U,  and  L > U.**
The hard half is the **lower bound L ≤ γ_λ on the orbit-CLOSURE coordinate ring ℂ[Y_{m,n}]_d** (not the open-orbit plethysm a_λ, which is
only an upper bound for γ_λ). All known explicit families give EQUALITY a_λ = k_n(λ); a gap could only open at the BOUNDARY of the Kronecker
polytope, where no λ is known. Coupled obstacles: (a) existence of such (λ) with γ_λ > δ_λ is OPEN; (b) exhibiting/verifying one without
solving a #P-/NP-hard positivity instance (T11-A.2) is the SHARPER obstacle. **Asymptotic criterion:** a VP_ws≠VNP-relevant separation
needs L > U to hold for n beyond EVERY fixed polynomial bound in m, not merely one fixed exponent. Post-2019 pivots (data): finer
multiplicity/asymptotics; unpadded + symmetry formulations (Landsberg–Ressayre; Grochow–Mulmuley–Qiao); border-rank/matrix-mult GCT.

## Honest status vs the ultimate objective (P vs NP)
Weg 2 is the genuine superpolynomial-candidate route (unlike T8/T9/T10, all polynomial-capped) AND evades the rank barrier — but it meets
its own double barrier (occurrence dead + positivity #P/NP-hard). No certified obstruction; no refuted construction either. Deliverable =
bounded open problem T11-B. This does NOT prove anything about P vs NP; it maps precisely where the GCT route is stuck and why.
