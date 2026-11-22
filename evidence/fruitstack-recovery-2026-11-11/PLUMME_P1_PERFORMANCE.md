# PlumMe P1 performance — selection hot path (2026-11-11)

Live service `plumme-mcp.service`, branch `integration/stability-001` (local commits, not pushed), restarted once after the change (pid 1487153).

## Changes (PlumMe-integration)
| Commit | Files | Effect |
|---|---|---|
| 1365c54 | `src/plumme/reliability.py`, `src/plumme/scheduler.py`, `src/plumme/market.py`, tests `test_reliability_incremental.py`, `test_screen_hot_path.py` | receipt-log reliability report parsed incrementally (2.67 s -> 0.03 s per call, identical output); no per-offer `circuit.snapshot()`; static non-generative check once per offer object; provider credential answer once per screen |
| c444be0 | `pool_health.py`, `credentials.py` (+2 tests) | state/credential files not re-read per offer |
| 17804d6 | `adapters/claude_headless.py`, `adapters/codex_headless.py` | lean headless worker calls |
| b9087fd | `scheduler.py`, `service.py`, adapters (+test) | subscription session limit: swap in same call, bench until reset / 30 min |

Dynamic gates (circuit, credential cooldown, quota, pool blocks, rate limits, budgets, admission lifecycle, billing) are still evaluated on every screen; the C11 kernel, receipts and decision records are unchanged. Suite: 977 passed, 11 skipped.

## Measurements
| Metric | Before | After |
|---|---|---|
| `screen()` offline, ~3,000 real offers (cProfile bench `bench_screen.py`) | 120 ms | 27 ms |
| `plum_query_supply` live (screen only, no model call), p50 of 10 | ~250 ms | ~82 ms |
| Service CPU at rest (60 s avg) | 13 % | 8 % |
| Start-up saturation | ~4 min (before c444be0) | 53 s |

5 short requests, free route `nemotron-3.5-lightning` (PREFERRED binding), `plumme_perf5_2026-11-11.json`:
| Run | Total wall | OK | Wall p50 / p95 | Provider p50 / p95 | PlumMe overhead (wall - provider) | Peak concurrent provider calls | Service CPU |
|---|---|---|---|---|---|---|---|
| Sequential | 151.7 s | 3/5 (1 PROVIDER_UNAVAILABLE after 60 s, 1 RATE_LIMITED) | 35.0 / 60.4 s | 34.8 / 60.2 s | 176-263 ms, p50 231 | 1 | 5.9 s |
| Concurrent | 78.8 s | 5/5 | 39.8 / 78.8 s | 39.1 / 78.5 s | 239-1080 ms, p50 660 | 5 | 3.3 s |

Limitation: the provider itself answered in 17-78 s during the check (freellmapi and NVIDIA routes of the same model), so end-to-end p50/p95 is provider latency and is NOT comparable with the earlier Haiku 2.6 s / Luna 6.0 s single calls. Valid conclusions: PlumMe's own share is ~0.2 s sequential; five independent requests ran fully in parallel (peak 5 in flight, total = slowest call, not the sum).

## Remaining bottlenecks
1. Concurrent PlumMe overhead grows to 0.24-1.1 s: every acquisition still screens all offers on the single service event loop (~80 ms each live), so simultaneous acquisitions queue behind each other.
2. Free-route provider latency/availability (here 17-78 s, one 60 s failure, one rate limit) dominates end-to-end time.
3. Background qualification traffic keeps hitting known-refusing routes (NVIDIA 403, llm7/ModelScope 401) — not addressed here.
