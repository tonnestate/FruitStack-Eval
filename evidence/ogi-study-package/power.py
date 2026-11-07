"""Exact McNemar power for the OGI study package (planning only; no data, no provider call).

Power of the two-sided exact conditional McNemar test at level alpha for n paired tasks, discordant
probability p_d and pi = P(arm A only | discordant). D ~ Binom(n, p_d); given D the A-only count is
Binom(D, pi); the test rejects when the exact two-sided binomial p-value under pi0 = 0.5
(= 2 * smaller tail, symmetric) is <= alpha.

    python power.py            # prints the table used in PREREG_DRAFT.md section 5
"""
import numpy as np
from scipy.stats import binom

MAX_N = 3000
D = np.arange(MAX_N + 1)


def critical_lo(alpha: float) -> np.ndarray:
    """Largest k with 2 * P(X <= k | d, 0.5) <= alpha for every d (-1: no rejection possible)."""
    lo = np.full(MAX_N + 1, -1)
    for d in range(1, MAX_N + 1):
        ks = np.nonzero(2 * binom.cdf(np.arange(d + 1), d, 0.5) <= alpha)[0]
        lo[d] = ks[-1] if ks.size else -1
    return lo


def power(n: int, p_d: float, pi: float, lo: np.ndarray) -> float:
    d = D[:n + 1]
    l = lo[:n + 1]
    reject = np.where(l >= 0, binom.cdf(l, d, pi) + binom.sf(d - l - 1, d, pi), 0.0)
    return float(np.sum(binom.pmf(d, n, p_d) * reject))


def n_for(p_d: float, pi: float, lo: np.ndarray, target: float = 0.8, step: int = 10):
    return next((n for n in range(step, MAX_N + 1, step) if power(n, p_d, pi, lo) >= target), None)


if __name__ == '__main__':
    print('alpha | p_d | pi | n for power >= 0.80 (step 10; None = above 3000)')
    for alpha in (0.05, 0.025):
        lo = critical_lo(alpha)
        for p_d in (0.10, 0.143, 0.20, 0.30):
            for pi in (0.60, 0.67, 0.75, 0.80):
                print(f'{alpha} | {p_d} | {pi} | {n_for(p_d, pi, lo)}')
