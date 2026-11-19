import itertools
# (1) mSP >= N+1 needs every clause to be RELEVANT (in some minimal UNSAT set) - else an ideal program could drop it. Check n=6.
n=6; U=list(itertools.combinations(range(n),3)); X=list(itertools.product((0,1),repeat=n))
ok={}
for x in X:
    for i,c in enumerate(U):
        pass
# a clause c is relevant iff some MUS contains it; by symmetry it suffices to find one MUS containing clause 0 and use S_6-transitivity on triples
cl=[(0,1,2),(0,1,3),(0,2,3),(0,4,5),(1,2,4)]      # owner's n=6 example, GF(3)-blind, minimal?
def sat(F): return any(all(sum(x[v] for v in c)==1 for c in F) for x in X)
print("example UNSAT:", not sat(cl), "| every proper subset SAT (minimal):", all(sat(cl[:i]+cl[i+1:]) for i in range(len(cl))))
# (2) Lemma 3 hypotheses on the computed P4: four distinct elements, three 2-sets, no member inside {a,d}
P4=[{"126","124"},{"124","145"},{"145","123"}]; elems=set().union(*P4); a,b,c,d="126","124","145","123"
print("4 distinct elements:", len(elems)==4, "| path a-b-c-d:", P4==[{a,b},{b,c},{c,d}], "| no member within {a,d}:", not any(m<= {a,d} for m in P4), "| {b,d} not a member:", {b,d} not in P4)
