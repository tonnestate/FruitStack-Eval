# SER H3 evaluation (PAPER.md §3.2, §5.1)

Standalone, deterministic evaluation of the localization prior. No FruitStack imports, no network.
Dependencies: Python 3.11+, numpy, scipy (pytest for tests). All present on Kaggle images.

```
python ser_h3.py digest                                   # config + prompt digest for preregistration
python ser_h3.py run --tasks TASKS/ --out OUT/            # arms A, B
python ser_h3.py run --tasks TASKS/ --out OUT/ --filter my_gemma:generate   # arms A, B, C
python -m pytest -q                                       # 11 tests, synthetic data
```

Output: `OUT/traces.jsonl` (per task: gold, seeds, filtered seeds, raw filter response, top-20 per arm,
metrics, timings, source file hash), `OUT/summary.json`, `OUT/summary.md` (table for PAPER §5.1).

## Input: one JSON file per task (the only part an adapter must produce)

```json
{
  "task_id": "repo__123",
  "issue": "full issue text",
  "symbols": [
    {"id": "n17", "file": "pkg/core.py", "name": "parse", "qualname": "pkg.core.Parser.parse",
     "signature": "(self, raw)", "text": "source body", "start_line": 40, "end_line": 72}
  ],
  "edges": [["n17", "n23", "calls"], ["n3", "n17", "contains"]],
  "gold_patch": "unified diff of the reference patch (pre-patch line numbers)",
  "dense_ranking": ["n23", "n17", "..."]
}
```

- `symbols`, `edges`: from the competition graph for the task's snapshot. Line numbers refer to the
  pre-patch snapshot. If raw `graphs/` files are not available, rebuild nodes/edges via
  `get_code_neighbors` and record that in PAPER §3.1.
- `dense_ranking` (optional): symbol ids returned by `search_similar_code(issue, k)` in rank order.
  Omit it for **all** tasks if unavailable; arm A then is BM25 only.
- `gold_patch` is read only for scoring. It never reaches seeds, PPR or the Gemma prompt.
- Edge types: by default all types count as content edges. To restrict, set
  `CONFIG["content_edge_types"]` **before** the preregistration commit (it changes the digest).

## Gemma filter (arm C)

`--filter module:function` takes a function `generate(prompt: str) -> str` that returns the raw
text of `gemma-4-31b-it-qat-w4a16-ct` for the given prompt (greedy decoding). Prompt construction
(`FILTER_PROMPT`), parsing and the fallback rule are fixed in `ser_h3.py`. The model can only
remove seeds; an empty or unparseable answer falls back to the unfiltered seeds and is counted.

## Frozen parameters (`CONFIG`)

alpha 0.5 · 10 top seeds + up to 10 verbatim-name seeds (length >= 4, no dunders) · RRF k = 60 ·
arm-A top 3 protected inside top 10 · Recall: symbol @10, file @1/@5 · paired bootstrap (10,000,
seed 0) and Wilcoxon signed-rank · non-inferiority margin 0.02 on the direct subset.

## Gold-location rule

Modified pre-existing `.py` files from the reference patch. Gold symbols are the innermost symbols
whose span contains a removed/changed old line, or strictly encloses an insertion point (symbol
starts at or before the line above the insertion and ends at or after the line below). New files are
excluded; lines outside any symbol are counted as `unattributed_lines`. Tasks without gold symbols
are excluded from symbol recall but kept for file recall.
