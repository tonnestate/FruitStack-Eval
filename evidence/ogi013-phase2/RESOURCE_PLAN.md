# OGI-013 — consolidated resource plan and single approval request for the outstanding campaign

**All numbers are ESTIMATES from measured episodes (C3 demos d1/d2: 33–77 requests, 43k–196k tokens, 26–31 min per episode; PILOT-4: 15–22 requests, 62k–93k tokens, 2–11 min) — not confirmed capacity. Nothing below is authorised; the PILOT-4 authorisation is exhausted and is not reused.**

## Components (episodes = one task × one condition)
| component | episodes | provider requests est. (cap) | tokens est. (cap) | wall est. sequential (cap) |
|---|---:|---|---|---|
| R0 finish C2 (8 incomplete pairs, 16 arms), then evaluate offline | 16 | 320 – 1,280 (1,760) | 0.6M – 3.2M (3.2M) | 3 – 8 h (24 h) |
| R1 C3 Phase A remaining (airline:6 + 44 others; RG2-RANDOMIZED) | 45 | 900 – 3,600 (4,950) | 1.8M – 9.0M (9.0M) | 8 – 23 h (68 h) |
| R2 C3 Phase B (14 held-out retail tasks × 8 conditions; 126 episodes if RG2-LEARNED is permitted and authorised) | 112 (126) | 2,240 – 8,960 (12,320) | 4.5M – 22.4M (22.4M) | 19 – 58 h (168 h) |
| R3 COLLAB-1 (48 tasks × SINGLE, COLLAB, SINGLE-E) | 144 | 2,880 – 11,520 (15,840) | 5.8M – 28.8M (28.8M) | 24 – 74 h (216 h) |
| **Total** | **317 (331)** | **6,340 – 25,360 (34,870)** | **12.7M – 63.4M (63.4M)** | **53 – 164 h (476 h)** |
Estimate bounds per episode: 20–80 requests, 40k–200k tokens, 10–31 min; caps per episode: 110 requests, 200,000 tokens, 24,000 tokens per agent step (whole step, continuations included), 90 min. Failed whole-block simulator discards (≤3 attempts) consume little and are covered by the margin below.
Calendar time is quota-bound, not compute-bound (free tiers: e.g. Groq gpt-oss 200k tokens/day, OpenRouter 50 free requests/day, Google resets 00:00 Pacific): realistic duration is multi-day to multi-week and **UNKNOWN**; the capacity assessment of 2026-10-28 itself says sustainability is not confirmed.
Cash exposure: **USD 0.00** (routes with unknown prices are refused; TRIAL_CREDIT / INCLUDED entitlements may be consumed and are reported as entitlement use, with tokens, not as cash).

## Consolidated approval request (ONE decision; a proposal until the owner approves it by hash)
Authorise, for R0–R3 together: provider requests ≤ 40,000; tokens ≤ 70,000,000; cash USD 0.00 with no paid route; ≤ 110 requests, ≤ 200,000 tokens, ≤ 24,000 tokens per agent step and ≤ 90 minutes per episode; the full eligible PlumMe supply (AUTO) with no vendor restriction; entitlement consumption within those totals; execution in the registered order
(C2 end → C2 evaluation → C3 Phase A → train/ORG-GATE → FREEZE → Phase B → evaluation; COLLAB-1 after C3 Phase B, or in parallel only if the owner says so); automatic halt at any limit; **no automatic restart** after a halt. RG2-LEARNED (R2's ninth condition) stays out unless ORG-GATE/1 returns LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM **and** the owner authorises that arm.
Approval token: `sha256sum evidence/ogi013-phase2/RESOURCE_PLAN.md` (any edit invalidates it). The limits equal the sum of the per-episode caps (34,870 requests; 63.4M tokens) plus ~15% / ~10% for discarded attempts; expected use is far below them (see the estimate columns).

## Open decisions that only the owner can make (blocking)
1. **Lift the HOLD** of 2026-10-28T10:17Z ("do not resume without explicit owner order") and authorise resumption of C3 — Phase A/B cannot start without it.
2. **PREREG_LOCK.txt is absent although `airline:2` already ran.** Rule how the protocol treats that block (valid / excluded / run again) — no lock may be created retroactively by an agent.
3. **Which code runs C3:** the locked implementation (`ogi013-org-bridge` d887dfb, lock hashes match) has BudgetGovernance session budgets but not the pilot-grade per-step ParentBudget, request counting by `provider_attempt_count`, or the lease-contract preflight. Running as locked keeps the pre-registration intact; porting the controls changes locked files and needs a dated amendment before more C3 data.
   Recommended: run C3 as locked, with per-episode session ceilings from an owner-created `runs/host_budget.env` (calls 110, tokens 200,000, cost 0.0) plus a campaign-level guard in a NEW file (does not touch locked files).
4. Whether to complete C2 (R0) at all: it is "a separate, new experiment"; skipping it removes 16 episodes but RUNBOOK step 1–2 treat its end as a precondition.
5. The campaign-level guard and the COLLAB-1 launcher/evaluator are offline work still to be written (new files; hash-frozen before launch). They are not authorised live work and were not started here.
