# Selective Evidence Reactivation for Autonomous Software Engineering

## Graph-Seeded Localization and Event-Triggered Revisiting of Abandoned Hypotheses

**Kaggle Gemma 4 Developer Agent Paper Track — research writeup**
**Version:** 0.2, ⟦TBD: date of final submission⟧
**Research system:** FruitStack, a multi-model agent stack; a budget-aware router chooses the model for every step among authorized free, trial-credit and included-subscription routes (no cash-billed routes); the participating models are logged and reported.
**Code and data:** ⟦TBD: public repository URL⟧ (Apache-2.0) · Preregistration commit (H3): `b6131d3`

### Abstract

Coding agents under step budgets fail in two costly ways: they look in the wrong place first, and they keep patching it after the evidence has turned against it. We study one mechanism aimed at both, **Selective Evidence Reactivation (SER)**. A localization prior ranks repository symbols by fusing BM25 retrieval with Personalized PageRank (PPR) over the code graph, optionally after a language-model recognition filter on the seeds. During repair, the harness keeps a ledger of the symbol the agent is editing; when an executed check refutes it, a deterministic trigger marks it refuted and shows a small packet of previously ranked, abandoned candidates. We test three preregistered hypotheses on SWE-bench Verified with a multi-model agent whose models are chosen per step by a router. ⟦F: abstract results⟧

### 1. Introduction

Repository-level repair agents work under budgets, so the first localization decision matters: a wrong first location costs turns, and agents tend to stay with it even after a test run shows that edits there do not change the failure. Retrieval alone does not fix this — the agent abandons rank five once it commits to rank one — and showing the full history does not either, because a long failed approach competes for attention with the evidence that it failed.

We separate two questions. *Where should the agent look first?* is a ranking problem over the code graph. *When should it look again?* is a triggering problem: a verified event, not the model's judgment, decides when an abandoned candidate becomes relevant. SER answers both with one shared candidate ranking, so its parts can be ablated separately.

**Hypotheses (preregistered; H3 commit `b6131d3`, H1/H2 commit `de415c0`):**

- **H3 — Structural localization.** Seeded PPR over the code graph increases symbol Recall@10 over lexical retrieval; a recognition filter on the seeds increases it further; neither lowers recall where the gold symbol is directly retrievable (margin 2 points).
- **H1 — Coupling.** Event-triggered reactivation (E) resolves more tasks than the same agent receiving the same number of candidates at the same checkpoints without the trigger (E⁻).
- **H2 — Selective disclosure.** E resolves at least as many tasks as a full-history agent (D\*) under the same wall-clock budget.

We claim no novelty for graphs, PageRank, retrieval or agent memory individually.

### 2. Related work

**Agents and localization.** SWE-bench [9] established repository-level issue resolution with execution-based grading; SWE-agent [10] showed the weight of the agent–computer interface; Agentless [11] is a strong fixed localize–repair–validate baseline. RepoGraph [12], LocAgent [13] and OrcaLoca [14] use code graphs for retrieval, agent navigation and action scheduling. PageRank has re-weighted suspiciousness scores in classical fault localization [15].

**Graph memory.** HippoRAG [2, 3] combines LLM recognition of query entities with PPR over a knowledge graph; GraphRAG [1] and LightRAG [4] organize retrieval around graphs. G-Memory [5] and ReasoningBank [6] store experience across tasks; for coding agents, subtask-level memory helps [7] while episodic memory can inject noise [8].

**Gap.** Code-graph work treats localization as one-shot ranking or free navigation; memory work concerns reuse *across* tasks. We study a narrower link: a verified in-episode test outcome deterministically decides when a *previously ranked but abandoned* candidate re-enters the context, against an identical policy without the trigger. We also adapt HippoRAG's recognize-then-propagate pattern [3] to code graphs.

### 3. Method

#### 3.1 Inputs

The planned competition data (with 256-dimensional embeddings [16]) was not accessible on our execution host, so we use SWE-bench Verified [9] (500 instances). The graph is rebuilt per task at its base commit with Python's `ast`: nodes are functions, methods and classes (file, qualified name, signature, source span); edges are *contains* (lexical nesting) and *calls* (resolved in the same file first, else to a global name with at most three definitions; more ambiguous names stay unlinked).

#### 3.2 Localization prior (H3)

All arms share the candidate set and cutoffs; only the ranking differs.

**Arm A.** BM25 over symbol text (qualified name, signature, docstring, body) with the issue as query. The planned dense component was removed from all arms because no query encoder was available.

**Seeds.** Arm A's top 10, plus every symbol whose name appears verbatim in the issue or its traceback.

**Arm B, + PPR.** p = (1 − α) s + α Pᵀ p, with s uniform over the seeds, P the row-normalized, symmetrized transition matrix over content edges (contains, calls) and α = 0.5 fixed in advance. The final score fuses arm-A and PPR ranks by reciprocal rank fusion (k = 60); arm A's top 3 always stay in the top 10, so a central node cannot displace the strongest direct hit.

**Arm C, + LLM recognition filter.** Before propagation, a model chosen per call by the router sees the issue and the seed list (names and signatures only) and returns the relevant subset. It can only remove seeds; if it removes all, or its answer cannot be parsed, the unfiltered seeds are used and logged. The prompt is frozen.

#### 3.3 Episode ledger and verified events (H1, H2)

In every arm the harness, not the model, maps each edit to the innermost symbol it touches and records it in a ledger; the symbol edited most recently is the *active hypothesis*. A *checkpoint* is every executed test or script run. Events are computed only from executed tool results:

| Event | Definition |
|---|---|
| PATCH_NO_EFFECT | the same check, re-run after edits confined to the active symbol, fails with an unchanged signature (exit code and failing tests) |
| TRACE_SHIFT | the failure's traceback frames, previously within two graph hops of the active symbol, no longer are |

#### 3.4 Event-triggered reactivation (arm E)

The trigger fires when an event concerns an ACTIVE hypothesis and at least one *eligible* candidate exists: a symbol in the pool (reciprocal-rank fusion of arm B's top 20 and a PPR ranking seeded with the current traceback frames) that is not the active symbol, not refuted and not shown before in this episode. The active hypothesis is then marked REFUTED_UNDER_ASSUMPTIONS, and the next tool result is prefixed with an **evidence packet** of 3 candidates (name, file, line span, signature) and one **historical contrast** line ("edits to `X` did not change the outcome of this check"). The contrast is a warning, not a verdict; the agent may return to `X`.

#### 3.5 Control arms

- **E⁻ (no coupling).** Same ledger, pool, packet format and size, at every checkpoint; the packet holds the 3 pool candidates that best match the current failure output (BM25), with no event detection, refutation or contrast.
- **D\* (full history).** No packet; the agent sees its complete raw history, truncated above 120k characters by a frozen rule (first 4 entries plus the most recent that fit). E and E⁻ see the runner's default rendered history plus the packet.

E versus E⁻ isolates the trigger; E versus D\* tests selective against full disclosure.

### 4. Experimental protocol

**Tasks.** H3: 497 SWE-bench Verified instances, drawn deterministically and stratified by repository (manifest in the preregistration); 3 pilot instances are excluded (their recall values were seen during the pilot; disclosed). H1/H2: the Django tasks of the same manifest, in order, whose grader calibration is valid (the base snapshot fails and the reference patch resolves; 130 of 206), started until the preregistered time cutoff. Gold locations for H3 are the symbols and files whose spans intersect the reference patch hunks; reference patches are used only for scoring.

**Outcome (H1, H2).** Resolved when the hidden fail-to-pass and pass-to-pass tests pass on the final workspace, graded outside the agent process; timeouts, crashes and empty patches count as unresolved.

**Execution system (H1, H2).** Every arm runs the same multi-model organisation: an author, an independent critic on a read-only copy that runs tests (only after the author submits), and a reviser. A budget-aware router picks the model of every step from authorized free, trial-credit and included-subscription supply. All arms share tools, the initial top-10 list from arm B and a 3,600 s wall-clock limit; ledger and packets apply only to the editing roles. The three arms of a task run concurrently and so share supply conditions, but not models; the per-arm model distribution is reported. Amendments are listed in Section 7.

**Analysis.** All comparisons are paired per task.
- H3: primary endpoint is symbol Recall@10, B versus A, then C versus B, by Wilcoxon signed-rank test with a paired bootstrap 95% CI. Non-inferiority is evaluated on the *direct* subset, defined as tasks where arm A already ranks a gold symbol within its top 10.
- H1: exact McNemar test on resolved status, E versus E⁻, two-sided α = 0.05.
- H2: E versus D\*, exact McNemar test with Holm correction across H1 and H2.
- Secondary: file Recall@{1, 5}; persistence, defined as the number of further edits to a symbol after PATCH_NO_EFFECT on it; repeated refuted approaches; turns, tokens and wall time per task.

**Power.** H1/H2 sample size is fixed by the time cutoff, not by power. With few discordant pairs McNemar's test detects only large asymmetries, so we report risk differences with bootstrap 95% CIs, and an underpowered null as inconclusive, not as no effect.

**Leakage controls.** All arms start from the same frozen snapshot. No arm sees reference patches, hidden tests or outcomes of other arms. Tool set, runner, organisation mode, wall-clock limit and grader revision are identical across arms; models are chosen per step by the router and logged per step (Section 6).

### 5. Results

#### 5.1 H3 — Localization prior

| Arm | Symbol R@10 | File R@1 | File R@5 | Direct subset R@10 |
|---|---|---|---|---|
| A hybrid (BM25) | 0.386 | 0.292 | 0.614 | 0.826 |
| B + PPR | 0.401 | 0.297 | 0.635 | 0.831 |
| C + LLM filter | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |

Rows A and B: 497 confirmatory tasks (478 with a gold symbol for symbol recall; direct subset n = 223). Paired differences: B − A symbol Recall@10 = +0.016 (95% CI +0.007 to +0.026; Wilcoxon p = 6.0 × 10⁻⁴; B better on 15 tasks, worse on none). B found a gold symbol in its top 10 that A missed on 9 tasks. On the direct subset, B − A = +0.005 (95% CI +0.001 to +0.010), so B is non-inferior at the preregistered margin of −0.02. File Recall@5: +0.021 (95% CI +0.002 to +0.042); file Recall@1: +0.005 (95% CI −0.029 to +0.040). Scoring all 497 tasks for A and B took 54 min on 8 CPU cores, with no GPU. C − B = ⟦TBD⟧ (95% CI ⟦TBD⟧). Seeds removed by the filter: median ⟦TBD⟧; fallback to unfiltered seeds in ⟦TBD⟧ tasks.

#### 5.2 H1 and H2 — Repair

| Arm | Resolved / n | Median turns | Median tokens | Median wall time |
|---|---|---|---|---|
| D\* full history | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |
| E⁻ no coupling | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |
| E reactivation | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ | ⟦TBD⟧ |

Discordant pairs: E-only ⟦TBD⟧, E⁻-only ⟦TBD⟧ (McNemar p = ⟦TBD⟧). E-only ⟦TBD⟧, D\*-only ⟦TBD⟧ (Holm-adjusted p = ⟦TBD⟧). The trigger fired in ⟦TBD⟧ of ⟦TBD⟧ E episodes. Persistence after PATCH_NO_EFFECT: E ⟦TBD⟧, E⁻ ⟦TBD⟧, D\* ⟦TBD⟧.

#### 5.3 Failure analysis

*Wrong trigger, ignored packet (django-11848).* E edited the correct function (`parse_http_date`); a re-run of the same test module failed unchanged, PATCH_NO_EFFECT fired and the gold symbol was marked refuted. The agent ignored the packet, edited the same function twice more and still did not pass; the episode stopped on no progress. E⁻'s first edit to that function passed the visible tests and resolved the task. The arms differ in edit quality and model mix (E mostly qwen3.5-397b and llama-3.3-70b, E⁻ mostly laguna-xs-2.1), not in where they looked. An unchanged test signal refutes the *edit*, not the *location*.

*No useful candidate (django-14155).* The trigger fired correctly (the edited symbol was not gold), but no gold symbol was in the candidate pool, so reactivation could only offer wrong alternatives. H3 recall bounds H1 exactly here.

*Silent episodes.* In ⟦F: 28 of 30⟧ E episodes no event fired: the agents rarely produced the pattern the trigger needs (repeated edits to one symbol, then the same check with an unchanged result). Most episodes ended by the runner's existing no-progress guard after few checkpoints, so E behaved like a no-packet baseline.

*History helps the critic stage (django-11292).* D\* submitted a patch, the independent critic found one issue, and the reviser's revision was rejected for no progress; the frozen workspace still passed the grader. The patch adds the requested `--skip-checks` option but also changes `requires_system_checks` and duplicates an option entry — resolved by the tests, yet not a patch a reviewer would accept as is. Resolved status measures test behaviour, not patch quality.

*Resolution without submission.* Several resolved episodes (e.g. E on django-11880) never submitted a patch; the grader scores the final workspace as preregistered. Submission and resolution are therefore reported separately (Table 2, P0 column in the evidence summary).

### 6. Discussion and limitations

**Localization.** Graph propagation gives a small, consistent gain over lexical retrieval: +1.6 points of symbol recall, never worse on any task, at negligible cost. ⟦F: C sentence⟧

**Reactivation.** H1 and H2 are inconclusive at ⟦F: n = 30⟧: discordant pairs are few and both risk differences have confidence intervals that include zero. The dominant reason is coverage, not effect: the trigger fired in ⟦F: 2⟧ episodes, and in one of them it refuted the correct symbol. Under this runner the agent's own loop (and the no-progress guard) ends episodes before the repeated-edit pattern forms. A study of SER's mechanism needs either longer episodes or a trigger on a weaker signal; we did not change the trigger after seeing these runs.

**Model mix and resources.** ⟦F: 17⟧ models served steps; they were chosen per step by the router, not by arm, and arms of a task ran concurrently. Differences between arms therefore mix SER with model assignment and should not be attributed to SER alone. D\* used about twice the tokens of E and E⁻ (median ⟦F: 208k vs 109k and 102k⟧) and submitted a patch to the critic more often (⟦F: 11 vs 5 and 6⟧ of 30), consistent with full history, rather than the packet, driving its resolution count; the design cannot separate this from the extra tokens.

**Scope.** All results come from one harness, one router-chosen pool of authorized free, trial-credit and included-subscription models and Python repositories (H3: 12 repositories; H1/H2: Django only, because our Docker-free grader supports Django). Model choice is not controlled within a task pair; arms of a task run concurrently, so they share the same supply conditions, but a per-pair model mismatch adds noise. The results do not establish transfer to other languages, models or task distributions.

**Trigger coverage.** The trigger can only help when the gold symbol is already in the candidate pool. H3 therefore bounds H1, and we report how often the pool contained a gold symbol at the time of triggering.

**Event validity.** PATCH_NO_EFFECT can misfire when the active symbol is correct but the edit is wrong. We report how often a refuted symbol was in fact a gold symbol.

**Filter risk.** The recognition filter can remove the correct seed, and its model varies per call. The safety path limits, but does not eliminate, this risk.

**Cross-task memory.** The broader idea, reactivating evidence from *other* tasks when a verified assumption changes, needs task families with controlled assumption changes. It is outside the scope of this study.

### 7. Reproducibility

The repository contains the harness, frozen prompts, preregistration, per-episode traces (ledger, packets, events, per-step model and router receipt identifiers, grader output) and the scripts that produce every number in Section 5 (`h3_eval/`, `h1_eval/analyze_h1.py`). H3 arms A/B ran on 8 CPU cores without a GPU. Router internals and credentials are not part of the release.

**Deviations from the preregistration, all made before the affected outcomes were computed:** (A1/A3) arm C's filter model is chosen by the router instead of a fixed Gemma checkpoint; (A2) session ceilings copied from an earlier study (zero cost, 110 calls, 200k tokens) were removed, leaving only the wall-clock limit; (H1-A1) after 4 single-author episodes all arms were restarted in the author–critic–reviser mode, and those episodes are excluded; (A4) arm C's sample cutoff was moved to 2026-11-11 06:00 UTC for the submission timeline. Grader calibration was extended in manifest order to all eligible Django tasks before the campaign reached them. Pilot, aborted and exploratory runs are kept separately and excluded.

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