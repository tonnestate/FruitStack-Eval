# T58 — Hamiltonian-cycle projection of U_G, VNP membership/hardness, quantitative transfer, and the mechanism of the 9/4 proof (2026-11-28)
Corrects T57 (which searched theory/*.md only and missed Proofbook 17584/17585/17879). Status: CLAIMED derivations; external inputs marked EXT. No claim about P vs NP.

## A. HC_h = rho_h(U_{G_h})  (uses Proofbook 17584; transfer to F2, F3 and every field)
Local state sum: positions i=1..h, state v_i in [h], v_1=1 fixed, nb=ceil(log2 h) bits per position, unused codes weight 0.
Tables: A_ij(a,b)=[a!=b] for non-consecutive pairs; [a!=b]X_ab for (i,i+1); [a!=b]X_{b,1} for the closing pair (1,h).
Product nonzero iff v is a permutation (all pairwise distinct); its value is prod_i X_{v_i v_{i+1}} (cyclic). Sum over assignments = HC_h(X), each directed tour once (v_1=1 fixes the rotation); the reference triangle is pinned, so no division by 6.
17584: Z_S = ev_w(U_G), U_G in N[Y] (one variable y_{alpha,a} per selector). rho_h: y -> X_ab (consecutive-table entries, a!=b), y -> 1 (other tables, a!=b), y -> 0 (a=b or invalid code). Identity holds in N[X]; hence over every commutative semiring and every field by ring homomorphism (no characteristic assumption).
Size: tables O(h^2), entries <= 4^nb < 4h^2 each, AND chain of 2nb-1 gadgets of constant size: |V(G_h)| = O(h^4 log h) (built: h=3: 1919 vertices, h=4: 5301, h=5: 67023). Gadget-level machine check (G_3, G_4 over Z, F2, F3) NOT completed.
Hand-checked gadget facts: converter (edges jy,jz,yz,xy,yR2,xR2,zR1) gives x=1[colour(j)=1] uniquely for all 3 colours of j; EO triangle (i~R2,k~R0) has exactly the 3 colourings (0,1,2),(0,2,1),(1,0,2), each with exactly one coordinate of colour 1.
Is it already in 17879? Step 5 of 17879 contains the general statement (every clause sum is a p-projection of U_G; U_G not in VP conditional on EXT). HC itself, the explicit distinctness encoding and the field check are not written there; HC_h is a clause sum, so this is a special case.

## B. VNP membership and the equivalence
U_G(y)=sum over e in {0,1}^{3|V|} g(y,e), g=prod_v oh_v(e) * prod_{uv in E}(1 - sum_c e_{uc}e_{vc}) * prod_v (1+e_{v1}(y_v-1)),
oh_v = e0(1-e1)(1-e2)+(1-e0)e1(1-e2)+(1-e0)(1-e1)e2. Every factor is 0/1 on Boolean e over any field, pinned vertices are constants, deg g = O(|V|+|E|), size O(|V|+|E|): g in VP, so U_G in VNP in every characteristic.
Hardness: HC_h=rho_h(U_{G_h}) is a p-projection; HC is VNP-complete over every field (EXT: OpenAI hamperm Sec. 1.1 citing Valiant, Buergisser; not independently re-derived here, in particular characteristic 2). So U_G is VNP-complete (for the family G_h) and: U_G in VP  <=>  VP = VNP.

## C. Quantitative transfer (EXT: OpenAI hamperm Thm 1.1, 2026-11-24)
Thm 1.1: over every field of characteristic chi, N>=N0(chi): degree-component border size L(HC_N) >= exp(c (log N)^2/(log log N)^2), c absolute; formal polynomials, border/approximate degree-N component allowed.
Transfer: a circuit (exact or border, any depth) for U_{G_h} with S gates gives, after substituting rho_h (variables/constants are free), a circuit with <= S gates whose degree-h component in X is HC_h. Hence S >= exp(c(log h)^2/(log log h)^2).
In n=|V(G_h)|=Theta(h^4 log h): log h = (1/4)log n - O(log log n), so
L(U_{G_h}) >= exp( (c/16 - o(1)) (log n)^2/(log log n)^2 ) for all n of the form |V(G_h)|, h>=N0(chi). If |V|=O(h^kappa): c/kappa^2.
Lean status (lean379.md): Lean proves only the eventual superpolynomial (> N^C for every C) EXACT-circuit bound for HC over every field; the exp(c(log N)^2/(loglog N)^2) bound for degree-component border circuits is explicitly UNFORMALIZED. The quantitative bound is therefore resting on the paper proof.

## D. Three models (must not be conflated)
1. Formal polynomial computation (above): lower bound proven (EXT).
2. Finite-field evaluation on Boolean inputs: circuits only need to agree with U_G on {0,1}^N; they may compute g = f + sum (x_i^2-x_i)h_i. The formal bound says nothing here (17879 Step 6a; 17585 control K_{n,n}: DP O(n) although tw=2n+1). HC with Held-Karp gives formal size O(2^h h^2) as upper bound.
3. Boolean semiring (or/and) evaluation of U_G at 0/1: 3-COL decision, NP; lower bound = NP vs P/poly, not implied.
Implications: formal upper bound => models 2,3 upper bounds; the converse direction (lifting formal lower bound to model 2/3) is exactly the open core.

## E. Matrix multiplication proof (mm94, Sections 2-27): mechanism and transfer
Proof by contradiction. (Thm 2.2, unconditional) any trivalent tensor network over finite field k (sum over internal bits, exact 0/1 output) for t independent copies of list distinctness D_w (2^w words of 2w bits) has volume > t n_w w^sigma, uniformly 1<=t<=2^w (routing of tagged records; sorting-network upper bound O(w^2) per bit). (Thm 2.1) if omega_k<9/4, a trivalent network of size m<=n^1.05, e>=n exterior bits has a network for V^{(x)d} (d<=n^{o(1)}) of size d(m h^{-gamma}+e h^eta), h=ceil(log2 n). Recurrence (Sec. 27), x_j=s_j/e_j size per exterior bit, q=h^{-(1-delta)a}<1: x_{j+1} <= q max{x_j, 2h^{2a}}, so x_J <= max(q^J x_0, 2 q h^{2a}); a=A/J, J fixed; copy factor cancels; log2 r_j=O((log h)^2); descent over K/k costs O([K:k]^2)=h^{o(1)}. After J rounds volume/bit = O(w^eta) < w^sigma: contradiction, hence omega_k>=9/4 for finite k; Lemma 2.5 transfers to every field.
The user-quoted form x' <= h^{-a/2} x + h^{2 sigma} (build/list.tex) is NOT in the extracted mm94 text; the proof text has the max-form above (same fixed-point O(h^{2a})). list.tex itself not located; unverified.
Exact assumptions used: (i) a bilinear algorithm with exponent<9/4 specialised to finite k, applied through Lemma 23.1 to tensor POWERS of a network (multiplicative tensor structure, replicas keep individual exterior bits); (ii) start network with m/e polylogarithmic-to-n^0.05, saved only by powers of h=log n; (iii) lower bound uniform in replication t. The gap exploited is polylogarithmic (w^sigma vs w^eta), not superpolynomial.
Transfer assessment (E2, QE*, Search-MCSP, T49): requires an object with a tensor-power-compatible compression operator and a replication-uniform exact lower bound. P=NP gives decision circuits, not contraction (sum over internal bits) of tensor networks; the analogue would be P^{#P}-type contraction, and 17879 Step 6(b) already shows no accelerator arises. Transfers: the MODEL (bit-tensor networks = Boolean local state sums = the form of U_G) and Thm 2.2 as an unconditional polylog-superlinear lower bound for exact finite-field state-sum networks on Boolean inputs (model 2), but for D_w, not for U_G; HC's distinctness encodes h words of log h bits (a bijection test), a restriction of the domain of D_w, so Thm 2.2 does not apply to it directly. Not transferred: the compression step. Further reading of Sections 5-26 not completed beyond Section 2, 27 and the table of contents.
