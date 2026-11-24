# A40A_GATE — oracle-free streaming reduction sheet

> **Operational status:** Prior freeze order withdrawn; the runbook is a conditional template pending explicit reauthorization. Freeze is NOT active or VPS-verified. No scheduler, queue, writer or production checkout was changed by this audit.

Baseline d7635f9ea437c494f1c032e4faadfb673a4e90b1. Source: manuscript v0.25, lines 450–488, and McKay–Murray–Williams STOC 2019 Thms 1.2–1.3, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf.

## Exact target
There exist time-constructible s(m)>=m and A in PH such that for every uniform deterministic one-pass oracle-free RAM algorithm M solving the total exact Search-MCSP^A[s(m)] relation, every c,d in N and every m0 there exists m>=m0 with S_M(m)>s(m)^c or tau_M(m)>s(m)^d. Tau includes final reporting. Oracle gates in the output circuit are not runtime oracle access. This is the negation, for the selected s,A, of existence of a single uniform exact polynomial-space, polynomial-worst-case-update machine. It implies P!=NP via MMW; converse not established.

## Known and missing
MMW provides an oracle-assisted solver; under P=NP its PH queries can be eliminated with polynomial overhead. Manuscript (8), the stronger nonuniform staged-circuit exclusion, implies (40a), not conversely as far as established. Do not identify (8) with arbitrary unrestricted Boolean circuits. Linear-state lower bounds in manuscript lines 492–513 and Q-85e487150a are restricted; no general nonlinear lower bound follows. Both reported Lean declarations remain unsourced and outside the chain.

## Model reduction test
Fixing a representation proves a weaker exclusion. To derive (40a) one would need to show every admissible polynomial-resource general machine can be replaced by a machine in that class with polynomial space, update and reporting overhead and unchanged total search semantics. Generic affine-state normalization is false: AND on N bits has a one-bit nonlinear streaming accumulator; any affine F2 final-state map x -> Mx+b followed by an arbitrary exact decoder must have ker(M)=0, since the unique accepting input cannot collide with another input. Thus affine state requires >=N bits. This is a counterexample to generic normalization, not to a Search-MCSP-specific transformation or to (40a).

## Next mathematical check
State the smallest Search-MCSP-specific normalization lemma with exact resource bounds, then identify the structural invariant that rules out the AND-type gap and test the oracle-assisted MMW construction. A proof treating oracle updates as arbitrary black boxes cannot simply exclude that already existing solver; identify the exact model-sensitive step. Relative/oracle barriers are not by themselves a proof that every nonrelativizing approach fails. No established Natural Proofs/algebrization classification for this exact proposed lemma; audit separately once a technique exists.

Status: OPEN. No evidence of equivalence to P!=NP, and no established reduction to a solved restricted case. The conditional MMW transfer is valuable independently of route choice.
