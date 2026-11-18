"""Exact minterms (MUS, f=1) and maxterms (maximal satisfiable sets, f=0) of the monotone UNSAT function of a constraint universe.
Bitmask DP over all 2^k selections."""
import itertools


def universe(kind, n):
    if kind == "1in3":
        return list(itertools.combinations(range(n), 3))
    if kind == "xor3":
        return [(t, b) for t in itertools.combinations(range(n), 3) for b in (0, 1)]
    raise ValueError(kind)


def sol_mask(kind, c, n):
    if kind == "1in3":
        return sum(1 << a for a in range(1 << n) if sum(a >> v & 1 for v in c) == 1)
    t, b = c
    return sum(1 << a for a in range(1 << n) if sum(a >> v & 1 for v in t) % 2 == b)


def terms(kind, n):
    U = universe(kind, n)
    k = len(U)
    S = [sol_mask(kind, c, n) for c in U]
    sat = bytearray(1 << k)
    m = [0] * (1 << k)
    m[0] = (1 << (1 << n)) - 1
    sat[0] = 1
    for x in range(1, 1 << k):
        low = x & -x
        m[x] = m[x ^ low] & S[low.bit_length() - 1]
        sat[x] = m[x] != 0
    del m
    bits = [1 << i for i in range(k)]
    minterms = [x for x in range(1 << k) if not sat[x] and all(sat[x ^ b] for b in bits if x & b)]
    maxterms = [x for x in range(1 << k) if sat[x] and all(not sat[x | b] for b in bits if not x & b)]
    return U, k, minterms, maxterms
