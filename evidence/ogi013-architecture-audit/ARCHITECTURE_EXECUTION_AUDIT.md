# OGI-013 architecture-vs-execution audit (2026-11-02; zero provider calls; read-only on code and recorded rows)

Flags: IMP = implemented, TST = offline tests exist and pass, ACT = called by `run_T`/`run_E` in QA-2D v2, REAL = rows that exercised it. Proofs are file:line in `audit.json` (key lines below).

| component | IMP | TST | ACT in QA-2D v2 | REAL data |
|---|---|---|---|---|
| CherryMe adaptive control (Brother Mode run_rounds/_run_parallel, ACE orchestrator/ensemble) | yes | yes | NO | yes |
| EVC (fs_codemode/evc.py) | yes | yes | NO | NO |
| Shapley (fs_codemode/shapley.py) | yes | yes | NO | NO |
| Code Mode facade / duo / sieve / contract | yes | yes | NO | yes |
| PlumMe model and route selection | yes | yes | partial | yes |
| MangoMe shared state | yes | partial | partial | yes |
| CogC (context compilation) | yes | not run | NO | NO |
| Argument verification (classify_argument + sandbox) | yes | yes | yes | partial |
| Evidence-weighted answer fusion | partial | yes | NO | NO |

Key proofs
- QA-2D decision path: `runners/ogi013_qa2d.py` run_T:153 -> ask:189 -> luna_step (qa1:326) / nemo_step (:103) -> Episode.step (tau2_agent:292) -> LineageHeart (lineage_heart:64, PINNED_MODEL) -> PlumMe; classify_argument :230/:263; TeamState/MangoLedger :163-164; run_E:307 = drafts + majority_tie_luna:37.
- No import of `evc`, `shapley`, `fs_codemode`, `cherryme` or `cogc` in `runners/ogi013_qa2d.py` (imports at :9-23).
- Tests run 2026-11-02: CherryMe brother 16 passed, CherryMe responsibility/ensemble set 36 passed, PlumMe 499 passed/7 skipped, FSE codemode+argument+qa2d+parity 36 passed, MangoMe-related FSE 45 passed; `test_ogi013_mango_acceptance.py` 10 skipped (no Mongo URI).

## What QA-2D v2 does and does not support
QA-2D v2 executed a simplified baseline: two blind first answers (Luna, nemotron), at most two critique/reply exchanges with a sandbox/format argument check, a fixed closing rule (verified last objection, else Luna), and independent controls. It did not execute CherryMe's adaptive control or responsibility consolidation, EVC-driven activation, Shapley-informed selection, the Code Mode facade, CogC compression or evidence-weighted fusion, and PlumMe only supplied a pinned model with route failover. The 53 evaluated questions (40 usable T rows, of which 4 reached an exchange) are not a test of the intended organisation. This audit makes no claim about the hypothesis in either direction.

## Offline analysis on the 40 OK T rows (descriptive; selected sample: infrastructure-failed rows excluded; no claim)

| first answers / result | correct | 95% exact CI |
|---|---|---|
| Luna first | 34/40 | [70.2, 94.3]% |
| nemotron first | 38/40 | [83.1, 99.4]% |
| team final | 36/40 | [76.3, 97.2]% |

- The 4 disagreement rows (8284, 7661, 517, 7855): Luna's first answer correct in 0, nemotron's in 4, team final correct in 2. In 7661 (NO_CONSENSUS, final = Luna's current answer) and 7855 (nemotron conceded to a formal objection) the final was wrong although nemotron's first answer was right.

### Shapley sensitivity (post-hoc attribution; depends on the stated assumption: a critique link with a single member is inert: v({m, link}) = v({m}))

| no-critique reference for {luna,nemo} | luna | nemo | link (critique exchange) |
|---|---|---|---|
| Luna's first answer (as shipped) | +39.17 | +49.17 | +1.67 |
| nemotron's first answer (alternative) | +40.83 | +50.83 | -1.67 |

The link's contribution is the final accuracy minus the chosen reference, so it flips sign with the reference; points are accuracy points on 40 rows.

### EVC replay: 4 recorded disagreement rows exist (fit half 21 rows with 3 disagreements). EVC cannot be calibrated or evaluated on them; no policy comparison is reported.
