# E - xAI Grok Build Workflows / Multi-Agent (primary sources, 2026-11-14)

Method: each URL fetched 2026-11-14 via WebFetch (page -> markdown -> small-model extraction; quotes are
as returned by that extraction, not re-verified against raw HTML). All 5 URLs resolved (no failure/redirect).
Classes: DEMONSTRATED = controlled measurement; REPORTED = vendor number, no method; PRODUCT_CAPABILITY = documented feature, no performance evidence.
Result: NO source contains a DEMONSTRATED claim. No benchmarks, ablations, or quality numbers on any page.

## 1. https://x.ai/news/workflows (dated Jul 23, 2026) - Grok Build Workflows

| Claim | Class | Section/notes |
|---|---|---|
| "fan a task out across hundreds of parallel agents, verify the results, and report back in one background run" | PRODUCT_CAPABILITY | intro; no measurement |
| Default budget 128 agents/run; max 1,024 for large jobs | REPORTED | numbers are budgets/caps, not performance |
| Grok "authors the workflow from your request" and smoke-checks it before launch; user does not write the script | PRODUCT_CAPABILITY | WHO DECIDES fan-out = the model (plan-time), bounded by agent budget; no stated criteria |
| Plan = "a small script: the phases of work, the agents in each phase, and how their results roll up"; demo phases Context, Review, Verify, Synthesize | PRODUCT_CAPABILITY | fixed-phase script generated per task; fan-out is therefore task-dependent but decided once up front, not shown to adapt mid-run |
| Each agent "starts with a clean, focused context"; "fan out specialist reviewers" | PRODUCT_CAPABILITY | independent contexts yes; how specialists are defined: not stated |
| Hierarchy | not described | phases + per-phase agents only; no manager/sub-manager tree |
| Skeptical review: "independent skeptics verifying every finding before it reaches the final report" (plan can include) | PRODUCT_CAPABILITY | optional plan element; no false-positive/recall evidence; skeptic independence beyond clean context not specified |
| Aggregation: final Synthesize phase -> "ranked report"; /deep-research "returns a cited report" | PRODUCT_CAPABILITY | schema of findings not documented |
| Durability: "Progress is saved as the run goes, so pausing and resuming never redoes finished work." Controls pause (p), stop (x), save (s) | PRODUCT_CAPABILITY | single sentence. Not stated: checkpoint granularity (per agent? per phase?), crash recovery, idempotency of side-effecting steps, treatment of in-flight agents at pause, storage location |
| Visibility: `/workflows` shows "live, phase by phase, with per-agent token counts" | PRODUCT_CAPABILITY | human TUI view; no stated machine-readable trace/API |
| Saved workflows: `.grok/workflows/` (team), `~/.grok/workflows/` (user); each is a slash command with args (`/pr-review 5137`) | PRODUCT_CAPABILITY | reuse of generated scripts |
| Demo readout: 0/128 agents, 12s elapsed, 8.42% context, label "Grok 4.5" | REPORTED | UI mock/demo value, not a measurement of anything |
| MCP, sandbox, pricing | not mentioned | only "Try Free" button + install curl; "session stays free" = session stays usable |

## 2. https://docs.x.ai/developers/model-capabilities/text/multi-agent - Grok Multi-Agent API (Beta)

| Claim | Class | Notes |
|---|---|---|
| Two configurations only: 4 or 16 agents. Param: `agent_count` (xAI SDK 4|16); `reasoning.effort` low/medium -> 4, high/xhigh -> 16 (OpenAI SDK/REST/Vercel) | PRODUCT_CAPABILITY | WHO DECIDES = CALLER picks count (coarse, fixed); server chooses roles/spawning, undocumented. Contrast with Workflows (model-authored, up to 1,024) |
| "multiple agents are launched to discuss and collaborate on your query"; "multiple agents may run in parallel" | PRODUCT_CAPABILITY | discussion topology unspecified |
| "A designated leader agent is responsible for synthesizing the discussion and presenting the final answer." | PRODUCT_CAPABILITY | flat leader + peers; leader = aggregator; no skeptic role named |
| Server runs the agent loop for built-in tools (web_search, x_search, code_execution, collections_search) and remote MCP | PRODUCT_CAPABILITY | client-side function calling and custom tools NOT supported |
| VISIBILITY default: only leader's tool calls + final response returned. Sub-agent state (intermediate reasoning, tool calls, outputs) is ENCRYPTED, returned only with `use_encrypted_content=True` (xAI SDK) | PRODUCT_CAPABILITY | encrypted = opaque to caller (round-trip/continuation use, not inspection); no per-agent plaintext trace documented |
| Reasoning tokens: count via `usage.reasoning_tokens`; streaming `include=["verbose_streaming"]` shows "Thinking..." token count; reasoning text not shown | PRODUCT_CAPABILITY | count only |
| Beta; behaviour may change; model `grok-4.20-multi-agent`; Chat Completions unsupported; `max_tokens` unsupported; multi-turn via `previous_response_id` | PRODUCT_CAPABILITY | note: no caller-side output cap |
| Billing: all leader + sub-agent input/output/reasoning tokens and server tool calls billed; 16-agent "significantly more tokens" than 4 | PRODUCT_CAPABILITY (pricing) | no $ rates, no multiplier given; points to Pricing pages |
| Latency/scheduling/resource numbers; quality gain vs single agent | none stated | nothing to classify |

## 3. https://docs.x.ai/developers/tools/remote-mcp
- Params: `server_url` (req; "Only Streaming HTTP and SSE transports"), `server_label` (req; prefixes tool calls), `server_description`, `allowed_tools` (native SDK: `allowed_tool_names`), `authorization` (token -> Authorization header), `headers` (`extra_headers`). PRODUCT_CAPABILITY.
- Without `allowed_tools`, all server tool definitions are injected into model context; allowed_tools = allowlist (context reduction / restrict to read-only ops). Allowlist is the ONLY documented boundary.
- Approval: NONE. "The `require_approval` and `connector_id` parameters in the OpenAI Responses API are not currently supported." So no human-in-the-loop gate on MCP calls; the server executes them autonomously (server-side loop).
- Visibility: streaming shows server-side tool calls (name+args) live; `response.tool_calls`, `usage`, `server_side_tool_usage`. Not stated whether tool results are shown.
- No numeric limits, timeouts, error semantics, rate limits documented. Advice: HTTPS + auth on MCP server.
- Combined with Sec.2: in multi-agent mode a sub-agent's MCP calls fall inside encrypted sub-agent state unless leader-visible (inference, not stated).

## 4. https://docs.x.ai/developers/tools/code-execution
- Python only; "most popular" packages (NumPy, Pandas, Matplotlib, SciPy) pre-installed.
- "No access to external networks or file systems"; "Limited file system access"; "Temporary execution context that doesn't persist between requests." (PRODUCT_CAPABILITY; isolation strength/technology unspecified.)
- Timeouts and memory limits: no values ("may have execution time constraints", "might hit memory limitations").
- Code/output visibility: page does not say; streaming example shows server-side tool calls; outputs only evidenced via final text. No pricing on page.
- Implication: no state persistence between requests => cannot serve as a durable workspace for resumed workflows.

## 5. https://docs.x.ai/developers/advanced-api-usage/async
- This is client-side concurrency, NOT a deferred/resumable job API. `AsyncClient` (xai_sdk) / `AsyncOpenAI`; semaphore-style cap `max_concurrent` (default 2 in example) / `max_in_flight_requests=2`; cannot exceed console rate limits (values not on page). Scale mention "hundreds or even thousands of requests".
- Long timeout 3600 s recommended for reasoning models (examples).
- Deferred work: only a pointer to the Batch API ("queue the requests and fetch them later"), linked to /developers/advanced-api-usage/batch-api, NOT fetched/described here (not in assigned list; unverified).
- Polling, resumability, idempotency keys: explicitly not mentioned.
- No latency numbers anywhere. Multi-agent doc does not say whether multi-agent requests can use background/batch.

## 6. Documented mechanics vs marketing (skeptical read)
- "Hundreds of agents", "verify", "never redoes finished work" are assertions. Only concrete, checkable items: 128/1,024 budgets, 4/16 agent counts, encrypted sub-agent state, MCP allowlist, no require_approval, sandbox no-network/non-persistent.
- Two distinct products with different control: Workflows = CLI feature (model-authored script, up to 1,024 agents, human TUI trace); Multi-Agent API = server-side leader+peers (caller picks 4/16, opaque). Do not conflate; docs do not say Workflows are built on the multi-agent API. Model names inconsistent across pages (Grok 4.5 demo label, grok-4.20-multi-agent, grok-4.7 in async example) - unreconciled.
- Zero evidence that parallel/skeptic/leader structures beat a single model at equal compute; token billing for all agents implies cost scales with agent count.
- Extraction was by a small model summarizer; before relying on a quote for a decision, re-read the raw page.

## 7. Provider-independent mechanisms worth comparing
Host baseline: durable step ledger (idempotent steps, UNKNOWN reconciliation), model scheduler with per-model competence, Brother-Mode generate/critique/revise, hash-chained evidence ledger. What each mechanism would still be missing:

1. Model-authored task-dependent fan-out plan (phases/agents/rollup script, budget-capped 128/1,024).
   Host missing: a planner step that emits a typed phase DAG per task (not just per-step model choice); an agent-count budget as first-class resource; an eval showing planned fan-out beats fixed fan-out. xAI itself gives no such eval.
2. Clean-context independent specialists.
   Host missing (if Brother-Mode critique shares transcript): enforced context isolation per critic (no leader transcript), plus a measured independence check (do critics agree for the right reasons). xAI documents isolation, not its effect.
3. Dedicated skeptic phase verifying EVERY finding before synthesis.
   Host missing: per-finding verification as a mandatory gate (claim-level, not answer-level critique), with the verdict recorded per finding in the evidence ledger; skeptic-vs-generator model diversity chosen by the competence scheduler.
4. Leader/synthesizer aggregation (Multi-Agent API) and Synthesize phase.
   Host missing: structured finding schema (claim, evidence ref, verifier verdict, confidence) so aggregation is deterministic and auditable rather than prose; xAI documents neither.
5. Pause/resume "never redoes finished work".
   Host mostly ahead (idempotent steps, UNKNOWN reconciliation). Gap to check: pause of in-flight fan-out (cancel vs drain), partial-phase resume, and resume across a changed plan. xAI discloses none of this, so there is nothing to copy; host should not assume parity claims are real.
6. Opaque encrypted sub-agent state (caller sees leader only).
   Host missing: nothing; this is a counter-example. A hash-chained ledger needs plaintext per-agent outputs to hash; xAI's encrypted blobs cannot be audited by the caller, so provider multi-agent output can only be ledgered as one opaque step (final answer + usage + token counts), classified UNVERIFIABLE internally. Host should record the encrypted blob hash for replay but not treat inner reasoning as evidence.
7. Per-agent live token counts in a phase view (/workflows).
   Host missing: per-agent cost/token attribution in the ledger (xAI Multi-Agent API gives only aggregate usage; Workflows gives it only in a human TUI).
8. MCP allowlist with no approval gate.
   Host missing: an effect-class policy (read-only vs mutating) enforced host-side, since the provider offers allowlist only and server-side loop executes without approval; any mutating MCP tool via xAI is un-gated.
9. Ephemeral no-network sandbox.
   Host missing: durable workspace/artifact capture of sandbox outputs into the ledger before the context vanishes (nothing persists between requests).
10. Saved workflows as slash commands (.grok/workflows).
   Host missing: versioned, hash-pinned workflow definitions replayable for evaluation; xAI saves scripts but states no versioning.
11. Async/batch.
   Host missing: nothing proven; xAI async page is just client concurrency (default 2 in-flight) + 3600 s timeouts; Batch API unverified. Scheduler should treat provider rate limits as unknown until measured.
12. Cost control: all agents billed, no `max_tokens` on multi-agent API.
   Host missing: hard per-step token/cost ceiling enforced on the host (provider cannot cap multi-agent output).

Net: xAI offers capabilities, not evidence. The comparable value is design vocabulary (plan-as-script, per-finding skeptics, budgeted fan-out) to test against the host baseline, not performance claims to import.
