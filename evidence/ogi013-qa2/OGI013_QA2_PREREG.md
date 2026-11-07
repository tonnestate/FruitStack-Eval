# OGI-013 QA-2 — pre-registration (prepared 2026-10-31 while QA-1 runs; NOT started; written before any QA-2 data exists)

**What it is.** An exact replication of the sealed QA-1 protocol (`evidence/ogi013-lead/OGI013_QA1_PREREG.md`, sha256 `95c7a023f857d838b2b457a7b57d5a99c78910560976f8429823c1435c598bb2`) on **GPQA Diamond, all 198 questions**.
Everything not listed under "Differences" is identical: arms T, E, S, L; prompts; answer format `ANSWER: <letter>` (strict, last occurrence); outcome; confirmatory family (H1: T vs its constituent S model, H1c: T vs E, HL: T vs L; exact McNemar, Holm over 3, alpha 0.05); effect size; descriptive T trace; integrity rules (one rerun on infrastructure failure only, sensitivity analysis, no interim analysis); claim boundary; 0 EUR cash.
The analysis script is the SAME file as in QA-1 (`runners/analyze_qa1.py`, sha256 `d5803210feba3fc40803a5b8f94c089a8e90085ff49e06223b03227a85e79d6c`); the lock writer refuses to continue if its sha256 differs.

## Differences (all forced by the dataset, none by outcomes)
- **Dataset:** GPQA Diamond (`Idavidrein/gpqa`, `gpqa_diamond.csv`), 198 questions, 4 options. It is gated: QA-2 starts only when the owner has accepted the dataset terms and provided a Hugging Face token with access. This preparation never accepts terms and never works around the gate (`runners/prepare_qa2.py` stops with exit 3 without access).
- **Option order:** GPQA lists the correct answer first, so the options are put in a deterministic order from sha256("OGI013-QA2-options|" + record id + "|" + option index); the key letter follows. No random state.
- **S model:** selected at QA-2 lock time by the same procedure as QA-1 (AUTO first rank among models passing a 10-call availability probe) and recorded in `QA2_LOCK.txt`; it is again pinned as T's solver 1. H1 is worded "T vs its constituent <model>".
- **Lock:** its own file, `evidence/ogi013-qa2/QA2_LOCK.txt` (dataset file sha256, ids sha256, S model, sha256 of this file and of `analyze_qa1.py`, component commits, none `-dirty`), sealed before the first QA-2 call.
- Question texts are never committed.

## Order of work when access exists (`evidence/ogi013-qa2/start_qa2.sh --go`)
1. refuse while the QA-1 run is still active (shared supply); 2. `prepare_qa2.py --check`; 3. prepare data outside the repository; 4. `--select-s` probe; 5. write and commit the lock; 6. run all 198 x 4 arms with the sealed runner.
