# OGI-013 — Functional check of the team procedure (formerly "MICRO PILOT"; lead order 2026-10-30, amended before any grading)

This is a functional check of the team procedure. It is not an OGI test, not a benchmark result, and is never reported as one.
(The original order text is reproduced here in substance; sections 1-3 are unchanged, the title and section 4 are replaced by the amendment below.)

## 1. Evaluator v2.2 (defect D7)
Installed from the package (sha256 `7ed2e5404ff625eabe94acf6c500095614dbe1e7e9caefb728ed8d0f5dea33eb`); `CALIBRATION_v2_2.json` reproduced on the VPS (9/9); every recorded 11019 row re-graded as an additional v2.2 column, recorded grades never overwritten.

## 2. Tasks (package `ogi013-micro-pilot.tar.gz`, sha256 `0361ebfd4853170af23fdf33d87c49d4bf2290ed705e07bb5c43a17415450373`)
`micro__intervals-1`, `micro__duration-1`, `micro__lru-1`: seeded-bug repositories in the frozen driver's layout. Hidden tests check only behaviour stated in the issue. Built-in trap: a plausible first fix passes the visible tests and misses an edge case named in the issue. New tasks, no contamination risk.

## 3. Arms and caps
T team episode (frozen rules, MangoMe ledger, per-episode work/turn); S one sticky PlumMe AUTO author, same supply and caps; L Luna (Codex headless), same task prompt. Per episode at most 300,000 tokens and 30 min (CLI ceilings; loop guards unchanged). 9 episodes (3 tasks x 3 arms), one start each; a crash is that episode's result (`INFRA_FAILED`), no restart and no FIX. An episode killed by the end of the operator's session is `OPERATOR_INTERRUPTED` (not counted, kept, rerun once).
Output: grade all snapshots with v2.2; `CHAIN.md`; token count per arm.

## 4. Decision rule (REPLACED by the amendment of 2026-10-30)
The functional check yields only one of two outcomes:
- **STOP**, or
- **PROCEED_TO_C3_PLANNING**.
T resolving more tasks than S is **not** evidence of organisational value: n = 3, no token matching, no N arm.

## 5. Reporting rules (amendment)
- Tokens per arm are reported next to every resolved count.
- The report does not contain the claims "organisation helps / improves / adds value".
- Report once, after the 9 episodes: one table (task x arm: resolved, F2P, tokens, wall time) plus `CHAIN.md`.

## 6. Arm N (only after owner approval)
Same PlumMe supply, no organisation layer, same caps as T, on the 3 tasks, one start each, after the 9 episodes finish. Not started; requires the owner's approval.
