"""Gal / Razborov rank bound for monotone span programs: for any matrix A on U x V (U subset f^-1(0), V subset f^-1(1)) over F,
mSP_F(f) >= rank_F(A) / max_i rank_F(A restricted to R_i), R_i = {(u,v): i not in u, i in v} (other entries zeroed).
Here f = UNSAT of a clause universe; V = minterms (MUS), U = maxterms (maximal SAT sets) unless stated otherwise."""
import random
import numpy as np


def rank_mod(M, p):
    M = np.array(M, dtype=np.int64) % p
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        nz = np.nonzero(M[:, c])[0]
        nz = nz[nz != r]
        if len(nz):
            M[nz] = (M[nz] - np.outer(M[nz, c], M[r])) % p
        r += 1
        if r == rows:
            break
    return r


def bound(A, U, V, k, p):
    A = np.array(A, dtype=np.int64) % p
    total = rank_mod(A, p)
    worst, arg = 0, None
    for i in range(k):
        b = 1 << i
        mask = np.array([[(not u & b) and bool(v & b) for v in V] for u in U])
        ri = rank_mod(A * mask, p)
        if ri > worst:
            worst, arg = ri, i
    return {"rank": total, "max_rank_Ri": worst, "bound": total / worst if worst else float("inf")}


def critical(U, V, p, rng=None):
    """Support on critical pairs |v \\ u| = 1; entries 1, or random nonzero elements of GF(p) if rng is given."""
    return [[(rng.randrange(1, p) if rng else 1) if bin(v & ~u).count("1") == 1 else 0 for v in V] for u in U]


def disjoint(U, V, p, rng):
    """Random entries on all pairs (dense)."""
    return [[rng.randrange(p) for _ in V] for _ in U]
