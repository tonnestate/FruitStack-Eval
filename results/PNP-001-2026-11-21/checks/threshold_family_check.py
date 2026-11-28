"""Owner result 2026-11-16 (threshold family): F(n, m) = "at most m of the n variables are 0". Checks #F(n,m) = sum_{r<=m} C(n,r), the reduced
cut matrix rank min(a, b, m, n-m) + 1 and the full cut rank over Q and GF(2) for every cut size, by exact enumeration in the PhysalisMe
sandbox (tool call, no model call)."""
import asyncio, json, httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

CODE = r'''
from math import comb
from fractions import Fraction
from itertools import product
def rank_q(M):
    A = [[Fraction(x) for x in r] for r in M]; r = 0
    for c in range(len(A[0]) if A else 0):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r
def rank_f2(M):
    rows = [int("".join(str(x) for x in r), 2) for r in M]; r = 0
    for bit in reversed(range(len(M[0]))):
        p = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r
def main(I):
    bad, checked_reduced, checked_full = [], 0, 0
    for n in range(2, 13):
        for m in range(0, n + 1):
            for a in range(1, n):
                b = n - a
                H = [[int(i + j <= m) for j in range(b + 1)] for i in range(a + 1)]
                want = min(a, b, m, n - m) + 1
                if rank_q(H) != want or rank_f2(H) != want: bad.append(("reduced", n, m, a))
                checked_reduced += 1
                if n <= 10:
                    left, right = list(product((0, 1), repeat=a)), list(product((0, 1), repeat=b))
                    M = [[int((x.count(0) + y.count(0)) <= m) for y in right] for x in left]
                    if rank_q(M) != want or rank_f2(M) != want: bad.append(("full", n, m, a))
                    checked_full += 1
            count = sum(1 for x in product((0, 1), repeat=n) if x.count(0) <= m) if n <= 12 else None
            if count != sum(comb(n, r) for r in range(m + 1)): bad.append(("count", n, m))
    return {"reduced_checked": checked_reduced, "full_checked": checked_full, "mismatches": bad[:10],
            "R(20,10) by formula": min(10, 10, 10) + 1, "#F(20,10) by formula": sum(comb(20, r) for r in range(11))}
'''

async def main():
    c = Client(streamable_http_client('http://physalisme/mcp', http_client=httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport(uds='/run/physalisme/mcp.sock'), timeout=900)))
    async with c:
        r = await c.call_tool("physalis_code_run", {"code": CODE, "input": {}, "timeout_s": 800, "memory_mb": 4096})
        print(json.dumps(r.structured_content, default=str))
asyncio.run(main())
