# Proofbook seq 478 — HYPOTHESIS

- key: `fd2bd56bbbb5fe70`
- at: 1795001653.223596
- mission: PNP-001/desk
- hash: `709b07939e6ef9984df5ce3a44ca6c35c1f1e4316e6a70d0f8374245e6e79278` (prev `55c0fd6a42ae116bf3ebfb75bae989003fc4bfd5d7eec54a0cd5fe74c17bb1c2`)
- graph nodes: PB:709b07939e6ef9984df5ce3a44ca6c35c1f1e4316e6a70d0f8374245e6e79278
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For formulas with null3=4 and cons3=1: sat = 1

## Full row (verbatim JSON)

```json
{
 "seq": 478,
 "at": 1795001653.223596,
 "problem": "p_vs_np",
 "mission": "PNP-001/desk",
 "key": "fd2bd56bbbb5fe70",
 "kind": "HYPOTHESIS",
 "evidence": {
  "exact_tests": 97,
  "by_family": {
   "read2": 52,
   "read3": 18,
   "symmetric": 15,
   "cubic_graph": 12
  },
  "sizes": [
   8,
   9,
   10
  ],
  "train_support": 612,
  "assignment": "A0019"
 },
 "exhaustion": null,
 "novelty": {
  "class": "NEW_CANDIDATE"
 },
 "pnp_link": "Exact structural laws of positive 1-in-3-SAT (decision, #SAT, parity): every law is either a tractable island (an algorithmic restriction a lower-bound proof must exclude) or an invariant a lower-bound argument can use (T41/T43 question Q-BD). Laws are candidates until proved.",
 "refined_from": "b7a6d53a924c4c70",
 "source_task": "20261118T120845-398f5638",
 "statement": "For formulas with null3=4 and cons3=1: sat = 1",
 "status": "EXACTLY_TESTED on finitely many unseen instances (open, not proved)",
 "prev": "55c0fd6a42ae116bf3ebfb75bae989003fc4bfd5d7eec54a0cd5fe74c17bb1c2",
 "hash": "709b07939e6ef9984df5ce3a44ca6c35c1f1e4316e6a70d0f8374245e6e79278"
}
```
