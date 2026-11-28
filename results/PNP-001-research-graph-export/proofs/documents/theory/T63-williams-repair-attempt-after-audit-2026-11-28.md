# T63 — Williams blocks after the seven-point audit: corrected inputs, exact shortcut question, repair attempts (2026-11-28)

Status: derivation; P != NP not claimed. Companion of T62 (cost accounting). Labels as in T62.

## 1. Audit corrections applied to the active documents (2026-11-28)
| # | doc | correction | effect on Williams analysis |
|---|---|---|---|
| 1 | T54 Cor 2.3 | t=0 fibre sees only the cube-free (reduced) part; "C|_{t=0}≠0 ⇒ tight", converse false (Q=x³z²: formal F=−x³, C≡t²x→0) | none of W1–W6 uses it; graded QE must not be used to read formal degrees |
| 2 | T50 B1 | T48 8.1/9.1 do not give g−f∈I for two circuits | no equivalence certificate is available for "block circuit = block function" |
| 3 | T53 §2(ii) | F = N_even − N_odd (mod 3) | F3 QE is not a counting oracle without weight normalization |
| 4 | T48 §6 | only the rank and a compact description of the cover are polynomial; explicit cover 2^{d−1} | no explicit cover output in any step |
| 5 | T49 L3 | W must be Boolean-valued on Boolean inputs (counterexample over F3, q(u)=(u²−u)/2) | W2/W6 unaffected; Williams' char-2 field is covered since P(v) is only used at Boolean v |
| 6 | T54 §5 | homogenization gives t^k f^h, not f^h; saturation needed | no certificate size is claimed anywhere below |
| 7 | T58 §D | formal LB ⇒ F only | W-statements are algorithmic upper/lower bounds on the ADD recursion, not circuit lower bounds |
Also reused (not new): multilinearization/Hamiltonian-cycle hardness is T50 §4; T53 §2a only restates it.
Owner-reported, not verified here and not used: T4 (pairing), T35 (quantifier order), T6 (precision), T44 (equivalence claim). T40 and T42 counterexamples were checked (one line each) and the documents corrected.

## 2. Question: do the corrected tools give an exact shortcut for Williams' block functions?
Place of cost (from T62): time(ADD) = (#calls)(per-call work), #calls >= (2m)^B, per-call work >= b, m > deg M_f (W1), B = T'/b.
Each tool against the two factors:
- *Functional QE (T52 corrected, T54 corrected):* gives an extension F_corr² of degree <= 2e*, but evaluation is a sum over 3^d points with d ~ #gates (exponential), and its formal polynomial is VNP-hard (T53 §1). It lowers neither factor.
- *Certificate transfer/composition (T48 §9, corrected §9.6):* acts on certificates, none exists for block circuits (items 2, 6). Not applicable.
- *Boolean ideal cancellation / shared-interface elimination:* act on a given system; identity (5) is itself a group-averaging projection, optimal in its class (W6). No replacement identity with fewer masks.
- *Spectral masking:* (5) IS exact spectral masking by the character sum over mu_m; W6 shows m >= deg+1 is necessary for any scalar-character version.
Result: **no exact shortcut for the work.** The count (2m)^B cannot be reduced by these tools; the cost of one extension value is not the bottleneck (T62 W2).

## 3. Repair attempts (each with its cost)
**R1. Mask only the inputs once (single group over the composed polynomial).** The root value is a function of the n input bits; M_root has degree <= n << (5b)^B (the degree of the composed arithmetization). One mask group of size m > n would suffice to extract v_root in n+1 evaluations of M_root at non-Boolean points. But evaluating M_root at non-Boolean points is the T53/T50 problem (⊕P-hard in general, W3). Williams' recursion is exactly the device that restores Booleanity level by level. Cost: moves the whole difficulty into one non-Boolean evaluation. REJECTED, reason exact.
**R2. Copy the child value into several masked contexts at once (vector registers).** ADD returns y^ + v where y^ holds catalytic garbage g. To add v to a second register y2 one needs v itself, which is available only as g + v. Subtracting g requires g, which the catalytic algorithm is not allowed to know. So the m-fold re-injection cannot be shared by copying. A variant that stores v (non-catalytic) is the ordinary recursion: time d^B, space B d b. This is the known frontier; the catalytic gain is purely in space. REJECTED for work.
**R3. Piecewise extension P = sum_k P_k with different small degrees.** Each piece needs its own mask set of size m_k > D_k, and each mask set re-runs the child recursion. Per-level multiplicity becomes sum_k m_k >= D+1 (W6). No gain. REJECTED.
**R4. Choose a different block size or machine to make deg small.** deg M_f >= b/c for universal M' (e.g. AND of b tape bits), so m = Theta(b) already (Williams' |F| >= d b² is only for register shortening). The minimum of b·6^{T'/b} is at b = T': the single-block (direct) simulation. REJECTED: time >= 6T'.
**R5. Interpolation with F3-QE extension (corrected) instead of multilinear.** Needs characteristic-3 version of the cancellation (adding v twice no longer cancels; use subtraction) and degree 2e* < m; evaluation 3^d; as in §2. No gain.

## 4. Net statement
(i) The corrected inputs (items 1–7) do not enlarge the set of usable identities; (ii) the exact reason Williams-type compression saves space but not work is the equality of two exponential quantities: the recursion multiplicity (2m)^B equals, in order, the degree (5b)^B of the composed arithmetization, i.e. the price of extracting a value from catalytic garbage by averaging; (iii) every repair that tries to avoid it either relocates the cost (R1), needs knowledge the catalytic setting withholds (R2), or fails the counting bound (R3, R4).
The corrected criterion of T62 §7 (instance size T^{o(1)}, reduction time o(T/log T), everything charged) stays unmet.
First unproved implication: unchanged (T61 §7). No contradiction from P = NP.
