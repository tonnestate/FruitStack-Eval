# OGI-013-PILOT-1 — proposal (NOT executed; needs the owner's approval of the budget below)

Exploratory, separate from the preregistered study (no hypothesis test, no effect on PROTOCOL.md / locks / results). Question it can answer: on ONE fixed task, what does a single model cost and achieve, and what does the
economy-mode organisation add or cost, per recorded dispatch? It also supplies the counterfactual that the final-demo d2 trace lacks (does a single model pass task 6?). n = 1 per arm: descriptive only.

Task: airline 6 (read-only; expected action get_reservation_details; archived c2 comparison: FIXED 0.0 and ADAPTIVE 0.0; final-demo d2 under full RG/2: 1.0). Simulator: the same pinned model for both arms, gemini-3.1-flash-lite@vision
(seeded in the route file; a documented deviation from "PlumMe-chosen" for this pilot only). Supply: unchanged AUTO (no FREE_ONLY, no credit exclusion, full model pool).
Arms: SINGLE (mode single, one model per step) | RG2-ECONOMY (mode rg2, OGI013_ORG_ECONOMY=1, policy OFF, fresh state; escalation only for a stated purpose, bounded dispatch allowances).

## Explicit maximum consumption (evidence/ogi013-pilot/pilot_budget.json; enforced by pilot_guard.py watch, fail-closed)
| scope | max provider dispatches (incl. simulator calls) | max recorded tokens (in+out) |
|---|---|---|
| SINGLE arm | 45 | 160,000 |
| RG2-ECONOMY arm | 105 | 320,000 |
| **whole pilot** | **150** | **480,000** (cash 0.00 USD, wall 90 min) |
Basis (measured, d2 / task 6): agent steps 15 dispatches / 81,102 tokens; simulator 13 calls / 19,730 tokens; one economy escalation <= 6 + 2x4 dispatches (~3,000 tokens each). Expected: SINGLE ~28 dispatches / ~100k tokens;
ECONOMY ~45-60 dispatches / ~170-230k tokens. The caps are about 1.5x the expectation. Reference without the correction: airline:2 = 79 dispatches / 236k tokens; c2 means 42-56 dispatches / 117-174k tokens per episode.

## Recording and stopping
Every provider dispatch is a receipt row (plumme-state/receipts.jsonl); simulator calls are in sim-usage.jsonl; ORG_DECISION / ORG_SKIPPED events carry purpose, yield and dispatch totals. The guard polls every 10 s and, on any cap, writes PILOT_HALT and
SIGTERMs the run's process group. Missing/mismatched approval = refusal. No retry loop exists outside the engine's own call budget and the simulator's cooldown-aware wait.

## To approve (owner)
`sha256sum evidence/ogi013-pilot/pilot_budget.json > /root/pilot-approval.txt` then `PILOT_APPROVAL=/root/pilot-approval.txt evidence/ogi013-pilot/run_pilot.sh`. Nothing runs without that file, and a changed budget invalidates it.
