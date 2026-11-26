# Proofbook seq 947 — REFUTATION

- key: `ed8856eadd7e2def`
- at: 1795025108.9107327
- mission: PNP-001/director
- hash: `351044825bd9d6677aad3b2067395c1022b771347bb04859e90476a306d79945` (prev `f3e31b7d251ba7f8656e27fb63672999a14ccbf586d020ad92e533289964109e`)
- graph nodes: PB:351044825bd9d6677aad3b2067395c1022b771347bb04859e90476a306d79945
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

Non-port (P4 minor) does not indicate hardness: 2-SAT (in P) has a P4 minor at n=3, hence is not a matroid port for all n>=3; so no implication non-port => super-linear circuit size exists. D-013 remains a theorem about ideal secret sharing / ideal mSP only.

## Full row (verbatim JSON)

```json
{
 "seq": 947,
 "at": 1795025108.9107327,
 "problem": "p_vs_np",
 "mission": "PNP-001/director",
 "key": "ed8856eadd7e2def",
 "kind": "REFUTATION",
 "evidence": "lab/transfer/p4_control.py exhaustive minor search: witness present (x0|~x1),(x0|x1),(~x1|x2); free a=(~x0|~x1), b=(~x0|x1), c=(~x0|~x2), d=(~x0|x2): UNSAT = ab|bc|cd; calibrations 1in3 n=5 and XOR n=4 without P4; hand-checked by PlumMe referee W-83465c2ba7394d3e",
 "register": "D-020",
 "statement": "Non-port (P4 minor) does not indicate hardness: 2-SAT (in P) has a P4 minor at n=3, hence is not a matroid port for all n>=3; so no implication non-port => super-linear circuit size exists. D-013 remains a theorem about ideal secret sharing / ideal mSP only.",
 "target": "matroid-port route (D-011..D-013 as hardness evidence)",
 "prev": "f3e31b7d251ba7f8656e27fb63672999a14ccbf586d020ad92e533289964109e",
 "hash": "351044825bd9d6677aad3b2067395c1022b771347bb04859e90476a306d79945"
}
```
