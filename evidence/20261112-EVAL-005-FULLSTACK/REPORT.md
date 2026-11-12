# EVAL-005 F3 repair runs and first operational full-FruitStack missions (2026-11-12)

Exploratory engineering evidence. Nothing here is confirmatory; the 50 inquiry tasks are DRAFT (no owner-approved references) and
their HIST/ORG split was inspected during diagnosis, so it is not held-out any more. Grader `fse-inquiry/1` unchanged in every run.

## 1. F3 (frozen inquiry-engine arm) vs single AUTO call, same 50 tasks, zero-charge supply

Raw data: `/root/fruits/research/FRUITSTACK-EVAL-005-RERUN-20261112/{.,run2-search-retry,run3-key-fixes,run4-retrieval}`
(`results.jsonl`, `graded.jsonl`, `classified.jsonl`, per-shard receipts, `REVISIONS.txt` in run 4). Classifier: `runners/eval005_classify.py`.

| run | change under test | F3 correct (verdict+key, verified evidence) | F3 verdict right | F3 answered | F3 wrong verdict | F3 tokens | control correct* |
|---|---|---|---|---|---|---|---|
| 1 | today's stack + PlumMe zero-charge screen (34152e2) | 7 | 11 | 11 | 0 | 907,346 | 43 |
| 2 | + CherryMe search retry (e75e184) | 11 | 15 | 16 | 1 | 1,246,901 | 43 |
| 3 | + slash dates, key retry (FSE c399387) | 18 | 19 | 22 | 3 | 2,161,987 | 33 |
| 4 | + PDF text, EUR-Lex via Publications Office, worker-failure trace (CherryMe 3a164b4), key value from prose (FSE ddc4ff1) | 21 | 25 | 26 | 1 | 2,070,539 | 38 |

\* The control answers from model knowledge with retrieved excerpts as context; it has NO evidence requirement. Its number is factual
correctness only and is not comparable with F3's source-verified correctness. It varies with the AUTO model draw (run 2: gpt-oss-120b,
run 3: laguna-xs-2.1).

Every F3 answer in runs 1-4 is backed by quorum-verified primary evidence. Run 4 abstentions (24): 11 no admissible source on the
PRIMARY-ALLOWLIST/1, 7 sources delivered but unverified, 6 retrieval failures. Run 4 verdict-right-without-key (4) are KEY_NOT_IN_EVIDENCE:
the verified quote does not contain the asked value and the extraction worker said UNKNOWN.

Wrong verdicts accepted by two verifiers (run 3), from the recorded replies: inq-law-07 = verification logic ('Article 2' was no asserted
value; fixed CherryMe 46abcd3, replay over 88 recorded SUPPORTS promotions drops only these); inq-tech-10, inq-law-05 = correlated
misreading of one shared quote by small verifier models (laguna-xs-2.1, mistral-nemo) whose values are present: not catchable by a
deterministic check. In every eval run PlumMe selected with competence status UNKNOWN (632/632 in run 3): each shard starts with an empty
state and PLUMME_COMPETENCE_SNAPSHOT was never set.

## 2. Operational full FruitStack missions (runners/fs_runtime.py, PEACH-MISSION/1 + research phase)

Raw data: `/root/fruits/research/FRUITSTACK-FULLSTACK-OPERATIONAL-20261112/` (`REVISIONS.txt`, `run.sh`, `out*/`). Real PlumMe supply,
zero-charge dispatch, isolated PlumMe state, frozen competence snapshot of the live service (content sha256 da87a7a7...). MangoMe memory
backend, OrangeMe local ledgers (no production writes). Tasks A/B (+B control) from `config/fs_runtime/offline_fixture.toml`, host-executed checks.

| attempt | stack change | outcome |
|---|---|---|
| 1 | - | every Brother Mode solve step BUDGET_RESERVATION_BELOW_OUTPUT_LIMIT: headless gpt-6-luna bills ~17,170 input tokens/call, worker child budget exhausted after 4 LSD steps, never replaced |
| 2 | PeachMe 6e5b784 (exhausted worker retired + replaced) | replacement works; solvers answer correctly but without the ANSWER line the host reads -> NO_CANDIDATE |
| 3 | FSE f794dd3 (objective asks for the ANSWER line) | candidates found; executed checks CONTRADICTED correct `math.isqrt(n)` / `math.comb(n, k)` (argument list) -> FALSIFIED nodes |
| 4 | FSE 313c14b (call with arguments executed; non-call text no evidence) | **A, B, B-control: mission_success true**; executed check SUPPORTS; MangoMe checkpoint, OrangeMe memory, AppleMe diagnosis, knowledge applied in B; 24 receipts, 19 ok, 292,648 tokens, cost classes INCLUDED 17 / ANONYMOUS_FREE 5 / FREE_TIER 2 |

`integration_path_ok` stays false in attempt 4 only for unrecovered provider failures (rate limit, timeout -> Brother Mode NO_SECOND_SOLVER in A).
Learning: applied vs control on B both reward 1.0 -> NO_EFFECT_OBSERVED (n=1).

## 3. What is and is not shown

Shown (live-executed, independently checked by the host's executed check): the integrated chain MangoMe -> PeachMe -> CherryMe RG/2 inquiry
-> Research Tree / LSD Room / Brother Mode with PlumMe workers (competence-driven selection) -> PhysalisMe tool evidence -> AppleMe
diagnosis and advice -> executed verification -> knowledge -> MangoMe checkpoint -> OrangeMe ledger, on two simple tasks.
Not shown: any organizational gain, any advantage over a single model or over an Anthropic reference, behaviour on hard tasks.
Not connected: Aurora's deep-mission worker calls CherryMeEngine directly and never runs this chain (needs MangoMe reachable as www-data).
