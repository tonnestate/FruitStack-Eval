# PNP-001 — Register of failed or incomplete runs (owner order 2026-11-18)

Owner order: failed experiments and tests are documented and REPEATED when the cause is technical. They must not be dropped.
Classification:
- TECH = technical cause (code, environment, stack, time limit);
- MATH = genuine mathematical outcome (negative result in a stated search space).
Status:
- RERUN-OK = repeated, result recorded;
- RERUN-QUEUED;
- RERUN-RUNNING;
- OPEN = not yet repeated, with the reason.

## Local experiments (lab/)
| # | Run | What failed | Cause | Status / result |
|---|---|---|---|---|
| L1 | exp5x/sim.py, 1st run (venv without numpy) | never started | TECH: /opt/fruitstack/venv has no numpy | RERUN-OK with system python3 |
| L2 | exp5x/sim.py, 2nd run | timeout at 50 min, results only written at the end, nothing saved | TECH: no incremental save | RERUN-OK (incremental save added) |
| L3 | exp5x/sim.py, 3rd run | stalled for hours at Z/2^18 | TECH: subgroup closure by single steps (up to 2^18 passes) | RERUN-OK: doubling closure (self-check 100/100), complete, 972 rows (T40 §5) |
| L4 | exp5x/sim.py, 3rd run, stopped | the stop also killed the PI's shell | TECH: PI process error (pattern kill) | no data lost; memory rule extended |
| L5 | crt/crt.py | 19 "hierarchy violations" | TECH: rows with skipped JOINT (M > 2^24) were counted | RERUN-OK: 0 violations (T42) |
| L6 | onein3/anf_top.py, parts 4–5 | aborted before the reduction check | TECH: depended on a gadget not yet found | RERUN-OK: anf_top_rerun.py, all 8 sign patterns, top coefficient = #3SAT mod 2 and count equal (weak test: all 8 have count 7) |
| L7 | onein3/gadget_search.py | no OR gadget found | MATH (stated search space: no output variable, ≤ 3 aux, ≤ 3–4 clauses) | superseded: gates.py found functional AND/OR gates with an output variable (T41 §6) |
| L8 | onein3/read3.py (PI's own read-≤3 construction), 1st run | interrupted by the owner | — | rerun requested by the owner |
| L9 | onein3/read3.py, 2nd + 3rd run | timeout 1500 s / 1700 s | TECH (diagnosed 2026-11-18): the exact propagating counter needs ~4 s for ONE composed 3-SAT clause (138 vars, 116 clauses after the read-≤3 transform); 40 two-clause cases do not fit | 4th run (07:15-09:15, 2026-11-18) hit the 2 h limit again; NO output: results are only printed at the end (stdout buffered, nothing saved incrementally) -> TECH. Next rerun: save + flush per case, per-case budget, cases that exceed it recorded as DISCARDED (not waited for). STATUS: RERUN-PENDING |
| L10 | onein3/owner_read3.py, 1st run | never ran | TECH: system python3 has no sympy | RERUN-OK with /opt/fruitstack/venv-host/bin/python: 150/150 ×4, 120/120 |
| L11 | scratchpad closure.py (T38 O6), 1st run | hang | TECH: brute-force closure over the transformation monoid | RERUN-OK: truth-table closure (T38 §3b) |
| L12 | scratchpad proj.py (T39), 1st run | timeout | TECH: brute-force SAT over auxiliary variables | RERUN-OK: DPLL, n = 1..9 equivalence (T39) |
| L13 | onein3/aut2.py (AUT-2, MOD-P, Sylow conjugacy), 1st run | timeout 1500 s | TECH: brute-force Aut over all permutations up to n = 9; Sylow search over all 2-element combinations; imports re-ran the full self-tests of onein3.py and fixpoint.py | self-tests guarded behind __main__ (import 0.02 s); greedy Sylow + conjugates; n ≤ 7; RERUN-OK: 285/285 parity, 81/81 MOD-P, 283/283 D5 path, 83/83 Sylow quotients isomorphic (T41 §13c) |

## FruitStack missions (contracts/longrun-2026-11-15/pnp-iter*.out)
| # | Iteration / mission | What failed | Cause | Status |
|---|---|---|---|---|
| F1 | it. 4 & 5, first submissions | never started | TECH: request > 4000 characters, accept.sh hid the rejection | requests shortened; accept.sh fixed |
| F2 | it. 4 (51a47598) | no answer (synthesis failed) | TECH: stack fault F-1 | RERUN-QUEUED (pnp-iter04-04.out) |
| F3 | it. 5 (113f17a8) | "verified" refutation of E1 was false | TECH: stack fault F-3 (program check on a qualitative claim) | RERUN-QUEUED (pnp-iter05-04.out) |
| F4 | it. 6 (a7954e5d) | BLOCKED, MISSION_WALL_BUDGET | TECH: stack fault F-4 (synthesis reserve 300 s) | RERUN-QUEUED (pnp-iter06-03.out, after it. 11) |
| F5 | it. 9 (b4968eda) | BLOCKED, MISSION_WALL_BUDGET | TECH: F-4 | RERUN-OK: d6d314b7 COMPLETED; O6 objection answered (T38) |
| F6 | it. 10 (80b3922a, T40) | "refutations" based on wrong code | TECH: candidate F-5 (research-worker code quality) | RERUN-QUEUED (pnp-iter10-04.out); the stack cause F-5 is NOT repaired (owner: no architecture change without an order), so a rerun can fail the same way. That is then recorded here. |
| F7 | it. 7 (4fac7453), it. 8 (5f7f6f33) | COMPLETED, UNVERIFIED | not a failure by itself | EVALUATED by the PI 2026-11-18 (below) |
| F8 | T39 adversarial verification | never queued (announced "after iteration 9") | PI omission | QUEUED 2026-11-18 as it. 12 (req-pnp-iter12.json) |
| F9 | T38 O3, O7, O8 | not examined by it. 9 | scope of the mission | QUEUED 2026-11-18 as it. 13 (req-pnp-iter13.json) |

## Queue at the time of writing (2026-11-18)
it. 11 (T41, running) → it. 6 rerun → it. 4 rerun → it. 5 rerun → it. 10 rerun → it. 12 (T39) → it. 13 (T38 O3/O7/O8). One mission at a time; reruns use the unchanged
request files.

## PI evaluation of iterations 7 and 8 (2026-11-18)
- It. 7 (4fac7453, T36 falsification test; COMPLETED, UNVERIFIED; 3223 s):
  - The agents report "sum of maximal crossing lengths 80 (or 83) vs n²/4 + n = 48 for n = 12". This is NOT a counterexample to
    T31 C1. C1 bounds Σ_i D(L; cut_i), the communication complexity of the LANGUAGE (a lower-bound quantity). Crossing-sequence
    lengths of one particular machine can be arbitrarily larger. The mission itself left the run disputed: wrong model (HWTU
    instead of a multitape TM) and no stated measure.
  - Two CherryMe checks were rejected as INVALID (NOT_ALLOWED call, SYNTAX), so code-quality problems recur (candidate F-5).
  - No claim was settled. T36 is unchanged.
- It. 8 (5f7f6f33, T37 alias correction; COMPLETED, UNVERIFIED; 3377 s):
  - (A) character-sum alias condition p − 1 > D and (C) multi-prime CRT repair agree with T37.
  - (B) is the owner's counterexample: c_4 = 41 for W = (1⁴, 2⁵). PI recount: 1 + C(4,2)·5 + C(5,2) = 1 + 30 + 10 = 41 ≡ 0 mod 41.
  - (D) (transfer via 2611.11832 Thm 2) stays disputed, as in T37.
  - The "CSP alias test" numbers 84/128, 12/729, 2/3125 come from code that is not in the record. Not reproducible, not used.
  - No new statement. T37 is unchanged.
| F10 | CherryMe independent check of D-004 (mission 216eb8a6, 2026-11-18 11:17-11:32) | BLOCKED MISSION_WALL_BUDGET after 900 s, all claims unchecked | TECH: the request did not name the registered problem, so Aurora gave the 900 s lane instead of the 3600 s research wall; also CherryMe split the request and added a FALSE side claim ("all 66 classes satisfiable"). Fixes: desk wording "PNP-001 (P versus NP)"; only the claim equal to our count statement can settle it (side claims recorded as notes). | REPEAT QUEUED (attempt 2) |
| F11 | Staging lab restarts 11:07 and 11:09 | 6 discovery tasks killed (A0004-6, A0010-12) | TECH: lab tasks lived in the server's process tree / cgroup; a restart killed them (live: every deploy would). Fix: each task in its own systemd scope; desk retries infrastructure crashes once unchanged. A0010-12 requeued by PI as A0016-18, A0004-6 retried by the desk itself. | RERUN DONE/RUNNING |
| F12 | read3.py 4th run | see L9 | 5th run incremental + resumable started 10:15 | RUNNING |
| L9/F12 result | read3.py 5th run (incremental, resumable) 2026-11-18 | COMPLETED | direct read-<=3 transform 200/200 parsimonious; composed 3-CNF -> 1-in-3 -> read-<=3: 8/8 one-clause sign patterns parsimonious; 12 two-clause cases DISCARDED (600 s per-case budget; exact counter on ~270-variable instances), recorded, not refuted. Output lab/onein3/read3.progress.json, read3.out.json | CLOSED (two-clause cases: OPEN, need a faster counter, e.g. component decomposition) |

## F13 / F14 (2026-11-18, D-014 research cycles, staging)
- F13 RC-706334ce: all audits and proposals returned empty text (model supply), no question selected - technical failure, no result. Cycle not counted; next cycle got normal output. Repeat if recurrent.
- F14 RC-659b56dc: owner directive OWNER-D014 was only one of 82 evidence items; the organisation selected an off-directive question (Laplacian lambda_2 of the incidence graph vs SAT, 30 instances). Result kept as exploratory evidence. Organisational fix (goal, not method): pnp_research.py reads PNP_RESEARCH_DIRECTIVE into the MISSION text of every role; proposals must serve it or state a justified DEPARTURE; reviewers score MISSION against it. Restarted 5 cycles (PID 2651177).

## F15 Audit of the D-014 campaign + verified root cause (2026-11-18)
Cycles since the directive (staging research.jsonl):
- RC-706334ce: 2/2 audits and 4/4 proposals empty -> NOT a research investigation (NOT COUNTED). Not a transient outage: PlumMe marks such workers success=False, failure_class=SEMANTIC_OUTPUT_FAILURE (diagnostic call: 2 of 4 workers, qwen3.8-27b and qwen3.5-9b via ovhcloud); pnp_invent.plum() discarded success/failure_class and passed "" on. Proposals with code but empty question = parser defect (_sections required literal "QUESTION:").
- RC-659b56dc: executed, off-objective (Laplacian lambda_2 vs SAT on 30 instances; question text starts with "**" = parser defect). KEPT as exploratory evidence; does NOT address OWNER-D014; not counted toward D-014.
- RC-6a623a04: stopped during audit (1 of 2 audits empty) when the campaign was halted - no result.
Valid D-014 investigations so far: 0.
Root causes (all three verified from evidence): (1) objective stored as evidence item OWNER-D014 among 82 (extra.facts -> digest); (2) dispatch swallowed PlumMe failure verdicts; (3) brittle section parser.
Correction (Aurora-sync 7db49dd, existing pnp_research/pnp_invent, no new orchestrator): objective file PNP_RESEARCH_DIRECTIVE enters MISSION as a delimited "ACTIVE RESEARCH OBJECTIVE (owner instruction - authoritative; NOT evidence)" block for every role; OWNER-* facts excluded from the evidence digest; proposals need QUESTION + CONTRIBUTION + code; reviewers score OBJECTIVE 1-5, proposals below 3 rejected (logged); failed workers logged as WORKER_FAILED with PlumMe's failure_class and topped up once; cycles without an admissible, objective-advancing proposal logged CYCLE_NOT_COUNTED with reason; attempts bounded (2x requested). Calibration, proof ledger, provenance unchanged.
- F15 demonstration RC-ac317744 (corrected control, 7db49dd): OBJECTIVE logged with sha256; worker failures now visible (RATE_LIMITED, SEMANTIC_OUTPUT_FAILURE) and topped up; selected question on-objective (extend the D-012 GF(3) port structure to n=6,7 for a Gal matrix family; peer OBJECTIVE 3.5); one proposal (Z4/Z8 transformation) rejected with score 0.0 = NO reviewer score (fixed in fa6ff42: retry, logged UNREVIEWED). RESULT INVALID: experiment expected "rank 10" for the 10 clause vectors in GF(3)^6 (max rank 6; true rank 5 over GF(3) and GF(2), Claude) and computed rank with sympy over Q; its "contradicts D-012" claim is wrong - D-012 is about 10 program rows, not rank. Interpreter gpt-oss-20b identified both errors; nemotron-3.5-bolt-e4b accepted the false contradiction. LINEAGE_WARNING (number 012 copied from digest) was a false positive (an evidence id). Verdict: mission control WORKS (objective reaches agents and governs selection); scientific advance NOT achieved (invalid experiment). Counted as an on-objective investigation with an INVALID result.
- F16 RC-85edfc60 (on-objective, direction 2, peer OBJECTIVE 4.0): VACUOUS experiment - lab provenance cm-fdd2e7d06d8b40e1: numpy imported but no library call, 0.37 s, result "simulated_global_rank: 2". No evidence; NOT counted. Fix (Aurora-sync, after 7db49dd/fa6ff42): post-execution check _vacuous() from the lab's own provenance (imported_not_called without method calls, or "simulated/hypothetical/placeholder" in code/result; pure-python enumeration is not flagged) -> one repair turn, else CYCLE_NOT_COUNTED.
- F17 RC-501997d0 (on-objective, peer OBJECTIVE 3.0): main returned null -> vacuous; check extended (Aurora-sync f228506: empty result = "main returned no result"). Not counted. Campaign restarted (PID 2659409).
- F18 lab/circuits orbits_xor3_k6: one orbit (120 subsets, MUS (2,2,4,4)) stopped at BUDGET with proven lower bound 8 after 2189 s - to be repeated with a larger budget.
- F19 RC-49cdc738 (D-014): implementer gpt-oss-120b PROVIDER_UNAVAILABLE and PlumMe did not substitute within the PREFERRED pool -> author's code ran; first run TypeError (sympy rank(modulus=)), repaired run returned INVALID data: "total_sat_selections: 4" for n=5 (true 476, D-010) and the matrix uses the 20 clauses as columns (Gal's columns are unsatisfiable selections; with 20 columns rank >= 22 is impossible). Result invalid, kept as record. Fix: implementer walks the rotated pool on failure (Aurora-sync, next commit after d713fee).
- F20 ATLAS RC-983e19d0: all 3 proposals drifted back to 1-in-3-SAT (GF(3) port, near-matroid, lambda_2) although the ATLAS objective excludes fit-to-PNP as criterion; peers scored OBJECTIVE 1.0 -> correctly NOT counted. Cause: both campaigns shared one evidence digest dominated by 1-in-3 records (D-001..D-015); also CONTEXT_OVERFLOW (gpt-oss-120b). Fix (Aurora-sync 219b32d): per-campaign evidence scope PNP_RESEARCH_EVIDENCE (id prefixes); ATLAS scoped to LIT-ATLAS/OPT/ROTHVOSS/LIMIT/WILLIAMS/PATTERNS/SEYMOUR/MSP/SUPPORT/GAUSS/KKY/CANCEL. Restarted (PID 2666713).
- F21 D-014 RC-d222b236: 4 on-topic proposals (Gal matrices) all rejected (peer OBJECTIVE 1-2). Reviews were correct about the DRAFT code (fabricated ranks, clauses used as rows/columns instead of SAT/UNSAT selections, circular use of mSP=10) - but since d713fee an implementer rewrites the code, and the lab INPUT held only per-formula data, not the selection universe the objective needs (source of the earlier "4 SAT selections" error). Fix (Aurora-sync fbf19ef): exact verified campaign data as INPUT['1in3_n5'|'1in3_n6'|'xor3_n5'] (clauses, minterms, maxterms; lab/gal/data.py) via PNP_RESEARCH_DATA, documented to proposers and implementer; reviewers score the QUESTION/CONTRIBUTION and list draft defects; implementer receives the peer critiques. D-014 evidence scope REG, LIT-MSP/SEYMOUR/LIMIT/ROTHVOSS/OPT/SUPPORT, BOOK. Restarted (PID 2667821).
- F22 ATLAS RC-86dc4a0a (mechanism B, state compression; peer OBJECTIVE 3.0): FIRST implementer success (nemotron-3-ultra-550b, lab cm-12e6f37aec6e4aad, computed, with calibration). Scientifically NO evidence: grouped_size = baseline + 3*classes by construction (cannot shrink), count preservation checked tautologically (no count computed), signature ignores cross-clause overlap, hand-set calibration labels wrong in 3 of 5 cases - all identified by the organisation's own interpreter (claude-haiku-5-5). Counted as an executed investigation with a NULL result; kept. Open: implementer computes but can still choose a tautological measure - reviewers/interpreters catch it after the fact.
- F23 (Claude's error, 2026-11-18 14:53): Iteration 12 (T39 adversarial verification, mission 35a393f4) SIGKILLed ~1 min after start by an AppleMe deploy + ananasme@www-data restart; the hand-written "no mission worker" guard did not abort. Technical cause, not a result. Iteration 12 resubmitted (contracts/longrun-2026-11-15/pnp-iter12-02.out), then Iteration 13. AppleMe deploys now only via deploy.sh appleme (tested REFUSED guard).
- F24 ATLAS RC-2ea46e69 (state compression / treewidth): computed and calibrated (elimination counts = brute force), question lifecycle worked (ADDRESSES -> APPROACH iteration). No evidence: all instances min-fill width 2-3, no variation; interpreters said so. MISSED: the question is KNOWN (#SAT is FPT in incidence treewidth, e.g. Samer-Szeider) - the directive's "check known theorems first" was not applied by proposer, reviewers or interpreters. Pattern to watch.
- F25 D-014 vacuity false positive RC-d55cb9d3 first run (unused sympy import, 78 s real computation) - rule fixed 5ecd6af; its result D-014b then found INVALID as a Gal measurement (pairs x clauses matrix), directive gained a binding DEFINITION of A.
- F23 resolved: Iteration 12 rerun (mission c8d922ea) COMPLETED, verification UNVERIFIED, wall 3191 s (contracts/longrun-2026-11-15/pnp-iter12-02.out); Iteration 13 started right after. The PlumMe deploy waiter checked "no worker" before taking the submit lock and was refused by deploy.sh's guard when Iteration 13 started in between - no harm; waiter now takes the lock first, then checks.
