# OGI-013: independently evaluated adaptive FruitStack organisation

**Revision: OGI13-PAIRED/1 (NEW; does not modify PILOT-PROC/1 or any deposited OGI-012 evidence).**
**Research status: NOT_PROVEN.** Source code in a proposal branch is not a VPS evaluation. Original full-stack mandate: GitHub issue #1; implementation tracking: GitHub issue #2.

## Research intent

FruitStack tests **organisational** intelligence with replaceable, low-cost workers, not an AGI model-weight claim. The organisation is allowed to be irregular, sparse, dynamic, and simpler than a company. A single worker or deterministic tool is sufficient when it gives the best verified result. Fixed and adaptive collaboration must use identical models, provider supply, skills, tools, task/grader versions, and budget caps. The observed extra cost of recruitment, verification, retries, coordination and recovery must be counted; free-tier quota depletion is a resource, even when billed USD is zero.

## Architecture of the actual experiment

External host runner (not an evaluator import):
- IntakeGov/SPRARI and MangoMe own qualified work identity and reuse/canonical acceptance.
- CherryMe owns cognitive inquiry and how to assemble competences; PlumMe owns labour market, skill eligibility, model/route supply and its own DecisionLog.
- PeachMe is the virtual session/signal admission layer, PomeloMe the deterministic effect/recovery runtime, AppleMe is NoLLM trajectory assurance.
- OrangeMe preserves the project ledger; CogC compiles safe efficient model-specific context; BlueberryMe controls sensitive egress. Other specialist tools are invoked only for justified tasks.
- One job can deliberately have one worker, while another uses a task-specific irregular competence graph.
- Independently configured external benchmark grader and resource counters export observation rows. The independent evaluator **never** imports any product modules.

**Blocking real-world integration checks:** exact VPS source/branch parity; PeachMe metered CherryMe child calls (proposal PeachMe PR #18); PomeloMe effects and reconciliations (proposals PeachMe PR #19 / PomeloMe PR #2); CherryMe responsibility graph (proposal CherryMe PR #3). Never describe unmerged proposals as live dependencies.

## Observation contract: FSE-OGI13-PAIR/1

One JSONL row per `(task_id, arm)`, where `arm` is `FIXED` or `ADAPTIVE`. The host exports only independently graded outcomes and non-sensitive receipt identifiers; **no prompts, secrets, raw outputs or provider credentials**. Required fields:

- Task parity: `task_id`, `benchmark_id`, `benchmark_revision`, `task_manifest_digest`, `grader_digest`.
- Treatment parity: `model_pool_digest`, `skills_digest`, `tools_digest`, `budget_digest`, `supply_regime_id`.
- Canonical source and execution lineage: `work_ref`, `trace_ref`, `provider_receipt_refs` (list; must be complete to claim efficiency).
- Grader: `grade_status` is `VERIFIED`, `UNKNOWN` or `INCOMPLETE`. For `VERIFIED`, `grade` must be a finite number from 0 to 1 and `grader_receipt_ref` / `independent_verifier` must identify the independently produced verdict. Unknown/incomplete rows have `grade=null`. A verified **full success** is grade 1; partial grades are not full successes.
- Resource vector: `provider_calls` (all attempts including failures), `total_tokens`, `quota_units`, `cost_usd`, `wall_seconds`, `human_minutes`; omit nothing silently: use JSON `null` for any unknown. Actual USD zero is permissible only with complete provider evidence; a free-tier label alone does not prove zero cost.
- `competence_edges` is a list of stable competence/skill/tool collaboration IDs, **not transient worker IDs** or provider routes. The absence of a connection can be meaningful: an isolated worker need not have any edges.

Optional host metadata such as signed evidence hashes and fault-injection descriptions is retained with host evidence outside the evaluator's deterministic scoring module.

### Run

```bash
fse ogi13 compare --observations evidence/ogi13/paired_observations.jsonl --require-complete > evidence/ogi13/paired_summary.json
```

This reads the exported rows, computes fixed/adaptive paired success, human effort, quota usage, wall time, calls, tokens and cost **per verified successful task**, and identifies exclusions and reporting gaps. With `--require-complete`, unmatched tasks, mismatched resources, missing receipts or incomplete grading return exit 1, with the report still printed.

## What a summary does and does not prove

- **Denominator is assigned paired tasks.** UNKNOWN/INCOMPLETE outcomes are treated as nonsuccess (and reported), not quietly excluded to inflate adaptive quality.
- **Resource-per-success uses the entire paired population** (successful + unsuccessful attempts). It is undefined if an arm has no verified success, any resource dimension is unavailable, or a required provider receipt is missing. No invented USD zero or hidden quota depletion.
- **"One added edge" subgroup is descriptive only.** Adding multiple edges, deleting a connection, or swapping a topology cannot isolate the contribution of a single edge. A cluster need not be fixed or round.
- **No causal claim is produced** by this report. Precommitted random allocation, cluster-aware uncertainty, official scorer versions and independence checks remain separate OGI-013 requirements.
- **Strings are not signatures.** A nonempty grader receipt reference does not prove its authenticity. `grader_provenance_attested=false` remains fixed until a separate independent verifier validates the original evidence. This tool never declares that OGI or AGI has been demonstrated.
- **Active policy not changed.** This analysis does not activate PlumMe Keras shadow recommendations, alter CherryMe cognition, build a new orchestrator, or write to canonical MangoMe/OrangeMe ledgers.
- **No frozen protocol rewritten.** No new benchmark task, cut-off, grade, sample size or pre-registered threshold is silently inserted into the existing F1/F3/A pilot.

## Minimum next steps for the local truth writer

1. Verify accepted GitHub source and actual VPS installations/hook wiring across **all** components. Ensure the canonical truth and `main`/`sync/local-truth` mirrors remain equal; preserve OGI-012.
2. Run the current product draft acceptance tests, including real child-call budget, Model/Skill policy and crash-safe effects; demonstrate one full MangoMe → PeachMe/CherryMe/PlumMe → PomeloMe/AppleMe → MangoMe/OrangeMe path with true receipts.
3. Freeze a separate OGI-013 benchmark-specific manifest and external grader for GAIA, tau2/tau3, SkillsBench, LongMemEval-V2 where legally/technically executable; prevent worker self-grading.
4. Alternate or randomize FIXED vs ADAPTIVE on the **same tasks and hardware/worker pool**, record supply drift and pre-specified budget ceilings. Preserve unknown/censored calls, verified worker replacement and fault/recovery evidence.
5. Export the paired rows and recompute the independent report. State actual n, completion coverage, usage completeness and negative results. Only a separately registered inference/ablation protocol can consider a causal or OGI claim.

## Governance

For FruitStack-Eval, the owner explicitly permits merging OGI-013 work into `main`, unlike product crown jewels. However the repository's accepted-state invariant additionally requires `LOCAL CANONICAL VPS == main == sync/local-truth`. A direct web commit before VPS parity is established would create an artificial G1 failure. The proposal can be developed/reviewed on the existing allowed `web/chatgpt` branch; a final accepted merge must keep the mirrors and the host source consistent. No force push or history rewrite.
