# QA-2D protocol amendment A1 (versioned; 2026-10-31) — written BEFORE any restarted confirmatory execution

## Record of what happened
- Lock v1: `QA2D_LOCK_v1_SUPERSEDED.txt`, committed at `6c20e7a` (code frozen at `84ed28f`). It is preserved unchanged.
- The run was started under lock v1 (21:57Z), then stopped by explicit PIDs at 22:24Z when the lead's correction order arrived. It had written 246 rows: 198 reused SL rows and 48 new rows (16 questions: T/E/SN).
  These rows are archived at `runs/qa2d/out_superseded_prelock_1/` (results.jsonl sha256 prefix `51e9deccfb18d02e`). They are **not** used by the restarted analysis (new output directory; the analysis reads only the new
  `results.jsonl`). Nothing was deleted or edited.

## Post-lock changes (6c20e7a -> 9c86db6), complete list for the locked files
| file | change | effect on QA-2D arms |
|---|---|---|
| `ogi013_qa2d.py` | T: the exchange loop stops when no objection was filed (no second identical critique round) | **protocol-relevant, T only**: removes a repeated critique round; applies only when both critiques are "ISSUES: NONE" |
| `ogi013_qa2d.py` | failures carry the provider's own message (`reason`, `provider_message`) | logging only |
| `ogi013_qa1.py` | `DUO_EPISODE_TOKENS` constant; `EPISODE_MAX_TOKENS` gains the "TC" arm | none for T, E, SL, SN (T and E keep 400,000) |
Other commits touch only files outside the lock (Code Mode facade, adapter, replay, host-check driver, tests, docs).

## Independence from the 16 observed questions
- Of the 12 OK T rows among them, 11 agreed at once and 1 (qid 8284) reached consensus after one exchange with one objection. **No row contained the situation the T change affects** (an exchange with no objection filed), so the
  change could not have been, and was not, motivated by those observations. It came from the T/TC code comparison during the parity review. No threshold, prompt, scoring rule, sample or model supply was changed.
- The preregistered infrastructure rules (no retry, pause above 10 % after 40 questions) are unchanged.

## SL reuse: compatibility checked (`runners/check_sl_reuse.py`, no model call)
Same 198 ids in the same order, same question text/options/key, prompt bytes identical (`QUESTION_PROMPT + ANSWER_SUFFIX`), identical Codex invocation (argv, stdin, CODEX_HOME), 198 L rows all OK. Result: compatible. The
reused rows keep `reused_from: "QA-1 L"`.

## Restart conditions
A new lock (v2) is written on the then-current commits before any restarted execution; it lists all component commits (none dirty), the prompts hash, the analysis script hash and this amendment's hash. Output goes to a new directory.
