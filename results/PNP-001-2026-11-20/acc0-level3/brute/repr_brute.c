/* PNP-001 ACC0 level 3 brute force (director 2026-11-20).
   For t = n + k <= 7: enumerate every affine subspace V of GF(3)^t exactly once (reduced row echelon form [M | b]),
   compute Sol = V cap {0,1}^t (128-bit mask), project onto the first n coordinates (inputs; last k = Boolean existential aux).
   For each function f on n inputs (n = 3, 4) and k = t - n record: min dim V over representations of f, and the same among
   representations with unique witnesses (every accepted x has exactly one y).  Output: lines "t n k fmask bestdim bestdim_unique". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int T, NP;                     /* NP = 2^T Boolean points; point index bit j = coordinate j */
static u128 rowmask[2187][3];         /* points z with a.z = c (mod 3), a indexed base 3 */
static int pivots[8], R;
static int8_t best[2][65536], bestu[2][65536];   /* [n-3][fmask] */
static long long leaves;
static void project(u128 sol, int dim) {
  for (int nn = 3; nn <= 4 && nn <= T; nn++) {
    int k = T - nn, w = 1 << nn; uint64_t f = 0; int tot = 0;
    for (int y = 0; y < (1 << k); y++) {
      uint64_t part = (uint64_t)((sol >> (y * w)) & (((u128)1 << w) - 1));
      f |= part; tot += __builtin_popcountll(part);
    }
    int uniq = (tot == __builtin_popcountll(f));
    int8_t *b = &best[nn - 3][f], *bu = &bestu[nn - 3][f];
    if (*b < 0 || dim < *b) *b = dim;
    if (uniq && (*bu < 0 || dim < *bu)) *bu = dim;
  }
}
/* rows are generated top-down: row i has pivot pivots[i] (coefficient 1), zeros in other pivot columns and left of its pivot,
   free GF(3) entries in non-pivot columns right of the pivot, free right-hand side */
static void rec(int i, u128 sol) {
  if (i == R) { leaves++; project(sol, T - R); return; }
  int p = pivots[i], freec[8], nf = 0;
  for (int j = p + 1; j < T; j++) { int isp = 0; for (int q = 0; q < R; q++) if (pivots[q] == j) isp = 1; if (!isp) freec[nf++] = j; }
  int combos = 1; for (int q = 0; q < nf; q++) combos *= 3;
  for (int c = 0; c < combos; c++) {
    int a = 1, pw[8]; pw[0] = 1; for (int j = 1; j < T; j++) pw[j] = pw[j - 1] * 3;
    a = pw[p]; int cc = c;
    for (int q = 0; q < nf; q++) { a += (cc % 3) * pw[freec[q]]; cc /= 3; }
    for (int rhs = 0; rhs < 3; rhs++) rec(i + 1, sol & rowmask[a][rhs]);
  }
}
int main(int argc, char **argv) {
  T = atoi(argv[1]); NP = 1 << T;
  int na = 1; for (int j = 0; j < T; j++) na *= 3;
  for (int a = 0; a < na; a++) for (int z = 0; z < NP; z++) {
    int v = 0, aa = a; for (int j = 0; j < T; j++) { v += (aa % 3) * ((z >> j) & 1); aa /= 3; }
    rowmask[a][v % 3] |= (u128)1 << z;
  }
  memset(best, -1, sizeof best); memset(bestu, -1, sizeof bestu);
  u128 all = (NP == 128) ? ~(u128)0 : (((u128)1 << NP) - 1);
  for (int mask = 0; mask < (1 << T); mask++) {          /* pivot set */
    R = 0; for (int j = 0; j < T; j++) if (mask >> j & 1) pivots[R++] = j;
    rec(0, all);
  }
  fprintf(stderr, "t=%d affine subspaces enumerated: %lld\n", T, leaves);
  for (int nn = 3; nn <= 4 && nn <= T; nn++)
    for (int f = 0; f < (1 << (1 << nn)); f++)
      if (best[nn - 3][f] >= 0) printf("%d %d %d %d %d %d\n", T, nn, T - nn, f, best[nn - 3][f], bestu[nn - 3][f]);
  return 0;
}
