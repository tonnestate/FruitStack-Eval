# FruitStack Frontier Research Transfer — Technical Report (2026-11-14)

**Scope.** This report covers the owner order "FRUITSTACK — FRONTIER RESEARCH TRANSFER & CAPABILITY UPGRADE" and its four phases: evidence and inventory, targeted implementation, focused local validation, and documentation.

**Evidence levels.** Every statement carries one of the following labels:
- **[SRC]** a primary-source finding;
- **[LIVE]** observed on the installed system or on real owner missions;
- **[TEST]** a local deterministic test;
- **[REPLAY]** an offline re-evaluation of recorded real data;
- **[PRED]** a theoretical prediction that has not been measured.

No benchmark campaign was run. EVAL-006 was not restarted, and PILOT-B stays stopped and unchanged.

**Phase-1 source files** are in `reports/frontier-2026-11-14/`:

| File | Content |
|---|---|
| `A_google_scaling_anthropic.md` | Google agent-system scaling; Anthropic advanced tool use and multi-agent research |
| `B_deepmind_verification_discovery.md` | AlphaProof Code, Aletheia, AlphaEvolve |
| `C_openai_tools_evals.md` | OpenAI tool search, programmatic tool calling, agent evals, skills, MCP |
| `D_fruitstack_inventory.md` | Read-only inventory of the installed system, with file:line evidence |

Sources were read through a fetch tool that returns model extractions. Key numbers must be checked against the PDFs before anyone cites them externally.

## 1. Frontier findings that matter for FruitStack

### 1.1 Google Research, "Towards a science of scaling agent systems" (paper v3, arXiv 2512.08296)

**Study size.** The paper (v3) covers 260 configurations, 6 benchmarks and 9 models. The blog states 180 configurations and 4 benchmarks.

**Architecture value is task-dependent [SRC, demonstrated].** Relative to a single agent, effects range from −70 % (sequential planning, PlanCraft) to +81 % (decomposable Finance). The mean effect is about 0.

**Capability saturation [SRC, demonstrated].** Above a single-agent baseline of about 45 % success, adding agents has negative returns (β = −0.236, p = 0.004, survives Holm correction).

**Coordination cost [SRC, demonstrated].**
- Overhead is +58 % (independent) to +515 % (hybrid).
- Turns grow as n^1.72.
- Mean success is about equal across architectures, at 3–10× the cost.

**Error amplification [SRC].**
- Unverified independent aggregation amplifies errors 17.2×; centralized orchestration with verification amplifies them 4.4×.
- Orchestrator verification reduces errors by 22.7 %.
- The amplification main effect on accuracy is not significant, so a causal claim is not established.

**Architecture prediction [SRC].** The best architecture is predictable for 87 % of held-out configurations. The prediction uses capability, tool count and baseline; per-instance decomposability was not measured.

### 1.2 Anthropic

**Advanced tool use [SRC, reported internally].**

| Mechanism | Reported effect |
|---|---|
| Tool Search | −85 % tool-definition tokens; MCP-eval accuracy 49 → 74 % (Opus 4) |
| Programmatic Tool Calling | −37 % tokens; GAIA 46.5 → 51.2 % |
| Tool Use Examples | parameter accuracy 72 → 90 % |

No sample sizes or variance are given.

**Multi-agent research system [SRC, reported].**
- A lead agent with subagents scored +90 % over a single agent.
- Token usage explains 80 % of performance variance, so much of the gain is extra compute.
- Multi-agent work helps breadth-first parallel tasks and hurts shared-context tasks such as coding.
- Effort scaling is set explicitly: 1 agent for simple queries, more than 10 only for complex research.

### 1.3 DeepMind

**AlphaProof Code [SRC].** The repository `google-deepmind/code-verification` is Apache-2.0, with MIT/AGPL third-party parts, and no code was reused here.
- Human-approved specifications are trusted.
- Lean 4 proofs come from untrusted agents.
- A deterministic gatekeeper alone can declare a goal done. It compares the statement and all transitive definitions with a held-out copy, allows only standard axioms, rejects `sorry`/`native_decide`, and replays the proof in a fresh kernel.
- Amendments are decided by a critic who never sees proof attempts. They must be necessary, non-weakening and small. A weakening is escalated to a human.
- Non-vacuity is enforced through satisfiability and reachability witnesses, plus mutants such as re-introduced real bugs that must break the theorem.
- Observed spec gaming: an agent redefined a predicate as `False`.

**Aletheia [SRC, blog].** The loop is generator → verifier → reviser.
- The verifier has three verdicts: correct, minor fix (sent to the reviser), critically flawed (sent back to the generator).
- The verifier is a natural-language model, not a formal checker.
- The system may explicitly admit failure.

**AlphaEvolve [SRC].** It runs evolutionary search with a user-written executable `evaluate` function and an evaluation cascade with early pruning. It uses a MAP-Elites and island program database and a fast-plus-strong model ensemble. Verification is domain-specific.

### 1.4 OpenAI [SRC]

Deferred tool loading with client-side tool search, programmatic tool calling (only the final result returns to the model), trace grading, the open Agent Skills format, and MCP `allowed_tools` / `require_approval` are all **provider-independent patterns**. Only their hosted runtimes are proprietary. None of the pages reports a measured benefit.

## 2. FruitStack as installed (pre-existing mechanisms) [LIVE, inventory D]

**Already present:**
- Adaptive staffing: interaction lanes, CherryMe triage (model-judged), and `peachme.research.research_decision` as the single activation rule.
- Brother Mode with stop reasons.
- Executed checks: RECOMPUTE (no model), and COMPUTED_CHECK, where 2 independent workers formulate assertions and the host evaluates them.
- Research Tree with FALSIFIED nodes, ExperienceLibrary, PlumMe Beta-Bernoulli competence, hash-chained receipts, ToolGateway effect classes.
- `_TRUSTED_KINDS`: only host verifiers feed competence.
- The `study_gate` grader in FruitStack-Eval.

**Absent:**
- EVC as code.
- Deterministic solvers in any live virtualenv (no sympy, z3, mpmath, FLINT, GDAL/PROJ or Lean).
- Lazy tool-schema loading and capability metadata (purpose, I/O contract, determinism, latency).
- PomeloMe and PhysalisMe on the live path.
- A geographical-competition repository (only marketing GEO exists).

A "ZOMBIE" project was not found under that name; memory refers to a PlumMe scope bug. The repository searches for ZOMBIE and geo timed out, so both findings are not exhaustive.

**Real-mission outcome table [LIVE, read-only, `analysis/real_missions.py`].**
- 71 recorded missions: 24 completed, 33 blocked, 14 error. All 24 completed missions ran on the full runtime.
- In **24/24 full-runtime missions the multi-model research phase was not activated**:
  - 12 were settled by the inquiry and executed checks;
  - 10 were triaged as single-worker;
  - 1 was a simple task;
  - 1 had an invalid triage.
- Every verified outcome came from executed checks: 13 SUPPORTS, 3 CONTRADICTS, 5 NOT_CHECKABLE, 3 INVALID_CHECK, 1 DISAGREEMENT.
- Claims: 13 supported, 3 refuted, 21 unknown.

This matches the Google finding [SRC]: the organisation's verified value on real owner tasks currently comes from **deterministic or quorum-executed checks**, not from adding agents.

## 3. Gap analysis

For each item: what the research shows, what FruitStack already has, the gap, the expected benefit, and the decision taken.

### G1 — Non-vacuity of executed checks (AlphaProof Code gatekeeper) → implemented
- **Research:** A gatekeeper must reject proofs that cannot fail, and mutants must break the spec [SRC].
- **FruitStack before:** COMPUTED_CHECK already rejected unsourced numbers, unchecked claim figures and checks that compute nothing.
- **Gap:** A loose tolerance (`abs(x-1100)<50`), a one-sided bound, `!=` used for an equality claim, or a tautology beside a real computation would **SUPPORT a false claim**.
- **Expected benefit:** fewer false SUPPORTS.
- **Overhead:** two extra host evaluations per passing vote; no model call.

### G2 — Spec-level non-vacuity for mission claims → implemented earlier on 2026-11-14 (Aurora `9b1b89d`)
- **Research:** Agents game specs by weakening them; an agent defined a predicate as `False` [SRC].
- **FruitStack equivalent [LIVE]:** The claim formulator turned the owner's calculation into "the rates can be calculated", so the grader had nothing to check. A wrong residual debt (179,000 against 182,627 EUR) went out unverified.
- **Fix:** Calculation tasks now yield concrete figure statements, and a meta-claim filter rejects statements about the question itself.

### G3 — Diagnosable organisation decisions (prerequisite for calibrated EVC) → implemented
- **Research:** Architecture choice is predictable from measured features [SRC]. Owner order: calibrate on real outcomes.
- **FruitStack before:** Triage inputs and results were not persisted. A live `INVALID` triage (mission b46e6514) could not be diagnosed.

### G4 — EVC / capability-saturation rule → NOT implemented (measurement first)
- **Research:** Above a ~45 % baseline, adding agents hurts [SRC].
- **FruitStack today:** Research activation is already rare (0/24) [LIVE], so a saturation gate would change nothing measurable now.
- **Instead:** The calibration basis was built (G3 and `analysis/real_missions.py`).
- **Prediction [PRED]:** The useful rule is the inverse question: *when* to escalate. Candidate features are triage `task_class`, the best qualified worker's PlumMe competence for the task class, and claim checkability. These must be fitted on real outcomes before any promotion.

### G5 — Executed checks in Aurora research → existing mechanism unwired, deferred
- `verifier` and `check_author` exist in PeachMe and in FSE `code_checks.py`, but Aurora passes neither [LIVE].
- They are only relevant for code missions, and the owner's real missions are not code. Study B (PILOT-B) was stopped by the owner, so this is deferred.

### G6 — Tool search / programmatic tool calling / capability catalogue → not implemented
- **Research:** These pay off with many tools (Anthropic: little value under 10 tools) [SRC].
- **FruitStack [LIVE]:** Aurora research passes no tool registry at all, and FruitStack's models do not call tools in-loop. There is nothing to defer yet.
- **Prediction [PRED]:** This becomes valuable once deterministic solver tools exist (G7).

### G7 — Deterministic math and geo tooling → owner decision
- No solver is installed in any live venv [LIVE].
- Installing sympy/mpmath (pure Python) into the worker venv is a live-environment change, and FLINT, z3, GDAL/PROJ and Lean need system packages. Deferred to the owner (see §6).

### G8 — Aletheia three-way verdict → mostly present
- REFUTED, UNVERIFIED and repair already exist, and FALSIFIED nodes are kept.
- No new mechanism was added. Naming a distinct "critically flawed → regenerate" verdict is follow-up work.

## 4. Changes made (branches pushed with `[skip ci]`; nothing merged)

| # | Component | Branch @ commit | Change | Live? |
|---|---|---|---|---|
| 1 | CherryMe `cherryme/claim_check.py` | `cc/computed-check-nonvacuity` @ b723562 | Mutation control: each claim figure is scaled ×1.01/×0.99. If all assertions still hold → `INVALID:NON_DISCRIMINATING`, which counts as no vote, and another independent worker is asked. Refutations need no mutant. Conventions (12 months, 100 %) are never mutated through a percent reading. | No (needs a release switch) |
| 2 | CherryMe `engine.py` | same @ 46979d7 | A refused (INVALID/UNPARSEABLE) triage keeps a 600-character excerpt of the worker answer. | No |
| 3 | PeachMe `mission.py` | `cc/synthesis-objective-hint` @ d31a3e3 | RESEARCH_SKIPPED/SELECTED events carry `triage` (status, record, model, receipt, excerpt). | No |
| 4 | PeachMe `mission.py` | same @ 8ad210d | The synthesis lease objective is bounded like research, so objectives over 512 characters no longer fail `INVALID_OBJECTIVE`. | No (awaits owner) |
| 5 | Aurora `aurora_chat.py` | `cc/decision-contract` @ 9b1b89d | Calculation tasks → concrete figure claims; meta-claim filter; only-meta → unknown (the mission is kept). | **Yes**, with backup |
| 6 | Aurora `aurora_peach_runtime.py` | same @ 055c980 | The result keeps `event_details` (error codes and reasons). | **Yes**, with backup |
| 7 | AnanasMe systemd drop-in | (host config) | Mission Control gets the same full-runtime environment as tonn-crm (identical file). | **Yes**; rollback: delete file and restart |
| 8 | FruitStack-Eval `analysis/real_missions.py` | `cc/superiority-evidence-2026-11-14` | Read-only table of decision against outcome over real missions; includes a self-check. | n/a |

## 5. Validation

- **[TEST] CherryMe:**
  - `tests/test_claim_check.py`: 8/8, including the new negative-control test. Loose tolerance, one-sided bound and tautology are rejected; the tight check still passes; refutation is unaffected.
  - Triage and responsibility tests: 54/54.
- **[TEST] PeachMe:** mission end-to-end 17/17 and research tests 49 passed, run against the patched CherryMe. The PeachMe suite earlier: 402 passed. The same 10 PomeloMe failures appear on the untouched baseline.
- **[TEST] Aurora:** runtime and decision-contract tests 14/14; claim-formulation tests 4/4.
- **[REPLAY] G1 against real data:** all **22 PASS votes** recorded in real owner missions were re-judged with the new rule, and **22 still PASS**. There are no false rejections on real data, and no historical vacuous support was found.
- **[LIVE] G2 on the owner's real Makler request (mission b46e6514):**
  - The fast model's wrong figures (A = 1,875, B = 1,750 EUR) were **REFUTED** by COMPUTED_CHECK, using two lineages (gpt-6-luna and gpt-oss-120b) with the host evaluating.
  - The answer gave the correct 1,100 and 1,180 EUR.
  - The comparison claim stayed UNKNOWN, honestly, because its assumptions are not stated in the task.
  - This is one case. It shows the mechanism works; it does not establish a rate.
- Sandboxing: all tests ran sandboxed (systemd-run with no network beyond localhost and live state directories inaccessible).

## 6. Limitations and open owner decisions

1. Changes 1–4 are verified locally but **not live**. Going live means a release-symlink switch for CherryMe/PeachMe, which needs owner approval; the auto-mode classifier stopped such a switch earlier.
2. tonn-crm, the old Mission Control path, still has the previous `aurora_chat` loaded until it is restarted.
3. The non-vacuity rule uses a 1 % perturbation. A claim stated only roughly ("about 1,100 EUR") whose check uses a wider tolerance will now get no vote and stay UNVERIFIED rather than SUPPORTED. This is deliberately conservative.
4. No deterministic solver is installed. Mathematical and geographical tool capability (sympy/mpmath first; FLINT, z3, Lean, GDAL/PROJ next) needs an owner decision on installing into the worker environment.
5. COMPUTED_CHECK assertions are still model-formulated. The host guarantees arithmetic, number provenance, agreement and now discrimination, but not that two workers cannot formulate the same wrong model of the problem. **This is not formal proof.**
6. A creator-portal HMAC secret appeared in a local tool output during this work. It was not sent anywhere. Rotation is recommended; this was already open.

## 7. Follow-up experiments needed before claiming performance gains

- **E1 (G1):** False-SUPPORT rate of COMPUTED_CHECK with and without the negative control, on a frozen set of real calculation claims with seeded wrong figures. Exact McNemar via `study_gate`.
- **E2 (G4):** Fit escalation features against real outcomes once ≥100 full-runtime missions carry the new `triage` event data. Report the predictive accuracy on a later hold-out period before any rule is promoted.
- **E3 (OGI-013, unchanged question):** None of the above is evidence that organised collaboration beats controlled alternatives. The controlled designs stay as written in `evidence/20261114-SUPERIORITY-SYNTHESIS/REPORT.md`.

---

## Addendum (same day): xAI/Grok and DeepSeek, and a cross-vendor synthesis

Source files: `reports/frontier-2026-11-14/E_xai_grok.md` and `F_deepseek.md`. All 12 URLs resolved.
- **DeepSeekMath-V2:** read from the arXiv HTML v1. Figures were not recoverable, and the model-weights licence was not read.
- **GitHub:** the deepseek-ai organization listing showed 10 of 47 repositories.

### A1. xAI / Grok [SRC]

**Evidence status.** No measured performance on any page: everything is a documented product capability.

**Grok Build Workflows (2026-07-23).**
- Grok writes a plan script (phases → agents → roll-up) from the request, smoke-checks it, and fans out 128 agents by default (max 1,024).
- Each agent starts with a clean context, and independent "skeptics" are optional.
- Persistence is one sentence: "Progress is saved as the run goes, so pausing and resuming never redoes finished work." Granularity, crash semantics and side-effect idempotency are not documented.
- Traces are a human UI view only.

**Multi-Agent API (beta, `grok-4.20-multi-agent`).**
- The caller chooses 4 or 16 agents; the server decides the roles.
- A leader synthesises the final answer.
- Sub-agent state is returned only as **encrypted content**.
- There are no client tools and no `max_tokens`.

**Remote MCP.** The only boundary is `allowed_tools`. `require_approval` is not supported.

**Code execution.** An ephemeral Python sandbox without network.

**Async.** Client-side concurrency only, not a resumable job API.

### A2. DeepSeek [SRC]

**DeepSeekMath-V2 (arXiv 2511.22570).**
- **Verifier:** a proof-level verifier lists issues *before* scoring (0 / 0.5 / 1) and needs no reference solution.
- **Meta-verifier:** it checks that each reported issue really exists and that the score matches. It exists because a score-only verifier earned reward on flawed proofs while hallucinating issues. Mean analysis quality rose from 0.85 to 0.96.
- **Generator:** it is trained to self-verify, because an untrained generator overclaims its own correctness.
- **Auto-labelling:** the label is the lowest score confirmed by several valid analyses.
- **Test-time scaling:** up to 64 proofs × 64 analyses with iterative refinement.
- **Reported results (REPORTED):** IMO 2025 83.3 %, Putnam 2024 118/120. These were graded by the authors' own experts and verifier, not independently.
- **The authors' framing:** "no issue found in 64 attempts" is evidence, not formal proof.

**API (2026-11-13).** Current ids are `deepseek-flash` and `deepseek-v4-pro`.
- Thinking is on by default; effort is low / high / max.
- With tools, all prior reasoning content must be passed back.
- Strict tool schemas are beta.
- The KV prefix cache is best-effort, and its pricing difference is not stated on the page.
- Search/Fetch is a provider-billed API.

### A3. Comparison with FruitStack's operational implementation

| Mechanism (source) | FruitStack today [LIVE / inventory] | Gap and decision |
|---|---|---|
| Plan-as-script fan-out, 128–1,024 agents (Grok Workflows) | CherryMe triage → `research_decision` (one rule for all hosts); Brother Mode with 2 solvers; PeachMe research pool with `max_workers` 3 | **Rejected.** No evidence that it is better (A1). Google [SRC] shows negative returns above a ~45 % baseline, and 24/24 real missions needed no research. Large fan-out conflicts with "only resources justified by the task". |
| Clean specialist contexts (Grok) | CogC role packets hide origin answer, opinions and ranking from workers (`cherryme/cogc.py`) | Present. |
| Independent skeptics (Grok, optional) | COMPUTED_CHECK quorum from different independence groups; LSD Room challenge; FALSIFY questions | Present, with stronger rules (host-evaluated, number provenance, negative control). |
| Durable checkpoints / resume without redoing work (Grok, one sentence) | PeachMe StepLedger (idempotent step keys, UNKNOWN-step reconciliation, receipts held), MangoMe checkpoints, KIwiMe recovery timer | FruitStack is ahead on documented semantics; nothing to copy. |
| Encrypted sub-agent state (Grok API) | Hash-chained receipts; mission record keeps workers, receipts and assertions | **Rejected** for study arms: it cannot be independently inspected. A provider multi-agent call could only be recorded as one opaque UNVERIFIABLE step. |
| MCP with `allowed_tools` and no approval (Grok) | ToolGateway effect classes; undeclared tool = IRREVERSIBLE; PomeloMe effect authorisation (not live) | FruitStack's boundary is stricter. |
| Proof-level verifier listing issues before scoring (DeepSeekMath-V2) | COMPUTED_CHECK: assertions first, then the host evaluates (no model score) | Present in a stronger, executed form for computable claims. Learned natural-language verification of non-computable reasoning is not present. |
| Meta-verification of issue reports (DeepSeekMath-V2) | Refutation required only verdict agreement | **Implemented (G9):** a refutation counts only if the independent workers agree on the computed counter-value. |
| Verify the delivered text, not only pre-formulated claims (DeepSeekMath-V2 lesson) | Only claims were checked; the answer could carry unchecked figures | **Implemented (G10):** deterministic figure audit of every Aurora answer; live. |
| Generator self-verification (DeepSeekMath-V2) | Synthesis states which parts are verified (label computed from findings, never from model wording) | A model's self-claim stays non-authoritative (the paper itself reports overclaiming). No change. |
| Lowest-confirmed-score aggregation; adaptive verification effort (DeepSeekMath-V2) | Quorum of 2, up to 2 spare workers on invalid formulations | Partly present. Escalating on disagreement is follow-up work (E4). |
| Thinking effort and reasoning-content contract (DeepSeek API) | PlumMe routes models; no per-call effort parameter | Not implemented. It matters only if DeepSeek is routed with tools, and the reasoning content must then be preserved across turns. Recorded as a PlumMe adapter requirement. |

### A4. Strongest available mechanism per function (cross-vendor)

| Function | Strongest documented mechanism | Evidence | FruitStack position |
|---|---|---|---|
| Adaptive organisation | Google: architecture predicted from capability, tools and baseline (87 % held-out) | DEMONSTRATED | Triage plus single activation rule; calibration data now recorded (G3). E2 pending. |
| Parallel execution | Anthropic: parallel subagents for breadth-first research (+90 %, mostly extra compute) | REPORTED | Present (parallel critics, research pool); rarely needed by real missions. |
| Tool / capability discovery | Anthropic Tool Search (−85 % tokens) / OpenAI deferred loading | REPORTED | Not yet relevant (no in-loop tools). |
| Deterministic computation | Executed checks with host evaluation (FruitStack) / AlphaEvolve evaluator cascade | DEMONSTRATED (domain) | RECOMPUTE + COMPUTED_CHECK; no solvers installed (G7). |
| Formal verification | AlphaProof Code: Lean kernel + deterministic gatekeeper + held-out spec | DEMONSTRATED (case) | Not present. Executed checks are evidence, not proof. |
| Independent grading | AlphaProof gatekeeper + DeepSeek meta-verification | DEMONSTRATED / REPORTED | `study_gate` (offline), COMPUTED_CHECK negative control (G1), counter-value agreement (G9), answer audit (G10). |
| Organisational learning | DeepSeek verifier-labelled data loop (needs training); AlphaEvolve program database | REPORTED | PlumMe competence (Beta-Bernoulli), ExperienceLibrary, FALSIFIED nodes; no promotion without validation. |
| Recovery / self-repair | (none of the vendors documents more than FruitStack's step ledger) | — | StepLedger + KIwiMe. |
| Context efficiency | Anthropic programmatic tool calling (−37 % tokens) | REPORTED | CogC role packets; no MCP result capping (follow-up). |
| Evidence preservation | AlphaProof: logged amendments, held-out spec, replay | DEMONSTRATED (case) | Receipts, mission records, `event_details`, triage events (G3), `study_gate` sealed manifests. |

### A5. Additional changes (branches pushed with `[skip ci]`)

| # | Component | Commit | Change | Live? |
|---|---|---|---|---|
| G9 | CherryMe `claim_check.py` | `cc/computed-check-nonvacuity` @ 92a8a03 | A refutation needs the independent workers to agree on the counter-value. Otherwise the outcome is DISAGREEMENT (`COUNTER_VALUES_DIFFER`). CONTRADICTS evidence names "computed instead: X". | No (release switch) |
| G10 | Aurora `aurora_peach_runtime.py` | `cc/decision-contract` @ 6c8a504 | Figures in the delivered answer that no check covered are named in a note and in `answer_figures_unchecked`. Grouped thousands are read as thousands; the percent reading applies only before "%". | **Yes**, with backup `.bak-20261114T081518Z` |

**Validation**

- **[TEST]** CherryMe tests: 55/55. PeachMe mission end-to-end: 17/17. Aurora tests: 21/21, against both the live and the patched CherryMe.
- **[REPLAY]**
  - The 2 real model-check refutations (b46e6514) still stand, with agreeing counter-values 1100 and 1180.
  - Of 23 real full-runtime answers, 6 carry figures that nothing checked, including the wrong 179.000 EUR (49ed0bdb). In b46e6514 the correct 1.100 and 1.180 are also flagged. The live CherryMe does not yet state "computed instead", and with G9 deployed these figures would be covered.

**Performance and resources.** G9 and G10 are deterministic; they add no model call and need microseconds per claim or answer. G1/G9 can cost at most the existing 2 spare worker calls when a formulation is rejected.

**Was the grader defect addressed?** Yes, on three levels:
1. Concrete figure claims instead of meta-claims (G2, live).
2. Checks that cannot fail, or refutations without an agreed value, no longer count (G1 and G9, branch).
3. Figures that bypass the claims entirely are now named in the answer (G10, live).

What remains is a model-formulated computation shared by both workers. That needs either a trusted reference formula (an owner-curated computation library) or formal methods.

### A6. Follow-up experiment

**E4 (G9/G10).** On the frozen set of real calculation claims (E1), seed both wrong figures and wrong counter-models. Measure false-REFUTED and false-SUPPORTED rates with and without counter-value agreement, using an exact paired test via `study_gate`. A learned verifier (e.g. a DeepSeekMath-V2-style model) may be added only as an additional vote, never as the sole authority approving its own outputs.

### A7. Follow-up actions taken in parallel (2026-11-14, later the same day)

- **Live (owner approval "Du kannst alles machen, aber bitte jetzt nicht das CRM neu starten"):**
  - CherryMe-current → 92a8a03 (G1, G9, triage excerpt).
  - PeachMe-current → d31a3e3 (512-character objective fix, triage events).
  - sympy 1.14 and mpmath 1.3 installed in the worker venv.
  - Rollback notes are in `/root/contracts/frontier-2026-11-14/ROLLBACK-*.txt`.
- **Live acceptance on the owner's Makler request (mission 81772a97):**
  - Rate A 1.100 EUR: SUPPORTED by two discriminating checks.
  - Claim "rate B is 1.200 EUR": REFUTED, with "computed instead: 1180".
  - `answer_figures_unchecked = []`.
  - Triage activated research for the first time (CHALLENGE). Several LSD research workers failed with unusable output or rate limits, which is a supply issue and still open.
- **Zombie processes:**
  - Mission and observer subprocesses were never waited for. Aurora 054ddda now reaps them in a background thread. It is live in AnanasMe after a restart; tonn-crm was not restarted, per the owner.
  - An hourly read-only report runs as `fruitstack-zombie-check.timer` and writes `/var/lib/fruitstack/zombie-check.jsonl`.
  - The 3 remaining zombies belong to the Codex app-server daemon.
- **Cost-rule mismatch (PILOT-B addendum 1):** PeachMe `cc/paywall-free-account` @ d3c6482. Routes of owner-declared free accounts (no payment method) reserve zero cash. An unknown price alone stays refused, deliberately narrower than PlumMe's rule. The live switch was stopped by the auto-mode safety check and needs explicit owner approval.
- **MCP result size (Anthropic and OpenAI context efficiency):** PlumMe `cc/compact-mcp-results` @ c4534ca.
  - Status tools are compact by default, with `full=true` to opt in.
  - Measured live payloads: plum_recovery_status 448 KB, plum_status 115 KB, plum_market_status 72 KB (5–8 s).
  - No FruitStack caller reads the large views.
  - Deploying needs a plumme-mcp restart, which is an owner decision.
- **Correction to inventory D §8:** Project ZOMBIE exists, at `/root/Zombie` (tonnestate/Zombie, public; protocol v1.7 and harness, no completed experiments). No geographical-research programme was found on the host.
