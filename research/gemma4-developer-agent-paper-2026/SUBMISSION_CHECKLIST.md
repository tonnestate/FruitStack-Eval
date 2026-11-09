# Submission checklist — not part of the Kaggle writeup

Deadline: Thu 2026-11-12 23:59 UTC (Fri 00:59 German time). Target: final submit Thu 22:00 German time.

## Before the first run (preregistration commit)
- [ ] Join both Kaggle competitions; accept rules; check eligibility clause and employee clause.
- [ ] Confirm node/edge types in `graphs/` and whether a query encoder for `embeddings/` is shipped (PAPER §3.1, §3.2 arm A).
- [ ] Freeze: alpha = 0.5, m = 10 seeds, RRF k = 60, safety path top 3, packet size 3, prompts, model ID, decoding params, turn/token/time caps.
- [ ] Commit the preregistration file and record the SHA in PAPER header and §1.
- [ ] Timing pilot on k tasks; then fix n and the task order; pilot tasks excluded.

## Results to fill (grep for ⟦TBD)
- [ ] Abstract: one sentence per hypothesis with effect + 95% CI.
- [ ] §5.1 H3 table and paired differences.
- [ ] §5.2 repair table, discordant pairs, trigger rate, persistence.
- [ ] §5.3 failure cases, §6 interpretation, §8 verdicts.
- [ ] §7 notebook links, hardware, wall-clock totals.

## References to verify before submit
- [ ] [4] LightRAG venue (Findings of EMNLP 2025).
- [ ] [5] G-Memory venue (NeurIPS 2025).
- [ ] [8] CTIM-Rover venue (REALM 2025).
- [ ] [15] PageRank fault localization (Zhang et al., ISSTA 2017) — authors/title.
- Already checked online: [7] arXiv:2602.21611 (ICML 2026 poster), [12] RepoGraph ICLR 2025, [13] LocAgent arXiv:2503.09089, [14] OrcaLoca ICML 2025.

## Submission
- [ ] Word count of PAPER.md body ≤ 3,000 (tables and captions included, to be safe).
- [ ] Repo public, Apache-2.0, traces + notebooks included.
- [ ] Submit a first writeup Wednesday (unsubmitted drafts are ineligible); update Thursday.
