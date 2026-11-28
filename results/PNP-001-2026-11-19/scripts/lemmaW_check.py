"""Sanity check of Lemma W's construction: for random B over GF(3), a tree decomposition of G_B of width w yields (via tau = a bag containing
supp(r_i)) a matroid tree decomposition whose node widths sum_j r(E\\F_j) - (k-1) r(E) are all <= w + 1."""
import random, itertools, networkx as nx
from networkx.algorithms.approximation import treewidth_min_degree
random.seed(3)
def rank3(vecs, d):
    M=[list(v) for v in vecs]; r=0
    for c in range(d):
        p=next((i for i in range(r,len(M)) if M[i][c]%3),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=1 if M[r][c]==1 else 2; M[r]=[(x*inv)%3 for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]: f=M[i][c]; M[i]=[(a-f*b)%3 for a,b in zip(M[i],M[r])]
        r+=1
    return r
viol=checks=0; maxgap=-99
for trial in range(400):
    d=random.randint(2,7); n=random.randint(d,14); dens=random.choice([0.2,0.35,0.6])
    while True:
        R=[[random.choice((1,2)) if random.random()<dens else 0 for _ in range(d)] for _ in range(n)]
        if rank3(R,d)==d: break
    G=nx.Graph(); G.add_nodes_from(range(d))
    for r in R:
        s=[j for j in range(d) if r[j]]
        G.add_edges_from(itertools.combinations(s,2))
    w,TD=treewidth_min_degree(G)
    bags=list(TD.nodes())
    tau=[next(b for b in bags if set(j for j in range(d) if r[j])<=set(b)) for r in R]
    for t in bags:
        nbrs=list(TD.neighbors(t)); k=len(nbrs)
        if k==0: continue
        H=TD.copy(); H.remove_node(t); width=-(k-1)*d
        for nb in nbrs:
            comp=nx.node_connected_component(H,nb)
            rest=[R[i] for i in range(n) if tau[i] not in comp]
            width+=rank3(rest,d)
        checks+=1; viol+= width>w+1; maxgap=max(maxgap,width-(w+1))
print(f"Lemma W construction: {checks} node checks over 400 random B (d<=7, n<=14): violations {viol}, max(width-(w+1)) = {maxgap}")
