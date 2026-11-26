# OBL-UNIFORM-QE / Route Q-C: oracle Murray-Williams barrier and witness-sensitive search (2026-11-26)

Status legend: VERIFIED-BY-AUTHOR = checked line by line by the director (Claude family); counts only after a review by another
model family (proof state Q-88090df9cf). CLAIMED = derivation complete as written, not yet independently checked.

Notation. M = SAT/PARITY input length. R(x) in {0,1}^N, N = poly(M) (the budget uses N = O(M^1.7)). Bit i of R(x) depends on at
most t = M^{o(1)} bits of x (locality) and is computable in time M^{o(1)} (uniform budget only where stated). A is a fixed
oracle. MCSP^A[s] = truth tables with an A-oracle circuit of size <= s; A-gates have fan-in <= s, so queries have length <= s.
#C_s = number of A-circuits of size <= s = 2^{O(s^2 log s)} (wire lists), = 2^{M^{o(1)}} for s = M^{o(1)}.

## B0 - owner's oracle extension of Murray-Williams (VERIFIED-BY-AUTHOR)

Claim. For every fixed A (not even computable), every local many-one map R with s, t = M^{o(1)} and N <= 2^{M^{o(1)}} satisfies:
x -> [R(x) in MCSP^A[s]] has depth-3 circuits of size 2^{M^{o(1)}}. Hence it is not PARITY, nor (via XOR chains) SAT.

Proof. For a fixed circuit C, T_C := tt(C^A) in {0,1}^N is a constant string (A fixed). R(x) in MCSP^A[s] iff
OR_{C, |C|<=s} AND_{i<=N} [R(x)_i = (T_C)_i]. Each [R(x)_i = b] is a function of t input bits: CNF with <= 2^t clauses of width t.
Total: OR (2^{O(s^2 log s)}) of AND (N * 2^t) of OR (t) = depth 3, size 2^{O(s^2 log s)} * N * 2^t * t = 2^{M^{o(1)}}.
Hastad: depth-3 circuits for PARITY_M need size 2^{Omega(M^{1/2})}. Contradiction. No uniformity of R and no property of A is
used. Promise/gap versions: the same formula separates YES (size <= s1) from NO (size > s2). SAT: the XOR chain encoding
y(x) = AND_j (z_j XOR z_{j+1} XOR x_j ...) is a projection with O(1) bits of x per output bit, so a local reduction for SAT
composes to a local reduction for PARITY with t' = O(t). Check of the owner's table: all four rows confirmed; free choice of
A does not touch the argument because A enters only through the constants T_C.

Consequence for QE*: local many-one DECISION reductions to MCSP^A with s, t = M^{o(1)} are excluded for every A. QE* sessions
must not pursue them (any A, any uniformity, any gap version).

## B1 - AC0 decoders do not help (VERIFIED-BY-AUTHOR)

Search reduction: f(x) = D(x, W) for every admissible W, where W = some C with tt(C^A) = R(x), or W = BOT if none exists.
f(x) = OR_C [valid(C,x) AND D(x,C)] OR [AND_C NOT valid(C,x) AND D(x,BOT)], valid(C,x) = AND_i [R(x)_i = (T_C)_i].
If D(.,C) is computable by depth-d circuits of size 2^{M^{o(1)}} for each fixed C (in particular D in AC0), f has depth d+4 and
size 2^{M^{o(1)}}: excluded for PARITY and SAT exactly as in B0. So a witness-sensitive reduction needs a decoder outside
quasi-AC0. The owner's budget (D in DTISP(M^1.7, M^{o(1)})) allows PARITY inside D, so B0/B1 do NOT exclude it. Confirmed: the
search direction is open with respect to the PARITY barrier.

## B2 - small target size is unconditionally excluded (VERIFIED-BY-AUTHOR)

Let T_A(s) = deterministic time to evaluate A on all queries of length <= s within space poly(s) (A in PH: T_A(s) = 2^{O(s^k)}).
Deterministic simulation: enumerate C in order (space O(s^2 log s)); for each, stream i = 1..N, compute R(x)_i and C^A(i),
compare; take the first valid C (or BOT), run D. Time 2^{O(s^2 log s)} * N * (M^{o(1)} + s*T_A(s)) + M^{1.7}, space M^{o(1)}.
If s^2 log s + log T_A(s) <= (0.1 - delta) log M, SAT in DTISP(M^{1.8-delta+o(1)}, M^{o(1)}), contradicting SAT not in
DTISP(M^c, M^{o(1)}) for c < 2cos(pi/7) = 1.8019. This holds for total AND non-total versions (BOT is decided exactly).
Consequence: the witness-sensitive route needs s^2 log s + log T_A(s) > 0.1 log M, i.e. s >= (log M)^{Omega(1)}.

## B3 - total reductions with a cheap oracle are excluded (CLAIMED; depends on lemma ROBUST)

Total = R(x) in MCSP^A[s] for EVERY x (no BOT). Cheap A = T_A on length-s queries is M^{o(1)} (e.g. A in P).
Then SAT(x) = EXISTS C [valid(C,x) AND D(x,C)] = FORALL C [valid(C,x) -> D(x,C)], with |C| = M^{o(1)} and the matrix in
DTISP(M^{1.7+o(1)}, M^{o(1)}) (stream i, evaluate C^A(i) cheaply). So
SAT in E := EXISTS^{n^{o(1)}} DTISP(n^{1.7+o(1)}, n^{o(1)}) and in U := FORALL^{n^{o(1)}} DTISP(same).

Lemma ROBUST (CLAIMED). If NTIME(n) is contained in E_c intersected with U_c (short quantifier n^{o(1)}), then every alternation-trading
proof of NTIME(n) not in DTISP(n^c, n^{o(1)}) goes through. In particular this holds for c < 2cos(pi/7).
Proof sketch:
(i) Speedup: EXISTS^{short} DTISP(T,S) is contained in EXISTS^{short + kS} FORALL^{log k} DTISP(T/k, S). The prefix merges with the first block. The dual form is used for U.
(ii) Slowdown: the innermost block (Q n^a) DTISP(n^b) is an NTIME or coNTIME computation on an input of length n^{max}. By the assumption and closure of E and U under complement, it lies in both E and U with exponent c*max. Choose the copy whose short quantifier equals the preceding block and merge.
(iii) The outermost block, which holds the start prefix, is removed by the final slowdown, which yields E and U again. So the proof starting at E(n^a) ends at U(n^{a'}) with a' < a.
(iv) Hierarchy: E_delta(n^a) is not contained in U(n^{a'}). Proof: L(x) = EXISTS w, |w| <= |x|^delta, such that the clocked U-machine M_x rejects (x,w). This is the complement of M_x's U-language, in E at exponent a' + o(1) < a.
Points for the reviewer:
(1) Williams' proofs need the speedup in both quantifier forms.
(2) The o(1) bookkeeping across the n^{a_i}-length inputs.
(3) Whether the cited 2cos(pi/7) proof has exactly this line structure.

Consequence (if ROBUST holds):
- A total witness-sensitive search reduction with cheap A is impossible.
- A total reduction with A in PH directly implies A is not in P, hence P != NP. MMW streaming is not needed, so the route is circular for total reductions: its correctness proof must use properties that fail for every easy oracle.
- Exact logical strength: implies P != NP. No structural handle is known.

## FD - normal form of any witness-sensitive search reduction (VERIFIED-BY-AUTHOR)

Let F_s = { T_C : |C| <= s } (|F_s| <= 2^{O(s^2 log s)}).
- Fibers: Phi_T = R^{-1}(T) for T in F_s. Each fiber is recognisable by a quasi-AC0 CNF.
- BOT region: B = { x : R(x) not in F_s }.
- On Phi_T, SAT equals D(., C) for every C with T_C = T. Each such C is an s-bit advice string for the whole fiber.
- On B, SAT equals D(., BOT), a fixed DTISP(M^1.7, M^{o(1)}) machine.

So the reduction is exactly the following. The instance space is split into at most 2^{M^{o(1)}} locally recognisable fibers plus B. SAT is in DTISP(M^1.7) on B, and in DTISP(M^1.7) on each fiber with s-bit fiber advice. A enters only through which tables are in F_s, i.e. which fibers exist and how hard their advice is to find.

## W1 - first construction attempt and its first failing inference

W1 setup:
- A is any PH oracle.
- R(x)_i = <a_i, x> mod 2 with t-sparse vectors a_i, where {a_i} determines x (N = M^1.7 random sparse checks).

First failing inference: R is injective, so every fiber is a single point.
- Since |F_s| <= 2^{M^{o(1)}}, the set H = R^{-1}(F_s) has at most 2^{M^{o(1)}} instances.
- Every other instance lies in B, where D(., BOT) alone must decide SAT.
- The time-space lower bound only uses the instances Red(y) of an NTIME(n) language. Almost all of them lie in B, so D(., BOT) is the original DTISP algorithm and the construction gains nothing.

Repair (constructive, carried forward):
- R must be lossy, so that the fibers are large and cover the reduction images Red(y).
- The s-bit advice must then help SAT on a whole fiber.

This is the precise remaining obligation:

OBL-QE-W. Construct a local R (N = O(M^1.7), t = M^{o(1)}), a fixed A in PH and a decoder D in DTISP(M^1.7, M^{o(1)}) such that:
(a) every instance Red(y) of a fixed NTIME(n)-complete language lies in a fiber Phi_T with T in F_s;
(b) on each such fiber, D(., C) decides SAT for every C with T_C = T;
(c) the reduction is non-total, or A is not cheap (B3);
(d) s >= (log M)^{Omega(1)} (B2).

(a)+(b) suffice for Route Q-C: under P=NP the MMW streaming algorithm finds a valid C or certifies BOT, so L(Red) is in DTISP(M^{1.7+o(1)}, M^{o(1)}). (c) and (d) are necessary (B3, B2).

Open and not excluded by B0-B3:
- non-total witness-sensitive reductions with expensive A;
- adaptive Turing reductions;
- randomized reductions.

## Book search (owner item: decision-to-search, partial certificates, oracle constructions, exact-one, witness extraction)

Staging proofbook up to seq 16877, excluding APPROACH and RETRACTION rows:

| Topic | Hits | Result |
|---|---|---|
| decision-to-search | 16 | Only MMW Thm 1.3/1.4 citations (16797) and Route E (16779). No transfer usable for OBL-QE-W. |
| partial certificate | 1 | Reformulation series (P = NP => small certificates), already labelled equivalent to P != NP. Not usable. |
| oracle constructions | 89 | Mostly relativization/BGS citations. No PH oracle built for MCSP compression. |
| exact-one | 42 | Succinct Exact-One work. SuccinctExactOneValue is EXP-complete, so no fiber-advice property separates it. |
| witness extraction | 1 | No construction. |

Nothing in the book addresses OBL-QE-W directly. The task is a new construction (question Q-1c841c90f7).
