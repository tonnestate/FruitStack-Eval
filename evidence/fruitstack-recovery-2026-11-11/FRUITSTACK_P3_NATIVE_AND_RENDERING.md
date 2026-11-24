# FruitStack P3 — native candidates, fast-path transport, AnanasMe rendering (2026-11-11)

## Runtime inspected
PlumMe service `integration/stability-001` 88fa17d (pid 1508008, restarted for 88fa17d); CherryMe/PeachMe/AppleMe on `deploy/20261109T143734Z`
(d5daa60 / 4d1a2ba / aca5f8b; PeachMe 1 and AppleMe 38 uncommitted changes, not ours); Aurora `/opt/fruitstack/integration` (no git);
AnanasMe is not deployed on the VPS (no service/checkout); Aurora face: `/var/www/tonnestate.de/public/mission-control/app.js`.

## CPU candidates (measured)
| Candidate | Measurement | Verdict |
|---|---|---|
| PlumMe market screen per acquisition | ~80-110 ms CPU live; 49 % static capability/role checks over ~2,900 offers, 11 % requalify | no C: the C11 pool already ranks; a C screen would duplicate admission/billing/cost logic. Static verdicts are not cacheable by object (offers mutated in place by discovery, billing guard). Remains the top PlumMe CPU item. |
| CherryMe integrated CogC (`compile_packet`) | 20-50 µs per packet (60 evidence items) | negligible vs multi-second provider calls |
| CherryMe mission worker imports | ~0.4 s per mission process | not CPU work; acceptable per mission |
| Aurora fast worker | 1.23 s interpreter + mcp/httpx2 imports per owner message (subprocess) vs ~0.36 s PlumMe+MCP | **largest non-provider latency → fixed in Python (stdlib)** |
| PeachMe ToolGateway / AppleMe / MangoMe | not on the measured owner path (Aurora → PlumMe/CherryMe) | not changed |

## Implemented
1. Aurora `aurora_chat.py`: the fast worker is ONE stateless MCP `tools/call` over HTTP+SSE with the standard library (the service runs stateless Streamable HTTP; no session id). `mission_facade._chat` calls it in-process. Bridge interpreter (Python 3.10, www-data): facade overhead per message 6-11 ms (was ~1.4 s); end-to-end 4.9 s / 9.2 s = Luna provider time. Diff `aurora_p3.diff`; test `aurora_test_fast_path_escalation.py` 7/7 (adds a real HTTP/SSE server).
2. PlumMe 88fa17d (live): model-scoped 401/403 back off from 6 h (after a4e4310, 21 distinct llm7 models were probed once each in 16 min with a 10 min first step). Observed state: 24-26 llm7 models in model cooldown, ModelScope whole-key at escalation 2.
3. AnanasMe 89b7adc (branch `cc/ananasme-render-perf`, local, NOT deployed): keyed message rendering + state-aware polling. Chromium, real HTTP+SQLite harness, 120 messages: idle requests/30 s 20 → 3, idle script 14.1 → 4.7 ms, render on an active reply 115 → 6.9 ms, rebuilt nodes 244 → 3, open "Laufdetails" preserved (no → yes), reply visible 4.93 → 4.70 s. Hidden-tab effect not measurable in this harness. Suite 137 passed, 1 pre-existing failure (also on HEAD). `scripts/browser_render_check.py` reproduces it.
4. Aurora face: already pauses its own clock via IntersectionObserver; TalkingHead's internal loop while scrolled out of view not measured → unchanged.

## Not changed, by evidence
No native C/C11 change: no measured CPU-bound operation where C would improve the complete operation without duplicating PlumMe authority logic.

## Security finding
`systemctl cat tonn-crm.service` exposes `TE_CREATOR_PORTAL_HMAC_SECRET` in plain text in the unit file (value not repeated here) → move to a credential file and rotate.
