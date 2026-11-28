# PNP-001 — Contract K6: Perfect-Matching Boundary Rank and SAT-to-UNSAT Lifting
Owner contract 2026-11-21 (~22:15, marked "Extrem Critical Execution"; authoritative text: the owner's message; this file is its working
copy for agents). Programme P3 (proof complexity). Status OPEN. Do not claim P != NP. Do not infer high cut rank from the NUMBER of perfect
matchings. Continues Q-12f2991045 (combinations contract, priority 1) - same line, do not duplicate.

## 1. Objective
Do bounded-degree Exact-One-SAT formulas from cubic bipartite expanders need exponential d-SDNNF size for EVERY vtree, and does
Berkholz-Micun lifting then give exponential refutation lower bounds?

## 2. Primary sources (complete proofs)
1 Berkholz-Micun, "Proof Systems Based on Structured Circuits", SAT 2026: Theorem 13, Theorem 21, Lemma 22. 2 Esperet et al., "Exponentially
Many Perfect Matchings in Cubic Graphs". 3 Knowledge compilation: rectangle partitions, communication-matrix rank, d-SDNNF, bounded
treewidth. 4 Existing lower bounds for perfect-matching constraints / structured compilation (also ledger seq 49, 73: Bova-Capelli-Mengel-
Slivovsky, expander CNFs, DNNF).
Read proof-book entries T1-4 and F1 and the existing `pm_cutrank.py` experiments (director: locations not found under
/root/fruits/research/PNP-001 in a quick check - locate them, e.g. in the FruitStack-Eval results branch, or record them as missing).
Confirm the T1 cut-rank argument is about the exact edge-variable matching function, not another monotone function.

## 3. SAT translation
Cubic G, variable per edge, EXACTLY_ONE per vertex. Prove bijection with perfect matchings; clause width <= 3; each edge variable in six
clauses; check all size/occurrence requirements of Theorem 13.

## 4. Boundary-signature rank lemma
Partition E = A u B; boundary d(A,B) = vertices incident to edges of both sides. A-feasible signature sigma = set of boundary vertices
matched by a valid partial matching on A; sigma extendible if a valid partial matching on B covers exactly the complementary boundary
vertices. Prove or refute (the owner's formula arrived truncated; intended reading, to be confirmed):
  rank(M_{A,B}) = |{sigma : sigma extendible}|  over every field.
Proposed proof: partition the communication matrix into disjoint all-one blocks indexed by compatible signatures. Check every condition:
invalid partial assignments, isolated vertices, arbitrary fields, empty cases. Search the matching communication-complexity literature
before any novelty claim.

## 5. Independent-switching lemma
Perfect matching M0, r vertex-disjoint M0-alternating cycles, each with a boundary vertex whose cycle edges lie on opposite sides:
investigate rank(M_{A,B}) >= 2^r. Prove injectivity of signatures under independent cycle flips. Then: do such cycles exist in sufficient
number across ALL balanced partitions of an explicit cubic expander family? Do not assume. If only r = Omega(n / log n), report exactly
that (superpolynomial may still matter).

## 6. Mandatory negative control: prism graphs G_m = C_m x K_2, m even
Connected, cubic, bridgeless, exponentially many PMs, bounded treewidth. Verify polynomial-size d-SDNNFs; explain why this refutes
"exponentially many PMs => exponential d-SDNNF size". Reproduce small exact rank calculations independently.

## 7. Main open theorem
Explicit infinite family of cubic bipartite expanders G_n such that for EVERY vtree T some T-induced cut has rank(M_{A,B}) >= 2^{Omega(|V|)};
then the rank-to-d-SDNNF argument (if it applies) gives the representation bound. Do not infer the all-vtree statement from random
balanced cuts. If it fails: a vtree with subexponential rank at every relevant cut, or another decisive counterexample. Separate
combinatorial expansion from independent realisability of boundary signatures.

## 8. Lifting (only after sec. 7)
Berkholz-Micun Theorem 13 with exact proof-system assumptions (no weakening); k = 3, factor n^18; explicit refutation lower bound, scoped to
the applicable structured systems. Compare with Lemma 22 (Vertex Cover). New theorem, known corollary, or already published?

## 9. Independent critic (separate role)
PM correspondence; boundary-rank identity; alternating-cycle criterion; "for every vtree"; expander assumptions; lifting requirements;
literature; no transfer to general SAT algorithms or P != NP. Every computation independently reproducible.

## 10. Deliverable K6-REPORT.md
A published-theorem audit; B boundary-signature rank lemma; C switching lemma or counterexample; D exact small instances; E strongest
proved all-vtree bound; F lifting application; G novelty; H critic's verdict.
Restrictions: preserve proof book and running experiments; no production, orchestration or CI changes.
Final objective: a genuine new lower bound for the Exact-One/PM family, or the first false implication with a verified counterexample.

## Director note (2026-11-21 ~22:25)
pm_cutrank.py (owner-supplied) is now at /root/fruits/research/PNP-001/checks/pm_cutrank.py, first run output in pm_cutrank.out.txt next to
it. Observed: rank of every tested cut <= #PM and mostly equal to #PM (5,6,8,12). Since every 1-entry of M_{A,B} is one perfect matching,
rank <= #PM always holds; on these small random cubic graphs the test therefore saturates at #PM and cannot show growth like
2^(#crossing structures). Needs: bipartite expander families with many PMs, larger n, all vtrees (not random cuts), and an independent
second method. Scope: exploratory data only.

## Owner source check (2026-11-21 ~22:40)
"T1-4" = T1 Satz 4 (theory/T1-ie-compression-and-barrier.md; proof-book entries 58-61, positive 2-CNF only - the transfer to PM is the
open problem). F1 = staging proof-book entry 5228 (F1 sparsity cap; not in the LIVE export): each perfect matching splits uniquely into its L- and R-part, giving exactly one 1-entry, so rank(M_{A,B}) <= #PM. pm_cutrank.py: see director note above. Sec. 4
identity confirmed as intended reading: rank_F(M_{A,B}) = #{boundary signatures realisable on one side by an internally valid partial
assignment and completed by the complementary signature on the other side} - still to be proved.

## Candidate chain (owner deep research 2026-11-21 ~23:00; CANDIDATE, audit: Q-5967b9ee0c)
Expander 2-CNF (Bova-Capelli-Mengel-Slivovsky, DNNF 2^{Omega(n)}) -> Phi_G = AND_{uv} EXACT1(x_u, x_v, z_uv), exists z Phi_G = H_G =
AND (not x_u or not x_v), unique extension; forgetting z in a DNNF (literals -> true) does not increase size, so DNNF(Phi_G) >= 2^{Omega(v)}
-> Phi_G is a width-3 CNF, <= 9 occurrences, N = 5v/2 -> Berkholz-Micun Thm 13: 2^{cv} <= C t^2 N^18, t = 2^{Omega(N)} for the covered
structured systems without weakening. Limits: Lemma 23 (Z(phi) has polynomial Resolution refutations) - no transfer beyond those systems;
likely a direct corollary of Lemma 22 (H_G is the vertex-cover CNF); does NOT settle K6 (PM encoding has 2 occurrences per edge variable;
parity obstruction against 3-terminal PM equality gadgets). Supporting: Berkholz-Mengel-Wilhelm STACS 2024 Thm 10 / Lemma 11.
Owner check (2026-11-21, later): the candidate chain encodes INDEPENDENT SETS (vertex variables + edge auxiliaries), NOT perfect matchings;
book it separately from K6. Lemma 23 holds for every CNF: Z(Phi_G) has polynomial Resolution refutations, so no transfer to Resolution or
stronger systems. Expected outcome of Q-5967b9ee0c after independent review: derived theorem (corollary of known results), closed.
