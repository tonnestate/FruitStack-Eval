# OGI-013 AMENDMENT-1 — measurement implementation of independent verification (prospective)

Written 2026-10-28, after four diagnostic RG/2 demonstration runs and BEFORE any further evidence is collected. It amends the MEASUREMENT IMPLEMENTATION only.
`evidence/ogi013-c3-prereg/PROTOCOL.md`, `PREREG_LOCK.txt`, `evidence/ogi013-rg2-demo/PROTOCOL.md`, ORG-GATE/1, the hypotheses H1–H5, the task lists/splits, the official tau2 grader,
the independent quorum (>=2 workers with DIFFERENT independence keys and verbatim quotes), the Holm/McNemar analysis and the demo criteria 1–6 are NOT changed and stay byte-for-byte as sealed.

## Defects found (each verified in code and in preserved evidence)
D1 Compound claim. Each decision was put to the engine as ONE claim: "<whole reply or tool call with its ids/dates/amounts> follows the policy and is justified by the customer's request and the
   observed system data". The EvidenceVerifier judges a claim against ONE host excerpt at a time, and a SUPPORTS promotion additionally requires every asserted value of the claim to occur in the
   judges' quotes. No single excerpt (policy chunk, conversation, tool result) contains policy, request and data together, so promotion was structurally unsatisfiable.
   Evidence: run4 (archived) produced 36 VERIFIER judgments, all NOT_ADDRESSED, 0 promoted; run1–run3 produced none (verifier unreachable, see D4).
D2 Label mapping. The verifier records judgments as VERIFIER contribution rows with the raw relation (SUPPORTS / CONTRADICTS / NOT_ADDRESSED) and marks a quorum promotion as
   epistemic_status=VERIFIED, disposition=ACCEPTED (Evidence verdict PASS / CONTRADICT). rg2_trace_report.py looked for row verdicts "PASS"/"CONTRADICT" and therefore could never see a promotion.
D3 Wrong location. rg2_trace_report.py read contributions from `tasks/<id>/org/cherry`, but the engine workspace is the arm's shared `OGI013_ORG_STATE_DIR/cherry`; every report had zero contribution
   rows (`worker_contribution: null`). Two tasks of one arm share that directory, so rows must be filtered to the claims decided in the run being reported.
D4 Unreachable verifier (fixed earlier, commit ec01890/86a2630 history): claims were asked as FALSIFY, which is not a grounded question type, so host grounding and the verifier never ran (run3: 0 verifier rows).

## Amendment (what changes)
A1 The compound decision claim is kept unchanged, asked as FALSIFY, deliberated by the engine's workers exactly as before (dissent and its revision path are unchanged).
A2 In addition the host derives, WITHOUT any model, up to 2 ATOMIC provenance propositions per decision from the proposed action: every identifier-like value (id, date, amount) in tool arguments
   (first) or in a reply. Claim text: "The value <v> [given as '<tool.arg>' of the assistant's tool call | stated in the assistant's reply] appears in what the customer said or in a system tool result of this conversation."
A3 Each atomic claim is ONE SCIENCE (grounded) question. Host excerpts: a window (+-1200 characters) around the last occurrence of <v> in what the CUSTOMER said (USER lines only; the assistant's own words are
   never a source) and in the TOOL RESULT lines, SHA-256 bound; if <v> occurs in neither, the tail of the tool results is offered so the value is judged NOT_ADDRESSED (unsupported), never dropped.
A4 The EvidenceVerifier is unchanged (quorum 2, distinct independence keys, verbatim quotes, third judge on dissent). Atoms are skipped under the pre-registered no-verify ablation (RG2-NO-VERIFY).
A5 A quorum-verified CONTRADICTS of an atom sets the decision status to REFUTED (verified dissent); the existing revision path then applies. UNSUPPORTED (not addressed) is not dissent.
A6 rg2_trace_report.py: reads the shared state directory (`--state-dir`, filtered to the claims of the reported run incl. atom claims listed in ORG_DECISION.atoms); independent verification = a (claim, source) pair
   with >=2 VERIFIER rows that are VERIFIED/ACCEPTED with SUPPORTS or CONTRADICTS (legacy PASS/CONTRADICT accepted) from >=2 DISTINCT independence keys. Judgments exist but none promoted -> `false` (was `null`).
   organisational_success formula unchanged: worker_contribution AND (causal effect OR independent verification) AND official reward 1.0.
A7 Verifier judgments are persisted per task as `tasks/<id>/org/verifier.log`; whether the verifier was attached is written to `verifier-attached.txt`.
Scope limit (stated, not hidden): atoms verify the PROVENANCE of asserted values, not policy compliance. Policy compliance remains judged only by worker deliberation (unverified, dissent-triggered revision).

## Other infrastructure corrections made in the same window (no effect on hypotheses, splits, thresholds)
Uncapped simulator output (PlumMe negotiates), simulator model chosen from a live-surveyed executable pool with cooldown-aware wait/fail, workers fenced off the simulator's model, worker pool limited to
PlumMe-executable models, organisational state restored on discarded attempts, discarded attempts archived (never deleted), Phase A held by `PHASE_A_RELEASE`.

## Historical evidence (kept, never reinterpreted)
Demo runs 1–4 under `runs/org-demo/run{1,2,3,4}-*` and `evidence/ogi013-rg2-demo/run{1,2,3}-*` are diagnostic. Their verdict `organisational_success=false/null` is a verdict of the defective measurement, not a test of organisational intelligence.

## Tests (offline, no model calls): tests/test_ogi013_measurement_amendment.py
Genuine atomic claim promoted by two lineages; unsupported / dishonest-quote / single-judge / same-lineage cases rejected; the original compound claim cannot be promoted by a policy chunk;
the report detects quorum promotion, rejects unpromoted judgments, requires distinct keys, ignores other runs' claims in the shared state, accepts legacy labels.

## Freeze
`AMENDMENT-1.LOCK.txt` records the implementation commit and the SHA-256 of the implementing files. One controlled live demonstration follows; Phase A stays held until its verdict is reported.
