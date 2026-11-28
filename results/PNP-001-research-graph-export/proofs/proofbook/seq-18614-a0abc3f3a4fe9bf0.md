# Proofbook seq 18614 — CONNECTION

- key: `a0abc3f3a4fe9bf0`
- at: 1795864401.3858135
- mission: director/mechanism-extraction
- hash: `a20b0853764e659e94bd7dcaa33d58de5103c1c840be5e296f0e08fc6782afc0` (prev `7a1c9c136c5ea88d40f7123a53701be36b7f1357539b2810496d9746a6a339d7`)
- graph nodes: PB:a20b0853764e659e94bd7dcaa33d58de5103c1c840be5e296f0e08fc6782afc0
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18614,
 "at": 1795864401.3858135,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "a0abc3f3a4fe9bf0",
 "kind": "CONNECTION",
 "about": [
  "mech:x17138-circularity-c-rprime-owner-2026-11-26-the-obligation-"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x17138-circularity-c-rprime-owner-2026-11-26-the-obligation-",
  "name": "x17138 CIRCULARITY C-RPRIME (owner 2026-11-26): the obligation 'every small G",
  "preconditions": "no explicit assumption found in the source statement",
  "effect": "CIRCULARITY C-RPRIME (owner 2026-11-26): the obligation 'every small Gap-MCSP[N^beta] circuit has W(C) <= N^{beta-2eta}' (W as in D6', seq 16840) is equivalent to 'no small Gap-MCSP[N^beta] circuit exists': if C of size S exists, C' = (C AND P_N) OR (C AND NOT P_N) with P_N a linear-size De Morgan p; The correct non-circular obligation is NORM: existence of a small circuit implies existence of a circuit of size <= N^{1+eps} with W <= N^{beta-2eta} for the same promise problem (then D6' + AF give the contradiction).",
  "limitations": "CIRCULARITY C-RPRIME (owner 2026-11-26): the obligation 'every small Gap-MCSP[N^beta] circuit has W(C) <= N^{beta-2eta}' (W as in D6', seq 16840) is equivalent to 'no small Gap-MCSP[N^beta] circuit exists': if C of size S exists, C' = (C AND P_N) OR (C AND NOT P_N) with P_N a linear-size De Morgan p",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 17138 (extraction preserves, never upgrades the status)",
  "representations": "parity, circuit, gate",
  "interfaces": "parity, circuit, gate, bound:N^beta, bound:W(C) <= N^{beta-2eta}, bound:O(N)",
  "provenance": "PROOF_STEP seq 17138 key eccc698cd1081a77 mission director/closure-exclusions",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "parity",
   "circuit",
   "gate"
  ],
  "guarantees": [
   "CIRCULARITY C-RPRIME (owner 2026-11-26): the obligation 'every small Gap-MCSP[N^beta] circuit has W(C) <= N^{beta-2eta}' (W as in D6', seq 16840) is equivalent to 'no small Gap-MCSP[N^beta] circuit exists': if C of size S exists, C' = (C AND P_N) OR (C AND NOT P_N) with P_N a linear-size De Morgan p",
   "The correct non-circular obligation is NORM: existence of a small circuit implies existence of a circuit of size <= N^{1+eps} with W <= N^{beta-2eta} for the same promise problem (then D6' + AF give the contradiction)."
  ],
  "bounds": [
   "N^beta",
   "W(C) <= N^{beta-2eta}",
   "O(N)",
   "support >= 1/p",
   "Omega(N)",
   "N^{beta-2eta}",
   "size <= N^{1+eps}",
   "W <= N^{beta-2eta}"
  ]
 },
 "connection": "MECHANISM mech:x17138-circularity-c-rprime-owner-2026-11-26-the-obligation-: CIRCULARITY C-RPRIME (owner 2026-11-26): the obligation 'every small Gap-MCSP[N^beta] circuit has W(C) <= N^{beta-2eta}' (W as in D6', seq 16840) is equivalent to 'no small Gap-MCSP[N^beta] circuit exists': if C of size S exists, C' = (C AND P_N) OR (C AND NOT P_N) with P_N a linear-size De Morgan p",
 "origin": "director",
 "prev": "7a1c9c136c5ea88d40f7123a53701be36b7f1357539b2810496d9746a6a339d7",
 "hash": "a20b0853764e659e94bd7dcaa33d58de5103c1c840be5e296f0e08fc6782afc0"
}
```
