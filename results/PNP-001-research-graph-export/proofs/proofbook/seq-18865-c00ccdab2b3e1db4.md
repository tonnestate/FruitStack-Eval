# Proofbook seq 18865 — PROOF_STEP

- key: `c00ccdab2b3e1db4`
- at: 1795877686.0150943
- mission: director/pi-t70
- hash: `ae83402bbeb54a6f0dee357909a8106e221f7b10526b325736d5768bafb3827c` (prev `253058c416f063f19a5e4f3a4438893438490b9f75f60cc2c94c9674e61cce34`)
- graph nodes: PB:ae83402bbeb54a6f0dee357909a8106e221f7b10526b325736d5768bafb3827c
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

theory/T70-algebraic-residual-conservation-2026-11-28.md; CLAIMED, Claude family, finite checks verify-T70/residual.py. Provenance: block-synopsis idea Fable text; affine-relation transfer owner; inner-product obstruction review by a Claude instance; residual conservation and Phi-chart owner; algorithm class = Karr + trace partitioning, known, relativizing. Prop 4 + cocycle: residual transport q_{i+1}(F_i z)=M_i(z) q_i(z) with Boolean-matrix M_i exists iff F_i(V_i) subset V_{i+1} (M_l = f*prod_{t<l}(1+q_t), disjoint decomposition of OR; checked on 300 random instances), so existence carries no content beyond inductivity; the content is the size of (q_i,M_i); composition q_{i+2}(F_{i+1}F_i z)=M_{i+1}(F_i z) M_i(z) q_i(z); for constant M the product is trivial, for M_i in a small matrix semigroup powers follow dyadically (T69 Prop 6). Solver circuit S: residuals q_g=w_g+gate_g(w_a,w_b), Phi_S(x,w)=(x,w+S(x)) makes one evaluation a single piece at cost |S|; compact global residual for the exponential alternating computation of D (S called exponentially often) is NOT constructed; non-relativizing only in that q_g uses gate structure, adequacy open.

## Full row (verbatim JSON)

```json
{
 "seq": 18865,
 "at": 1795877686.0150943,
 "problem": "p_vs_np",
 "mission": "director/pi-t70",
 "key": "c00ccdab2b3e1db4",
 "kind": "PROOF_STEP",
 "conclusion": "theory/T70-algebraic-residual-conservation-2026-11-28.md; CLAIMED, Claude family, finite checks verify-T70/residual.py. Provenance: block-synopsis idea Fable text; affine-relation transfer owner; inner-product obstruction review by a Claude instance; residual conservation and Phi-chart owner; algorithm class = Karr + trace partitioning, known, relativizing. Prop 4 + cocycle: residual transport q_{i+1}(F_i z)=M_i(z) q",
 "premises": [
  18828,
  18833,
  18850
 ],
 "statement": "theory/T70-algebraic-residual-conservation-2026-11-28.md; CLAIMED, Claude family, finite checks verify-T70/residual.py. Provenance: block-synopsis idea Fable text; affine-relation transfer owner; inner-product obstruction review by a Claude instance; residual conservation and Phi-chart owner; algorithm class = Karr + trace partitioning, known, relativizing. Prop 4 + cocycle: residual transport q_{i+1}(F_i z)=M_i(z) q_i(z) with Boolean-matrix M_i exists iff F_i(V_i) subset V_{i+1} (M_l = f*prod_{t<l}(1+q_t), disjoint decomposition of OR; checked on 300 random instances), so existence carries no content beyond inductivity; the content is the size of (q_i,M_i); composition q_{i+2}(F_{i+1}F_i z)=M_{i+1}(F_i z) M_i(z) q_i(z); for constant M the product is trivial, for M_i in a small matrix semigroup powers follow dyadically (T69 Prop 6). Solver circuit S: residuals q_g=w_g+gate_g(w_a,w_b), Phi_S(x,w)=(x,w+S(x)) makes one evaluation a single piece at cost |S|; compact global residual for the exponential alternating computation of D (S called exponentially often) is NOT constructed; non-relativizing only in that q_g uses gate structure, adequacy open.",
 "prev": "253058c416f063f19a5e4f3a4438893438490b9f75f60cc2c94c9674e61cce34",
 "hash": "ae83402bbeb54a6f0dee357909a8106e221f7b10526b325736d5768bafb3827c"
}
```
