// Closure of the staircases under Rules C, T and B (optionally + README Lemma 8), up to n = 20.
// Same method as engine 2 of clos.cpp (derived placements of one size = all source-to-sink paths of
// the "tape graph"; see REPORT.txt section 4), with wider bit fields, a memo in the suffix walk, path
// counting by dynamic programming and an early stop once every tree shape has been seen.
//   ./clos2 NMAX NEST BLK      NEST: 1 = Lemma 8 (needs full enumeration, slow above 16)   BLK: 0/1/2 as in clos.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_set>
#include <functional>
using namespace std;
typedef uint64_t u64; typedef uint32_t u32;
const int MAXN = 20;
int NMAX, optNest, optBlk;
const long long NTREES[21] = {0,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320,48629,123867,317955,823065};
bool isGrowth(const int *P, int m) {
    if (m == 0) return true;
    if (P[m] != 0) return false;
    u32 used = 1u | (1u << m);
    for (int k = m-1; k >= 1; k--) { int a = P[k], b = a + k; if (a < 0 || b > m) return false;
        bool ua = used >> a & 1, ub = used >> b & 1; if (ua == ub) return false; used |= (1u << a) | (1u << b); }
    return true;
}
void info(const int *P, int m, int *ell) { u32 used = 1; ell[0] = 99;
    for (int k = m; k >= 1; k--) { int a = P[k], b = a + k; int nw = (used >> a & 1) ? b : a; ell[nw] = k; used |= 1u << nw; } }
struct Code { u64 bits; int len; };
int adjN[MAXN], adjL[MAXN][MAXN];
Code encTree(int v, int par) {
    Code ch[MAXN]; int c = 0;
    for (int i = 0; i < adjN[v]; i++) if (adjL[v][i] != par) ch[c++] = encTree(adjL[v][i], v);
    sort(ch, ch + c, [](const Code &a, const Code &b) { return (a.bits << (48 - a.len)) > (b.bits << (48 - b.len)); });
    Code r; r.bits = 1; r.len = 1;
    for (int i = 0; i < c; i++) { r.bits = (r.bits << ch[i].len) | ch[i].bits; r.len += ch[i].len; }
    r.bits <<= 1; r.len++; return r;
}
u64 canon(const int *P, int m) {
    int n = m + 1; int deg[MAXN];
    for (int i = 0; i < n; i++) adjN[i] = 0;
    for (int k = 1; k <= m; k++) { int a = P[k], b = a + k; adjL[a][adjN[a]++] = b; adjL[b][adjN[b]++] = a; }
    if (n == 1) return 2;
    int left = n; int lv[MAXN], nl[MAXN], nlv = 0, nnl; bool gone[MAXN] = {0};
    for (int i = 0; i < n; i++) { deg[i] = adjN[i]; if (deg[i] == 1) lv[nlv++] = i; }
    while (left > 2) { nnl = 0;
        for (int q = 0; q < nlv; q++) { int v = lv[q]; gone[v] = true; left--; for (int i = 0; i < adjN[v]; i++) { int w = adjL[v][i]; if (!gone[w] && --deg[w] == 1) nl[nnl++] = w; } }
        memcpy(lv, nl, sizeof(int) * nnl); nlv = nnl; }
    u64 best = 0;
    for (int q = 0; q < nlv; q++) { Code c = encTree(lv[q], -1); if (c.bits > best) best = c.bits; }
    return best;
}
typedef function<void(const int*, int)> Emit;
void ruleL8(const int *P, int m, const Emit &emit) {
    int n = m + 1, ell[MAXN + 1]; info(P, m, ell);
    for (int L = 1; L <= m; L++) {
        int c = 0, minlen = 99;
        for (int i = 1; i <= m; i++) if (P[i] <= L-1 && P[i] + i >= L) { c++; minlen = min(minlen, i); }
        if (minlen != m - c + 1) continue;
        int j = n - c, u = L - j; if (u < 0) continue;
        if (!(u == 0 || ell[u] >= j)) continue;
        int Q[MAXN + 1];
        for (int i = 1; i <= m; i++) { int a = P[i], b = a + i; if (a >= L) a++; if (b >= L) b++; Q[b - a] = a; }
        Q[j] = u; emit(Q, m + 1);
    }
}
void ruleB(const int *P, int m, bool windowsOnly, const Emit &emit) {
    int p = m + 1, ell[MAXN + 1]; info(P, m, ell);
    if ((p - 1) * 2 + 1 > NMAX) return;
    int owner[MAXN]; bool bandUsed[MAXN] = {0};
    auto build = [&]() {
        for (int t = 2; (p - 1) * t + 1 <= NMAX; t++) {
            int Q[MAXN + 1]; int M = (p - 1) * t;
            for (int i = 1; i <= m; i++) Q[t * i] = t * P[i];
            for (int j = 0; j < m; j++) for (int d = 1; d < t; d++) { int a = t * owner[j], b = j * t + d; if (a > b) swap(a, b); Q[b - a] = a; }
            emit(Q, M);
        }
    };
    if (windowsOnly) {
        for (int w = 1; w <= p; w++) { bool ok = true;
            for (int i = 1; i <= w - 1; i++) { if (2*i <= w - 1) { if (ell[i] < w - 2*i) ok = false; } else if (ell[i] < 2*i - w + 1) ok = false; }
            if (!ok) continue;
            for (int j = 0; j < m; j++) owner[j] = (j < w - 1) ? w - 1 - j : 0;
            build(); }
        return;
    }
    function<void(int)> rec = [&](int j) {
        if (j == m) { build(); return; }
        for (int v = 0; v < p; v++) { int beta = (v <= j) ? j - v : v - j - 1;
            if (bandUsed[beta]) continue; if (v != 0 && beta >= ell[v]) continue;
            bandUsed[beta] = true; owner[j] = v; rec(j + 1); bandUsed[beta] = false; }
    };
    rec(0);
}
// E[n]: bit ((k*32+p) << 18 | F>>1).   F = set of free labels (subset of 1..m-1).
vector<u64> E[MAXN + 1]; vector<u64> R[MAXN + 1]; vector<vector<u32>> RL[MAXN + 1];
static inline u64 eidx(int k, u32 F, int p) { return ((u64)(k * 32 + p) << 18) | (F >> 1); }
static inline bool getE(int n, int k, u32 F, int p) { u64 i = eidx(k, F, p); return E[n][i >> 6] >> (i & 63) & 1; }
static inline bool setE(int n, int k, u32 F, int p) { u64 i = eidx(k, F, p); u64 b = 1ull << (i & 63); if (E[n][i >> 6] & b) return false; E[n][i >> 6] |= b; return true; }
static inline bool getR(int n, int k, u32 F) { u32 i = (k << 18) | (F >> 1); return R[n][i >> 6] >> (i & 63) & 1; }
static inline bool setR(int n, int k, u32 F) { u32 i = (k << 18) | (F >> 1); u64 b = 1ull << (i & 63); if (R[n][i >> 6] & b) return false; R[n][i >> 6] |= b; return true; }
void addPlacement(int n, const int *P) { int m = n - 1; u32 F = ((1u << m) - 1) & ~1u;
    for (int k = m - 1; k >= 1; k--) { setE(n, k, F, P[k]); F &= ~((1u << P[k]) | (1u << (P[k] + k))); } }
void computeReach(int n) {
    int m = n - 1; fill(R[n].begin(), R[n].end(), 0); RL[n].assign(m + 1, vector<u32>());
    if (m < 2) return;
    u32 F0 = ((1u << m) - 1) & ~1u; setR(n, m - 1, F0); RL[n][m - 1].push_back(F0);
    for (int k = m - 1; k >= 1; k--) for (u32 F : RL[n][k])
        for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) { u32 G = F & ~((1u << p) | (1u << (p + k))); if (setR(n, k - 1, G)) RL[n][k - 1].push_back(G); }
}
bool changed; int bs_ns, bs_nt; unordered_set<u64> memo;
void back(int i, u32 Fprev, int lo, int hi) {
    int ms = bs_ns - 1, mt = bs_nt - 1;
    if (i > ms - 1) return;
    u64 key = ((u64)i << 40) | ((u64)(lo + 32) << 32) | ((u64)hi << 24) | (Fprev >> 1);
    if (i > 1 && !memo.insert(key).second) return;
    for (int p = 0; p + i <= ms; p++) {
        int a = p, b = p + i;
        if ((Fprev >> a & 1) || (Fprev >> b & 1)) continue;
        for (int c = 0; c < 2; c++) {
            u32 Fi = Fprev | (1u << (c ? b : a));
            if ((Fi & 1u) || (Fi >> ms & 1u)) continue;
            if (!getE(bs_ns, i, Fi, p) || !getR(bs_ns, i, Fi)) continue;
            int nlo = max(lo, -p), nhi = min(hi, mt - i - p);
            for (int s = nlo; s <= nhi; s++) {
                if (bs_ns == bs_nt && s == 0) continue;
                u32 Fs = s >= 0 ? Fi << s : Fi >> (-s);
                if (Fs & 1u || Fs >> mt & 1u) continue;
                if (setE(bs_nt, i, Fs, p + s)) changed = true;
            }
            if (bs_ns == bs_nt && nlo == 0 && nhi == 0) continue;
            back(i + 1, Fi, nlo, nhi);
        }
    }
}
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: clos2 NMAX NEST BLK\n"); return 1; }
    NMAX = atoi(argv[1]); optNest = atoi(argv[2]); optBlk = atoi(argv[3]);
    if (NMAX > MAXN) return 1;
    for (int n = 1; n <= NMAX; n++) { E[n].assign(((u64)1 << 28) / 64, 0); R[n].assign((1u << 23) / 64, 0); }
    for (int n = 2; n <= NMAX; n++) {
        int m = n - 1;
        for (u32 bitsS = 0; m >= 1 && bitsS < (1u << (m - 1)); bitsS++) { int P[MAXN + 1]; P[m] = 0;
            for (int k = m - 1; k >= 1; k--) P[k] = P[k + 1] + (bitsS >> (k - 1) & 1);
            addPlacement(n, P); }
        for (int ns = 3; ns < n; ns++) { bs_ns = ns; bs_nt = n; memo.clear(); back(1, 0, -30, 30); }
        int rounds = 0;
        do { changed = false; rounds++;
            computeReach(n);
            bs_ns = bs_nt = n; memo.clear(); back(1, 0, -30, 30);
            for (int k = 1; k <= m - 1; k++) for (u32 F = 0; F < (1u << m); F += 2) { if (__builtin_popcount(F) != k) continue;
                u32 Fr = 0; bool have = false;
                for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) {
                    if (!have) { for (int x = 1; x < m; x++) if (F >> x & 1) Fr |= 1u << (m - x); have = true; }
                    if (setE(n, k, Fr, m - k - p)) changed = true; } }
        } while (changed);
        computeReach(n);
        // number of derived placements = number of source-to-sink paths (dynamic programming)
        vector<u64> cur(1u << 18, 0), nxt(1u << 18, 0); u64 total = 0;
        if (m >= 2) { cur[(((1u << m) - 1) & ~1u) >> 1] = 1;
            for (int k = m - 1; k >= 1; k--) { for (u32 F : RL[n][k - 1]) nxt[F >> 1] = 0;
                for (u32 F : RL[n][k]) { u64 c = cur[F >> 1]; for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) nxt[(F & ~((1u << p) | (1u << (p + k)))) >> 1] += c; }
                for (u32 F : RL[n][k]) cur[F >> 1] = 0; swap(cur, nxt); }
            total = cur[0]; } else total = 1;
        // enumerate paths: verify each against the definition, collect tree shapes; stop early when all shapes are seen,
        // unless the full list is needed to feed Rule B or Lemma 8 at a larger size
        bool needAll = (optBlk && 2 * m + 1 <= NMAX) || (optNest && n < NMAX);
        unordered_set<u64> trees; u64 seen = 0; bool stop = false; int P[MAXN + 1]; P[m] = 0;
        function<void(int, u32)> rec = [&](int k, u32 F) {
            if (stop) return;
            if (k == 0) { seen++;
                if (!isGrowth(P, m)) { fprintf(stderr, "NON-GROWTH PLACEMENT DERIVED\n"); exit(1); }
                trees.insert(canon(P, m));
                if (optNest && n < NMAX) ruleL8(P, m, [&](const int *Q, int mq) { if (!isGrowth(Q, mq)) exit(2); addPlacement(mq + 1, Q); });
                if (optBlk) ruleB(P, m, optBlk == 1, [&](const int *Q, int mq) { if (!isGrowth(Q, mq)) exit(2); addPlacement(mq + 1, Q); });
                if (!needAll && (long long)trees.size() == NTREES[n]) stop = true;
                return; }
            for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) { P[k] = p; rec(k - 1, F & ~((1u << p) | (1u << (p + k)))); }
        };
        if (m >= 2) rec(m - 1, ((1u << m) - 1) & ~1u); else { P[1] = 0; rec(0, 0); }
        printf("n=%2d  derived placements %12llu  (%d rounds)  trees reached %7zu of %lld%s   [placements enumerated and re-tested: %llu]\n", n, (unsigned long long)total, rounds,
               trees.size(), NTREES[n], (long long)trees.size() == NTREES[n] ? "  ALL" : "", (unsigned long long)seen);
        fflush(stdout);
    }
}
