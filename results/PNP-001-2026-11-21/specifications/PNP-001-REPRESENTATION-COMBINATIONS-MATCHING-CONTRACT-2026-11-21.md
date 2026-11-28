# PNP-001 — Owner analysis: combinations across SAT, graph and algebra representations (2026-11-21, ~22:00)
Working copy for agents (authoritative text: the owner's message). Every literature statement below is the owner's CANDIDATE reading:
verify at the primary source (exact theorem number, hypotheses, constants) before use. Nothing here is accepted or PROVED.

## Principle
Do not invent another representation. Find a structural property that provably cannot be removed cheaply when moving between two or
more representations. Avoid known failed inferences: independent combination of CRT solution sets, tensor rank = computational cost,
plain rank and MUS counts. Controlled families: disjoint clauses, clause chains, recursive clause structures (exact counts, transfer
matrices known).

## 1. Positive 1-in-3-SAT with two occurrences = perfect matching (register D-002)
Cubic graph G, variable x_e per edge, clause x_e1 + x_e2 + x_e3 = 1 per vertex: #SAT(F_G) = #PM(G). Decision in P; counting #P-complete
on cubic bipartite graphs; planar counting in P (FKT); cubic bipartite graphs always have a PM (answer always YES). Control case that
separates existence / count / representation complexity. Task: run #SAT methods, algebraic rank measures and certified knowledge
compilation on these cases at once -> which invariants measure DECISION hardness and which only complex solution spaces (a filter).

## 2. Tensor-graph rewriting as a #SAT proof system
de Beaudrap-Kissinger-Meichanetzidis, "Tensor Network Rewriting Strategies for Satisfiability and Counting" (ZH calculus); "Proof Systems
for Tensor-based Model Counting" (AAAI; two proof systems, simulations, exponential separations). Missing statement: a lower bound for
EVERY admissible rewriting sequence inside the chosen system for our families (disjoint, chains, recursive, GF(3)-blind kernels, F_16).
Already open: Q-556d8094b7 (ZH rewriting as a proof system, corrected), Q-2bdb903445 (retracted predecessor) - extend, do not duplicate.

## 3. SAT -> UNSAT lifting (Berkholz-Micun, "Proof Systems Based on Structured Circuits", SAT 2026, Theorem 13)
CNF phi, n vars, width <= k, <= log n occurrences per variable: RepSize(phi) <= O(t^2 n^{2k^2}), t = refutation size of Z(phi) in the
named structured proof systems (no weakening rule). Inverted: t >= sqrt(RepSize(phi) / O(n^{2k^2})). 1-in-3 per vertex as 4 CNF clauses;
each edge variable in 6 clauses, width 3 -> loss n^18. Task: explicit cubic graph family whose PM / 1-in-3 function needs exponential
d-SDNNF size. The K_{n,n} DNNF bound does not suffice (degree grows). Prior ledger: seq 49 Bova-Capelli-Mengel-Slivovsky "Expander CNFs
have Exponential DNNF Size"; seq 73 (covers the Boolean form only); seq 1846 (SAT 2026 tree decision diagrams).

## 4. Pfaffian number (Pant-Singh 2026, "Exponential Lower Bounds for the Pfaffian Number of Graphs")
PfNum(G_n) >= (8/3)^{floor(n/6)}, witnessed by cubic bipartite graphs. A bound on one algebraic representation, NOT on SAT time. Question:
can a causal tensor-rewriting system bypass it by different factorisation of intermediates, and which bounded rewriting systems remain
bound by it? Prior: T7/T8 Pfaffian-permanent theory (Q-780c8e9527, Q-9fdb3e80e4).

## 5. Factorised join representations (Berkholz-Vinall-Smeeth, ICDT 2026)
Size_{union,product} >= M^{Omega(tw)} for suitable database instances. Question: which of these bounds survive if every relation is the
fixed R_1in3 = {100, 010, 001}? Compare with the upper bound of de Colnet-Szeider-Zhang (IJCAI; compilation exponential in incidence
treewidth). Planar matching graphs are the control: high treewidth, counting still polynomial.

## 6. Dynamic representation switching (Staudt et al., "Exploiting Dynamic Sparsity in Einsum", NeurIPS 2025; AAAI 2026 "Proof Systems
That Tightly Characterise Model Counting Algorithms")
Question: what does the best sequence of admissible representation switches cost, including conversion costs? Do dynamic switches inside a
defined proof system need less work or only redistribute it?

## 7. Polynomial calculus -> pebbling (Jaser-Toran, "Pebble Games and Algebraic Proof Systems", LMCS 2026)
Monomial-calculus refutation of a pebbling formula with degree s and size t -> black-pebbling strategy with space s, time <= t+s. Question:
a resource-preserving translation (degree, size, space controlled) between one of our GF(3)-blind families (F_8 quadratic NS certificate,
F_16 degree-2 PC bound) and pebbling formulas - or a proof that none exists.

## 8. Test matrix (proposed, not executed) and certification
Disjoint/chained 1-in-3 (transfer matrix vs contraction, separator size); F_8/F_16 (certificates vs rewriting); cubic bipartite (Pfaffian vs
other tensor forms); cubic expanders (DNNF + lifting); planar matching (control); XOR-SAT and 2-SAT (negative controls: an invariant that
marks them hard is wrong). Certified counting: CPOG (Bryant-Nawrocki-Avigad-Heule, Lean 4 checked) as an independent layer for existing
exact counts. SAT 2026 "Factoring Learned Clauses" (XOR/ITE extraction) on our XOR/Carry encodings.

## 9. Owner priorities
1 SAT -> matching -> DNNF -> UNSAT proof system (missing: d-SDNNF lower bound for a bounded-degree family);
2 SAT -> tensor graph -> dynamic representation switches (missing: representation-independent resource comparison incl. conversions);
3 SAT -> PC -> pebbling time-space (missing: resource-preserving translation for our families).
First: embed the cubic bipartite 1-in-3 family completely into the lifting theory and the Pfaffian/tensor theory.

## Restrictions
Mathematical research only; no architecture/PlumMe/orchestration change; do not interrupt running sessions or the Pareto run; no CI.
Every result labelled PUBLISHED THEOREM / INDEPENDENTLY PROVED / OPEN / REFUTED. Never claim P != NP.
