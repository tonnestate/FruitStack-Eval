# T24 — Which compressions of circuits into fixed-width CNF can exist at all? (PI, 2026-11-17)

STATUS: elementary lemmas (K1 owner's counting argument, generalised; K2 from Dell–van Melkebeek, abstract-level source) plus
literature. No computation. Not reviewed (subagents unavailable until 2026-11-19). Not in the ledger.
Owner decision: before any computation, clarify mathematically which compression can be possible at all.

## Setting
Target (owner's boxed obligation): for every fixed k, exact #SAT/SAT for all n-input circuits of size n^k in time 2^n/n^{ω(1)}
(this is the hypothesis of Williams' NEXP ⊄ P/poly theorem — open; not a consequence of the Oct 2026 papers).
Route examined here: reduce the circuit to a w-CNF on N variables and run the claimed fixed-width algorithm, time
2^{C_w N (log log N)^2/sqrt(log N)} (formal) — this beats 2^n only if N <= n·sqrt(log n)/(C_w (log log n)^2) (up to constants).

## K1 — function-preserving encodings (owner's lemma, generalised to width w)
An existential encoding is a w-CNF φ(x, y) on N >= n variables with C(x) = 1 ⇔ ∃y φ(x, y) = 1.
(i) There are at most (2N+1)^w possible clauses of width <= w, hence at most 2^{(2N+1)^w} encodable functions.
(ii) Fix any M inputs; each of the 2^M subsets is the 1-set of a function with a DNF circuit of size O(nM).
With size budget n^k: M = n^{k-1}/c functions-count 2^{n^{k-1}/c}.
Hence every size-n^k circuit has a width-w encoding with N variables only if (2N+1)^w >= n^{k-1}/c, i.e.
    N >= Ω(n^{(k-1)/w}).
Consequences: for w = 3 and k >= 5 (owner's case), N = n·polylog is impossible; in general N = n·polylog forces w >= k-1 (up to
log factors). For w >= k-1 counting gives NO obstruction — and the claimed algorithms hold for every fixed width. So the owner's
bound is real but width-specific; it does not exclude the route with width w = Θ(k).
(Tseitin: w = 3, N = n + s — far above the counting bound; it is the blow-up, not counting, that kills Tseitin at size n^{1+ε}.)

## K2 — satisfiability-preserving polynomial-time reductions (conditional)
Dell–van Melkebeek (STOC 2010; ECCC TR10-038, abstract): for d >= 3, ε > 0, if satisfiability of n-variable d-CNF has a
protocol of cost O(n^{d-ε}) then coNP ⊆ NP/poly. A k-CNF on n variables with Θ(n^k) clauses is a circuit of size O(n^k).
A polynomial-time satisfiability-preserving reduction to a w-CNF on N = n·polylog variables has output size O(N^w) = Õ(n^w) bits;
for w < k this is a compression of k-SAT to O(n^{k-ε}) bits. Hence, unless coNP ⊆ NP/poly, such reductions need w >= k.
Not covered: reductions running in super-polynomial (e.g. 2^{o(n)}) time — the 2^n/n^{ω(1)} budget would allow them.

## Known positive encodings
- Tseitin: any circuit, w = 3, N = n + s (parsimonious).
- Linear-size series-parallel circuits: Valiant/Calabro depth reduction, OR of 2^{n/d} k-CNFs with k = 2^{2^{O(d)}}
  (Jahanjou–Miles–Viola, proof of Cor. 3(2')): N = n + n/d, constant width. Linear-size log-depth: width n^ε (not fixed).
- OpenAI ETH manuscript Cor. 1.4 (read in source, paper.txt l.122–128): E^NP ∌ circuits of size c·n·sqrt(log n), infinitely
  often — this is exactly the Tseitin + clause-linear-bound transfer (supersedes T23 §3, which re-derived it).

## Conclusion (the precise remaining gap for the encoding route)
For each fixed k one needs function- or satisfiability-preserving encodings of all size-n^k circuits into width-w CNF with
w >= k-1 (forced by K1; w >= k by K2 for poly-time reductions unless coNP ⊆ NP/poly) and N <= n·sqrt(log n)/(C_w (loglog n)^2)
variables, computable within the time budget — and the hidden constant C_w of the claimed algorithms must be controlled as w grows
with k. Nothing known rules this out; no construction is known beyond series-parallel/linear size. The non-encoding route
(direct contraction/interpolation on circuits, owner's box) is open; its relevant cost measure is contraction width
(2^{O(treewidth)} by Markov–Shi), not local bond dimension.
Owner's corrections adopted: (§2) local index dimension is irrelevant, contraction width matters; (§3) deg Z(t) <= Σ deg T_v
(no depth-induced degree explosion for locally parametrised contractions).
