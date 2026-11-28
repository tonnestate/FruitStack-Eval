import itertools
X,Y=0b1100,0b1010; M=0xF   # truth tables of length 4, bit order: input index 0..3 = MSB..LSB
best={X:0,Y:0}
def dfs(funcs,size,maxs):
    for f in funcs:
        if f not in best or best[f]>size: best[f]=size
    if size==maxs: return
    new=set()
    for a in funcs:
        new.add(~a&M)
        for b in funcs: new.add(a&b); new.add(a|b)
    for g in new-set(funcs): dfs(funcs+(g,),size+1,maxs)
dfs((X,Y),0,5)
tt=lambda f: format(f,'04b')
assert len(best)==16, len(best)
for s in range(0,6):
    L={tt(f) for f,c in best.items() if c<=s}
    for t in range(0,5):
        cls={}
        for p in map(''.join,itertools.product('01',repeat=t)):
            key=frozenset(z for z in map(''.join,itertools.product('01',repeat=4-t)) if p+z in L)
            cls.setdefault(key,[]).append(p)
        bound=1+len({w[:t] for w in L})
        print(f"s={s} |L|={len(L)} t={t} I_t={len(cls)} bound={bound}")
        assert len(cls)<=bound
