# Selective Evidence Reactivation for Agentic Software Engineering

## Problem–Solution Coupling, Graph Retrieval, and Controlled Disclosure for Cross-Task Repair Knowledge

**Research manuscript — Kaggle Gemma 4 Developer Agent Paper Track**  
**Version:** 0.1 research draft, 9 November 2026  
**Scientific status:** Original, unpublished proposal with a specified experimental protocol. No confirmatory outcome is asserted in this version.

### Abstract

Autonomous software-engineering agents repeatedly encounter related failures, changed assumptions, unsuccessful repairs, and partially transferable solutions. Conventional retrieval can supply relevant text but does not necessarily recognize when a verified change to a problem constraint invalidates a previous repair or warrants revisiting an abandoned strategy. Conversely, indiscriminate disclosure of prior solutions can bias independent exploration. We propose **problem–solution-coupled evidence reactivation**: a versioned, provenance-aware experience graph whose typed links connect changed requirements, solution hypotheses, and evidence scoped to explicit assumptions. A deterministic trigger selects a small set of applicable or historically contrasting experiences; hybrid lexical–semantic retrieval and problem-seeded Personalized PageRank (PPR) provide complementary structural discovery. We separate scientific validity from retrieval ranking and distinguish verified, conditional, falsified, and unknown findings. The proposed study tests a coupled reactivation policy against an otherwise identical uncoupled retrieval policy, and tests selective disclosure against a matched-budget full-history control. The primary endpoint is independently verified successful repair of software defects, not memory retrieval accuracy, model self-assessment, token savings, or the performance of the research infrastructure itself. We specify data lineage, blinding, negative controls, analysis, and limitations. Empirical results remain to be collected.

### 1. Introduction

Coding agents can navigate repositories, edit files, and run tests, yet many executions begin without operational access to the evidence accumulated during prior, related tasks. A stored patch may solve a failure only under a particular dependency version, input contract, or concurrency invariant. A failed patch can also be informative: it may refute an approach under one assumption while remaining relevant after that assumption changes. Reusing such history therefore requires more than a nearest-neighbor match between issue descriptions.

The research question is:

> **Can verified changes in software-problem assumptions, coupled to a versioned problem–solution evidence graph, improve independently validated repairs through selective reactivation of prior experience without sacrificing independent exploration?**

We investigate three separable propositions:

- **H1 — Coupling:** event-triggered reactivation of appropriately scoped evidence improves verified repair success compared with the same memory, retrieval opportunities, and resources without the trigger.
- **H2 — Selective disclosure:** selectively revealing warranted prior evidence can outperform—or at least avoid degradation relative to—access to the full admissible history under an equal context and execution budget.
- **H3 — Structural retrieval:** adding problem-seeded PPR to hybrid lexical–semantic retrieval improves recovery of valid multi-hop experience without materially degrading recall of direct, relevant evidence.

These are hypotheses, not findings. The contribution sought is a falsifiable mechanism and an auditable experimental contrast, not a new claim of novelty for graphs, RAG, PageRank, agent memory, or multi-agent systems individually.

### 2. Related work and remaining gap

GraphRAG structures retrieval around explicit relations and broader corpus organization [1]. HippoRAG connects knowledge graphs with Personalized PageRank for associative retrieval [2], and HippoRAG 2 studies the balance between associative and factual memory [3]. LightRAG supports graph/text retrieval and incremental updates [4]. G-Memory organizes experience at multiple levels across agents [5]. ReasoningBank distills strategies from successful and unsuccessful agent trajectories [6]. Research specifically on software-engineering memory shows both opportunities and failure modes: coarse episode-level memories can mismatch a current subtask [7], while episodic memory may inject noise or unhelpful history [8].

Our target differs from a generic long-term-memory store. The treatment is a **typed, version-checked causal trigger**: when an independently verified condition changes, only evidence connected to the affected solution and valid under the new condition becomes eligible for prioritized reactivation. Historical counterexamples remain visible as warnings without being promoted to present-day truths. Separately, selection and non-disclosure are tested rather than assumed beneficial.

### 3. Versioned problem–solution experience graph

Let the research state at revision t be

**G_t = (V_P, V_S, V_E, E_PP, E_SS, E_PS, E_EV, ν_t)**,

where V_P contains problems, requirements, assumptions, and subproblems; V_S contains approaches, patches, hypotheses, counterexamples, and results; V_E contains independently assessable evidence; and ν_t is the authoritative revision. Typed edges record problem dependencies, solution relationships, problem-to-solution applicability, and solution-to-evidence provenance.

Each independently defined problem has one versioned project record. A persistent project ledger, rather than agent chat transcripts, is the source of truth. Cross-project retrieval uses derived, rebuildable indices; graph scores may never overwrite original evidence. The current code or dependency revision, the scope of a claim, its source receipt, and its verification method accompany every result.

A memory item has an epistemic state such as **HYPOTHESIS**, **CONDITIONALLY_SUPPORTED**, **VERIFIED**, **REFUTED_UNDER_ASSUMPTIONS**, **UNRESOLVED**, or **SUPERSEDED**. A failed provider call is not a failed repair; agreement between agents is not independent verification. Refutations are preserved with their exact preconditions and are reconsidered, not erased, when those preconditions change.

An evidence item becomes a transferable candidate only when its prerequisite constraints can be checked against the receiving problem. A suggested analogy is stored as a hypothesis until validated. An apparently similar patch from an incompatible version is not silently treated as applicable.

### 4. Retrieval and the coupling mechanism

#### 4.1 Structural discovery

The default candidate generator combines lexical search (e.g., BM25) and optional dense retrieval. It may expand along **content-bearing, provenance-supported graph edges**, followed by problem-seeded PPR:

**p = (1 − α)s + αPᵀp**,

where s is the restart distribution derived from the current verified problem entities, P is the normalized transition matrix over eligible content relations, and α is a predeclared continuation probability. PPR can identify experiences connected through multiple meaningful steps; it cannot assign truth to those experiences.

**Usage counts, agent popularity, raw frequency, and negative/contradiction labels do not become positive transition edges.** They are considered separately during evidence eligibility, negative-knowledge checking, and analysis. The graph and its seed, revision, transition-edge policy, and retrieved evidence IDs are logged for reproducibility.

We retain a direct-retrieval safety path: a graph-ranking candidate is not allowed to suppress essential direct evidence merely by occupying a high centrality position. The structural-retrieval ablation compares hybrid retrieval against hybrid plus PPR at the same candidate and context limits. Both direct-evidence recall and multi-hop retrieval quality are reported; any loss is disclosed.

#### 4.2 Deterministic event-triggered reactivation

A verified change event is represented as

**e = (subject, predicate, old, new, revision, scope, evidence, status)**.

The trigger fires only when all of the following hold:

1. The event is independently **VERIFIED** and changes a typed problem prerequisite.
2. A revision-valid, content-bearing problem–solution edge identifies a solution affected by that prerequisite (e.g., REQUIRES, TESTED_UNDER, INVALIDATED_UNDER, BECOMES_APPLICABLE_IF).
3. The candidate experience has a provenance-linked relationship to that solution and passes access checks.
4. A frozen, deterministic scope predicate classifies the evidence as **APPLICABLE** or **HISTORICAL_CONTRAST**. Missing scope information yields **INELIGIBLE**.

A historical contrast can warn that a repair failed under the old condition; it does not assert the old result under the new condition. Triggering marks the affected hypothesis **REVIEW_REQUIRED**, not VERIFIED or REFUTED. This separation prevents retrieval from masquerading as discovery.

Predefined null cases—unchanged prerequisites, unverified events, absent typed links, revoked evidence, and incompatible scopes—must not trigger activation. These are testable implementation invariants, but passing them alone does not establish a scientific benefit.

#### 4.3 Selective context and independent work

Each agent receives a bounded, role-appropriate projection from an authorized common state. Authorization (what can legally be read) and activation (what should be disclosed now) are distinct. Necessary obligations and source references are not discarded to save tokens. The experience graph is globally queryable only through scoped, logged interfaces; it is not automatically pasted into every agent's prompt.

In independent solving phases, a blinded worker may receive a deliberately restricted evidence packet. It must not possess direct credentials to the underlying project ledger or an alternative tool path to the withheld history. The later verification phase may consult additional evidence under a separately documented access policy. This protects experimental independence while permitting controlled transfer.

### 5. Independent experimental study

The object of study is **the scientific effect of evidence activation on coding-task outcomes**, not the overall quality of any particular AI platform. A complete, cooperative research system conducts the experiments; model/provider selection and internal coordination remain operational mechanisms rather than separately scored contestants.

#### 5.1 Tasks and unit of assignment

Use real software repair tasks with immutable starting commits, dependency snapshots, issue descriptions, and independently executable validation tests, supplemented where needed by authored tasks that introduce an explicit, verified change to a relevant requirement or dependency assumption. Each task must have an independently checked target behavior and a defined family of potentially reusable past experiences.

The unit of randomization is the task-family or matched episode with a frozen initial state; related instances are grouped to avoid cross-arm memory contamination. Task difficulty, repository, agent tool set, model pool, total execution ceilings, and grader revision are fixed before outcomes are observed. Task provenance and benchmark licensing must permit use; publicly known gold patches and hidden-test solutions cannot be injected into memory.

The evidence corpus is frozen before each confirmatory block. No outcome from a held-out test becomes accessible to any treatment arm until all paired episodes for that block have finished.

#### 5.2 Conditions

| Arm | Common facilities | Treatment |
|---|---|---|
| **D** | Versioned evidence, ordinary retrieval, full cooperative problem-solving facilities | Strong established deterministic reference without the new event coupling |
| **E⁻** | Same graph, memory, capabilities, tools, workers, retrieval checkpoints and budget as E | Hybrid/graph retrieval on the current subproblem; **no** change-triggered problem–solution reactivation |
| **E** | Identical facilities and limits to E⁻ | Verified change events prioritize scoped prior experiences; unfilled evidence slots revert to ordinary retrieval |
| **D*** | Same admissible evidence corpus, capabilities, timing and total context budget as E | Full-history-access / broad-disclosure control, without E's selective-withholding policy; a frozen compression/packing rule is necessary when history exceeds the context limit |

The **primary mechanistic comparison is E versus E⁻**. The **separate confirmatory disclosure comparison is E versus D***. D* is deliberately strong: it has access to the complete *admissible* history, not a weakened memory store. Equal maximum prompt size does not imply filling unused slots with irrelevant text; actual exposure and consumption are measured. An ablation of hybrid versus hybrid+PPR retrieval addresses H3 without conflating graph connectivity with event coupling.

A further, separately scoped study may compare a revision-aware referential handoff against full restatement at the same checkpoint. That communication study is **not** folded into the primary code-repair success claim.

#### 5.3 Outcomes and analysis

**Primary outcome:** proportion of assigned tasks for which the produced patch applies cleanly and passes an independent, frozen executable acceptance suite. Missing, timed-out, unauditable, or incomplete attempts count as unsuccessful for the primary intention-to-treat denominator and are reported by failure class.

**Secondary outcomes:** documented reuse of verified knowledge; prevention of repeated refuted approaches; retention of directly relevant evidence; erroneous activation; agent/tool calls; quota usage; wall time; money charges; verification cost; and human interventions. Token reduction is not a substitute for correctness.

For paired tasks, report the E−E⁻ and E−D* differences in verified success with confidence intervals computed using task-family clustered resampling; show the full paired discordance table. Analysis procedures, sample size/power targets, exclusions, and stopping rules must be fixed **before** the confirmatory run. Hypotheses without sufficient data remain unresolved. Report subgroup comparisons between cross-project transfer, within-project reuse, changed-assumption repair, and negative-knowledge cases as exploratory unless preregistered.

The evidence bundle for each episode includes the starting revision, evidence-snapshot digest, arm assignment, event and graph-edge IDs, retrieved and withheld memory IDs, model and tool fingerprints, access audit, final patch, independent grader result, and complete resource receipts. No model's own assertion of success is accepted as the outcome label.

#### 5.4 Leakage and falsification safeguards

The experiment rejects contaminated data paths: common research memory is cloned per arm; no unassigned direct ledger access is permitted; future outcomes are withheld; prior gold solutions are excluded; grading executes outside the agent process; and outcome labels cannot rewrite earlier evidence. A positive result is invalidated if hidden information reached one arm, the model pool or task definition differed between matched runs, or a critical receipt is missing.

A decisive negative result is scientifically meaningful: event coupling could expose misleading history, interfere with useful exploration, or fail because a simpler retrieval policy already finds all relevant evidence. We will report such outcomes rather than relabeling them as success.

### 6. Research status, limitations, and interpretation

This manuscript currently specifies the mechanism and an independently verifiable experimental design. **No confirmatory E/E⁻ or E/D* repair-success comparison is presented here, and no improvement, statistical significance, or generalized transfer is claimed.** Existing engineering integration tests and unrelated research datasets are not substituted for these experimental outcomes.

Key threats are incorrect graph annotation, stale project revisions, incomplete provider receipts, benchmark leakage, nonrepresentative task families, hidden test limitations, and context-policy drift. The first confirmatory stage freezes externally or mechanically verified change events and typed links to isolate the reactivation mechanism. A later end-to-end study must include the error rates of automatically generated events and links; the stage-one result cannot establish robustness of the complete autonomous pipeline.

The proposed mechanism is compatible with heterogeneous cooperative workers and with smaller models, but such compatibility is not evidence that a Gemma-based implementation has already been trained or benchmarked. Neither model weights nor a specific product architecture are asserted to be the research contribution.

### 7. Conclusion

The central idea is not to remember *more* of an agent's past, but to reactivate **the right, assumption-scoped evidence at the moment a verified problem change makes it relevant**, while preserving independent search and explicitly retaining falsified attempts as conditional negative knowledge. Typed problem–solution links, provenance, PPR-assisted retrieval, a deterministic eligibility trigger, and controlled disclosure make this proposal testable. Whether they improve software repair success remains an empirical question to be decided by the planned independent comparisons.

### References

[1] Edge et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/

[2] Gutiérrez et al. (2024). *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models*. NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/6ddc001d07ca4f319af96a3024f6dbd1-Abstract-Conference.html

[3] Gutiérrez et al. (2025). *From RAG to Memory: Non-Parametric Continual Learning for Large Language Models* (HippoRAG 2). ICML 2025. https://proceedings.mlr.press/v267/gutierrez25a.html

[4] Guo et al. (2025). *LightRAG: Simple and Fast Retrieval-Augmented Generation*. Findings of EMNLP 2025. https://aclanthology.org/2025.findings-emnlp.568/

[5] Zhang et al. (2025). *G-Memory: Tracing Hierarchical Memory for Multi-Agent Systems*. NeurIPS 2025. https://papers.nips.cc/paper_files/paper/2025/hash/136a45cd9b841bf785625709a19c6508-Abstract-Conference.html

[6] Ouyang et al. (2026). *ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory*. ICLR 2026. https://github.com/google-research/reasoning-bank

[7] Shen et al. (2026). *Structurally Aligned Subtask-Level Memory for Software Engineering Agents*. ICML 2026. https://proceedings.mlr.press/v306/shen26ad.html

[8] Lindenbauer et al. (2025). *From Knowledge to Noise: CTIM-Rover and the Pitfalls of Episodic Memory in Software Engineering Agents*. https://aclanthology.org/2025.realm-1.30/

[9] Jimenez et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* https://www.swebench.com/

[10] Google DeepMind (2026). *Gemma 4 Developer Agent Paper Track: submission requirements and evaluation*. https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview

---

**Editorial note (not part of the Kaggle submission):** Research-specific evidence tables, exact task and corpus manifests, preregistration digest, statistical power calculation, and results must be populated from real independent runs. Do not submit provisional hypotheses as completed experiments. This file is intentionally isolated from OGI and does not change any prior study protocol.
