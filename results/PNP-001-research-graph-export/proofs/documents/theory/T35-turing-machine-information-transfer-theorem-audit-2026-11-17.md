# T35 — PNP-001 Turing Machine Information-Transfer Theorem Audit (PI, 2026-11-17)

STATUS: integrates T27, T31, T34 with the block-simulation theorem of Strassle–Subercaseaux (read in source) and OpenAI #137. New PI
lemmas B1, U1, D1 below are elementary; correction K1 narrows T31 Theorem C1. NOT independently verified: FruitStack mission
req-pnp-iter07.json (chained after iteration 6). Not in the ledger.
Legend: [PUB] published fact (source read), [DED] PI deduction (proof given), [CONJ] conjecture/open, [CAND] candidate needing check.

## 1. Verified inventory
| # | statement | model | status |
|---|---|---|---|
| H | Hennie 1965: palindromes need Ω(n²) on 1-tape TMs; via crossing sequences ≥ communication (Kushilevitz–Nisan Ch. 12) | 1-tape, input on work tape | [PUB, classical] |
| P | Paterson 1972: one-tape time t ⊆ space O(√t) (crossing-sequence based) | 1-tape | [PUB, classical, not re-read] |
| O137 | OpenAI #137 (openai/math, Simulating-One-Tape-Time-in-Two-Fifths-Power-Space-September-25-2026): one writable tape + read-only input heads, outcome up to time T in O(T^{2/5} polylog T) space | offline 1-tape | [PUB, abstract read; Lean doc 137 exists] |
| HPV | Hopcroft–Paul–Valiant 1977: DTIME(t) ⊆ DSPACE(t/log t); every multitape (N)TM can be made b-block-respecting with constant overhead | multitape | [PUB, used as Lemma 3.1 in 2611.11832] |
| W25 | Williams 2025: DTIME(t) ⊆ DSPACE(√(t log t)) | multitape | [PUB, not re-read] |
| PF | Pippenger–Fischer 1979: oblivious simulation, time-t TM → circuits of size O(t log t); Cook 1988 quasilinear Cook–Levin: O(t log t) variables | multitape | [PUB, classical] |
| B | Bennett 1973/1989: reversible simulation, time O(t^{1+ε}), space O(s log t) | multitape | [PUB, classical] |
| PPST | Paul–Pippenger–Szemerédi–Trotter 1983: DTIME(n) ≠ NTIME(n), via DTIME(t) ⊆ Σ4TIME(t/log* t) | multitape | [PUB, classical] |
| SS | Strassle–Subercaseaux arXiv:2611.11832, Lemma 2.1 + Thm 2 + Lemma 1.3: NTIME[t] ⊆ DTIME[2^{O(t/√log t)}], t ≥ n, also counting accepting paths | multitape NTM | [PUB, read] |
| ETH | OpenAI Thm 1.1 / D.1; Claude (Anthropic) Thm 1, Thm A (T34 §0) | k-CNF / circuit-CSP | [PUB, read] |

Machine-model transformations (exponent changes only, no class changes): 1-tape ↔ multitape T ↦ O(T²); d-dim tapes → 1-tape
polynomial; RAM (log-cost) → multitape polynomial; multitape → uniform circuits O(T log T) (PF); reversible: T ↦ O(T^{1+ε}) (B).
Superpolynomial bounds are invariant under all of these; polynomial exponents are not (PAL: n² vs n).

## 2. Reconstruction of the block simulation (WP2) — the exact operation responsible [PUB, 2611.11832 §2.1]
1. HPV normal form: M is b-block-respecting (each head stays in one block of b cells during each epoch of b steps).
2. Enumerate the head-movement pattern π ∈ {L,S,R}^{d(t/b−1)}: 2^{O(t/b)} branches, deterministic. π fixes the DATA-FLOW GRAPH between
   epochs (which earlier epoch last wrote each block read now).
3. For fixed π: variables = block contents + state/heads at epoch boundaries — O(t) variables in total; one constraint circuit per epoch
   (arity O(b), size O(b log b) via PF), each variable shared by ≤ 2 constraints (density ≤ 2).
4. Solve each circuit-CSP with Lemma 1.3 (arity ≤ n^{9/10}, constant density: 2^{O(n/√log n)}·poly|Φ|); b = t^{9/10}-ish balances 2^{O(t/b)}.
Responsible operation (answer to WP2's list): NOT fewer transitions and NOT algebraic compression in the encoding. It is
(i) moving the log t overhead of oblivious simulation INSIDE the constraints (the counting engine is charged per VARIABLE, not per
constraint size), (ii) guessing the coarse movement pattern so the history becomes a density-2 constraint graph whose variables are only
the inter-epoch interfaces. The algebraic compression happens in the counting engine (T34 §1), not in the reduction.

## 3. WP3 — common structure of crossing sequences and block simulations
Framework. For a computation of M on x with time T, space S, and a partition 𝓑 of its space–time history into cells (spatial
intervals × time intervals), let G_𝓑 be the graph on cells with an edge when information passes between them, and
I_𝓑(M,x) = Σ_edges (bits passed). Instances: (a) Hennie: 𝓑 = {left, right of boundary i} over all time, I = |CS(i)|·log|Q|;
(b) SS: 𝓑 = blocks × epochs, I = interface bits; (c) Cook–Levin tableau: 𝓑 = single cells; (d) Anthropic's sum-of-products graph:
edge bits of a CNF (T34 §1).
Lemma U1 [DED]. For a b-block-respecting d-tape machine running T steps, the SS interface count is I_SS = Θ(d·T + T/b·log|Q|): each epoch
emits exactly its d touched blocks (d·b symbols) plus state/head data, and there are T/b epochs.
Lemma B1 [DED] (the interface measure is time in disguise). For every language L, let I*_L(n) = min over block-respecting machines
deciding L of max_{|x|=n} I_SS. Then I*_L(n) = Θ(T*_L(n)) up to the constant-factor overhead of HPV, where T* is the optimal multitape
time. Proof: U1 for both directions plus HPV's constant overhead. ∎ Hence a lower bound on I* IS a time lower bound — no independent
property is gained.
What the measures DO govern [DED from SS + Lemma 1.3 + Anthropic bound in m]: for NONDETERMINISTIC histories, deterministic simulation
time ≤ 2^{O(T/b)} · 2^{O(I/√log I)} · poly(T). Interface bits are an UPPER-bound resource (cost of deterministic simulation of guessing),
exactly as clause edge bits are in Anthropic's algorithm.
Transformations: I_𝓑 changes by constant factors under HPV normalisation and by O(log T) factors under PF obliviousness; it is NOT
invariant under change of model (PAL: 1-tape crossing I = Θ(n²), 2-tape I = Θ(n)) and not under change of representation (T31 C2,
T34 §1: signed rewritings shrink edge bits of a fixed graph).

## 4. WP4 — transfer attempts (PNP-TRANSFER-001)
| attempt | restricted bound | transfer | verdict |
|---|---|---|---|
| T-a communication across input cuts | Hennie Ω(n²) | ≤ O(K·n) for every L (T31 C1) | capped; input-information cap [DED, T31] |
| T-b interface bits I* | none independent | I* = Θ(T*) (B1) | restatement [DED] |
| T-c tensor/edge-bit width of a fixed network | 2^{Ω(n)} contraction on expanders | refuted by XOR-SAT (T31 C2) and by the ETH engines for all k-CNF (T34) | refuted as a general lower bound [PUB+DED] |
| T-d time → space simulation + space hierarchy | see K1 | survives model changes up to exponents | VALID for languages hard for space; does not reach SAT (D1) |
Correction K1 to T31 Theorem C1 [DED]: C1 caps only communication/cut-sum arguments. Crossing sequences ALSO feed time→space
simulations (Paterson; O137), and combined with the space hierarchy these beat n²: by O137, for a language L ∈ DSPACE(n) \ DSPACE(o(n))
(space hierarchy, n space-constructible) and every ε > 0, no offline one-writable-tape machine decides L in time O(n^{5/2−ε}):
otherwise O137 (time cap supplied in binary, O(log n) space) puts L in DSPACE(n^{1−2ε/5} polylog n) ⊆ DSPACE(o(n)). Same argument
with W25: no multitape machine decides L in time O(n^{2−ε}) (Williams states this corollary for W25; not re-read).
(Novelty of the O137 corollary: [CAND] — check whether the OpenAI article states it.) These are unconditional lower bounds above the
communication cap, obtained by DIAGONALISATION (space hierarchy) after an information-transfer simulation — the only combination in
this audit that yields lower bounds for general (multitape) machines.
Lemma D1 [DED] (exact transfer theorem; decomposition of SAT ∉ P). If (a) for every ε > 0, DTIME(t) ⊆ DSPACE(t^ε) for all
time-constructible t ≥ n, and (b) SAT ∉ DSPACE(n^δ) for some δ > 0, then SAT ∉ P.
Proof. If SAT ∈ DTIME(n^k), apply (a) with ε = δ/(2k): SAT ∈ DSPACE(n^{δ/2}), contradicting (b). ∎
Status of the premises: (a) is the time→space compression extended from √t (W25) to every power t^ε — it alone implies P ≠ PSPACE (T27
§2 argument) and P ⊆ ∩_ε DSPACE(n^ε); open, no evidence for it. (b) is a space lower bound for SAT; it implies NP ⊄ L; open. D1 is the
precise form in which "information that must be re-transported under bounded space" (T31 §3) could give P ≠ NP: it splits the target
into a simulation theorem (a) and a space lower bound (b). Both are at least as hard as known open separations; D1 is a reduction of the
proof obligation to two named statements, not progress on either.

## 5. WP5 — status of earlier PNP-001 hypotheses
| hypothesis | status |
|---|---|
| cut rank / bond dimension / contraction width lower-bounds SAT (T1, T10, T25, T31 C2) | valid only for fixed networks; refuted for general algorithms (XOR-SAT; ETH engines) |
| T24/T28 constant-width encodings with n√log n variables (Lemma G) | Lemma G vacuous once arity N^{9/10} is allowed (T34 J4); question restated, OPEN |
| ETH-based conditional bounds | rationale obsolete (ETH false); Weak ETH / SH (arXiv:2611.02650) still open |
| GCT occurrence obstructions | excluded (Bürgisser–Ikenmeyer–Panova); multiplicity obstructions open (T11) |
| communication cap n² (T31 C1) | correct for communication arguments; narrowed by K1 |
| information transport ⇒ superpolynomial (T31 D) | correct for input information; D1 isolates the bounded-space route |
| emergent/collective invariants (T32) | restatement (W4) or restricted |
| fluid computation (T33) | computability only |

## 6. WP6 — both directions
P = NP direction: best proved: k-SAT in 2^{O(n/√log n)} (sparse), NTIME[t] ⊆ DTIME[2^{O(t/√log t)}]. Polynomial time would require
breaking Weak ETH / SH; no transformation in this audit gives it. Not established.
P ≠ NP direction: no unconditional superpolynomial bound. Strongest unconditional bounds touched here: offline 1-tape n^{5/2−o(1)} and
multitape n^{2−o(1)} for SOME linear-space language (K1; not SAT, not NP); E^NP ⊄ SIZE(c n √log n) i.o. (T23). The strongest unresolved
transfer theorem is D1's premise pair (a)+(b), together with T28/J4 (circuit-CSP encodings, NEXP ⊄ P/poly side).
What the audit establishes: information-transfer measures are either input-capped (T-a), equal to time (B1), representation-dependent
(T-c), or useful only through space-bounded re-transfer plus diagonalisation (K1, D1). No invariant survives arbitrary polynomially
equivalent representations while being independently bounded for SAT.
