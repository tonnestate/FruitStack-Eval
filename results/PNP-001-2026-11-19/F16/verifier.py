"""Independent, exact checker for an XOR/carry 1-in-3-SAT degree-3 witness.

Python standard library only. Input files next to this script:
PNP-001_Iterated_Degree2_Best_Counterexample.json
PNP-001_Degree3_Nullstellensatz_Certificate.json

All operations are exact modulo 2/3 or Boolean enumeration with propagation.
The model uses, per clause {a,b,c}, two axioms in GF(2)[x]/<x_i^2+x_i>:
  L = 1+x_a+x_b+x_c = 0
  Q = x_ax_b+x_ax_c+x_bx_c = 0.
"""
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import json

ROOT=Path(__file__).resolve().parent
instance=json.loads((ROOT/'PNP-001_Iterated_Degree2_Best_Counterexample.json').read_text())
proof=json.loads((ROOT/'PNP-001_Degree3_Nullstellensatz_Certificate.json').read_text())
F=tuple(tuple(c) for c in instance['clauses']); n=instance['n']; m=len(F)
assert n==16 and m==11 and len({v for c in F for v in c})==16
assert len(set(F))==m and all(len(set(c))==3 for c in F)
assert [tuple(c) for c in proof['clauses']]==list(F)

# Small exact polynomial ring of multilinear monomials with maximum total degree 3.
monomials=[0]+[1<<i for i in range(n)]+[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]+[(1<<i)|(1<<j)|(1<<k) for i,j,k in combinations(range(n),3)]
index={x:i for i,x in enumerate(monomials)}
assert len(index)==697

def poly(mons):
    v=0
    for b in mons:v^=1<<index[b]
    return v

def mul(p, term):
    """Boolean-ring multiplication by one monomial, with x_i*x_i=x_i."""
    out=0
    while p:
        low=p&-p;k=low.bit_length()-1
        combined=monomials[k]|term
        assert combined in index, 'degree > 3'
        out ^= 1<<index[combined]
        p ^= low
    return out

L=[poly([0]+[1<<v for v in c]) for c in F]
Q=[poly([(1<<i)|(1<<j) for i,j in combinations(c,2)]) for c in F]

# 1. Independently check identity 1 = sum_i M_i L_i + sum_j N_j Q_j, degree <=3.
accumulator=0
for item in proof['certificate_summands']:
    c=tuple(item['clause']); multiplier=sum(1<<i for i in item['multiplier_variable_indices'])
    typ=item['source'];i=F.index(c)
    assert multiplier.bit_count()<=(2 if typ=='L' else 1)
    accumulator ^=mul(L[i] if typ=='L' else Q[i],multiplier)
assert accumulator==1, 'the degree 3 identity is invalid'

# 2. Exhaustive Boolean DPLL refutation, with re-run on each one-clause deletion.
def dpll(clauses, assignments):
    assignments=list(assignments)
    while True:
        changed=False
        for c in clauses:
            ones=sum(assignments[i]==1 for i in c)
            unknown=[i for i in c if assignments[i]<0]
            if ones>1 or ones+len(unknown)<1:return False,1
            if ones==1:
                for i in unknown:assignments[i]=0;changed=True
            elif ones==0 and len(unknown)==1:
                assignments[unknown[0]]=1;changed=True
        if not changed:break
    if all(all(assignments[i]>=0 for i in c) for c in clauses):
        assert all(sum(assignments[i] for i in c)==1 for c in clauses)
        return assignments,1
    scores=[0]*n
    for c in clauses:
        for i in c:
            if assignments[i]<0:scores[i]+=1
    k=max(range(n),key=lambda i:scores[i])
    assert scores[k]>0
    count=1
    for val in (0,1):
        nxt=assignments[:];nxt[k]=val
        result,calls=dpll(clauses,nxt)
        count+=calls
        if result is not False:return result,count
    return False,count

sat_result,unsat_nodes=dpll(F,[-1]*n)
assert sat_result is False
minimal_witnesses=[]
for i in range(m):
    sat_solution,_=dpll(F[:i]+F[i+1:],[-1]*n)
    assert sat_solution is not False
    minimal_witnesses.append(''.join(str(max(0,v)) for v in sat_solution))

# 3. GF(3) RREF plus explicit solution (free variables = 0)
M=[[int(j in c) for j in range(n)]+[1] for c in F]
rank3=0; pivots=[]
for col in range(n):
    candidate=next((i for i in range(rank3,m) if M[i][col]),None)
    if candidate is None:continue
    M[rank3],M[candidate]=M[candidate],M[rank3]
    scale=pow(M[rank3][col],-1,3)
    M[rank3]=[(x*scale)%3 for x in M[rank3]]
    for k in range(m):
        if k==rank3 or not M[k][col]:continue
        mult=M[k][col]
        M[k]=[(a-mult*b)%3 for a,b in zip(M[k],M[rank3])]
    pivots.append(col);rank3+=1
assert all(any(row[:n]) or row[n]==0 for row in M)
x3=[0]*n
for r,j in enumerate(pivots):x3[j]=M[r][n]
assert all(sum(x3[i] for i in c)%3==1 for c in F)

# 4. INDEPENDENT degree-2 closure: start with L,Q,x_i*L; close under
#    multiplication of every newly derived linear consequence by every x_i.
maxcol=1+n+n*(n-1)//2
assert maxcol==137
MASK=(1<<maxcol)-1
basis={}

def add_to_span(x):
    assert 0<=x<=MASK
    while x:
        k=x.bit_length()-1
        if k not in basis:
            basis[k]=x
            return True
        x^=basis[k]
    return False

def degree2_term(x):return x & MASK

for i in range(m):
    add_to_span(L[i]);add_to_span(Q[i])
    for j in range(n):add_to_span(mul(L[i],1<<j))

linear_seen=set()
rounds=0
while True:
    new=[p for k,p in basis.items() if k<=n and p not in linear_seen]
    if not new:break
    rounds+=1
    for line in new:
        linear_seen.add(line)
        for j in range(n):add_to_span(mul(line,1<<j))
assert 0 not in basis, 'degree-2 contradiction exists'

# 5. Construct an independent linear functional E on degree <= 2 polynomials,
# E[1]=1, E[any line generated by degree-2 PC] = 0. This is a dual
# certificate of the nonexistence of degree-2 refutations.
augmented=[p for p in basis.values()]+[1|(1<<maxcol)]
nsys=len(augmented); row=0;pivot_columns=[]
for col in range(maxcol):
    r=next((j for j in range(row,nsys) if augmented[j]>>col&1),None)
    if r is None:continue
    augmented[row],augmented[r]=augmented[r],augmented[row]
    for j in range(nsys):
        if j!=row and (augmented[j]>>col&1):augmented[j]^=augmented[row]
    pivot_columns.append(col);row+=1
assert not any((v&MASK)==0 and (v>>maxcol&1) for v in augmented)
functional=0
for i,col in enumerate(pivot_columns):
    if augmented[i]>>maxcol&1:functional |=1<<col
assert functional&1
assert all((p&functional).bit_count()%2==0 for p in basis.values())

report={
  'n':n,'m':m,'clauses':[list(c) for c in F],
  'GF3_rank':rank3,'GF3_solution_count':3**(n-rank3),'GF3_explicit_solution':x3,
  'GF2_degree2_basis_dimension':maxcol,'GF2_degree2_closure_rank':len(basis),
  'GF2_degree2_codimension':maxcol-len(basis),
  'GF2_degree2_rounds':rounds,
  'GF2_degree2_dual_functional_hex':hex(functional),
  'GF2_degree2_dual_functional_monoms_1_bits':[monomials[j] for j in range(maxcol) if functional>>j&1],
  'degree3_nullstellensatz_summands':len(proof['certificate_summands']),
  'degree3_identity_exact_mod_boolean':True,
  'DPLL_unsat':True,'DPLL_nodes':unsat_nodes,'clause_minimal':True,
  'minimality_satisfying_assignments_after_removing_clause':minimal_witnesses,
  'model':'GF(2) XOR/carry with Boolean axioms; PC degree in this fixed encoding',
  'caution':'No claim of minimum variable count or of lower bounds in other encodings.'
}
output=ROOT/'PNP-001_F16_Exact_Verification_Report.json'
output.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('CONFIRMED n',n,'m',m,'GF3',rank3,'GF3_points',3**(n-rank3))
print('CONFIRMED UNSAT DPLL nodes',unsat_nodes,'clause minimal',True)
print('CONFIRMED NO DEGREE2 PC: closure rank',len(basis),'of',maxcol,'dual E[1]=1 and annihilates closure')
print('CONFIRMED DEGREE3: 82-term NS certificate identity, exactly 1')
print('Saved',output)
