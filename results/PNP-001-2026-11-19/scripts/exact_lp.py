"""Exact rational LP optimum over {t in Q^d : a_i . t >= b_i} for small d, certified:
HiGHS finds an optimal vertex in floating point; the host rebuilds it EXACTLY from d linearly independent tight constraints (rational solve),
checks exact feasibility, and certifies optimality by an exact dual y >= 0 on the tight set with sum y_i a_i = c (LP duality).
Returns (value, vertex) with exact Fractions, or None if certification fails (caller falls back to exact vertex enumeration)."""
from fractions import Fraction as Fr
import itertools
import numpy as np
from scipy.optimize import linprog
def _rref(M):
    M=[row[:] for row in M]; piv=[]; r=0
    for c in range(len(M[0])):
        p=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r],M[p]=M[p],M[r]; inv=M[r][c]; M[r]=[v/inv for v in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0: f=M[i][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        piv.append(c); r+=1
    return M[:r], piv
def exact_min(c, cons):
    d=len(c)
    if d==0: return (Fr(0), [])
    A=np.array([[float(x) for x in a] for a,b in cons]); b=np.array([float(b) for a,b in cons])
    res=linprog([float(x) for x in c], A_ub=-A, b_ub=-b, bounds=[(None,None)]*d, method="highs")
    if res.status!=0: return None
    t=res.x; slack=A@t-b
    tight=[i for i in np.argsort(np.abs(slack)) if abs(slack[i])<1e-7]
    # choose d independent tight constraints, solve exactly
    chosen=[]; rows=[]
    for i in tight:
        trial=rows+[list(cons[i][0])]
        _,pv=_rref([r[:] for r in trial])
        if len(pv)==len(trial): rows=trial; chosen.append(i)
        if len(chosen)==d: break
    if len(chosen)<d: return None
    R,pv=_rref([[*cons[i][0], cons[i][1]] for i in chosen])
    v=[R[k][d] for k in range(d)]
    if not all(sum(x*y for x,y in zip(a,v))>=bb for a,bb in cons): return None
    # exact dual on ALL exactly-tight constraints: y >= 0, sum y_i a_i = c  (small exact LP via enumeration of d-subsets of tight set)
    T=[i for i in range(len(cons)) if sum(x*y for x,y in zip(cons[i][0],v))==cons[i][1]]
    for sub in itertools.combinations(T, d):
        Rm,pv2=_rref([[cons[i][0][g] for i in sub]+[c[g]] for g in range(d)])
        if len(pv2)<d or (pv2 and pv2[-1]==d): continue
        y=[Rm[k][d] for k in range(d)]
        if all(x>=0 for x in y): return (sum(x*y_ for x,y_ in zip(c,v)), v)
    return None
