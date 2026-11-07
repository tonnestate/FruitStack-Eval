# CherryMe cognitive memory — implementation-ready specification for the next milestone (CM-MEM/1)

Status: specification only; nothing here is implemented or changes the running evaluation. It extends existing CherryMe, it does not add a competing memory system.

## 1. What exists and is reused (verified by file inspection, 2026-10-29)
| need | existing component | use |
|---|---|---|
| durable claims, lookup | `cherryme/knowledge.py` `KnowledgeStore` (publish / records / lookup = lexical token overlap, min_overlap 0.34), `KnowledgeFirstGrounder` | stays the **system of record** for verified claims; its `lookup` becomes the lexical leg of retrieval |
| orchestration | `cherryme/ensemble.py` ACE/1 (`choose_ensemble`, `EnsembleDecision.truth_authority = False`), `responsibility.py` | decides WHICH worker structure; retrieval results enter as context sources, never as decisions |
| verification, completion | `verification.EvidenceVerifier` (quorum), `completion.CompletionInspector`, `engine.normalize_provenance`, `models.Claim/Evidence` | the only path by which a retrieved item may become a verified claim |
| canonical work graph | MangoMe `work_identities`, `edges(from_id,to_id)`, `claims`, `evidence`, `work_checkpoints`; `checkpoint_work`, `submit_evidence`, `claim_done` | node/edge source for GraphRAG; read-only for retrieval |
| shared ledgers | OrangeMe `ProjectLedger.get/put(expected_revision)`, `ChatLedger.read(since)` | revision-stamped memory; every index entry records the ledger revision it was built from |
| execution context | PeachMe `FruitStackSession.context()` → frozen `ContextView`, `CherryBrainAdapter.claim_texts`, **egress gate `authorize_model_input`** | the single place where retrieved text may reach a model |
| supply | PlumMe routes incl. `Modality.EMBEDDING` offers, `DecisionLog`, `record_decision_feedback` | embedding/rerank calls go through PlumMe like any other dispatch (budget, receipts, lineage) |
| learning gate | `runners/train_org_policy.py` (Keras ensemble vs baselines, bootstrap CI, ECE, conformal, attestation; "a verdict only permits") and `ogi013_org_learning.py` (VERIFIED outcome join) | template for the retrieval-learning gate; no embedding/reranker training exists yet |
Not present anywhere (greenfield): BM25, dense/hybrid retrieval, reranker, GraphRAG, vector index.

## 2. Principles (non-negotiable)
1. **Retrieval is advisory.** Every hit carries `{source, locator, ledger_revision, provenance, authority: CANDIDATE}`; only `EvidenceVerifier`/`CompletionInspector` produce VERIFIED claims. Retrieval never writes to `KnowledgeStore`, MangoMe or OrangeMe.
2. **Indexes are rebuildable caches.** Truth stays in KnowledgeStore / MangoMe / OrangeMe; deleting an index loses nothing. Each entry stores the source revision; a changed revision marks it STALE and excludes it unless refreshed.
3. **One egress path.** Retrieved text enters a prompt only through `authorize_model_input`; the context is bounded by the step's token authorisation (the same ParentBudget that bounds the step).
4. **Same supply, same accounting.** Embedding and rerank requests are PlumMe dispatches (receipts, lineage, zero-cash policy); a local embedding model is a LOCAL-cost route, not a second stack.
5. **Learning only through the gate.** A learned retriever/reranker may be used only when an ORG-GATE-style attestation (held-out, calibrated, CI above a baseline) permits it AND the owner activates it; the default is the non-learned hybrid.

## 3. Components (modules under `cherryme/memory/`, all optional imports)
- `corpus.py` — `MemoryItem(id, text, source_kind ∈ {KNOWLEDGE, WORK, EVIDENCE, LEDGER, CHAT}, locator, revision, provenance, tags)`; `iter_items(sources) -> Iterator[MemoryItem]` reading KnowledgeStore.records(), MangoMe work/evidence/claims (read API only), OrangeMe ledger values and chat. Deterministic ids = sha256(source_kind|locator|revision).
- `lexical.py` — BM25 (stdlib) over MemoryItem text; replaces nothing: `KnowledgeStore.lookup` remains the compatibility path.
- `dense.py` — `Embedder` protocol (`embed(texts) -> list[vector]`) with two implementations: `PlumMeEmbedder` (EMBEDDING-modality route via the PlumMe service) and `LocalEmbedder` (optional, e.g. a small sentence model; absent = dense leg disabled). `VectorIndex` protocol with an in-memory/numpy brute-force default and an OPTIONAL local file index (sqlite-vec or hnswlib) behind the same protocol.
- `graph.py` — `GraphView` built from MangoMe `edges`/`claims`/`work_identities`: k-hop expansion from seed items (claim ↔ evidence ↔ work ↔ checkpoint), edge types preserved; GraphRAG = hybrid seeds + bounded expansion (max_hops, max_nodes) + path provenance.
- `retrieve.py` — `retrieve(query, *, budget, filters, mode="hybrid") -> RetrievalResult(hits, trace)`: lexical top-k ∪ dense top-k ∪ graph expansion → reciprocal-rank fusion → optional reranker → token-budgeted packing. `trace` lists each leg, scores, dropped-for-budget items and STALE exclusions (auditable).
- `rerank.py` — `Reranker` protocol; default none; Keras reranker (below).
- `learn.py` — builds training rows from VERIFIED outcomes only: (query context, retrieved item ids, per-item use in the verified-correct action ← from `record_decision_feedback` / `attribute_episode_outcome`), splits by task (registered hash split), trains (a) a Keras embedding-adapter/reranker and (b) compares with BM25/dense baselines; writes an attestation with held-out nDCG@k / recall@k, calibration, bootstrap CI; verdict PERMITTED / INSUFFICIENT / NOT_BETTER. Never activates anything.
- `adapter.py` — `MemoryContextAdapter` for PeachMe: `context_sources(view) -> list[ContextSource]` consumed by CherryMe's `ContextCompiler`, passing the egress gate.

## 4. Interfaces (stable)
`retrieve(query: str, *, budget_tokens: int, filters: dict|None, mode: Literal["lexical","dense","graph","hybrid"]="hybrid") -> RetrievalResult`; `RetrievalResult.hits: list[Hit(item: MemoryItem, score: float, legs: dict, path: list|None)]`;
`index.sync(sources) -> SyncReport(added, stale, removed)` (idempotent; revision-driven); `attest(rows, gate_json) -> Attestation`. No function mutates a source of record.

## 5. Milestones and acceptance tests
- **M1 lexical + hybrid skeleton (no model):** corpus adapters, BM25, RRF, packing, trace, staleness. Accept: deterministic results on a fixed corpus; STALE items excluded after a ledger revision change; every hit has full provenance; zero writes to sources (asserted by read-only fakes).
- **M2 dense leg through PlumMe:** `PlumMeEmbedder` with budget/receipt accounting, optional local index. Accept: embedding dispatches appear in receipts under the zero-cash policy; index rebuild equals incremental sync; dense disabled ⇒ lexical results unchanged.
- **M3 GraphRAG over MangoMe edges:** bounded k-hop expansion with path provenance. Accept: expansion respects max_hops/max_nodes; no edge crosses an authority boundary (items without read authority are never returned).
- **M4 learning gate:** Keras reranker/embedding adapter from VERIFIED outcomes; held-out by task hash split; attestation like ORG-GATE/1. Accept: with insufficient rows the verdict is INSUFFICIENT and the default path is untouched; a permitted verdict still changes nothing until the host activates it.
- **M5 evaluation inside the OGI baseline (after OGI-013 is established):** A/B on retrieval-sensitive tasks with the official benchmark and the COLLAB-1-style decision metrics; report recall@k, decision quality, cost (requests/tokens) — a null result is reportable.

## 6. Failure and safety behaviour
Index unavailable ⇒ fall back to `KnowledgeStore.lookup`, record `degraded=true` in the trace. Embedding route unavailable/rejected ⇒ dense leg skipped, counted as a failed dispatch, never retried beyond the step's request budget. Over-budget packing ⇒ drop lowest-ranked, never truncate mid-item. Conflicting items ⇒ both returned with their provenance and revisions; the verifier decides, retrieval does not.

## 7. Out of scope
Replacing KnowledgeStore, any new database or orchestration engine, automatic activation of learned components, changes to MangoMe/OrangeMe schemas, anything touching the C3 or COLLAB-1 evaluations.
