# OGI-013 research status: Brother Mode as an organized cognitive system

Offline work only. No provider call, no new experiment, no archived record changed. Branch `ogi013-collab-proof`.
Reproduce the reconstruction: `runners/ogi013_reconstruct.py --runs /root/fruits/research/OGI013-QA1/runs --out evidence/ogi013-reconstruction`
(generated: `evidence/ogi013-reconstruction/EPISODES.json`, raw per-episode exchange copies in `sources/` with sha256, `discoveries.jsonl`).
Ground truth in every table below is the benchmark answer key of the question. A model's statement that it is right is never used as proof.

## A. Brother Mode implementation audit (code facts)

| mechanism | where | state |
|---|---|---|
| independent first answers | `cherryme/brother.py` `run_rounds` / `_run_parallel` (n_solvers, parallel, each solver blind) | IMPLEMENTED, exercised (QA-2D v2, S1) |
| cross-model criticism | same; CRITIQUE ledger rows, format `ISSUES: FOUND/NONE`, `CLAIM/EVIDENCE/CONSEQUENCE` | IMPLEMENTED, exercised (12 objections in the 57 reconstructed episodes) |
| evidence verification of an objection | `runners/ogi013_argument.py` `classify_argument` + sandbox; levels suggestion / formal / reproduced / independently_confirmed | IMPLEMENTED. For multiple-choice items nothing can be executed: every observed objection is `executed: false` (suggestion or formal). Verification power on this benchmark is therefore close to zero (see D) |
| replies, concessions, revisions | reply actions `concede`, `evidence`, `withdraw`; REVISION rows | IMPLEMENTED, exercised (concessions in 605, 8284, 517, 7661, 7855, 8512) |
| decision / closing | `runners/fs_codemode/loop.py` `CooperationControl` (WeightBook, `close()`), corrected in `a10d7c9`, `d2c1116` | IMPLEMENTED, corrected. Evidence-free weights can no longer decide (`UNRESOLVED_PRIMARY_RETAINED`); same-lineage samples are one member |
| model selection and execution | PlumMe AUTO, `ogi013_lineage_heart.py` pins models; receipts per call | IMPLEMENTED; identity now validated from receipts (`INFRA_INCOMPLETE` fail-closed) |
| evidence persistence | MangoMe work identity + ledgers, `MangoLedger`/`TeamState`; per-episode events and exchange files | IMPLEMENTED (archived outside the repo under `/root/fruits/research/OGI013-QA1/runs/`, now copied per episode into `evidence/ogi013-reconstruction/sources/`) |
| organizational knowledge | CherryMe `knowledge.py` `KnowledgeStore` + `KnowledgeFirstGrounder`: quote-verified source facts, hash chain, `lookup`, reuse counter | PARTIAL: stores and reuses grounded document facts; no link from a stored item to a later outcome; not wired into QA-1/QA-2D/S1 |
| learning of team structure | `ogi013_org_learning.py`, `evidence/ogi013-learning/SPEC.md`, `ORG_GATE_V1.json` (RANDOMIZED structure arms, Keras policy, gate) | IMPLEMENTED as contract + store + tests; NO data (no randomized verified episodes) |
| EVC / Shapley / CogC | `fs_codemode/evc.py`, `shapley.py`; CogC | IMPLEMENTED and tested, NOT active in QA-2D/S1 (audit 2026-11-02), no calibration data (4 disagreement rows) |
| answer fusion by evidence weight | `loop.py` | PARTIAL: only decisive with an independently confirmed objection; otherwise the primary's initial answer is kept |

Missing: (1) a verified-discovery ledger with retrieval/application/outcome (added now, section E); (2) any verifier for item types that cannot be executed; (3) randomized-structure data for the learner.

## B. Evidence reconstruction (57 recoverable episodes)

The earlier statement "archived S1 records do not contain the complete critique history" is corrected: the per-episode exchange files survive in the run directories (`s1/run1/out/exchange/*.json`, `events/*.jsonl`) and hold first answers, every objection (target, lineage, level, state, decision path), every reply and the controller decision. They are now preserved in the repo with hashes. In S1 only 605 and 693 contain objections; the 12 Luna-only episodes contain none.

Sources: S1 16 T episodes (12 Luna-only duplication, 4 genuine duo), QA-2D v2 40 OK T episodes (genuine duo), 1 engineering host check (8512). QA-1 (198 rows) stored a single first answer per row: no collaboration to reconstruct. COLLAB-1 / pilot / tau2 episodes were not reconstructed (not part of the multiple-choice line; no per-episode exchange examined).

Effect on the primary (Luna's designated first answer) against the key:

| group | n | unchanged right | unchanged wrong | improved | degraded | changed, still wrong | episodes with an objection |
|---|---|---|---|---|---|---|---|
| QA-2D v2 duo | 40 | 34 | 3 | 2 (8284, 517) | 0 | 1 (7661) | 4 |
| S1 genuine duo | 4 | 2 | 1 (693) | 1 (605) | 0 | 0 | 2 |
| S1 Luna-only (not collaboration) | 12 | 5 | 3 | 1 (464) | 3 (11613, 11894, 1659) | 0 | 0 |
| host check (not study data) | 1 | - | - | 1 (8512, role order unrecorded) | - | - | 1 |

Documented correction cases (exact context):

| QID | context | first answers | key | final | reading |
|---|---|---|---|---|---|
| 464 | S1, Luna-only duplication | Luna F, second Luna sample E | E | E | final correct by registration-order tie-break; not a collaboration, not reproducible under the corrected rule (retains F) |
| 11613 | S1, Luna-only | H (right), sample F | H | F | harm by tie-break; not collaboration |
| 11894 | S1, Luna-only | D (right), sample H | D | H | harm by tie-break |
| 1659 | S1, Luna-only | H (right), sample G | H | G | harm by tie-break |
| 7985 | S1, Luna-only | H, second Luna sample A | A | H | the right answer existed in a second Luna sample and was not selected: sample diversity, not cross-model cooperation. Corrected rule also keeps H, as it must without evidence |
| 8512 | engineering host check (`qa1b/hostcheck1`), TC/T arm, Luna + nemotron, not study data | one answer A, one F (arrival order only) | F | F | nemotron objection (formal, not executed) accepted by concession; correct. One observation, outside any preregistered design |

Other genuine-duo events (all objections model-asserted, `executed: false`):
- Corrections toward the key: 605 (nemotron objection, Luna concedes J to B), 8284 (nemotron right, Luna concedes), 517 (nemotron right, Luna concedes).
- Harmful concessions: 7855 (Luna's formal objection, empty-set argument; nemotron's correct A conceded to G) and 7661 (Luna's tie argument; nemotron's correct D conceded, final A is neither first answer). In both, the final was wrong while a correct first answer existed; the single arms SL and SN were correct on both items.
- 693: Luna objected to nemotron, nothing moved, both first answers wrong.

Observed vs hypothetical: everything above is observed. The only hypothetical is `S1_COUNTERFACTUAL.json` (corrected controller replayed on archived closings; not an experiment).
Not recoverable: raw provider response bodies beyond the exchange texts (not copied; receipt ids are in the events); the second Luna sample's role ordering in the host check; any stored or reused discovery (none was ever recorded).

Net, descriptive, genuine duo only (44 episodes; 8512 excluded as non-study): 3 corrections of Luna's first answer by nemotron-side objection or answer (605, 8284, 517), 0 harm to a right Luna first answer, 2 harmful concessions that destroyed a right nemotron first answer (7661, 7855).

## C. Organizational learning assessment

Cycle: discovery -> independent verification -> storage -> retrieval -> later application -> measured outcome.

| step | status |
|---|---|
| discovery (collaborative) | observed: 6 genuine-duo episodes produced a changed or conceded answer |
| independent verification | only against the dataset key (post hoc, not available to the system at run time); 4 supported, 2 contradicted. Nothing was executed or independently verified by the system itself |
| storage | CherryMe `KnowledgeStore` stores grounded source facts but none of these. The new ledger (E) stores them with state and provenance |
| retrieval | 0 retrievals of any discovery in any run |
| later application | 0 |
| measured outcome with control | 0 |

Result: 0 organizational-learning instances. 4 verified discoveries are `STORED_NOT_REUSED`; 2 are `FALSIFIED` and kept as negative findings (7661, 7855: the concession path accepted a wrong claim). The multiple-choice items are task-specific (applicability: same question only), so they cannot test transfer; an EVAL-002 test needs tasks that share reusable knowledge (for example repeated policy rules in the tau2 domain) and a control without the store.

## D. Scientific evidence assessment

EVAL-001, organizational intelligence gain.
- S1: invalid for the question (12/16 runs were Luna twice); not evidence against Brother Mode.
- QA-2D v2: closed infeasible (infrastructure share above threshold; 53 of 400 planned questions). Primary counts (failures counted wrong): SL 41/53, SN 39/53, T 36/53, E 36/53. Complete cases T vs SL (n=40): 36 vs 34, T vs SN (n=38): 34 vs 36. Cost: T 902,513 tokens and 129 calls vs SN 47,649 tokens and 53 calls over the same 53 questions (about 19 times the tokens).
- Corrected / damaged / unchanged (QA-2D, 40 OK rows): corrected 2, damaged 0 right Luna answers, unchanged 37, one changed-still-wrong. Against the stronger single member (nemotron first answer 38/40) the team (36/40) is lower.
- No significance claim: counts are small, the sample is selected by infrastructure success, the pair design is exploratory.

EVAL-002, organizational learning: no reuse was ever recorded; see C.

EVAL-003, emergent capability: among the 53 QA-2D questions with all of T, SL and SN, there is no question that T solved while both single arms failed. The two questions where T was wrong while a single arm was right are the two harmful concessions. Even if one existed, it would first have to be separated from sampling variance of one model (SL was right on 7661 and 7855 where Luna's in-team first answers were wrong), majority voting and extra compute (control E exists for compute).

Structural limit found: for multiple-choice items no objection can be executed, so cooperation is a persuasion channel in both directions (4 pulls toward the key, 2 away, none checked by the system). Without an independent verifier or a task type with executable checks, Brother Mode cannot be expected to show a systematic gain here; this is a property of the benchmark choice, not a defect of the controller.

## E. Implementation corrections made now (offline, no experiment)

- `runners/ogi013_reconstruct.py`: reproducible episode reconstruction, evidence levels kept apart (model_asserted / executed / dataset_key).
- `runners/ogi013_org_discoveries.py`: append-only hash-chained learning ledger. Model "verification" is rejected, same-run reuse does not count, an outcome needs a recorded application and a control, falsified claims are kept, and "learned" is derived, never asserted. Seeded offline from the reconstruction only (6 discoveries, nothing invented for retrieval or application).
- Tests: `tests/test_ogi013_org_discoveries.py` (6), `tests/test_ogi013_reconstruct.py` (2); with `test_ogi013_s1_integrity.py` 25 pass.
- Not done on purpose: wiring the ledger into live runs (no new experiments ordered), changes to CherryMe/PlumMe/MangoMe worktrees (other work in progress there).

## F. Final research status

| claim | status | basis |
|---|---|---|
| A cross-model objection can change an answer to the correct one | PARTIALLY DEMONSTRATED | 3 study observations (605, 8284, 517) + 1 engineering observation (8512); the same channel also removed a correct answer twice (7661, 7855); no chance control |
| EVAL-001 net organizational gain over the best single member | INVALID OR INSUFFICIENT EVIDENCE | S1 invalid (identity defect); QA-2D v2 infeasible; team below nemotron alone on complete cases; cost about 19x |
| EVAL-002 organizational learning | NOT YET DEMONSTRATED | 0 retrievals/applications; storage and ledger exist, no later-task test |
| EVAL-003 emergent capability | NOT YET DEMONSTRATED | no item solved by the team that both members failed |
| The earlier negative S1 conclusion about Brother Mode | INVALID OR INSUFFICIENT EVIDENCE | controller and identity defects; the replay is hypothetical and proves nothing positive either |

No status was changed by the repair of an implementation defect. What would settle the questions (not started, needs an order): a task family with executable verification so objections can be independently confirmed; a Nemotron supply that does not exceed the 10 percent failure threshold (or a second reliable lineage); a repeated-knowledge task set with a no-store control for EVAL-002.
