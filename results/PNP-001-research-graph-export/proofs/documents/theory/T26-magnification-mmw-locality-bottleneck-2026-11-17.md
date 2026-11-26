# T26 — One hardness-magnification theorem worked to its blocking step (PI, 2026-11-17)

STATUS: primary sources read by the PI (McKay–Murray–Williams STOC 2019, people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf;
Chen–Hirahara–Oliveira–Pich–Rajgopal–Santhanam ECCC TR19-168). Independent check via FruitStack/PlumMe (one neuron answered; Claude subagents blocked by the usage limit until
2026-11-19). Not in the ledger.

## Step 0 — choosing the theorem (owner criterion: the conclusion must imply P ≠ NP)
- CHOPRS frontiers A–E conclude EXP/NQP/NP ⊄ NC¹ — none implies P ≠ NP. Rejected.
- CHOPRS Thm 1(a) (OS18, approximate MCSP ∉ Circuit[N^{1+ε}] ⇒ NP ⊄ P/poly): conclusion fits, but (a) is proved EQUIVALENT to the
  non-existence of P/poly-natural properties against Circuit[n^d] (CHOPRS Thm 1) — the hypothesis is a cryptography-strength statement.
- Chosen: MMW19 Theorem 1.4, third bullet — worst-case, search version, conclusion NP ⊄ P/poly.

## Step 1 — the theorem with all quantifiers
Objects: n, N = 2^n; s(n) >= n time-constructible; A ∈ PH an oracle.
search-MCSP^A[s]: input T ∈ {0,1}^N (truth table of an n-bit function); output: the description of an A-oracle circuit of size
<= s(n) computing T, or the all-zero string if none exists.
Theorem (MMW19, Thm 1.4 third bullet). If search-MCSP^A[s(n)] does not have circuits of size N·poly(s(n)) and depth poly(s(n)), then
NP ⊄ P/poly.
Quantifier form of the hypothesis H(s,A): for every polynomial p, NOT [for all large n there is a circuit of size N·p(s(n)) and depth
p(s(n)) computing search-MCSP^A[s] on N-bit inputs]. Contrapositive proved: NP ⊆ P/poly ⇒ ∃ p such circuits exist.
Conclusion NP ⊄ P/poly ⇒ P ≠ NP. Circuit model: Boolean circuits of bounded fan-in (the theorem's "circuits"); size counts gates.

## Step 2 — the proof and the exact place of locality
Lemma 3.1 (MMW19): for ℓ(n) >= s(n)^2, search-MCSP^A[s] has uniform AC circuits of size Õ(N·s/ℓ) and depth O(n/log ℓ) whose ONLY
non-trivial gates are Circuit-Min-Merge^A[s] oracle gates of fan-in ℓ.
- Circuit-Min-Merge^A[s]: given circuit descriptions D_1..D_d with disjoint intervals I_1..I_d, output the lexicographically first
  A-circuit of size <= s agreeing with D_k on I_k for all k (or "none"). It lies in Σ3P^A (guess C', ∀-check consistency,
  ∀ smaller C'' inconsistent).
- Construction: a d-ary tree, d = ℓ/(100 s log s). Leaves: N constant-size circuits D^0_j with D^0_j ≡ T(j). Each gate G^i_j merges d
  child descriptions on consecutive intervals into one description of size s; the root covers all of T.
- Correctness: by induction D^i_j agrees with T on its interval [j d^i, (j+1) d^i). If T has a size-s circuit C*, every merge
  succeeds because C* is consistent with all children on their intervals. If a merge fails, T has no size-s circuit.
- Magnification step: under NP ⊆ P/poly, Σ3P^A ⊆ P/poly (A ∈ PH), so each merge gate is replaced by a poly(ℓ) = poly(s) circuit;
  total size N·poly(s), depth O(n/log ℓ)·poly(s) = poly(s) (n <= s). Contradiction with H(s,A).
Locality (CHOPRS Prop. 63 [MMW19]; their Def. 62): unconditionally,
    search-MCSP^A[s] ∈ [ q = O(N/poly(s)) oracle gates, fan-in ℓ = poly(s), adaptivity O(n/log s) ] – Circuit[N/poly(s)].
Bottleneck: any technique that proves "f ∉ Circuit[N·p(s), depth p(s)]" and remains valid when the circuit may additionally use
O(N/poly(s)) arbitrary oracle gates of fan-in poly(s) cannot prove H(s,A) — it would also exclude the oracle circuits of Lemma 3.1,
which exist. The blocking point is the replacement of Circuit-Min-Merge^A gates: the problem's global constraint (ONE size-s circuit
for all N bits) is NOT lost under localisation — the merge tree preserves it exactly, because size-s witnesses restrict to intervals
and merge from witnesses alone ("mergeable short witnesses", description length O(s log s) ≪ N). All global difficulty is pushed into
the ℓ-bit merge function.
So a proof of H(s,A) must use the circuit complexity of the local merge function itself, i.e. must distinguish oracle gates computable
by poly(ℓ)-size circuits from arbitrary ones. Gate elimination, random restrictions, communication/rank arguments (e.g. the owner's
equality example) treat small sub-circuits as black boxes and do not make this distinction.

## Step 3 — what the blocking point really demands (revised after review)
Independent check (FruitStack/PlumMe, gpt-oss-120b, receipt_8d5c17766ada48d9a0638095805c3dac; a second neuron, nemotron-3.5-super,
failed without output). Its verdicts, checked by the PI:
- (a), (c), (f) confirmed.
- (b) objected "NP ⊆ P/poly gives only PH ⊆ Σ2 (Karp–Lipton)": REJECTED. NP ⊆ P/poly ⇒ NP/poly ⊆ P/poly (Cook–Levin with the advice
  hard-wired) ⇒ by induction Σ_k ⊆ P/poly for all k ⇒ PH ⊆ P/poly; Karp–Lipton concerns the uniform collapse. Step (b) stands.
- (d) objection incoherent (a Σ3 search inside the gate is exactly "difficulty in the ℓ-bit merge function"); not adopted.
- (e) flagged; on re-examination the original converse candidate is MIS-SPECIFIED: a merge instance of ℓ = poly(s) bits describes,
  through circuits, a partial table of length up to N = 2^n with n <= s — it is a SUCCINCT problem. "N·poly(s) circuits for the
  explicit N-bit problem ⇒ poly(ℓ) circuits for the succinct merge" demands an explicit-to-succinct transfer that in general fails.
  The candidate is withdrawn.

Corrected analysis of the blocking point:
  Merge^A[s] ∈ P/poly (as a function of its ℓ-bit input)  ⇒  search-MCSP^A[s] has circuits of size N·poly(s), depth poly(s)  (Lemma 3.1).
Contrapositive: H(s,A) ⇒ Circuit-Min-Merge^A[s] ∉ P/poly ⇒ Σ3P^A ⊄ P/poly ⇒ PH ⊄ P/poly ⇒ NP ⊄ P/poly.
So EVERY proof of the "weak-looking" hypothesis H (a lower bound of size N·poly(s) on N-bit inputs) necessarily establishes a
SUPERPOLYNOMIAL circuit lower bound for one explicit function: the ℓ-bit Circuit-Min-Merge^A[s] (a Σ3P^A search problem). The locality
barrier is the visible form of this fact: techniques blind to the internal complexity of ℓ-bit sub-functions cannot do that.
Precise remaining statement at the blocking point (for this theorem):
  (M*) For some time-constructible s(n) >= n and A ∈ PH, Circuit-Min-Merge^A[s] on ℓ = Θ(s²)-bit inputs has no circuits of size
       poly(ℓ).
(M*) is implied by H and itself implies NP ⊄ P/poly. Magnification does not lower the difficulty below (M*); it relocates the
problem to a superpolynomial lower bound for an explicit Σ3^A-type function on short inputs — of the same nature as the original goal.
DECISION (gate): this magnification route offers NO lever beyond a direct superpolynomial lower bound for an explicit PH-function.
Documented obstruction, not a candidate proof step.
Owner check rules applied: (i) equality counterexample — rank/communication measures excluded; (ii) access to input structure — H
concerns explicit circuits on the full truth table, no query restriction; (iii) black-box lower bounds (owner's OR_{2^n} proof) are
not used anywhere.
