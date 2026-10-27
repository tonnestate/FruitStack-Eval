# OGI-013 airline-test FIXED vs ADAPTIVE (2026-10-26) - observation only

- 20 paired tasks (tau2 airline test split), every pair: same PlumMe-selected simulator MODEL in both arms, arm order alternated by task-id parity, free routes only (PlumMe AUTO; PLUMME_TRIAL_CREDIT=off from 2026-10-26T15:28Z).
- Official tau2 grades: FIXED 3/20, ADAPTIVE 3/20 (tasks 6, 13, 19 in both arms). Discordant pairs: 0. Success-rate delta 0.0.
- Descriptive resource means (ADAPTIVE minus FIXED, per task, all attempts): provider_calls -9.0, total_tokens -43,433, wall_seconds -85.9. Cost/quota/human minutes unknown on free routes -> per-verified-success resources UNDEFINED (evaluator rule), complete_usage_pairs = 0.
- NOT shown: any causal or organisational advantage (evaluator: causal_effect_proven=false, organisational_advantage_proven=false). Floor effect: 17/20 tasks failed in both arms; many episodes ended by AppleMe LOOPING -> PeachMe reflex stop, so the lower ADAPTIVE usage may reflect earlier stops, not efficiency.
- Discarded attempts (simulator route failure, whole pair dropped and re-run, max 3): see progress.txt and discarded/. Cost evidence: `export_rows.py --cost-report` (all routes carry FREE cost_class; cost_usd null on many receipts, so free status is label-based, not measured). One TRIAL_CREDIT sim call occurred in a discarded attempt of pair 22 before trial credit was switched off.
- Files: rows.jsonl (evaluator input), compare.json (evaluator output), progress.txt.
