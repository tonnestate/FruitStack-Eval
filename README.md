# PNP-001: open research notebook on P vs NP

This repository publishes the **proof books, manuscripts, proofs and verifiers** of PNP-001, a research
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
| Current manuscript (v0.25) | [`PNP-001-UNIFIED-RESEARCH-SYNTHESIS-v0.25.md`](results/PNP-001-2026-11-22/papers/PNP-001-UNIFIED-RESEARCH-SYNTHESIS-v0.25.md) |
| Proof book, readable | [campaigns](results/PNP-001-2026-11-18/beweisbuch/LESBAR-STAGING-kampagnen.md) · [live book](results/PNP-001-2026-11-18/beweisbuch/LESBAR-LIVE-stand-heute.md) |
| Proof book, raw (JSON Lines, hash chain) | [`beweisbuch/`](results/PNP-001-2026-11-18/beweisbuch/) (see its [README](results/PNP-001-2026-11-18/beweisbuch/README.md) for the verdict states) |
| Proof state of each open question | [`qe-star/proofstate-live/`](results/PNP-001-2026-11-22/qe-star/proofstate-live/) |
| Current proof attempt (QE\*) | [`qe-star/`](results/PNP-001-2026-11-22/qe-star/) |
| Findings and failed runs | [discovery register](results/PNP-001-2026-11-18/registers/DISCOVERY-REGISTER.md) · [failed runs](results/PNP-001-2026-11-18/registers/FAILED-RUNS-REGISTER.md) |
| Lean 4 formalisation | [`lean/`](results/PNP-001-2026-11-19/lean/) |
| Research contracts and specifications | [11-21](results/PNP-001-2026-11-21/specifications/) · [11-22](results/PNP-001-2026-11-22/specifications/) |

## Verifiers

The scripts that recompute the finite results are stored next to the results they check:

- [`F16/verifier.py`](results/PNP-001-2026-11-19/F16/verifier.py): exact verification of the degree-3 Nullstellensatz certificate
- [`2026-11-19/scripts/`](results/PNP-001-2026-11-19/scripts/): enumerations, rank and degree computations
- [`2026-11-20/completeness-n10/`](results/PNP-001-2026-11-20/completeness-n10/): independent C re-implementation of the n ≤ 10 enumeration
- [`2026-11-20/acc0-level3/`](results/PNP-001-2026-11-20/acc0-level3/) and [`mg3/`](results/PNP-001-2026-11-20/mg3/): ACC0 and matchgate checks
- [`2026-11-21/checks/`](results/PNP-001-2026-11-21/checks/): rank, cut-rank and refutation checks
- [`2026-11-18/lab/`](results/PNP-001-2026-11-18/lab/): exact circuit sizes, Gal matrices, matroid-port checks

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

[2026-11-18](results/PNP-001-2026-11-18/README.md) ·
[2026-11-19](results/PNP-001-2026-11-19/README.md) ·
[2026-11-20](results/PNP-001-2026-11-20/README.md) ·
[earlier manuscripts](results/PNP-001-2026-11-22/papers/)

This repository holds research results only. The software of the research organisation is not part of it.
