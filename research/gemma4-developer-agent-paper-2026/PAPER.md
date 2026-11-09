# Selective Evidence Reactivation for Offline Coding Agents

## Graph-Seeded Localization and Event-Triggered Revisiting of Abandoned Hypotheses with Gemma 4

**Kaggle Gemma 4 Developer Agent Paper Track — research writeup**
**Version:** 0.2, ⟦TBD: date of final submission⟧
**Model:** `⟦TBD: gemma-4-31b-it-qat-w4a16-ct | gemma-4-e4b-it-qat-w4a16-ct⟧`, run offline on Kaggle L4×4 with internet disabled
**Code and data:** ⟦TBD: public repository URL⟧ (Apache-2.0) · Preregistration commit: `⟦TBD: SHA⟧`

### Abstract

Coding agents that run offline on a small open model have little room for wasted steps. Two failure modes are especially costly: they look in the wrong place first, and they keep patching the wrong place after the evidence has turned against it. We study one mechanism that addresses both, **Selective Evidence Reactivation (SER)**. First, a localization prior ranks repository symbols by fusing lexical and dense retrieval with Personalized PageRank (PPR) over the competition's code graph. Gemma 4 acts as a recognition filter that removes irrelevant seed symbols before propagation. Second, during repair, the agent keeps a ledger of localization hypotheses and the checkable assumptions behind them. When an executed test refutes such an assumption, a deterministic trigger marks the current hypothesis as refuted and reactivates a small, eligible set of previously ranked but abandoned candidates. We test three preregistered hypotheses on the competition's development tasks. H3 asks whether graph propagation improves localization recall. H1 asks whether event-triggered reactivation improves verified repair over an identical retrieval policy without the trigger. H2 asks whether this selective disclosure matches or beats a full-history agent under the same budget. ⟦TBD: one sentence per hypothesis with effect size and 95% CI, including null results.⟧

### 1. Introduction

The competition asks for an agent that repairs real Python defects on everyday hardware without network access. Under these constraints the agent's first localization decision matters more than usual. A wrong first location costs turns, and small models tend to stay with it. We call this *premature local closure*: the agent keeps editing the first plausible location even after a test run has shown that edits there do not change the failure.

Retrieval alone does not solve this. A retriever can rank the right symbol fifth, but the agent abandons rank five once it commits to rank one, and nothing brings it back. Showing the agent its entire history does not solve it either. Long histories of a failed approach compete for attention with the evidence that it failed.

We therefore separate two questions. *Where should the agent look first?* That is a ranking problem over the code graph. *When should it look again?* That is a triggering problem: a verified event, not the model's own judgment, decides when an abandoned candidate becomes relevant. SER answers both with one shared candidate ranking, so the mechanism can be ablated part by part.

**Hypotheses (preregistered, commit `⟦TBD⟧`):**

- **H3 — Structural localization.** Adding seeded PPR over the code graph to hybrid lexical–dense retrieval increases symbol-level Recall@10 of gold-patch locations. Adding a Gemma 4 recognition filter on the seeds increases it further. Neither addition lowers recall on tasks where the gold symbol is directly retrievable (non-inferiority margin: 2 percentage points).
- **H1 — Coupling.** Event-triggered reactivation (arm E) resolves more tasks than the same agent receiving the same number of retrieved candidates at the same checkpoints without the trigger (arm E⁻).
- **H2 — Selective disclosure.** Arm E resolves at least as many tasks as a full-history agent (arm D*) under the same turn, token and time budget.

These are hypotheses about one mechanism under one set of conditions. We do not claim novelty for graphs, PageRank, retrieval or agent memory individually.

### 2. Related work

**Agents and localization.** SWE-bench [9] established repository-level issue resolution with execution-based grading. SWE-agent [10] showed that the agent–computer interface strongly affects outcomes. Agentless [11] showed that a fixed localize–repair–validate pipeline is a strong baseline. Several systems use code structure explicitly. RepoGraph [12] builds a line-level repository graph and retrieves ego-subgraphs. LocAgent [13] parses codebases into directed heterogeneous graphs of files, classes and functions with import, invocation and inheritance edges, and lets an agent navigate them with tools. OrcaLoca [14] schedules and prunes localization actions by priority and distance. PageRank has also been used in classical fault localization, where it re-weights spectrum-based suspiciousness scores [15].

**Graph memory.** HippoRAG [2] and HippoRAG 2 [3] combine LLM-based recognition of query entities with PPR over a knowledge graph for associative retrieval. GraphRAG [1] and LightRAG [4] organize retrieval around graph structure. G-Memory [5] and ReasoningBank [6] store experience across tasks. For coding agents, subtask-level memory improves on episode-level memory [7], while episodic memory can also inject noise [8].

**Gap.** Code-graph localization work treats localization as a one-shot ranking or as free agent navigation. Memory work concerns reuse *across* tasks. We study a narrower link: a verified, in-episode test outcome deterministically decides when a *previously ranked but abandoned* candidate re-enters the agent's context. We compare it against an identical policy that has the same candidates and checkpoints but no trigger. We also adapt the HippoRAG recognition-then-propagate pattern to code graphs and measure it there. Our retrieval core builds on HippoRAG 2 [3]; it is not a new version of it.

### 3. Method

#### 3.1 Inputs

For each task the competition provides an issue description, a repository snapshot, a directed code graph of symbols and their relationships, and 256-dimensional code embeddings [16]. ⟦TBD: confirm node and edge types from the data card, e.g. module, class, function; contains, calls, imports, inherits.⟧ A symbol node carries its file, name, signature and source span.

#### 3.2 Localization prior (H3)

All arms use the same candidate set and the same cutoffs. Only the ranking function differs.

**Arm A, hybrid retrieval.** BM25 over symbol text (qualified name, signature, docstring, body) with the issue text as query, fused with dense cosine similarity by reciprocal rank fusion (RRF, k = 60). ⟦TBD: if the competition does not ship the encoder for query embeddings, the dense component is removed from all arms equally, and this is reported.⟧

**Seeds.** The top m = 10 symbols from arm A, plus every symbol whose name appears verbatim in the issue text or in a traceback it contains.

**Arm B, + PPR.** We solve

p = (1 − α) s + α Pᵀ p,

where s is uniform over the seeds and P is the row-normalized transition matrix over **content edges only**: containment, calls, imports and inheritance, symmetrized. α = 0.5 is fixed in advance. Nothing derived from usage, popularity or agent behaviour ever becomes an edge. The final score fuses the arm-A rank and the PPR rank by RRF. A *direct-retrieval safety path* keeps arm A's top 3 symbols in the output regardless of their PPR score, so a highly central node cannot displace the strongest direct hit.

**Arm C, + Gemma recognition filter.** Before propagation, Gemma 4 receives the issue and the seed list (qualified name and signature only, no bodies) and returns the subset it judges relevant to the issue. It can only *remove* seeds, never add symbols, so the filter cannot inject knowledge about the repository from outside the graph. If it removes all seeds, the unfiltered seeds are used and the event is logged. The prompt is frozen at the preregistration commit.

#### 3.3 Episode ledger and verified events (H1, H2)

The agent follows one fixed loop in all arms: localize, reproduce, patch, run tests, repair. It has the same tool set and the same turn, token and wall-clock limits everywhere. In arms E and E⁻ the harness, not the model, keeps a ledger.

A **hypothesis** is h = (symbol, status, assumptions). Its status is ACTIVE, ABANDONED, REFUTED_UNDER_ASSUMPTIONS or REVIEW_REQUIRED. Each hypothesis carries only assumptions that the harness can check mechanically:

- *reproduces*: the agent's reproduction script fails on the unpatched snapshot;
- *fault-at-symbol*: editing the hypothesis symbol changes the outcome of the reproduction or of the targeted test;
- *trace-locality*: the frames of the current failure lie within two graph hops of the hypothesis symbol.

**Verified events** come only from executed tool results, never from model statements:

| Event | Definition |
|---|---|
| PATCH_NO_EFFECT | after an edit confined to the active symbol, the reproduction outcome and the failing test outcome are unchanged |
| TRACE_SHIFT | the failure's traceback no longer satisfies trace-locality for the active symbol |
| REGRESSION(t) | a previously passing test t now fails |
| REPRO_RESOLVED | the reproduction passes and the targeted tests pass |

#### 3.4 Event-triggered reactivation (arm E)

The trigger fires only when **all** of these hold:

1. A verified event contradicts an assumption of the ACTIVE hypothesis (PATCH_NO_EFFECT contradicts *fault-at-symbol*; TRACE_SHIFT contradicts *trace-locality*).
2. At least one *eligible* candidate exists. A candidate is eligible if it appeared in the episode's initial localization ranking or in a PPR re-ranking seeded with the new traceback frames, if it is not itself REFUTED_UNDER_ASSUMPTIONS under the current assumptions, and if it has not already been reactivated in this episode.

When the trigger fires, the active hypothesis becomes REFUTED_UNDER_ASSUMPTIONS, together with the event that refuted it. The agent then receives a fixed-format **evidence packet** of at most 3 eligible candidates (symbol, file, signature, why it was ranked) plus one **historical contrast** line, for example: "edits to `X.parse` did not change failure F". The contrast is a warning, not a verdict. The agent remains free to return to `X.parse`, and the harness does not force a switch. Null cases must not fire the trigger: an unchanged outcome after an edit *outside* the active symbol, an unverified claim by the model, or the absence of eligible candidates. These invariants are unit-tested; passing them is an implementation check, not evidence of benefit.

#### 3.5 Control arms

- **E⁻ (no coupling).** The ledger, the candidate pool, the packet format, the packet size and the checkpoints (after every test execution) are identical to E. The packet is filled with the top 3 candidates retrieved for the agent's current subgoal text, without event detection, refutation marking or historical contrast.
- **D\* (full history).** No ledger and no packet. The agent sees its complete raw history. If the history exceeds the context limit, a frozen rule keeps the issue, the first localization step and the most recent turns. E and E⁻ instead see a compacted history (the issue, the ledger and the most recent turns) plus the packet, under the same total token cap.

E versus E⁻ isolates the trigger. E versus D\* tests selective disclosure against full disclosure.

### 4. Experimental protocol

**Tasks.** ⟦TBD: n⟧ development tasks from the competition data, in a fixed order. ⟦TBD: k⟧ tasks were used for a timing pilot and are excluded from all reported results. Pilot outcomes were not inspected beyond wall time and harness errors.

**Gold locations (H3).** The symbols and files whose source spans intersect the hunks of the reference patch, mapped on the pre-patch snapshot. Reference patches are used **only** for H3 scoring and are never visible to any arm.

**Outcome (H1, H2).** A task is resolved when the final patch applies cleanly and the hidden validation tests pass. Grading runs outside the agent process. Timeouts, crashes and empty patches count as unresolved, and are reported by failure class.

**Analysis.** All comparisons are paired per task.
- H3: primary endpoint is symbol Recall@10, B versus A, then C versus B, by Wilcoxon signed-rank test with a paired bootstrap 95% CI. Non-inferiority is evaluated on the *direct* subset, defined as tasks where arm A already ranks a gold symbol within its top 10.
- H1: exact McNemar test on resolved status, E versus E⁻, two-sided α = 0.05.
- H2: E versus D\*, exact McNemar test with Holm correction across H1 and H2.
- Secondary: file Recall@{1, 5}; persistence, defined as the number of further edits to a symbol after PATCH_NO_EFFECT on it; repeated refuted approaches; turns, tokens and wall time per task.

**Power.** With ⟦TBD: n⟧ paired tasks, McNemar's test detects only large asymmetries in discordant pairs. ⟦TBD: minimum detectable discordance from the pilot.⟧ We therefore report effect estimates with confidence intervals, not only p-values. An underpowered null is reported as inconclusive, not as evidence of no effect.

**Leakage controls.** All arms start from the same frozen snapshot. No arm sees reference patches, hidden tests or outcomes of other arms. The model, quantization, decoding parameters, tool set and grader revision are identical across arms and recorded with the preregistration commit.

### 5. Results

#### 5.1 H3 — Localization prior

| Arm | Symbol R@10 | File R@1 | File R@5 | Direct subset R@10 |
|---|---|---|---|---|
| A hybrid | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |
| B + PPR | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |
| C + Gemma filter | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |

Paired differences: B − A = ⟦TBD⟧ (95% CI ⟦TBD⟧); C − B = ⟦TBD⟧ (95% CI ⟦TBD⟧). Seeds removed by the filter: median ⟦TBD⟧; fallback to unfiltered seeds in ⟦TBD⟧ tasks.

#### 5.2 H1 and H2 — Repair

| Arm | Resolved / n | Median turns | Median tokens | Median wall time |
|---|---|---|---|---|
| D\* full history | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |
| E⁻ no coupling | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |
| E reactivation | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |

Discordant pairs: E-only ⟦TBD⟧, E⁻-only ⟦TBD⟧ (McNemar p = ⟦TBD⟧). E-only ⟦TBD⟧, D\*-only ⟦TBD⟧ (Holm-adjusted p = ⟦TBD⟧). The trigger fired in ⟦TBD⟧ of ⟦TBD⟧ E episodes. Persistence after PATCH_NO_EFFECT: E ⟦TBD⟧, E⁻ ⟦TBD⟧, D\* ⟦TBD⟧.

#### 5.3 Failure analysis

⟦TBD: 3–5 short, concrete cases: one where reactivation recovered the gold symbol, one where it distracted the agent, one where the trigger never fired because no eligible candidate existed.⟧

### 6. Discussion and limitations

⟦TBD: interpretation tied strictly to the numbers in Section 5.⟧

**Scope.** All results come from one model, one harness and one set of development tasks from Python repositories. They do not establish transfer to other languages, models or task distributions.

**Trigger coverage.** The trigger can only help when the gold symbol is already in the candidate pool. H3 therefore bounds H1, and we report how often the pool contained a gold symbol at the time of triggering.

**Event validity.** PATCH_NO_EFFECT can misfire when the active symbol is correct but the edit is wrong. We report how often a refuted symbol was in fact a gold symbol.

**Filter risk.** The Gemma recognition filter can remove the correct seed. The safety path limits, but does not eliminate, this risk.

**Cross-task memory.** The broader idea, reactivating evidence from *other* tasks when a verified assumption changes, needs task families with controlled assumption changes. It is outside the scope of this study.

### 7. Reproducibility

The repository contains the harness, the frozen prompts, the preregistration file, per-episode JSONL traces (prompts, responses, tool results, events, ledger states, packets) and the Kaggle notebooks that produced every number in Section 5. A single command regenerates all tables from the traces. ⟦TBD: notebook links, hardware, wall-clock totals.⟧

### 8. Conclusion

SER proposes that a coding agent does not need *more* of its own history, but the right abandoned option at the moment a test shows that the current one is wrong. ⟦TBD: one-sentence verdict per hypothesis, stated exactly as measured.⟧

### References

[1] Edge et al. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. arXiv:2404.16130.
[2] Gutiérrez et al. (2024). HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. NeurIPS 2024.
[3] Gutiérrez et al. (2025). From RAG to Memory: Non-Parametric Continual Learning for Large Language Models (HippoRAG 2). ICML 2025.
[4] Guo et al. (2025). LightRAG: Simple and Fast Retrieval-Augmented Generation. Findings of EMNLP 2025.
[5] Zhang et al. (2025). G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems. NeurIPS 2025.
[6] Ouyang et al. (2026). ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory. ICLR 2026.
[7] Shen et al. (2026). Structurally Aligned Subtask-Level Memory for Software Engineering Agents. ICML 2026. arXiv:2602.21611.
[8] Lindenbauer et al. (2025). From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents. REALM Workshop 2025.
[9] Jimenez et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR 2024.
[10] Yang et al. (2024). SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS 2024. arXiv:2405.15793.
[11] Xia et al. (2024). Agentless: Demystifying LLM-based Software Engineering Agents. arXiv:2407.01489.
[12] Ouyang et al. (2025). RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph. ICLR 2025. arXiv:2410.14684.
[13] Chen et al. (2025). LocAgent: Graph-Guided LLM Agents for Code Localization. ACL 2025. arXiv:2503.09089.
[14] Yu et al. (2025). OrcaLoca: An LLM Agent Framework for Software Issue Localization. ICML 2025. arXiv:2502.00350.
[15] Zhang et al. (2017). Boosting Spectrum-Based Fault Localization Using PageRank. ISSTA 2017.
[16] Google DeepMind (2026). Gemma 4 Developer Agent Competition: dataset description. Kaggle.