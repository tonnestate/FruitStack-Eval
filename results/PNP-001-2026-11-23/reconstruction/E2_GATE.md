# E2_GATE — Boolean-to-general-IPS transfer (OPEN, E1 parked)
Baseline d7635f9ea437c494f1c032e4faadfb673a4e90b1. This is a proposed sufficient lemma, not an established result.

## Exact research target
Let Psi_n be precisely the doubly lifted non-3-colorability CNF family in THEOREM-12.md, lines 7–12, with fixed gadget parameter p and order-lift selector construction. Let X_n be its Boolean variables, Q_{n,j}(X_n) the clause-falsification products, and B_{n,i}=X_i^2-X_i. Fix field F=F_2 as a proposed single-field target (Theorem 12 claims every field); E1 and E2 must use the same field and encoding. Define IPS_F(Psi_n) as the minimum number of arithmetic gates in a division-free general algebraic circuit C_n(X,Y,Z), over F, computing a polynomial satisfying the formal polynomial identities
C_n(X,0,0)=0 and C_n(X,Q_n(X),B_n(X))=1.
Inputs/constant convention must be aligned with the paper; permit field constants 0,1, arbitrary DAG sharing, fan-in two + and multiplication, subtraction expressible over F_2. No restriction on degree or placeholder degree in the general IPS target. Circuit families may be nonuniform; no claim about efficient construction.

**E2(F_2):** P=NP implies that there exist constants k>=1, K>0, n0 such that for every n>=n0 there exists C_n as above of size <= K n^k.
The choice of F_2 is a narrowing for research, not a claim that the source theorem already provides E2. Polynomial-size input encoding must be preserved. Because the family is explicit and UNSAT for each n, a decider for its membership/rejection alone supplies no certificate in IPS.

## Literature gate
- Cook–Reckhow: NP=coNP iff there exists a polynomially bounded propositional proof system. Under P=NP this existence follows, not a bound for a specified system. See Grochow–Pitassi, Circuit Complexity, Proof Complexity, and Polynomial Identity Testing: The Ideal Proof System, JACM 2018, https://arxiv.org/abs/1404.3820 and https://www.cs.toronto.edu/~toni/Papers/jacm-gp.pdf.
- Grochow–Pitassi: general IPS superpolynomial lower bounds imply an algebraic separation VP != VNP (with appropriate field/model conventions); the known transfer is not a Boolean separation. IPS simulates Extended Frege under the relevant conventions; simulation of one strong proof system does not imply simulation of all polynomially bounded systems. The abstract and public source descriptions do not establish E2.
- Grochow, Polynomial Identity Testing and the Ideal Proof System, https://arxiv.org/abs/2306.02184: PIT in NP iff IPS can be p-simulated by a Cook–Reckhow system. This direction does not give polynomial IPS proof lengths from P=NP.
- Bounded-arithmetic K2 contract concerns translations of restricted theories and does not itself show that P=NP proves the requisite arithmetic sentences or yields short IPS certificates.
- Literature check is targeted, not exhaustive; no known theorem supplying E2 for this family was identified. Status OPEN / no verified transfer. Do not cite absence of a search hit as a proof of nonexistence.

## Decision
E1: for every fixed k,K, if a general IPS certificate of size <=K n^k exists, a roABP-IPS_LIN refutation of polynomial width exists in some order, with exact certificate identities. A family-specific implication suffices. Theorem 12 + E1 gives superpolynomial general IPS lower bounds in the sense of no polynomial bound on all sufficiently large lengths. E2 + that consequence gives P != NP. Without E2, no Boolean separation; without E1, the restricted lower bound remains restricted.

Only E2 source/transfer audit is active within E. E1 parked until an exact known or proved sufficient transfer is identified or owner authorizes an algebraic-only milestone. Existing Lemma 15 requires a full roABP and sparse placeholder support, not arbitrary general IPS. Theorem 14 requires bounded placeholder degree; Theorem 16 concerns a canonical product certificate. Neither supplies E1 or E2.

If E2 remains unsupported after targeted source and family-specific proof audit, report both E and A as open and ask owner to choose the priority; A has a known MMW Boolean transfer but its uniform nonlinear streaming lower bound (40a) is open. Do not infer tractability solely from the number of missing arrows. A remains formalization-only until owner changes scope.

Small-instance controls, if E1 later reopens: explicit identities, exact coefficient rank in all relevant orders, polynomial overhead hypothesis fixed in advance, compare same family/encoding. A finite failure can refute a specific exact conversion algorithm or numerical bound, not an asymptotic existential polynomial bound with unconstrained constants.
