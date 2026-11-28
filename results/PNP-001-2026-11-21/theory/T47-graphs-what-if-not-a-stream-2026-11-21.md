# T47 — Escalating graph vs computation graph: "What if it is not a stream?" (director deep research, 2026-11-21)

Owner request 2026-11-21: compare escalating graphs and computation graphs for comparabilities that bring P != NP closer; question
"what if it is not a stream". Builds on EGC-001 (theory/oracle-elimination/EGC-001-SIMULATION.md), T26 (MMW locality), T27/T31
(time-space). Labels: [Q] primary source read (file named), [G] recollection, [E] director inference - NOT reviewed, routed to the
organisation as questions (section 6). Nothing here is PROVED. P != NP is not claimed.

## 1. Four computation shapes for search-MCSP^A[s] (N = 2^n truth-table length, s >= n)
| shape | model | magnification statement | conclusion | source |
|---|---|---|---|---|
| S1 path, lex order | one-pass streaming, poly(s) space and update | MMW Thm 1.3 / 1.5 (A in PH) | P != NP | [Q] literature/sources/mmw19/paper.txt |
| S2 escalating graph | event-driven graph, poly(s) config, poly(s) events per input bit | EGC-001: = S1 up to poly | same as S1 | [E, CLAIMED] EGC-001 |
| S3 random-access time-space | RAM/TM, time n^{1+eps}, space n^eps, n^eps advice (n = input length) | CJW Thm 1.2, sparse NP languages, converse also holds | NP not in Circuit[n^k] for every k (NOT P != NP) | [Q] eccc-TR19-118/paper.txt |
| S4 general DAG | circuits size N*poly(s), depth O(log N) / poly(s) | MMW Thm 1.4 bullets 2/3 | NP not in NC^1 / NP not in P/poly | [Q] mmw19 |
Lower bounds against a stronger shape imply those against a weaker one: S4 >= S3 >= S1 (a stream is a random-access algorithm that reads in
order; a TISP machine is a circuit of size about time*space - only the polynomial matters). So "not a stream" asks for a HARDER lower
bound that is still sufficient; its value is only that other techniques live there.

## 2. Is the stream order essential? [E] No.
MMW's Stream-Merge^A[s] [Q, mmw19 Sec. 4] asks for the lex-first minimum circuit C' with C'(x) = C(x) for all x < x_i and C'(x_{i+j-1}) = y_j.
The proof only needs that the set of already-seen positions is described by the index i and that membership is efficiently decidable.
For any fixed polynomial-time computable order pi, replace "x < x_i" by "pi^{-1}(x) < i": the predicate stays in Sigma_3^A (one more
poly-time evaluation), the invariant "C_i agrees with every seen bit" survives because seen bits = values of C_i. Hence MMW Thm 1.2/1.3
should hold for every uniform fixed order. Adaptive (data-dependent) read orders break the index description; but lower bounds for
adaptive random access are S3 and are stronger anyway. Consequence: the hardness is not in the ORDER of the stream.

## 3. Escalating graph with random-access input = CJW model [E]
EGC-001 with events that may read any input position: a configuration of n^eps bits, n^{1+eps} events, a fixed rule table of n^eps
bits (non-uniform part) is a time-n^{1+eps}, space-n^eps algorithm with n^eps advice (RAM, word size O(log n)). By CJW Thm 1.2 [Q]: for a
family of 2^{n^beta}-sparse NP languages, "no such graph decides L_beta (for all beta, one eps)" is EQUIVALENT to NP not in Circuit[n^k]
for all k. So the escalating-graph idea, once it is not a stream, lands exactly on a published equivalence - no gain and no loss.

## 4. Where the non-stream route is blocked (three precise gaps)
G1 sparse diagonalisation [Q, CJW Thm 1.3]: HS65-style diagonalisation gives a (2^{n^eps} * n)-sparse language in TIME[n^{1+eps} polylog]
   (hence in NP) not decidable in time n^{1+eps} with n^eps advice. CJW: making it sparser (2^{n^beta}, beta < eps, same eps) would give
   NP not in Circuit[n^k]. [E] The coupling sparsity exponent = advice exponent looks inherent to counting-based diagonalisation
   (one must have more instances than advice strings to diagonalise). A no-go theorem for "black-box diagonalisation cannot be sparser
   than the advice" would be a genuine barrier result; its absence is the first missing lemma.
G2 time-space via SAT hardness [Q for TS bounds: CJW Thm 1.5; T27 for SAT not in DTISP(n^c, n^{o(1)}), c < 2cos(pi/7)]:
   for s = 2^{(log N)^delta}, MMW only needs time N^{1+o(1)}, far below the known n^{1.8} SAT bound. Transfer would need a reduction
   SAT -> search-MCSP^A[s] of quasi-linear length whose output bits are computable in N^{o(1)} time (local). Barriers:
   (a) for s = poly(n), search-MCSP^A[s] is solvable in 2^{polylog N} time (enumerate 2^{O~(s)} circuits, oracle queries of length n
       cost poly(N)) [E, elementary] - so it cannot be NTIME[m]-hard under quasi-linear reductions unless NTIME[m] is in quasi-poly time;
   (b) Murray-Williams (CCC 2015, ToC 13(4) 2017) [Q abstract]: MCSP is not NP-hard under O(N^{1/2-eps})-time projections,
       unconditionally. General local (non-projection) reductions are not covered - the first missing statement.
   CJW Thm 1.5 shows TS lower bounds survive extreme sparsity (a 1-sparse coNTIME[n^{1+o(1)}] language not in TS[n^c, n^{o(1)}], c <
   golden ratio) - so sparsity alone is not the obstacle; the obstacle is linking the TS-hard sparse language to MCSP.
G3 computation-graph topology (S4) [G]: graph properties alone cannot give superlinear bounds (linear-size superconcentrators exist -
   Valiant 1976, Pippenger 1977); Valiant's depth reduction (remove O(m/loglog m) edges of a size-m, depth-O(log m) DAG to cut the
   depth substantially) [G] is useful only for LINEAR size m = O(N); MMW bullet 2 needs size N*poly(s), where m/loglog m already
   exceeds N. And the locality barrier (T26; CHOPRS Prop. 63 [Q]):
   search-MCSP^A[s] HAS merge-tree circuits with Circuit-Min-Merge oracle nodes of fan-in poly(s) (MMW Lemma 3.1). Any graph-level
   invariant (topology, depth, pebbling, expansion, escalation statistics) that does not look inside nodes is satisfied by these
   circuits and therefore cannot prove the bound.

## 5. Comparabilities that survive (the useful part)
C1 [E] Stream order is irrelevant (sec. 2) - stop investing in order/rewiring variants of escalating graphs.
C2 [Q+E] Escalating graph (random access) = CJW TISP-with-advice model; for sparse NP languages its lower bounds are equivalent to
   NP not in Circuit[n^k] (sec. 3). Fixed-polynomial, not P != NP; for P != NP keep the MMW search-MCSP^A route (S1) or S4 bullet 3.
C3 [E] Every graph route reduces to ONE local object: the poly(s)-input node Circuit-Min-Merge^A[s] / Stream-Merge^A[s]. A superpolynomial
   circuit lower bound for that Sigma_3^A search problem is what S1-S4 all need (T26 line 60-63). The "graph idea" must therefore be an
   invariant of the NODE function that is destroyed by small-fan-in oracle gates - otherwise the locality barrier applies.
C4 [E] Sharpest new targets: (i) G1 no-go for sparse diagonalisation; (ii) G2(b) extension of Murray-Williams from projections to general
   N^{o(1)}-local reductions - either a no-go (closes the non-stream TS route) or a construction (would transfer the SAT TS bounds and,
   with MMW, give P != NP; hence expected to fail, the failing step is the result).

## 6. Routed to the organisation (proof-book questions, K1 lane)
Q-A order-robustness of MMW Thm 1.2/1.3 (sec. 2); Q-B escalating graph with random access vs CJW Thm 1.2 parameters (sec. 3) and G1;
Q-C local reductions SAT -> search-MCSP^A[s] vs Murray-Williams and the quasi-poly obstruction (G2); Q-D graph invariants vs MMW Lemma 3.1
merge-tree circuits (G3, C3). Question ids are recorded in the ledger CONNECTION entry that cites this file.

## 7. Owner analysis merged (2026-11-21, later; owner's [Q]/[E] as stated by the owner)
- MMW Thm 1.7 [Q, mmw19 lines ~240]: MKTP[p(N)] without N*poly(p(N))-size, poly(p(N))-depth circuits => NP not in P/poly; streaming
  bullet => P != NP. MKTP (query any bit of the string) is the natural random-access twin of the escalating graph.
- Controls [E, owner]: (i) cubic bipartite expanders: w*(F(G)) = 2 tw(G) + 1 = Omega(v), yet colourings are found in O(v + |E|) by BFS -
  large basis-robust width does not force decision hardness; (ii) an XOR DAG on an expander has tw(D_C) = Omega(v), size O(v), computes
  a linear function - hardness must belong to the FUNCTION (all implementations), not to one execution graph; (iii) the MMW merge
  graph is a tree (treewidth 1); hardness sits inside the merge nodes (= C3 above).
- Cut lemma [E, owner]: any circuit with kappa cross edges under a gate split gives DCC(f) <= kappa + 1, so log rank M_f <= kappa + 1;
  EQ_m shows single cuts give at most linear bounds. Open: a cumulative cut cost I_graph(f) <= polylog(N)|C| for EVERY circuit.
- Space simulations [owner, C]: Shalunov (circuit evaluation in O(sqrt(q log q)) space), Jaser-Toran (monomial calculus degree d,
  size t => black pebbling space d, time t + d); cell-probe amortised Omega(log^2 N/(loglog N)^2) for dynamic Boolean problems
  (arXiv, 2026-11-08) - method only, polylog.
