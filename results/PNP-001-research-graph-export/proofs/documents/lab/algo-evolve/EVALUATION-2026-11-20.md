# Algorithm Evolution Engine - first evaluation (2026-11-20)
Code: physalis-mathverify branch cc/algo-evolution, commit cf671eb (src/physalisme/algoevolve.py, tests/test_algoevolve.py, 5 tests pass);
driver Aurora-sync integration/algo_evolve_cycle.py (d065c7a). Isolated lab: scratchpad evo-run2 (data copy of the staging reference,
own state dir); generated code ran only in the PhysalisMe Code Mode sandbox. Not deployed.
Problem: positive 1-in-3-SAT, exact #SAT labels (786 reference instances at start; 949 after adversarial rounds).

Run (seed 1): generation 0 = systematic enumeration of all 19 one-step programs; generations 1-4 with 6 children each (insert, delete,
swap, param, replace, crossover; operator choice weighted by credit). 43 evaluated: 32 SOUND, 7 VACUOUS, 4 INCORRECT (mod 4 - rank_mod is
only correct for prime moduli - and density 0.7, rejected with counterexamples). Best selection-split coverage 0.9953 (gen 0, branch 4)
-> 0.9984 (gen 1, anneal 2000 + branch 4; gen 3 swap gives branch 4 + anneal 2000); held-out coverage 0.9931. Operator credit after the run:
crossover 0.50, delete/swap 0.33, insert 0.27, param 0.25, replace 0.20.

Verification gap found and closed (CEGIS): the deliberately unsound op density 0.5 ("m < n/2 => SAT") was SOUND on the static reference
(no counterexample in it) and entered the front alone and inside a crossover child. A champion-only adversarial round found nothing. With
new problem-family moves (pad with unused variables; plant a small UNSAT core from the reference) the generator found two UNSAT
instances (n = 19, m = 8 and m = 9) answered SAT; they joined the reference permanently. Re-evaluation: density 0.5 -> INCORRECT (2 wrong),
density 0.5 + branch 4 + anneal 2000 -> INCORRECT (2 wrong), branch 4 + anneal 2000 -> SOUND (coverage 0.9958 of 949).

Cross-domain operators (registry in algoevolve.CROSS_DOMAIN): anneal (statistical physics, Metropolis/annealing; one-sided SAT witness,
checked) - part of the best algorithm; fba (flux-balance analysis, LP feasibility of A x = 1, 0 <= x <= 1; one-sided UNSAT) - sound in tests
and on the reference; proof obligation: exact rational Farkas re-check before any claim relies on one LP answer.

Category of every result: finite evidence on a finite reference domain. No algorithmic improvement beyond known methods is claimed (bounded
DPLL, propagation and annealing are standard). Limits: meta-learning is a credit table, not TPOT; adversarial search budget small;
selection objective is coverage, not asymptotic behaviour; R-MCSP / Track B application not started.
