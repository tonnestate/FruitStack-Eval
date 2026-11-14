# Frontier research A: Google "Science of Scaling Agent Systems" + Anthropic advanced tool use + multi-agent research system
Date: 2026-11-14. Method: WebFetch of originals (blog + arXiv HTML v3). WebFetch returns a small-model extraction of each page, not raw text: numbers below are as extracted; verify critical ones against the PDF before citing externally. No URL failed. The arXiv HTML extraction was truncated in places (appendices only partly seen).

Classification: D = DEMONSTRATED (controlled measurement), R = REPORTED (internal, little detail), REC = RECOMMENDATION.

## 0. Sources
- S1 blog: https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/ (Kim, Liu; published 2026-01-28)
- S1p paper: https://arxiv.org/abs/2512.08296 (HTML v3 read: https://arxiv.org/html/2512.08296)
- S2: https://www.anthropic.com/engineering/advanced-tool-use (fetched OK)
- S3: https://www.anthropic.com/engineering/multi-agent-research-system (fetched OK)
- DISCREPANCY: blog says 180 configurations; paper v3 says 260 (4 benchmarks x 45 + 2 x 40). Blog lists 4 benchmarks, paper v3 six (adds SWE-bench Verified, Terminal-Bench). Use paper v3 numbers; blog is from an earlier version.

## 1. Google paper (S1/S1p)
Design: 260 configs; 6 benchmarks (BrowseComp-Plus, Finance-Agent, PlanCraft, Workbench: 45 configs each = 9 models x 5 archs; SWE-bench Verified, Terminal-Bench: 40 each, 8 models; 20 instances each, CI about +-20pp/cell). 9 models: GPT-5-nano/mini/5, Gemini 2.0 Flash/2.5 Flash/2.5 Pro, Claude Sonnet 3.7/4/4.5. Architectures: Single-Agent (SAS), Independent, Centralized, Decentralized, Hybrid. Matched budget ~4,800 reasoning tokens/trial. Tool counts {2,3,4,5,7,16}. Intelligence Index 42-71. Prompts identical across conditions (not tuned).

### 1.1 Architecture effect is task-dependent, not uniformly positive  [D]
- Claim: MAS gains range from -70.0% to +80.8% vs SAS; overall mean MAS delta -0.3% (95% CI [-58.7, +77.2]).
- Evidence (section "Results", paper 4.2, Fig. 2), delta vs SAS mean:
  - Finance-Agent (SAS 0.349): Centralized +80.8%, Decentralized +74.5%, Hybrid +73.1%, Independent ~+57%.
  - Workbench (0.629): Decentralized +5.6%, Central/Hybrid -1.2%, Independent ~-11%.
  - BrowseComp-Plus (0.318): Decentralized +9.2%, Centralized +0.2%, Independent ~-35%.
  - PlanCraft (0.568): Hybrid -39.1%, Decentralized -41.5%, Centralized -50.3%, Independent -70.0%.
  - SWE-bench Verified (0.522): Hybrid -2.1, Central -3.1, Decentral -5.4, Independent -14.9%.
  - Terminal-Bench (0.344): Independent +1.7%, Centralized -19.2%.
- Blog states PlanCraft "every multi-agent variant degraded 39-70%" and Finance centralized +80.9% (consistent).

### 1.2 Decomposability / sequential dependency  [D for the benchmark pattern; the threshold is REPORTED-ish, derived from 6 benchmark-level points]
- Claim: parallelizable/decomposable tasks (Finance: distinct subanalyses) benefit; strictly sequential tasks (PlanCraft) are harmed ("sequential penalty").
- Evidence: domain "complexity/dependency" scores (paper App. C): Workbench 0.000, SWE-bench 0.255, Finance 0.407, Terminal-Bench 0.414, PlanCraft 0.419, BrowseComp-Plus 0.839. Extracted text claims a critical threshold D~0.40 (below: net MAS gain; above: overhead dominates). CAUTION: Finance (0.407) and PlanCraft (0.419) are nearly identical on this score yet have opposite outcomes (+81% vs -70%), so the score alone does not separate them; n=6 benchmark-level points. Treat as weak.
- Not shown: a per-task decomposability measurement validated against outcome; the score is a benchmark-level label, not computed per instance.

### 1.3 Capability saturation  [D (statistical, cluster-robust), but dataset-level n=6 clusters]
- Claim: when single-agent baseline accuracy exceeds ~45%, adding agents gives negative returns.
- Evidence: interaction P_SA x log(1+n_agents) beta=-0.236, 95% CI [-0.396,-0.076], p=0.004; decision boundary ~0.45 raw. Survives cluster-robust (p=0.004) and Holm (p_Holm=0.018). Threshold matches 94% of 16 model x benchmark configs (binomial p<0.001). Baseline main effect beta=0.250 p=0.001.
- Conflicting note: the 45% rule is fit on the same data; held-out only partly (see 1.9). Heterogeneous exceptions exist (1.8).

### 1.4 Coordination overhead  [D]
- Table 5 (means across benchmarks): success SAS 0.466 | Indep 0.370 | Decentral 0.477 | Central 0.463 | Hybrid 0.452. Turns 7.2 / 11.4 / 26.1 / 27.7 / 44.3. Overhead O% 0 / 58 / 263 / 285 / 515. Efficiency E_c (success per cost) 0.466 / 0.234 / 0.132 / 0.120 / 0.074. Success per 1K tokens 67.7 / 42.4 / 23.9 / 21.5 / 13.6.
- Turns scale superlinearly in agents: T = 2.72 (n+0.5)^1.724, R2=0.974. Hybrid 6.2x SAS turns, Central 3.8x, Decentral 3.6x.
- Overhead bands: <100% gives ~+2-4%; 200-300% best success/cost (Central, Decentral); >400% (Hybrid) over-coordination. Message density plateau c*~0.39 (S=0.73+0.28 ln c, R2=0.68; authors call it descriptive).
- Overhead main effect in the fitted model is NOT significant (beta 0.011, p=0.611); the overhead x tools term is also not significant under the final model (p=0.211) though significant under naive OLS on 4 benchmarks (-0.162).
- Takeaway: MAS cost 3-10x tokens/turns for roughly equal mean success; the benefit is only in selected tasks.

### 1.5 Tool-use bottleneck  [D]
- Claim: efficiency-tools trade-off: tool-heavy tasks suffer more from coordination.
- Evidence: E_c x T beta=-0.096 [-0.154,-0.037], p=0.002 (survives Holm p=0.026). log(tools) main effect +0.166 p<0.001 (more tools = more headroom, not worse performance per se). Blog example: coding agent with 16+ tools.
- Not shown: causal mechanism; only 6 tool-count levels, confounded with benchmark.

### 1.6 Error amplification / absorption  [D for the trace-level numbers; the metric is trace-level]
- Amplification A_e (trace-level): Independent 17.2x, Decentral 7.8x, Hybrid 5.1x, Central 4.4x, SAS 1.0. Task-level amplification only ~1.1-1.3.
- Centralized/Hybrid/Decentral error reduction average 22.7% (CI [20.1,25.3]), peak 31.4% on Finance. Independent +4.6% amplification (no correction). Central: logical contradiction 9.1% vs baseline 12.3-18.7%; context omission 8.3% vs 15.8-25.2%. Hybrid numerical drift up to 26.4%; coordination failures Hybrid 12.4%, Decentral 3.2%, Central 1.8%.
- Caveat: A_e main effect on accuracy is not significant (beta 0.014 p=0.658); only the A_e x P_SA interaction is (-0.080, p=0.022). So "amplification causes failure" is not established statistically; it is descriptive.
- Table 5 values are architecture constants applied across benchmarks.

### 1.7 Fitted predictive model  [D within-sample CV; limited generalization]
- 19 predictors (intelligence, tools, agents, baseline, overhead, message density, redundancy, efficiency, error, interactions). R2_train 0.463, R2_CV 0.373 (+-0.170); with Agentic Capability Index 0.481 / 0.413. Blog quotes R2=0.513 (earlier version).
- Architecture selection: picks best architecture for 87% of held-out configs vs 20% random, 54% capability-only. Cross-validation holds out experiments (within-domain), so 87% is a "restricted sense" of generalization (the abstract itself says so).
- Adding coordination-structure features barely helps R2_CV (0.360 -> 0.363 -> 0.373 with interactions): most predictive power comes from intelligence, tools, and baseline, not coordination metrics.
- External hold-out (GPT-5.2, Gemini-3.0 Pro/Flash, Intelligence Index 75, beyond training range 42-71): overall MAE 0.077 (15 predictions), MAPE 19.9%; 11 of 15 findings validated (73%); Hybrid over-predicted by +37%.
- Key features usable pre-activation: single-agent baseline accuracy (P_SA), tool count, model capability, expected architecture overhead.

### 1.8 Heterogeneity and family effects  [D, small n]
- 13 BrowseComp-Plus configs: centralized heterogeneous teams trailed strong homogeneous by mean 12.6pp; decentralized mixing +2.0pp. But Anthropic centralized with LOW-capability orchestrator + high-capability subagents scored 0.42 vs 0.32 homogeneous high (+31%) -> inconsistent; do not generalize.
- Family signatures: OpenAI Hybrid best on structured tasks (Finance 52% vs 39% SAS; Workbench 56% vs 42%), ~$0.008 per 1% gain; Anthropic Centralized most stable (mean 43%, SD 2.3%), Hybrid ~$0.024/1%; Google <5% spread across topologies, ~$0.012/1%. Gemini: Independent matches/beats SAS; GPT-5.2: -22.2%.

### 1.9 NOT shown / limitations (paper Section 5)
- Max 9 agents; superlinear communication growth untested beyond.
- Prompts untuned; same across models. SWE/Terminal only 20 instances (+-20pp).
- Only 6 dataset clusters: dataset-level predictors (SE inflation up to 2.9x) are descriptive.
- No per-instance decomposability measurement, no dynamic/adaptive team sizing, no learned-from-experience routing, no cost-aware optimization beyond token proxy; budget matched (not "more tokens = better").
- Internal inconsistencies noted in extraction (redundancy defined two ways; Finance SAS baseline 0.349 vs 0.280). Blog vs paper config counts differ.

## 2. Anthropic Advanced Tool Use (S2)
Three beta features (header advanced-tool-use-2025-11-20).

### 2.1 Tool Search Tool (defer_loading: true)  [R: internal evals, few details]
- What: tools marked deferred are not in context; Claude searches (regex, BM25, or custom embeddings) and loads 3-5 matches. Whole MCP servers can be deferred; keep 3-5 most-used tools loaded. Prompt caching preserved.
- Numbers: 5-server MCP setup (58 tools) ~55K tokens before the conversation (Jira alone ~17K; seen up to 134K). 50+ MCP tools: ~77K -> ~8.7K tokens (85% reduction, ~500 up-front + ~3K for found tools). MCP eval accuracy: Opus 4 49% -> 74%; Opus 4.5 79.5% -> 88.1%.
- Trade-offs (stated): extra search latency; best for 10+ tools or >10K tokens of definitions; little value for <10 tools, tools used every session, compact definitions. Relies on good names/descriptions.
- Section: "Tool Search Tool".

### 2.2 Programmatic Tool Calling  [R]
- What: Claude writes Python in a code-execution sandbox to call tools (loops, conditionals, asyncio.gather); only final output enters context. Tools opt in via allowed_callers.
- Numbers: avg tokens on complex research tasks 43,588 -> 27,297 (-37%); internal knowledge retrieval 25.6% -> 28.5%; GAIA 46.5% -> 51.2%; ~200KB raw expense data (2,000+ items) -> ~1KB; 20+ call workflow avoids 19+ inference passes.
- Trade-offs: extra code-execution step; little help for single-tool calls, small responses, or when reasoning over every intermediate is needed; document return formats; best for parallel idempotent operations.

### 2.3 Tool Use Examples (input_examples)  [R]
- What: 1-5 realistic examples per tool show formats, nested objects, optional-param correlations, tool choice.
- Numbers: complex parameter handling accuracy 72% -> 90% (internal).
- Trade-offs: more tokens; little value for simple tools / standard formats.
- Best practice (REC): layer features by the biggest bottleneck (context bloat, big results, param errors).
- Not shown: eval composition, sample sizes, variance, per-model effects; no controlled ablation of interactions between the three.

## 3. Anthropic multi-agent research system (S3)
### 3.1 Orchestrator-worker architecture  [REC/description]
- Lead agent plans, saves plan to memory (context >200K tokens truncates), spawns parallel subagents with own search loops + interleaved thinking; subagents act as compressing filters; lead synthesizes and can spawn more; a CitationAgent adds citations. Replaces static RAG with adaptive search. Section "Architecture overview".

### 3.2 Performance and token variance  [R]
- Opus 4 lead + Sonnet 4 subagents beat single-agent Opus 4 by 90.2% on the internal research eval. Section "Benefits of a multi-agent system".
- On BrowseComp three factors explained 95% of variance; token usage alone 80%; tool-call count and model choice the rest. Upgrading to Sonnet 4 gained more than doubling the Sonnet 3.7 token budget.
- Cost: agents ~4x chat tokens, multi-agent ~15x. Value of task must justify cost.
- Important: this suggests much of the multi-agent gain is more compute/tokens (confound with Google's matched-budget design, which finds no average gain at equal budget). Compatible readings: MAS = a way to spend more tokens in parallel and across contexts.

### 3.3 When multi-agent helps / hurts  [REC]
- Helps: breadth-first, parallelizable, information exceeding one context window, many complex tools.
- Hurts: shared context / many inter-agent dependencies (most coding tasks); agents not yet good at real-time coordination/delegation. Consistent with Google S1 direction.

### 3.4 Effort-scaling and delegation rules  [REC; "early versions spawned 50 subagents for simple queries" is R]
- Simple fact-finding: 1 agent, 3-10 tool calls. Direct comparison: 2-4 subagents, 10-15 calls each. Complex research: >10 subagents with divided responsibilities.
- Each subagent brief needs objective, output format, tool/source guidance, task boundaries; vague briefs gave duplicated work.
- Start wide then narrow; extended thinking as scratchpad; heuristics over rigid rules; guardrails against runaway.

### 3.5 Parallelism  [R]
- Lead spawns 3-5 subagents in parallel; each uses 3+ tools in parallel; research time cut by up to 90% on complex queries.
- Synchronous lead bottleneck remains (waits for each batch); async adds state/error complexity.

### 3.6 Tool design / self-improvement  [R]
- Tool-testing agent rewrote flawed tool descriptions: -40% task completion time.

### 3.7 Compact results to the lead  [REC]
- Subagents store output in filesystem artifacts and pass lightweight references to avoid the "game of telephone" and token overhead; summarize completed phases into external memory; spawn fresh-context subagents for long horizons (Appendix).

### 3.8 Evaluation  [REC + R]
- Start with ~20 queries (large effects). LLM-as-judge single call, 0.0-1.0 score + pass/fail on factual accuracy, citation accuracy, completeness, source quality, tool efficiency; best matched humans. Humans caught SEO-farm source bias. End-state evaluation for state-mutating agents with checkpoints. Section "Effective evaluation of agents" + Appendix.

### 3.9 Failure modes  [R, anecdotal]
- Too many subagents for simple queries; endless searches for nonexistent sources; excessive inter-agent updates; verbose queries; continuing after sufficient results; wrong tool selection; small lead-prompt changes shift subagent behavior unpredictably; stateful errors compound -> durable execution/checkpoints/retries; rainbow deployments.

## 4. Implications for an adaptive multi-model organization
All rules are hypotheses to test; thresholds come from specific benchmarks and model sets (mostly 2025 models) and must be recalibrated on our own outcome data.

Computable BEFORE activating agents (pre-activation features):
- F1 baseline: single-agent pass rate (cheap probe: 1 SAS attempt or history of the same task class). S1: P_SA.
- F2 decomposability: fraction of subtasks that are independent given a plan (plan a DAG first); critical-path length / total work = sequential depth ratio.
- F3 tool count visible to the task; F4 expected context size vs window; F5 value/cost ratio; F6 model capability (own benchmark per model).

Decision rules (each with source basis and a test):
1. R-SAS-HIGH: if estimated SAS success >= ~0.45 (S1 1.3), use single agent (or best single model + verification) unless F4 exceeds context. Test: on our task classes, sweep SAS success and measure MAS delta; expect sign flip near 0.45; compare.
2. R-SEQ: if the plan DAG's critical-path/total-work ratio is high (strict sequential chain, shared mutable state, e.g. PlanCraft, coding) -> single agent. S1 -70%/-50% on PlanCraft, S3 on coding. Test: build tasks with controlled DAG width; expect MAS delta to be monotone in width.
3. R-PARALLEL: if >= 3 independent subtasks with low shared context (Finance-like, breadth research) AND SAS success < 0.45 -> centralized orchestrator-worker (best error containment 4.4x, +81% on Finance, stable for Claude). Test: Finance-like decomposable tasks vs matched-token SAS.
4. R-NEVER-INDEPENDENT: never run unverified independent parallel agents with simple aggregation (17.2x amplification; -70% PlanCraft, -35% BrowseComp). Always route results through an orchestrator/verifier. Test: independent vs centralized at equal tokens.
5. R-TOOLS: if tool count is large (S1: 16 tools) and the task is sequential, prefer SAS; to cut tool cost use deferred loading/tool search (S2) not more agents. Test: tool count x architecture grid; measure interaction E_c x T.
6. R-BUDGET: normalize by tokens. Before claiming MAS value, compare against SAS given the same total tokens (best-of-n / longer thinking). S3's 80% variance from tokens and S1's matched-budget null mean together imply this baseline is mandatory. Test: SAS with 15x budget vs MAS.
7. R-OVERHEAD: cap coordination at ~2-3x baseline overhead (S1 optimal band 200-300%); avoid hybrid (515% overhead, +37% over-predicted, lowest efficiency). Cap agent count (S1 tested <=9; S3 effort tiers: 1 / 2-4 / >10 by complexity). Test: success per 1K tokens vs agent count; stop adding agents when marginal gain < cost.
8. R-EFFORT-TIERS (S3 REC): classify query complexity -> {1 agent, 3-10 calls; 2-4 agents; many agents}. Test: tier classifier accuracy vs oracle best tier.
9. R-HETERO: do not assume strong-orchestrator or weak-orchestrator is better; S1 evidence is contradictory (-12.6pp vs +31%). Make orchestrator choice an experiment per model pair. Test: factorial orchestrator x worker model.
10. R-CONTEXT: if information exceeds a single context window or results are large, use subagents/PTC-style code execution to return compact results (S2 -37% tokens; S3 artifact references). Test: token and accuracy change with and without compaction.
11. R-VERIFY: end-state/LLM-judge checks on final state (S3); expect them to add cost but absorb errors (S1 error reduction 22.7%).
12. R-PREDICT: fit a small model (features F1-F6 + architecture) on our own runs; S1 got 87% architecture-selection accuracy using mostly intelligence+tools+baseline; use it only as a prior with SAS as a safe default, and expect weaker accuracy out of distribution (S1 hold-out MAE 0.077; 73% of findings replicated on newer models).

Experimental design hints: matched-token controls; per-instance decomposability labels (not benchmark-level); >=100 instances per cell (S1 20-instance cells gave +-20pp CIs); report overhead, turns, and error propagation, not only accuracy; keep SAS as baseline arm in every comparison.

## 5. Evidence-quality summary
- Strongest: S1 architecture-by-benchmark deltas, overhead/turn tables, capability-saturation interaction (cluster-robust), tools x efficiency trade-off.
- Weak/fragile: D~0.40 threshold (6 points, Finance/PlanCraft nearly identical score), error amplification as a causal driver (main effect n.s.), family/heterogeneity patterns (small n, contradictory), R2 only 0.37-0.41.
- Anthropic posts: internal, no CIs, no sample sizes; treat as engineering experience, not controlled evidence.
