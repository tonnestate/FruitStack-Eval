# Scoped critical-path quarantine report

> **Operational status:** Prior freeze order withdrawn; freeze runbook is a non-executable-in-policy template pending explicit reauthorization. Freeze is NOT active or VPS-verified. No scheduler, queue, writer or production checkout was changed by this audit. Research is not stopped by this repository.

Baseline d7635f9ea437c494f1c032e4faadfb673a4e90b1. The scope contains 42 nodes and 37 edges, of which 27 are mathematical dependencies. Starting at each target, traverse consumer-to-premise DEPENDS_ON only. The existing 21 blocked nodes partition as follows:

## E (4)
- E:E1
- E:E2
- E:IPS-LB
- E:PNP

## A (2)
- A:Prop13-stream
- A:eq40a

## AalternativeOnly (4)
- A:Prop13-staged
- A:Prop15
- A:eq8
- A:width-bridge

## outside (12)
- A:Q-08a1c5b68f:S0028
- A:Q-08a1c5b68f:S0029
- A:Q-156fa9c912:S0037
- A:invalid-residual-upper
- A:invalid-review40
- A:no_tail_bounds
- A:restriction_independent_gates_survive
- B:Q-10bbdfaf2a:S0148
- B:Q-10bbdfaf2a:S0217
- B:Q-10bbdfaf2a:S0508
- B:Q-10bbdfaf2a:S0509
- E:seq14287

Blocking of a conditional conclusion because a premise is open does not refute its conditional proof. Neither unsourced Lean theorem is an admitted premise. Every node has unresolved.global_blocking=true because the full graph and statement audits are incomplete; scoped_blocked is the narrower computed flag. This is a conservative evidence policy, not an operational freeze. No mathematical dependent of a red seed was demonstrated in this slice; unknown dependents remain unresolved.
