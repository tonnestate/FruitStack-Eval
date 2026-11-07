## PLAN A

1. ACTION: Replace nemotron-3-ultra gateway with a locally-run small model (e.g., Qwen2.5-7B or Llama-3.2-3B via ollama/vLLM) as the second lineage; keep Luna (gpt-6-luna via Codex) as the primary.  
   WHY: Nemotron supply fails 429/502 and leaks reasoning at length caps, making any cooperation signal unreproducible. A local model gives deterministic availability and zero cash cost.  
   VERIFY: Run 50 synthetic QA-2D items; both models return answers without 429/502 errors and without reasoning leakage (check token counts < cap).  
   COST: ~200k tokens for local inference; owner quota unchanged.

2. ACTION: Implement a minimal "Brother Mode" evaluation harness that runs the full CherryMe closed loop (blind drafts → cross-critique → named replies → EV-based round decision → closing) on each item, logging every intermediate artifact.  
   WHY: QA-2D tested a simplified baseline, not the full architecture; offline unit tests exist but never ran on real items. The harness makes the full loop observable.  
   VERIFY: Harness produces a complete JSON trace per item (drafts, critiques, replies, EV scores, round count, final answer) for 10 items; owner inspects one trace end-to-end.  
   COST: ~50k tokens for 10 items × 2 models × ~3 rounds; sandbox code only.

3. ACTION: Construct a preregistered comparison design: (A) Luna alone, (B) Local model alone, (C) Full CherryMe loop (Luna + Local), (D) "Best-of-2" oracle (pick the correct single-model answer when they disagree). Run on 200 held-out multiple-choice items (e.g., MMLU subset).  
   WHY: Exploratory rows only show nemotron often right when disagreeing; this doesn't separate cooperation from "pick the better model". Condition (D) isolates the selection effect; (C) vs (A)/(B)/(D) isolates cooperation.  
   VERIFY: Preregistered JSON spec (items, seeds, stopping rules) committed before run; results CSV with per-item accuracy for A/B/C/D; statistical test (McNemar, α=0.05) showing C > max(A,B,D) with p<0.05.  
   COST: ~2M tokens total (200 items × 4 conditions × ~2.5k tokens); spread over 4 weekly quotas (500k/week cap).

4. ACTION: Add a "cooperation diagnostic" to CherryMe: log per-round agreement/disagreement, critique acceptance rate, and EV-driven continuation decisions.  
   WHY: Without mechanism-level evidence, a win on (C) could be luck. Diagnostics reveal whether the loop actually uses cross-model information.  
   VERIFY: For each item in the 200-item run, produce a cooperation report: rounds used, % critiques incorporated, final answer source (Luna/Local/synthesized). Owner checks that C items show non-trivial critique incorporation (>10% of rounds).  
   COST: Negligible extra tokens (logging only).

5. ACTION: Integrate CogC (context compression) into the CherryMe loop so critiques/replies stay within a 4k token context window without truncation artifacts.  
   WHY: Nemotron leaked reasoning at length caps; local models also have context limits. Compression prevents silent degradation in later rounds.  
   VERIFY: Run 20 items with and without CogC; verify token counts stay <4k and final answers identical (deterministic compression).  
   COST: ~100k tokens for 20 items × 2 conditions.

6. ACTION: Wire PomeloMe (idempotency keys) and MangoMe (work ledger) into the harness so every run is replayable and auditable without re-spending tokens.  
   WHY: Owner quota is scarce; re-running failed/partial studies burns budget. Idempotency + ledger enables exact resume and audit.  
   VERIFY: Kill harness mid-run at item 150; restart with same run-id; verify it resumes at 151 and final ledger matches a full uninterrupted run.  
   COST: ~50k tokens for test kill/resume cycle.

7. ACTION: Run a pilot OGI-013 study: 50 items from a distinct domain (e.g., GPQA biology) using the full stack (PlumMe routing → CherryMe loop → CogC → PomeloMe/MangoMe → AppleMe assurance checksum).  
   WHY: Previous OGI-011/012 blocked by supply; this validates end-to-end integration on a new domain before scaling.  
   VERIFY: Pilot produces a signed AppleMe assurance bundle (input hash, code version, output hash, per-item traces) that owner can verify offline. Accuracy on (C) exceeds (A) and (B) by ≥5% absolute (directional, not powered).  
   COST: ~500k tokens (one weekly quota).

8. ACTION: If pilot shows directional cooperation signal (C > A,B), preregister a powered OGI-014 study (n=500 items, α=0.05, 80% power for 4% absolute gain) and execute in 5 weekly batches. If not, halt and publish negative result with full traces.  
   WHY: Zero-cash constraint demands hard go/no-go criteria. Publishing negative results preserves credibility and avoids quota burn on dead ends.  
   VERIFY: Preregistration JSON + final CSV + AppleMe bundle + statistical report (effect size, CI, p-value) posted to owner's repo.  
   COST: Up to 5M tokens over 5 weeks (500k/week cap); only spent if pilot passes go criterion.

## PLAN B

1. **[BOTH] ACTION:** Mark QA-2D “infrastructure-infeasible; cooperation effect unknown” and suspend superiority claims. **WHY:** Supply failures and reasoning leakage undermined the study; disagreement results do not show that cooperation adds value. **VERIFY:** Study records and summaries use this status and make no added-value claim. **COST:** Minutes; no model calls.

2. **[MERGED] ACTION:** Select two distinct free or local model lineages only after a small, hard-capped viability check. Confirm local runtime and hardware are available before choosing a local model; require both candidates to meet fixed reliability and valid-answer thresholds. Nemotron is optional. **WHY:** Nemotron’s gateway has failed often, and local capacity is unknown. **VERIFY:** A short report records model/version, successful completions, malformed responses, latency, and resource use; stop if no pair passes. **COST:** Small capped calls or local setup; no cash.

3. **[L] ACTION:** Preregister a narrow paired benchmark: items, scoring, exclusions, prompts, versions, sample size, conditions, and analysis. Include each model alone and the full Brother Mode loop; define how failures and malformed outputs count. **WHY:** QA-2D used a simplified baseline, and the closed loop has not been run in a real study. **VERIFY:** A dated protocol exists before scored calls. **COST:** A few hours; no model calls.

4. **[MERGED] ACTION:** Inspect and verify the live harness uses the intended FruitStack path, including CogC, PeachMe, MangoMe, OrangeMe, PomeloMe, AppleMe, PlumMe, CherryMe, and Code Mode sandbox limits. Add attempt-level logging, idempotent replay, and measured token/latency accounting. **WHY:** Existing QA-2D did not test the full architecture; offline tests do not establish real-study behavior. **VERIFY:** A small dry run produces traceable component, budget, assurance, and replay records. **COST:** Engineering time and a tiny capped dry run; no cash.

5. **[MERGED] ACTION:** Compare Brother Mode against both standalone models and a deployable answer-selection baseline using only inference-time information; keep prompts, items, and call caps comparable. **WHY:** Existing disagreement rows could reflect choosing the stronger model, and a ground-truth oracle would not be a fair deployable baseline. **VERIFY:** Report paired outcomes, uncertainty, failures, and token use for every condition. **COST:** Bounded by the preregistered cap; defer extra baselines if they exceed it.

6. **[N] ACTION:** Run a small cost-measuring pilot before considering a larger study; set a hard token ceiling and stopping rule in advance. **WHY:** The weekly quota must be protected, and proposed larger studies have speculative costs. **VERIFY:** Pilot report gives actual per-item costs and whether the loop can be completed within the ceiling; do not scale if it cannot. **COST:** Small capped run; zero cash.

7. **[L] ACTION:** Change controller weights only from independently scored, held-out outcomes, with a preregistered evidence threshold. **WHY:** The controller is unit-tested offline but has no real-study evidence validating its contribution weights. **VERIFY:** Each weight change links to held-out evidence; otherwise weights remain unchanged. **COST:** Engineering effort and local checks; no cash.

8. **[MERGED] ACTION:** Report negative or inconclusive results, supply failures, deviations, and uncertainty; require a fresh holdout before broader claims or scaling. **WHY:** Earlier studies were blocked by supply, and a single successful run cannot establish general cooperation gains. **VERIFY:** The report limits claims to tested models and conditions and documents the stopping decision. **COST:** A few hours of analysis; no extra calls beyond the cap.

**REJECTED:**

- Requiring Nemotron as a benchmark member: its supply history makes it an unreliable required condition.
- A fixed 50-item GPQA study and 200-item follow-up: those sizes and token estimates are not justified before measuring actual cost and viability.
- A five-prompt local smoke test as a prescribed setup: local hardware and runtime are unknown; first check availability, then use a capped viability check.
- Requiring nonzero critique acceptance or identical answers with and without CogC: these are not established success criteria for cooperation or compression.
- A specific “higher self-reported confidence” router: confidence may be uncalibrated; preregister a fair inference-time baseline appropriate to the chosen models.

## PLAN C

1. **ACTION:** Suspend OGI superiority claims and label the QA-2D result “infrastructure-infeasible; cooperation effect unknown.” **WHY:** Nemotron supply failures and reasoning leakage invalidated the study, while the earlier disagreement rows cannot distinguish cooperation from choosing the stronger model. **VERIFY:** The study record and any summary use that wording and make no added-value claim. **COST:** A few minutes; no model calls.

2. **ACTION:** Define one narrow benchmark and preregister its scoring, exclusions, model versions, prompts, sample size, and analysis before collecting new results. Include Luna alone, Nemotron alone, and the full duo; compare on the same items. **WHY:** QA-2D used a simplified baseline, and the full closed loop has not run in a real study. **VERIFY:** A dated protocol exists before the first scored call and specifies how missing or malformed responses count. **COST:** A few hours; no model calls.

3. **ACTION:** Make supply viability a capped go/no-go check using only free routes. Measure success rate, latency, cooldowns, and valid-answer rate; stop at a small preregistered call cap. **WHY:** Prior 429/502 refusals and length-cap reasoning leakage made the duo infeasible, and the owner’s weekly quota must be protected. **VERIFY:** A short report shows whether the route meets the preregistered thresholds without exceeding the cap; if it fails, don’t run the benchmark. **COST:** Small, hard-capped number of calls; no cash.

4. **ACTION:** Run the benchmark with paired items and randomized item order, keeping prompts and budgets fixed across conditions. Record every attempt, failure, retry, token use, and final answer. **WHY:** Existing exploratory results are confounded by Nemotron often being right when the models disagree; paired single-model controls are needed to test whether cooperation adds value. **VERIFY:** Reproducible per-item logs include all three conditions and preserve failures rather than silently dropping them. **COST:** Bounded calls set by the protocol; modest setup effort; no cash.

5. **ACTION:** Add ablations for “choose the better standalone model” and “simple answer aggregation” alongside Brother Mode. **WHY:** Current disagreement rows do not show that cross-critique or closing improves on selecting the stronger member. **VERIFY:** Results report each baseline and the duo’s paired difference, with uncertainty, on the same items. **COST:** Additional calls within the same cap, or defer ablations to a later preregistered run; no cash.

6. **ACTION:** Audit the real execution path before the study: confirm the full FruitStack components, run budgets, circuit/health state, idempotency, and Code Mode limits are actually active and logged. **WHY:** The architecture audit found QA-2D did not test the full architecture; offline unit tests don’t establish real-study behavior. **VERIFY:** A dry-run trace shows the intended components and budget decisions for a sample episode, with no external paid routes and no model-generated code outside a sandbox. **COST:** A few hours; one tiny capped dry run if needed; no cash.

7. **ACTION:** Keep the closed-loop controller from treating unverified agreement or a single benchmark win as contribution evidence. Update weights only from held-out, independently scored outcomes; require an explicit evidence threshold before changing routing. **WHY:** The brief says contribution weights should be verified, but there is no real-study evidence yet. **VERIFY:** Logs show the evidence supporting each weight change, and a test with unverified or in-sample signals leaves weights unchanged. **COST:** Engineering effort; local tests only; no cash.

8. **ACTION:** Set a stopping rule and publish results either way, including failures and negative or inconclusive outcomes. Repeat on a fresh holdout before claiming a general cooperation benefit. **WHY:** Earlier studies were blocked by supply, and a single dataset or successful run would not establish reliable added value. **VERIFY:** The report includes protocol deviations, supply metrics, paired outcomes, uncertainty, and a clear claim limited to the tested setting; any broader claim waits for replication. **COST:** A few hours of analysis and writing; bounded calls only; no cash.