# Addendum to EXECUTE_NOW_LUNA.md (2026-11-09, from Claude review)

Binding on top of `EXECUTE_NOW_LUNA.md`. Where they conflict, this addendum wins.

1. **Model.** Use only `gemma-4-31b-it-qat-w4a16-ct` for every arm and for the Gemma recognition
   filter. Remove the E4B alternative from the PAPER.md header.
2. **H3 is ready to run: use `h3_eval/ser_h3.py`.** It is standalone, deterministic and tested
   (11 tests, `python -m pytest -q` in `h3_eval/`). Do not rebuild H3 inside FruitStack. Your only
   job for H3: write the per-task JSON adapter described in `h3_eval/README.md`, record
   `python ser_h3.py digest` in the preregistration commit, then run arms A/B (no GPU) and C
   (`--filter module:generate` wrapping Gemma 4 31B, greedy). Paste `summary.md` into PAPER §5.1.
3. **Query encoding.** Use the official `search_similar_code(query, k)` as `dense_ranking` (the
   dense component of arm A). If it is unavailable, omit `dense_ranking` for **all** tasks and say
   so in PAPER §3.2. Fill §3.1 with the actual node and edge types.
4. **Graph.** PPR needs the full content-edge graph. Load raw `graphs/` files if available;
   otherwise reconstruct via `get_code_neighbors`, cache per snapshot with a digest, and state
   this in §3.1.
5. **Priority order under compute limits:**
   (a) H3 on all eligible dev tasks;
   (b) E vs E-minus paired on as many tasks as the budget allows;
   (c) D-star only if (b) is complete.
   Freeze n before the confirmatory run. Report H1/H2 as effect estimates with 95% CI. If
   discordant pairs are too few, label the result "inconclusive"; never claim "no effect".
6. **Mechanistic secondaries, always reported:** trigger rate, gold symbol present in the eligible
   pool at trigger time, wrong-trigger rate (refuted symbol was actually gold), persistence after
   PATCH_NO_EFFECT. With a ~15% base resolve rate these carry most of the evidence.
7. **Budget.** Assume about 6 min per task per arm on L4x4 (12 h for all tasks in official
   scoring). Measure in the timing pilot before fixing n.
8. **Agents under test run Gemma only.** FruitStack may orchestrate, log and grade, but no other
   model may generate, filter or rank inside any arm.
