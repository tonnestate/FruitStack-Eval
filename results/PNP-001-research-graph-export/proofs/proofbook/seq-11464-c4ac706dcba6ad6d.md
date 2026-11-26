# Proofbook seq 11464 — CONNECTION

- key: `c4ac706dcba6ad6d`
- at: 1795389125.1404686
- mission: agent/pnp-desk/research/R1835:claude-haiku-5-5@default
- hash: `9a2429c9209a2e2d0f4ac90f4b68a6fe2015fc0e17dc3b19e534deae9bb1da23` (prev `4fc45d6c3d63f0ba446339c6eafd7ea0c583f3d0b9e0a7bd2afd0cd9a0bbd2e8`)
- graph nodes: PB:9a2429c9209a2e2d0f4ac90f4b68a6fe2015fc0e17dc3b19e534deae9bb1da23
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

L-AFF restates S0023 with the update recurrence unrolled. For affine one-pass machines (q_{t+1}=M_t q_t + x_t v_t + c_t, any update time) with a total decoder for Search-MCSP[s] on Yes_s, ker A = {0}, so S >= 2^m. For admissible s = m^O(1) this gives space > s^c for every c, independent of update time. The decoder may be any function, so oracle gates in D are allowed, but oracle gates in the update are not. The bound is tight (storing x is affine). It does not touch G0001 (update time) and is not progress toward (8) or (40a).

## Full row (verbatim JSON)

```json
{
 "seq": 11464,
 "at": 1795389125.1404686,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R1835:claude-haiku-5-5@default",
 "key": "c4ac706dcba6ad6d",
 "kind": "CONNECTION",
 "chosen_because": "New lemma cannot be recorded as a proof step through proof_state_update (only existing step ids are accepted). CONNECTION records it as a restricted-class fact without claiming it closes G0001.",
 "origin": "agent",
 "question": "Q-85e487150a",
 "statement": "L-AFF restates S0023 with the update recurrence unrolled. For affine one-pass machines (q_{t+1}=M_t q_t + x_t v_t + c_t, any update time) with a total decoder for Search-MCSP[s] on Yes_s, ker A = {0}, so S >= 2^m. For admissible s = m^O(1) this gives space > s^c for every c, independent of update time. The decoder may be any function, so oracle gates in D are allowed, but oracle gates in the update are not. The bound is tight (storing x is affine). It does not touch G0001 (update time) and is not progress toward (8) or (40a).",
 "prev": "4fc45d6c3d63f0ba446339c6eafd7ea0c583f3d0b9e0a7bd2afd0cd9a0bbd2e8",
 "hash": "9a2429c9209a2e2d0f4ac90f4b68a6fe2015fc0e17dc3b19e534deae9bb1da23"
}
```
