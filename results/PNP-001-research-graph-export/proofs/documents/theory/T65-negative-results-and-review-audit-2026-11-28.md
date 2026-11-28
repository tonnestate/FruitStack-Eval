# T65 — Audit of the 32 refutations, early hypotheses (entries 26,27,35,36,37,52), the 42 syntheses and the 90 unconfirmed closures (2026-11-28)

Method: Proofbook rows read in the live ledger (`staging/proofbook.jsonl`, 18336 rows), graph read-only. Classes: [T] a mathematical theorem/claim refuted by counterexample; [C] a particular construction fails; [I] an implementation/engine bug; [E] evidence insufficient; [S] an intermediate requirement too strong / overclaim withdrawn; [R] refuted as route but the refutation is itself conditional.
No refutation among the 32 is a general impossibility theorem of a research direction, except the one marked [R].

## A. The 32 REFUTATION rows
| seq | what | class | remark |
|---|---|---|---|
| 46 | "#F even ⇔ all models monochromatic" (weak-model hypothesis) | [T] | valid counterexamples (x1; x1∧x2); no direction closed |
| 91 | SOSA paired reduction gives a sign-free survivor core ⇒ cancellation decides SAT | [C]+[E] | [REPAIRED 2026-11-28, see T4: the claim 'survivors all +1 after the first cancellation' is false (11/6) but a second involution ι(x,S)=(x,S△{min V(x)}) leaves exactly SAT(φ) with sign +1 (5/0); sign-free core exists and equals SAT(φ); per-assignment identity N+−N−=[x⊨φ] verified] one concrete pairing fails (mixed signs 6/11); review noted "circular, all-+1 unproven". NOT an impossibility of signed cancellation (cf. T4 finding) |
| 103 | T6 "intrinsic padding obstruction" | [S] | withdrawn by the row itself; precision-vs-normalization cost still to be combined (T6 finding of the owner) |
| 139,146,151 | permanent Hessian rank claims (c ≤ ⌊n/2⌋, c=2 structure, rank-2 family) | [T] on intermediate claims | Satz T9-B unaffected (row 146) |
| 172–212 (rows 7–16) | T11/T13 GCT multiplicity framings, padding-floor equivalence, null-cone extension | [S]/[T] | corrections of overclaims; the padding-floor *equivalence* is refuted by a certified counterexample, the ≤ direction retained |
| 200,201 | border Waring Θ vs Ω; task split ℓ=5 scope | [S] | |
| 443–456 | invented SAT procedures (nemotron/qwen) unsound | [C] | exact #SAT counterexamples; each kills ONE procedure |
| 947 | 2-SAT as control for the port criterion | [T]+[E] | refutes "non-port ⇒ superpolynomial"; the "linear circuit size" part unsupported (T45 corrected) |
| 1143,1153,6193 | GF(3)-blind / mod-9 / cov=rank3+1 conjectures | [T] | explicit exact counterexamples |
| 11359 | Lemma D1 (one-step drop) | [T], repairable | Lean counterexample: AND-NOT gate is the OUTPUT gate, so the negation cannot be absorbed into a successor; the lemma holds if g is not the output gate (or the bound is s for output negation). Edge case, not a dead direction |
| 16761,16839 | CJW20 pseudorandom restriction "for every De Morgan circuit …" | [T] on the universal claim | parity-tree and window-gate counterexamples refute the universal bound; they do not exclude a version restricted to circuits for Gap-MCSP (the row says so) |
| 18279 | AND gadget computes XNOR | [I]/[C] | erratum; corrected gadget verified |
| 18292 | T59 §5/§7/§10 statements | [T] | my own corrections |
| 18299 | coupling "gate-ideal saturation/canonical selector forces small space" | **[R]** | argument: the properties hold for every circuit; if they forced log-space witness construction then Circuit Value ∈ L, i.e. P = L. P = L is OPEN, so this does not refute the coupling; it shows the coupling would prove a statement at least as strong as P = L. The wording "refuted as a route" must read "cannot be proved without proving P = L-type statements". |
So: 0 of 32 prove a general impossibility; 1 (18299) was worded as a closure and is conditional on an open conjecture.

## B. Early hypotheses (entries 26, 27, 35, 36, 37) and entry 52
No correction existed in the ledger for 26, 27, 35, 37 before this audit.
- **26** (contraction-state entropy ∝ log #F): "contraction state entropy" is undefined (depends on order and tensor-network layout); "supported on instances n=4..14" is evidence, not a statement. Class: ILL-DEFINED, no mathematical content to refute or keep.
- **27** (symmetry of clause tensors preserved under variable elimination): ill-defined as stated; for a clause (a∨b∨c) eliminating c against (c∨d) gives 1 + [a∨b]·d, symmetric only under a↔b: the full symmetry group is not preserved. Class: false as the natural reading, otherwise ILL-DEFINED.
- **35** (cut rank = minimum size of a clause set whose union implies a variable assignment): for F = Π_{i≤m}(x_i∨y_i) the cut rank across {x}|{y} is 2^m (Kronecker power of [[0,1],[1,1]], rank 2 each) but no clause set implies any assignment. REFUTED (counterexample m=2, rank 4).
- **36** refuted by 46 (valid).
- **37** (∃ satisfiable F, n ≤ 12, tensor rank > 2 "across any cut"): with "every cut" it is false for every F (a cut isolating one variable has a 2-row matrix, rank ≤ 2); with "some cut" it is trivially true ((x1∨y1)(x2∨y2), rank 4). Class: ambiguous quantifier; neither reading is a research result.
- **52** (grouping inclusion–exclusion terms needs exactly r_i classes): correct only for exact representation of the whole function f_F (T1 Satz 1). It is not a lower bound for computing the scalar #F: F = Π(x_i∨y_i) has cut rank 2^m, #F = 3^m. T1 §1 header and scope corrected in this audit (T1 now states the scope). Whether other documents used "rank = compression of the count" as a barrier: T10 (rank barriers) concerns arithmetic-circuit lower bound methods, not this statement; not affected.

## C. The 42 syntheses (statements read, not all proofs)
- Counting/bound statements re-derived by hand and found correct: SYN-04cf (M ≤ (s+1)(n+s)(3(n+s)²)^s), SYN-0fa5 (2^k(h+1)−1), SYN-8525 (q_t ≤ min(K,2^t,2^{2^{N−t}})), SYN-d5e6, SYN-f8bd, SYN-ff6e (one-hot 4q+1), G0176/S0513 (2^{d+1}−4+q(2^d−1)), G0142/S0244 (state count ≥ #residuals at one level for time-invariant Q too).
- Proof/wording defects confirmed: SYN-cc1f (span equivalence), SYN-e12a (zero vector), SYN-d74a (equal-length parenthetical), SYN-0cd3 (256 = single functions), SYN-3aa6 (s=0), SYN-cbdc (shrink), SYN-421a refutation is VALID (counter 0..N needs n+1 bits, claimed M+⌈log2 N⌉).
- SYN-440d refutation valid (F={x=0,y=0,y=1}). SYN-fc44 counterexample valid.
- **Streaming/counter family (0c07, 1f05, c0c4 refuted; 08c3, f2aa survived; 421a refuted; 0cd3, d175, 731252, a479, 184f, b925, f5cd survived):** consistent standard: (1) behaviour on streams LONGER than N = 2^n is out of scope when the statement is about the length-2^n truth table; the three wrap-around refutations are valid only against a claim that the machine rejects longer streams (f2aa states the wraparound explicitly and survived); (2) state-bit counts and gate counts are strict (421a is a genuine off-by-one). Under this standard 0c07, 1f05, c0c4 are NOT refuted for the stated scope (status REFUTED_BY_DEPENDENT_REVIEW should be re-evaluated by the graph owner; I do not write to `synthesis_acceptance`).
## D. The 90 unconfirmed closures
Most are lists of synthesis ids (no text); the closing statements that exist are among the 42 above and were checked at statement level. I did NOT re-prove them; the status stays UNCONFIRMED. No new elementary error was found in the readable closing statements; the confirmed defects of §C are proof-presentation errors, not wrong statements (except the T38/T28-type items fixed earlier).

## E. Not done
Line-by-line proof files (1,502), the remaining ~11,000 APPROACH/NUMERICAL rows, external theorems used load-bearing (Kannan, IKW, Pich–Santhanam, PPST: recalled, not re-read; Williams STOC 2025 §3.1/App. A read).
