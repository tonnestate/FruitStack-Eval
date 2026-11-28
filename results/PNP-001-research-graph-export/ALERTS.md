# Research director alerts (newest last; generated, append-only source: desk/alerts.jsonl)

## 2026-11-28T14:24:36+0100  SESSION_FAILURES  `SESSION_FAILURES:REVIEW-2026112813`
- finding: lane REVIEW: 18 sessions in 6 h, 0 with FINAL
- significance: workers cannot close their work inside the turn limit
- affected: REVIEW
- proofbook ids: []
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: countdown nudge + continuation rule active; repeated heads are demoted by the lane sorter

## 2026-11-28T14:24:36+0100  STAGNATION  `STAGNATION:REVIEW-2026112813`
- finding: lane REVIEW: no proof step, verification, refutation or connection in 18 sessions (6 h)
- significance: lane output is approach descriptions / numerical records only
- affected: REVIEW
- proofbook ids: []
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: REVIEW share rebalanced; the lane's repeated heads are demoted

## 2026-11-28T14:24:36+0100  STAGNATION  `STAGNATION:COMPRESS-2026112813`
- finding: lane COMPRESS: no proof step, verification, refutation or connection in 18 sessions (6 h)
- significance: lane output is approach descriptions / numerical records only
- affected: COMPRESS
- proofbook ids: []
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: REVIEW share rebalanced; the lane's repeated heads are demoted

## 2026-11-28T14:24:38+0100  DISCOVERY  `DISCOVERY:18764`
- finding: Bingo COMPOSITION comp:koopman-hankel-bm-bostan-mori-cost-calculus: 
- significance: new constructed object / cross-project transfer
- affected: comp:koopman-hankel-bm-bostan-mori-cost-calculus
- proofbook ids: [18764]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:38+0100  DISCOVERY  `DISCOVERY:18765`
- finding: Bingo COMPOSITION comp:shear-decoupling-tower-x-hankel-rank-separation-x-t52-elimin: 
- significance: new constructed object / cross-project transfer
- affected: comp:shear-decoupling-tower-x-hankel-rank-separation-x-t52-elimin
- proofbook ids: [18765]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:38+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:18772`
- finding: RETRACTION recorded: Q-c7c02fd18c
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-c7c02fd18c
- proofbook ids: [18772]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director
