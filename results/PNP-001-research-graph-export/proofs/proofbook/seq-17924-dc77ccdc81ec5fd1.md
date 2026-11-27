# Proofbook seq 17924 — PROOF_STEP

- key: `dc77ccdc81ec5fd1`
- at: 1795764601.7293243
- mission: director/closure-exclusions
- hash: `056117a65da3e576e4e9edd573627deed3368e9cd77e6130ccd3adf21b37b837` (prev `46bd0361b591f032a9a12eaed0658bd2ff1ba7195d1db3219af3765ac4362cc0`)
- graph nodes: PB:056117a65da3e576e4e9edd573627deed3368e9cd77e6130ccd3adf21b37b837
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

BLOCK NORMALIZATION OF STRUCTURE VERSUS LOCAL INFORMATION (owner question 2026-11-27; PI theorem and limits; CLAIMED, Claude family). (1) Owner observation, checked. A bag of k vertices of G becomes 2k parameters. Formal states go from 3^k to 9^k; locally admissible states stay 3^k (3 of 9 pairs (p,q) per vertex, 17922). Solution information is identical, and the coordinate change of 17923 inverts the expansion. (2) Theorem (PI). Let H be a constraint primal graph and P a partition of its variables into connected blocks of size <= t, with quotient graph H/P. Then tw(H/P) <= tw(H) <= t(tw(H/P)+1) - 1, and likewise for pathwidth. Proof: H/P is a minor of H (contract connected blocks), and treewidth is minor-monotone. For the upper bound, substitute each block into the bags of an optimal decomposition of H/P. Both bounds are attained: J of 17923 (quotient G, tw = max(tw(G),1)) and the block form G[K_2] (17922/17923, tw = 2 tw(G)+1). So the variable-level width can sit anywhere in this interval for the same quotient structure. (3) Normalized measure. Merge each block into one compound variable whose domain D_b is the set of locally admissible block states. Define the semantic width w_sem = min over decompositions of H/P of max over bags B of sum_{b in B} log_3 |D_b| (weighted treewidth with weights log|D_b|; the term is from the literature, cited from memory, unverified). w_sem depends only on H/P and the |D_b|, so it is invariant under every blockwise bijective recoding. For the prism block form, D_b has 3 elements and H/P = G, so w_sem = tw(G)+1 = the value for G itself. Structural expansion and semantic conservation are then two coordinates of one exact statement. (4) Limit. The invariance holds for block-local bijections only. A global bijection of F3^n can map a solution set of size 3^k onto F3^k x {0}, whose primal graph has no edges. So no width measure is invariant under arbitrary bijections. The only fully invariant quantity is the number of solutions (U_G(1)), which is #P-type information and says nothing about deciding (edgeless G has the most colourings). A general normalization therefore has to fix the admissible class of recodings, and block-local is the natural exact class. (5) Consequence for the universal function: U_G is invariant under blockwise recodings (monomial substitutions, 17913, Fable A2) and carries the semantics. w_sem is the matching structural invariant, and both are preserved by the whole prism pipeline. No lower bound, no running-time claim; no obligation closed.

## Full row (verbatim JSON)

```json
{
 "seq": 17924,
 "at": 1795764601.7293243,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "dc77ccdc81ec5fd1",
 "kind": "PROOF_STEP",
 "conclusion": "tw(H/P) <= tw(H) <= t(tw(H/P)+1)-1 for connected blocks, both tight; semantic width invariant under blockwise bijections only",
 "premises": [
  17913,
  17922,
  17923
 ],
 "statement": "BLOCK NORMALIZATION OF STRUCTURE VERSUS LOCAL INFORMATION (owner question 2026-11-27; PI theorem and limits; CLAIMED, Claude family). (1) Owner observation, checked. A bag of k vertices of G becomes 2k parameters. Formal states go from 3^k to 9^k; locally admissible states stay 3^k (3 of 9 pairs (p,q) per vertex, 17922). Solution information is identical, and the coordinate change of 17923 inverts the expansion. (2) Theorem (PI). Let H be a constraint primal graph and P a partition of its variables into connected blocks of size <= t, with quotient graph H/P. Then tw(H/P) <= tw(H) <= t(tw(H/P)+1) - 1, and likewise for pathwidth. Proof: H/P is a minor of H (contract connected blocks), and treewidth is minor-monotone. For the upper bound, substitute each block into the bags of an optimal decomposition of H/P. Both bounds are attained: J of 17923 (quotient G, tw = max(tw(G),1)) and the block form G[K_2] (17922/17923, tw = 2 tw(G)+1). So the variable-level width can sit anywhere in this interval for the same quotient structure. (3) Normalized measure. Merge each block into one compound variable whose domain D_b is the set of locally admissible block states. Define the semantic width w_sem = min over decompositions of H/P of max over bags B of sum_{b in B} log_3 |D_b| (weighted treewidth with weights log|D_b|; the term is from the literature, cited from memory, unverified). w_sem depends only on H/P and the |D_b|, so it is invariant under every blockwise bijective recoding. For the prism block form, D_b has 3 elements and H/P = G, so w_sem = tw(G)+1 = the value for G itself. Structural expansion and semantic conservation are then two coordinates of one exact statement. (4) Limit. The invariance holds for block-local bijections only. A global bijection of F3^n can map a solution set of size 3^k onto F3^k x {0}, whose primal graph has no edges. So no width measure is invariant under arbitrary bijections. The only fully invariant quantity is the number of solutions (U_G(1)), which is #P-type information and says nothing about deciding (edgeless G has the most colourings). A general normalization therefore has to fix the admissible class of recodings, and block-local is the natural exact class. (5) Consequence for the universal function: U_G is invariant under blockwise recodings (monomial substitutions, 17913, Fable A2) and carries the semantics. w_sem is the matching structural invariant, and both are preserved by the whole prism pipeline. No lower bound, no running-time claim; no obligation closed.",
 "prev": "46bd0361b591f032a9a12eaed0658bd2ff1ba7195d1db3219af3765ac4362cc0",
 "hash": "056117a65da3e576e4e9edd573627deed3368e9cd77e6130ccd3adf21b37b837"
}
```
