# PNP-001-EGC-001 - escalating graph transducers: model and simulation theorem (director draft 2026-11-21; CLAIMED, needs independent review)
Contract: owner message 2026-11-21 "ADDENDUM: ESCALATING GRAPH COMPUTATION" (subordinate to Q-08a1c5b68f / Lemma M).

## A. Model (deterministic)
Configuration G = (V, E, W, a, Q) encoded as a bit string of length S_graph (node ids, adjacency, weights/typed rules, activities, local
memories, pending-event queue, scheduler state - everything). One external bit x_t is appended to Q as an input event. A deterministic
scheduler sched(G) returns the next event e (or QUIESCENT); an event applies a local rule rho to the addressed node's record and its
incident records and may enqueue events, add/delete edges or nodes, change weights. Rules are fixed (uniform family: rho and sched are
computable by a fixed program; non-uniform: may depend on n). Per input t: events e_1..e_{k_t} until QUIESCENT; non-termination within
the budget = failure. Resources: S_graph (max over t), work W_t = sum of event costs in the chosen machine model, depth D_t (longest
dependency chain), decoder D_out. Escalation statistics (branching ratio sigma_t, cascade length, peak activity) are DESCRIPTIVE.

## B. Simulation theorem (claimed)
Let a deterministic escalating graph transducer solve total search-MCSP^A[s] (or any stream problem) with configuration size S_graph,
and per-input event count k_t, each event reading/writing O(1) records of O(log S_graph) bits plus a scheduler step of the same kind.
(i) RAM with word size O(log S_graph): a one-pass streaming machine whose state IS the configuration performs the update in
    O(k_t) word operations (+ the scheduler's cost), space O(S_graph).
(ii) Multitape TM (MMW's model): update time O(k_t * S_graph) (each record access may traverse the tape); space O(S_graph).
(iii) Per-step circuits: F_t of size O(k_t * S_graph * log S_graph) (one memory read/write = multiplexer over S_graph bits per event);
     decoder cost unchanged.
Proof: unroll the event loop (deterministic scheduler, termination within k_t), simulate each event by addressed memory access
(RAM: O(1); TM: one sweep; circuit: MUX/DEMUX of size O(S_graph log S_graph)). Dynamic topology is part of the configuration, so
rewiring is ordinary memory writes. Uniformity is preserved when rho and sched are uniform. Parallel depth is not a resource of the
MMW model; a parallel cascade of depth D and work W is simulated sequentially in O(W) events. Conversely every streaming transducer is
a one-node graph. QED (sketch; independent review required, in particular the event-cost assumption).
Consequence: escalating graph transducers and one-pass streaming algorithms coincide up to POLYNOMIAL overhead in (S_graph, W_t):
poly-space/poly-work graphs give poly-space/poly-update streaming algorithms and vice versa. Hence:
- Lemma M / QE* is invariant under passing to escalating graphs: a graph cannot break M unless a streaming algorithm can, and a
  lower bound for streaming applies to graphs with the same polynomial resources.
- Escalation (amplification, feedback, rewiring) can change CONSTANT or POLYNOMIAL factors and the work/depth split, never the
  polynomial-vs-super-polynomial question that Lemma M is about. H5 (complexity-theoretic relevance) is therefore NOT a route to M.
- Open in finite experiments only: whether graph mechanisms find smaller finite (S, W, D) points than direct SAT synthesis (H1-H4),
  which is OBSERVED-level engineering information.
Missing assumption that would break the theorem: events with unbounded fan-in work per event counted as O(1) (e.g. a "global
aggregation" event over all nodes) - then W_t must count the aggregation size; with honest accounting the theorem holds.
