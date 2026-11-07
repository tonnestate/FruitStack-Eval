# OGI study package: budget (DRAFT, an estimate and a cap proposal, NOT an authorization)

**Authorization statement.** This study must not start without explicit owner authorization. Nothing in this package authorizes a provider call, a pilot, a dataset download for study items or any spend. Authorization works per stage: the owner writes an approval file containing the sha256 of the locked `budget.md` and `runner_config.json` for exactly one stage (the COLLAB-1 pattern). Any edit invalidates it. The launcher must refuse to start without an approval file whose hashes match.

## 1. Per-call and per-task basis (archived numbers only)
| source | arm | tokens | calls | per call | per task |
|---|---|---|---|---|---|
| QA-2D v2 closure, 53 questions (`evidence/ogi013-qa2d-v2-closure`) | T | 902,513 | 129 | 6,996 | 17,029 tokens, 2.43 calls (per OK row: 22,563, 3.2) |
| same | E | 840,367 | 129 | 6,514 | 15,856, 2.43 (per OK row: 20,497, 3.1) |
| same | SN | 47,649 | 53 | 899 | 899, 1 (per OK row: 1,134) |
| micro pilot SWE-bench, 3 tasks (`evidence/ogi013-micro/PILOT.md`) | T / S / L | 666,710 / 139,255 / 283,310 raw | - | - | 222k / 46k / 94k per task |
| COLLAB-1 estimate, tau2 (`evidence/ogi013-collab1/BUDGET_REQUEST.md`) | episode | 40k-200k | 20-80 requests | - | C3 demos 33-77 req / 43k-196k; PILOT-4 15-22 req / 62k-93k |

QA-2D numbers are lower bounds, because failed rows record no tokens. The "per OK row" values divide by the rows that succeeded (T 40, E 41, SN 42).

## 2. Planning estimates per arm per task (M = 2 members)
| domain | T | E | S_luna (= L) | S_member_2 | episode cap per arm (T, E / S, L) | basis |
|---|---|---|---|---|---|---|
| D1 tau2 | 50 req, 120k | 50, 120k (matched) | 30, 70k | 30, 70k | 110 req, 200k / 110, 200k | COLLAB-1 midpoints; COLLAB-1 per-episode cap |
| D2 BigCodeBench | 6, 42k | 6, 42k | 1, 7k | 1, 7k | 20, 120k / 3, 24k | QA-2D T per-call tokens (about 7k) x calls; 6 T calls assumed because code disagrees more often than multiple choice (3.2 on QA-2D). No archived code-function run exists |
| D4 MATH-500 L5 | 3.2, 22.6k | 3.1, 20.5k | 1, 7k | 1, 1.1k | 12, 60k / 3, 24k | QA-2D per OK row; S at T's per-call tokens, SN at its own |
| D3 SWE-bench Verified | about 222k | about 222k | 94k (L) | 46k (S) | 1,500 req, 3M (PREREG circuit breaker) | micro pilot; **not in any stage below** (separate authorization) |

## 3. Totals per study and per stage (expected / cap)
| stage | study | n | expected requests | expected tokens | cap requests | cap tokens |
|---|---|---|---|---|---|---|
| A | EVAL-001 D2 | 200 tasks x 4 arms | 2,800 | 19.6M | 9,200 | 57.6M |
| A | EVAL-002 D2 transfer | 200 pairs x 2 T-shaped arms | 2,400 | 16.8M | 8,000 | 48.0M |
| A | EVAL-003 phase 1 | 148 x 2 members x 3 attempts | 888 | 6.2M | 2,664 | 21.3M |
| A | EVAL-003 phase 2 (worst case U = all 148) | 148 x (T + E; V is free) | 1,776 | 12.4M | 5,920 | 35.5M |
| **A total** | | | **7,864** | **55.0M** | **25,784** | **162.4M** |
| B | EVAL-001 D1 tau2 | about 164 tasks x 4 arms | **26,240** | **62.3M** | **72,160** | **131.2M** |
| C | EVAL-001 D4 math (secondary) | 150 x 4 arms | **1,245** | **7.7M** | **4,500** | **25.2M** |
| **all** | | | **35,349** | **125.0M** | **102,444** | **318.8M** |

Seeding for EVAL-002 reuses the EVAL-001 D2 T episodes at no extra cost. Caps are per-episode caps times episodes. A capped episode ends as BUDGET_STOP (scored as a failure), and the campaign continues until the stage cap.

Suggested order: A first. It is the cheapest stage and the only one with fully executable grading for all three questions. B and C run only after A's report and a separate approval.

## 4. Fixed caps (enforced by the launcher and PlumMe; any hit halts with exit 3)
- **Provider-call cap per stage** = the cap column above (A 25,784; B 72,160; C 4,500 requests). A request counts `provider_attempt_count`, at least 1; retries, continuations, credential rotation and rejected attempts all count (COLLAB-1 definition).
- **Token cap per stage** = the cap column above, recorded input plus output. A failure without recorded usage is charged a 4,000-token reserve.
- **Money cap: USD 0.00 cash.** Only route classes ANONYMOUS_FREE, FREE_TIER, LOCAL, TRIAL_CREDIT and INCLUDED are allowed; TRIAL_CREDIT and INCLUDED use is reported as entitlement. Any other or unknown route class without a recorded cost halts. A cash budget above zero is a different study and needs its own approval stating the amount.
- Wall time: 14 days per stage. Per-task episode time: 90 minutes (TIMEOUT counts as non-success).

## 5. Current PlumMe route economics (read-only, offline, no inference)
`route_classes.py` was run against PlumMe main `0ac462a` (package 0.1.12) and its bundled donor free-allowance registry (OmniRoute v3.8.50, commit `5458026c`). Output in `route_classes.json`:

| class | model routes | providers |
|---|---|---|
| FREE (keyless / recurring allowance, terms ok or caution) | 230 | 38 |
| TRIAL (one-time-initial or recurring-credit: zero cash but runs out) | 113 | 26 |
| EXCLUDED (discontinued, or terms avoid / ambiguous / unknown) | 113 | 17 |
| paid (LOW / NORMAL / PREMIUM) | not countable offline: needs live provider discovery, which was not run | - |

The registry describes what a provider's free allowance covers, not which accounts this host holds or which routes are healthy. It is an upper bound on candidate zero-cash supply, not a capacity estimate. The QA-2D closure showed that the binding constraint is supply reliability, not route count: 15 of 36 infrastructure failures were HTTP 429 with no capacity. Stage B (about 26k requests, mostly tau2 multi-turn) is the most exposed. Before lock, a PlumMe supply snapshot (offline classification plus live health, with no inference) must show at least two independent lineages that can serve the roster, and its hash goes into the lock.

## 6. What this budget does not cover
D3 (SWE-bench), D5 (research claims), any sham-brief arm, reruns after a CLOSED_INFRASTRUCTURE_INFEASIBLE closure, paid routes, and any change to caps after outcomes exist.
