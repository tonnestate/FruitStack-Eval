# G - Aurora mission latency, staffing, KIwiMe (read-only analysis, 2026-11-14)

Scope: all 25 results with runtime == "peachme-mission" in /var/lib/aurora/missions (of 72 results; 47 have no runtime field).
No model calls, no live-state writes; owner request texts not copied (ids and counts only). Scripts in the session scratchpad.
Outcomes: 12 COMPLETE/VERIFIED, 9 BOUNDED_ANSWER/UNVERIFIED, 3 BOUNDED_ANSWER/PARTLY_VERIFIED, 1 BLOCKED/UNRESOLVED; error_code None in all 25.

## Method and limits
- mission_record.json events have `seq` but NO timestamps. Phase times therefore come from peachme.sqlite3 `events.at`
  plus file mtimes: t0 = request.json mtime, end = result.json mtime (request->result = total wall).
- Phase boundaries: intake = t0 -> first session OPEN; setup = OPEN -> first `cherry:` STEP_ADMITTED; inquiry = first cherry admit ->
  last STEP_DONE/UNKNOWN before the first research/synthesis step; triage gap = inquiry end -> first `research:` admit
  (or synthesis admit when no research); research = first -> last `research:` event; synthesis = synthesis admit -> its STEP_DONE;
  return = synthesis done -> result written. Claim checks and triage are not separate sqlite events (claim checks are local computed
  checks), so they sit inside intake/setup/triage-gap. Step latency joined by receipt_id: 147/147 STEP_DONE joined to
  /root/.plumme/receipts.jsonl (fields provider, model, latency_ms, success, failure_class only).
- Only 1 of 25 missions entered research, so research stats are n=1 (not a distribution).

## 1. Phase breakdown (seconds, n=25)
| phase | median | max | share of summed wall |
|---|---|---|---|
| intake (request -> session open) | 4.7 | 6.0 | 3.3% |
| setup (open -> first inquiry step) | 1.2 | 3.3 | 0.9% |
| inquiry steps (CherryMe questions) | 74.4 | 514.7 | 81.8% |
| triage gap (-> research or synthesis) | 1.7 | 8.0 | 1.4% |
| research (n=1 mission) | 307.3 (that mission) | 307.3 | 8.4% |
| pre-synthesis gap | 0 | 4.2 | 0.1% |
| synthesis (1 model call) | 5.9 | 10.0 | 3.9% |
| return (state/memory return) | 0.2 | 0.4 | ~0% |
| TOTAL wall | 90.7 | 530.0 | 100% |
- Dominant phase: inquiry (82% of all wall time; 89% for the 24 no-research missions). Research is dominant only in its single mission
  (59% of 517 s). Everything else (intake, synthesis, return) is under 10 s.
- Inquiry is effectively serial: wall time / summed receipt latency of the mission's steps = 0.92 (median). Only the opening
  burst (3 steps admitted within 0.1 s in the sampled mission) overlaps; later steps follow one by one.
- Slowest missions: e135b7d2 (530 s total, inquiry 515 s, 19 steps), c301e2d1 (463 s inquiry), d2c4f248 (386 s inquiry).
- Failed attempts inside inquiry: 32 of 69 contribution rows are ATTEMPT_FAILED; their latency sums to 1298 s = 43% of summed
  inquiry wall (3010 s). Top failing missions lost 150-190 s each to failed attempts. 25 steps (one per mission) ended
  STEP_UNKNOWN -> ABANDONED after median 60 s (max 90 s) in flight.
- Failure classes (inquiry rows): TIMEOUT 10 (902 s combined), MALFORMED_OUTPUT 9, MODEL_UNAVAILABLE 8, QUOTA_EXHAUSTED 4, OTHER 1.

### Per-model latency (inquiry rows from mission records, seconds; staffed model, ok = no failure class)
| model_key | ok | fail | ok median | ok max | failed-attempt time |
|---|---|---|---|---|---|
| qwen3.8-27b | 15 | 15 | 27.3 | 84.9 | 942 s (max 90) |
| qwen3.6-27b | 13 | 9 | 35.0 | 78.1 | 237 s (max 90) |
| qwen3.5-397b-a17b | 2 | 2 | 60.6 | 81.4 | 32 s |
| qwen2.5-vl-72b-instruct | 2 | 3 | 6.7 | 6.7 | 8 s |
| gpt-6-luna | 4 | 0 | 9.4 | 10.8 | 0 |
| qwen3.5-9b | 0 | 2 | - | - | 77 s |
| claude-haiku-5-5 | 1 | 1 | 8.8 | 8.8 | 2 s |
Receipt-side view of all 147 joined steps (ok only): gpt-6-luna n=80 median 6.4 s max 34.9; Qwen3.8-27B n=15 median 27.3 max 84.9;
Qwen3.6-27B n=11 median 37.6 max 78.1; Qwen2.5-VL-72B n=9 median 6.7; gpt-oss-120b(groq) n=4 median 1.6; laguna-xs-2.1 n=5 median 3.4;
mistral-small-3.2-24b n=5 median 3.0; nemotron-bolt-e4b n=5 median 6.3. Synthesis is always gpt-6-luna (about 6 s).
Failures at receipt level: groq gpt-oss-20b, freellmapi north-mini-code, ovhcloud Qwen3.8-27B each 1 SEMANTIC_OUTPUT_FAILURE.
Caveat: the 24 h receipts file (9519 receipts) is dominated by ~200-call probe batches per model (median 0.3-2 s), not mission work; do not read it as mission latency.

### Research phase (the one mission, 81772a97)
~307 s. Rounds of lsd/solve/challenge/revise steps across 3-4 concurrently opened workers (gpt-6-luna, Qwen2.5-VL-72B, nemotron-bolt-e4b,
mistral-small; luna took part in every round). Failures: 2 SEMANTIC_OUTPUT_FAILURE, 2 RATE_LIMITED, 1 NO_WORKER_SLOT; loop guard stopped after
2 rounds. Workers retired after one failure each, then replaced (extra worker opens ~3 s each, environment reserve/bind).

## 2. Staffing (CherryMe organization records, 69 inquiries-rows, all 25 missions)
- Every responsibility is a single PRIMARY (REASONING 43 times, FALSIFY 12, PROVOKE 1); no multi-worker inquiry organization was staffed.
- Staffed: qwen3.8-27b 27x, qwen3.6-27b 17x, qwen3.5-397b 3x, qwen2.5-vl-72b 3x, gpt-6-luna 3x, qwen3.5-9b 2x.
  (claude-haiku-5-5 appears only as fallback evidence worker.)
- ALL staffed models have competence_status UNKNOWN with competence_evidence_n = 0; selection_weight 0.10-0.12 everywhere.
  Selection is therefore not competence- or latency-driven in these missions.
- Faster qualified alternative exists in the data: gpt-6-luna (median 9.4 s inquiry / 6.4 s over 80 receipts, 0 failures in 84 steps incl.
  synthesis) is staffed in only 3 of ~55 responsibilities, while qwen3.8-27b (median 27 s, 50% failed rows, up to 90 s timeouts) takes 27.
  Qwen2.5-VL-72B (median 6.7 s) is also faster but failed 3 of 5 rows (QUOTA/malformed), so evidence is thin.

## 3. KIwiMe
- Units: aurora-kiwime-recovery.timer (active, every 5 min) + .service (oneshot, last run 09:47 CET, idle).
- /var/lib/aurora/kiwime/status.json (observed 2026-11-14): counts VERIFIED 0, AWAITING_VERIFICATION 0, RECONCILIATION_REQUIRED 0,
  REJECTED 0, ABANDONED 1. recovery.sqlite3: 1 instance, 3 history rows, 1 contract.
- The single instance (2fae07b0...) belongs to mission 13d2ca20, step cherry:985c8ed5..., first RECONCILIATION_REQUIRED (journal 00:17:52
  CET), then ABANDONED at 00:18:52 because the signed evidence fact (kiwime-evidence/fact-f88d...json, verifier plumme-receipt-verifier)
  says receipt failed: AUTH_FAILED (succeeded=False).
- Answer: NO live mission/step has reached VERIFIED through KIwiMe recovery. Journal for the last 3 d shows only that one episode,
  then idle runs. learning_feedback tables are empty in all 25 PeachMe DBs (0 VERIFIED/PARTIAL feedback rows).
- Gap: 25 other steps ended STEP_UNKNOWN -> ABANDONED (timeouts, 60-90 s) inside PeachMe but only 1 reached KIwiMe, so KIwiMe's
  recovery path is not exercised by the common timeout case (HYPOTHESIS why: those steps are abandoned by PeachMe/CherryMe policy
  before reconciliation is required).

## 4. Improvement candidates
1. MEASURED - Cut wasted wait on failing slow routes. 43% of inquiry wall (1298 of 3010 s) is failed attempts; 10 TIMEOUTs alone cost 902 s
   (60-90 s each, mostly qwen3.8-27b / qwen3.6-27b on ovhcloud). A per-call deadline near ~30 s (ok p100 for fast routes is <35 s) or
   hedging to a second route after ~15 s would remove most of that.
2. MEASURED - Staffing ignores observed latency and reliability: all competence UNKNOWN (n=0), weights ~0.1. Feed receipt-derived
   latency/failure stats into selection; gpt-6-luna (median 6-9 s, 0/84 failures) vs qwen3.8-27b (27 s, 50% failed rows). Needs a
   quality check first, since competence is unmeasured (luna sample for inquiry is only 4 ok rows).
3. MEASURED - Inquiry steps run essentially serially (wall/sum latency 0.92), with up to 19 steps per mission (e135b7d2: 515 s).
   HYPOTHESIS - independent questions on different claims (e.g. GAP on claim A and claim B) could run concurrently; wall then approaches
   the longest chain instead of the sum. Requires confirming claims are independent in CherryMe's scheduler.
4. MEASURED - Research (when entered) is round-based with workers retired on a single failure and replaced; 307 s for one mission, with
   rate-limit and unusable-output failures and a loop guard stop. HYPOTHESIS - a retry/ fallback with a known-good fast worker
   (luna) instead of opening fresh workers each time would shorten it; n=1, treat as weak.
5. MEASURED - Fixed overheads are small (intake ~5 s, synthesis ~6 s, return 0.2 s); optimizing them yields under 10% of wall.
   The 5 s intake (context restore + claim checks before session open) is the only candidate there.
6. MEASURED (gap) - KIwiMe has recovered nothing to VERIFIED; the timeout class (25 ABANDONED steps) bypasses it. HYPOTHESIS - routing
   timed-out steps through KIwiMe reconciliation (check whether the provider finished late) could recover some answers instead of
   re-asking; unverified that late completions exist.
