# e2e_offline_2026-11-07_v2 — OFFLINE / SCRIPTED

**Label:** offline fixture. The provider texts behind PlumMe are scripted (fixed answer per task, identical in applied and control runs) through PlumMe's public
`ProviderAdapter` interface (no PlumMe `tests/` import). Every other component runs its real code path. This is evidence that the integrated path executes and records
what it did. It is **not** evidence of model capability or organizational gain.

Command: `python runners/fs_fullstack_e2e.py OUT` (= `fs_runtime.py --config config/fs_runtime/offline_fixture.toml OUT --mode offline-fixture`), exit code 0.

Component commits: FruitStack-Eval main d106a5d + branch `fsi/acceptance`; PeachMe 19379f5 + `fsi/acceptance` (ResearchPlan.verifier); CherryMe 11675ee;
PlumMe ccee075; AppleMe aca5f8b; OrangeMe c0beb27; MangoMe f9fcb63 (in-memory backend); PhysalisMe 448a3b1 (synthetic dataset).

Result:
- integration_path_ok: true for A, B, B-control (all stages, MangoMe checkpoint, 1 PhysalisMe tool receipt each, 8 research steps each, executed verifier ran).
- mission_success: false for all three. State UNRESOLVED: the inquiry claim stays UNKNOWN because the fixture investigator has no grounded source. Valid outcome, not success.
- Learning: A's candidate `math.isqrt` was SUPPORTED by the executed check → discovery VERIFIED (executed) → retrieved and applied in B → B and B-control
  both graded 1.0 by the executed check → `NO_EFFECT_OBSERVED`. B's own discovery (`math.comb`) is `STORED_NOT_REUSED`.

Files: `summary.json`, `stdout.json`, `learning.jsonl` (hash-chained ledger), `mission_<tag>.json`, `research_tree_<tag>.jsonl`, `tool_receipts_<tag>.jsonl`.
