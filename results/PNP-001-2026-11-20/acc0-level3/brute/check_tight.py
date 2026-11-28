"""Theorem B check: best representation surplus equals the affine-hull bound  <=>  f in D (equalities + dis-equalities).
n = 3: all 255 nonzero functions; n = 4: all functions representable with k <= 3, against exact D membership."""
import itertools, collections
from analyse import data, daff, pts
def in_D(f,n):
    P=[tuple((x>>j)&1 for j in range(n)) for x in range(2**n)]; ones=[P[x] for x in range(2**n) if f>>x&1]; acc=set(P)
    for a in itertools.product(range(3),repeat=n):
        val=[sum(ai*xi for ai,xi in zip(a,x))%3 for x in P]; vo={sum(ai*xi for ai,xi in zip(a,x))%3 for x in ones}
        for c in range(3):
            if vo=={c}: acc&={P[i] for i in range(2**n) if val[i]==c}
            if c not in vo: acc&={P[i] for i in range(2**n) if val[i]!=c}
    return acc==set(ones)
for n in (3,4):
    c=collections.Counter()
    for f in range(1,2**(2**n)):
        ks=data.get((n,f))
        if not ks: continue
        tight = n-min(d for d,_ in ks.values()) == n-daff(pts(n,f))
        c[(tight,in_D(f,n))]+=1
    print(f"n={n}: (at bound, in D) counts over representable f: {dict(c)}")
