# OGI-013 research status — reconciled C1 / C2 / C3 / pilots (2026-10-29)

Sources: repository files, `runs/` evidence, hash re-computations done in this session (read-only). Nothing historical was changed.

## C1 (observation; FIXED vs ADAPTIVE; 20 airline test-split tasks)
- Result as recorded (`evidence/ogi013-c1-airline-test/RESULT.md`): official grades FIXED 3/20, ADAPTIVE 3/20 (tasks 6, 13, 19 in both arms), 0 discordant pairs, delta 0.0; descriptive means ADAPTIVE−FIXED: −9.0 provider calls, −43,433 tokens, −85.9 s. 17/20 failed in both arms (floor effect).
- Integrity: `c1-airline-test.SHA256SUMS` re-verified: 911 OK, 0 FAILED, 0 missing.
- **Erratum candidate (not applied; history untouched):** RESULT.md says "free routes only", but `integrity.json` lists TRIAL_CREDIT receipts in kept arms (FIXED 6, ADAPTIVE 5). TRIAL_CREDIT is zero-cash but a consumed entitlement.
  Other recorded limits: model mix differs per arm under AUTO; 20 discarded arms (simulator route failures); no randomisation or grader provenance attested.

## C2 (pre-registered 2026-10-27; same 20 tasks; one intervention in AppleMe events)
- NOT COMPLETE and NOT EVALUATED: `PROTOCOL.md` only; no RESULT/compare/rows/integrity file. progress: 12 task pairs ended exit 0 in both arms (2, 6, 18, 19, 24, 29, 31, 35, 37, 44, 45, 48; a runner exit is not a grade), 8 pairs incomplete
  (8, 13, 16, 22, 25, 26, 30, 32) — 16 arms without an official result (`supervisor/c2_missing_official_results.txt`), 42 discarded entries (all "simulator route failed"). Canonical C2 state: "separate, new experiment", unfinished.

## C3 (pre-registered; AMENDMENT-1 + ERRATUM-1; lock revisions 1–9)
- Registered: conditions SINGLE, SINGLE-E, FIXED, RG2-OFF, RG2-OFF-NOPERSIST, RG2-NO-TRIAGE, RG2-NO-VERIFY, RG2-NO-KNOWLEDGE, RG2-LEARNED (only if ORG-GATE/1 permits AND the owner authorises), RG2-RANDOMIZED (Phase A only). H1 RG2-OFF>SINGLE, H1c >SINGLE-E, H2 >FIXED, H3 >NOPERSIST,
  H4 LEARNED>OFF (only if testable), H5 ablations descriptive. Exact two-sided McNemar, α 0.05, Holm over {H1,H1c,H2,H3,(H4)}, Clopper-Pearson on discordant pairs; unit = task block; unknown/incomplete = non-success; ≤3 attempts per block (whole-block discard only for SIM_ROUTE_FAILED), then INFRA_INCOMPLETE.
- Design: Phase A = 20 airline test + 26 retail train (seed 1013, holdout 0.3) = 46 tasks, RG2-RANDOMIZED. Phase B = 14 retail held-out tasks × 8 (or 9 with LEARNED) = 112–126 episodes. ORG-GATE/1: ≥300 rows, ≥40 tasks, ≥12 test tasks, ≥40 rows per structure, ECE ≤ 0.10, log-loss-gain CI lower bound > 0.
- **Lock integrity:** all hashes in `AMENDMENT-1.LOCK.txt` (latest revision per file) MATCH on the locked code branch `ogi013-org-bridge` (d887dfb), including `ogi013_tau2_agent.py` 4e4d5e79, `ogi013_sim_supply.py` 12e707f5 and `rg2_trace_report.py` f40b0f1f (re-computed with `git show d887dfb:<file>`).
  They MISMATCH on `ogi013-collab-proof` (HEAD 7782562, 12 commits ahead of d887dfb) because the pilot work edited those three locked files. **Consequence: C3 must run from the locked code (d887dfb / the ogi013-org worktree), never from this branch.** The collab-proof edits are pilot-only (gated by `OGI013_PILOT_BUDGET`, tests assert
  the frozen path is unchanged) but they are not part of the registered implementation; carrying any of them into C3 needs an owner-approved lock amendment before further data is collected. No lock was created or modified in this session.
- **Missing artefacts:** `PREREG_LOCK.txt` and `FREEZE.txt` do not exist; `supervisor.sh` requires the former before any C3 run — yet `airline:2` already ran (reward 1.0, 52 decision rows). This is a process anomaly to be ruled on by the owner; it must not be "fixed" by creating a lock now.
- **Phase A state:** 1 of 46 blocks complete (airline:2); airline:6 started and failed (CalledProcessError, exit code not recorded); 6 `airline:2-interrupted*` discards; no `learned/`, no attestation; Phase B and FREEZE not started.
- **Authorisation state:** `PHASE_A_RELEASE` 2026-10-28T09:08Z, then `HELD by owner order (resource control) … do not resume without explicit owner order` at 10:17Z; queue stopped; no `runs/host_budget.env` (no cash authorised); no token/request ceiling exists for the campaign.
- **Prerequisites not met today:** (1) C2 unfinished/unevaluated (RUNBOOK step 1–2), (2) PREREG_LOCK absent, (3) owner HOLD, (4) no campaign resource authorisation, (5) pilot-grade per-step/request controls exist only on collab-proof, not in the locked code (see RESOURCE_PLAN §Open decisions).
  → **Phase A and Phase B were not started** (not permitted by their actual prerequisites and authorisations). Offline C3 work possible without touching locked files: none outstanding that is unblocked; the learner/gate code and tests exist and pass in the offline suite.

## Pilots (exploratory, outside the registered study)
PILOT-1 stopped before inference (LEASE_BUDGET_EXPANSION, 0 spend); PILOT-2 stopped at agent step 10 (input bound by bytes; fixed); PILOT-3 never ran; PILOT-4 completed both arms (0.0/0.0, see `PILOT4_ANALYSIS.md`). Each authorization was single-use and is exhausted.
