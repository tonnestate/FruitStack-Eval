# OGI-013-PILOT-1 — proposal (NOT executed; needs the owner's explicit approval of the budget below)

Exploratory, separate from the preregistered study (no hypothesis test, no effect on PROTOCOL.md / locks / results). Question: on ONE fixed task with a write action, what does a single model
cost and achieve, and what does the committed collaboration step (`OGI013_ORG_COLLAB=1`: economy gate -> Brother-Mode challenge / revise / re-review / specialist) add or cost, per recorded dispatch?
n = 1 per arm: descriptive only, no effect size, no OGI claim.

Corrections to the earlier draft of this pilot (it could not have tested the collaboration):
- it ran the shared `ogi013-org` checkout, which has no collaboration module -> `run_arm.sh` runs THIS checkout (`PILOT_CODE`), refused unless clean and containing the module and the gate;
- the second arm never set `OGI013_ORG_COLLAB=1` -> it does now (mode rg2, policy OFF); the run records whether any `ORG_COLLAB` review happened and says "arm tested nothing" otherwise;
- airline task 6 is read-only, so the economy gate would only log `ORG_SKIPPED` -> task 24 (expected action `book_reservation`, a write);
- per-arm caps never matched (budget keys `SINGLE`/`RG2-ECONOMY` vs arm directories) -> keyed by the real arm directories; an arm without a cap halts;
- a dispatch with missing usage counted as 0 tokens -> a successful dispatch without usage HALTS; a failed one is charged `reserve_tokens_per_dispatch`;
- enforcement was a 10 s poll after the fact -> `runners/ogi013_pilot_gate.py` refuses every agent step and simulator attempt BEFORE the provider dispatch if the dispatch (+ reserve) would cross a cap
  (`pilot_guard.py watch` remains as a backstop). Frozen conditions never set `OGI013_PILOT_BUDGET`, so they are unaffected.

Arms: SINGLE (mode single) | COLLAB (mode rg2, `OGI013_ORG_COLLAB=1`, policy OFF), same code checkout, same pinned simulator model (seeded; documented deviation), unchanged AUTO supply, fresh state each.

## Explicit maximum consumption (`pilot_budget.json`)
| scope | max provider dispatches (incl. simulator) | max recorded tokens (in+out) |
|---|---|---|
| SINGLE arm | 40 | 50,000 |
| COLLAB arm | 80 | 120,000 |
| **whole pilot** | **120** | **170,000** (cash 0.00 USD, wall 90 min, reserve 4,000 tokens per dispatch) |

Basis (archived c2 runs, task 24): fixed 40 dispatches / 27,616 tokens; adaptive 80 / 73,106. Expected SINGLE ~20-30 dispatches / ~20-30k tokens; COLLAB adds at most 5 calls per reviewed write.
The reserve means a dispatch is refused when used + 4,000 would cross a cap, so the usable token headroom is the cap minus the reserve.

## To approve (owner)
`sha256sum evidence/ogi013-pilot/pilot_budget.json > /root/pilot-approval.txt` then `PILOT_APPROVAL=/root/pilot-approval.txt evidence/ogi013-pilot/run_pilot.sh`. Nothing runs without that file;
any edit of the budget invalidates the approval. This proposal authorises no expenditure by itself.
