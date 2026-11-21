# PNP-001 — Owner review "Können unsere bisherigen Ergebnisse zusammen bereits P != NP beweisen?" (2026-11-21, ~21:30)
Working copy of the owner's analysis for agents (authoritative text: the owner's message). Every statement below is the owner's
CANDIDATE reading, to be independently verified - nothing here is accepted. Owner's own verdict: no complete proof chain exists.

## 1. Parameter gap (owner)
MMW's streaming implication is stated for suitable circuit-size bounds s(n), in particular s(n) >= n. All current test classes have
s < n: SC_{3,1} (n=3, s=1), SC_{3,2}, SC_{4,1}, SC_{4,2}. Tests are valid finite studies of state coding and gate cost, but even a proved
optimal trade-off there does not meet the MMW premise; finite exact bounds at n=3,4 do not imply asymptotic bounds. A transfer to growing
n and suitable s(n) is required and not shown. CHECK: MMW's exact parameter quantifiers from the primary source.

## 2. Minimum state bits follow from a general statement (owner)
Claim: for a proper subclass F of all N-bit truth tables, with time-dependent encodings and unbounded update/decoder cost,
S_min = ceil(log2(|F| + 1)). Reason: the |F| functions need distinct final states (an output circuit computes exactly one function) plus a
reject state; conversely at each step at most |F| prefixes are extendable - code them distinctly, one shared code for all others; with
position-dependent transitions codes are reused per step. Matches 38->6, 70->7, 526->10, 2680->12. Consequence: the minimum state bits carry
no structural information under these assumptions; the Pareto run is the first part that measures computation. For a time-INDEPENDENT
transducer without known position the derivation does not apply directly - the SAT synthesizer must use the same model assumptions.
Director note (fact, 2026-11-21): gate_pareto_sat.py synthesises a separate circuit per step t (time-dependent), one code per live prefix
and exactly ONE shared dead state; redundant/multiple dead codes are not in its search space (scope of its optima).

## 3. Theorem 16 and Boolean algebra (owner)
ACC0-level-3 report: Theorem 16 studies P_Psi(x) = prod_{D in Psi} (1 - Q_D(x)) with exponential coefficient rank over certain variable
partitions for an unsatisfiable CNF family. Since Psi is unsatisfiable, P_Psi = 0 on every Boolean input: the multilinear representation of
the Boolean function is the zero polynomial, while the formal (unreduced mod x_i^2 - x_i) polynomial has high rank AND a polynomial-size
arithmetic circuit (product of small clause polynomials). Not a contradiction to Theorem 16 - it shows why its bound stays inside the
proof/certificate model. A new combination must preserve algebraic information that survives Boolean simplification.

## 4. MCSP formula lower bounds force reuse (owner)
Chen-Jin-Williams Thm 1.6: for fixed 0 < beta < 1 and every eta > 0, L(MCSP[N^beta]) > N^{2+beta-eta} for large N (owner checked the
original). REUSE-MCSP-NOTE: a circuit with G gates and r reused gate results converts to a formula with O(G 2^r) leaves. Hence
r >= (2+beta-eta) log2 N - log2 G - O(1); for G <= N^{1+eps}: r >= (1+beta-eta-eps) log2 N - O(1). Unconditional consequence of known
theorems, no novelty claim; only logarithmically many reused gates. Next question: bound the work of CONSISTENTLY UPDATING reused values
under arbitrary input sequences, not just their number.

## 5. TR26-313 (9 Nov 2026), "A Little Derandomization Goes a Long Way: Unconditional Circuit Lower Bounds using Low-Degree PIT"
Unconditional: either a strong circuit lower bound for a language in NE, or VP^0_Z != VNP^0_Z; the Boolean branch gives for EVERY fixed k a
language in NP not in SIZE(n^k). Quantifier: forall k exists L_k is weaker than exists L forall k (only the latter gives NP not in P/poly);
an algebraic separation over Z does not give P != NP without a further theorem. Owner check: our PC/IPS results do not exclude or
strengthen either branch. Open: an exact transfer from one of our algebraic model classes to the general arithmetic circuits named there.

## 6. TR26-316, "Hard Instances for Strong Semantic Proof Systems"
Annihilating polynomials + pseudo-reduction operators + rank lower bounds (building on an AI-generated proof for resolution over
parities); exponential bounds against semantic Sigma-Pi-Sigma polynomial calculus, superpolynomial for some deeper systems. Candidate:
XOR/Carry and F_16 contradictions + annihilators + pseudo-reduction + rank bounds; test on our explicit GF(3)-blind colouring families
whether it beats Theorems 12 and 14. Success = stronger proof complexity, not P != NP.

## 7. TR26-260 (updated 3 Nov 2026), "An Explicit 4n - O(log n) Size Lower Bound against General Boolean Circuits"
General Boolean circuits; gate elimination over a changing space of INDEPENDENT PARAMETERS with reparametrisations. Question: can a state
recoding of a streaming transducer be treated as a parameter transformation so that a gate-elimination invariant is independent of the
binary state coding? First for the complete partial transition functions of the small SC classes. Limit: the published bound is linear.

## 8. Owner priorities
1 search-MCSP + coding-independent (parametric) gate elimination; 2 MCSP formula bounds + causal reuse -> unavoidable update cost;
3 XOR/Carry + annihilators + pseudo-reduction; 4 PIT win-win + our algebra.

## 9-10. Directive
No new general idea campaign. PhysalisMe: a formal proof-chain check BACKWARDS from P != NP: for each candidate fix the exact published
transfer theorem, then check whether a proved FruitStack result meets its COMPLETE premise (model class, parameter range, quantifiers,
space, time, decoder cost); draw the next implication only on an exact fit. Main new transition: compatible state encodings + partial
transition functions + parameter-based gate elimination -> a nontrivial bound for ALL admissible state representations, first in a
manageable model class, then for an infinite family. Parallel: annihilator method vs XOR/Carry. Results combine only through a PROVED
transfer theorem.
