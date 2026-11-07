# Simulator-route failures during the RG/2 demo (infrastructure, not results)

Evidence: runs/org-demo/d1-discarded-* (+ .log), state-discarded-*, org-demo-d1.route.discarded-*; per-attempt sim-usage.jsonl and plumme-state/{receipts,failure_receipts}.jsonl.

1. Hard-coded simulator cap: ogi013_sim_supply.py passed max_output_tokens=1024. The pinned reasoning model north-mini-code spent it on hidden reasoning
   (receipt: EMPTY_CONTENT finish_reason=length reasoning_present=True output_tokens=1024 max_tokens=1024); 34 of 44 calls failed. PROTOCOL.md says per-response
   limits are negotiated by PlumMe -> cap removed (None). First call afterwards succeeded (997 tokens).
2. Daily free-tier quota: after the cap fix north-mini-code was rate-limited on both free routes (kilo anonymous pool, OpenRouter); re-pinned model gpt-oss-120b (groq)
   answered one call, then HTTP 429 "tokens per day (TPD): Limit 200000, Used 198386". PlumMe cannot know the daily remainder before the call; the pinned model then has no
   eligible route (NO_EQUIVALENT_ROUTE) and the block is discarded (registered rule, whole block, max 3).
3. Credit routes listed by the catalog (TRIAL_CREDIT: nvidia, deepinfra, ...) are not executable now: nvidia FORBIDDEN, others PinnedWorkerUnavailable (no credentialed route).
4. Supervisor defects fixed: shared org-demo/state was not restored after a discarded attempt; run dirs were deleted/nested on retry (now archived under unique names).
5. Phase A is held until $SUP/PHASE_A_RELEASE exists.
