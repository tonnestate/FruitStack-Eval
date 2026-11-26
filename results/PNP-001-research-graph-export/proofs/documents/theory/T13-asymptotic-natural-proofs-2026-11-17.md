# T13 — Algebraic natural proofs: asymptotic HWV families (PI, 2026-11-17)

Mandate (owner): asymptotic ONLY — no fixed-instance VP claims. A single fixed polynomial has a finite circuit; VP is about uniform
families. Define a uniform family (P_{T_n})_{n>=1} of HWV covariant equations and classify its complexity, then check the GKSS/FSV barrier
PRECONDITIONS (which are conditional on succinct hitting sets, not a blanket VP-equation exclusion). Primary sources verified.

## T13-1 — the uniform family
W_n = (C^{n^2})*, V_n = Sym^n(W_n), N(n)=C(n^2+n-1, n) = #coefficients. Pick a degree sequence d(n), a partition lambda(n) |- n*d(n), and a
semistandard Young tableau T_n of shape lambda(n) (content: each of 1..d(n) appears n times, matching the plethysm Sym^{d(n)}(Sym^n W_n)).
Schur-Weyl gives a multihomogeneous HWV polynomial P_{T_n}(Z) of degree d(n) in the N(n) coefficient variables Z = coeff(f):
    P_{T_n}(coeff(f)) = < HWV(T_n), f^{tensor d(n)} >,  HWV(T_n) = column-antisymmetrize (determinant contractions) + row-symmetrize.
GCT soundness candidate iff: P_{T_n} vanishes on D_n = closure(GL.det_n) for all f, and P_{T_n}(coeff(l^{n-m}perm_m)) != 0 for infinitely many n.

## T13-2 — three complexity measures (BDI21 taxonomy; arXiv:2002.11594, CCC 2021, verified)
BDI21 verbatim results: "every lower bound in GCT can be proved by the use of HWVs"; "we prove the NP-hardness of the evaluation of HWVs in
general"; "efficient algorithms if the TREEWIDTH of the corresponding Young-tableau is small, where the point of evaluation is concisely
encoded as a noncommutative ABP"; "a large new class of separating functions that can be efficiently evaluated at points with low (border)
Waring rank"; "border Waring rank is bounded from above by the ABP width".
1. CONSTRUCTION complexity: cost to produce T_n / a circuit for P_{T_n} from 1^n. For combinatorial T_n: typically P/PSPACE. (Uniformity; ties to T5.)
2. REPRESENTATION complexity: minimal algebraic circuit size of (P_{T_n}) in the N(n) coefficient variables. **Governed by the TREEWIDTH of
   the tableau graph (NOT merely rows ell(lambda), BDI21's precise parameter):** small treewidth => P_{T_n} efficiently evaluable (VP-regime);
   unbounded treewidth => evaluation NP-hard => under standard assumptions P_{T_n} not in VP.
3. EVALUATION complexity at a SPECIFIC f_n: cost of the single number P_{T_n}(coeff(f_n)). BDI21: can be in P EVEN WHEN the general HWV is
   NP-hard, precisely when f_n has LOW (border) WARING RANK / small noncommutative-ABP encoding. det_n and perm_m are highly structured, so
   obstructions may be efficiently CERTIFIABLE at them even with a non-VP separating equation.

## CORRECTIONS (owner, 2026-11-17) — two earlier claims here were WRONG
1. "Growing tableau treewidth is NECESSARY for a GCT obstruction" is NOT PROVEN. BDI21 proves NP-hardness of GENERAL HWV evaluation + efficient
   algorithms under structural conditions; it gives NO lower bound tw(G_{T_n})=omega(log n) => P_{T_n} not in VP for any specific family, and
   bounded treewidth does NOT imply VP (the runtime also depends on the input ncABP width). Must not be a research invariant.
2. "perm/det have low (border) Waring rank" is FALSE. VERIFIED here: dim span{d^k f} = C(n,k)^2 exactly for det_n, perm_n (n=2,3), so border
   Waring rank >= C(n,floor(n/2))^2 = Theta(4^n/n), EXPONENTIAL. BDI21 Prop 6.6: minimal noncommutative-ABP width ncw(f) = max_k dim(d^k f) =
   C(n,floor(n/2))^2, also exponential. So BDI21's "efficient at low-Waring-rank points" does NOT apply to det/perm by that property.
3. BDI21 Thm 7.2 runtime = w^{omega*(tau+1)} * poly(s,d,N,|T|): TWO independent parameters, ncABP width w AND tableau treewidth tau. Treewidth
   alone is not a complexity verdict. GKSS/FSV barrier is CONDITIONAL on succinct hitting sets for VP (open; CKRST FOCS 2020: VP-natural proofs
   exist in some settings), so "P in VP" alone does not kill the approach.

## T13-4 CORRECTED — separating equation vs multiplicity obstruction (the right framing)
A separating HWV equation P with P in I(D_n), P not in I(Y_{m,n}) proves non-inclusion Y_{m,n} not subset D_n, but does NOT imply
gamma_lambda > delta_lambda. Requiring delta_lambda=0 < gamma_lambda IS an occurrence obstruction, already excluded by BIP (n>=m^25). The
correct, more general and NOT-BIP-excluded condition: let H_{lambda,d} = weight-lambda HWV space (dim p_lambda), with evaluation maps
E_D: H_{lambda,d} -> C[D_n] and E_Y: H_{lambda,d} -> C[Y_{m,n}]; then delta_lambda = rank E_D, gamma_lambda = rank E_Y, and a concrete
geometric separating equation exists IFF
    **ker E_D  NOT subset  ker E_Y**   (some HWV vanishes on the determinant closure but not on the padded-permanent closure).
This is strictly MORE GENERAL than a multiplicity obstruction: gamma_lambda > delta_lambda is SUFFICIENT but NOT necessary - kernels can
differ even at equal ranks.

## Verified structural observation at (3,4,4) (directly serving the corrected leitfrage)
At (3,4,4), EVERY occurring lambda has delta_lambda(det) = p_lambda (full ambient multiplicity): the 5 p=2 give rank E_D = 2 = p, the 23 p=1
give rank E_D = 1 = p. Hence E_D is INJECTIVE => ker E_D = {0} for ALL 28 lambda => NO HWV vanishes on D_4 in degree 4 => NO separating equation
of this form exists at d<=4. The determinant orbit closure realizes the FULL ambient multiplicity through degree 4. So the separating-equation
frontier is the first (n,d,lambda) where delta_lambda(det) < p_lambda (ker E_D != 0); only there can ker E_D not subset ker E_Y begin.

## Corrected research subgoal (bounded, provable, not the full open problem)
Find a STRUCTURAL sufficient condition under which an HWV vanishes identically on the determinant orbit closure WITHOUT the same condition
forcing vanishing on the padded permanent - i.e. a controlled source of ker E_D not subset ker E_Y. Concretely: locate the smallest (n,d,lambda)
with delta_lambda(det) < p_lambda (determinant drops below ambient), then test whether that kernel vector also vanishes on Y_{m,n}. Existence of
the full asymptotic separating family (for every fixed poly bound on n) remains THE open problem and is not to be restated as the next step.
