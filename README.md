# FruitStack-Eval: research results and evaluations

> **CURRENT STATUS:** The previous freeze order was withdrawn; operational freeze is NOT active or VPS-verified. This audit branch is a historical evidence snapshot. VPS_ACTIVATION.md is a conditional manual template only, not a standing instruction. No route priority is finalized. The actual VPS state has not been independently observed.


This repository publishes research results and the evaluations of an AI research organisation: proof books,
manuscripts, proofs, verifiers, evaluation reports and computed data. It contains no software of the organisation.

## PNP-001: open research notebook on P vs NP

PNP-001 publishes the **proof books, manuscripts, proofs and verifiers** of PNP-001, a research
programme led by Björn Tonn. The work is carried out by an organisation of AI research agents from
several model families. Every claim, check, refutation and retraction is written to an append-only,
hash-chained proof book. This repository is a public copy of those books and of the evidence behind them.

> **Status (22 November 2026): P ≠ NP is _not_ proved here.** The central result so far is
> *conditional*. Manuscript v0.25, Theorem 3, derives P ≠ NP from a lower-bound premise (8). By
> McKay–Murray–Williams (STOC 2019, Thm. 1.3), the weaker oracle-free uniform streaming premise (40a)
> would also suffice. **Both premises are open.** Unconditional results hold only in the restricted
> models and finite domains stated with each result.

## Start here

| What | Where |
|---|---|
| Current manuscript (v0.25) | [`PNP-001-UNIFIED-RESEARCH-SYNTHESIS-v0.25.md`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-22/papers/PNP-001-UNIFIED-RESEARCH-SYNTHESIS-v0.25.md) |
| Proof book, readable | [campaigns](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/beweisbuch/LESBAR-STAGING-kampagnen.md) · [live book](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/beweisbuch/LESBAR-LIVE-stand-heute.md) |
| Proof book, raw (JSON Lines, hash chain) | [`beweisbuch/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/beweisbuch/) (see its [README](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/beweisbuch/README.md) for the verdict states) |
| Proof state of each open question | [`qe-star/proofstate-live/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-22/qe-star/proofstate-live/) |
| Current proof attempt (QE\*) | [`qe-star/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-22/qe-star/) |
| Findings and failed runs | [discovery register](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/registers/DISCOVERY-REGISTER.md) · [failed runs](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/registers/FAILED-RUNS-REGISTER.md) |
| Lean 4 formalisation | [`lean/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-19/lean/) |
| Research contracts and specifications | [11-21](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-21/specifications/) · [11-22](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-22/specifications/) |

## Evaluations

Each evaluation stays on its own branch, under the branch name the papers cite. Every branch keeps its reports and computed data.

| Evaluation | Start here |
|---|---|
| OGI-013: independently evaluated adaptive organisation | [`OGI013_EVALUATION.md`](https://github.com/tonnestate/FruitStack-Eval/blob/fsi/ogi013-final/OGI013_EVALUATION.md) · [collaboration results](https://github.com/tonnestate/FruitStack-Eval/blob/ogi013-collab-proof/evidence/ogi013-lead/RESULTS.md) |
| Superiority evidence (2026-11-14) | [synthesis report](https://github.com/tonnestate/FruitStack-Eval/blob/cc/superiority-evidence-2026-11-14/evidence/20261114-SUPERIORITY-SYNTHESIS/REPORT.md) |
| Riemann-hypothesis research archive (2026-11-20) | [archive index](https://github.com/tonnestate/FruitStack-Eval/blob/cc/rh-evidence-archive-20261120/evidence/rh-research-archive-2026-11-20/INDEX.md) |
| Developer-agent paper (Gemma 4, 2026-11-09) | [paper](https://github.com/tonnestate/FruitStack-Eval/blob/research/gemma4-paper-20261109/research/gemma4-developer-agent-paper-2026/PAPER.md) |
| Pilot F1/F3 (2026-10-14) | [pilot protocol](https://github.com/tonnestate/FruitStack-Eval/blob/main/PILOT_PROTOCOL.md) · [report](https://github.com/tonnestate/FruitStack-Eval/blob/main/evidence/20261014T023511Z-DEV-F1DEV-F3DEV/REPORT.md) |
| OGI-011 route arms (2026-10-12) | [branch `cc/ogi-011`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/ogi-011) |

All branches: [branch list](https://github.com/tonnestate/FruitStack-Eval/branches/all).

## Verifiers

The scripts that recompute the finite results are stored next to the results they check:

- [`F16/verifier.py`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-19/F16/verifier.py): exact verification of the degree-3 Nullstellensatz certificate
- [`2026-11-19/scripts/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-19/scripts/): enumerations, rank and degree computations
- [`2026-11-20/completeness-n10/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-20/completeness-n10/): independent C re-implementation of the n ≤ 10 enumeration
- [`2026-11-20/acc0-level3/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-20/acc0-level3/) and [`mg3/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-20/mg3/): ACC0 and matchgate checks
- [`2026-11-21/checks/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-21/checks/): rank, cut-rank and refutation checks
- [`2026-11-18/lab/`](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/lab/): exact circuit sizes, Gal matrices, matroid-port checks

## How results are accepted

1. A claim enters the proof book as a **CLAIMED** step together with its evidence.
2. Finite statements are recomputed independently, and the result is recorded as `FINITE_CONFIRMED`.
3. A step counts as **proved** only after an adversarial review in a *different session by a
   different model family*, recorded as `SURVIVED_REVIEW` or `REFUTED`. Formal parts must also be
   accepted by the Lean kernel (`FORMALLY_VERIFIED`).
4. Nothing is deleted. A refuted or retracted entry stays in the book, and failed runs are listed in the
   failed-runs register.

Each proof-book entry carries `prev` and `hash`, so later edits to the book are detectable.

## Daily notes

[2026-11-18](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/README.md) ·
[2026-11-19](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-19/README.md) ·
[2026-11-20](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-20/README.md) ·
[earlier manuscripts](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-22/papers/)
