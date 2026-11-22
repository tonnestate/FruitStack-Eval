# LUNA — EXECUTE, MEASURE, FINISH (Gemma 4 Paper v0.2)

**Operator instruction, 2026-11-09. Urgent. No babysitting, no further planning phase.**

## Outcome to deliver

Complete the existing scientific study described in `research/gemma4-developer-agent-paper-2026/PAPER.md` (v0.2) by executing its frozen, auditable experiments and replacing result placeholders with **real measured values**. The publicly described subject is Selective Evidence Reactivation (SER) for offline coding agents, not FruitStack as a product. Use the complete existing FruitStack infrastructure **internally as the research executor**, not as the subject or public brand of the paper. Do not rerun OGI-013 or substitute its results.

Research repository: `tonnestate/FruitStack-Eval`, existing PR #22, branch `research/gemma4-paper-20261109`. This file and the manuscript were synchronized to the branch on 9 November 2026. Synchronize your local checkout safely with this remote source, preserving any newer local edits; do not overwrite local findings.

**Paper deadline:** 2026-11-12 23:59 UTC; operational target 22:00 Europe/Berlin on November 12. We intend to enter **both** Gemma 4 competitions. The Coding Agent contest is a separate deliverable; do not sacrifice the Paper Track deadline for speculative platform work.

## Execute without waiting for operator approval at every stage

1. Read v0.2 `PAPER.md` and the existing submission checklist. Do **not** reset the scope to architectural assessment, platform verification, OGI-013, or a new manuscript. Count and track each `⟦TBD` placeholder.
2. Confirm official Kaggle rules, data access, model ID, agent/tool and submission constraints. Human-only account actions (join, accept rules, publication, final Kaggle submission) should be reported together once; do not block autonomous research on them. Do not make restricted changes without authorization.
3. Inspect only the runtime paths strictly needed to **execute the first task**: Gemma model availability, provided graph/embedding access, retrieval/agent entrypoints, validator and receipts. If something is missing, demonstrate the exact failure, make the smallest authorized correction and retry. Stop general audits.
4. Commit preregistration **before** inspecting confirmatory outcomes: alpha=0.5, ten seeds, RRF k=60, direct-retrieval top-three safeguard, evidence packet size three, model ID, prompt versions, decoding, budgets, task selection and order, independent grading, and planned statistics. Conduct a short timing-only pilot; exclude pilots from confirmatory outcomes.
5. **H3 now:** execute real localization tasks with A = hybrid retrieval, B = hybrid + PPR, C = hybrid + PPR + Gemma filter. Compute Recall@10, file recall, paired effects/intervals, false negatives and actual compute. Keep gold-patch spans outside all agent inputs. Save raw trace records and executable analysis, not just summaries.
6. **H1/H2 next:** run paired E versus E-minus and E versus D-star full coding-repair episodes on the same frozen tasks and executable independent tests. Track actual verified patch success, triggered reactivations, eligible candidates, wrong triggers, failure categories and resources. Use correct offline Gemma infrastructure for the competition agent; full internal FruitStack may conduct research but cannot be smuggled into Kaggle's offline submission.
7. Fill v0.2 results, abstract, statistical uncertainty, failure examples, discussion and hypothesis verdicts from real evidence. If inconclusive or negative, say so. Never fabricate, extrapolate, self-grade, borrow OGI data, or present an unperformed experiment as completed. Check every citation, word count <=3000, trace reproducibility, and Kaggle rules.
8. Push the integrated paper, preregistration, analysis code and non-sensitive evidence **to the existing branch and PR #22**. Preserve the existing draft; no new paper, unrelated PR chain, or unapproved public release/merge. Avoid inadvertently exposing proprietary source or secrets.
9. In parallel, preserve the separate Gemma 4 Coding Agent workstream and prepare a competition-compliant `submission.zip` with `agent.yaml` and only allowed models/tools, validated in the permitted offline environment. Prioritize Paper Track where time conflicts occur. Do not represent a leaderboard CSV as an experimental dataset.

## Autonomous operating rule

Do not ask for permission to run routine, bounded, authorized research experiments or to commit non-sensitive work to the established draft branch. Do not request the operator to select task sequences, dictate commands, or repeatedly debug tool integration. Make the best defensible choice under existing rules, execute it, document the decision and move to the next stage. Use independent verifiers, real receipts and hard spend/runtime limits. No unauthorized paid API spend, security bypasses, branch force pushes, public publication, Kaggle submission, or other irreversible actions.

If an unavoidable blocker requires operator-only action, send **one concise blocker report**: the exact failing command/receipt, actions already tried, the one required human action, and which independent activities continue. Never stop the entire project for a nonblocking uncertainty.

Provide a single concise final delivery report with: task count, H3 A/B/C observed outcomes, paired E/E-minus and E/D-star verified results (including confidence intervals or honest insufficiency), reproducibility command and artifact paths, PR commit, remaining TBDs, competition submission readiness and only essential owner actions.

**Success means completed experiments and an evidence-backed manuscript, not another architecture assessment, passing unit tests, or an elaborate plan. Begin real execution immediately.**
