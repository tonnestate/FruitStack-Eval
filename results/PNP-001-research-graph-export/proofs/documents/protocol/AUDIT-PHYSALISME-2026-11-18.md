# Audit: why FruitStack does not exploit PhysalisMe (director, 2026-11-18, evidence-based)

Scope: staging lab used by the PNP-001 campaigns (socket `.../scratchpad/staging/mcp.sock`, server PID 2582942, source
`/root/fruits/integration/physalis-mathverify`), live lab `physalisme-mcp.service` (`/run/physalisme/mcp.sock`, PHYSALIS_MAX_CONCURRENCY=4),
campaign loop `/root/fruits/integration/Aurora-sync/integration/pnp_research.py`, desk `pnp_desk.py`, PlumMe `src/plumme`, CherryMe
`cherryme/claim_check.py`. F = observed fact (command/log cited), I = inference.

## 1. Capability inventory (summary)
- F: `physalisme/server.py` registers **60 MCP tools** (`grep -c @mcp.tool`), incl. synchronous (`physalis_code_run`, `physalis_sat_solve`,
  `physalis_math_evaluate`, `physalis_ml_experiment`, `physalis_model_fit/explain`, `physalis_dataset_from_code`, `physalis_exact_law_search`,
  `physalis_representation_experiment`, `physalis_replay_experiment`, `physalis_review_experiment`, `physalis_challenge`, ...) and asynchronous
  ones (`physalis_task_start/status/cancel/verdict`: leased, cancellable, checkpointed background tasks; methods discovery_run, refinement_study,
  algo_evaluate, exact_law_search, symbolic_search, pipeline_search).
- F: not registered in PomeloMe (no `physalis` reference in any PomeloMe tree).
- F: access = Unix socket, root/www-data (`srw-rw---- root www-data /run/physalisme/mcp.sock`). Callers: host processes (campaign loop, desk,
  CherryMe `claim_check.py`/`math_mcp.py`, Aurora mission workers). UNVERIFIED: per-agent authorization inside AnanasMe missions.

## 2. MCP accessibility from the research agents' context
- F: research agents are PlumMe workers called via `plum_work` / `run_neuron` (pnp_invent.plum, pnp_research.implement). PlumMe has no
  tool-call execution loop (`grep tool_calls src/plumme/*.py` -> only knowledge.py; `allowed_tools` exists in models/scheduler but no role
  config grants any). **Agents cannot discover or invoke any PhysalisMe tool.** Their only lab channel: Python text that the loop runs via
  `physalis_code_run`.
- F: the agent prompts in pnp_research.py contain **no PhysalisMe tool name** (grep). The campaign loop itself calls 1 tool
  (`physalis_code_run`); desk/pnp_invent additionally `physalis_task_start`, `physalis_algo_*`.
- F (live test, same call path as campaigns): inside the sandbox `sklearn`, `shap`, `pysat`, `networkx`, `sympy` import; `tpot` does not;
  `physalisme.circuits` and `physalisme.discovery` do NOT import (sandbox package lacks the lab's own algorithms); the lab data dir is NOT
  readable (`PermissionError`); INPUT holds only what the loop passes (a ~786-instance sample + campaign data such as gal_data.json).

## 3. Duplication (stored experiment programs, `state/codemode/code/*.py`, 140 programs)
- F: 73 define their own modular rank / Gaussian elimination; 45 re-implement satisfiability by enumerating 2^n assignments; 3 their own MUS
  enumeration; **0 import physalisme**; 1 uses pysat, 1 sklearn, 1 shap. Median program 135 lines.
- F (director): exact computations of the day (2^20 n=6 universe, n=7 cores, Smith-form searches, mod-9 check, circuit orbits) were run as
  standalone scripts in `lab/slice`, `lab/circuits` outside the lab - same pattern.
- I: cause is not agent ignorance alone - the lab's functions and datasets are physically unreachable from the sandbox (§2), and nothing in
  the prompts says they exist.

## 4. Background engine (09:44-13:49)
- F: it was the existing **desk** (`pnp_desk.py`, owners `PNP-001/desk/A0001..A0029`), not an autonomous lab loop: 29 discovery_run tasks
  (20 EVALUATED: verdicts USEFUL/REDUNDANT; 9 FAILED: 9 "worker process vanished", 6 "exhaustive enumeration bounded to n <= 6", 3 lease
  expired, 3 superseded).
- F: stopped because its generator `seed_from_evidence` (pnp_desk.py:255) is a **fixed grid** of 4 family sets x 3 targets, sizes [5,6],
  seed 42: exhausted -> `queue: 0, running: 0` from 13:49 to 20:00 (desk.log), then the desk process hit its 30000 s timeout.
- F: verification queue: **29 laws PENDING** (e.g. "For formulas with m=4: sat = cons3", "null2=0: sat = 0") - by design laws about all n
  wait for a PI review that never came (pnp_desk.py:315-318: only finite claims are auto-submitted); 2 finite claims sent to CherryMe via
  Aurora missions ended UNSETTLED.
- F: the director's `pnp_compute_lane.py` (built 21:3x, stopped at owner order) **duplicated the desk's scheduling responsibility**; it ran
  4 tasks concurrently (load 7.1/8) - proving capacity, not a missing component.

## 5. Shared data
- F: datasets exist (`data/`: 19 CSVs, desk registry of 11 datasets; discovery ledger 1092 entries; experiments log with result per run)
  but are not queryable by agents: not mounted in the sandbox, not passed in INPUT, and (until today's digest change) not in the campaign
  digest. No Problem x Instance x Representation x Algorithm store that experiments write into; each program returns a JSON blob.

## 6. ML / AutoML (installed / implemented / exposed / executed / utilized)
| capability | installed | implemented in lab | exposed to agents | executed | scientifically utilized |
| scikit-learn | yes 1.9.1 | yes (ml_experiment, discovery automl) | no (sandbox import only) | yes: discovery_run automl this morning (169 ML_SUPPORTED ledger entries); campaigns: 1 of 140 programs | no evidence any campaign used it |
| SHAP | yes | model_explain | no | UNVERIFIED in discovery runs | no |
| TPOT2 | NO | - | - | no | no |
| feature engineering | - | discovery features (measure) | no | yes (desk runs) | not consumed |
| clustering / anomaly | UNVERIFIED | UNVERIFIED | no | no evidence | no |

## 7. Feedback-loop trace (one real finding)
"For formulas with m=4: sat = cons3" (lab discovery, desk A00xx): lab experiment -> exact dataset -> exact law search -> CONJECTURED ->
verification queue -> submitted to CherryMe (Aurora mission) -> UNSETTLED -> no hypothesis, no follow-up, never seen by D-014/ATLAS/GAP.
Break points: (a) verification mission inconclusive, (b) no route from desk findings into the campaigns, (c) PI review step manual.
The campaign side shows the reverse: GAP's GF(3)-blindness questions were answered by director scripts (D-018, D-023, D-024), not by lab
tools, and agents re-asked settled questions until the digest was fixed (c4e36d5).

## 8. Concurrency and ownership
- F: lab capacity: live service PHYSALIS_MAX_CONCURRENCY=4; staging handled 4 concurrent tasks + 2 code runs; one live task PER OWNER
  (tasks.py:98, idempotency). Campaign loops: one synchronous code_run per ~7-min LLM cycle (lab busy 18.7% of 6 h, 0.19 cores mean).
- Ownership as built: scheduling of background lab work = desk (fixed grid); hypothesis selection = campaign loops (LLM); lab execution =
  PhysalisMe; verification = CherryMe via Aurora missions (finite) + PI (laws, manual); model allocation = PlumMe; supervision = AppleMe.
  Two disconnected task systems: desk (lab tasks, no LLM hypotheses) and campaigns (LLM hypotheses, no lab tasks).

## 9. Root causes (verified)
1. Agents have no tool access: PlumMe workers are text-only; PhysalisMe's 60 tools are unreachable for them (§2).
2. The single channel (code_run sandbox) exposes neither the lab's algorithms nor its datasets (§2, §5) -> mass re-implementation (§3).
3. Two disconnected loops: the desk owns lab background work but its experiment generator is a hard-coded grid that ran out (§4); the
   campaigns own hypotheses but cannot submit lab tasks. Nothing connects campaign hypotheses to desk assignments.
4. Lab findings do not flow back: desk/discovery results never reached the campaigns (digest) and 29 conjectures wait on a manual PI step.
5. Verification is centralized by design: laws need PI review; CherryMe's executed checks (claim_check RECOMPUTE / physalis_math_evaluate)
   cover arithmetic claims, not lab recomputations; lab replay/review/challenge tools are unused.

## 10. Minimal corrective actions (ranked by scientific impact; none built yet)
1. Connect, don't add: let campaigns ENQUEUE desk assignments (desk already schedules, leases, verifies) instead of my lane - replaces the
   desk's fixed grid with campaign-proposed discovery/law-search parameters. (Retire pnp_compute_lane.py.)
2. Make the lab's own building blocks importable in the sandbox (circuits, discovery.measure/generate, exactlaws) and expose its datasets
   read-only to code_run (or pass dataset ids) - removes the 73/45 re-implementations.
3. Tell the agents what exists: a compact capability brief (tool names, dataset ids, importable functions) in the implementer/proposal prompt,
   generated from the server's own tool list - not a fixed experiment list.
4. Route lab-verifiable claims to the lab's replay/review/challenge tools automatically; keep only proofs and "does it bear on general
   computation" for the director; clear the 29 PENDING laws by classifying them (finite-checkable -> lab; general -> proof obligation).
5. Install TPOT2 only if ML is actually routed (2) - otherwise it stays an unused dependency.
