# FruitStack Riemann Hypothesis research — evidence archive (recovered 2026-11-20)

Recovered by Claude (research director) on owner order "RECOVER AND PUSH ALL EXISTING RIEMANN HYPOTHESIS RESEARCH EVIDENCE".
Archival only: no file was edited, no status was changed, nothing was re-run. Every file is a byte copy of its source;
`MANIFEST.jsonl` lists all 562 files with source path, SHA-256, size, modification time and `identical_to_source` (562/562 true at
copy time). Secret/privacy scan (API-key patterns, private keys, bearer tokens, e-mail addresses, personal names, home paths, IPs;
text files and `strings` of the SQLite/DuckDB files): no hits, nothing redacted.

## 1 Contents

| Directory | Source | What it is |
|---|---|---|
| `proofbook/riemann_hypothesis.jsonl` | `/var/lib/cherryme/knowledge/proofs/` | the RH proof book (AppleMe ledger), 94 hash-chained entries, 2026-11-15 21:46 → 2026-11-16 16:44 CET |
| `proofbook/riemann_hypothesis.backup-20261116164358.jsonl` | `/root/contracts/cherryme-continuity-2026-11-16/backup-…/` | the 71-entry state of 2026-11-16 16:43 (the "about 71 entries" of the operational report); a strict subset of the 94 |
| `cherryme-missions/<mission-id>/` | `/var/lib/cherryme/missions/` | 22 CherryMe missions whose record mentions the Riemann hypothesis: mission record, events, contributions, claims (`cherry/claims/C-*.json`), research tree, AppleMe event log and database |
| `longrun-2026-11-15/` | `/root/contracts/longrun-2026-11-15/`, `/root/contracts/operational-resilience-2026-11-15/STATE.md` | run outputs `riemann-mission14..22.out`, `riemann-org1.out`, escalations, state dumps, requests, `run-riemann.sh`, operational STATE (runs 6-9) |
| `contracts/` | `/root/contracts/` | `FRUITSTACK-RH-RESEARCH-1.2-FIRST-PASS-2026-11-07.md`, `OGI-RH-STRESS-TEST-DESIGN-2026-11-07.md` |
| `rh-research-v1.2/` | `/root/fruits/research/fruitstack-rh-research-v1.2/` | the 2026-11-07 research workspace: code, tests, contract test status, DuckDB research graphs incl. runs RUN-2026-11-07-LUNA-01..03 |
| `alpoege-audit/RH-EVIDENCE-AUDIT.md` | `/root/fruits/research/RH-2026-ALPOEGE/` | today's audit of the external Alpöge/Claude claim (not FruitStack research results) |

Already on GitHub before this archive (unchanged, this branch is based on it): branch `fsi/ogi-rh-harness`, commit `bac1847` -
`runners/ogi_rh/`, `evidence/ogi-rh-stress-test/`, `tests/test_ogi_rh_*.py` (the OGI-RH offline harness).

## 2 Chronology
- 2026-11-07: RH research 1.2 first pass (research graph, exact test-function certificates, equal-budget harness, LUNA runs 01-03) and the
  OGI-RH stress-test design; OGI-RH harness committed (`fsi/ogi-rh-harness`).
- 2026-11-15 08:27 → 10:28 CET: first wave of CherryMe RH missions (973b5c7f, a5f515a3, 608cd391, 808720dd, c4113820, b316c890, 59d57c8d,
  b81f490a, a6edee0e, 61dc01b7, 70984b14, 57510fab).
- 2026-11-15 17:46 → 2026-11-16 08:33 CET: long-run Riemann runs (593f122a, 5aea2c13, 8177d537, 67df373e, ce4b7b9b, 5fc8cfb1 = run 6,
  6d828e6c = run 7, 4377b0a0 = run 8, 7d97fd76 = run 9, 390455a0); the proof book starts 2026-11-15 21:46 with run 6.
- 2026-11-16 16:43: proof book at 71 entries (continuity backup); 16:44: last entry (94).
- No RH research entries after 2026-11-16 16:44 were found (the PNP-001 programme took over the research organisation).

## 3 Counts (computed from the archived files)
- Research sessions: **22 CherryMe missions** (1 COMPLETED, 21 UNRESOLVED); 16 of them wrote proof-book entries.
- Proof book, 94 entries: 1 TARGET, 9 KNOWN_RESULT (operator-seeded literature citations), 6 HYPOTHESIS, 15 NUMERICAL_EVIDENCE (each
  with one execution receipt, none independently checked: field `checked` empty), 44 APPROACH (25 `NOT_INVESTIGATED`, 19
  `INVESTIGATED_NO_PROOF`), 19 QUESTION.
- Mission claims: 49 (`cherry/claims/*.json`): **11 SUPPORTED, 38 UNKNOWN**.
- Claims with an actual proof: **0**. Statements proved: **0**. Independently verified mathematical results: **0** beyond the 11
  SUPPORTED mission claims, which are 11 copies of one known numerical fact (below), supported by each mission's own evidence check.
- Previously not on GitHub: everything in this archive except the OGI-RH harness (proof book, missions, run outputs, workspace v1.2,
  contracts).

## 4 Strongest findings (exact references; status as recorded, nothing relabelled)
1. "Die ersten 1000 nichttrivialen Nullstellen der Riemannschen Zetafunktion haben den Realteil 1/2." - SUPPORTED in 11 missions, e.g.
   `cherryme-missions/70984b14-…/cherry/claims/C-01M7F4KQXE69FQ3M0MN3E2S877.json`. A replication of a long-known computation (zeros
   are verified on the line far beyond this range; proof book seq 10 cites 3·10^12); not new.
2. Numerical evidence on zero statistics, proof book seq 18 (250 zeros, unfolded mean spacing 0.99967), seq 24, 26, 33, 38, 63 (first
   zeros on the line): finite computations with receipts, unchecked.
3. Hypotheses seq 60-62, 64-66 (simple zeros, linear independence of ordinates, spacing distributions, variance of zero counts): these
   restate known open conjectures; no derivation attached.
4. Anomalies that must NOT be read as evidence against RH: seq 67 lists "zeros" 4.83, 5.86, 10.17 (not zeta zeros - a faulty
   computation); seq 68/69 report negative Li-type coefficients for n <= 30, contradicting the known positivity of the first Li
   coefficients - almost certainly a computation error, never checked.
- No theorem, lemma or proof of an RH-related statement was produced. No Lean files exist in this research (the v1.2 Lean adapter never
  ran: Lean is not installed).

## 5 Missing or unrecoverable
- `FruitStack_RH_Research_Masterplan_v1.2_2026-11-07.md`: not found on this server (searched /root/fruits, /root/contracts, memory).
- `longrun-2026-11-15/STATE.md` of the long-run directory itself, if it ever existed, was not present; the operational STATE is included.
- Model provenance per proof-book entry is sparse: 79 of 94 entries carry no `model` field; the rest name laguna-xs-2.1, qwen2.5-vl-72b,
  muse-glimmer-30b, qwen3.5-9b, llama-3.3-70b, claude-haiku-5-5, qwen3.5-397b.
- A second ledger in the same directory (`research-d37bfe30e8be.jsonl`, 73 entries) is a Collatz research question, not RH; excluded.
- Missions whose record mentions Riemann only incidentally may be included (mention counts 1-5: 390455a0, 808720dd, c4113820, a5f515a3,
  608cd391, b81f490a, 59d57c8d, a6edee0e); kept rather than guessed away.
