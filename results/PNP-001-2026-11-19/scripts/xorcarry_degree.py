"""ALG-BIT-001 reproduction (director, 2026-11-19): degree-2 GF(2) refutations of minimal GF(3)-blind cores in the XOR/carry encoding.
Axioms per clause (a,b,c): L = 1+a+b+c, q = ab+ac+bc. Polynomials = GF(2) bitmasks over monomials.
 NS2       : 1 in span{q_i, L_j, x_k*L_j}, monomials NOT reduced (x^2 kept separate)   - owner's F8 identity is of this type
 NS2_bool  : same modulo x^2 = x (multilinear)
 PC2_bool  : degree-2 polynomial calculus mod x^2=x: closure of span{q_i, L_j} under (degree<=1 element) * variable
Labelled counts: cores canonicalised under S_n, each class weighted by n!/|Aut|."""
import json, sys, itertools, math, collections
n=int(sys.argv[1]); src=sys.argv[2]
cores=[[tuple(c) for c in x["clauses"]] for x in json.load(open(src))["cores"]]
def canon(cl):
    return min(tuple(sorted(tuple(sorted(p[v] for v in c)) for c in cl)) for p in itertools.permutations(range(n)))
def run(cl, boolean):
    # monomial index: () const, (i,) linear, (i,j) i<=j quadratic (i==j only if not boolean)
    mons={}
    def idx(m):
        if boolean and len(m)==2 and m[0]==m[1]: m=(m[0],)
        m=tuple(sorted(m))
        return mons.setdefault(m,len(mons))
    def poly(terms):
        b=0
        for m in terms: b^=1<<idx(m)
        return b
    L=[poly([(),(a,),(b,),(c,)]) for a,b,c in cl]
    Q=[poly([(a,b),(a,c),(b,c)]) for a,b,c in cl]
    Lt=[[(),(a,),(b,),(c,)] for a,b,c in cl]
    gens=L+Q+[poly([tuple(sorted(m+(k,))) for m in t]) for t in Lt for k in range(n)]
    def reduce_basis(vs):
        basis={}
        for v in vs:
            while v:
                h=v.bit_length()-1
                if h in basis: v^=basis[h]
                else: basis[h]=v; break
        return basis
    one=1<<idx(())
    def contains(basis, v):
        while v:
            h=v.bit_length()-1
            if h not in basis: return False
            v^=basis[h]
        return True
    B=reduce_basis(gens); ns=contains(B,one)
    if not boolean: return ns, None
    # PC2: repeatedly add x_k * (degree<=1 elements of the span)
    deg1mask=sum(1<<i for m,i in mons.items() if len(m)<=1)
    cur=reduce_basis(L+Q)
    while True:
        # degree<=1 subspace of cur: eliminate quadratic monomials
        qmask=sum(1<<i for m,i in mons.items() if len(m)==2)
        vs=list(cur.values()); low=[]
        piv={}
        for v in vs:
            w=v
            while w & qmask:
                h=(w&qmask).bit_length()-1
                if h in piv: w^=piv[h]
                else: piv[h]=w; w=None; break
            if w is not None and w: low.append(w)
        inv={i:m for m,i in mons.items()}
        new=[]
        for v in low:
            terms=[inv[i] for i in range(v.bit_length()) if v>>i&1]
            for k in range(n): new.append(poly([tuple(sorted(m+(k,))) for m in terms]))
        nb=reduce_basis(list(cur.values())+new)
        if len(nb)==len(cur): break
        cur=nb
    return ns, contains(cur,one)
classes={}
for cl in cores:
    k=canon(cl) if n<=7 else tuple(sorted(cl))
    classes.setdefault(k,cl)
res=collections.Counter(); first_fail=None
for k,cl in classes.items():
    w=math.factorial(n)//sum(1 for p in itertools.permutations(range(n)) if tuple(sorted(tuple(sorted(p[v] for v in c)) for c in k))==k) if n<=7 else 1
    a,_=run(cl,False); b,c=run(cl,True)
    key=("NS2" if a else "NS2_bool" if b else "PC2_bool" if c else "NEEDS_DEGREE>=3")
    res[key]+=w; res["total"]+=w
    if key=="NEEDS_DEGREE>=3" and first_fail is None: first_fail=k
print(f"n={n}: listed {len(cores)}, classes {len(classes)}, {'labelled' if n<=7 else 'listed'} counts: {dict(res)}")
if first_fail: print("first core needing degree >= 3:", first_fail)
