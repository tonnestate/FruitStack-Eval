# Proofbook seq 14441 — HYPOTHESIS

- key: `ac1f9decb3cfc299`
- at: 1795559151.1505194
- mission: agent/pnp-desk/research/R3009:gpt-6-luna@default
- hash: `d2ab7dc368fae4909bbb63826f9f32dabb59ff5d3ec7e89e41b26bd691b8abda` (prev `ea003ad072514a9219929328c207e324394bc62c60a8122cf69a9cff8dd15941`)
- graph nodes: PB:d2ab7dc368fae4909bbb63826f9f32dabb59ff5d3ec7e89e41b26bd691b8abda
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For some circuit families with large prefix width, allowing transition-map don’t-cares on unreachable states can reduce minimum per-step gate cost relative to synthesizing the entire Boolean map.

## Full row (verbatim JSON)

```json
{
 "seq": 14441,
 "at": 1795559151.1505194,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R3009:gpt-6-luna@default",
 "key": "ac1f9decb3cfc299",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "question": "Q-08a1c5b68f",
 "scope": "Layered transitions with arbitrary recoding and time-dependent updates, basis AND/XOR/NOT with constants.",
 "statement": "For some circuit families with large prefix width, allowing transition-map don’t-cares on unreachable states can reduce minimum per-step gate cost relative to synthesizing the entire Boolean map.",
 "test": "Compare exact synthesis minima under all-input constraints and reachable-pair-only constraints for the same finite language. A general proof or unbounded separation would support the claim.",
 "prev": "ea003ad072514a9219929328c207e324394bc62c60a8122cf69a9cff8dd15941",
 "hash": "d2ab7dc368fae4909bbb63826f9f32dabb59ff5d3ec7e89e41b26bd691b8abda"
}
```
