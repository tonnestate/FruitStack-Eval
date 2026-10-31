# QA2D_LOCK_v2 — provenance addendum 1 (append-only; retrospective)

**Written at 2026-10-31T23:20:46Z, AFTER 40 new v2 rows (14 questions) had already been collected (v2 run 22:53:39Z–23:10:12Z). This addendum was NOT present before the first v2 model call.** QA2D_LOCK_v2 (commit `f88e7d7`) is unchanged; there is no lock v3.

## Bootstrap file (`runners/ogi013_host_bootstrap.py`)
| item | value |
|---|---|
| sha256 of the file at source commit `dde6307` (`git show dde6307:…`) | `02934ed3a181949f867852a6d55b7e3a2ecee6cf2b26ac3b5ddece238e827659` |
| sha256 of the executable file in the v2 runtime worktree (`/root/fruits/integration/ogi013-collab-proof/runners/ogi013_host_bootstrap.py`) | `02934ed3a181949f867852a6d55b7e3a2ecee6cf2b26ac3b5ddece238e827659` (identical) |
| git blob id at `dde6307` / HEAD / working file | `ce9b66b46f128143290d39b6ce7fdcf41daf1b8e` in all three |
| last commit touching the file | `e3abd24` (2026-10-30T17:53:26+01:00), before the launch |
| file mtime | 2026-10-30T17:43:16+01:00, before the launch (2026-10-31T22:53:39Z) |

## Evidence that the executed source matched the locked revision (state-based, not name-based)
- Launch: repository commit `f88e7d7` (lock commit, 2026-10-31T23:53:37+01:00 = 22:53:37Z, two seconds before the run started), source commit `dde6307`, runtime path `/root/fruits/integration/ogi013-collab-proof`, command: `run_qa1.sh` with `OGI013_RUNNER=runners/ogi013_qa2d.py`.
- The HEAD reflog shows no commit between the lock commit and this check; the tracked tree is clean (0 changed tracked files).
- All runner and analysis hashes listed in QA2D_LOCK_v2 were recomputed at the time of this check and MATCH: ogi013_qa2d.py, ogi013_qa1.py, ogi013_argument.py, ogi013_vote.py, ogi013_team_code.py, analyze_qa2d.py, analyze_qa1.py.
- Component sources printed by the bootstrap at launch (`OGI013_SOURCE` lines in `runs/qa2d_v2/study.log`): mangome 835d8be, orangeme 953e725, peachme efa9bab, pomelome 348975e, plumme v0.1.9-92-ga81546c (= a81546c), cherryme c905539, appleme c2ee35a.
  QA2D_LOCK_v2 lists five component commits; OrangeMe, PomeloMe and AppleMe are recorded here for the first time. Their "changed_or_untracked_entries" (PomeloMe 3, AppleMe 10) are untracked `__pycache__` entries only; `git describe --dirty` shows no tracked modification (checked at this addendum).
- Limit: the process's executed bytes were not captured at launch; the conclusion rests on file hash = committed blob, mtime before launch, clean tree and an unchanged HEAD since launch.

## Accounting preserved at the time of this addendum
Results file `runs/qa2d_v2/out/run/results.jsonl`: 238 rows (198 reused SL + 40 new), sha256 prefix `91dad87ced57ead0`. `invocations.json`: `{"used": 73}`. PlumMe receipts in the v2 window: 42 nemotron provider attempts (39 success, 3 failed); the remaining 31 of the 73 invocations are Luna (Codex) calls, which PlumMe does not receipt.

## Truth state at the time of this addendum
GitHub `main` = `sync/local-truth` = `ab6cabe5`; canonical local `main` and `sync/local-truth` = `ab6cabe` (fast-forward only); the nine uncommitted ABC items in the canonical checkout are byte-identical to before (45 files hashed before/after).
