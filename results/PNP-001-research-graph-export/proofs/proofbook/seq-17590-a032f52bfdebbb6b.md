# Proofbook seq 17590 — PROOF_STEP

- key: `a032f52bfdebbb6b`
- at: 1795744592.6738899
- mission: director/closure-exclusions
- hash: `f0eb18b0b6e17c862d457b20e4ad609db828bb498b225f7b7d5233d7a25885ce` (prev `ddcee59d1501bb133135a16e84cd445c7dc434a6965020328c1a57a9194655c7`)
- graph nodes: PB:f0eb18b0b6e17c862d457b20e4ad609db828bb498b225f7b7d5233d7a25885ce
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

JOINT AW CONTROL MODEL FOR THE WHOLE ARCHITECTURE (owner 2026-11-27; PI check; CLAIMED, Claude family). A is PSPACE-complete and Ã its multilinear extension, which is PSPACE-computable, so NP^Ã = P^A = PSPACE (AW Thm 5.1, owner-sourced). For explicit poly-size graphs with poly-length Ã-constraints, each task is in FPSPACE with poly output, hence in FP^A: SAT, finding a colouring, exact counting (counter of n log2 3 + 1 bits), single coefficients of U_G^Ã, rational partition functions (poly bit length), semantic minimization (Sigma2, in PSPACE) and the affine hull (running Gaussian elimination). Correct. Consequence: any proof that uses only these operations as subroutines and stays valid in this world cannot separate NP from P. Owner pointer 'coefficient access != symbolic computation' is the VP versus #P-coefficient gap. It meets the obstacle already recorded in 17563: arithmetic lower bounds are oracle-free and hold in every world, and the known transfer runs only Boolean => algebraic (Buergisser, from memory), not algebraic => Boolean. No new route; no obligation closed.

## Full row (verbatim JSON)

```json
{
 "seq": 17590,
 "at": 1795744592.6738899,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "a032f52bfdebbb6b",
 "kind": "PROOF_STEP",
 "conclusion": "whole architecture runs in the AW world NP^Ã = P^A; operation-level use cannot separate P and NP",
 "premises": [
  17563,
  17589
 ],
 "statement": "JOINT AW CONTROL MODEL FOR THE WHOLE ARCHITECTURE (owner 2026-11-27; PI check; CLAIMED, Claude family). A is PSPACE-complete and Ã its multilinear extension, which is PSPACE-computable, so NP^Ã = P^A = PSPACE (AW Thm 5.1, owner-sourced). For explicit poly-size graphs with poly-length Ã-constraints, each task is in FPSPACE with poly output, hence in FP^A: SAT, finding a colouring, exact counting (counter of n log2 3 + 1 bits), single coefficients of U_G^Ã, rational partition functions (poly bit length), semantic minimization (Sigma2, in PSPACE) and the affine hull (running Gaussian elimination). Correct. Consequence: any proof that uses only these operations as subroutines and stays valid in this world cannot separate NP from P. Owner pointer 'coefficient access != symbolic computation' is the VP versus #P-coefficient gap. It meets the obstacle already recorded in 17563: arithmetic lower bounds are oracle-free and hold in every world, and the known transfer runs only Boolean => algebraic (Buergisser, from memory), not algebraic => Boolean. No new route; no obligation closed.",
 "prev": "ddcee59d1501bb133135a16e84cd445c7dc434a6965020328c1a57a9194655c7",
 "hash": "f0eb18b0b6e17c862d457b20e4ad609db828bb498b225f7b7d5233d7a25885ce"
}
```
