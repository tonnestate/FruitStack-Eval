# PNP-001 — Contract K7: Subexponential Tensor Counting, T1 Satz 2, and the Algorithm-to-Lower-Bound Template
Owner contract 2026-11-21 (authoritative text: the owner's message; this file is its working copy for agents). Programme P1 (algorithms =>
lower bounds). Status OPEN. Labels: [Q] checked at the source, [G] from memory, [E] own inference, [C] claimed by an external preprint, not
independently verified. Nothing is PROVED by PNP-001 unless a section says so. Desk lane: T-B.

## 0. Why
1 [C] OpenAI preprint "The Exponential Time Hypothesis is False" (26 Oct 2026) and Anthropic preprint "A 2^{o(n)} Time Algorithm for 3-SAT"
  (github.com/anthropics/formal-math, eth/paper.pdf, 27 Oct 2026 UTC): deterministic #k-CNF in 2^{O_k(n log log n / sqrt(log n))}, Lean 4
  formalisations; headline bound proved by tensor contraction (Dias-Lima, arXiv:2611.00517).
2 [C] Wu-Wang, "Circuit Lower Bounds for Extended Gate Bases from Subexponential Counting" (arXiv:2611.02560): a language in E^NP needs
  > c m sqrt(log m)/log log m gates i.o. over unbounded fan-in AND/OR, binary XOR, NOT, any depth; cites an OpenAI bound Omega(m sqrt(log m))
  for binary-gate circuits in E^NP.
3 [Q per owner] Dias-Lima: with extracted constants the certified running time is above 2^n unless log2(n+m) > 10^9 at bounded density.
Relation: PNP-001 tensor-train counting, proof-book entries 51-55 (T1 Satz 2: #F mod p in O(m n R*^3)).

## 1. Stage A — source verification (mandatory first)
1 Obtain both papers + Lean files: exact Lean theorem statement, `#print axioms`, any `sorry`, computational model formalised, certified
  bound; every gap to the headline bound. FIRST confirm that the documents and repository exist at the stated locations; if not found, the
  claim is UNVERIFIED, never assumed.
2 Build the Lean projects in the existing PhysalisMe/Lean infrastructure; a build failure is recorded with the exact error, not worked around.
3 Wu-Wang and the OpenAI lower bound: exact circuit model (basis, fan-in, what is counted), class E^NP, "infinitely often", external
  theorems each step uses.
4 Independent reviews, errata, refutations, confirmations since 26 Oct 2026, with dates.
Output: table, one row per claim: VERIFIED-FORMAL / VERIFIED-PARTIAL (weaker statement) / UNVERIFIED / DISPUTED (with source). Stage B only
for VERIFIED-FORMAL or VERIFIED-PARTIAL claims (partial: use only the formally verified bound).

## 2. Stage B — method comparison with T1 Satz 2
Common notation (network, contraction order, intermediate ranks, ring: Q, Z/2^k, GF(p), extension rings; where the gain arises); the exact
ingredient behind the sqrt(log n) saving; effect of T1 ingredients (GF(p) + CRT over several primes, minimisation lemma entry 53, Hadamard
lemma entry 54, separator lemmas entries 59, 60) on the exponent, or "no effect" with reason.

## 3. Stage C — the exponent
Can n/(log n)^{1/2+o(1)} become n/(log n)^a, a > 1/2? (1) From the Wu-Wang template the explicit map counting time 2^{n/g(n)} => lower bound
s(m) for E^NP; check against m sqrt(log m) at g = sqrt(log n). (2) The g needed for s(m) = m (log m)^k for every fixed k. (3) Any improvement:
complete proof, tested on bounded-density k-CNF, random 3-CNF at threshold, positive 1-in-3, GF(3)-blind cores, F_16. (4) Conditional limits
first (counting versions of other hypotheses, Orthogonal Vectors - which Anthropic states it does not refute); list them.

## 4. Stage D — distance to the MCSP target
Target: for some fixed c, MCSP[m^c] needs > N (log N)^k gates for every fixed k (NP not in P/poly via MMW19 / Theorem R). (1) Gaps: E^NP vs an
NP language; sqrt(log) vs every power of log. (2) Does any published magnification theorem accept N sqrt(log N) for a sparse NP language
(Chen-Jin-Williams FOCS 2019, Oliveira-Pich-Santhanam, MMW)? exact required bound each. (3) Can the Williams template use MCSP-type languages
directly (Wu-Wang's W is diagonal)? what fails.

## 5. Controls
Locality (small fan-in oracle gates; where non-relativising); natural proofs (why the method is not natural); no step PROVED from an external
preprint alone.

## 6. Output K7-REPORT.md
A verification table; B common notation + source of the saving; C map g -> s(m), needed g, improvement with proof or exact obstruction;
D gaps to MCSP + magnification check; E chain labelled PUBLISHED THEOREM / CLAIMED / INDEPENDENTLY PROVED / OPEN.

## 7. Restrictions
Mathematical research only; no changes to architecture, PlumMe, agent management or running sessions; no CI; proof-book conventions; nothing
PROVED without independent review; P != NP not claimed.
