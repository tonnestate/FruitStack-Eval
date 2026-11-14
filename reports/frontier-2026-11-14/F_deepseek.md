# F_deepseek: DeepSeekMath-V2 + DeepSeek API docs (primary-source research)

Date: 2026-11-14. Research only, no code changes. Labels: DEMONSTRATED (shown by evidence in the source),
REPORTED (author claim, figures not text-verifiable), RECOMMENDATION (author advice), PRODUCT_CAPABILITY (vendor doc).

## 0. Fetch log (what was actually read)
- https://arxiv.org/abs/2511.22570 : OK. v1 only, submitted 2025-11-27, cs.AI/cs.CL. Authors: Shao, Luo, Lu, Ren, Hu, Ye, Gou, Ma, Zhang (DeepSeek-AI).
- https://arxiv.org/html/2511.22570v1 : OK, full text read (text only). Math formulas and figures are images/MathML: formula
  alt-text was recovered from the HTML source; figure numbers (Fig. 1-3) are NOT readable. The PDF fetch returned binary
  (compressed streams) and was not used. Paper has no dedicated "Limitations" section.
- https://api-docs.deepseek.com/updates/ , /guides/thinking_mode/ , /guides/tool_calls/ , /guides/kv_cache/ , /guides/search/ : all OK.
  Note: page summaries were produced by a fetch-side model; exact quotes are limited. Re-check critical values against the live page.
- https://github.com/deepseek-ai : OK but only 10 of 47 repos were visible; DeepSeek-Math-V2, V3.x, R1, Prover were NOT in the visible list
  (cannot confirm either way from that page).
- https://github.com/deepseek-ai/DeepSeek-Math-V2 : OK (exists).

## 1. DeepSeekMath-V2: facts from the paper
Base model: DeepSeek-V3.2-Exp-Base (README). Task: natural-language theorem proving. Optimizer: GRPO, alternating verifier / generator
iterations (Sec 3.1).

### 1.1 Verifier (proof-level, not answer-level)  [DEMONSTRATED as method; accuracy numbers REPORTED]
- Motivation (Sec 1): final-answer reward is an unreliable proxy ("correct answers don't guarantee correct reasoning") and inapplicable
  to proofs. Answer-trained models showed "high false-positive rates, often claiming incorrect proofs are valid".
- Input: problem + full proof. Output: a "proof analysis" that FIRST summarizes identified issues, THEN gives a score in {0, 0.5, 1}:
  1 = complete and rigorous; 0.5 = sound overall logic, minor errors or omitted details; 0 = fatal errors / critical gaps / does not
  address the problem. Rubric also says citing a paper does not excuse proving the cited argument (Appendix A.2).
- Fixed output format enforced by reward: key phrase "Here is my evaluation of the solution:" and "...the final overall score should be:"
  with score in \boxed{}.
- Cold-start data: 17,503 AoPS proof problems (olympiads, TSTs, post-2010 proof problems); candidate proofs from a variant of
  DeepSeek-V3.2-Exp-Thinking prompted to refine over several rounds; random sample scored by math experts on the rubric.
  (Dataset size of the scored subset is not given in text.)
- Reward: R_format * R_score, R_score = 1 - |s' - s| (predicted vs expert score). Starts from DeepSeek-V3.2-Exp-SFT.
- Verifier needs NO reference solution ("A proof is more likely valid when no issues can be identified despite scaled verification").

### 1.2 Meta-verifier (guards against hallucinated issues)  [DEMONSTRATED as method; 0.85->0.96 REPORTED]
- Problem named explicitly: with score-only reward, on flawed proofs the verifier "can receive full reward by predicting the correct
  scores while hallucinating non-existent issues". I.e. right verdict, fabricated reasons.
- Meta-verification = second pass that checks (a) do the issues the verifier names actually exist in the proof, (b) do they logically
  justify the score under the rubric. Appendix A.3 prompt has four aspects: Step Restatement, Defect Analysis (most important:
  does the defect exist AND is the analysis of it accurate), Expression Analysis (even minor inaccuracies), Score Analysis (score matches
  defects found). Meta-verifier does NOT solve the problem and ignores positive claims: if the evaluation finds no defects it is
  deemed reasonable regardless (so it only audits FAIL/issue reports, not PASS verdicts).
- Training: experts score verifier analyses -> dataset; meta-verifier trained by RL with same format+score rewards.
  Verifier reward then becomes R_V = R_format * R_score * R_meta (R_meta = meta-verifier quality score).
- Result: mean meta-verifier quality score of verifier analyses on a validation split rose 0.85 -> 0.96 with unchanged proof-score
  accuracy. One model does both verification and meta-verification.

### 1.3 Generator with verifier as reward + self-verification  [DEMONSTRATED as method]
- Generator reward R_Y = verifier score s of the proof.
- Observed failure (Sec 2.2.2): a generator asked to write and check its own proof in one shot "tends to claim correctness even when the
  external verifier easily identifies flaws"; it can refine against EXTERNAL feedback but is not rigorous on its own work.
- Fix: generator outputs proof Y then a self-analysis Z in the verifier's format/rubric (prompt A.1). Both are scored by the verifier:
  proof score s, self-analysis gets R_Z = R_score(s', s) * R_meta(Z) (s' = self-score). Total reward
  R = R_format(Y,Z) * (alpha*R_Y + beta*R_Z), alpha = 0.76, beta = 0.24.
- Incentives (author-stated): honest admission of errors beats false claims of correctness; best = correct proof AND accurate
  recognition; fix as many issues as possible before finalizing. Prompt A.1 says: score 1 only if no issues found; if issues remain,
  present them faithfully; "worst" response is a wrong solution claimed correct.

### 1.4 Scaling verification compute to auto-label hard proofs; keeping the gap  [DEMONSTRATED as method; quality REPORTED]
- Rationale: new generator proofs are harder for the verifier; manual annotation does not scale. Two observations: (1) more verifier samples
  raise the chance of catching real issues in flawed proofs; (2) reviewing reported issues (= meta-verification) is easier than finding
  issues from scratch.
- Pipeline: for each proof, generate n independent verification analyses; for analyses with score 0 or 0.5, generate several
  meta-assessments, analysis counts as valid if the majority confirm it; take the lowest score among analyses; if at least k valid analyses
  give that lowest score, label the proof with it; if no legitimate issue across all attempts, label 1; otherwise discard or send to experts.
  (The values of n, m, k were lost in text extraction; NOT stated here. Check the PDF.)
- "In our last two training iterations, this fully automated pipeline replaced human annotation entirely"; "quality checks confirmed
  automated labels aligned well with expert judgments" (no numbers given in text).
- Generation-verification gap: the paper's mechanism to keep it is the loop (hard new proofs -> labeled by heavy verification -> retrain
  verifier). Each new verifier initialized from a checkpoint consolidating verification+generation via rejection fine-tuning (Sec 3.1).
- "Hard negatives": the paper does not use this term. Closest concept: proofs the verifier misses in a single attempt ("challenging cases
  where the verifier may fail to identify issues in a single attempt") become training data. Do not cite as "hard negatives" without caveat.

### 1.5 Test-time scaling  [DEMONSTRATED procedures; results REPORTED]
- One-shot (Sec 3.3.1): 8 proof samples per problem on 91 in-house CNML-level problems; correctness = majority vote over 8 verifier analyses
  (verifier = their own final verifier; i.e. the judge is the authors' model). Beats GPT-5-Thinking-High and Gemini 2.5 Pro (figure, no
  numbers in text).
- Sequential refinement with self-verification (Sec 3.3.2): generate proof + self-analysis, re-prompt with previous output (prompt A.4)
  until self-score is perfect or max attempts. Tested max 1..8 sequential attempts (initial + up to 7 refinements) on IMO Shortlist 2024
  (31 problems) with 32 independent threads; correctness = majority vote over 32 verifier analyses. Metrics: Pass@1 (mean final proof per
  thread) and Best@32 (best proof per problem chosen by SELF-assigned scores). Claim: Best@32 clearly above thread average, Pass@1 rises
  with iterations (figure only; numbers not in text). Context cap 128K tokens per attempt is why refinement is needed.
- High-compute search (Sec 3.3.3): pool initialized with 64 proofs x 64 verification analyses each. Each iteration: take the 64 highest
  proofs by mean verification score, pair each with 8 randomly selected analyses (prioritizing those reporting issues, score 0/0.5), one
  refined proof per pair, update pool. Up to 16 iterations, or stop when a proof passes all 64 verifications. Single model (final
  generator) does generation and verification. Experts graded the top-scored proofs.

### 1.6 Reported results (conditions above; high-compute search unless noted)  [REPORTED]
- IMO 2025: 83.3% of points (P1-P5 solved; P6 not), gold-level. (35/42 is my arithmetic from 83.3%, not stated.)
- CMO 2024: 73.8% of points (4 solved + 1 partial), gold-level.
- Putnam 2024: 98.3% = 118/120 (11 of 12 fully, 1 with minor errors); highest human score cited as 90.
- IMO-ProofBench (60 problems: 30 basic, 30 advanced; DeepMind benchmark): "outperforms DeepThink (IMO Gold) on the basic set,
  competitive on the advanced set"; DeepSeekMath-V2 graded by the authors' own experts following the grading guidelines, other numbers
  copied from Luong et al. 2025. Exact scores only in a figure; not recoverable here.
- Caveats: grading by authors' experts and their own verifier (not independent); no seeds/variance reported in text; results depend on large
  compute (64x64 samples, 16 iterations); IMO P6 and hardest problems unsolved.

### 1.7 Stated limitations
- No dedicated section. Conclusion: "significant challenges remain"; "hardest IMO-level problems remain challenging for our model".
- Positive claim to treat cautiously: for unsolved problems the generator "typically identifies the genuine issues"; solved problems pass all 64
  checks. This is evidence of calibrated self-assessment on these benchmarks only.
- Self-verification alone is weak without training (their own observation in 1.3).

### 1.8 Learned verification vs formal proof
- Paper's own framing (Sec 4): Lean/Isabelle give a guarantee once compiled but need formalization; AlphaProof needed intensive compute
  (silver IMO 2024); DeepSeek-Prover-V2 and Seed-Prover (5/6 IMO 2025) are formal. DeepSeekMath-V2 is informal natural-language proof and an
  LLM verifier: probabilistic, no soundness guarantee. Confidence = "no issue found across 64 verification attempts", which is evidence, not proof.
  They hope informal progress will help formal systems.

### 1.9 Release / license  [PRODUCT_CAPABILITY]
- Repo github.com/deepseek-ai/DeepSeek-Math-V2: GitHub shows "Apache-2.0 license" for the repo (code). README: "The use of DeepSeekMath-V2
  models is subject to the Model License" (link to repo LICENSE). The model-license text and whether it equals Apache-2.0 were NOT verified
  (fetch showed only the label). Weights: huggingface.co/deepseek-ai/DeepSeek-Math-V2. Inference via DeepSeek-V3.2-Exp repo. Outputs folder
  has model predictions. arXiv paper license: arXiv perpetual non-exclusive. TODO before any reuse: read LICENSE file directly.
- Practical: the weights are a V3.2-Exp-scale model (not runnable cheaply); the API docs list no DeepSeekMath-V2 endpoint.

## 2. Ideas usable WITHOUT retraining (prompting / orchestration only)  [RECOMMENDATION unless noted]
The paper demonstrates these procedures only with models trained for them; their efficacy with untrained general models is NOT shown by the paper.
1. Proof-level / answer-level critique with an issues-first format: verifier writes issue list THEN score (0/0.5/1). Cheap to copy.
2. Multiple independent verification passes (paper: 8, 32, 64) with differing seeds/models; take the lowest score, require N confirming passes.
3. Meta-verification of issue reports: second call receives (task, answer, issue report) and checks only "does this defect exist, is the analysis
   accurate, does the score match the defects" (copy the A.3 structure; ignore claimed-correct parts). Majority of meta-assessments decides.
   Guards against false-positive FAILs (hallucinated issues). Note the asymmetry: it does not audit PASS verdicts.
4. Aggregation rule from the auto-labeler: label = lowest score confirmed by >= k valid analyses; no valid issue anywhere = pass; otherwise
   escalate (human / more compute). Adaptive effort: spend more passes only on proofs with disagreement.
5. Refinement with verifier feedback: feed the proof + several (prioritized issue-reporting) analyses back to the generator; loop until all
   verifications pass or an iteration cap (paper: 16).
6. Best-of-n selection by mean verifier score; stop early at unanimous pass.
7. Generator self-analysis in the same output with an honesty instruction (prompt A.1 text). Caveat: paper found UNTRAINED generators overclaim
   correctness; so use a SEPARATE verifier call/model rather than trusting self-score. Self-score is useful mainly after training.
8. Use a different model family as verifier to reduce shared blind spots (not from the paper; the paper uses one model for both roles).
Do NOT apply without training: the R_V / R_Y / R_Z reward shaping, RL against verifier, rejection fine-tuning consolidation, learned
calibration of self-score, the claim that verifier gets "ahead" of the generator.

## 3. DeepSeek API docs (state as read 2026-11-14)  [PRODUCT_CAPABILITY]
### 3.1 Updates page (newest first; dates exactly as listed)
- 2026-11-13: "Full suite of application APIs": `deepseek-flash` with web search, deep-thinking search, file input, URL reading, model safety;
  standalone Search and Fetch, OCR, ASR, TTS APIs; demo chat client.
- 2026-10-17: in-house Search API opened; `deepseek-flash` now points to DeepSeek-V4.1-Flash-1017; price unchanged.
- 2026-09-10: DeepSeek-V4.1-Flash released; `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` temporarily routed to V4.1 Flash; old
  V4 Flash / Vision Exp retired; V4 Pro continues past 2026-09-14; API prices reduced (no figures).
- 2026-08-21: DeepSeek-V4-Flash-Vision-Exp (experimental).
- 2026-08-13: DeepSeek-V4-Pro GA update; Responses API; thinking effort low/high/max for V4-Pro and V4-Flash; peak/off-peak pricing,
  off-peak half of peak, effective 2026-08-16 16:00 UTC.
- 2026-07-31: DeepSeek-V4-Flash update (0731); Responses API.
- 2026-04-24: DeepSeek-V4 (`deepseek-v4-pro`, `deepseek-v4-flash`; OpenAI ChatCompletions and Anthropic interfaces). `deepseek-chat` and
  `deepseek-reasoner` map to non-thinking / thinking of `deepseek-v4-flash`; discontinuation was set for 2026-07-24 (page does not say whether
  the aliases are still served; verify before relying on them).
- 2025-12-01: V3.2 (chat -> non-thinking, reasoner -> thinking); V3.2-Speciale temp endpoint, no tool calls, until 2025-12-15 15:59 UTC.
- Earlier: V3.2-Exp (2025-09-29), V3.1-Terminus (09-22), V3.1 hybrid (08-21), R1-0528 (05-28), V3-0324, R1 introduced 2025-01-20, V3 2024-12-26.
- Context caching on disk introduced 2024-08-02. Page lists the 2025-01-20 line oddly (V3 via deepseek-reasoner): likely a typo.
- Current identifiers (use these, not chat/reasoner): `deepseek-flash` (V4.1-Flash-1017), `deepseek-v4-pro`; `deepseek-v4-flash` temporary route.

### 3.2 Thinking mode
- Default: ON, effort `high`. Enable/disable: OpenAI format `{"thinking": {"type": "enabled|disabled"}}` (via extra_body in OpenAI SDK);
  Anthropic format `{"reasoning": {"effort": "none|low|high|max"}}` (none = off).
- Effort: OpenAI `reasoning_effort` low/high/max; Anthropic `output_config.effort`. Mapping: minimal,low->low; medium,high,xhigh->high; max,ultra->max.
- temperature, presence_penalty, frequency_penalty: no effect in thinking mode, no error. top_p: deepseek-flash applies only in thinking
  (range 0.95-1.0); deepseek-v4-pro ignores it in thinking mode. `tool_choice: none` disables tools.
- `reasoning_content` returned beside `content`. Without tools: no need to pass back (ignored). With tools: MUST pass back reasoning_content of
  all previous turns, else HTTP 400. Max-token limit not stated on page.

### 3.3 Tool calls
- Contract: tools = {type: function, name, description, parameters (JSON Schema)}; model returns name+args; client runs it and appends a
  role:tool message with tool_call_id. Thinking-mode tools supported since V3.2. Mid-conversation tool-call insertion only on Anthropic/
  Responses API, not Chat Completions.
- Strict mode (Beta): base_url `https://api.deepseek.com/beta`; every function needs `strict: true`; server validates schemas. Works in thinking
  and non-thinking. Supported: object, string, number, integer, boolean, array, enum, anyOf, $ref/$def. Objects: all props required,
  additionalProperties false. Unsupported: string minLength/maxLength, array minItems/maxItems. Strings: pattern and some formats supported;
  numbers: min/max/exclusive/multipleOf/const/default supported.

### 3.4 KV (context) cache
- On by default. Hit only if the request prefix fully matches a persisted "cache prefix unit"; best-effort, no 100% guarantee. Units persisted at
  request boundaries (end of user input, end of model output), on detected common prefixes, and at fixed token intervals for long text.
  Usage fields: prompt_cache_hit_tokens, prompt_cache_miss_tokens. Cache build takes seconds; cleared when unused "usually within a few hours to a
  few days". Minimum size and hit/miss price difference: NOT stated on this page (check pricing page). Implication: keep stable instructions first,
  variable task text last.

### 3.5 Search guide
- It is a PROVIDER feature plus guidance: "Search & Fetch" raw APIs. Search: POST /v1/tools/search (in-house engine; query, count, need_content,
  operators like site: and after:). Fetch: POST /v1/tools/fetch (page -> Markdown). Billing $0.75 per 1,000 successful requests each; rate limits
  100 QPS Search, 25 QPS Fetch (account-level, plus per-domain for Fetch). Model-driven search lives in a separate web-tools guide.

### 3.6 GitHub org
- 47 repos; visible (10): deepseek-harness (MIT), deepseek-recipe, DeepInfer (Apache-2.0), chat-demo (MIT), awesome-deepseek-integration (CC0),
  3FS (MIT), DeepJIT (MIT), dsh-superagent-prototype (MIT), DeepEP-Ascend, FlashMLA (MIT), DeepEP (MIT). Math-V2 repo exists with Apache-2.0 label.

## 4. Mapping to a host grader (COMPUTED_CHECK)
Current design: two cross-family workers write boolean assertions; host evaluates with restricted evaluator; numbers must come from the task or
claim; every claim figure must be checked; negative control = +-1 % perturbation must flip the check. Failure: claim formulator emitted vague
meta-claims so nothing was checked, and a wrong figure reached the answer.

Mechanisms that add value BEYOND COMPUTED_CHECK (orchestration only, RECOMMENDATION; paper evidence is for trained models):
1. Verify the FINAL ANSWER TEXT, not only pre-formulated claims (the paper grades the whole proof, issues first). A verifier pass that reads the
   delivered answer and lists every figure/assertion it contains closes the "wrong figure reached the answer" hole. Host-side complement (mine,
   deterministic, not from paper): extract all numerals from the answer text and require each to be covered by a passing check; uncovered figure =
   no vote. This also defeats vague meta-claims, because coverage is measured against the answer, not against the formulator's output.
2. Issues-first, score-after format (0/0.5/1) for the verifier: forces enumerated defects; a "1" requires zero unresolved issues.
3. Meta-verification of any FAIL/issue report before it blocks an answer: checks the issue exists in the text and justifies the verdict.
   Guards false-positive FAILs (hallucinated issues). It does not check PASS: PASS already has the +-1 % negative control; keep both.
4. Self-verification by the generator: use only as an additional signal, never the sole vote (paper: untrained generators overclaim). Cheap
   variant: require the answer to carry an explicit list of its own figures with sources, which the host then checks.
5. Adaptive verification effort: 1 pass when workers agree and all figures covered; escalate to more independent passes (paper uses 8-64) and
   lowest-confirmed-score aggregation when they disagree; unanimity as stop condition; escalate to human when valid issues are inconsistent.
6. Refinement loop: feed confirmed issue reports back to the generator, bounded iterations (paper: up to 16 in a high-compute setting).
7. Best-of-n by mean verifier score when multiple candidate answers are available.
Not applicable without training: reward shaping (R_V, R_Y, R_Z), RL against the verifier, auto-labeling to retrain a verifier, the training-time
generation-verification gap maintenance, and trust in a model's self-score as calibrated.
Differences to note: COMPUTED_CHECK is deterministic evaluation of boolean assertions (sound if assertions are correct and cover the claim); the
paper's verification is a learned, probabilistic judge. They are complementary: deterministic checks for numbers, LLM issue-report + meta-check
for prose/logic coverage. Risk: LLM verifiers share correlated errors; cross-family workers mitigate (paper does not test this).
