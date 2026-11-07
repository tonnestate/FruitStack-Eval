# OGI-013 QA-1 — pre-registration (written 2026-10-31, before any QA-1 data exists)

**Question.** Does the organised FruitStack team (CherryMe challenge/revise rounds, PlumMe roster, MangoMe shared state) answer hard questions more often correctly than (a) its best constituent model alone, (b) the same models with the same number of calls and a majority vote, and how does it compare with Luna alone?

## Items
- **Primary:** GPQA Diamond, all 198 questions, if the dataset is accessible on the host.
- **Fallback:** MMLU-Pro (test split). Sort all question ids by `sha256("OGI013-QA1|" + question_id)` and take the first 198.
- The choice and the dataset file sha256 are recorded in `QA1_LOCK.txt` before the first model call on any study item.
- Question texts are never committed; evidence stores ids, hashes, answers and grades only.

## Arms (paired per question; same question prompt for every arm; answer format `ANSWER: <letter>`)
- **T — team.** CherryMe `run_rounds(parallel=True)`, 2 independent solvers of distinct lineages (blind until both submit), challenge, reply exchange (≤ 2 per objection), revision, `DEFAULT_MAX_ROUNDS`. The roster is pinned per question; small models (≤ 12B, nemotron-lightning/nano class) are excluded from every role. Every prompt's team state is read from MangoMe. Final answer: the agreed final position; without agreement, one independent specialist chooses among the existing final positions (it may not introduce a new answer).
- **E — equal effort, no organisation.** The same roster models, round-robin, `k` independent drafts, where `k` = the number of model calls T used on that question; majority vote on the letter; ties go to the earliest draft. No critique, no exchange.
- **S — best constituent.** One call per question by one fixed model: the model PlumMe AUTO ranks first for the solve role at lock time (recorded in `QA1_LOCK.txt`). It is pinned as T's solver 1.
- **L — Luna alone.** One call per question via the existing subscription route, no tools.
- Supply: free routes plus Luna via subscription; 0 EUR cash.

## Outcome and tests
- **Outcome:** correct if the parsed letter equals the key. An unparsable answer is incorrect.
- **Confirmatory family (Holm, two-sided alpha 0.05, exact McNemar on discordant pairs):**
  - H1: T vs S
  - H1c: T vs E
  - HL: T vs L
- **Effect size:** paired risk difference with an exact CI.
- **Power (simulated, n = 198, Holm over 3):** 98 % for +20 points, 87 % for +15, 53 % for +10. A non-significant result is a null result at this n, not evidence of equality.

## Descriptive (not confirmatory)
- Calls, tokens and wall time per arm.
- For T, per question:
  - first answers of both solvers vs the final answer, classified as wrong→right, right→wrong, unchanged;
  - number of grounded objections, REPLY events and answer changes, each with the ledger event that caused it.
- MangoMe reads and writes per question.

## Integrity
- `analyze_qa1.py` is committed together with this file and sealed in `QA1_LOCK.txt` (sha256 of both) before the first study call. No interim analysis.
- **Infrastructure failure of an arm on a question:** one rerun of that arm on that question. If it fails again, it counts as incorrect for that arm (primary). A sensitivity analysis excludes such questions from all arms. Both are reported.
- No other exclusion, no change of arms, prompts or tests after the lock.

## Claim boundary
- Allowed statement: "On QA-1 (dataset, n, date), T answered x % correctly vs y % (S), z % (E), w % (L); paired differences with CI and Holm-adjusted p."
- Not allowed: "intelligent", "superintelligence", "OGI proven". Also not allowed: a BenchLM ranking, because the items may be contaminated, which affects all arms equally.
