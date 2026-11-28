# Proofbook seq 18646 — CONNECTION

- key: `19f08ddffd2bfda0`
- at: 1795864515.397118
- mission: director/mechanism-extraction
- hash: `26cf8915df862b881c996716ba5257812d86ae495275f84abbf9195a039310cb` (prev `d040626c20acfc697b31e6f053ce550ce77462992eb51f6af1b8063eb05d012a`)
- graph nodes: PB:26cf8915df862b881c996716ba5257812d86ae495275f84abbf9195a039310cb
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18646,
 "at": 1795864515.397118,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "19f08ddffd2bfda0",
 "kind": "CONNECTION",
 "about": [
  "mech:x17237-weighted-subst-owner-bound-2026-11-26-director-check-"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x17237-weighted-subst-owner-bound-2026-11-26-director-check-",
  "name": "x17237 WEIGHTED-SUBST (owner bound 2026-11-26, director check and split;",
  "preconditions": "(R2) Given R1, max_j L(A_j) <= N^{2+beta-Delta-CK beta} suffices: every anti-checker output bit needs a SUBQUADRATIC formula; the weights mu_j matter only up to the factor L(V) = N^{O(beta)}.; Unconditional counterpart (CJW20-GAP seq 17198): for every anti-checker generator with L(V) <= T^C, some output bit has L(A_j) >= N^{2+beta-xi-CK beta}; deriving the opposite from the assumption is the obligation.; OPS 2021 p.23 (local copy toc-v017a011 l.1168-1172) names exactly R2 (rounds re-inspect earlier y_j) as the obstacle under NP subset Formula[poly].; (R2) Given R1, max_j L(A_j) <= N^{2+beta-Delta-CK beta} suffices: every anti-checker output bit needs a SUBQUADRATIC formula; the weights mu_j matter only up to the factor L(V) = N^{O(beta)}.",
  "effect": "Substituting a formula for each output bit A_j at each of its mu_j(V) occurrences gives exactly L(F) <= sum_j mu_j(V) L(A_j); sum_j mu_j(V) = L(V).; Director split, with t = N^{K beta}: (R1) L(V) <= N^{2+beta-Delta} is needed;; V is an NP predicate on T = N^{O(beta)} bits, so ANY fixed polynomial bound L(V) <= T^C (C independent of beta) suffices for small beta - but NP subset P/poly gives V only circuits;",
  "limitations": "V is an NP predicate on T = N^{O(beta)} bits, so ANY fixed polynomial bound L(V) <= T^C (C independent of beta) suffices for small beta - but NP subset P/poly gives V only circuits;; R1 is 'V in Formula[poly]', supplied by NP subset Formula[poly] (OPS's stronger hypothesis), not by NP subset P/poly.; (R2) Given R1, max_j L(A_j) <= N^{2+beta-Delta-CK beta} suffices: every anti-checker output bit needs a SUBQUADRATIC formula; the weights mu_j matter only up to the factor L(V) = N^{O(beta)}.",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 17237 (extraction preserves, never upgrades the status)",
  "representations": "polynomial, circuit, formula",
  "interfaces": "polynomial, circuit, formula, bound:exactly L(F), bound:N^{K, bound:L(V) <= N^{2+beta-Delta}",
  "provenance": "PROOF_STEP seq 17237 key 757a33c99dfb9f96 mission director/closure-exclusions",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "polynomial",
   "circuit",
   "formula"
  ],
  "guarantees": [
   "Substituting a formula for each output bit A_j at each of its mu_j(V) occurrences gives exactly L(F) <= sum_j mu_j(V) L(A_j); sum_j mu_j(V) = L(V).",
   "Director split, with t = N^{K beta}: (R1) L(V) <= N^{2+beta-Delta} is needed;",
   "V is an NP predicate on T = N^{O(beta)} bits, so ANY fixed polynomial bound L(V) <= T^C (C independent of beta) suffices for small beta - but NP subset P/poly gives V only circuits;"
  ],
  "bounds": [
   "exactly L(F)",
   "N^{K",
   "L(V) <= N^{2+beta-Delta}",
   "N^{O",
   "L(V) <= T^C",
   "L(V) >= t^{2+1/K-o(1)}",
   "has >= t^{2+1/K-o(1)}",
   "L(A_j) <= N^{2+beta-Delta-CK"
  ],
  "compatibility": [
   "(R2) Given R1, max_j L(A_j) <= N^{2+beta-Delta-CK beta} suffices: every anti-checker output bit needs a SUBQUADRATIC formula; the weights mu_j matter only up to the factor L(V) = N^{O(beta)}."
  ],
  "assumptions": [
   "(R2) Given R1, max_j L(A_j) <= N^{2+beta-Delta-CK beta} suffices: every anti-checker output bit needs a SUBQUADRATIC formula; the weights mu_j matter only up to the factor L(V) = N^{O(beta)}.",
   "Unconditional counterpart (CJW20-GAP seq 17198): for every anti-checker generator with L(V) <= T^C, some output bit has L(A_j) >= N^{2+beta-xi-CK beta}; deriving the opposite from the assumption is the obligation.",
   "OPS 2021 p.23 (local copy toc-v017a011 l.1168-1172) names exactly R2 (rounds re-inspect earlier y_j) as the obstacle under NP subset Formula[poly]."
  ]
 },
 "connection": "MECHANISM mech:x17237-weighted-subst-owner-bound-2026-11-26-director-check-: Substituting a formula for each output bit A_j at each of its mu_j(V) occurrences gives exactly L(F) <= sum_j mu_j(V) L(A_j); sum_j mu_j(V) = L(V).; Director split, with t = N^{K beta}: (R1) L(V) <= N^{2+beta-Delta} is needed;; V is an NP predicate on T = N^{O(beta)} bits, so ANY fixed polynomial bo",
 "origin": "director",
 "prev": "d040626c20acfc697b31e6f053ce550ce77462992eb51f6af1b8063eb05d012a",
 "hash": "26cf8915df862b881c996716ba5257812d86ae495275f84abbf9195a039310cb"
}
```
