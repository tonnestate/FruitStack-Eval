"""EXACT (not sampled) circuit-size distribution of all k-subsets of a constraint universe, unconditional AND filtered (PNP-001 D-010c).
Circuit size is invariant under the symmetry group of the problem (variable permutations; for xor3 also variable complementation,
which maps (t,b) -> (t, b ^ |t & neg| mod 2)), because a symmetry only permutes the input bits. So each orbit is solved once and
weighted by its size. Filters (owner's selection audit): non-constant, all k bits essential, some MUS of size > 2.
Resumable JSONL keyed by canonical subset. Usage: orbits_k.py KIND K"""
import itertools, json, sys, time
from pathlib import Path
from physalisme import circuits as C

N = 5
sys.path.insert(0, str(Path(__file__).parent))
from matched_k import universe, table, mus_of  # noqa: E402


def group(kind):
    out = []
    for p in itertools.permutations(range(N)):
        for neg in (range(1 << N) if kind == "xor3" else [0]):
            out.append((p, neg))
    return out


def act(kind, c, p, neg):
    if kind == "1in3":
        return tuple(sorted(p[v] for v in c))
    t, b = c
    return (tuple(sorted(p[v] for v in t)), b ^ (sum(neg >> v & 1 for v in t) % 2))


def main(kind, k, seconds=1800):
    U = universe(kind)
    pos = {c: i for i, c in enumerate(U)}
    G = [[pos[act(kind, c, p, neg)] for c in U] for p, neg in group(kind)]
    out = Path(__file__).with_name(f"orbits_{kind}_k{k}.jsonl")
    done = {tuple(json.loads(l)["canon"]) for l in out.open()} if out.exists() else set()
    seen, orbits = set(), []
    for S in itertools.combinations(range(len(U)), k):
        if S in seen:
            continue
        orb = {tuple(sorted(g[i] for i in S)) for g in G}
        seen |= orb
        orbits.append((min(orb), len(orb)))
    total = sum(w for _, w in orbits)
    print(kind, k, "subsets", total, "orbits", len(orbits), flush=True)
    for canon, w in orbits:
        if canon in done:
            continue
        cons = [U[i] for i in canon]
        tt = table(kind, cons)
        mus = mus_of(tt, k)
        sizes = [bin(m).count("1") for m in mus]
        const = len(set(tt)) == 1
        ess = C.essential_inputs(tt, k)
        passes = not const and ess == k and max(sizes, default=0) > 2
        r = C.min_size(tt, k, max_s=25, seconds=seconds)
        rec = {"kind": kind, "k": k, "canon": list(canon), "weight": w, "of_total": total, "constant": const, "essential": ess,
               "passes_filters": passes, "mus": len(mus), "mus_sizes": sorted(sizes), "size": r["size"],
               "lower_bound": r["lower_bound"], "status": r["status"], "seconds": r.get("seconds"), "witness": r.get("witness"),
               "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with out.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(kind, k, "w", w, "pass", passes, "size", r["size"], r["status"], "mus", sizes, "secs", r.get("seconds"), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
