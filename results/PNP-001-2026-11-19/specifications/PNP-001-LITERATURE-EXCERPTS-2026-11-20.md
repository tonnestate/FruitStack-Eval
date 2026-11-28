# PNP-001 literature excerpts for agents (director, 2026-11-20)
Agents cannot open /root/fruits/research/PNP-001/literature/sources/*; read the cited passages here (short verbatim excerpts for internal research use, line numbers refer to the local pdftotext copies). Read with spec_read("PNP-001-LITERATURE-EXCERPTS-2026-11-20.md").

## HIW23 - Hirahara, Ilango, Williams, Beating Brute Force for Compression Problems, ECCC TR23-171
```
  Abstract
  A compression problem is defined with respect to an efficient encoding function f ; given a
  string x, our task is to find the shortest y such that f (y) = x. The obvious brute-force algorithm
  for solving this compression task on n-bit strings runs in time O(2ℓ · t(n)), where ℓ is the length
  of the shortest description y and t(n) is the time complexity of f when it prints n-bit output.
  We prove that every compression problem has a Boolean circuit family which finds short de-
  scriptions more efficiently than brute force. In particular, our circuits have size 24ℓ/5 · poly(t(n)),
  which is significantly more efficient for all ℓ ≫ log(t(n)). Our construction builds on Fiat-Naor’s
  data structure for function inversion [SICOMP 1999]: we show how to carefully modify their
  data structure so that it can be nontrivially implemented using Boolean circuits, and we show
  how to utilize hashing so that the circuit size is only exponential in the description length.
  As a consequence, the Minimum Circuit Size Problem for generic fan-in two circuits of size
  4
  s(n) on truth tables of size 2n can be solved by circuits of size 2 5 ·w+o(w) · poly(2n ), where
  w = s(n) log2 (s(n) + n). This improves over the brute-force approach of trying all possible
  size-s(n) circuits for all s(n) ≥ n. Similarly, the task of computing a short description of a
  4
Smaller Circuits for MCSP. The first major consequence of Theorem 1.2 is a Boolean circuit
family for MCSP that decisively beats exhaustive search. It has been conjectured since the 1950s
that any algorithm solving MCSP must exhaustively search over all possible circuits (see Trakht-
enbrot [Tra84] for a fascinating history of these “perebor” conjectures). Our results refute this
conjecture when we are allowed non-uniform circuits as our algorithmic model.
  In more detail, we consider circuits of fan-in two over any desired basis. Let Search-MCSP[s(n)]
be the search problem:
  Given a truth table T of length 2n , determine if the function f : {0, 1}n → {0, 1}
  represented by T has a circuit of at most s(n) gates, and if so, produce an encoding of
  such a circuit.
  The obvious algorithm for this search problem requires time 2O(s(n) log2 s(n)) · 2n · poly(s(n)):
enumerate over all 2O(s(n) log2 s(n)) circuits C of size s(n) with n inputs, and evaluate C on all 2n
possible inputs in 2n · poly(s(n)) time. The MCSP problem and its search version are believed to
be NP-hard, but their complexities remain (infamously) open (cf. [Hir22; Ila23] for some recent
developments).
  Using tight and efficient circuit encodings, we obtain an improvement over the trivial enumer-
ation algorithm for all circuit sizes s(n) ≥ n.
Theorem 1.3. For all size functions s(n), Search-MCSP[s(n)] on truth tables of size 2n can be
  4
solved by circuits of size 2 5 ·w+o(w) · poly(2n ), where w = s(n) log2 (s(n) + n).
  4  2  2
  Thus for example, there is a Boolean circuit C of size only 2 5 n log(n)+o(n log(n)) · poly(2n ) which,
given any truth table of length 2n as input, C outputs the description of a circuit with n2 gates for
the truth table, whenever such a circuit exists.

Smaller Circuits for MINKT. Theorem 1.2 is very general, and applies in a wide range of
1.2  Intuition
The starting point of our approach comes from cryptography, namely the problem of inverting a
function f : {0, 1}n → {0, 1}n using a minimal number of black-box calls to f . In particular, given
a y ∈ {0, 1}n , we wish to find an x such that f (x) = y. Following the pioneering work of [Hel80]
on data structures for inverting random functions, Fiat and Naor [FN99] presented data structures
with a rigorous time-space tradeoff. In particular, for f : {0, 1}n → {0, 1}n construed as an oracle,
Fiat and Naor show that one can construct a data structure with S bits of memory that can be
queried for function inversion in time T , where T · S 3 = 23n · poly(n). Setting T = S = 23n/4 , for
every fixed f we obtain a data structure storing 23n/4 · poly(n) bits such that, given any y in the
range of f , the data structure will output a pre-image of y in about 23n/4 steps.
  Given the power and generality of function inversion, one might wonder if it can be used to
build a non-trivial “data structure” for solving an NP-complete problem like CircuitSAT faster than
2n time. A natural first attempt is to set f to take a circuit C and a string w as input, outputting
C if C(w) = 1 and ⊥ otherwise. Given a worst-case inverter for f , one could attempt to solve
CircuitSAT by attempting to invert f on C.
  One major difficulty in carrying out such an approach is that the input length to the function
f is too large. If the circuit C has n inputs, the witness w and C both need at least n bits to
describe. (Note that, if the circuits or the witnesses could be described in say 0.9n bits, then we
could already trivially improve over 2n time by simply storing a 20.9n -size lookup table over the
circuits, or the witnesses.) Thus, f takes at least 2n input bits, and so the inversion circuit obtained
from Fiat-Naor has size at least 26n/4 ≫ 2n , which is worse than brute force.
  In contrast, the witness in a compression problem already encodes the input, so the previous
paragraph is not an issue. Indeed, if we simply apply Fiat-Naor’s function inversion to the Eval
function of a compression problem, we immediately obtain a data structure that takes 23n/4 space
and can compress n-bit queries in 23n/4 time for an arbitrary compression problem.
  However, there remain two issues in the generality of this simple approach, which we overcome.

  1. The first is a technical algorithmic issue. The data structure of Fiat-Naor requires random
  access to its storage, and the most obvious way of converting such a data structure to a circuit


  3
  would blow up the size by an intolerable amount (cf. footnote 2 of [DTT10]). This issue is
  what prevented Ren and Santhanam [RS21] from giving non-trivial circuits for MINKT via
  their equivalence between one-way functions (with exponential security) and the hardness
  of MINKT. (Note: this tight connection is not known for other compression problems, like
  MCSP.) We show how to implement Fiat-Naor with standard Boolean circuits, at the cost of a
  slightly larger circuit (the exponent in the circuit size becomes 4/5, rather than the exponent
  of 3/4). This requires us to be very careful about certain parts of the inversion procedure;
  we have to worry over details that Fiat and Naor did not worry about. As a result, we have
  to adapt both the inversion procedure and the analysis of it, in order to achieve our circuit
  size bound. Roughly speaking, by performing the necessary table lookups in large enough
  query batches, and adjusting the sizes of lookup tables in the analysis, it is possible to design
  nontrivial circuits that simulate the data structure by performing variations on sorting.
  2. The second problem is more fundamental. Fiat-Naor only provides a 23n/4 time data structure
  and algorithm for inversion, where n is the length of the input we wish to invert. Such a bound
  is useless when our desired description length ℓ is less than 3n/4, in which case the 2ℓ cost
  of brute-force enumeration is faster than Fiat-Naor! (For example, in the case of MCSP, we
  n
  would obtain a 20.75·2 -time data structure for solving MCSP on truth tables of length 2n .)
  That is, naively applying Fiat-Naor only yields an improvement over exhaustive search in the
```

## MMW19 - McKay, Murray, Williams, STOC 2019 (two-column layout: theorems are in the right column)
```
Wil08, BW15], so there is hope that such lower bounds could be  to Σ3 SATA and can make short queries to the oracle.
proved.
  In this work, we show (among many other results) that an  Theorem 1.2 (Section 4). Let s(n) ≥ n for all n, where s(n) is
N · poly(log N )-time lower bound on poly(log N )-space determin-  time constructible. Let A : {0, 1}⋆ → {0, 1} be an arbitrary oracle.
istic streaming algorithms for MCSP[nc ] is already as difficult as  There is a (one-pass) streaming algorithm for search-MCSPA [s(n)] on
separating P from NP! Note that deterministic streaming algorithms  2n -bit inputs running in 2n · Õ(s(n)) time with Õ(s(n)2 ) update time
are very restricted (one cannot even compute whether two given  and Õ(s(n)) space, using an oracle for Σ3 SATA with queries of length
N -bit strings are equal with o(N ) space). Our result is one conse-  Õ(s(n)).
quence of a more general theorem proved about a generalization of  One way to prove Theorem 1.2 would be to show that the circuit
MCSP, in which we allow compression by circuits with oracle gates  family derived in Theorem 1.1 can be evaluated in a time and space-
(as defined in prior work [AHK17, IKV18]). This “boosting” of a  efficient way. We instead give a direct proof (an explicit streaming
modest time-space lower bound for an NP problem to P , NP can  algorithm).
be seen as a form of hardness magnification, a term recently coined
by Oliveira and Santhanam [OS18]. Intuitively, a hardness magnifi-  Weak Streaming Lower Bounds for Compression Imply P , NP.
cation result is a kind of “slippery slope” theorem, showing how a  Applying the assumption P = NP to the oracle calls in Theorem 1.2,
very modest-looking lower bound for a believably-hard problem  we obtain a magnification from modest streaming algorithm lower
counterintuitively implies incredibly strong lower bounds (perhaps  bounds all the way to P , NP:
for a different hard problem). Other examples of similar phenomena  Theorem 1.3 (Section 5). If there is some time-constructible
are known, for n 1−ε -approximations to Cliqe [Sri03], low-depth  s(n) ≥ n and an A ∈ PH such that search-MCSPA [s(n)] is not solv-
circuit lower bounds for NC1 [AK10], and sublinear-depth circuit  able by a poly(s(n))-space streaming algorithm with poly(s(n)) update
lower bounds for P [LW12].  time, then P , NP.

1.1  Our Results  (Note that we do not require streaming algorithms to read a
  fresh bit in each step; the algorithm may work for some time be-
To state our theorems, we first need a couple of concepts for “gener-
alized” Boolean circuits. Let A : {0, 1}⋆ → {0, 1}. An A-oracle circuit
  fore requesting the next bit of the stream.) For example, if one
  can show that we cannot compress N -bit strings to SAT-oracle cir-
for a different hard problem). Other examples of similar phenomena  Theorem 1.3 (Section 5). If there is some time-constructible
are known, for n 1−ε -approximations to Cliqe [Sri03], low-depth  s(n) ≥ n and an A ∈ PH such that search-MCSPA [s(n)] is not solv-
circuit lower bounds for NC1 [AK10], and sublinear-depth circuit  able by a poly(s(n))-space streaming algorithm with poly(s(n)) update
lower bounds for P [LW12].  time, then P , NP.

1.1  Our Results  (Note that we do not require streaming algorithms to read a
  fresh bit in each step; the algorithm may work for some time be-
that is nearly identical to that of Theorem 1.1 using instead oracle
  4  STREAMING ALGORITHM FOR MCSP
calls to the following intermediate problem which can (as before)  We now turn to the streaming algorithm for search-MCSP.
be reduced to Σ3 SATA .  Reminder of Theorem 1.2. Let s(n) ≥ n for all n, where s(n) is
  time constructible. Let A : {0, 1}⋆ → {0, 1} be an arbitrary oracle.
STOC ’19, June 23–26, 2019, Phoenix, AZ, USA  Dylan M. McKay, Cody D. Murray, and R. Ryan Williams


There is a (one-pass) streaming algorithm for search-MCSPA [s(n)] on  minimum circuit Ci+1 output by Stream-MergeA has size at most
2n -bit inputs running in 2n · Õ(s(n)) time with Õ(s(n)2 ) update time  s(n). By induction, if T has an A-oracle circuit of size at most s(n),
and Õ(s(n)) space, using an oracle for Σ3 SATA with queries of length  then Algorithm 1 will produce this circuit and report that there is
Õ(s(n)).  such a circuit.
  Here we present an oracle reduction from the MCSP A [s(n)] prob-  On the other hand, if there is no such circuit for T , then there
lem to a problem related to Circuit-Min-MergeA [s(n)].  is some i = 1, . . . , 2n /t such that there is a size-s(n) circuit con-
  Let x 1 , . . . , x 2n be the list of n-bit strings in lexicographical order.  sistent with T on its first (i − 1) · t bits, but there is no size-s(n)
  circuit consistent with T on its first i · t bits. (Such a circuit exists
  trivially for i = 1, but by assumption no such circuit exists for
  Problem: Stream-MergeA [s(n)]
  i = 2n /t.) Let i ′ be the first such index. For all iterations before this
  Given: A t-bit description of an A-oracle circuit C with n in-
  i ′ , Stream-MergeA successfully outputs a circuit of size s(n), but
  puts and one output where t = 100s(n) log s(n), an x i ∈ {0, 1}n ,
  in iteration i ′ Stream-MergeA fails to find such a circuit, and thus
  and a t-bit string y = y1 · · · yt .
  outputs 0100s(n) log s(n) . The algorithm will notice this output is not
  Output: Either the string 1 ⟨C ′ ⟩ where C ′ is the lexigraphi-
  a valid circuit, and report there is no A oracle circuit of size s(n).
  cally first minimum-size A-oracle circuit of size at most s(n)
  It remains to show that Algorithm 1 uses small time and space.
  such that for all strings x < x i we have C ′ (x) = C(x), and for
  In each iteration of the for-loop, we read t more bits of T , query the
```

## Tal, The Bipartite Formula Complexity of Inner-Product is Quadratic, ECCC TR16-181
```

  Abstract
  A bipartite formula on binary variables x1 , . . . , xn and y1 , . . . , yn is a binary tree whose
  internal nodes are marked with AND or OR gates and whose leaves can compute any function
  of either the x or y variables. We
  Pshow  that any bipartite formula for the Inner-Product modulo
  n  e 2 ). The result is tight up
  2 function, namely IPn (x, y) = i=1 xi yi mod 2, must be of size Ω(n
  to logarithmic factors. To the best of our knowledge, this is the first super-linear lower bound
  on the bipartite formula complexity of any explicit function.
  We give two simple proofs that rely on the deep results of Reichardt [Rei11] and Forster
  [For02]. Moreover, the second proof establishes an average-case lower bound for the Inner-
  Product function. Namely, we show that any bipartite formula that agrees with IPn on at least
  1  1  e 2
  2 + nlog n of the inputs must be of size Ω(n ).
  From Forster’s Theorem and Lemma 2.3, we deduce our main theorem.

Theorem 3.2 (Main Theorem). The Bipartite Formula Complexity of IPn is Ω(n2 / log2 n).

Proof. Let F be the smallest bipartite formula computing IPn , and denote its size by s. By Forster’s
```

## CJW20 - Chen, Jin, Williams, Sharp Threshold Results, ECCC TR20-065
```
Theorem 1.6 (Super-Quadratic MCSP Lower Bounds). For every α ∈ (0, 1) and ε > 0, MCSP[nα ] doesn’t
have probabilistic n2+α−ε -size formulas.

```

## KKLMO - Kabanets, Koroth, Lu, Myrisiotis, Oliveira, CCC 2020, arXiv 2002.08533
```
plexity2 , we are given a string x ∈ {0, 1}n and a string 1ℓ . We accept (x, 1ℓ ) if and only if Kt(x) ≤ ℓ.

MCSP. In the Minimum Circuit Size Problem, we are given as input the description of a Boolean
function f : {0, 1}log n → {0, 1} (represented as an n-bit string), and a string 1ℓ . We accept (f, 1ℓ )
if and only the circuit complexity of f is at most ℓ.
be computationally much harder than GIPkn . However, it is more difficult to analyze these problems
compared to GIPkn because the latter is mathematically “structured,” while the former problems do
not seem to be susceptible to typical algebraic, combinatorial, and analytic techniques.
  More interestingly, MCSP and MKtP play an important role in the theory of hardness magnifi-
cation (see [OPS19, CJW19]). In particular, if one could show that MCSP restricted to an input
parameter ℓ ≤ no(1) is not in FORMULA[n1+ε ] ◦ XOR for some ε > 0, then it would follow that NP
cannot be computed by Boolean formulas of size nc , where c ∈ N is arbitrary. Theorem 1 makes
partial progress on this direction by establishing the first lower bounds for these problems in the
FORMULA ◦ G model. (We note that the proof of Theorem 1 Item 3 requires instances where the
parameter ℓ is nΩ(1) .)

  Using the “locality” of this PRG for FORMULA ◦ XOR, we get a lower bound for MCSP against
subquadratic-size formulas of XORs.

Theorem 34. For every integer s > 0, if MCSP on N -bit can be computed by some function in
FORMULA[s] ◦ XOR, then s = Ω̃(N 2 ).

```
