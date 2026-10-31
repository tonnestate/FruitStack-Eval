# OGI-013 QA-2D: pre-registration (lead order 2026-10-31; 0 EUR, no Claude member)

## Question
On MMLU-Pro (test split), does the Luna + nemotron duo, organised as a blind-answer / cross-critique / concession protocol (T), answer more questions correctly than (a) Luna alone (SL) and
(b) the same members at equal effort without organisation (E)? Nemotron alone (SN) is descriptive.

## Items
400 MMLU-Pro test ids in QA-1 hash order: sort all question ids by `sha256("OGI013-QA1|" + id)`; the first 198 are the QA-1 ids, the next 202 complete the set. Question texts are never committed.

## Arms (paired per question; sequential questions)
- **T (duo):** Luna and nemotron-3-ultra-550b answer blind in parallel (2 calls). Equal parsed letters: final = that letter. Otherwise cross-critique (each member judges the other's answer using exactly
  the labelled parts CLAIM / EVIDENCE / CONSEQUENCE), replies by the objected member naming the objection id, at most 2 exchanges, position changes logged. A concession counts (owner rule) if the objection is
  independent, substantive (GROUNDED_FORMAL or better), named by the response and the position change is logged; the objection then ends ACCEPTED. Unresolved after 2 exchanges = NO_CONSENSUS:
  final = the current answer of the member whose LAST objection was GROUNDED_VERIFIED, else Luna's.
- **E (equal effort):** k blind drafts alternating Luna / nemotron (Luna first), k = T's call count on that question (at least 2), majority vote of the parsed letters, tie goes to the tied letter Luna gave first.
- **SL:** Luna alone, 1 call. For the 198 QA-1 ids the QA-1 L rows are reused (identical prompt and model); the other 202 are run with the identical prompt.
- **SN:** nemotron-3-ultra-550b alone, 1 call (same prompt).
- Answer format: strict `ANSWER: <letter>`, last occurrence, option-range check (as QA-1). An infrastructure failure of any call makes that arm-row INFRA_FAILED (no rerun, no hidden retry); it counts as incorrect.

## Tests
Confirmatory, two-sided alpha 0.05, exact McNemar on discordant pairs, Holm over 2: **H1L** T vs SL, **H1c** T vs E. Paired risk difference with the exact conditional CI.
Sensitivity: the same tests on questions without any infrastructure failure in any arm.
Descriptive (outside the family): T vs SN; disagreement rate; chains with their three labels (CRITIQUE_ACCEPTED, INDEPENDENTLY_VERIFIED, QUALITY_IMPROVED) and key-based classes
(IMPROVING / PROTECTIVE / NEUTRAL / HARMFUL); HARMFUL changes; formal vs verified argument counts; tokens and calls per arm; MangoMe reads/writes.

## Execution
Sequential questions; PlumMe `RunBudget` hard cap of 3,000 invocations (nemotron provider attempts incl. route failover, plus Luna invocations); no hidden retries. The run pauses (exit 76) and reports on
a subscription or provider limit message, on an infrastructure-failure share above 10 % in any arm after 40 questions of the current process, or when the run cap is reached. A pause is not a failure: the run
resumes on the same lock without re-running finished rows (a row interrupted by a limit message is discarded and re-run).

## Claim boundary
The only allowed statements are of the form: "On QA-2D (MMLU-Pro test, n = <n>, <date>), T answered x % correctly vs y % (SL) and z % (E); paired differences with CI and Holm-adjusted p." No sentence says the
organisation "helps", "improves" or "adds value"; no ranking or superiority wording; a formal argument is never called "correct" (correctness is decided only by the key).

## Seal
`QA2D_LOCK.txt` records, before the first study call: the id-list hash and dataset hash, the sha256 of the prompts, of this file, of `analyze_qa2d.py` and the runners, and the component commits.
