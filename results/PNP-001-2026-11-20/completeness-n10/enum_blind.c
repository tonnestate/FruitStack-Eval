/* Independent second enumeration of minimal GF(3)-blind cores on n variables (director, 2026-11-20).
 * Shares NO code with the Python enumerator (cores_deg.py). Same mathematical premises:
 *  - every minimal blind core has a GF(3) solution using all three values (D-018, Lean-verified);
 *  - translation x -> x + c*1 and variable permutation normalise it to 0^k0 1^k1 2^k2, (k0,k1,k2) minimal under rotation;
 *  - then every clause has value sum 1 mod 3 (ALLOWED), and a minimal core has <= n-1 clauses (T44 C3/C4, proved).
 * Per type: number of minimal UNSAT subsets of ALLOWED with <= n-1 clauses, and those WITHOUT a degree-2 Nullstellensatz
 * refutation in the XOR/carry encoding over GF(2) (no Boolean axioms): 1 not in span{q_i, L_j, x_k L_j}.
 * Usage: enum_blind n k0 k1 k2 failfile   (n <= 10) */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#define W 16                                   /* 1024 assignments = 16 x 64 bits */
typedef unsigned __int128 u128;
static int n, A, cl[200][3], chosen[16];
static uint64_t mask[200][W];
static unsigned long long cores = 0, fails = 0;
static FILE *ff;
static int monidx[10][10];
static u128 bit(int i) { return ((u128)1) << i; }
static u128 lin1(int a) { return bit(1 + a); }
static u128 quad(int a, int b) { if (a > b) { int t = a; a = b; b = t; } return bit(monidx[a][b]); }
static int ns2(int m, const int *ix) {
    u128 basis[128]; memset(basis, 0, sizeof basis);   /* basis[h] has highest bit h */
    u128 gen[16 * 13]; int g = 0;
    for (int t = 0; t < m; ++t) {
        int a = cl[ix[t]][0], b = cl[ix[t]][1], c = cl[ix[t]][2];
        gen[g++] = quad(a,b) ^ quad(a,c) ^ quad(b,c);                         /* q */
        gen[g++] = bit(0) ^ lin1(a) ^ lin1(b) ^ lin1(c);                      /* L */
        for (int k = 0; k < n; ++k) gen[g++] = lin1(k) ^ quad(k,a) ^ quad(k,b) ^ quad(k,c);   /* x_k L */
    }
    for (int t = 0; t < g; ++t) {
        u128 v = gen[t];
        while (v) {
            int h = 127; while (!((v >> h) & 1)) --h;
            if (!basis[h]) { basis[h] = v; break; }
            v ^= basis[h];
        }
    }
    u128 v = bit(0);
    while (v) {
        int h = 127; while (!((v >> h) & 1)) --h;
        if (!basis[h]) return 0;
        v ^= basis[h];
    }
    return 1;
}
static int nonzero(const uint64_t *s) { for (int w = 0; w < W; ++w) if (s[w]) return 1; return 0; }
static void dfs(int start, int depth, const uint64_t *sol) {
    uint64_t nw[W];
    for (int j = start; j < A; ++j) {
        int z = 1;
        for (int w = 0; w < W; ++w) { nw[w] = sol[w] & mask[j][w]; if (nw[w]) z = 0; }
        if (z) {
            chosen[depth] = j; int k = depth + 1, minimal = 1;
            for (int drop = 0; drop < k && minimal; ++drop) {          /* every proper subset (one clause removed) must be SAT */
                uint64_t s[W]; for (int w = 0; w < W; ++w) s[w] = ~0ULL;
                for (int t = 0; t < k; ++t) if (t != drop) for (int w = 0; w < W; ++w) s[w] &= mask[chosen[t]][w];
                if (!nonzero(s)) minimal = 0;
            }
            if (minimal) {
                ++cores;
                if (!ns2(k, chosen)) {
                    ++fails;
                    int idx[16]; memcpy(idx, chosen, sizeof(int) * k);
                    for (int t = 0; t < k; ++t) fprintf(ff, "%d%d%d%c", cl[idx[t]][0], cl[idx[t]][1], cl[idx[t]][2], t + 1 < k ? ' ' : '\n');
                }
            }
        } else if (depth + 2 < n) {                                     /* size depth+1 < n-1: may still grow */
            chosen[depth] = j;
            dfs(j + 1, depth + 1, nw);
        }
    }
}
int main(int argc, char **argv) {
    if (argc != 6) return 2;
    n = atoi(argv[1]); int k[3] = {atoi(argv[2]), atoi(argv[3]), atoi(argv[4])};
    int val[10], p = 0;
    for (int c = 0; c < 3; ++c) for (int i = 0; i < k[c]; ++i) val[p++] = c;
    int mi = 1 + n;
    for (int i = 0; i < n; ++i) for (int j = i; j < n; ++j) monidx[i][j] = mi++;
    if (mi > 128) return 3;
    A = 0;
    for (int a = 0; a < n; ++a) for (int b = a + 1; b < n; ++b) for (int c = b + 1; c < n; ++c)
        if ((val[a] + val[b] + val[c]) % 3 == 1) { cl[A][0] = a; cl[A][1] = b; cl[A][2] = c; ++A; }
    for (int j = 0; j < A; ++j) {
        memset(mask[j], 0, sizeof mask[j]);
        for (int x = 0; x < (1 << n); ++x)
            if (((x >> cl[j][0]) & 1) + ((x >> cl[j][1]) & 1) + ((x >> cl[j][2]) & 1) == 1) mask[j][x >> 6] |= 1ULL << (x & 63);
    }
    uint64_t full[W]; for (int w = 0; w < W; ++w) full[w] = (1 << n) >= 64 * (w + 1) ? ~0ULL : (w * 64 < (1 << n) ? ((1ULL << ((1 << n) - w * 64)) - 1) : 0);
    ff = fopen(argv[5], "w");
    dfs(0, 0, full);
    fclose(ff);
    printf("n=%d type (%d,%d,%d): allowed %d, minimal cores %llu, NS2 failures %llu\n", n, k[0], k[1], k[2], A, cores, fails);
    return 0;
}
