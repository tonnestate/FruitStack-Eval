# A/B experiment: neuromodulation-inspired strategy selection vs. uniform evolution (owner 2026-11-21)
Started 2026-11-21 ~10:40 by the director. Pre-registered here before any result.
- Arms: U = uniform random strategy choice; M = three-factor rule (two eligibility traces, lambda 0.5 / 0.8, delayed reward = gain in
  saving_bits at the largest tested size per evaluation minute, w += 0.5 r (e_fast + 0.2 e_slow), softmax choice).
- Identical: objective capp_xor (XOR_2 o THR o THR, deterministic, eps 0.05) on thr2_evaluate v2 (fresh secret seeds, held-out and
  adversarial instances, brute force on the same instances); 15 generations; 1 refine round; same strategy list; same model supply.
- Isolation: each arm draws parents only from its own verified entries plus the director baselines (agent tags arm-U / arm-M).
- Logs: staging thr-ab-U.log, thr-ab-M.log; results in desk/thr_frontier_v2.jsonl.
- Primary outcome: number of DISTINCT VERIFIED_RUN algorithms with speedup > 1 at the largest tested size. Secondary: best
  saving_bits_over_log2n; number of WRONG / INCOMPLETE runs.
- Decision rule: M counts as better only if it wins the primary outcome by a clear margin (>= 2 more distinct verified algorithms) and is
  not worse on the secondary ones; one run of 15 generations is a pilot, not a proof - a positive pilot is replicated before adoption.
  If M is not better, the biological strategy-selection idea is not expanded further.

## Interpretation caveats (owner, added 2026-11-21 ~10:50 while the arms run; the decision rule above is UNCHANGED)
- "Distinct programs" may implement the same algorithm; a single structurally new algorithm can matter more than many variants. The
  report will therefore also group the verified programs by their stated mechanism (secondary, descriptive).
- The reward "saving_bits per evaluation minute" may favour quick constant-factor gains over slow ideas with asymptotic potential.
- A positive result shows better SEARCH PRODUCTIVITY, not a complexity improvement.

## Result (evaluated 2026-11-21 11:50 by the pre-registered rule; data desk/thr_frontier_v2.jsonl, agents arm-U / arm-M)
| | arm U (uniform) | arm M (trace) |
|---|---|---|
| evaluations (incl. refine rounds) | 29 | 25 |
| VERIFIED_RUN / WRONG / INCOMPLETE | 24 / 5 / 0 | 25 / 0 / 0 |
| PRIMARY: distinct verified programs with speedup > 1 | 11 | 14 |
| best saving_bits / log2 n at the largest size | 0.782 | 0.682 |
- Rule: M better only if it wins the primary outcome by >= 2 AND is not worse on the secondary ones. M wins the primary by 3 and has
  fewer WRONG runs, but is WORSE on the best saving. => NOT a win under the rule. Pilot verdict: inconclusive; the trace policy is not
  adopted and, per the pre-registration, not expanded further on the basis of this pilot.
- Caveats: distinct programs are not distinct mechanisms (several share "half-split meet-in-the-middle"); and the measured speedups of
  this family are a POLYNOMIAL implementation effect (director attribution 2026-11-21: profile hashing merges nothing, D_L = D_R = 2^{n/2}),
  so both arms optimised constant/polynomial factors, not the asymptotic saving Lemma 3.8 needs.
