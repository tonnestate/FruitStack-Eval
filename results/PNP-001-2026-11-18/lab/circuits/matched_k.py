"""Exact minimum circuit size of SAT sub-families at matched input length k (PNP-001, D-010 follow-up).
For each problem (1in3, xor3 with both right sides, 2sat) on n=5 variables: draw k-subsets of the constraint universe, keep only
non-degenerate ones (non-constant, all k bits essential, at least one MUS of size > 2), compute the exact B2 circuit size (CaDiCaL,
UNSAT/SAT certificates, Knuth-calibrated) and the MUS structure. Append-only JSONL, resumable. Usage: matched_k.py K PER_KIND"""
import itertools, json, random, sys, time
from pathlib import Path
from physalisme import circuits as C

N = 5
OUT = Path(__file__).with_name("matched_k.jsonl")


def universe(kind):
    if kind == "1in3":
        return list(itertools.combinations(range(N), 3))
    if kind == "xor3":
        return [(t, b) for t in itertools.combinations(range(N), 3) for b in (0, 1)]
    return [((a, sa), (b, sb)) for a, b in itertools.combinations(range(N), 2) for sa in (0, 1) for sb in (0, 1)]


def holds(kind, c, a):
    bit = lambda v: a >> v & 1  # noqa: E731
    if kind == "1in3":
        return sum(map(bit, c)) == 1
    if kind == "xor3":
        return sum(map(bit, c[0])) % 2 == c[1]
    (u, su), (v, sv) = c
    return bit(u) == su or bit(v) == sv


def table(kind, cons):
    k = len(cons)
    return [int(any(all(holds(kind, cons[i], a) for i in range(k) if x >> i & 1) for a in range(1 << N))) for x in range(1 << k)]


def mus_of(tt, k):
    return [x for x in range(1 << k) if not tt[x] and all(tt[x & ~(1 << i)] for i in range(k) if x >> i & 1)]


def main(k, per_kind, seconds=900):
    done = {(r["kind"], tuple(map(tuple, r["idx"]))) for r in map(json.loads, OUT.open())} if OUT.exists() else set()
    for kind in ("1in3", "xor3", "2sat"):
        U, rng, got, tries = universe(kind), random.Random(f"{kind}-{k}"), 0, 0
        while got < per_kind and tries < 200000:
            tries += 1
            idx = sorted(rng.sample(range(len(U)), k))
            cons = [U[i] for i in idx]
            tt = table(kind, cons)
            mus = mus_of(tt, k)
            if len(set(tt)) == 1 or C.essential_inputs(tt, k) < k or max(map(lambda m: bin(m).count("1"), mus), default=0) <= 2:
                continue
            got += 1
            if (kind, tuple((i,) for i in idx)) in done:
                continue
            r = C.min_size(tt, k, max_s=25, seconds=seconds)
            sizes = [bin(m).count("1") for m in mus]
            over = [bin(a & b).count("1") for a, b in itertools.combinations(mus, 2)]
            rec = {"kind": kind, "k": k, "idx": [[i] for i in idx], "cons": cons, "sat_ones": sum(tt), "mus": len(mus),
                   "mus_sizes": sizes, "dnf_literals": sum(sizes), "mean_overlap": round(sum(over) / len(over), 3) if over else 0,
                   "size": r["size"], "lower_bound": r["lower_bound"], "status": r["status"], "seconds": r.get("seconds"),
                   "witness": r.get("witness"), "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
            with OUT.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            print(kind, k, "size", r["size"], r["status"], "mus", len(mus), "secs", r.get("seconds"), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
