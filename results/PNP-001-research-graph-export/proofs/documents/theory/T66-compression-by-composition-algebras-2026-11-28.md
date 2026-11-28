# T66 — Computation compression through composition algebras Phi(F2∘F1)=Phi(F2)*Phi(F1) (2026-11-28)

Status: ATTEMPT / construction space. No contradiction derived; P != NP not claimed. Labels: [U] derived here, elementary; [D] derived here, needs independent check;
[R] recalled, not opened; [?] open. Owner order 2026-11-28 ("Construct, Transfer and Amplify"), objective: T61/T62 compression, success condition alpha*k<1, reduction time o(T/log T).

## 0. Source read (alpo.ge/remark.pdf, 4 pages, narrative)
[READ] Claims a proof of RH with Claude, Lean files linked (14 parts, NOT opened/checked here); I cannot assess the claim. Only the method is used, as stated in the text:
(a) combine two ideas that already work in a toy setting; (b) find the analogous situation; (c) a sign-definite side (q N = M k + R: one side has definite sign, main term on the other, opposite signs => no cancellation);
(d) replace cancellation by iterated Parseval; (e) "multiplicity" obtained by CHAINING lifts, chain length ~ sqrt(X); (f) explicit per-step COST accounting of each lift ("one would stop at 2/3 a priori"); (g) bootstrap.
Transfer to compression: toy setting = affine dynamics; chaining = recursive composition; cost accounting = charge every level; sign-definiteness = a one-sided invariant that cannot cancel.

## 1. Toy setting, rigorous [U]
Representation Phi: step maps -> matrices over a ring, Phi(F2∘F1)=Phi(F2)Phi(F1). For an affine step x -> Ax+b on a d-dimensional state, F^T is computed from Phi(F)^T by repeated squaring: O(d^omega log T) operations, instance size poly(d) log T.
Generalization (Hankel/weighted automaton): an observation sequence y_t has linear recurrence of order d iff its Hankel matrix has rank d; then y_T costs O(d^omega log T) (Fiduccia). So "compressible by a composition algebra" = low Hankel rank of the OBSERVED behaviour (behavioural abstraction = minimal weighted automaton, Schuetzenberger).
Structural property responsible: a finite-dimensional faithful-on-the-orbit representation of the transition semigroup, i.e. the quotient of histories by behaviour is finite-dimensional.
Finite groups/monoids (Barrington-type) give depth compression to log T products but size stays T.

## 2. Hierarchy forces large Hankel rank [U]
If L in DTIME(T) \ DTIME(o(T/log T)) were decided by "build Phi(F) in setup s, then T-fold power", then s + d^omega log T = Omega(T/log T). So for hierarchy-hard L the observed behaviour has Hankel rank d >= (T/polylog)^{1/omega} unless the setup itself does the work. Linear compression alone cannot work for hierarchy-hard L (this is the unconditional negative side of the toy setting); H must enter through a NONLINEAR algebra.

## 3. Nonlinear algebra: relational composition, evaluated with H [D]
Phi(F) = the relation {(x,y): y = F(x)} as a circuit; Phi(F2∘F1)(x,z) = ∃m Phi(F1)(x,m) ∧ Phi(F2)(m,z); circuit size additive, so T-fold composition has size ~T (no compression by itself).
Blocking with alternation (Savitch/Williams style): split the T steps into b blocks, S = space (config size). Sigma_2 instance ∃ m_1..m_{b-1} ∀ i: Seg(m_i,m_{i+1}), size N' ~ b S + (T/b + S) polylog; b ~ sqrt(T/S): N' ~ sqrt(T S) polylog.
Cost under H (SAT in n^k): ∃-part is one oracle-free NP machine making ONE call to a coNP check of size N' => time N'^{k^2} (Sigma_2 in P with exponent k^2, accounting: one coNP decision N'^k, then Cook-Levin on a machine of that running time, then N'^{k*k}). [D, not independently checked]
Result [D]: SAT in DTIME(n^k) => DTISP(T,S) in DTIME((T S)^{k^2/2} polylog). For S = T^beta: exponent k^2 (1+beta)/2; < 1 iff k^2 < 2/(1+beta).
j-level alternation (chaining, the "multiplicity" analogue): b^{j+1} S = T, N' ~ S (T/S)^{1/(j+1)}, time N'^{k^{2j}} (each level squares the exponent: cost of chaining, to be recomputed exactly [?]).
So the construction compresses exactly as far as the boundary information b*S allows: instance size >= boundary data across time cuts.

## 4. Where it fails for the target [D]
The diagonal language in DTIME(T) \ DTIME(o(T/log T)) must simulate arbitrary machines of time o(T/log T), including those with space ~T; its own space is therefore ~T (beta ~ 1), N' ~ T, no compression.
Unconditional reason it cannot be repaired by choosing a small-space hard L: a space-S diagonalizer cannot diagonalize against machines with more space. So the obstruction is information across time cuts (crossing sequences / configuration size), the "information conservation" of earlier results, not the gate encoding.
Consistent with the known family of time-space tradeoffs [R] (Fortnow-van Melkebeek, Williams): they give speedups for small-space computation, not for the full class.

## 5. New directions suggested by the method (not yet results)
1. [?] Boundary information is only the config at the cut. For a SPECIFIC hard L, is there a behavioural quotient of configurations (Myhill-Nerode over the T-step future) much smaller than S? Hankel rank of the future behaviour over a nonlinear algebra (relations, tropical, F3-signed counts of T52) rather than a field.
2. [?] Replace the full config at a cut by a LOCALLY CHECKABLE FINGERPRINT (algebraic hash of the tape plus a checked update rule): size T^alpha, verified by sampled/sumcheck-style consistency; the cost question is whether the fingerprint can be updated in o(T) total without simulating.
3. [?] Sign-definite one-sided invariant (analogue of qN = Mk+R): use T52's signed counts D_J (exactly one sign on the Boolean fibre) as a no-cancellation certificate across the cut.
4. [?] Tensorization: Phi(F x G)=Phi(F) (x) Phi(G) multiplies dimension; test whether tensor depth buys alpha < 1 for k near 1 with the chaining exponent k^{2j} (section 3), i.e. optimize j against beta.

## 6. Dynamic observation spaces (owner Bingo 2.0, 2026-11-28) [U unless marked]
Koopman operator K f = f∘F on functions of the state; V_g = span{g, Kg, K^2 g, ...}. Equivalent objects: Hankel rank of the observation sequence over the whole state family, and the minimal weighted automaton of g.
**Theorem 6.1 (linear case).** If dim V_g = r with basis, K|V_g (r x r) and g's coordinates at x constructed, then g(F^T x) costs O(r^omega log T) field operations (repeated squaring). Not affine F needed.
**Theorem 6.2 (nilpotent case, no matrix powering).** If (K-I)^r g = 0 (index r), then for every T: g(F^T x) = sum_{j<r} C(T,j) ((K-I)^j g)(x) in any ring; mod p the binomials come from Lucas in O(r log T) ops. Proof: K^T = (I+(K-I))^T, binomial theorem for commuting operators, truncate by nilpotency. Checked exactly: the owner's system (r=3, T<30) and 200 random unipotent triangular Boolean systems on 5 variables (6 values of T each): 0 violations.
Owner example: p=ab, y'=y+p, z'=z+y over F2: z_T = z_0 + T y_0 + C(T,2) a b (verified for all 16 initial states, T<40; for T=1000000003, a=b=y0=1, z0=0 the formula gives y_T=0, z_T=0).
**Cost account (what 6.1/6.2 do NOT give).** Finite dimension != efficient construction. Needed: (i) closure/basis: g_j=(K-I)^j g as explicit objects, g_{j+1}=g_j∘F-g_j is a substitution; size can double in degree each step; (ii) index r; (iii) evaluating g_j at x. Total = r*(size of g_j, evaluation) + r log T. The compression is real only when r and size(g_j) are T^{o(1)}.
**Where the dimension explodes (exact).** Binary counter c' = c+1 on m bits (unipotent, triangular, Boolean): nilpotency index of the top bit is 2^{m-1}+1 (computed m=2..5: 3,5,9,17). So "compactly described, unipotent, triangular" does not imply small r; the index of a clock alone is ~ the period. Any T-step clock inside the computation costs r ~ T unless the clock enters as the parameter T (binary) rather than as state.
**Consequence for the target [U].** Combined with section 2: for a hierarchy-hard L the Koopman space of its universal step map restricted to the reachable family has dimension >= (T/polylog)^{1/omega}-type bounds when the setup is o(T); so Theorem 6.1/6.2 apply only after a transformation that REMOVES the information that makes the dimension large. The open mathematical question is the class of (F,g) where such a transformation (change of observation, T4 signed cancellation, T38 behavioural quotient, T52 elimination) keeps r small AND the language remains hierarchy-hard. No such class is known.
**Bingo 2.0 candidates.** CONSTRUCTION: V_g (T38 quotient) x T52 signed moments (exact one-sided counts) x T66 relational blocks. AMPLIFICATION: tensor/recursive composition of (F,g) with independent index bounds r_1 r_2; chaining cost k^{2j} (section 3). TRANSFORMATION: unipotent/nilpotent filtration of the Koopman space (lower central series of the group generated by F). SYNTHESIS: only if a class with hard L and small r is exhibited.

## 7. Composition Koopman x Lucas: nilpotent compression is orbit-length reduction (2026-11-28, discovery mode, derived without targeting an obligation)
Object: comp:koopman-lucas-period-duality = Theorem 6.2 (nilpotent binomial expansion) composed with Lucas' theorem (C(T+p^k,j) = C(T,j) mod p for j<p^k).
**Theorem 7.1 (period-index duality) [U, short proof; exact checks].** Let F act on a finite set X, g: X -> F_p with minimal Koopman nilpotency index r (so g_j=(K-I)^j g, j<r, are linearly independent). Then T -> g(F^T x) has minimal period exactly p^ceil(log_p r) (as a function of x and T).
Proof: g_T = sum_{j<r} C(T,j) g_j (Thm 6.2). Lucas gives period dividing p^k for p^k >= r. Independence of the g_j and of T -> C(T,j) mod p (distinct degrees) shows a period P must satisfy C(T+P,j)=C(T,j) for all j<r, in particular j=r-1, whose minimal period is p^ceil(log_p r). QED.
Checked: 60 random unipotent triangular systems on 5 Boolean variables, 0 mismatches; counter m=2,3,4: r = 3,5,9 and period 4,8,16.
**Theorem 7.2 (nilpotent iff p-group dynamics) [U; exact check on 300 random permutations].** For a permutation F, K is unipotent (all observations nilpotent) iff every cycle length is a power of p; the index is at most the longest cycle (K^{p^a}=I gives (K-I)^{p^a}=0).
**Consequences (derived properties, none aimed at an obligation).**
1. Compression by Theorem 6.2 is exactly reduction of T modulo the observation period p^k <= p*r: a T-step simulation becomes a (T mod p^k)-step one (cost r polynomial terms). Nothing beyond period reduction.
2. Genuine compression beyond periodicity needs a NON-nilpotent K on V_g whose minimal polynomial has multiplicative order much larger than its degree: LFSR-type dynamics. Checked: 16-bit LFSR, period 65535, T=5*10^5 by 16x16 matrix powering equals the simulation. The compressibility measure is log(period)/dimension; a nilpotent K has ratio <= log p.
3. Therefore a hierarchy-hard computation compressible by Theorem 6.1 must expose observations whose Koopman space is cyclic with high-order minimal polynomial, dimension r = T^alpha, and period >= T (otherwise T is trivially reduced); the problem moves to: which compactly described F have observations with small-degree, high-order minimal polynomial. Nilpotent/unipotent triangular systems are provably excluded as sources of compression (T-reduction only).
Status: derived and finitely checked; independent review and novelty check pending (the individual ingredients are standard: Lucas, linear recurrences over finite fields [R]).
