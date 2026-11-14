# C - OpenAI tool-use and eval docs (primary-source read, 2026-11-14)

Method: all 5 URLs fetched 2026-11-14 via WebFetch (page converted to markdown, then summarised by a small model; not raw HTML). All 5 resolved, no redirects or failures. Wording below is a faithful extraction; treat quotes as paraphrase of the page. None of the 5 pages states any measured benefit (token, latency, accuracy). Every "benefit" is qualitative ("may reduce"). Do not cite numbers from these pages.

## 1. Tool search (tools-tool-search)
Mechanism
- Model loads tool definitions only when needed; newly found tools are injected at the END of the context window to preserve the cached prefix.
- Responses API: only gpt-5.4 and later support `tool_search`. Add `{"type":"tool_search"}` to `tools`; mark functions (or an MCP server tool) `defer_loading: true`.
- Deferred function: model still sees name + description; mainly the parameter schema is deferred.
- Namespaces (recommended; models were trained on them): `{type:"namespace", name, description, tools:[...]}`. `defer_loading` applies to the functions inside, not the namespace. Mix of deferred/non-deferred allowed. Keep < 10 functions per namespace. Namespace/server description is what the model uses to decide what to load.
- Discovery: at start the model sees only names/descriptions of searchable containers; it issues a search, may load several namespaces/servers in one call (`paths` arg).
- Two modes: HOSTED (OpenAI searches tools declared in the request; known inventory) and CLIENT (`execution:"client"`, optional `description` and `parameters` schema; model emits `tool_search_call` and stops, app returns `tool_search_output` with same `call_id` + `tools`; for tenant/project-dependent discovery).
- Output items: `tool_search_call` (hosted: execution=server, call_id=null), `tool_search_output`, `function_call` (may carry `namespace`). `additional_tools` input item (role=developer) adds tools at a position in the conversation.
- Cache: changing/removing a loaded tool breaks the cache from that point; in client mode loaded tools persist across turns.
- Agents API: functions eager by default; need `tool_search` in agent.tools AND per-function `defer_loading`; MCP tools auto-deferred.
- Stated risks: extra discovery step; relies on model picking the right tool from names/descriptions; client-injected tool schemas must be validated, expose only trusted ones.
- Measured benefit: none. Docs say compare completion, input tokens, latency yourself.

## 2. Programmatic tool calling (tools-programmatic-tool-calling)
Mechanism
- Model writes JavaScript that orchestrates its tools: parallel calls, loops, conditionals, intermediate results held in the runtime, only a final `result` string returned.
- Runs in a fresh, isolated V8 runtime hosted by OpenAI (not your app, not a persistent container). Top-level await. No Node, packages, network, filesystem, subprocess, console, or state across runs. Client-owned function calls are still executed by YOUR app; it never runs the generated JS.
- Enable: `{"type":"programmatic_tool_calling"}` in tools; per tool `allowed_callers`: omitted/["direct"], ["programmatic"], or both. Code calls `tools.name({...})`.
- Contracts: `parameters` (JSON Schema) plus `output_schema` (shape of the JSON in `function_call_output.output`); both recommended so generated code can rely on fields. Unknown-shape tools should stay direct. Examples use strict:true, additionalProperties:false.
- Output items: `program` (code, call_id, opaque `fingerprint`), `function_call` with `caller.caller_id` = program call_id, `program_output` (`result`, status completed|incomplete). Client must echo `caller` unchanged on `function_call_output`; with store:false replay all items incl. reasoning (encrypted_content) in order; else previous_response_id. Handle `incomplete`.
- Supported tools: function, custom, mcp, apply_patch, local/hosted shell, code_interpreter. MCP require_approval can pause a program. tool_search is top-level only; deferred tools unavailable to a running program until loaded.
- Agents API: on by default; disable with enabled:false.
- ZDR needs org/project-level enablement (store:false alone is not enough).
- Not recommended for: single lookups, adaptive search where each result shapes the next step, writes / approval-sensitive actions, final citation validation. Recommends idempotent functions (replays/retries). App must still validate args/permissions per call.
- Model support not listed on the page (examples use "gpt-6-astra"; check the model page).
- Measured benefit: none; "can reduce intermediate output in context, depends on task". Compare correctness, evidence coverage, tokens, latency, cost, turns, retries, safety.

## 3. Agent evals / trace grading (agent-evals)
- Page is a thin decision/overview page. Trace = end-to-end record of one run (model calls, tool calls, guardrails, handoffs). Trace grading = graders score whole traces against structured criteria: right tool? handoff when needed? instruction/safety-policy violation? did a prompt/routing change help?
- Workflow: Dashboard Logs > Traces -> pick representative trace (SDK app or Agent Builder workflow, noted "transition window") -> create grader, run on selected traces -> refine prompts/tools/routing/guardrails. Then datasets + repeatable eval runs; advanced (external models, eval API, batch) lives in the separate Evals guide; Prompt optimizer uses a dataset.
- NOT stated on this page: grader types, span-level grading, grader independence from the agent, API shapes. Do not infer them; the Evals guide was not part of this task.
- Measured benefit: none.

## 4. Skills (tools-skills)
- Format: a directory with `SKILL.md` (front matter `name`, `description`; description = what + when) plus optional `references/`, `scripts/`, `assets/`. Follows the open Agent Skills standard (front matter validated). One SKILL.md per bundle.
- Upload: multipart files[] under one top-level folder, or zip (single top-level folder). Versioned: `default_version`, `latest_version`, `skill_reference.version` ("2"|"latest"); new upload may 404 briefly (poll GET version). Limits: zip 50 MB, 500 files/version, 25 MB uncompressed file, 32 capability dirs.
- Loading: hosted shell (`environment.type:"container_auto"`, `skills:[{type:"skill_reference",skill_id,version}]`; first-party ids like openai-spreadsheets); local shell (`type:"local"`, skills = name/description/path, no skill_reference); inline base64 zip via containers API; Agents API `capability_directories` on a self_hosted environment (harness scans for SKILL.md).
- Progressive disclosure: platform puts name+description+path into USER prompt context (not system prompt); model decides, then reads full SKILL.md, then linked files. Can force with "use the <name> skill".
- Security (stated): treat skills as privileged code; prompt-injection exfiltration risk; do not let end users attach arbitrary skills; approvals for writes/high-impact; review networking in shell guide.
- Measured benefit: none.

## 5. Remote MCP / connectors (tools-connectors-mcp)
- Remote MCP via `server_url` (Streamable HTTP, HTTP/SSE); private servers via Secure MCP Tunnel `tunnel_id`; legacy `connector_id` (Gmail, Drive, Teams, SharePoint, ...) deprecated for models released after 2026-09-01.
- Fields: type:"mcp", server_label, server_url, server_description, authorization (OAuth token; not stored by OpenAI, not in Response, resend every request), require_approval, allowed_tools, defer_loading.
- require_approval: default = approval before data is sent; "never" (whole server); "always"; per-tool `{"never":{"tool_names":[...]}}`. Flow: `mcp_approval_request` item -> new request with `mcp_approval_response` {approve, approval_request_id}; each approval covers ONE call.
- allowed_tools: import only named tools (cuts cost/latency for big servers).
- Listing: API fetches tools and emits `mcp_list_tools`; while that item stays in context there is no re-fetch (keep it in context for latency). Calls = `mcp_call` items (arguments, output, error, approval_request_id).
- defer_loading pairs with tool search (model sees server label + description only).
- Stated risks: prompt injection / data leak via URLs, server behaviour can change, third-party retention (store=true logs 30 days), prefer official servers, separate public-web and internal-data requests.
- Pricing: tokens only, no per-call fee. Rate limits 1000 RPM (Build), 2000 (Launch/Grow). Works with ZDR/data residency subject to server policy.
- Measured benefit: none.

## Classification
| Technique | Class | Hosted dependency |
|---|---|---|
| Tool search, deferred defs + namespaces | PROVIDER_INDEPENDENT (mechanism); hosted mode HOSTED_ONLY | Only the gpt-5.4+ trained behaviour and server-side search; client mode is already host-executed |
| Programmatic tool calling | PROVIDER_INDEPENDENT as a pattern; the OpenAI V8 runtime + `program` items are HOSTED_ONLY | Hosted V8, fingerprint/replay |
| Trace grading | Concept PROVIDER_INDEPENDENT; the dashboard/grader product HOSTED_ONLY | Logs>Traces, SDK tracing; independence/grader types undocumented here |
| Skills | PROVIDER_INDEPENDENT (SKILL.md is an open standard, we already use it); hosted skill_reference/versioning HOSTED_ONLY | Skills API, container_auto |
| MCP approval / allowed_tools | PROVIDER_INDEPENDENT (MCP is open; enforcement lives in the host) | Hosted MCP client only if using OpenAI-side calls |

## How our host/orchestrator could implement each (provider-agnostic, over MCP)
1. Tool search: host keeps a registry (name, one-line description, schema) per MCP server/namespace. Initial prompt lists only namespace names + descriptions plus ONE `tool_search(query|paths)` meta-tool. Search = BM25/embedding or exact path match; result = full schemas appended at the END of the message list (not the system prompt) to keep provider prefix caching; never remove loaded tools mid-session. Keep namespaces < 10 tools. Validate schemas from untrusted servers. Measure ourselves (completion, input tokens, latency): OpenAI gives no numbers.
2. Programmatic orchestration: expose tools to a sandboxed interpreter (WASM/QuickJS, Deno with no permissions, or a subprocess in a locked container) as `tools.*` stubs that RPC back to the host; host enforces per-call auth/approval, allowed_callers-style flag per tool (direct | programmatic | both), requires output_schema on programmatic tools, returns only the final result string to the model. Keep writes/approval-gated tools direct-only; make functions idempotent; log program text + every call as trace events.
3. Trace grading: record one structured trace per run (model calls, tool calls with args/results, approvals, handoffs, guardrail hits) in our own store; run graders offline as separate processes, ideally a different model/provider than the agent and with no access to the agent's scratch state, using deterministic checks first (tool choice, policy violations, schema validity), LLM-judge second; feed datasets of traces into regression runs. Independence must be designed by us; the OpenAI page does not document it.
4. Skills: keep SKILL.md directories; inject only name+description+path into the user-turn context, load body and references on demand through a read tool; version by directory hash or git tag; allowlist skills per workflow; treat as privileged (review, no open catalogue).
5. MCP boundaries: host-side policy layer in front of every MCP call: per-server `allowed_tools` filter applied at list time (cuts tokens and attack surface), per-tool approval policy (always | never-for-listed | default ask), one approval = one call, approval record (id, tool, args hash, decision) logged; cache the tool list per session and refresh on explicit version change; separate public-web and internal-data sessions; credentials injected by host, never passed through the model.

## Gaps / not verified
- Evals guide (grader types, independence, API) not read; do not assume.
- Model support for programmatic tool calling unlisted; "gpt-5.4+" for tool search is from the page, not independently confirmed.
- WebFetch summarised via a small model: exact field names are as reported there; re-check against the raw page before coding against them.
