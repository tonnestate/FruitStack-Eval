# F3 (integrated FruitStack) vs AUTO single-call control — EXPLORATORY development run, 2026-10-14
Status: exploratory. The 50 development tasks (`tasks/dev/pilot_inquiry_tasks_DRAFT.jsonl`) have no owner-approved references; nothing here is confirmatory. The registered F2/F3 protocol was not touched.

## Question / hypothesis
Does the integrated FruitStack chain (CherryMe inquiry + independent quote-bound verification + knowledge + AppleMe assurance, PlumMe AUTO supply) answer the inquiry tasks better than a baseline with the same supply and the same task information? Prediction: higher correct-answer rate. (Not fixed before the run; the control definition was set after the first run, see deviations.)

## Conditions
- CONTROL (`runners/auto_control.py`, labelled F1 in the analyzer files only): same host retrieval as F3, excerpts in the prompt, ONE unpinned PlumMe AUTO call (up to 7 acquisitions = the F3 call budget of 14), no orchestration, no verification, no knowledge, no assurance.
- F3: `runners/f2f3_epoch2.py` (6 shards, 8-9 tasks each, own state/workspace/knowledge), PlumMe AUTO, per-task timeout 1200 s.
- Same 50 tasks, same retriever, no provider filter. PlumMe 0.1.12 (`122b81b`, selection repair), CherryMe `a667256`, FSE-analysis driver `223c5e4` (+ uncommitted `auto_control.py`), FruitStack-Eval `9a32b03`. Grading: `fse inquiry grade` (independent, references never seen by the system).

## Results (`estimates.json`, `graded.jsonl`)
| | CONTROL | F3 |
|---|---|---|
| correct | 37/50 (0.74) | 9/50 (0.18) |
| no answer / abstained | 8 | 31 abstained (CherryMe INCOMPLETE(SUPPLY)), 1 unreconciled timeout (inq-org-06) |
| mean utility | 0.75 | 0.27 |
| provider attempts / tokens | 118 / 34,090 | 808 / 764,714 |
| wall time (sum) | 806 s | ~16,260 s |
- F3 − CONTROL: success rate −0.56 [−0.74, −0.42]; utility −0.48 [−0.70, −0.29] (cluster bootstrap by subfamily). Concordance: control only 32, F3 only 4, both 5, neither 9.
- Among the 19 tasks F3 answered: F3 9 correct (47%), control 12 correct (63%) on the same tasks. On the 31 tasks F3 abstained, control was correct on 25.
## Interpretation (limits stated)
- Supported: under today's free supply the integrated chain did not outperform the baseline; it was worse, mostly because it abstained on 62% of tasks.
- Cause of the abstentions (receipts, not a controlled test): independent verification needs several delivered answers and the free routes failed (FORBIDDEN 61, RATE_LIMITED 51, SEMANTIC_OUTPUT_FAILURE 37, BILLING_OR_CREDIT_EXHAUSTED 27, TIMEOUT 8, MODEL_NOT_FOUND 4). Competing explanations (supply quality vs architecture) are NOT separated by this run.
- Not supported / not tested: organisational learning (18 findings were published, 0 reused: tasks are unrelated and each shard has its own knowledge store; no with/without-knowledge comparison was run); system-level advantage; any OGI claim.
- Component participation (F3 result.json, 49/50 tasks): PlumMe, CherryMe, AppleMe, knowledge store, independent quote-bound verification; MangoMe only as LOCAL_OUTBOX; PeachMe, PomeloMe, CogC, OrangeMe did not participate (not relevant to these inquiry tasks, no artificial activity created).
## Selection repair (PlumMe 0.1.12)
Before: 57/57 decisions of the first F3 run on kilo-gateway (`dev-f3-run0-preserved`). After: F3 receipts kilo-gateway 492, google 92, nvidia 75, pollinations 68, openrouter 48, llm7 33 of 808 (control: kilo 52, nvidia 30, google 12, openrouter 10, pollinations 8, llm7 6); selector `pool_spread`, propensities in decisions. Kilo remains the largest share because it delivered most successes; nvidia (FORBIDDEN credential) was tried once per model and never delivered.
## Economics
cost_usd is null (unknown) on 442 of 808 F3 receipts and 85 of 118 control receipts; FREE_ONLY routes, no paid call was configured, no billing evidence collected. Cost is unknown, not zero. Analyzer files map unknown to 0 only to run the tool. F3 used ~22x the tokens and ~20x the wall time of the control.
## Deviations
Control defined after the first (pinned openrouter/free, 32/50) run and after a manual-provider-pool attempt (archived `dev-f3-pooled-RESTRICTED-not-auto`) and an old-policy run (`dev-f3-OLD-POLICY-before-repair`); a 3-attempt control was abandoned for unequal budget (`dev-control/_abandoned-3attempt`). One F3 task timed out (counted as no answer, 1200 s). Shard-local knowledge stores. The F1 pinned run `20261014T023511Z-DEV-F1DEV-F3DEV` stays as history (its F3 had no retrieval; invalid).
## Reproducibility
Raw per-shard results, journals, DecisionLogs and receipts in `raw/`; `results.jsonl` → `graded.jsonl` (independent grader); `estimates.json`. Confirmatory F2/F3 experiment: unchanged, its independence gate (G2) still unsatisfied.
