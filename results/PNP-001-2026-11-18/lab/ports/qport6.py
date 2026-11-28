"""Q-PORT-6 / Stage-1 theorem attempt: find a Seymour-1976 forbidden minor in the MUS clutter of positive 1in3 on n=6.
A hit is a CERTIFICATE (=> not a matroid port over any field, for all n >= 6 by the restriction lemma); no hit proves nothing.
Restriction lemma: deleting (clutter deletion) every clause using a variable outside {1..6} from the n-clutter leaves exactly the
6-clutter (extra variables are then free), and minors of minors are minors."""
import itertools, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from qport1 import forbidden_minors, minimal  # noqa: E402

N = 6
U = list(itertools.combinations(range(N), 3))
K = len(U)
SOL = [sum(1 << a for a in range(1 << N) if sum(a >> v & 1 for v in c) == 1) for c in U]
FULL = (1 << (1 << N)) - 1
tt = [0] * (1 << K)
tt[0] = FULL
for x in range(1, 1 << K):
    low = x & -x
    tt[x] = tt[x ^ low] & SOL[low.bit_length() - 1]
MUS = [frozenset(i for i in range(K) if x >> i & 1) for x in range(1 << K)
       if not tt[x] and all(tt[x & ~(1 << i)] for i in range(K) if x >> i & 1)]
lab = lambda i: "".join(str(v + 1) for v in U[i])  # noqa: E731
print("n=6 MUS", len(MUS), "sizes", dict(sorted(__import__("collections").Counter(map(len, MUS)).items())), flush=True)
W = [U.index(c) for c in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (0, 4, 5), (1, 2, 4)]]   # D-008 smallest witness
rng = random.Random(6)
out = Path(__file__).with_name("qport6_hits.jsonl")
for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 300):
    keep = set(W) | set(rng.sample([i for i in range(K) if i not in W], 5))
    cl = [a for a in MUS if a <= keep]                       # deletion of all other clauses (a minor)
    hits = forbidden_minors(cl, sorted(keep))
    if hits:
        for name, (d, c, m) in hits.items():
            rec = {"trial": trial, "keep": [lab(i) for i in sorted(keep)], "forbidden": name, "delete": [lab(i) for i in d],
                   "contract": [lab(i) for i in c], "minor": [[lab(i) for i in a] for a in m]}
            out.open("a").write(json.dumps(rec) + "\n")
            print("HIT", json.dumps(rec), flush=True)
        break
    if trial % 20 == 0:
        print("trial", trial, "no hit", len(cl), "sets", flush=True)
