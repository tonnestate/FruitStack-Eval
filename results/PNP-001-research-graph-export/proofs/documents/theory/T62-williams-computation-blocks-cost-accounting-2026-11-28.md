# T62 — Williams' computation-block architecture (STOC 2025) against our algebra: exact cost accounting, admissible extensions, and the corrected T61 criterion (2026-11-28)

Status: derivation. P != NP is NOT claimed. Labels: [U] unconditional, [H] under H (uniform P = NP), [R] read in the original paper this session
(`people.csail.mit.edu/rrw/time-vs-space.pdf`, §3.1, Appendix A; §3.2/3.3 only skimmed by headings), [S] sketch with stated assumptions.
Shared Markdown context for Claude and Codex.

## 1. Reconstruction [R]
Oblivious two-tape machine M' (time T' = O(t log t)), time blocks of length b, B = T'/b blocks. Computation graph G: node i = time block, in-degree ≤ 5.
Node function f_u : {0,1}^{5b} -> {0,1}^b runs b steps of M' on the (≤4) tape blocks supplied by the children. TreeEvaluation instance = unrolling of G into a tree of
height B+1, fan-in d=5, size 2^{Theta(B)}, accessed implicitly (children computable in polylog space from the oblivious head schedule).
Cook–Mertz ADD (Appendix A), field F of characteristic 2, m = |F|-1 (odd), omega a primitive m-th root of unity: ADD(u, x^_1..x^_d, y^) returns y^ + v_u by
 sum_{i=1}^m  P(omega^i x^_1 + v_{u1}, ..., omega^i x^_d + v_{ud}) = P(v_{u1},..,v_{ud})      (5)
for every polynomial P with deg P < m. Register contents x^ are arbitrary (catalytic) and are restored; char 2 makes "add v twice" cancel.
(2) is the multilinear extension (degree d*b, needs |F| >= d b^2), (6) a degree-d(|S|-1)t extension over S^t (needs d(|S|-1)t < |F|) to shorten registers to O(b) bits.

## 2. What (5) really needs (removes the "multilinearization" assumption) [U, proved here]
**Lemma W1 (rewritten 2026-11-28; four separate requirements).** Let f : {0,1}^N -> F (N = d b) be a node function and P a polynomial in N variables over F, |F| = m+1, omega a primitive m-th root of unity.
1. *Interpolation identity (5)* — requires only deg P < m (total degree). It holds for EVERY polynomial of that degree, Boolean-valued or not. Proof: expand P(omega^i x^ + v) in monomials of x^; a monomial of x^-degree k carries sum_{i=1}^m omega^{ik}, which is 0 if m does not divide k and equals m = -1 (nonzero in every characteristic) if m | k; with k <= deg P < m only k = 0 survives and the sum is m·P(v). In characteristic 2, m is odd so m = 1 and the sum is P(v) exactly; in other characteristics one gets -P(v) and the sign must be tracked.
2. *Correctness of the encoded node function* — requires P(a) = f(a) for a in {0,1}^N, because the arguments v_{u1..ud} actually fed in are Boolean strings. This is the only place where the Boolean cube enters; P need not be Boolean-valued elsewhere.
3. *Field characteristic* — used for register restoration only: ADD adds v_{ur} to x^_r in one call and again in the second loop; in characteristic 2 the two additions cancel, otherwise one subtracts (Cook–Mertz handle general fields).
4. *Register restoration / catalytic behaviour* — independent of 1–3: every call must return the registers it was given, up to the intended additions.
Admissible polynomials exist iff deg M_f < m, where M_f is the unique multilinear representative (exact degree of f over F): reduction modulo x_i^2 - x_i is degree non-increasing, so every P with (2) has deg P >= deg M_f, and M_f itself is admissible. So no multilinearization circuit is needed, but m > deg M_f is forced. (Over F_3 the QE polynomial F_corr is ±1-valued and not admissible; F_corr² is.)

## 3. Cost accounting (every construction separated)
| item | Williams (multilinear, (2)) | note |
|---|---|---|
| Representation size | explicit tree 2^{Theta(B)}; implicit: O(b) catalytic + O(B log(d b)) local | explicit size is exponential in T'/b |
| Construction time | per node-children poly(log t) via oblivious schedule | no explicit tree is built |
| Evaluation time of one extension value | sum over 2^{d b} Boolean points (O(b) space) | exponential in b |
| Recursion count | N(h) = 1 + 2 d m N(h-1) calls | see §4 |
| Certificate size | none (algorithmic; no formal certificate) | T48 §9.6 |
| Verification time | = re-running the evaluation (no verifier shortcut) | |

## 4. Theorem W2 (time can never beat direct simulation) [U, derived from the pseudocode in [R]]
Each non-leaf ADD(u) makes 2 d m calls (d m in the first loop, d m in the second), m >= 3 (smallest admissible: F_4, m = 3). Along the chain of nodes j = B, B-1, ..., 0 (edge (j-1,j) always
present) the call count satisfies N(h) >= 2 m N(h-1), so the number of internal calls is >= (2m)^B >= 6^B. Each internal call touches the b-bit registers: >= b operations. Hence
 time(ADD architecture) >= b * 6^{T'/b}  >= 6 T'   for every block length b <= T'  (the function x -> 6^x / x is increasing for x >= 1, with x = T'/b).
**This lower bound does not involve the cost of evaluating the extension at all.** Even an oracle giving every f~_u(.) value in O(1) leaves time >= 6T'. The time/space tradeoff
(space ~ sqrt(t log t), time 2^{Theta~(sqrt t)}) is intrinsic to the m-fold masking recursion, not to the exponential sum over Boolean points. ∎
**Corollary.** The extension-evaluation cost is not the obstacle to a *work* reduction; the recursion multiplicity m^{T'/b} is. A reduction of work must lower the number of recursive injections
of the same child value, not the cost of one extension value.

## 5. Why the masks cannot be fewer [U, proved here; restricted class]
**Proposition W6 (scalar-character masking needs deg P + 1 masks).** Let G be a finite abelian group acting on x^ through characters theta_i (monomial x^alpha transforms by sum alpha_i theta_i) and
suppose the average over G annihilates every monomial with 0 < |alpha| <= D. Then |G| >= D + 1.
*Proof.* Take alpha = k e_1, 1 <= k <= D: need k theta_1 != 0, so theta_1 has order > D and divides |Ghat| = |G|. ∎
So (5) is optimal among such averaging identities with D = deg P >= deg M_f (Lemma W1): per level >= deg_F(f_u) + 1 masks. Our Boolean-ideal cancellation / certificate composition
(T48 §2, composition law eta_12 = eta_1 + D_1 eta_2) and quotient identity act on a *given* constraint system and do not provide a group-averaging identity with fewer masks. [No claim beyond the stated class.]

## 6. Evaluating the extensions: what our algebra gives and does not give
**Proposition W3 (evaluation of multilinear block extensions is as hard as ⊕P) [U for the reduction; S for the embedding].**
(i) Let g : {0,1}^k -> {0,1}. Over F of characteristic 2 with |F| > k, M_g(a,..,a) = sum_y g(y) a^{|y|}(1+a)^{k-|y|} is a polynomial in a of degree <= k whose coefficient of a^k is
sum_w N_w = (# g^{-1}(1)) mod 2 (the factor (1+a)^{k-w} has leading coefficient 1). k+1 evaluations and interpolation therefore give the ⊕-count of g in time poly(k) + (k+1)*cost(M_g).
(ii) Multilinear extensions commute with Boolean restriction, so M_{f_u}(c, .) = M_{g} for the restriction g of f_u to a subset of its inputs with the others fixed to Boolean constants c.
(iii) [S, assumption: M' universal, k polylog k <= b] a block of a universal oblivious machine can run, on fixed Boolean tape contents encoding a CNF phi with O(k) clauses and free bits y,
the linear-time verifier phi(y); then g = phi and (i) yields ⊕SAT.
Hence **poly(b)-time evaluation of M_{f_u} at all points of F^{db} for all block functions of universal M' implies ⊕P ⊆ P** (⊕SAT is ⊕P-complete). Under H one has PH = P but ⊕P ⊆ P is not forced (T59);
the same type of statement holds for the F_3 functional QE polynomial of the gate encoding, with ⊕P replaced by Mod_3 P (correction 2026-11-28: over F_3 the evaluation of the Hamiltonian-cycle polynomial at the all-ones point gives #HC mod 3, not mod 2; T53 §1: the formal F_C of the Hamiltonian-cycle check is VNP-hard). Also, F_corr itself is a ±1-valued extension and is not admissible for (5) (it must equal f on the cube); F_corr² equals the indicator over F_3 and is admissible with degree ≤ 2e*.
So evaluation shortcuts through multilinearization, through functional QE, or through the formal polynomial are all excluded by the same ⊕P statement (a consequence of T53 §2a / T50 MT).
What remains is Lemma W1: a *non-multilinear* admissible P with a small arithmetic circuit and degree < m. Boolean circuit arithmetization gives deg up to 2^{depth}; the b-step block has depth
Omega(b) (sequential) so m would be 2^{Omega(b)}, registers grow to b^2 bits and the space becomes T^{2/3}: no gain. Whether a low-degree small-circuit admissible P exists for every block function is
the open Boolean-size => low-degree-arithmetic-size question (a weaker form of MT of T50; not settled by any result here).

## 7. Corrected success criterion for T61 §8 (owner correction accepted)
T61 §8 said "compress the Cook–Levin instance to o(T)". That is insufficient. Let H give a solver with unknown exponent kappa: time n'^kappa on instances of size n'. A reduction R computing
an instance I_{M,x} of size n' = |I| in time tau_R decides L in time tau_R + n'^kappa + (certificate/verification costs). A contradiction with the time hierarchy for every kappa needs
 tau_R = o(T / log T)   and   n' <= T^{1/kappa - epsilon} for every fixed kappa, i.e. **n' = T^{o(1)}**,
and the whole composed procedure (reduction + solver + any recursive recomputation) must be charged. Williams' instance has explicit size 2^{Theta(T'/b)} and implicit-access time >= 6T' by Theorem W2:
it fails both clauses, independently of the evaluation question.

## 8. What was constructed and what remains
Constructed [U]: Lemma W1 (exact admissibility class; removes the multilinearization assumption), Theorem W2 (a work lower bound for the ADD architecture independent of extension evaluation),
Proposition W6 (optimality of the mask count in the scalar-character class), Proposition W3 (all multilinearization-type evaluation routes imply ⊕P ⊆ P), the corrected criterion §7.
Not constructed: any architecture with work < T'. The two exact reasons: recursion multiplicity (W2/W6) and absence of a small low-degree admissible extension (§6). Nothing here is a contradiction from H.
Next candidate (not started): redesign that injects each child value once into several masked contexts simultaneously (vector registers), trading space for the factor m; this changes W2's recurrence to
N(h) ~ 2d N(h-1) with space multiplied by m and is the only recursion-level lever identified.
