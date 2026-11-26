# Proofbook seq 16800 — PROOF_STEP

- key: `aa96fee8bead58f8`
- at: 1795710981.2453547
- mission: director/closure-quant
- hash: `16ff2ba44618ed527c6680dd68b13b57025f790de90f704c0af30953d99d2a70` (prev `c921c8329d7026bf184e02954cf319880884aa1a57857977cfccb65cb4e7eb33`)
- graph nodes: PB:16ff2ba44618ed527c6680dd68b13b57025f790de90f704c0af30953d99d2a70
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

CJ1 CJSW Thm 1.4 PROOF AT THE SOURCE (arXiv-2203.14379 paper.txt l.906-930): under P = NP the algorithm is search-MCSP streaming (Lemma 3.2) on the WHOLE input followed by Succinct-DISJ (coNP) on the found circuit - deterministic. Refuter outputs have circuit complexity <= c(log n)^c (Lemma 2.5). Hence a polylogtime-uniform-AC0-constructive separation of DISJ from DETERMINISTIC streaming algorithms with these resources already implies P != NP.

## Full row (verbatim JSON)

```json
{
 "seq": 16800,
 "at": 1795710981.2453547,
 "problem": "p_vs_np",
 "mission": "director/closure-quant",
 "key": "aa96fee8bead58f8",
 "kind": "PROOF_STEP",
 "conclusion": "CJ1 CJSW Thm 1.4 PROOF AT THE SOURCE (arXiv-2203.14379 paper.txt l.906-930): under P = NP the algorithm is search-MCSP streaming (Lemma 3.2) on the WHOLE input followed by Succinct-DISJ (coNP) on the found circuit - deterministic. Refuter outputs have circuit complexity <= c(log n)^c (Lemma 2.5). Hence a polylogtime-uniform-AC0-constructive separation of DISJ from DETERMINISTIC streaming algorithms with these resources already implies P != NP.",
 "premises": [
  "CJSW Thm 1.4",
  "CJSW Lemma 2.5",
  "CJSW Lemma 3.2"
 ],
 "prev": "c921c8329d7026bf184e02954cf319880884aa1a57857977cfccb65cb4e7eb33",
 "hash": "16ff2ba44618ed527c6680dd68b13b57025f790de90f704c0af30953d99d2a70"
}
```
