# Independent H3 mathematical verification — 2026-11-10

**Independent check outcome: 8 passed / 0 failed.**

This is an independently implemented **technical verification** of H3's mathematical and statistical primitives. It is **not** a new SWE-bench experiment, additional confirmatory sample, Gemma/PlumMe inference, or evidence that H1/H2 repairs succeed.

## Provenance and execution

- Source: `gemma_h3_independent_checks.py` in this directory.
- Execution: Python + NumPy + SciPy + pytest in the independent assistant runtime, 2026-11-10.
- Observed terminal output: `8 passed in 0.93s` (pytest).
- The checks do **not** import `h3_eval/ser_h3.py`; they implement small mathematical components independently.
- Existing primary H3 code, task manifest, raw traces, preregistration, and manuscript were **not modified**.

## Eight executed checks

1. Personalized PageRank on a two-node graph agrees with the analytical solution at alpha 0.5.
2. PageRank probability mass is conserved with dangling nodes.
3. Graph propagation reaches connected multi-hop nodes but not disconnected nodes.
4. The direct-retrieval top three remain inside the protected top ten.
5. Reciprocal rank fusion (RRF, k=60) follows the specified rank and tie ordering.
6. Paired bootstrap and signed-rank logic return the expected null case.
7. Paired bootstrap and signed-rank logic detect an all-positive case.
8. Frozen alpha and RRF-k constants match the preregistered settings.

**Interpretation:** The eight invariants held on synthetic inputs. They do **not** establish that the complete production evaluator is defect-free or that SER improves real software repairs.

## Primary H3 results — arithmetic cross-check only

The following values are taken from the **existing primary** `evidence/h3_confirmatory/summary.json` (497 tasks, 478 with gold symbols). They are **not** independent benchmark runs:

| Metric | A (BM25) | B (+ PPR) | B−A |
|---|---:|---:|---:|
| Symbol Recall@10 | 0.385547910 | 0.401421341 | +0.015873431 |
| File Recall@1 | 0.292152918 | 0.297283702 | +0.005130785 |
| File Recall@5 | 0.614012647 | 0.635474753 | +0.021462106 |

The primary pipeline reports a paired 95% bootstrap interval of **[+0.007348, +0.025811]** for B−A Symbol Recall@10 and 15 improved versus 0 worsened tasks. Subtracting its reported A and B means independently confirms the displayed mean difference, but the underlying task-level statistics have **not** yet been independently rerun in this validation.

## Reproduction

From the research directory:

```bash
python -m pytest -q evidence/independent_validation/gemma_h3_independent_checks.py
```

Run the next independent analysis against the **already committed** `evidence/h3_confirmatory/traces.jsonl.gz`, task manifest, and summary. Reconstruct Symbol Recall@10 from each task's ranked symbol IDs and gold symbols, rerun the paired bootstrap, and explicitly verify pilot exclusion and manifest coverage before reporting task-level agreement. Keep such results in this independent-validation directory, not in the original confirmatory dataset.

**Limitations:** H3 C results and H1/H2 repair outcomes were not independently executed. File recall requires a symbol-to-file mapping to recompute independently; averaging precomputed file metrics is not a full revalidation. No claim about primary outcome validity, gold-patch attribution, or causal effects follows from the 8/8 synthetic test result.


## Trace-level independent audit utility added

`independent_h3_validation.py` is also committed in this directory. It is independent of the primary `ser_h3.py` module and offers two modes:

```bash
cd research/gemma4-developer-agent-paper-2026
python evidence/independent_validation/independent_h3_validation.py --self-test
python evidence/independent_validation/independent_h3_validation.py \
  --traces evidence/h3_confirmatory/traces.jsonl.gz \
  --manifest h3_eval/TASK_MANIFEST.json \
  --reported-summary evidence/h3_confirmatory/summary.json \
  --out evidence/independent_validation/H3_INDEPENDENT_AUDIT.json
```

The independent 8-check mode passed locally, and synthetic end-to-end trace ingestion plus deliberate per-task recall tampering detection both passed. **No completed raw-trace audit is claimed yet**: the second command has been provided for execution where the already committed gzip trace and manifest are checked out together. It will independently recompute symbol recall and paired statistics from recorded rankings and gold-symbol IDs and fail loudly on disagreement. Preserve the generated audit JSON as a separate secondary validation receipt.
