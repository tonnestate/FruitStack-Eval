"""ACC0 level 3e (director, 2026-11-20, owner correction): counting semantics of algorithm R.
R enumerates complete Boolean solutions (x,y) of A(x,y)=b, so it counts PAIRS. The projected count #{x : exists y} equals it iff every
accepted x has exactly one witness. Checks: owner counterexample; class D (linearly determined aux) always unique; random C0-exists
systems with free auxiliaries frequently differ."""
import itertools, random
def counts(rows,b,n,k):
    pairs=0; xs=set()
    for z in itertools.product((0,1),repeat=n+k):
        if all(sum(a*v for a,v in zip(r,z))%3==bb for r,bb in zip(rows,b)): pairs+=1; xs.add(z[:n])
    return pairs,len(xs)
print("owner counterexample (constraint x = 0, one free aux y):", counts([[1,0]],[0],1,1), "(pairs, projected)")
random.seed(9); dbad=0; gen_diff=0; T=300
for _ in range(T):
    n=random.randint(1,6); E=[[random.randint(0,2) for _ in range(n)] for _ in range(random.randint(0,3))]
    N=[[random.randint(0,2) for _ in range(n)] for _ in range(random.randint(0,3))]; k=len(N)
    rows=[e+[0]*k for e in E]+[N[j]+[2 if i==j else 0 for i in range(k)] for j in range(k)]   # N_j x - y_j = c_j + 1
    b=[random.randint(0,2) for _ in E]+[random.randint(0,2) for _ in N]
    p,q=counts(rows,b,n,k); dbad+= p!=q
    k2=random.randint(1,3); rows2=[[random.randint(0,2) for _ in range(n+k2)] for _ in range(random.randint(1,3))]; b2=[random.randint(0,2) for _ in rows2]
    p2,q2=counts(rows2,b2,n,k2); gen_diff+= p2!=q2
print(f"class D (linearly determined aux): pairs != projected in {dbad} of {T}; random C0-exists with free aux: differ in {gen_diff} of {T}")
