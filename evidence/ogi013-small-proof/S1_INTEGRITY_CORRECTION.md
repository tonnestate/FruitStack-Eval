# S1 integrity correction (2026-11-07) — append-only; PREREG.md, selection.json, s1_results/results.jsonl and S1_RESULT.md (historical verdict) are unchanged

## Defect
`claim_slot()` in `runners/ogi013_qa1.py` returned `"solver1"` when both slots were taken. CherryMe retries a failed solve once; when the nemotron (solver2) solve failed, the retry was assigned to solver1 and executed as a **second Luna solve**. The row check (`len(firsts) < 2`) counted solution rows, so Luna twice passed and the row was stored as status OK. `final_positions` then holds Luna twice (`gpt-6-luna@codex`, `gpt-6-luna@codex#1`) and the controller chose between two Luna samples.

## Corrected validity classification of the stored S1 T rows (offline, `ogi013_s1.py --reclassify`; `S1_RECLASSIFICATION.json`)
| Class | Rows | qids |
|---|---|---|
| GENUINE_LUNA_NEMOTRON (both lineages submitted a first answer) | 4 | 1876, 605, 3121, 693 |
| LUNA_ONLY_DUPLICATION (no nemotron position, Luna twice in final_positions) | 12 | all other 12 |
| INFRA_FAILED | 0 stored (the 12 should have been INFRA_INCOMPLETE) | — |
Controller decisions over all 16 T rows: CONSENSUS 8, VERIFIED_OBJECTION 0, PROVISIONAL_UNVERIFIED 8 (weights or a formal concession chose among unverified candidates; none is evidence of improvement). Among the 4 genuine rows: 1876 correct (consensus), 3121 correct (consensus), 605 correct (formal concession, provisional), 693 wrong (weights, provisional).

## Consequence
The S1 estimate (0.720) and its verdict ("advantage not shown") do not test the Luna+nemotron hypothesis: 12 of 16 rows are Luna-vs-Luna sampling. The historical verdict is kept as recorded; it must not be cited as evidence for or against OGI. 4 genuine rows are far too few for any estimate. A corrected experiment requires a new prospective protocol/version (not created here; no run was made).

## Implementation changes (runners/ogi013_qa1.py, runners/fs_codemode/loop.py, runners/ogi013_s1.py)
1. `SolverSlots`: each slot is claimed once; a further claim returns None and the solve fails with `SOLVER_SLOT_EXHAUSTED` without any provider call (no fallback to solver1/Luna).
2. `solver_identity_problems`: validates the submitted positions from execution data (executed model key, lineage, receipt id), recorded at submission time; duo requires luna AND nemotron lineages and models; distinct lineages always.
3. A missing independent member raises `Infra("INFRA_INCOMPLETE")` (also replaces the old row-count check); the row carries `solver_identities`.
4. Closing record and T row: `provisional`, `verified_improvement` (true only for an independently confirmed objection), `unresolved_disagreement` (all candidates preserved), `selection_status` (VERIFIED / CONSENSUS / PROVISIONAL_UNVERIFIED). The rule names are unchanged; unverified weights are no longer presentable as evidence-backed.
5. `classify_t_row` / `reclassify` for the offline reclassification.
6. Tests: `tests/test_ogi013_s1_integrity.py` (7 tests). On the pre-fix code 5 of them fail (including "DID NOT RAISE Infra" for a failed nemotron solve); the 2 that pass there are offline checks of the stored rows.
