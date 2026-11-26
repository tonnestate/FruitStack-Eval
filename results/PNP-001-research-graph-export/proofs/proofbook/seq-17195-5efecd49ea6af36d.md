# Proofbook seq 17195 — PROOF_STEP

- key: `5efecd49ea6af36d`
- at: 1795728915.259027
- mission: director/closure-exclusions
- hash: `59aab84c810091b5d6dd8130823ae683de2be3cac006c00356576d08aaecc7c5` (prev `be3ba474a9611c40631111fd88f42d33037af8fcbbaab420f9e9334906f6f35d`)
- graph nodes: PB:59aab84c810091b5d6dd8130823ae683de2be3cac006c00356576d08aaecc7c5
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

CJ3-R (REPAIR of seq 16802 / Q-88090df9cf:S0139; owner construction 2026-11-26, director check; CLAIMED). Input x then y (n bits each), n known. m=ceil(log2(2n+2)), h=floor(log2 m), budget B=m^{max(1,floor(sqrt h))}. A* runs all programs of description length <= h (K <= 2m) as bit generators P(n,i), each cut off after B simulated steps; per program an active bit and a bit d_P. Every stream bit is compared with P(n,i) (mismatch or timeout deactivates); in the second half A* recomputes P(n,i) for x_i from the program instead of re-reading it and sets d_P |= P(n,i) AND y_i. Output: NOT d_P for an active program, else a fixed default b0. ONE PASS, no random access (objection 3 fixed); m(n) and the time bound are explicit (objections 1, 2 fixed). Correctness: a program still active at the end reproduced every input bit, so d_P = [x and y intersect]. T = n m^{O(sqrt log m)}, S = m^{O(sqrt log m)}, inside the CJSW class for f(n)=ceil(log2 log2(n+2)) (any f=omega(sqrt log log n)). Every fixed deterministic generator with (log n)^c time per bit is enumerated and within budget for all large n, so A* answers correctly on its outputs. COLLISIONS: if u != v are prefixes produced by such generators, the generator of u is active after u and inactive after v, so A*'s states differ (for all large n): deterministic polylog-time collision generators are EXCLUDED against A* (unconditional). Under P=NP the PH collapses on input length m=log n, so every polylogtime-uniform AC0 generator (single bit in PH on m) is computed in time m^{O(1)}=(log n)^{O(1)} and is also captured.

## Full row (verbatim JSON)

```json
{
 "seq": 17195,
 "at": 1795728915.259027,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "5efecd49ea6af36d",
 "kind": "PROOF_STEP",
 "conclusion": "CJ3-R (REPAIR of seq 16802 / Q-88090df9cf:S0139; owner construction 2026-11-26, director check; CLAIMED). Input x then y (n bits each), n known. m=ceil(log2(2n+2)), h=floor(log2 m), budget B=m^{max(1,floor(sqrt h))}. A* runs all programs of description length <= h (K <= 2m) as bit generators P(n,i), each cut off after B simulated steps; per program an active bit and a bit d_P. Every stream bit is compared with P(n,i) (mismatch or timeout deactivates); in the second half A* recomputes P(n,i) for x_i from the program instead of re-reading it and sets d_P |= P(n,i) AND y_i. Output: NOT d_P for an active program, else a fixed default b0. ONE PASS, no random access (objection 3 fixed); m(n) and the time bound are explicit (objections 1, 2 fixed). Correctness: a program still active at the end reproduced every input bit, so d_P = [x and y intersect]. T = n m^{O(sqrt log m)}, S = m^{O(sqrt log m)}, inside the CJSW class for f(n)=ceil(log2 log2(n+2)) (any f=omega(sqrt log log n)). Every fixed deterministic generator with (log n)^c time per bit is enumerated and within budget for all large n, so A* answers correctly on its outputs. COLLISIONS: if u != v are prefixes produced by such generators, the generator of u is active after u and inactive after v, so A*'s states differ (for all large n): deterministic polylog-time collision generators are EXCLUDED against A* (unconditional). Under P=NP the PH collapses on input length m=log n, so every polylogtime-uniform AC0 generator (single bit in PH on m) is computed in time m^{O(1)}=(log n)^{O(1)} and is also captured.",
 "premises": [
  "seq 16802 (CJ3)",
  "CJSW Thm 1.4 (theoretics.episciences.org)"
 ],
 "prev": "be3ba474a9611c40631111fd88f42d33037af8fcbbaab420f9e9334906f6f35d",
 "hash": "59aab84c810091b5d6dd8130823ae683de2be3cac006c00356576d08aaecc7c5"
}
```
