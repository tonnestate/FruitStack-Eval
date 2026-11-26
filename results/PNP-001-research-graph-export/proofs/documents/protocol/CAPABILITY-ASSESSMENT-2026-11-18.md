# PNP-001 — Capability assessment of autonomous research (2026-11-18, staging, measured)

Evidence: staging logs `research.jsonl`, `invent.jsonl`, `algorithms.jsonl`, desk `state.json` (scratchpad staging), proofbook copy.
Agents: PlumMe-allocated workers (nemotron-3.5-bolt, gpt-oss-20b/120b, gemma-4-26b, mistral-small-3.2, qwen3-vl-30b, qwen2.5-vl-72b,
allam-2-7b, rocinante-12b, deepseek-v4.1-flash, step-5-preview).

| Capability | Works? | Evidence |
|---|---|---|
| Select a question from the record, citing evidence ids | YES | cycle RC-9ed87d7e/RC-bc9cf2e8: proposals cite REG3-REG10, UNIV1-3, BOOK, DESK |
| Peer review and selection without PI | YES (weak) | scores 0.0-3.0; 0.0 = reviewer gave no parseable scores |
| Causal chain (next experiment cites previous result) | YES, but the rule is crude | 2 of 4 proposals in cycle 2 rejected for not citing; those were the structural questions (gemma) |
| Write an experiment that answers its own question | MOSTLY NO | cycle 1: placeholder ("unknown_or_calculated_via_lab"); cycle 2: re-used register numbers instead of computing; mixed denominators (5/445 vs 119/322) |
| Method critique of an executed experiment | PARTLY | cycle 1: placeholder flagged as unsound; cycle 2: "simulation relies on known data points" (leakage) flagged; the denominator error NOT found |
| Invent executable algorithms | RARELY | 5 rounds, 18 proposals: 6 vacuous, 4 not runnable, 4 incorrect (34-634 wrong), 4 sound; 1 with new coverage (11 instances) |
| Falsify an invented algorithm | NO (agents) / YES (laboratory) | agent "counterexamples" were satisfiable single clauses; the GF(3) rule was refuted by a laboratory search launched by the PI (n=8, m=6, C=0) |
| Use the laboratory's analysis tools in missions | NO | missions 66bd/8272/06f8: physalis_code_run 9-32x, discovery/ML tools 0x |

Why the organization did not detect its methodological shortcomings earlier:
1. No stage asked for a critique of the METHOD: missions verified the PI's claims; nothing fed the organization's own process data back.
2. The agents never saw their own track record (tool usage, rejection rates) - added now as digest items (MIS*, INVENT, DESK).
3. Model mix: REASONING/REVIEWER roles are served mostly by small fast models; they parse tasks well and write runnable but shallow code.
4. Correctness was decided by the host (good), but nobody was rewarded for finding a counterexample, so the challenger role produced none.

Open corrections (next): (a) the causal rule should accept a proposal that cites ANY result of the chain or explains why it departs;
(b) experiments must compute from INPUT, not from digest numbers - check by data-lineage (result values must not appear verbatim in
the digest); (c) reviewer prompts must check denominators / units; (d) a stronger model class for the experiment-writing role, measured
against the small ones (balancer input); (e) challenger rewarded by verified counterexamples, run against every SOUND procedure.
