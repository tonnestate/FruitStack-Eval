# Proofbook seq 55 — PROOF_STEP

- key: `e9cbb05ff30aedd2`
- at: 1794840107.6964037
- mission: pi-theory-T1-T2
- hash: `25514cea5a296197d9925726174ca53be75d4f38533f73b7998ca36ce2b9af99` (prev `252794604fb9a5ce33c74d0c8eca9a5976da94b1404b8735231009191b0482d9`)
- graph nodes: PB:25514cea5a296197d9925726174ca53be75d4f38533f73b7998ca36ce2b9af99
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

#F mod p is computable in O(m n R*^3) operations, R* the largest cut rank over GF(p) of the clause prefixes F_j (T1 Satz 2)

## Full row (verbatim JSON)

```json
{
 "seq": 55,
 "at": 1794840107.6964037,
 "problem": "p_vs_np",
 "mission": "pi-theory-T1-T2",
 "key": "e9cbb05ff30aedd2",
 "kind": "PROOF_STEP",
 "assumptions": [],
 "checks": [
  "cm-79b294b8605b4c9e"
 ],
 "conclusion": "#F mod p is computable in O(m n R*^3) operations, R* the largest cut rank over GF(p) of the clause prefixes F_j (T1 Satz 2)",
 "document": "/root/fruits/research/PNP-001/theory/T1-ie-compression-and-barrier.md#Satz2",
 "justification": "induction over clause prefixes; minimal TT maintained mod p; CRT for the exact count",
 "premises": [
  "The minimal tensor-train (ROABP) width of f at cut i equals the rank of its cut matrix M_i(f) (T1 Satz 1)",
  "Two Gaussian-elimination sweeps over GF(p) turn a tensor train into one whose ranks equal the cut ranks over GF(p) of the function it represents (T1 minimisation lemma)",
  "The pointwise product of two tensor trains has cut ranks at most the products of their ranks (T1 Hadamard lemma)"
 ],
 "prev": "252794604fb9a5ce33c74d0c8eca9a5976da94b1404b8735231009191b0482d9",
 "hash": "25514cea5a296197d9925726174ca53be75d4f38533f73b7998ca36ce2b9af99"
}
```
