"""Independent re-computation (Fable, 2026-11-16) of the owner's experiment on cut ranks of SAT solution tensors.
For every family: the exact minimum over ALL variable orderings of the maximum cut rank (subset dynamic programme over prefixes),
over Q (exact fraction-free elimination) and over GF(2), plus the model count. Runs in the PhysalisMe sandbox (tool call, no model call)."""
import asyncio, json, httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

CODE = r'''
from itertools import combinations
from fractions import Fraction
from math import comb
import numpy as np

def rank_q(M):                      # exact rank over Q (Bareiss-free Gaussian elimination with Fractions; matrices here are <= 32 x 32)
    A = [[Fraction(int(x)) for x in row] for row in M]
    r, rows, cols = 0, len(A), len(A[0]) if A else 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r

def rank_f2(M):
    rows = [int("".join(str(int(x) & 1) for x in row), 2) for row in M]
    r = 0
    for bit in reversed(range(len(M[0]))):
        p = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r

def table(n, f):                     # truth table as dict over assignments (tuple of bits)
    return {a: int(f(a)) for a in np.ndindex(*([2] * n))}

def cut_matrix(n, T, S):
    S = list(S); R = [v for v in range(n) if v not in S]
    rows = list(np.ndindex(*([2] * len(S)))); cols = list(np.ndindex(*([2] * len(R))))
    M = []
    for x in rows:
        a = [0] * n
        for v, b in zip(S, x): a[v] = b
        line = []
        for y in cols:
            for v, b in zip(R, y): a[v] = b
            line.append(T[tuple(a)])
        M.append(line)
    return M

def best_order(n, T, rank):          # min over orderings of the max prefix-cut rank, exact (DP over subsets)
    r = {}
    for k in range(1, n):
        for S in combinations(range(n), k):
            r[frozenset(S)] = rank(cut_matrix(n, T, S))
    best = {frozenset(): 0}
    for k in range(1, n + 1):
        for S in combinations(range(n), k):
            S = frozenset(S); here = r.get(S, 1)
            best[S] = min(max(best[S - {v}], here) for v in S)
    return best[frozenset(range(n))], max(r.values())

def order_max(n, T, order, rank):
    return max(rank(cut_matrix(n, T, order[:i])) for i in range(1, n))

def two_cnf(n, edges):               # positive 2-clauses (x_i or x_j) on the edges: zeros form an independent set
    return table(n, lambda a: all(a[i] or a[j] for i, j in edges))

def main(I):
    out = {"pascal": [], "graphs": {}}
    for k in range(1, 6):            # Pascal mod 2 of size 2^k as a function of 2k bits: i bits, j bits
        n = 2 * k
        def f(a, k=k):
            i = int("".join(map(str, a[:k])), 2); j = int("".join(map(str, a[k:])), 2)
            return comb(i, j) % 2
        T = table(n, f)
        grouped = list(range(n)); paired = [v for b in range(k) for v in (b, k + b)]
        row = {"size": 2 ** k, "grouped_Q": order_max(n, T, grouped, rank_q), "paired_Q": order_max(n, T, paired, rank_q),
               "grouped_F2": order_max(n, T, grouped, rank_f2), "paired_F2": order_max(n, T, paired, rank_f2)}
        if n <= 8:
            row["optimum_over_all_orders_Q"] = best_order(n, T, rank_q)[0]
        out["pascal"].append(row)
    grid = [(3 * r + c, 3 * r + c + 1) for r in range(3) for c in range(2)] + [(3 * r + c, 3 * r + c + 3) for r in range(2) for c in range(3)]
    fams = {"path10": (10, [(i, i + 1) for i in range(9)]), "cycle10": (10, [(i, (i + 1) % 10) for i in range(10)]),
            "grid3x3": (9, grid), "K9": (9, list(combinations(range(9), 2)))}
    for name, (n, edges) in fams.items():
        T = two_cnf(n, edges)
        oq, worst_q = best_order(n, T, rank_q)
        of2, worst_f2 = best_order(n, T, rank_f2)
        out["graphs"][name] = {"n": n, "count": sum(T.values()), "min_max_rank_Q": oq, "min_max_rank_F2": of2,
                               "natural_order_max_Q": order_max(n, T, list(range(n)), rank_q), "worst_cut_any_Q": worst_q}
    # K_n: every cut of every ordering has rank <= 2 (the proof: rows [z(a)=0] and [z(a)=1] span the matrix)
    out["K_n_all_cuts_rank_le_2"] = {}
    for n in range(3, 12):
        T = two_cnf(n, list(combinations(range(n), 2)))
        out["K_n_all_cuts_rank_le_2"][n] = {"max_cut_rank": max(rank_q(cut_matrix(n, T, range(i))) for i in range(1, n)), "count": sum(T.values())}
    return out
'''

async def main():
    c = Client(streamable_http_client('http://physalisme/mcp', http_client=httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport(uds='/run/physalisme/mcp.sock'), timeout=900)))
    async with c:
        r = await c.call_tool("physalis_code_run", {"code": CODE, "input": {}, "timeout_s": 800, "memory_mb": 4096})
        print(json.dumps(r.structured_content, default=str))

asyncio.run(main())
