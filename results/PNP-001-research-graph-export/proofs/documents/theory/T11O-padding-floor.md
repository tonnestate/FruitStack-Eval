# T11-O — The Padding-Floor Characterization of ker E_Y (PI + FruitStack, 2026-11-17)

An experiment-derived candidate general theorem about the padded-permanent orbit closure. Produced by the intelligent-search loop:
the (4^5) experiment at d=5 suggested it; the falsification-prioritized search confirmed it; one direction is proven.

## Statement
Let Y_{m,n} = closure(GL_{n²}·(z^{n-m}·perm_m)) ⊂ Sym^n(W), W=C^{n²}, z a padding linear form independent of the m² permanent
variables. For a weight-λ highest weight vector P_λ of degree d (λ ⊢ nd):
    **P_λ|_{Y_{m,n}} ≡ 0   ⟺   λ_1 < d(n-m).**

## Proof of (⟸) [PROVEN — Lemma A]
Any k-plane restriction factors as f|_U = u_1^{n-m}·C with C = perm_m|_U (choose coords z|_U = u_1). So every coefficient c_α of
f|_U with α_1 < n-m vanishes. A degree-d HWV monomial c_{α^(1)}···c_{α^(d)} has u_1-weight Σ_j α^(j)_1 = λ_1. If λ_1 < d(n-m),
by pigeonhole some factor has α^(j)_1 < n-m, which is 0 at f|_U; hence every monomial of P_λ vanishes at f|_U, for EVERY U. So
P_λ ≡ 0 on the whole orbit closure Y_{m,n}. ∎

## Evidence for (⟹) [CONFIRMED at (3,4,5); proof OPEN]
Falsification-prioritized intelligent search at (m,n,d)=(3,4,5), d(n-m)=5: tested all 23 five-row partitions + 22 partitions with
ℓ≤4, total 45 occurring λ. ZERO violations: every λ with λ_1 ≥ 5 is NON-vanishing on Y; the only vanishing case is (4,4,4,4,4)
(λ_1=4<5). (Note ℓ≤4, λ⊢20 forces λ_1≥5 — correctly predicted non-vanishing.) So ker E_Y(Y_{3,4})_{d=5} = exactly {λ_1<5}.

## Candidate proof route for (⟹) [to attempt]
Edge-reduction (Lemma B): at the tight case λ_1 = d(n-m), every HWV monomial must take u_1-exponent exactly n-m in each factor, so
P_λ(f|_U) collapses to P_λ(u_1^{n-m}·C̄_m) with C̄_m = perm_m(0,u_2,…,u_k) a generic degree-m form in k-1 variables. For λ_1 >
d(n-m) there is strictly more freedom (u_1-containing terms of C allowed), so non-vanishing should only get easier. An induction on
the number of variables / on λ_1 above the floor, plus genericity of perm_m|_U, is the natural route. Not yet carried out.

## Complexity relevance (honest)
This is a tool, not a lower bound. Consequence: any FORWARD separating equation for perm_m vs det_n (an HWV in I(D_n)\I(Y_{m,n}))
must have λ_1 ≥ d(n-m) — a reusable shape constraint on separators, derived once and valid for all (m,n,d). Combined with the
rectangular null-cone lemma (T11-N) and the symmetroid/row bound on the determinant side, it carves the separator search space
structurally instead of by enumeration. It does NOT by itself overcome the quadratic (Mignon-Ressayre/T8) barrier.

## Status
(⟸) proven; (⟹) confirmed on 45 cases at (3,4,5), proof open; novelty unchecked (padding-floor may be classical — pending
literature check). This is the learning loop's first theorem-shaped output: an experiment-derived candidate with one direction proven.

## REFUTED (2026-11-17): the EQUIVALENCE is false; the (<=) direction stands
Owner found a CERTIFIED COUNTEREXAMPLE to the converse (⟹). At (m,n,d)=(2,3,6), lambda=(8,2,2,2,2,2)|-18: p_lambda>0, lambda_1=8 >=
d(n-m)=6, yet gamma_lambda(Y_{2,3})=0 (vanishes on Y). So lambda_1>=d(n-m) is NOT sufficient for non-vanishing.
MECHANISM (symbolic, independently verified): for a cubic F=sum A_{ijk}x_ix_jx_k define the degree-6 HWV P(F)=det((A_{1ij})_{1<=i,j<=6}),
a weight-(8,2,2,2,2,2) covariant. The padded permanent z*perm_2 uses only m^2+1=5 essential variables, so for ANY g the 6x6 contraction
matrix (A_{1ij}) has rank <= 5 => its determinant = 0 => P|_{Y_{2,3}} == 0. P is not identically zero: F_0=x_1^3+3x_1(x_2^2+...+x_6^2)
gives contraction = I_6, P(F_0)=1. VERIFIED (sympy): z*perm_2 contraction rank 4 det 0; random g.f rank 5 det 0; F_0 rank 6 det 6^6.
The construction generalizes (r=m^2+2, lambda=(r(n-2)+2, 2^{r-1})) to an INFINITE family of counterexamples. This is subspace-variety
geometry (bounded number of essential variables), classical (Landsberg).

## CORRECTED RESULT — two necessary conditions (neither sufficient)
    gamma_lambda(Y_{m,n}) > 0  ==>  lambda_1 >= d(n-m)   AND   ell(lambda) <= m^2+1.
First condition: the PROVEN padding-floor (Lemma A). Second condition: the ESSENTIAL-VARIABLE / subspace-variety bound (Y ⊆ Sub_{m^2+1},
and S_lambda occurs in C[Sub_k] only if ell(lambda) <= k). Both are necessary filters on any surviving / separating HWV; neither is
sufficient. STATUS: equivalence REFUTED; (<=)/Lemma A retained; two-condition necessary filter adopted for AutoML candidate prioritization.
