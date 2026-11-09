# OGI-013 confirmatory study — stage budget and authorization request (2026-11-09)

**Nothing here is authorized.** An approval names ONE stage and the sha256 of this file and of `PROTOCOL.md` as locked; any edit invalidates it (package §0 rule). Approval of stage k does not approve stage k+1.

## 0. Owner decisions required before the lock
| id | decision | why it is the owner's |
|---|---|---|
| D1 | Confirm dataset licences: BigCodeBench-Hard (Apache-2.0 inferred from the parent card) and MATH-500 (MIT inferred via prm800k/hendrycks). Both `LICENSE_UNCONFIRMED` in `datasets.json`. | legal |
| D2 | BCB-Hard grader semantics. **A (current, #18):** candidate isolated from the tests behind a JSON boundary → only 16/148 tasks eligible → F2 descriptive, the two-family rule can never be met, no claim beyond MATH. **B:** official BigCodeBench semantics (candidate + hidden tests in one process, as the benchmark defines correctness) inside the same bwrap sandbox (no network, no /root, rlimits), plus a static tamper audit of the candidate (unittest/sys.modules/os._exit/`__import__` manipulation → row flagged and graded FAIL); eligibility re-derived offline (reference must pass). **Not yet measured:** the 128 tasks excluded only by boundary rules (53 reference-fails-under-boundary, 44 in-process mock.patch, 31 in-process filesystem inspection) are the candidates; the count is known only after B is built and run offline (zero cost). B reverses a hardening made after review, so it is a protocol choice, not an engineering fix. | grader integrity vs. task supply |
| D3 | Merge authorization (order in §3). | outward-facing, production repos |
| D4 | Subscription headless routes in the roster: `gpt-6-luna` (Codex/ChatGPT plan) and `claude-haiku-5-5` (Claude Code plan). They cost USD 0 per call but consume the owner's plan quotas, and today `gpt-6-luna` is the **only** role-qualified lineage. | owner quota |
| D5 | Stage S0 budget (§2). | spend authority |

## 1. Cost rules for every stage
- Hard cap **USD 0.00** billed. Only routes whose PlumMe cost class is LOCAL, ANONYMOUS_FREE, FREE_TIER with confirmed key, TRIAL_CREDIT where the provider enforces no overage, or (if D4) the two subscription headless routes. PlumMe AUTO policy (owner override 2026-10-27), `charge_observed` fail-closed settlement (PeachMe #37).
- PlumMe RunBudget per stage = the caps below; exceeding → exit 3, `BUDGET_STOP`, rows so far descriptive.
- No retry of an uncertain step (CherryMe no-replay guard); exhausted routes are not re-probed inside their cooldown.
- Resumable: rows are keyed (stage, family, task, arm); a finished row is never re-run.

## 2. Stages (estimates from the offline T row: 8 calls at n_solvers 2; confirmatory T with 3 solvers, revision, specialist and one advice round ≈ 15 calls; ≈ 3,000 tokens per call incl. output ≤ 2,000)
| stage | content | calls (est.) | tokens (est.) | cap (1.5×) |
|---|---|---|---|---|
| **S0** qualification | PlumMe REASONING qualification of up to 8 candidate lineages on MATH-500 levels 1–4 (366 items, disjoint from F1), 30 items each, held-out rule of PLUMME-FINAL-ACCEPTANCE 2026-11-09; output = roster (≥3 solvers + specialist), R_mono pin, best-S_m | 240 | 0.7 M | 360 calls / 1.1 M |
| S1 EVAL-001 main | T, E_div, R_mono, G_mas, S×4 (V reuses E_div drafts) on F1 (134) + F2 (16 under A; ≤ 144 under B, measured before lock) | ≈ 64 / task → 8.6 k (F1) + 1.0 k – 9.2 k (F2) | 29 M – 53 M | 26.4 k calls / 80 M |
| S2 ablations | F1: T-appleme, T-lsd; F2: + T-executed_critique — only components that passed the activation rule in S1 | ≤ 10.3 k | ≤ 31 M | 15.5 k / 46 M |
| S3 EVAL-003 | phase 1: 4 members × 3 × pool; phase 2 on frozen U: T, E_div, R_mono (+V) | 3.3 k + 45·|U| | ≤ 28 M | 9.3 k + 68·|U| |
| S4 EVAL-002 | memory / no-memory / sham on eligible transfer tasks (eligibility frozen first; < 120 → descriptive) | ≤ 45 / task | ≤ 37 M | 1.5× of eligible × 45 |

Throughput assumption (to be measured in S0, not promised): 20 schedulable workers → S1 takes several days on free quotas. The lock is valid for 30 days (package §8).

## 3. Merge order (D3)
PlumMe: canonical local `main` of `/root/fruits/sync/PlumMe` (31 commits ahead of origin, contains #25) pushed to origin first → CherryMe #14 → CherryMe #15 → PeachMe #37 (close #36) → PeachMe `fsi/ogi-research-injection` (new) → FruitStack-Eval #14 → #15 → #16 → #19 → #21 → #18 → #17 (retarget base to main; 4 new files only) → #20 → `fsi/ogi013-final-integration` (new: real-path T arm, two drift fixes, this protocol). Deploy only on separate authorization.

## 4. What happens after approval of S0
Automatic, no further question: S0 runs to completion → roster report → the lock (`STUDY_LOCK.txt`, PROTOCOL §12) is written and committed → stop and present the lock hash for the S1 approval. If S0 qualifies < 3 distinct lineages the study ends with that result (PROTOCOL §3).
