# Proofbook seq 18282 — PROOF_STEP

- key: `2c2b5edbd3a1efdc`
- at: 1795841974.1804116
- mission: PNP-001-T58-correction-2026-11-28
- hash: `fd0ae8b7c160af9bb854104dd02239c32b3267d843cc97eed32ccb21964be76a` (prev `c58e43b17ac76157b321dc59a0f4f54d27ebb35053cf91c3687749af0dd84b8b`)
- graph nodes: PB:fd0ae8b7c160af9bb854104dd02239c32b3267d843cc97eed32ccb21964be76a
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

QUANTITATIVE TRANSFER (corrected). EXTERNAL INPUT, unverified by Lean in this form: OpenAI hamperm Thm 1.1: over every field of characteristic chi, N>=N0(chi): degree-component border size L^[N](HC_N) >= exp(c (log N)^2/(log log N)^2); HC_N has no diagonal variables and counts each tour once, as HC_h above. Lean (lean379.md) proves only the eventual superpolynomial EXACT circuit bound (>N^C for every C); the exp(c(log N)^2/(log log N)^2) degree-component border bound is explicitly UNFORMALIZED. Exact applicability: because P(G_h;y)=HC_h(y) is itself homogeneous of degree h with only the h(h-1) weighted variables, exact circuits, border circuits and degree-h components of P(G_h;.) coincide with those of HC_h; no projection loss. For the fully weighted polynomial W(G_h;X) (3n variables) the substitution X_{v,c} -> constants/variables is a ring homomorphism rho applied to leaves (free in the model), gate count does not increase, and rho is continuous on the finite-dimensional coefficient space (degrees <=2^s), so rho(closure S) is in closure(rho S), then the degree-h component projection is linear: L(W)>=L^[h](HC_h). With n=|V(G_h)|=Theta(h^2 log h): log n = 2 log h + log log h + O(1), so log h = (1/2)log n - O(log log n), (log h)^2 = (1/4)(log n)^2 (1-o(1)) and loglog h <= loglog n: L(P(G_h)) >= exp((c/4 - o(1)) (log n)^2/(log log n)^2) for all n of the form |V(G_h)|, h>=N0(chi), over every field (threshold depends only on the characteristic). Dependencies: Thm 1.1 (paper proof), VNP-completeness of HC over every field (EXTERNAL, Valiant/Buergisser via the paper), this construction (CLAIMED, Claude).

## Full row (verbatim JSON)

```json
{
 "seq": 18282,
 "at": 1795841974.1804116,
 "problem": "p_vs_np",
 "mission": "PNP-001-T58-correction-2026-11-28",
 "key": "2c2b5edbd3a1efdc",
 "kind": "PROOF_STEP",
 "conclusion": "QUANTITATIVE TRANSFER (corrected). EXTERNAL INPUT, unverified by Lean in this form: OpenAI hamperm Thm 1.1: over every field of characteristic chi, N>=N0(chi): degree-component border size L^[N](HC_N) >= exp(c (log N)^2/(log log N)^2); HC_N has no diagonal variables and counts each tour once, as HC_h above. Lean (lean379.md) proves only the eventual superpolynomial EXACT circuit bound (>N^C for every C); the exp(c(log N)^2/(log log N)^2) degree-component border bound is explicitly UNFORMALIZED. Exact applicability: because P(G_h;y)=HC_h(y) is itself homogeneous of degree h with only the h(h-1) weighted variables, exact circuits, border circuits and degree-h components of P(G_h;.) coincide with those of HC_h; no projection loss. For the fully weighted polynomial W(G_h;X) (3n variables) the substitution X_{v,c} -> constants/variables is a ring homomorphism rho applied to leaves (free in the model), gate count does not increase, and rho is continuous on the finite-dimensional coefficient space (degrees <=2^s), so rho(closure S) is in closure(rho S), then the degree-h component projection is linear: L(W)>=L^[h](HC_h). With n=|V(G_h)|=Theta(h^2 log h): log n = 2 log h + log log h + O(1), so log h = (1/2)log n - O(log log n), (log h)^2 = (1/4)(log n)^2 (1-o(1)) and loglog h <= loglog n: L(P(G_h)) >= exp((c/4 - o(1)) (log n)^2/(log log n)^2) for all n of the form |V(G_h)|, h>=N0(chi), over every field (threshold depends only on the characteristic). Dependencies: Thm 1.1 (paper proof), VNP-completeness of HC over every field (EXTERNAL, Valiant/Buergisser via the paper), this construction (CLAIMED, Claude).",
 "premises": [
  17584,
  17879,
  18281
 ],
 "prev": "c58e43b17ac76157b321dc59a0f4f54d27ebb35053cf91c3687749af0dd84b8b",
 "hash": "fd0ae8b7c160af9bb854104dd02239c32b3267d843cc97eed32ccb21964be76a"
}
```
