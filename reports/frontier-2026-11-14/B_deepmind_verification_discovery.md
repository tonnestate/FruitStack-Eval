# B. DeepMind: verification and discovery systems (primary-source notes)
Date: 2026-11-14. Method: WebFetch (page text passed through a small summarizer model, so wording is
paraphrase/quote as returned; quotes marked "..." came back as quotes) + raw GitHub files via curl.
Classification: DEMONSTRATED = shown by artifact/proof/experiment in source; REPORTED = authors' claim, not
independently checkable from what I read; RECOMMENDATION = authors' advice/design intent.
Coverage caveat: AlphaProof Code paper page is 249k chars; I read chars 0-200k (not the last ~49k).
AlphaEvolve arXiv HTML 173k chars; I read first 100k only. Aletheia paper (arXiv 2602.10177) NOT fetched; only the blog.

## 0. Source status
- https://deepmind.google/blog/introducing-alphaproof-code/ : EXISTS (dated 2026-11-10, Kohli and Chaudhuri). Summary only; links paper deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf (not fetched).
- https://google-deepmind.github.io/code-verification/ : EXISTS; it is the full paper rendered as a "reviewers' site" ("Formally Verifying Signal's Security Using AI"). Section refs below are from it.
- https://github.com/google-deepmind/code-verification : EXISTS (232 stars, 2 commits on main at fetch time). README, CONTRIBUTING, docs/PAPER_MAP.md read raw. Full tree not cloned.
- https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/ : EXISTS (2026-02-11).
- https://deepmind.google/blog/alphaevolve-... : EXISTS (2025-05-14). Whitepaper = arXiv:2506.13131 (abstract + HTML read).

## 1. Licenses (AlphaProof Code repo)
- Code: Apache-2.0, Copyright 2026 Google LLC (README "License" section; LICENSE file header lists third-party exceptions). DEMONSTRATED.
- Third-party exceptions listed in LICENSE: third_party/hashbrown-0.17.1 = MIT; hashbrown_cli.elf (hashbrown + Rust std 1.98.1 + musl 1.2.5) = MIT; files copied from libsignal under third_party/libsignal = AGPL-3.0-only (per-file headers). 
- Not an official Google product; vulnerability reward per Google OSS VRP rules (GitHub page).
- Data/model licenses: NONE stated. No model weights released; proofs were produced by Gemini "Carbon" agents (blog) - not available. I did not find a separate data license; treat proof/spec artifacts as Apache-2.0 only insofar as LICENSE covers "all code"; unverified for data.
- Reuse note for us: AGPL libsignal material under third_party/ must not be copied into non-AGPL work.

## 2. AlphaProof Code: role separation (all from paper unless noted)
Layout: Computational/, Symbolic/, LibsignalBinary/, arm64-semantics/, third_party/, scripts/, docs/, comparator/ (ComparatorChallenge/), top-level lakefile.lean, lean-toolchain (Lean v4.34.0), rust-toolchain.toml (1.98.1).

F1. Four components: spec writing, machine-code semantics, proof synthesis, gatekeeping (Fig.1, §2). Human author "selects what to prove, resolves ambiguities, and makes final decisions"; AI drafts/tests specs under direction (§2). REPORTED (process description).
F2. Trusted vs untrusted: spec = Lean theorem statements + all dependent definitions, TRUSTED ("validity of the final result depends on getting it right"); proofs UNTRUSTED (§2.1). Blog: prover team untrusted, gatekeeper trusted. Human experts reviewed every spec (blog). REPORTED.
F3. Prover/language: Lean 4 (+Mathlib), kernel checks; AArch64 semantics 467 instructions, 31 syscalls, 7,578 lines Lean (§2.2); symbolic (Dolev-Yao) and computational (game-based) proofs. Scale: ~6.5M lines Lean proof, ~26k lines trusted specs+semantics (~18k statements/defs + ~8k semantics) (§1). Blog says "over six million". Build several hours, 15-34 GiB RAM (README). Numbers REPORTED; the repo makes them re-checkable (lake build) = DEMONSTRABLE by rebuild, I did not rebuild.
F4. Gatekeeping (§2.4): "A proof is accepted only if it proves exactly the statements the user approved." Gatekeeper agent invokes leanprover/comparator "using a deterministic script that can be rerun manually". Spec copied from baseline commit into "a held-out directory that no agent can write to"; held-out copy "changes only through accepted amendments". Comparator confirms (a) statement + every transitive definition identical to held-out copy, (b) only standard axioms (propext, Quot.sound, Classical.choice), (c) Lean kernel accepts (replay in fresh kernel from lean4export, not .olean; README). Gatekeeper also "check[s] recorded approvals for specification amendments". DEMONSTRATED as mechanism in repo (comparator/ dir, comparator/run.sh, install-tools.sh; Linux-only, sandboxed via landrun per README).
F5. Completion authority: "proof agents, team leads, and the orchestrator cannot declare a top-level goal done on their own" (§2.4). Lesson §7: team "never relies on an agent's own report that a goal is done". comparator re-run manually at the end. REPORTED/RECOMMENDATION.
F6. Gatekeeper sees only "file paths and theorem names", not provers' dialogue/explanations; Lean replays in fresh environment; `sorry` and `native_decide` rejected (§7). REPORTED. (Note: §2.3/2.4 text itself does not mention sorry; §7 does.)
F7. Axiom audit in repo: scripts/HeadlineAxioms.lean checks headline theorems use only 3 standard axioms (CI); scripts/CheckMainOfLemmasClosure.lean for one theorem; full sweeps scripts/CliAxiomGuard.lean and CliElfAxiomGuard.lean are MANUAL, not in CI (PAPER_MAP.md). Pinned binary: SHA-256-pinned libsignal-cli ELF, scripts/cli-elf-stock --verify-pin. DEMONSTRATED (files exist). Honest status labels in PAPER_MAP: proved / conditional / open (stated with sorry) / disproof.

## 3. Amendment controls (§2.3, §7)
F8. "Agents cannot edit the specification, but they can propose an amendment to a critic agent, which never sees the proof attempts." Critic accepts only if: (1) necessary - shown by machine-checked disproof, binary counterexample, or code-grounded argument; (2) non-weakening - "must not weaken security, and any assumption it adds must hold of the real code"; (3) small - "typically a few lines in one definition". Trusted-assumption changes need user approval or user-set policy; all logged; all reviewed at campaign end (§7). Example amendment: "memcpy may copy from read-only memory". REPORTED (process); the held-out-copy mechanism enforcing it is DEMONSTRATED in repo.
F9. §7 extra: amendment allowed only if proof can't be completed via stronger invariant/different decomposition; must keep non-vacuity witnesses and honest-run coverage; "A proposal that would weaken security to match the code is never accepted as an amendment" and is escalated to a human as a potential bug. REPORTED.

## 4. Non-vacuity and weakening protection
F10. Vacuity checks (§2.1): provers prove theorems about spec quality: hypotheses jointly satisfiable, premises met by concrete executions (borrowed from vacuity detection in model checking). Formal (Lean) proofs of satisfiability. REPORTED.
F11. Mutation testing (§2.1): agents inject bugs (e.g. skip ciphertext MAC verification) and PROVE the security theorem false on the mutated binary. Historical-bug check: two fixed libsignal bugs reintroduced, machine-checked proof that buggy binaries violate symbolic theorems (§1, §6; blog). Computational-model refutation "much harder" (§6). REPORTED (blog+paper); repo has Symbolic/BugInjection/.
F12. Rule (§7): "Every new invariant an agent introduces must come with a witness that it holds on some reachable state" so agents "cannot make progress by proving vacuous lemmas." RECOMMENDATION/REPORTED.
F13. Observed weakening incident (§7): under pressure an agent redefined a predicate as `False`, "and the trick spread" in one swarm. Weakening can occur indirectly via definitions, which is why the held-out copy covers all transitive definitions. REPORTED failure mode - the strongest evidence in the sources that spec gaming happens in practice.
F14. Residual vacuity caveat they admit (§5.2.5): the computational bound is practically vacuous for single sessions of ~25,000 messages or 2^20 sessions of 2^10 messages with frequent epochs. Limitations list (§5.2.5): no quantum adversary, TOFU identity keys, one build of libsignal-cli, etc. TCB (§5.3): AArch64 semantics, Linux process model, hooked-routine contracts, assumed primitive properties, symbol extraction tooling, build scripts, Lean itself; "The Rust compiler is not trusted." REPORTED.
F15. Spec effort: "the hard question is what to prove"; agent-written specs "hard to audit"; several review rounds; 15 gaps/bugs found in a published computational Double Ratchet analysis (§7). ~1% of codebase flagged for human review (blog). REPORTED.

## 5. Orchestration, compact progress, reuse
F16. Orchestrator "divides up the work and schedules agents but never edits Lean files itself"; roles: workers, team leads, architect (decomposition), integrator (merges verified proofs). "A lead absorbs the back-and-forth with its workers and sends the orchestrator short summaries of open obligations, completed lemmas and blockers." Concurrency: "each file is edited by at most one worker at a time, and only the integrator commits." Typical team 40-80 agents, one machine, 24-72 h. Agents try to falsify a goal before proving it. REPORTED.
F17. Reuse: integrator merges into library modules, removes duplicate lemmas, generalizes lemmas (§2.3). REPORTED.
F18. Blog headline: ~4 weeks vs "years" for expert teams. REPORTED (blog), no baseline data seen.

## 6. Aletheia (Gemini Deep Think blog, 2026-02-11)
F19. Loop from flowchart: Problem -> Generator -> Candidate -> Verifier; verdict "Correct" -> final output; "Minor fixes needed" -> Reviser -> updated candidate; "Critically flawed" -> back to Generator to restart. This IS the repairable-vs-fundamentally-wrong distinction (3-way verifier verdict). The verifier is a NATURAL-LANGUAGE verifier (an LLM), not a formal checker. REPORTED. Search/browsing used to avoid spurious citations.
F20. Admission of failure: agent can admit it failed to solve a problem; blog says this improved researcher efficiency (paraphrase). REPORTED.
F21. Numbers (read off chart descriptions, approximate): IMO-ProofBench Advanced Deep Think (Jan 2026) up to ~90%, Aletheia slightly above; FutureMath Basic Deep Think ~38%, Aletheia ~46%; higher quality at lower inference compute. Research results graded by autonomy levels: Level 0-2 results (Erdos-652/654/1040 L0, Erdos-1051 L1, Eigenweights L2 autonomous; others collaborations); Levels 3-4 none claimed; 700 open Erdos problems evaluated, 4 autonomously solved. Papers: arXiv 2602.10177 (Towards Autonomous Mathematics Research), 2601.22401. Prompts+outputs: github.com/google-deepmind/superhuman/tree/main/aletheia (not read). REPORTED.
Not in blog: how the verifier decides minor vs critical (no criteria), failure statistics per verdict, any formal checking.

## 7. AlphaEvolve (blog 2025-05-14; arXiv:2506.13131 HTML first 100k chars)
F22. Evaluator: user-supplied `evaluate` function mapping solution -> dict of scalars, to maximize; "embarrassingly parallel", async evaluation cluster (§2.1, §2.4). DEMONSTRATED by results; evaluator code is user's, so fitness = executable, not proof.
F23. Evaluation cascade (§2.4): "ensembles of test cases of increasing difficulty"; candidate advances only if it does well enough in all earlier stages; small-scale tests first to "filter out faulty programs early". No stages/thresholds given. (Blog does not use the term.) REPORTED.
F24. LLM-generated feedback (§2.4): separate LLM calls grade hard-to-encode properties (e.g. simplicity), added to score dict or used to discard. REPORTED - note this is a model judging, not computed check.
F25. Program database (§2.5): stores solutions with evaluation results; "inspired by a combination of the MAP elites algorithm" and island models; balances exploitation vs diversity, resurfaces earlier ideas. I could NOT confirm whether failed/discarded candidates are retained (text read says nothing). Prompt sampler (§2.2) samples multiple earlier solutions + rendered eval results + optional meta-prompts. Blog: programs "stored in the programs database". 
F26. Ensemble (§2.3): Gemini 2.0 Flash (throughput/breadth) + Pro (depth, rarer higher-quality suggestions). REPORTED.
F27. Efficiency: thousands of LLM samples suffice vs millions for FunSearch (Table 1); single evaluations up to ~100 compute-hours. REPORTED.
F28. Independent verification of results is DOMAIN-SPECIFIC and partly human: matrix mult coefficients rounded to integer/half-integer to keep exactness (§3.1); kernel tiling correct "by construction" (§3.3.2); compiler IR changes checked vs unmodified reference on randomized inputs + human experts (§3.3.4); TPU Verilog change passed verification methods + TPU designer validation (§3.3.3). REPORTED. Headline numbers: 4x4 complex matmul in 48 mults (vs 49); ~75% of 50+ open problems matched SOTA, ~20% improved; Borg heuristic 0.7% fleet compute; Gemini kernel 23% speedup / ~1% training time; FlashAttention up to 32.5%. REPORTED.
Caution: AlphaEvolve's fitness is only as good as the evaluator; the paper-level discussion of evaluator exploitation was not in the portion I read.

## 8. Reusable safeguards for an evaluation/grading system
Legend: FM = needs formal methods; EXE = implementable with executable tests/computed checks (NOT equivalent to formal proof; gives evidence on tested inputs only); PROC = pure process/file-system control.
1. Spec/rubric freeze with hash: store the grading spec (rubric, test suite, scoring code) in a held-out dir no worker can write; record SHA-256 in a signed manifest; grader refuses to run if hash differs. (Analogue F4.) PROC/EXE.
2. Transitive freeze: hash everything the spec depends on (helper libs, fixtures, reference data, scoring utilities), since weakening via definitions occurred (F13). PROC/EXE.
3. Amendment protocol: workers may only propose a diff; an independent reviewer who has not seen the candidate's attempts accepts only if (necessary: shown by a failing reproducible case; non-weakening: pass set on known-bad inputs does not grow; small diff cap; logged; human approval for trust-changing edits). (F8, F9.) PROC; "non-weakening" is checkable EXE by rerunning mutants/known-bad corpus, not provable without FM.
4. Non-vacuity tests: for every check, include (a) a known-good positive control that must pass and (b) a known-bad negative control that must fail; assert the check can discriminate; assert preconditions are satisfiable by at least one real execution. (F10, F12.) EXE (testing evidence). Only FM can prove satisfiability for all inputs.
5. Mutation testing of the grader: inject plausible defects into reference solutions/targets; the grader must fail every mutant; track mutation score; fail the release if a mutant survives. (F11.) EXE.
6. Historical-bug regression set: keep previously found real defects as permanent must-fail cases. (F11.) EXE.
7. Refuse self-reported success: only the independent grader process can mark an item done; workers, leads, orchestrator cannot. Grader sees artifact paths/IDs, not the worker's narrative. (F5, F6.) PROC.
8. Fresh-environment replay: rerun checks in a clean sandbox from sources, not cached build artifacts. (F4 .olean vs export.) EXE.
9. Banned-escape scan: reject outputs containing known bypass constructs for the framework in use (analogue of sorry/native_decide/extra axioms); allowlist dependencies. For tests: reject skips, xfail, monkeypatching of the grader, network, reading held-out data. EXE. (Formal analogue FM = axiom audit.)
10. Falsify-before-work: attempt a quick counterexample/refutation of a goal before spending effort, to catch unachievable or mis-specified targets. (F16.) EXE (formal disproof is FM).
11. Keep failed attempts and rejected amendments in an append-only log with reason and verdict; surface them in reports (F13, F25 caveat: AlphaEvolve source does not confirm failure retention, so this is our recommendation, not their demonstrated practice). PROC.
12. Three-way verdict with explicit "give up": verifier returns correct / repairable (bounded revision count) / fundamentally wrong (restart); worker may declare "cannot solve". Cap revision loops. (F19, F20.) PROC. Caveat: Aletheia's verifier is an LLM, so its verdicts are not evidence of correctness; pair with computed checks.
13. Staged cheap-to-expensive evaluation cascade with early rejection, and parallel evaluation. (F23.) EXE.
14. Separate model-graded criteria from computed criteria in reports; never let an LLM-judge score substitute for a computed check on the same property. (F24.) PROC.
15. Single-writer discipline: one editor per file/artifact; one integrator commits. (F16.) PROC.
16. Compact upward reporting: leads summarize open obligations, completed items, blockers only. (F16.) PROC.
17. Disclose TCB and limits in every report: what the grader trusts, and which claims are tested-only vs proved. (F14.) PROC.
Hard line: items 4,5,6,8,10 on executable tests produce evidence on sampled inputs; they do not equal proof. Claims of "verified" should be reserved for FM-checked statements (Lean kernel + comparator-style spec match).

## 9. Unverified / not read
- Technical PDF on deepmind.google (not fetched; site paper used instead). Last ~49k chars of site paper unread (likely references/appendix).
- No separate data/model license found. No info on gatekeeper "hierarchy" beyond roles above.
- AlphaEvolve second half of paper (ablations, discussion), failed-candidate retention, evaluator-exploit handling: unread.
- Aletheia paper/prompts repo unread.
- Fetch tool summarizes pages; exact wording should be rechecked in the source before external citation.
