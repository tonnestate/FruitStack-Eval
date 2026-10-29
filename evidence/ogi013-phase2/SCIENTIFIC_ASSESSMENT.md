# OGI-013 — capability scorecard and assessment of supported / unsupported claims (2026-10-29)

Technical execution, mechanism evidence, observed performance and statistical proof are kept apart. "Observed" = in recorded evidence; "offline" = scripted providers (proves wiring, not model behaviour); "UNKNOWN" = not measured.

## Scorecard
| capability | status | evidence | what it does NOT show |
|---|---|---|---|
| Real-provider SINGLE vs COLLAB runs end to end under a hard budget | **demonstrated** (PILOT-4) | both arms graded by the official grader; 37 requests, 154,533 tokens, USD 0.00; guard, receipts and report reconcile | n = 1; two failed pilots preceded it (3 integration defects found by live contact, now fixed) |
| Independent critique by another lineage | **observed once** | gpt-oss critic blocked a policy-ineligible cancel with a correct citation | not shown to help the score; critic's alternative action was wrong |
| Revision changes the executed decision | **observed once** | cancel → transfer executed | the new action was also wrong (ERROR_REPLACED_BY_DIFFERENT_ERROR) |
| Re-review validates the correction | **observed, unreliable** | third lineage returned ISSUES: NONE with itemised grounds | grounds misread the transfer rule: stated grounds ≠ correctness |
| Better decisions / task completion than SINGLE | **not shown** | rewards 0.0 vs 0.0 | no benefit and no harm established |
| Economically justified | **unknown** | review cost 34,624 tokens / 4 requests for one decision | no per-success cost (no successes) |
| Failure recovery without losing progress | **partly observed** | rejected providers (billing, forbidden) were skipped; episode continued | no deliberate failure injection live; offline only |
| Structure selection / worker allocation for different tasks | **not tested live** | C3 RG2 demo d1/d2 organisational_success (2026-10-28), 52 decision rows on airline:2 (reward 1.0, one block) | single episodes; no comparison |
| Reuse of organisational knowledge / persistence | **not tested** | C3 H3, H5 | no Phase A/B data |
| Learning that transfers to unseen tasks | **not demonstrated** | ORG-GATE/1 not run: no attestation, 1/46 Phase A blocks (needs ≥300 rows, ≥40 tasks) | the only valid statement is "no learned policy exists" |
| Offline machinery (lineage exclusion, grounds rule, budgets, leases, launcher, evaluator inputs) | **verified offline** | 197-test offline suite incl. real-launcher end-to-end with scripted transport; CI replica 3.11–3.13 | model behaviour |

## Claims
**Supported:** (1) the integrated FruitStack path (MangoMe, OrangeMe, PeachMe, PlumMe, CherryMe, AppleMe, PomeloMe) runs official tau2 episodes on real free-tier providers within a zero-cash budget with complete accounting; (2) the COLLAB mechanism can, on real models, route a write decision to an independently selected lineage, record the objection and the revision, and enforce zero-cost routing;
(3) such review can prevent a policy-violating write, and can also substitute another error and certify it — both seen on the same decision; (4) the user-simulator/benchmark termination rule can end an episode before a confirmed write (SINGLE), so single-episode rewards of 0 are weak evidence of agent quality.
**Unsupported (do not state):** that COLLAB improves task success or decision quality; that review is cost-effective; that the organisation selects structures, allocates workers by capability, persists or reuses knowledge better than baselines; that it learns or improves on unseen tasks; any statistical superiority or effect size; "organisational intelligence".
**Defects found so far (all fixed, evidence kept):** simulator lease cash mismatch (pilot-1), byte-per-token input bound (pilot-2), failed-write grading crash, COLLAB post-grade attribution crash, double-counting of tokens/requests in the guard. **Open (owner decisions):** C3 HOLD, missing PREREG_LOCK, code-branch divergence of locked files (see `RESEARCH_STATUS.md`, `RESOURCE_PLAN.md`).

## Next smallest evidence-backed step
Owner decision on the consolidated request → run R3 (COLLAB-1, frozen) because it is the only design that can separate review value from review cost on many tasks without touching C3; C3 Phase A/B proceed from the locked code once the HOLD is lifted and the PREREG_LOCK question is ruled on.
