"""Isomorphism classes of the listed minimal blind cores under full variable permutation (director, 2026-11-19, owner check).
Clause-variable incidence graph with ALL n variable nodes (unused variables isolated); class = graph isomorphism respecting sides.
Orbit size (labelled cores on [n]) = n!/|Aut|, |Aut| = number of side-preserving automorphisms (clauses are distinct, so each variable
permutation fixing the clause set gives exactly one automorphism)."""
import json, sys, math, collections
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
n=int(sys.argv[1]); r=json.load(open(sys.argv[2]))
def graph(cl):
    G=nx.Graph(); G.add_nodes_from((("v",i) for i in range(n)), side=0)
    for c in cl:
        G.add_node(("c",c), side=1); G.add_edges_from((("c",c),("v",v)) for v in c)
    return G
nm=lambda a,b: a["side"]==b["side"]
seen=set(); buckets=collections.defaultdict(list)
for x in r["cores"]:
    cl=tuple(sorted(tuple(c) for c in x["clauses"]))
    if cl in seen: continue
    seen.add(cl); G=graph(cl)
    h=nx.weisfeiler_lehman_graph_hash(G, node_attr="side", iterations=4)
    for rep in buckets[h]:
        if GraphMatcher(rep["G"],G,node_match=nm).is_isomorphic(): rep["members"]+=1; rep["kinds"].add(x["cert"]["kind"]); break
    else: buckets[h].append({"G":G,"cl":cl,"members":1,"kinds":{x["cert"]["kind"]}})
classes=[c for b in buckets.values() for c in b]
tot=0; byvars=collections.Counter(); kinds=collections.Counter()
for c in classes:
    aut=sum(1 for _ in GraphMatcher(c["G"],c["G"],node_match=nm).isomorphisms_iter())
    tot+=math.factorial(n)//aut; byvars[len({v for cl in c["cl"] for v in cl})]+=1; kinds[tuple(sorted(c["kinds"]))]+=1
print(f"n={n}: listed {len(r['cores'])}, distinct clause sets {len(seen)}, isomorphism classes {len(classes)}, by #variables {dict(sorted(byvars.items()))}")
print(f"orbit-weighted sum (labelled cores on [{n}]): {tot}")
print("certificate kinds per class:", dict(kinds))
json.dump({"n":n,"classes":[{"clauses":[list(c) for c in cl["cl"]],"members":cl["members"],"orbit":math.factorial(n)//sum(1 for _ in GraphMatcher(cl["G"],cl["G"],node_match=nm).isomorphisms_iter())} for cl in classes]}, open(sys.argv[2].replace(".json","")+"_classes.json","w"))
