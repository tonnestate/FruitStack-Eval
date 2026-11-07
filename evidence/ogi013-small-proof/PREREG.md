# OGI-013 small advantage test (S1) — preregistration, written BEFORE any provider call

Status: LOCKED at the commit that contains this file (selection.json and this text). Descriptive/stratified test, **not** a confirmatory study.

**Question.** Does the Luna + nemotron duo under the Brother closed loop (arm T, `run_T(duo=True, loop=True)`, commit 24d1eac) answer correctly more often than Luna alone, and not worse than nemotron alone?

**Items.** 198 QA-2D MMLU-Pro items with a recorded Luna single answer (SL, accuracy 149/198 = 0.7525). Two strata, drawn with seed 20261107 from items never run in QA-2D (no T/SN/E row; the 4 recorded disagreement rows are excluded): W = 8 items where Luna was wrong (pool 37), R = 8 items where Luna was right (pool 108). List: selection.json.

**Arms.** T (duo + loop) and SN (nemotron alone) on each of the 16 items. Luna alone = recorded SL (no new call).

**Primary estimate.** Duo accuracy on the population = (49/198)·rescue + (149/198)·(1−harm), where rescue = share of W items T answers correctly, harm = share of R items T answers wrongly. Same estimator for SN. Luna alone = 0.7525 by construction. Exact (Clopper–Pearson) 95% CIs for rescue and harm; report counts.
**Advantage is claimed only if** the lower CI bound of the estimated duo accuracy exceeds 0.7525 AND T is not below SN's estimate. Otherwise: no advantage shown. With n=8 per stratum this can only happen for a large effect; a smaller effect is reported as "not established", never as a result.

**Failure handling.** Infra failures (no retry) are reported as missing and counted against T (worst case) in a sensitivity line. No tuning, no loop-parameter change, no item swap after the first call.
**Caps.** RunBudget 500 provider requests, about 600k tokens total; stop and report if reached. Zero cash, no paid route, no Claude, one process.
**Not claimed.** No organisational added value beyond this item set; items were sampled from a set that was hard-ish for Luna; stratification corrects that only through the stated weights.
