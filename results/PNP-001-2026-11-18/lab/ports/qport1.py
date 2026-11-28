"""Q-PORT-1: is a clutter a matroid port? Seymour 1976 (as transcribed by owner from secondary sources, LIT-SEYMOUR): a clutter is a
matroid port iff it has no minor isomorphic to P4, Q4, b(Q4) or J_s (s >= 3). Clutter minors: deletion L\\e drops sets containing e;
contraction L/e removes e from every set and keeps the inclusion-minimal ones. Exhaustive over all (delete, contract) assignments."""
import itertools

FORBIDDEN = {"P4": [{1, 2}, {2, 3}, {3, 4}], "Q4": [{1, 2}, {1, 3}, {2, 3, 4}], "bQ4": [{1, 2}, {1, 3}, {1, 4}, {2, 3}]}       # blocker of Q4 (owner correction 2026-11-18)
# Q-PORT-2: ports of the excluded minors for GF(3)-representability (Seymour 1977), derived by Claude from the matroid definitions
TERNARY = {"port(U25)": [set(c) for c in __import__("itertools").combinations(range(1, 5), 2)],
           "port(U35)": [set(c) for c in __import__("itertools").combinations(range(1, 5), 3)],
           "port(F7)": [{2, 4}, {3, 7}, {5, 6}, {2, 3, 6}, {2, 5, 7}, {3, 4, 5}, {4, 6, 7}],
           "port(F7*)": [{2, 3, 6}, {2, 5, 7}, {3, 4, 5}, {4, 6, 7}]}


def is_J(cl):
    """J_s, s >= 3: one s-set plus the s pairs {i, x} for i in it, x outside."""
    big = [a for a in cl if len(a) >= 3]
    if len(big) != 1 or len(cl) != len(big[0]) + 1:
        return None
    pairs = [a for a in cl if len(a) == 2]
    xs = {next(iter(a - big[0]), None) for a in pairs}
    ok = len(xs) == 1 and None not in xs and all(len(a & big[0]) == 1 for a in pairs) and len({min(a & big[0]) for a in pairs}) == len(big[0])
    return f"J{len(big[0])}" if ok else None


def minimal(sets):
    sets = set(map(frozenset, sets))
    return {a for a in sets if not any(b < a for b in sets)}


def canon(cl):
    """Isomorphism invariant-safe canonical form: try all relabelings of the support (support <= 12 here, sizes small)."""
    sup = sorted(set().union(*cl)) if cl else []
    best = None
    for p in itertools.permutations(range(len(sup))):
        m = dict(zip(sup, p))
        key = tuple(sorted(tuple(sorted(m[x] for x in a)) for a in cl))
        best = key if best is None or key < best else best
    return best


def table_of(named):
    out = {}
    for name, cl in named.items():
        sup = set().union(*cl)
        out.setdefault((len(sup), len(cl)), {})[canon(minimal(cl))] = name
    return out


FORB = {}
for name, cl in FORBIDDEN.items():
    sup = set().union(*cl)
    FORB.setdefault((len(sup), len(cl)), {})[canon(minimal(cl))] = name


def forbidden_minors(clutter, elements, table=None, with_J=True):
    table = FORB if table is None else table
    hits = {}
    for assign in itertools.product((0, 1, 2), repeat=len(elements)):      # 0 keep, 1 delete, 2 contract
        dele = {e for e, a in zip(elements, assign) if a == 1}
        con = {e for e, a in zip(elements, assign) if a == 2}
        cl = minimal(a - con for a in clutter if not (a & dele))
        if not cl or frozenset() in cl:
            continue
        sup = set().union(*cl)
        if sup != set(elements) - dele - con:                                # unused elements: covered by the deletion branch
            continue
        key = (len(sup), len(cl))
        name = is_J(cl) if with_J else None
        if name is None and key in table:
            name = table[key].get(canon(cl))
        if name:
            hits.setdefault(name, (sorted(dele), sorted(con), sorted(map(sorted, cl))))
    return hits
