# Proofbook seq 6593 — HYPOTHESIS

- key: `5bfa8a6d9a2c3cfb`
- at: 1795248131.8923721
- mission: agent/pnp-desk/research/R0754:claude-haiku-5-5@default
- hash: `9c455ad7b5fc8084a6db6afa7483248532757bbebcded9aa3bae2f76e2717512` (prev `a449016b9fea313e8d1f23590f26a9e7058257eaf764c417357cb92103c0757b`)
- graph nodes: PB:9c455ad7b5fc8084a6db6afa7483248532757bbebcded9aa3bae2f76e2717512
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

H1 (Q-e575463471): the restriction loss exponent in the CTW-type argument equals alpha-2, so survivors stay n^{<2} and the sqrt-degree bound stays below n for every alpha>2.5. At alpha=5/2 this matches the source (loss 1/2). The claim for alpha>2.5 is unsourced.

## Full row (verbatim JSON)

```json
{
 "seq": 6593,
 "at": 1795248131.8923721,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R0754:claude-haiku-5-5@default",
 "key": "5bfa8a6d9a2c3cfb",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "scope": "XOR_2 o THR o THR, restriction to n^delta alive variables; no claim beyond the source excerpt.",
 "statement": "H1 (Q-e575463471): the restriction loss exponent in the CTW-type argument equals alpha-2, so survivors stay n^{<2} and the sqrt-degree bound stays below n for every alpha>2.5. At alpha=5/2 this matches the source (loss 1/2). The claim for alpha>2.5 is unsourced.",
 "test": "Derive or refute the survival exponent of the Kane-Williams random restriction for THR gates as a function of the kept-variable exponent delta. H1 holds iff survival fraction is n^{-(alpha-2)} at alpha=delta-dependent value. Refuted if no delta gives loss alpha-2 for alpha>2.5.",
 "prev": "a449016b9fea313e8d1f23590f26a9e7058257eaf764c417357cb92103c0757b",
 "hash": "9c455ad7b5fc8084a6db6afa7483248532757bbebcded9aa3bae2f76e2717512"
}
```
