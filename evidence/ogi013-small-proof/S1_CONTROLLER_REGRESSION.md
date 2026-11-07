# S1 controller regression — decision defect, fix and offline counterfactual (2026-11-07). Archived S1 results are unchanged; S1 and OGI-013 stay paused.

## Observed (archived, 12 Luna-only T rows — one lineage twice, so no independent collaboration)
Initial answers (solver1's first answer) 8/12 correct; final controller answers 6/12. Lost: 11613 (H→F), 11894 (D→H), 1659 (H→G). Recovered: 464 (F→E). The 4 other WEIGHTS rows (1641, 7985 and the consensus rows) kept the initial answer.

## Precise decision defect (`CooperationControl.close()`, `runners/fs_codemode/loop.py`)
1. A second sample of the same model key (CherryMe names it `<key>#<n>`) was treated as an independent member: it got its own weight and entered the candidate list.
2. Both samples had the prior weight 0.5; the tie-break was `-order.index(member)` over the signature keys, i.e. **registration order = whichever sample finished first**, unrelated to the designated initial answer. In 6 WEIGHTS rows the first-finished sample was the extra one in 4 (11613, 11894, 1659, 464) and the initial one in 2 (1641, 7985): a coin flip between two samples of one model.
3. The result was labelled `WEIGHTS_DECIDE_UNVERIFIED` although no weight had any evidence (all weights were the untouched prior).
(The upstream cause — Luna twice instead of Luna+nemotron — was fixed in the previous correction, a10d7c9; this package fixes the controller so the same situation, or equal/unsupported weights in a genuine duo, can no longer overturn an initial answer.)

## Changes
- Same-lineage samples collapse into ONE member; extra samples are kept only as `unresolved_disagreement` with status `same_lineage_sample_not_evidence`. A closing over duplicates only is `SAME_LINEAGE_NO_INDEPENDENCE`: it retains the designated primary's initial answer, `independent_collaboration=false`, `verified_improvement=false`, never CONSENSUS. A single executed candidate passed through by a caller (tau2 action path) is unchanged.
- Initial answer: `control.primary_first` (set by `run_T` to solver1's first answer) is the initial answer, not the first-finished sample.
- Equal or insufficient weights: unless the best weight exceeds the primary's by at least one verified update (`step_verified` = 0.10), the closing is `UNRESOLVED_PRIMARY_RETAINED` (primary's initial answer, provisional, disagreement preserved). Weights that do exceed it still decide, as `WEIGHTS_DECIDE_UNVERIFIED`, labelled provisional, never verified.
- A critique between two samples of one model cannot move any weight nor count as an independently confirmed objection.
- Genuine collaboration keeps its ability to change the initial answer: an independently confirmed objection by a different member still gives `INDEPENDENTLY_CONFIRMED_LAST_OBJECTION` (verified); formal concessions keep their path.
- Test-mock fix: the parallel Org mock in `test_fs_codemode_loop.py` gave both concurrent solves to model L (the S1 duplication itself); it now routes distinct members. Rule expectations renamed where equal weights now retain the primary (3 loop assertions, 1 QA-1 parameter).

## Offline counterfactual (HYPOTHETICAL — archived closings replayed through the corrected `close()`; not an experiment; `s1_results/S1_COUNTERFACTUAL.json`)
| Group | Initial | Observed final | Hypothetical final |
|---|---|---|---|
| 12 Luna-only rows | 8/12 | 6/12 | 8/12 |
| 4 genuine Luna+nemotron rows | 2/4 | 3/4 | 3/4 |
The hypothetical 8/12 equals the initial answers **by construction** (no independent member exists; the fix retains the initial answer) — it removes an artificial loss, it is not evidence that the controller or cooperation helps. The corrected rule also gives back the one accidental recovery (464). The 4 genuine rows are unchanged (605 keeps its documented concession path; critique events were not archived, but all 16 stored closings had 0 independently confirmed objections). No claim of organisational added value.

## Tests
`tests/test_ogi013_s1_integrity.py` (17 tests; 11 fail on the pre-fix controller): observed cases 11613, 11894, 1659, 464 against the archive; counterfactual tallies; independence of registration order; same-lineage agreement is not consensus; same-member critique cannot move weights; genuine confirmed criticism still changes the initial answer; unsupported weights retain it, supported weights stay provisional. Full suite: 7 failed (the same 7 pre-existing unrelated failures), 670 passed, 11 skipped.
