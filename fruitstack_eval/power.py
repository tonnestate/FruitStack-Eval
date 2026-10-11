"""Sample-size planning for the H4 non-inferiority test (protocol section 5.4).

Normal approximations, deliberately simple and documented:

paired (one task, two arms):   n = (z_{1-alpha} + z_{power})^2 * psi / (margin + delta)^2
unpaired (independent tasks):  n = (z_{1-alpha} + z_{power})^2 * (p1(1-p1) + p2(1-p2)) / (margin + delta)^2

psi    share of tasks on which the two arms disagree (discordant pairs)
delta  assumed true advantage of the new arm over the reference (0 = equal)
alpha  one-sided significance level
"""
from __future__ import annotations

import math
from statistics import NormalDist

_NORMAL = NormalDist()


def _check_common(margin: float, alpha: float, power: float, true_difference: float) -> float:
    if not 0.0 < margin < 1.0:
        raise ValueError("margin must be in (0, 1)")
    if not 0.0 < alpha < 0.5:
        raise ValueError("alpha must be in (0, 0.5)")
    if not 0.5 < power < 1.0:
        raise ValueError("power must be in (0.5, 1)")
    effective = margin + true_difference
    if effective <= 0.0:
        raise ValueError("margin + true_difference must be positive")
    z = _NORMAL.inv_cdf(1.0 - alpha) + _NORMAL.inv_cdf(power)
    return z * z / (effective * effective)


def paired_noninferiority_n(margin: float, discordance: float, *, alpha: float = 0.025,
                            power: float = 0.80, true_difference: float = 0.0) -> int:
    """Number of paired tasks for a non-inferiority test on success rates."""
    if not 0.0 < discordance <= 1.0:
        raise ValueError("discordance must be in (0, 1]")
    return math.ceil(_check_common(margin, alpha, power, true_difference) * discordance)


def unpaired_noninferiority_n(margin: float, reference_rate: float, *, alpha: float = 0.025,
                              power: float = 0.80, true_difference: float = 0.0) -> int:
    """Number of tasks per arm when the arms run on different tasks."""
    if not 0.0 < reference_rate < 1.0:
        raise ValueError("reference_rate must be in (0, 1)")
    new_rate = reference_rate + true_difference
    if not 0.0 < new_rate < 1.0:
        raise ValueError("reference_rate + true_difference must be in (0, 1)")
    variance = reference_rate * (1.0 - reference_rate) + new_rate * (1.0 - new_rate)
    return math.ceil(_check_common(margin, alpha, power, true_difference) * variance)
