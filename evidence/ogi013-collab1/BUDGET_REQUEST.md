# OGI-013-COLLAB-1 — ONE authorisation request (COLLAB-1 only)

Supersedes, for approval purposes, the multi-study request in `evidence/ogi013-phase2/RESOURCE_PLAN.md` (never approved; C2 and C3 are NOT part of this request and the C3 HOLD stays in force).
Approving means: save `sha256sum evidence/ogi013-collab1/collab1_budget.json > <approval file>` and start `run_collab1.py --approval <approval file>`. Any edit of the budget file invalidates the approval. Nothing here is authorised yet.

## What is requested (the file `collab1_budget.json`; read by the launcher and the guard, nothing is stated twice)
| resource | limit |
|---|---|
| episodes | 144 = 48 tasks × {SINGLE, COLLAB, SINGLE-E} (`run_collab1.py --plan`: 120 write-opportunity + 24 no-write-control) |
| provider requests per episode | 110 (retries, continuations and credential rotation count; rejected attempts count) |
| tokens per episode / per complete agent step | 200,000 / 24,000 (PlumMe continuations included) |
| time per episode | 90 minutes (the episode is killed and scored TIMEOUT = non-success) |
| cash | **USD 0.00**; routes ANONYMOUS_FREE, FREE_TIER, LOCAL, TRIAL_CREDIT, INCLUDED only (TRIAL_CREDIT / INCLUDED are zero-cash entitlements and are reported as entitlement use); any other or unknown class without a recorded cost halts |
| **base ceilings** | 144 × 110 = **15,840 provider requests**; 144 × 200,000 = **28,800,000 tokens** |
| discard overhead (explicit, separate) | 10 % = 1,584 requests and 2,880,000 tokens for whole-block simulator discards (≤ 3 attempts per block); their usage is counted |
| **campaign totals enforced** | **17,424 provider requests, 31,680,000 tokens**, USD 0.00, 14 days elapsed time |
| supply | the full eligible PlumMe supply (budget-aware AUTO), no vendor restriction |

## Expected consumption (ESTIMATE, not a guarantee)
20–80 requests and 40,000–200,000 tokens per episode (C3 demos 33–77 requests / 43k–196k tokens; PILOT-4 15–22 requests / 62k–93k tokens): **2,880–11,520 requests, 5.8M–28.8M tokens, 24–74 h** of sequential run time. Elapsed time is quota-bound (free tiers), so the 14-day limit is a ceiling, not a forecast.

## How the limits are enforced (verified by the acceptance suite, `tests/test_ogi013_collab1_campaign.py`)
Before each provider request: the pre-dispatch gate (per-episode and campaign totals from the receipts of ALL episodes including archived ones; unknown usage/cash fails closed) and, for every step, PlumMe's ParentBudget (the step's tokens, requests and zero cash across continuations and retries). Afterwards: the guard watch kills a run that crosses a campaign limit.
An episode cap ends that episode (BUDGET_STOP, non-success); a campaign limit halts the campaign (exit 3) and it is not restarted by itself. A restart of the same command continues unfinished work only: completed episodes are never run again; an interrupted episode is archived (its usage still counts) and run afresh.

## What approval does NOT cover
Paid routes, any change of the limits, C2, C3 (any phase), RG2-LEARNED, a second COLLAB-1 execution, or a change of the frozen protocol after outcomes exist.

## Preconditions the launcher checks itself (refuses otherwise)
approval hash; manifest hash; every frozen file byte-identical to `AMENDMENT_LOCK.txt` / `STUDY_LOCK.txt`; clean checkout; no halt file; canonical components; lease-contract preflight. Before the first episode: `prepare_study_base.py` (isolated base and database copy) and `make_amendment_lock.sh` have been run and the result committed.
