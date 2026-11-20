# Bridging Formula Lower Bounds and Circuit Complexity via Reuse-Bounded Simulations of MCSP

Project: PNP-001 / FruitStack. Snapshot: branch cc/pnp001-results-20261118, after commit f5670df (2026-11-20).
Status: conditional reduction (Theorem R) checked and independently reviewed internally; hypothesis R-MCSP OPEN.
**P != NP is NOT proved.** Internal review is not external peer review. Full working record: acc0-level3/ACC0-L3-REPORT.md, section 20.

## Abstract
We ask whether controlling intermediate-gate reuse in general Boolean circuits can turn known De Morgan formula lower bounds for
MCSP into circuit lower bounds strong enough for hardness magnification. An elementary simulation converts circuits to formulas with
loss 2^r in the number r of reused gates. Proposition R1 (parity + Khrapchenko) shows that any simulation with polynomial reuse loss
valid for all functions needs exponent c >= 1; Observation R1' shows the same for formulas with XOR leaves (inner product witness).
We isolate an MCSP-specific hypothesis R-MCSP (formula size subquadratic in circuit size for fixed-threshold MCSP) and observe that,
combined with Chen-Jin-Williams (STOC 2020) and McKay-Murray-Williams (STOC 2019), it would give NP not in P/poly. This reduction is a
straightforward combination of published results, not a new theorem; the content of this note is the precise localisation of the
missing step.

## 1 Conventions
N = 2^m truth-table length; F_{N,beta} = MCSP[N^beta] (fixed threshold, fixed finite basis). Circuits are De Morgan circuits over
AND/OR (fan-in 2) with **complemented wires** (NOT absorbed into wires). S(C) = number of binary gates; r(C) = number of binary gates
whose output feeds more than one wire, so 0 <= r <= S. L(f) = minimum leaf count of a De Morgan formula; CC(f) = minimum circuit size.

## 2 Generic reuse lemma (elementary, not novel)
Every circuit with S gates and r reused gates has an equivalent formula with at most 2^r (S + r + 1) = O(S 2^r) leaves.
Proof: replace reused gates by fresh variables y_i; every other gate has fan-out 1 and lies in exactly one of r + 1 trees
T_1..T_r, T_out, with at most S + r + 1 leaves in total. f(x) = OR_a [AND_i (T_i(x,a) <-> a_i) AND T_out(x,a)]; T_i <-> a_i is T_i or
its negation (negations pushed to leaves). By acyclicity, induction in topological order shows exactly one a is consistent (the true
gate values).

## 3 Proposition R1 and Observation R1'
**R1.** If L(f) <= C S(D) (r(D)+1)^c for every f and every circuit D for f, then c >= 1.
Proof: XOR_n has circuits with S, r = O(n) (chain z_k = (z_{k-1} v x_k) ^ not(z_{k-1} ^ x_k)); Khrapchenko gives L(XOR_n) >= n^2; so
n^2 <= C' n^{1+c} for all n, hence c >= 1.
Stronger obstacle: a generic simulation with ANY constant c would put P/poly inside poly-size formulas, i.e. NC^1/poly (Spira
balancing) - believed false. R1 excludes only lemmas valid for all functions, not restricted circuit classes or other techniques.
**R1' (elementary given Tal 2017; Tal source check pending).** XOR leaves are XORs of input variables, so FORMULA[s] o XOR lies in
bipartite formulas of size O(s). IP_n has linear circuits with ~n reused gates but bipartite formula size n^{2-o(1)} (Tal 2017). So any
generic conversion circuit -> FORMULA o XOR with loss S (r+1)^c needs c >= 1 - o(1): XOR leaves absorb parity, but not reuse of
computed intermediate values.

## 4 Published formula lower bounds (quantification matters)
- CKLM (ECCC TR19-022 rev. 1): L(MCSP) >= N^3 / 2^{O(log^{2/3} N)} with the threshold as INPUT, chosen near 2^n/n via the PRG local
  complexity (sec. 1.2.1). Not a bound for fixed MCSP[N^beta].
- KKLMO (CCC 2020, arXiv 2002.08533, Thm 34): MCSP not in FORMULA[N^{2-o(1)}] o XOR, threshold as input, proof needs l = n^{Omega(1)}.
  Fixed-threshold version not stated.
- **CJW 2020 (ECCC TR20-065), Thm 1.6:** for every beta in (0,1), eta > 0: MCSP[N^beta] has no probabilistic formulas of size
  N^{2+beta-eta} (leaf count). This is the premise used below.

## 5 Hypothesis R-MCSP (OPEN)
There are C > 0, 0 <= c < 1, beta_0 > 0 such that for every fixed beta in (0, beta_0) and all large N, every circuit D for F_{N,beta}
has an equivalent formula with at most C S(D) (r(D)+1)^c leaves. It suffices for minimum-size circuits.
This implies (it is not equivalent to) L(F_{N,beta}) <= C CC(F_{N,beta})^{1+c} with 1 + c < 2, and Theorem R uses only this weaker form;
the reuse parameter is a proof device, not part of what the implication needs.

## 6 Theorem R (conditional reduction)
If R-MCSP holds, then NP not in P/poly, hence P != NP.
Proof. Let D be minimum-size for F_{N,beta}, S = CC(F_{N,beta}). R-MCSP and r <= S: L <= C S^{1+c}. CJW20 Thm 1.6: L > N^{2+beta-eta}.
So S > (N^{2-eta}/C)^{1/(1+c)}; with eta < 1 - c this is >= N^{1+eps}, eps = (1-c-eta)/(1+c) > 0 independent of beta.
MMW19 Thm 1.4 (third item, contrapositive): if NP in P/poly, search-MCSP[s] has circuits of size N poly(s) (fixed polynomial,
depth poly(s)); for s = N^beta this is N^{1+k beta} for a fixed k; a decision circuit follows by verifying the search output
(cost N poly(s)). Choosing beta < eps/k contradicts S >= N^{1+eps}; depth is irrelevant since our bound is on size. Hence NP not in
P/poly, and P != NP since P is in P/poly.
The "for all small beta, one eps" restatement is from CJW TR19-118; it must not be confused with the CJW 2019 sparse-language theorem,
whose conclusion is NP not in SIZE[n^k] for each k, not NP not in P/poly.

## 7 Research obligation
A proof of R-MCSP must: hold for every minimum-size circuit for F_{N,beta}, with unrestricted fan-out and topology; give one c < 1
uniformly in small beta; survive parity-like AND inner-product-like intermediate computation (controls: EQ, IP, MUX); and be
**non-localizing** - MCSP[N^beta] has near-linear circuits with small fan-in oracle gates, so an argument that remains valid with such
gates proves a false statement. Natural-proofs and algebrization hypotheses must be examined, not assumed.
Next mathematical step: an exact decomposition definition (algebraic sub-computations + quantitatively bounded residual sharing) for
arbitrary nested DAGs, tested against IP and the locality criterion before any proof attempt. No enumeration campaign.

## 8 Status
| Component | Status |
|---|---|
| Generic reuse lemma O(S 2^r) | proved, internally reviewed |
| Proposition R1 (c >= 1) | proved, internally reviewed |
| Observation R1' (IP, XOR leaves) | elementary given Tal 2017; Tal source check pending |
| CKLM, KKLMO | published; threshold as input |
| CJW20 Thm 1.6 | published; fixed threshold |
| Theorem R | reduction from published results, internally reviewed |
| R-MCSP | OPEN |
| P != NP | OPEN |

## 9 References (verified against local copies unless noted)
1. Cheraghchi, Kabanets, Lu, Myrisiotis. Circuit Lower Bounds for MCSP from Local Pseudorandom Generators. ICALP 2019; ECCC TR19-022 rev. 1 (2020). https://eccc.weizmann.ac.il/report/2019/022/
2. Chen, Jin, Williams. Sharp Threshold Results for Computational Complexity. STOC 2020, Thm 1.6. https://eccc.weizmann.ac.il/report/2020/065/
3. McKay, Murray, Williams. Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes. STOC 2019, Thm 1.4.
4. Chen, Jin, Williams. Hardness Magnification for All Sparse NP Languages. FOCS 2019. https://eccc.weizmann.ac.il/report/2019/118/
5. Kabanets, Koroth, Lu, Myrisiotis, Oliveira. Algorithms and Lower Bounds for de Morgan Formulas of Low-Communication Leaf Gates. CCC 2020. https://arxiv.org/abs/2002.08533
6. Khrapchenko. Complexity of the realization of a linear function in the class of pi-circuits. Math. Notes 1971. (not checked locally)
7. Tal. Formula lower bounds via the quantum method. STOC 2017. (not checked locally)
