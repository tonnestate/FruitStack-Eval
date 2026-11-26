# T34 — The two ETH refutations (OpenAI, Anthropic), their common invariant, and the November transfer theorems (PI, 2026-11-17)

STATUS: sources verified and read in the original by the PI (locations below); synthesis and candidate C1 are PI derivations, NOT
independently verified. Review: FruitStack mission req-pnp-iter06.json (rewritten for this question; CherryMe workers are non-Claude
models — required because the Anthropic paper was written by Claude: conflict of interest, owner 2026-11-17). Not in the ledger.
Supersedes the scope of T33 (owner: OpenAI-only cross-mining is too narrow); T33's Navier–Stokes findings stand.

## 0. Verified source state (17 Nov 2026), local copies under literature/sources/
| source | id / location | status |
|---|---|---|
| OpenAI, The ETH is False (rev. 25 Oct) | openai/math@4eaee87 preprints/.../paper.pdf; Lean comparator SubexponentialSAT.lean `exact_count_and_sat` | read (overview, §1.1, §2) |
| Claude (Anthropic), A 2^o(n) time algorithm for 3-SAT (26 Oct) | hexagon:2610.00577v1; Lean github.com/anthropics/formal-math@16a5ce4/eth (MainResults.lean `MainTheorem`, `ETHIsFalse`) → anthropic-eth/ | read (Thm 1, §2.1–2.2, Lean statements) |
| Strassle–Subercaseaux, Simulating NTMs in subexp. deterministic time | arXiv:2611.11832 (9 Nov) | read (abstract, Thms 1–2, Lemma 1.3) |
| Krapivin–Przybocki–Subercaseaux, CNF Encoding Complexity of Boolean Functions | arXiv:2611.05614 (3 Nov) | abstract read |
| MIT Hardness Group, ETH is Dead, Long Live SH | arXiv:2611.02650 (2 Nov) | abstract read |
| Chukhin–Gajulapalli–Golovnev–Mihajlin, A Little Derandomization Goes a Long Way | ECCC TR26-313 (5/9 Nov) → eccc-TR26-313.txt | abstract read |
| Bannach–Demaine–Gomez–Hecher, #SAT→#2SAT with two calls | SOSA 2026, pp. 254–265 (arXiv:2506.06716 earlier version) | abstract (secondary) |
| Alman–Vassilevska Williams, 3SUM/APSP | arXiv:2610.06783 (5 Oct) | secondary only |
| "What the ETH Refutations Do Not Give" (6 Nov) | not found on arXiv; presumably Hexagon | NOT VERIFIED |

Exact statements that matter:
- Anthropic Lean `MainTheorem`: one machine M and constant C such that for every k ≥ 1, n ≥ 4, k-CNF φ (no repeated clauses, every
  variable occurring, m ≥ 2) M outputs #φ within 2^{C·min{k m/√log m, k² n loglog n/√log n}} steps. Bound in m without sparsification;
  sparse case 2^{O(kn/√log n)}.
- OpenAI Lean `exact_count_and_sat`: count + SAT bit in (L+1)^{O_k(1)} 2^{O_k(n (loglog n)²/√log n)}, polynomial visited space; manuscript
  sharper; Theorem D.1 (tensor contraction) proves both bounds of Thm 1.1.
- Strassle–Subercaseaux Thm 2 (transfer): if circuit-CSP with n variables, arity ≤ k(n), constant density is solvable in 2^{O(n/s(n))}
  poly(|Φ|), then NTIME[t] ⊆ DTIME[2^{O(t/k(t))}·2^{O(t/s(t))}]. Lemma 1.3 (from [Ope26, Thm D.1] and [Cla26, Thm A]): circuit-CSP with
  arity ≤ n^{9/10} and constant density in 2^{O(n/√log n)} poly(|Φ|). Hence Thm 1: NTIME[t] ⊆ DTIME[2^{O(t/√log t)}] (t ≥ n), counting
  version too. Quasilinear Cook–Levin alone would give only 2^{O(t√log t)} — they avoid it by block-respecting simulation into
  large-arity constraints.

## 1. The common invariant of the two proofs (answer to the owner's main question, part 1)
Both write #F = Σ_x Π_e Φ_e (sum of products of local factors) and both must beat the SAME obstruction: on expander-like formulas every
balanced cut is crossed by Ω(n) bits, so any fixed cut/contraction tree costs 2^{Ω(n)} (Anthropic §2.2 says this explicitly; it is T31
Theorem C2 for the fixed network). Both beat it by a SIGNED ALGEBRAIC REWRITING of the consistency (copy/equality) constraints:
- Anthropic: an edge "costs c bits" if Ψ(z_a, z_b) = Σ_{θ∈{0,1}^c} f(z_a,θ) f'(z_b,θ) with INTEGER-valued (possibly negative) f, f';
  pairs of equality edges are rewritten (eight-square identity) into parity "hyperedges" on four nodes, then merged — the total
  crossing cost drops while parts stay small.
- OpenAI: linear substitutions depending polynomially on an interpolation parameter decouple groups after fixing few integer linear
  "measurements"; the number of measurements is bounded by rank(I − M0) for an auxiliary rational matrix M0 built from a polynomial
  that interpolates (−1)^j on a short interval in commuting permutation matrices; Hermite interpolation recovers H(0) = #F.
Common invariant (PI formulation, to be checked): the cost of decoupling an interface is not its support size or Boolean/nonnegative
rank, nor treewidth, but a SIGNED (integer/rational) factorization rank of grouped equality constraints, made small by low-degree
representations of PARITY/sign characters ((−1)^j interpolation; parity hyperedges). Both proofs therefore exploit cancellation in
exactly the place where monotone/contraction methods have provable 2^{Ω(n)} lower bounds — the same "representation change beats a
fixed-representation lower bound" pattern as T31 C2 (XOR-SAT) and T32 E1, now for ALL k-CNF up to a 2^{o(n)} factor.
Consequence for PNP-001: confirmed again that contraction width / cut rank of a fixed network is not a lower-bound invariant (T31);
any lower-bound invariant must be stable under signed rewritings of equality constraints.

## 2. What follows from combining the invariant with the transfer theorems (part 2)
Direction matters: SAT algorithm → NTIME simulation (Strassle–Subercaseaux) transfers UPPER bounds; it cannot give P ≠ NP. The
lower-bound direction is Williams' algorithmic method (T21, T23): fast Circuit-SAT for a class C ⇒ NEXP or E^NP ⊄ C.
(a) Effect on T28 (my open question, Lemma G): with constraints of arity up to N^{9/10} allowed (Lemma 1.3), Lemma G's bound
    |S| ≥ CircuitSize(f)/2^w becomes VACUOUS. T28-open must be restated: does every size-n^k circuit on n inputs admit a perfectly sound
    circuit-CSP encoding with N ≤ (1 − o(1)) n √log n / C variables, constant density and arity ≤ N^{9/10}? A YES gives Circuit-SAT in
    2^{n − ω(log n)} for SIZE(n^k) and, by Williams, NEXP ⊄ P/poly — a major statement, still NOT P ≠ NP. Status: OPEN; no
    counting obstruction (constraint circuits may be large).
(b) Candidate C1 (PI, NOT verified, novelty unchecked): Valiant's depth reduction removes O(s/loglog n)·(depth factor) edges from a
    fan-in-2 circuit of size s = c·n and depth O(log n) so that every remaining output depends on ≤ n^ε cut edges/inputs. Guessing the
    removed edges gives a circuit-CSP with N = n + O(n/loglog n) variables, O(n/loglog n) constraints of arity n^ε (ε < 9/10), so
    Lemma 1.3 decides it in 2^{O(n/√log n)} — far below 2^n/n^{ω(1)}. Pushing s to n·g(n) with N/√log N ≤ n − ω(log n) allows
    g ≈ √log n · loglog n / C. Plugged into the JMV local-reduction pipeline (as in T23) this would give: E^NP ⊄ SIZE-DEPTH(c' n √log n
    loglog n, O(log n)) infinitely often — slightly beyond the c n √log n of OpenAI Cor 1.4 but only for logarithmic depth. To check:
    (i) Valiant's exact edge count for size n·g; (ii) that JMV's construction keeps depth O(log n); (iii) whether Strassle–Subercaseaux
    or the OpenAI/Anthropic consequence sections already state it. Classification now: CONDITIONAL on (i)–(ii), novelty OPEN. Relevance:
    restricted-class lower bound for E^NP; NOT P ≠ NP.
(c) NTIME[t] ⊆ DTIME[2^{O(t/√log t)}] with hierarchy theorems: an upper bound; combined with the nondeterministic time hierarchy or PPST
    (DTIME(n) ≠ NTIME(n)) it yields no superpolynomial separation. No P ≠ NP consequence.

## 3. Corrections to the forwarded research summary (owner's message 2026-11-17)
- "NE ⊄ SIZE(2^n/2n) would have considerable consequences for NP by padding": FALSE direction. Padding transfers circuit lower bounds
  from smaller to larger time classes (NP-hard ⇒ NE-hard), not from NE down to NP. TR26-313's first alternative gives no NP lower bound.
- TR26-313 itself: an unconditional disjunction (NE needs near-maximal circuits OR VP⁰_Z ≠ VNP⁰_Z); it decides neither. It is a
  Kabanets–Impagliazzo-type result made unconditional by integer low-degree PIT; relevant to our GCT/permanent line as a framework, not
  as a lever for P ≠ NP.
- SH / Weak ETH (arXiv:2611.02650): rules out 2^{O(n^{1−ε})} L^{O(1)} for 3SAT; consistent with both refutations; it is a hypothesis,
  not a theorem.
- #SAT → two #2SAT calls (SOSA 2026): count-preserving, hardness stays in #2SAT (#P-complete); no complexity collapse. Consistent with
  our earlier subtraction finding.
- Bürgisser–Ikenmeyer–Panova (no occurrence obstructions, JAMS 2019): correctly stated; already reflected in T11/T18.

## 4. Decision
New main question adopted (owner): common invariants of the two SAT proofs and their consequences with the transfer theorems.
Result so far: shared invariant = signed factorization rank / parity-character representation of equality constraints (§1); the only
lower-bound-direction consequences are Williams-type and stay in E^NP/NEXP vs restricted circuit classes (§2b) or the restated T28 (§2a).
Neither touches P ≠ NP. Independent verification by FruitStack (iteration 6), then decide whether §2b is worth a full proof.
