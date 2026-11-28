# Check of the recoding bounds (Claude Code, 2026-11-21, on owner request) - verified mathematics level, no novelty claim

Model: |Q| = m, S = ceil(log2 m) state bits, encoding psi: Q -> {0,1}^S injective (stationary), CC = fan-in-2 gates over a fixed complete
basis; values on unused codes are free. Circuit count: at most 2^{O((G+R) log(G+R))} circuits with G gates on R inputs/outputs.

1. Conjugacy-class-size argument: WRONG (owner correct). One m-cycle -> x+1 mod m, O(log m) gates, class size (m-1)!.
2. H_1(m) >= Omega(sqrt m / log m): CORRECT, with one gap closed here. If m < 2^S a single circuit C can realise SEVERAL cycle types
   (every C-invariant m-subset of codes that is a union of C-cycles). Number of sub-multisets of a partition of n = 2^S < 2m is at most
   prod(mult_i + 1) <= exp((1+o(1)) sqrt(2n)) <= exp((2+o(1)) sqrt m) (Lagrange optimum mult_i ~ K/i - 1, K = sqrt(2n)), while
   p(m) = exp((pi sqrt(2/3) + o(1)) sqrt m) = exp(2.565.. sqrt m). Hence #circuits >= exp(0.56 sqrt m) and G = Omega(sqrt m / log m) still
   follows. (For m = 2^S, psi is a bijection and the gap does not arise.)
3. H_1(m) <= O(sqrt m (log m)^2): CORRECT. d <= sqrt(2m) distinct lengths; per length block j: comparator x >= a_j (O(log m)), end test
   (x - a_j + 1) == 0 mod l_j by a bit-serial remainder (O(log m log l_j) = O(log^2 m)); OR / mux of the end flag and l_j over d blocks
   (O(d log m)); one incrementer, one subtractor, one mux (O(log m)). Total O(sqrt m log^2 m).
   => Omega(sqrt m / log m) <= H_1(m) <= O(sqrt m log^2 m); a random permutation does NOT need Omega(m) gates after optimal recoding.
4. Pairs (delta_0, delta_1): CC = Omega(m) for some pair under every common encoding: CORRECT. m^{2m} pairs vs encodings
   <= (2m)!/m! = 2^{m log m + O(m)} times shared circuits 2^{O((G+S) log(G+S))}; G <= eps m fails for small eps. Shared gates are counted.
   Tight: every pair has CC = O(2^S) = O(m) (Lupanov per output bit), so the pair bound is Theta(m).
5. Padding: R <= (2 - eta) S  =>  exists pair with CC_E = Omega(eta m) for every injective stationary E: Q -> {0,1}^R. CORRECT:
   encodings <= 2^{R m}, so 2^{R m} * 2^{O((G+R) log(G+R))} >= 2^{2 m S} forces G log G >= Omega(eta m log m). At R >= 2S the COUNTING
   PROOF fails (the encodings alone can carry 2 m S bits); this is NOT a proof that the lower bound fails at R >= 2S - whether every pair
   becomes cheap with 2S..O(m) padding bits is OPEN (no construction known here). Not covered: several codes per abstract state, time-varying encodings.
Open: explicit (constructive) hard pairs; time-varying / redundant representations. Literature to check before any novelty claim:
state-assignment complexity of sequential machines (Hartmanis-Stearns line), circuit complexity of permutations up to conjugation.
Formalisation: counting bounds need circuit-counting and partition asymptotics in Lean/Mathlib - feasible but large; not done here.

## Revision 2026-11-21 (owner request; claim labels used in PNP-001 question Q-see-ledger)
Claim A = item 2+3 (single permutation, Omega(sqrt m / log m) <= H_1(m) <= O(sqrt m log^2 m), constructive upper bound in item 3).
Claim B = item 4 (pairs, Theta(m) under any common stationary injective encoding with S bits).
Claim C = item 5 (padding R <= (2-eta)S keeps Omega(eta m); counting proof silent at R >= 2S, lower bound itself undecided there).
Finite check: function pairs on 4 states up to simultaneous relabeling = 2,836 orbits (exhaustive enumeration over 4^8 pairs and S_4;
Burnside: (65536 + 6*256 + 3*256 + 8*16 + 6*16)/24 = 68064/24 = 2836). Earlier differing counts are wrong.

## Literature comparison (from memory - verify exact statements before citing)
- Hartmanis-Stearns (Algebraic Structure Theory of Sequential Machines, 1966): state assignment via partitions with the substitution
  property / partition pairs - which encodings make next-state bits depend on FEW state variables (reduced dependence, decompositions).
  Structural, not gate-count lower bounds over all encodings. ESTABLISHED; A-C do not follow from it and do not contradict it.
- Shannon counting + Lupanov synthesis: almost all functions of n inputs need ~2^n/n gates and all have <= (1+o(1)) 2^n/n. B is
  Shannon-Lupanov counting lifted to orbits under relabeling (the m! encodings cost only m log m bits of the 2 m log m). B's tightness
  Theta(m) = Lupanov. ESTABLISHED technique; B and C are routine corollaries (novelty unlikely, possibly unstated in this form).
- POTENTIAL NOVELTY (literature not yet checked): A's two-sided sqrt(m) scale for permutations up to conjugation (partition-function
  lower bound with the sub-multiset correction; cycle-length-block upper bound), and C's explicit (2-eta)S padding threshold.

## Bridge D (exactly one): does any representation-invariant transition lower bound survive time-dependent encodings, one-to-many
## physical representations and amortised computation?  Status: OPEN; three proved observations delimit it.
D1 (proved, elementary): with one-to-many codes and UNBOUNDED R, transitions cost O(1) gates: keep (table, input history) in a shift
   register (a shift is wiring, 0 gates; insert b). Every code (table, w) represents q = delta_w(q_0). Hence no per-step lower bound can
   survive without (i) a bound on R and (ii) a readout/decoding requirement.
D2 (proved, elementary): with amortisation (micro-steps) gate count per micro-step is not invariant: store the 2m-entry transition table
   in a rotating ring (rotation = wiring), compare a counter with (q,b) and latch the matching entry: O(log m) gates per micro-step,
   2m micro-steps per abstract step, work O(m log m). The candidate invariant is WORK (gates x micro-steps) per abstract step.
D3 (contrast): in the cell-probe / RAM model one transition costs O(1) probes (table lookup). Any surviving bound must therefore use
   the absence of random access in circuits (locality of wires/gates), i.e. it is model-specific.
OPEN QUESTION D: for R = poly(m) bits, codes possibly one-to-many and time-dependent, readout of q within poly(log m) work, is the
   amortised work per input Omega(m / polylog m) for SOME pair (delta_0, delta_1)? Counting over circuits no longer suffices (the table can
   sit in the code); a proof would be a time-space style circuit lower bound for online pointer chasing. Not claimed. No transfer to
   online reconstruction is claimed.

## Frage 1 focus (owner 2026-11-21): information vs. computation - check by Claude Code
- DISJ_n (a then b, one pass): memory >= n bits (fooling: a != a' differ at i, b = e_i) and O(1) gates per update (a_i wired into cell i,
  r <- r OR (a_i AND b_i)) with time-dependent wiring: CORRECT. High communication complexity does NOT force high Boolean update cost.
- INDEX: data-then-address forces memory >= n (one-way CC of INDEX) and is still cheap: keep the data, halve the candidate block per
  address bit (n/2^j muxes at address bit j, O(n) gates in total, O(1) amortised per input bit). Address-then-data needs only
  log n + 1 bits and O(log n) gates per data bit. Below the capacity bound no algorithm exists at all: capacity, not a time-space tradeoff.
  CORRECT. The owner's ROBP remark (phase boundary address-before-data not given for non-oblivious read-once BPs) is accepted.
- Karchmer-Wigderson: KW-game communication = circuit DEPTH; the number of protocol leaves = FORMULA SIZE. Neither covers circuit size
  with shared gates. CORRECT; addendum: formula size is the KW quantity closest to the target, but sharing (circuits) is not covered.
- Structural fact for the target theorem type: unrolling an exact one-pass realisation gives an ordinary circuit for L_n of size
  sum_t CC(F_t) + CC(D_N) whose every cut between input positions t and t+1 carries <= S wires. Hence
  (i) every circuit lower bound for L_n is a lower bound for B(n) (with any S); (ii) a bound B(n) for a fixed S(n) is exactly a lower bound
  for circuits with ONLINE CUT-WIDTH <= S(n) (inputs in stream order). Time-dependent codes, redundancy, shared gates and deferred
  computation are all inside this circuit class automatically. For S >= N the question is unrestricted circuit complexity of L_n; for
  S = polylog N and L_n = MCSP it is the MMW streaming target (Thm 1.3: poly(s) update time => P != NP), i.e. magnification territory.
  Whether explicit superlinear bounds (B(n) >> N) are known for online cut-width S circuits in some regime S(n): NOT KNOWN TO ME -
  literature check needed (branching-program time-space tradeoffs, Ajtai / Beame-Saks-Sun-Vee, are for general read orders).
- OPEN FOCUS GAP (registered as the single remaining question of Frage 1): explicit L_n and S(n) with min over exact one-pass
  realisations of sum_t CC(F_t) + CC(D_N) >= B(n) where B(n) exceeds the store-and-read-out cost (B(n) = omega(N) for S(n) < N). No such
  bound is claimed; no transfer to online reconstruction or P vs NP is claimed.
