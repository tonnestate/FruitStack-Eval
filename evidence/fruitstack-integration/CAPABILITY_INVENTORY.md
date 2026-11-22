# FruitStack capability inventory (read-only reconnaissance, 2026-11-07)

Method: repository state, source reading and greps in the actual checkouts; execution evidence is taken from already archived OGI-013 evidence and **not re-run**. No provider call, no test suite run, no repository changed. "Not verified" means I did not inspect it.
Status scale: DECLARED (only stated) < IMPLEMENTED (code exists) < INTEGRATED (wired into a runtime path that calls it) < EXECUTED (archived run shows it working in that path). None of these is scientific proof.

## 1. Components

| component | checkout (branch @ head, dirty files) | version | status | basis |
|---|---|---|---|---|
| CherryMe (Brother Mode, engine, RG/2, KnowledgeStore, appleme_bridge) | `fruits/integration/ogi013-cherry-org` (ogi013-org-cherry @ 33c3d77, 5 dirty); `/root/CherryMe` is the root repo, not the component | n/a | Brother Mode INTEGRATED+EXECUTED (S1, QA-2D, tau2 pilots); KnowledgeStore IMPLEMENTED, not in runner path | `brother.py`, eval runners import it (10 files), S1/QA-2D evidence |
| PlumMe (supply, AUTO routing, receipts, DecisionLog) | `SUPPLY-001/wt/PlumMe` (cc/sp-repair-001 @ 7e36b2c, 6 dirty); prod install per memory 0.1.11 | n/a | INTEGRATED+EXECUTED | receipts/lineage identities used in every study row |
| PeachMe (session harness, budget governance, hooks) | `fruits/sync/PeachMe` (main @ 1bc90f8, 1 dirty) | 0.8.3 | IMPLEMENTED; INTEGRATED in the tau2 agent path (`FruitStackSession`, Mango/Orange/Cherry/Apple adapters); EXECUTED there (C1/C2 airline tests); NOT in the multiple-choice Brother Mode path | `fruitstack.py`, `claude_hooks.py`, eval `ogi013_tau2_agent.py` |
| AppleMe (deterministic trajectory health: dead, loop, stalled, thrashing, repeated error/output) | `fruits/sync/AppleMe` (sync/local-truth @ 8dfc33f, 3 dirty) | 0.1.2 | IMPLEMENTED with tests; INTEGRATED via `cherryme.appleme_bridge` in tau2 agent and `pilot_inquiry`; EXECUTED in the tau2 pilots (per archived protocols, not re-verified); NOT applied to Brother Mode/QA transcripts. Cognitive-trajectory signals (circular reasoning, ignored evidence, artificial consensus) not implemented as far as inspected (detectors are heartbeat/action/error oriented; engine internals not fully read) | `appleme/engine.py`, tests/test_trajectory_health.py |
| MangoMe (work identity, checkpoints) | `/root/MangoMe` (fix/claude-local-scope @ 1edeaa3, 18 dirty); pinned copy `ogi013-mangome-pinned` | 0.1.9rc4 | INTEGRATED+EXECUTED: every QA-2D/S1 episode writes TEAM_* checkpoints through `MangoLedger` | eval `ogi013_mango_ledger.py`, run ledgers |
| OrangeMe (memory/ChatLedger/Project-Ledger) | `SUPPLY-001/wt/OrangeMe` (main @ 953e725, clean) | 0.1.1 | INTEGRATED+EXECUTED as per-episode memory ledger (QA-1/S1 `OrangeRuntime`, tau2). History retrieval as organizational knowledge for later tasks: spec only (`evidence/ogi013-phase2/CHERRYME_MEMORY_SPEC.md`), not wired | eval `ogi013_qa1.py`, `ogi013_tau2_agent.py` |
| PomeloMe (effects, authority/budget envelopes, `EffectClass` READ/IDEMPOTENT_WRITE/COMPENSATABLE/IRREVERSIBLE) | `tonnestate-repos/PomeloMe` (main @ b62f64b, 2 dirty) | 0.1.0 | INTEGRATED in the code-task arm (`ogi013_host_composer.py`, `ogi013_code_task.py`); EXECUTED: not verified | eval runners |
| PhysalisMe (analytical MCP, 7 tools, typed claim gate) | `/root/PhysalisMe` (feature/analytical-mcp-v0.1 @ 6fce868, clean, **no main branch**) | 0.1.0 | IMPLEMENTED only. Zero imports in eval runners, **not registered** in Claude or Codex MCP config. Its README states no real CherryMe -> PeachMe -> MCP -> MangoMe chain exists | repo README ("Next implementation targets") |
| BananaMe (controlled repo mutation) | `tonnestate-repos/BananaMe` (main @ aa68979, 3 dirty) | 0.1.2 | IMPLEMENTED; no integration found in the eval path | 0 imports |
| BlueberryMe (privacy/egress) | `tonnestate-repos/BlueberryMe` (main @ 23a8e68, 3 dirty) | 0.3.0 | IMPLEMENTED; no integration found in the eval path | 0 imports |
| StrawberryMe | `.graphify/repos/tonnestate/StrawberryMe` (main @ 2a55474, 2 dirty) | 0.4.1 | INTEGRATED as an MCP server (Claude and Codex configs); not part of OGI runs | `claude.json`, `config.toml` |
| CogC | `/root/CogC` (main @ 0934376, 5 dirty) | 0.2.1 | IMPLEMENTED, installed as skill; EXECUTED in some earlier dev runs (cherry-events); not in S1/QA-2D (audit 2026-11-02) | architecture audit |
| SPARI | `tonnestate-repos/SPARI` (main @ 1e3bcec, clean) | n/a | installed skill; no runner integration | 0 imports |
| DragonFruitMe, PorcelainberryMe | `.local/share/tonnestate-mcp/dragonfruitme` (a copy of the root repo state, not a component checkout); `/opt/porcelainberryme` 0.1.0 | | not assessed; relevance undetermined | existence only |
| **LSD Room (4 perspectives) and Research Tree** | none | | **DECLARED only**: no implementation, spec or test found in CherryMe worktree, eval repo, contracts, integration research dirs, PhysalisMe or memory | greps |
| **Autonomy policy (AUTONOMOUS / HUMAN APPROVAL REQUIRED / BLOCKED)** | none | | **missing as one runtime policy**. Ingredients exist: PomeloMe `EffectClass` + `AuthorityEnvelope` + `BudgetEnvelope`; PeachMe restrict-only PreToolUse hook (`claude_hooks.py`: denies effectful tools when session not ACTIVE; never grants) and `PEACH-VIRTUAL-1` advisory dispositions; BlueberryMe egress; AppleMe health | source reading |

Repository hygiene found: most checkouts carry uncommitted edits of other sessions (CherryMe 5, MangoMe 18, PlumMe 6, CogC 5, ...). Changes to them must go through branches/PRs, not direct edits.

## 2. The 16-step lifecycle against the evidence

| step | status |
|---|---|
| 1 MangoMe mission/work identity | EXECUTED (eval runs) |
| 2 OrangeMe historical context | EXECUTED as episode memory; history retrieval for new work NOT integrated |
| 3 CogC compilation | IMPLEMENTED, not in the path |
| 4 CherryMe decomposition / strategy | partial: Brother Mode and RG/2 responsibilities EXECUTED; research strategy, hypotheses tree, LSD: DECLARED |
| 5 PlumMe supply | EXECUTED |
| 6 Brother Mode | EXECUTED, outcome evidence insufficient (see `evidence/ogi013-research-status/`) |
| 7 PeachMe boundaries | INTEGRATED+EXECUTED in tau2 path only |
| 8 workers research/criticize/revise | EXECUTED (multiple-choice and tau2) |
| 9 PhysalisMe evidence | IMPLEMENTED only |
| 10 AppleMe diagnosis | INTEGRATED+EXECUTED in tau2 path only |
| 11 CherryMe decides continue/finalize | EXECUTED (CooperationControl, corrected) |
| 12 BananaMe / PomeloMe effects | PomeloMe INTEGRATED in the code arm; BananaMe not |
| 13 StrawberryMe/assurance | StrawberryMe available as MCP, not in the loop |
| 14 MangoMe records | EXECUTED |
| 15 OrangeMe knowledge for future work | NOT integrated (ledger/LearningHook baseline exists, no runner) |
| 16 learning from verified outcomes | IMPLEMENTED offline (ledger, structure learner); no real reuse measured |

## 3. Consequences for the work order

The real gaps, in dependency order, are: (a) a single runtime autonomy decision policy composed from existing ingredients; (b) PhysalisMe made reachable (merge, register, PeachMe classification of its tools as read-only analytic, receipts into MangoMe); (c) a first real non-frozen driver that passes `learning=` and uses OrangeMe/MangoMe for retrieval; (d) AppleMe on Brother Mode transcripts; (e) LSD Room / Research Tree, which do not exist and need a design decision before code.

Nothing here claims scientific support for EVAL-001/002/003.
