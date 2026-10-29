# C3 — historical limitations and what any future valid continuation requires (report only; nothing here changes C3)

C3 stays on HOLD (owner order 2026-10-28T10:17Z). COLLAB-1 does not depend on C2 or on any item below. The C3 branch (`ogi013-org-bridge`, d887dfb, lock hashes verified) and all C3 evidence are untouched by this work.

## Historical integrity limitations (reported, not corrected)
1. `PREREG_LOCK.txt` was never written, although `supervisor.sh` requires it before any C3 run; Phase A block `airline:2` nevertheless ran (reward 1.0, 52 decision rows, 2026-10-28). The block is data collected without the sealing step.
2. `FREEZE.txt` does not exist; Phase B has not started; no ORG-GATE attestation exists; Phase A has 1 of 46 blocks (airline:6 failed, cause not recorded); 6 `airline:2-interrupted*` discards.
3. C2 is incomplete (8 pairs, 16 arms without an official result) and unevaluated.
4. C1 integrity lists TRIAL_CREDIT receipts in kept arms while RESULT.md says "free routes only" (erratum candidate).
5. The locked implementation and the research branch diverged: `ogi013-collab-proof` is 12+ commits ahead and edits three locked files (`ogi013_tau2_agent.py`, `ogi013_sim_supply.py`, `rg2_trace_report.py`) — pilot-only behaviour, but not the registered bytes.

## Required for any future valid C3 continuation (owner decisions; none taken here)
1. Lift the HOLD with an explicit order and a C3-only resource authorisation (requests, tokens, cash, time) — none exists.
2. Rule on `airline:2` and the missing PREREG_LOCK (valid with a dated disclosure / excluded / re-run); an agent must not create the lock retroactively.
3. Run C3 from the locked code (`ogi013-org-bridge`). Porting the pilot-grade controls (ParentBudget per step, request counting, lease-contract preflight, the SINGLE-E scope switch) to that branch changes locked files and needs a dated amendment BEFORE further C3 data.
4. Provide `runs/host_budget.env` (per-episode session ceilings, cash 0.0) and a campaign guard for C3 (the COLLAB-1 launcher/guard pattern can be reused as a NEW file).
5. Decide whether C2 must finish first (RUNBOOK) — COLLAB-1 does not wait for it.
6. SINGLE-E in C3 keeps its registered every-turn definition; its k source (median dispatches of organisation decisions) is a unit mismatch to be ruled on in that amendment, not here.
