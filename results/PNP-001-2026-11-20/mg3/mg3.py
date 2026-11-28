"""T41 §14e (owner's MG-3), PI check.
(1) T = [[a,b],[c,e]]: T^{(x)3} EXACT1_3 has weight entries f0..f3 = 3a^2 b, a^2 e + 2abc, b c^2 + 2ace, 3 c^2 e.
(2) Parity condition (f0 = f2 = 0 or f1 = f3 = 0) with det != 0 forces T monomial: Groebner bases with det*t - 1.
(3) Owner's propagation counterexample: E(0,1,2), E(0,3,4), E(0,5,6), E(1,3,5): no two clauses share two variables, no unit
    clause, but x0 = 0 in every solution; count = 3."""
import itertools, json, sympy as sp
a,b,c,e,t=sp.symbols("a b c e t")
T=sp.Matrix([[a,b],[c,e]]); T3=sp.kronecker_product(T,T,T)
f=sp.Matrix([int(sum(x)==1) for x in itertools.product((0,1),repeat=3)])
g=T3*f
w={0:g[0],1:g[1],2:g[3],3:g[7]}                     # indices 000, 001, 011, 111 (symmetric signature)
claimed={0:3*a**2*b,1:a**2*e+2*a*b*c,2:b*c**2+2*a*c*e,3:3*c**2*e}
formulas_ok=all(sp.expand(w[k]-claimed[k])==0 for k in w)
sym_ok=all(sp.expand(g[i]-w[sum(x)])==0 for i,x in enumerate(itertools.product((0,1),repeat=3)))
inv=(a*e-b*c)*t-1
G_even=sp.groebner([w[0],w[2],inv],t,a,b,c,e,order="lex")
G_odd=sp.groebner([w[1],w[3],inv],t,a,b,c,e,order="lex")
monomial_even=all(sp.groebner(list(G_even.exprs)+[x],t,a,b,c,e,order="lex").exprs==[x] or True for x in ())
# reduce b and c (resp. a and e) modulo the ideal: they must lie in the radical -> check b^k, c^k reduce to 0 for small k
in_rad=lambda G,x: any(G.reduce(x**k)[1]==0 for k in range(1,5))
cl=[(0,1,2),(0,3,4),(0,5,6),(1,3,5)]
sols=[x for x in itertools.product((0,1),repeat=7) if all(sum(x[i] for i in q)==1 for q in cl)]
pairs_share2=any(len(set(p)&set(q))>=2 for p,q in itertools.combinations(cl,2))
out=dict(f_prime_formulas=formulas_ok,symmetric=sym_ok,
         even_case_forces_b_c_zero=in_rad(G_even,b) and in_rad(G_even,c),
         odd_case_forces_a_e_zero=in_rad(G_odd,a) and in_rad(G_odd,e),
         propagation_example=dict(count=len(sols),x0_always_0=all(s[0]==0 for s in sols),some_pair_shares_two=pairs_share2))
json.dump(out,open("mg3.out.json","w"),indent=1); print(out)
