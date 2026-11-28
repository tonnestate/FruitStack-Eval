"""Degree-bounded Groebner refutation degree (director 2026-11-20, owner request). Measure: smallest d such that Singular std() with
degBound = d over the Boolean quotient ring F[x]/(x_i^2 - x_i) contains 1 (ordering dp). Close to, but not identical with, the PC degree;
an experiment supporting hypotheses, not a proof. Families: Tseitin (XOR-SAT, odd total charge) over F2 vs F3; subset sum sum x_i = n+1
over F101 (calibration); 3-colouring Col(G) and our F(G) (positive 1-in-3 as CNF) over F2 and F3."""
import itertools, subprocess, sys, json, time
def mono(vs):  return "*".join(vs) if vs else "1"
def indicator(vars_, bits):  return "*".join(f"x({v})" if b else f"(1-x({v}))" for v, b in zip(vars_, bits))
def tseitin(edges, nv):
    inc = {v: [i + 1 for i, e in enumerate(edges) if v in e] for v in range(nv)}
    charge = {v: (1 if v == 0 else 0) for v in range(nv)}                     # total charge odd -> unsatisfiable
    polys = []
    for v, es in inc.items():
        bad = [a for a in itertools.product((0, 1), repeat=len(es)) if sum(a) % 2 != charge[v]]
        polys.append("+".join(indicator(es, a) for a in bad))
    return len(edges), polys
def colouring(V, E):
    idx = {}; 
    for v in range(V):
        for c in range(3): idx[(v, c)] = len(idx) + 1
    P = [f"x({idx[(v,0)]})+x({idx[(v,1)]})+x({idx[(v,2)]})-1" for v in range(V)]
    P += [f"x({idx[(v,a)]})*x({idx[(v,b)]})" for v in range(V) for a, b in ((0,1),(0,2),(1,2))]
    P += [f"x({idx[(u,c)]})*x({idx[(w,c)]})" for u, w in E for c in range(3)]
    return len(idx), P
def fG(V, E):
    idx = {}
    def var(k):
        if k not in idx: idx[k] = len(idx) + 1
        return f"x({idx[k]})"
    clauses = [[var(("x", v, c)) for c in range(3)] for v in range(V)] + [[var(("x", u, c)), var(("x", w, c)), var(("y", u, w, c))] for u, w in E for c in range(3)]
    P = []
    for a, b, c in clauses:
        P += [f"(1-{a})*(1-{b})*(1-{c})", f"{a}*{b}", f"{a}*{c}", f"{b}*{c}"]
    return len(idx), P
def subset(n): return n, ["+".join(f"x({i})" for i in range(1, n + 1)) + f"-{n + 1}"]
def gdeg(nvars, polys, char, dmax, tlimit=240):
    for d in range(1, dmax + 1):
        src = (f'ring r = {char},(x(1..{nvars})),dp; ideal B; int i; for(i=1;i<={nvars};i++){{B[i]=x(i)^2-x(i);}} qring Q = std(B);\n'
               f'ideal I = {",".join(polys)};\n degBound = {d}; ideal G = std(I); if (reduce(1,G)==0) {{"YES";}} else {{"NO";}} quit;\n')
        try:
            out = subprocess.run(["Singular", "-q"], input=src, capture_output=True, text=True, timeout=tlimit).stdout
        except subprocess.TimeoutExpired:
            return f">{d - 1} (timeout at d={d})"
        if "YES" in out: return d
        if "NO" not in out: return f"error: {out[-200:]}"
    return f">{dmax}"
K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
K33 = [(a, b) for a in range(3) for b in range(3, 6)]
PRISM = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
Q3 = [(a, b) for a in range(8) for b in range(a+1, 8) if bin(a ^ b).count("1") == 1]
PET = [(i, (i+1) % 5) for i in range(5)] + [(5+i, 5+(i+2) % 5) for i in range(5)] + [(i, 5+i) for i in range(5)]
W5 = [(0, i) for i in range(1, 6)] + [(i, i % 5 + 1) for i in range(1, 6)]          # odd wheel: hub 0 + C5, not 3-colourable
if __name__ == "__main__":
    rows = []
    for name, E, nv in (("K4", K4, 4), ("K33", K33, 6), ("prism", PRISM, 6), ("Q3", Q3, 8), ("Petersen", PET, 10)):
        n, P = tseitin(E, nv)
        for ch in (2, 3):
            t = time.time(); d = gdeg(n, P, ch, 8); rows.append(("Tseitin", name, n, f"F{ch}", d, round(time.time() - t, 1)))
            print(*rows[-1], flush=True)
    for n in range(2, 11):
        t = time.time(); rows.append(("SubsetSum n+1", f"n={n}", n, "F101", gdeg(*subset(n), 101, n + 2), round(time.time() - t, 1))); print(*rows[-1], flush=True)
    for name, (V, E) in (("K4", (4, K4)), ("W5", (6, W5))):
        for fam, build in (("Col(G)", colouring), ("F(G)", fG)):
            n, P = build(V, E)
            for ch in (2, 3):
                t = time.time(); rows.append((fam, name, n, f"F{ch}", gdeg(n, P, ch, 6), round(time.time() - t, 1))); print(*rows[-1], flush=True)
    json.dump(rows, open("gdeg_results.json", "w"), indent=1)
