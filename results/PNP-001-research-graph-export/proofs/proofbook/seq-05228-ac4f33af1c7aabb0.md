# Proofbook seq 5228 — CONNECTION

- key: `ac4f33af1c7aabb0`
- at: 1795195480.8199677
- mission: director/synthesis
- hash: `a310ae2854389fd00936e01ad3f87a0b6d744753f9a5171323bb782709449c82` (prev `a92411822dc4718148d24530fb9b9a1ebe17352cb3885715a7b6f859bb80504f`)
- graph nodes: PB:a310ae2854389fd00936e01ad3f87a0b6d744753f9a5171323bb782709449c82
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

P != NP TRACK FILTERS (2026-11-20, spec section "P != NP track - mandatory filters"): F1 sparsity cap - a language with <= S yes-instances per length has cut matrices with <= S ones, rank <= S and read-once width <= S+1 in every order; for MCSP[s] log S = O~(s), so no cut/rank/restriction measure can prove the MMW19 streaming target. F2 locality - with a PH oracle the streaming algorithm exists (MMW19 Thm 1.2); arguments surviving oracle gates on poly(s) bits are dead. Target in our model: no read-once program with poly(s) state bits and poly(s)-time transition function for MCSP^A[s]; needs a measure on transition functions; OPEN, no candidate.

## Full row (verbatim JSON)

```json
{
 "seq": 5228,
 "at": 1795195480.8199677,
 "problem": "p_vs_np",
 "mission": "director/synthesis",
 "key": "ac4f33af1c7aabb0",
 "kind": "CONNECTION",
 "origin": "director",
 "statement": "P != NP TRACK FILTERS (2026-11-20, spec section \"P != NP track - mandatory filters\"): F1 sparsity cap - a language with <= S yes-instances per length has cut matrices with <= S ones, rank <= S and read-once width <= S+1 in every order; for MCSP[s] log S = O~(s), so no cut/rank/restriction measure can prove the MMW19 streaming target. F2 locality - with a PH oracle the streaming algorithm exists (MMW19 Thm 1.2); arguments surviving oracle gates on poly(s) bits are dead. Target in our model: no read-once program with poly(s) state bits and poly(s)-time transition function for MCSP^A[s]; needs a measure on transition functions; OPEN, no candidate.",
 "prev": "a92411822dc4718148d24530fb9b9a1ebe17352cb3885715a7b6f859bb80504f",
 "hash": "a310ae2854389fd00936e01ad3f87a0b6d744753f9a5171323bb782709449c82"
}
```
