# OGI-013-VALIDATION-1 — small prospective cohort (written before any episode)

Question: can the FruitStack organisation (PlumMe AUTO + CherryMe challenge/revision/specialist + continuity) produce better independently graded solutions than ONE fixed capable model on the same
tasks, and is any advantage more than extra inference (equal-resource control)? Separate from C1/C2/C3/COLLAB-1, which are untouched.

Conditions (same task, same initial state, same simulator model within the block, same official tau2 evaluator, per-episode ceilings identical to COLLAB-1: 110 requests, 200,000 tokens, 24,000 per step, 90 min, USD 0):
- **FIXED** - ChatGPT headless, ONE pinned model, no organisation, no second model, no re-selection (`runners/ogi013_codex_heart.py`). Owner preference Terra 6.0 is not executable with this login
  (verified: "The gpt-6-terra model is not supported when using Codex with a ChatGPT account"); the permitted alternative **Luna 6.0 = `gpt-6-luna`** is verified. Isolated CODEX_HOME (auth only; no hooks/AGENTS/MCP), read-only
  sandbox, ephemeral session. Codex adds a constant ~13k-token scaffold per call; accounted net of the measured constant, raw values kept in each receipt.
- **SINGLE-E** - equal-resource, non-organised control (k=3 independent drafts on write decisions, majority vote, PlumMe AUTO supply).
- **COLLAB** - the integrated FruitStack organisation, PlumMe AUTO, with the AMENDMENT-1 L-S rules.
Order: cyclic Latin square over the three tasks. Cohort: `select_tasks.py` (outcome-independent score over the 19 registered mechanism-sensitive tasks) -> retail:109, retail:110, retail:72.
Not claimed: any statistical superiority from n=3 tasks; BUDGET_STOP / SUPPLY / simulator failures are infrastructure outcomes, reported separately and never read as evidence about intelligence.
Evidence per episode: official tau2 result, receipts (model identity per inference), fruitstack-events (organisational decisions), step accounting, sim-usage.
