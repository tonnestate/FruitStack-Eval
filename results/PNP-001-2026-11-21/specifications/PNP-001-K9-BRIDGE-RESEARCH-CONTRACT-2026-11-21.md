# PNP-001 — Owner round "Bridge research: which results could actually lead to P != NP" (2026-11-21, late)
Working copy for agents (authoritative text: the owner's message). Status tags [Q]/[G]/[E]/[B]/[C] as in the K8 contract. Never claim
P != NP. Principle: combine results only where the combination STRENGTHENS the needed theorem; lower bounds in different classes do not
add up to a separation. Main target stays P2 (MCSP lower bound or uniform constructive refuter - both have published transfers).

## Bridge table (owner)
Direct: R-MCSP -> CJW20 -> MMW19 (open R-MCSP hypothesis); uniform constructive MCSP refuter -> CJSW (K8). Direct but demanding:
special Extended-Frege lower bounds -> Pich-Santhanam (TR23-199, conditional transfer, specific witnessing formulas + axioms).
Algorithmic: low-degree PIT -> win-win lower bounds (TR26-313); THR o THR CAPP -> Williams. Structural: spectral gate elimination ->
MCSP (new manuscript, unverified). Proof complexity: GF(3) kernel / Theorem 12 -> general IPS (no transfer).

## 1 Counting theorem (T-B lane, depends on K7 Stage A Q-cd3478a51e)
[C] OpenAI manuscript "The Exponential Time Hypothesis is False" (2026-10-25): exact counting of common zeros of sparse F_2 systems
(n vars, <= cn equations, constant degree, polylog monomials) in 2^{O(n (loglog n)^2 / sqrt(log n))}, poly space. [B, owner] positive
1-in-3 clause <=> 1+x+y+z+xyz = 0 over F_2 (degree 3, 5 monomials) - direct corollary for #positive-1in3 with m <= cn, IF the theorem
holds. Question: do Williams-type circuit-analysis instances translate into such systems without too many new variables / degree /
monomials? Name the first failing parameter. 2^{o(n)} is still superpolynomial.
## 2 Weak Rank Principle (K2-K6 lane)
[G->Q by owner] "The Weak Rank Principle: Lower Bounds and Applications": PCR over F_2 lower bounds, proof-complexity generators,
PCR cannot efficiently prove certain circuit-lower-bound statements. Compare with Theorem 12: which properties of the WRP construction
do our GF(3)/roABP families lack if the goal is hardness of circuit-lower-bound statements (Pich-Santhanam formulas), not of an
arbitrary CNF? The PCR -> Extended Frege step is open.
## 3 Low-degree PIT (T-B lane, amends Q-e988ea9656)
TR26-313 Thm 3: improving O_d(s t^{d-1}) to O(s t^{d-1-eps}) for GENERAL circuits computing degree-d polynomials => NE near-maximal
Boolean lower bounds OR superlinear arithmetic lower bounds for explicit VNP. An improvement only for our F_8/F_16 clause families does
NOT meet the hypothesis. Document the first failing step if our algebra does not extend.
## 4 roABP closure (K2-K6 lane, binding check rule)
[Q, owner] ITCS 2026 "On Closure Properties of roABPs": factoring, powering, symmetric substitution can blow up roABP width in every
order. RULE: every transformation of a roABP-IPS certificate needs a quantitative width-preservation statement; semantic equivalence is
not enough. Width_pi(f) = max_i rank M_{pi,i}(f) exactly - certify width changes via coefficient-matrix ranks.
## 5 Spectral gate elimination vs R1160 (K1 lane)
[C, unverified] J. Wittcop, "2N Circuit Lower Bounds for the Minimum Circuit Size Problem" (academia.edu, 2026-11): CC(MCSP[n-1]) >=
(2-o(1))N, claimed Lean 4 formalisation, not peer reviewed. Method: most restrictions remove >= 2 gates, exceptions bounded via a
Hoffman spectral bound, CC >= 2(N-m) - B. First: locate and check the Lean source and the proof; then: do the exceptions in our
synthesized circuits (R1160: 3 of 222 NPN classes at n=4 with max drop 1, incl. parity 0x6996, cm-e62b031d90e740c1) form a spectrally
controllable structure? Limit: threshold s = n-1 and linear bounds; magnification needs s = N^beta and N^{1+eps}.
## 6 Hitting sets (K2-K6 lane, verification aid)
[Q, owner] Shpilka 2026-11-09: poly-size hitting sets for multilinear any-order roABPs. Which identities in Lemma T, Lemma N and the
roABP-IPS certificates satisfy its hypotheses (deterministic PIT for PhysalisMe)? Identity testing is not a lower bound.
Restrictions: mathematical research only; no architecture/PlumMe/orchestration/CI changes; nothing PROVED without independent review.
