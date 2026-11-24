// Independent re-computation of the closure tables of results/composition/REPORT.md section 4.
// Written from the rule statements (REPORT.txt in this directory) and README sections 1-3; it shares
// no code with results/composition/.
//
//   ./clos NMAX P NEST BLK T [L6]
//     P    1 = Rule P (run filling)
//     NEST 0 none, 1 = README Lemma 8 (one leaf at a clean cut = Rule N with g = 1), 2 = Rule N
//     BLK  0 none, 1 = Rule D (mirror windows), 2 = Rule B (all valid designs)
//     T    0 none, 1 = Rule T (h of the same or smaller size), 2 = no rules: ALL growth placements
//     L6   1 = also allow the cut L = m+1 in Lemma 8 (README Lemma 6: new leaf on label 0)   [default 0]
//   Rule C (complement) is always on.  Start: all staircases of every size.
//   env DUMP=prefix : write the canonical forms of the trees reached at size n to prefix<n>.txt
//
// Labels 0..m, m = n-1.  A placement is P[k] = left foot of the bracket of length k.
// T = 0: explicit sets of placements, worklist closure.
// T = 1: the set of derived placements of one size is kept as the set of all source-to-sink paths of a
//        layered graph: node (k, F) = "time k, set F of free labels", edge (k, F, p) = "bracket k goes to
//        p".  (Justification that this equals the closure under T is in REPORT.txt, section 4.)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_set>
#include <set>
#include <functional>
using namespace std;
typedef uint64_t u64; typedef uint32_t u32; typedef uint16_t u16;
const int MAXN = 16;
int NMAX, optP, optNest, optBlk, optT, optL6 = 0;
const long long NTREES[17] = {0,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320};

static inline u64 enc(const int *P, int m) { u64 x = 0; for (int k = 1; k <= m; k++) x |= (u64)P[k] << (4*(k-1)); return x; }
static inline void dec(u64 x, int *P, int m) { for (int k = 1; k <= m; k++) P[k] = (x >> (4*(k-1))) & 15; }

bool isGrowth(const int *P, int m) {            // the definition
    if (m == 0) return true;
    if (P[m] != 0) return false;
    u32 used = 1u | (1u << m);
    for (int k = m-1; k >= 1; k--) {
        int a = P[k], b = a + k; if (a < 0 || b > m) return false;
        bool ua = used >> a & 1, ub = used >> b & 1; if (ua == ub) return false;
        used |= (1u << a) | (1u << b);
    }
    return true;
}
// ell[v] = length of the bracket that added label v (ell[0] = 99)
void info(const int *P, int m, int *ell) {
    u32 used = 1; ell[0] = 99;
    for (int k = m; k >= 1; k--) { int a = P[k], b = a + k; int nw = (used >> a & 1) ? b : a; ell[nw] = k; used |= 1u << nw; }
}
// ---- canonical form of the tree drawn by a placement (centre-rooted balanced-parenthesis word)
struct Code { u32 bits; int len; };
int adjN[MAXN], adjL[MAXN][MAXN];
Code encTree(int v, int par) {
    Code ch[MAXN]; int c = 0;
    for (int i = 0; i < adjN[v]; i++) if (adjL[v][i] != par) ch[c++] = encTree(adjL[v][i], v);
    sort(ch, ch + c, [](const Code &a, const Code &b) { return ((u64)a.bits << (32 - a.len)) > ((u64)b.bits << (32 - b.len)); });
    Code r; r.bits = 1; r.len = 1;
    for (int i = 0; i < c; i++) { r.bits = (r.bits << ch[i].len) | ch[i].bits; r.len += ch[i].len; }
    r.bits <<= 1; r.len++;
    return r;
}
u32 canon(const int *P, int m) {
    int n = m + 1; int deg[MAXN];
    for (int i = 0; i < n; i++) adjN[i] = 0;
    for (int k = 1; k <= m; k++) { int a = P[k], b = a + k; adjL[a][adjN[a]++] = b; adjL[b][adjN[b]++] = a; }
    if (n == 1) return 2;
    int left = n; vector<int> lv, nl; bool gone[MAXN] = {0};
    for (int i = 0; i < n; i++) { deg[i] = adjN[i]; if (deg[i] == 1) lv.push_back(i); }
    while (left > 2) {
        nl.clear();
        for (int v : lv) { gone[v] = true; left--; for (int i = 0; i < adjN[v]; i++) { int w = adjL[v][i]; if (!gone[w] && --deg[w] == 1) nl.push_back(w); } }
        lv = nl;
    }
    u32 best = 0;
    for (int v : lv) { Code c = encTree(v, -1); if (c.bits > best) best = c.bits; }
    return best;
}
string paren(u32 bits, int n) { string s; for (int i = 2*n - 1; i >= 0; i--) s += (bits >> i & 1) ? '(' : ')'; return s; }

// ---- rule products.  Each calls emit(Q, mQ).
typedef function<void(const int*, int)> Emit;
void complementOf(const int *P, int m, int *Q) { for (int k = 1; k <= m; k++) Q[k] = m - k - P[k]; }

// Lemma 8 / Rule N with g = 1: one new leaf at every clean cut with admissible u.
void ruleL8(const int *P, int m, const Emit &emit) {
    int n = m + 1, ell[MAXN + 1]; info(P, m, ell);
    int Lmax = optL6 ? m + 1 : m;
    for (int L = 1; L <= Lmax; L++) {
        int c = 0, minlen = 99;
        for (int i = 1; i <= m; i++) if (P[i] <= L-1 && P[i] + i >= L) { c++; minlen = min(minlen, i); }
        if (c > 0 && minlen != m - c + 1) continue;          // jumping brackets must be the c longest
        int j = n - c, u = L - j; if (u < 0) continue;
        if (!(u == 0 || ell[u] >= j)) continue;
        int Q[MAXN + 1];
        for (int i = 1; i <= m; i++) { int a = P[i], b = a + i; if (a >= L) a++; if (b >= L) b++; Q[b - a] = a; }
        Q[j] = u; emit(Q, m + 1);
    }
}
// Rule N, general g: U' = brackets of length >= j of a placement h on g+j vertices whose labels 1..j-1 are the last added.
// truncs[j][g] = list of U' as arrays of left feet for lengths j..j+g-1 (in h's labels)
vector<vector<int>> truncs[MAXN + 1][MAXN + 1];
void ruleN(const int *P, int m, int g, const Emit &emit) {
    int n = m + 1, ell[MAXN + 1]; info(P, m, ell);
    for (int L = 1; L <= m; L++) {
        int c = 0, minlen = 99;
        for (int i = 1; i <= m; i++) if (P[i] <= L-1 && P[i] + i >= L) { c++; minlen = min(minlen, i); }
        if (minlen != m - c + 1) continue;
        int j = n - c, u = L - j; if (u < 0) continue;
        if (!(u == 0 || ell[u] >= j)) continue;
        int Q[MAXN + 1];
        for (auto &U : truncs[j][g]) {
            for (int i = 1; i <= m; i++) { int a = P[i], b = a + i; if (a >= L) a += g; if (b >= L) b += g; Q[b - a] = a; }
            for (int i = j; i <= j + g - 1; i++) { int a = U[i - j]; Q[i] = (a == 0) ? u : u + a; }
            emit(Q, m + g);
        }
    }
}
void addTrunc(const int *P, int m) {       // register the truncations of a derived placement (all j)
    int ell[MAXN + 1]; info(P, m, ell);
    for (int j = 1; j <= m; j++) {         // g = m + 1 - j >= 1
        bool ok = true;
        for (int v = 1; v <= j - 1; v++) if (ell[v] > j - 1) ok = false;      // labels 1..j-1 added by the j-1 shortest
        if (!ok) continue;
        vector<int> U; for (int i = j; i <= m; i++) U.push_back(P[i]);
        truncs[j][m + 1 - j].push_back(U);
    }
}
// Rule B: every valid design, every t with (p-1)t+1 <= NMAX.   Rule D: only the window designs.
void ruleB(const int *P, int m, bool windowsOnly, const function<void(const int*, int)> &emit) {
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
        for (int w = 1; w <= p; w++) {
            bool ok = true;
            for (int i = 1; i <= w - 1; i++) { if (2*i <= w - 1) { if (ell[i] < w - 2*i) ok = false; } else if (ell[i] < 2*i - w + 1) ok = false; }
            if (!ok) continue;
            for (int j = 0; j < m; j++) owner[j] = (j < w - 1) ? w - 1 - j : 0;
            build();
        }
        return;
    }
    function<void(int)> rec = [&](int j) {
        if (j == m) { build(); return; }
        for (int v = 0; v < p; v++) {
            int beta = (v <= j) ? j - v : v - j - 1;
            if (bandUsed[beta]) continue;
            if (v != 0 && beta >= ell[v]) continue;
            bandUsed[beta] = true; owner[j] = v; rec(j + 1); bandUsed[beta] = false;
        }
    };
    rec(0);
}
void staircases(int m, const Emit &emit) {
    if (m == 0) return;
    for (u32 bitsS = 0; bitsS < (1u << (m - 1)); bitsS++) {
        int P[MAXN + 1]; P[m] = 0;
        for (int k = m - 1; k >= 1; k--) P[k] = P[k + 1] + (bitsS >> (k - 1) & 1);
        emit(P, m);
    }
}

// =====================================================================  engine 1 (no T)
unordered_set<u64> D1[MAXN + 1]; vector<u64> L1[MAXN + 1];
void engine1() {
    for (int n = 2; n <= NMAX; n++) {
        int m = n - 1; vector<u64> work; unordered_set<u64> donePrefix;
        Emit add = [&](const int *Q, int mq) {
            if (mq != m) { fprintf(stderr, "size mismatch\n"); exit(1); }
            if (!isGrowth(Q, mq)) { fprintf(stderr, "RULE PRODUCED A NON-GROWTH PLACEMENT\n"); exit(1); }
            u64 x = enc(Q, mq); if (D1[n].insert(x).second) { L1[n].push_back(x); work.push_back(x); }
        };
        staircases(m, add);
        int P[MAXN + 1];
        if (optNest == 1) for (u64 x : L1[n - 1]) { dec(x, P, m - 1); ruleL8(P, m - 1, add); }
        if (optNest == 2) for (int nf = 2; nf < n; nf++) for (u64 x : L1[nf]) { dec(x, P, nf - 1); ruleN(P, nf - 1, n - nf, add); }
        if (optBlk) for (int p = 2; p < n; p++) if ((n - 1) % (p - 1) == 0 && (n - 1) / (p - 1) >= 2) {
            int t = (n - 1) / (p - 1);
            for (u64 x : L1[p]) { dec(x, P, p - 1);
                ruleB(P, p - 1, optBlk == 1, [&](const int *Q, int mq) { if (mq == (p - 1) * t) add(Q, mq); }); }
        }
        while (!work.empty()) {
            u64 x = work.back(); work.pop_back(); dec(x, P, m);
            int Q[MAXN + 1]; complementOf(P, m, Q); add(Q, m);
            if (optP) {
                u32 used = 1u | (1u << m);
                for (int k = m - 1; k >= 1; k--) {       // time k: brackets longer than k placed
                    u32 fr = ((1u << (m + 1)) - 1) & ~used; int lo = __builtin_ctz(fr);
                    if (fr == (((1u << k) - 1) << lo) && donePrefix.insert(((x >> (4*k)) << (4*k)) | (u64)k).second) {   // the products depend only on the prefix
                        for (u64 y : L1[k + 1]) for (int pos = 0; pos < 2; pos++) {
                            int G[MAXN + 1]; dec(y, G, k); memcpy(Q, P, sizeof(Q));
                            for (int i = 1; i <= k; i++) Q[i] = G[i] + lo - 1 + pos;
                            add(Q, m);
                        }
                    }
                    used |= (1u << P[k]) | (1u << (P[k] + k));
                }
            }
        }
        if (optT == 3) {            // naive Rule T on explicit sets (cross-check of engine 2): all pairs, all k, to a fixpoint
            bool ch = true;
            while (ch) {
                ch = false; size_t before = L1[n].size();
                vector<u64> snapshot = L1[n];
                for (u64 xf : snapshot) {
                    int Pf[MAXN + 1]; dec(xf, Pf, m);
                    for (int nh = 3; nh <= n; nh++) { int mh = nh - 1;
                        vector<u64> hs = (nh == n) ? snapshot : L1[nh];
                        for (u64 xh : hs) {
                            int Ph[MAXN + 1]; dec(xh, Ph, mh);
                            u32 uf = 1u | (1u << m), uh = 1u | (1u << mh);
                            for (int k = min(m, mh) ; k >= 1; k--) {       // time k: brackets longer than k placed
                                if (k < m && k < mh) {
                                    u32 Ff = ((1u << (m + 1)) - 1) & ~uf, Fh = ((1u << (mh + 1)) - 1) & ~uh;
                                    int s = __builtin_ctz(Ff) - __builtin_ctz(Fh);
                                    if ((s >= 0 ? Fh << s : Fh >> (-s)) == Ff && __builtin_popcount(Ff) == k) {
                                        // hypothesis 2: every used foot of a moved bracket lands on a used label of f
                                        bool ok = true; u32 uu = uh; int Q[MAXN + 1]; memcpy(Q, Pf, sizeof(Q));
                                        for (int i = k; i >= 1 && ok; i--) { int a = Ph[i], b = a + i; int old = (uu >> a & 1) ? a : b;
                                            if (!(Fh >> old & 1)) { int o = old + s; if (o < 0 || o > m || !(uf >> o & 1)) ok = false; }
                                            uu |= (1u << a) | (1u << b); Q[i] = a + s; }
                                        if (ok) add(Q, m);
                                    }
                                }
                                if (k <= m - 1 || k == m) { if (k <= m) uf |= (1u << Pf[k]) | (1u << (Pf[k] + k)); }
                                if (k <= mh) uh |= (1u << Ph[k]) | (1u << (Ph[k] + k));
                            }
                        }
                    }
                }
                // C (and P) on the new ones
                while (!work.empty()) { u64 x = work.back(); work.pop_back(); dec(x, P, m); int Q[MAXN + 1]; complementOf(P, m, Q); add(Q, m); }
                if (L1[n].size() != before) ch = true;
            }
        }
        if (optNest == 2) for (u64 x : L1[n]) { dec(x, P, m); addTrunc(P, m); }
        set<u32> trees; for (u64 x : L1[n]) { dec(x, P, m); trees.insert(canon(P, m)); }
        printf("n=%2d  derived placements %10zu   trees reached %6zu of %lld%s\n", n, L1[n].size(), trees.size(), NTREES[n], (long long)trees.size() == NTREES[n] ? "  ALL" : "");
        fflush(stdout);
        if (getenv("DUMP")) { string fn = string(getenv("DUMP")) + to_string(n) + ".txt"; FILE *f = fopen(fn.c_str(), "w"); for (u32 t : trees) fprintf(f, "%s\n", paren(t, n).c_str()); fclose(f); }
    }
}

// =====================================================================  engine 2 (with T)
// E[n]: bit (k<<20 | F<<4 | p).  reach[n][k]: bitset over F.
vector<u64> E[MAXN + 1]; vector<u64> R[MAXN + 1];
static inline bool getE(int n, int k, u32 F, int p) { u32 i = (k << 20) | (F << 4) | p; return E[n][i >> 6] >> (i & 63) & 1; }
static inline bool setE(int n, int k, u32 F, int p) { u32 i = (k << 20) | (F << 4) | p; u64 b = 1ull << (i & 63); if (E[n][i >> 6] & b) return false; E[n][i >> 6] |= b; return true; }
static inline bool getR(int n, int k, u32 F) { u32 i = (k << 16) | F; return R[n][i >> 6] >> (i & 63) & 1; }
static inline void setR(int n, int k, u32 F) { u32 i = (k << 16) | F; R[n][i >> 6] |= 1ull << (i & 63); }
bool addPlacement(int n, const int *P) {       // add all edges of a placement
    int m = n - 1; bool ch = false; u32 F = ((1u << m) - 1) & ~1u;       // labels 1..m-1 free at time m-1
    for (int k = m - 1; k >= 1; k--) { ch |= setE(n, k, F, P[k]); F &= ~((1u << P[k]) | (1u << (P[k] + k))); }
    return ch;
}
void computeReach(int n) {
    int m = n - 1; fill(R[n].begin(), R[n].end(), 0);
    if (m >= 2) setR(n, m - 1, ((1u << m) - 1) & ~1u);
    for (int k = m - 1; k >= 1; k--)
        for (u32 F = 0; F < (1u << m); F++) if (getR(n, k, F))
            for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) setR(n, k - 1, F & ~((1u << p) | (1u << (p + k))));
}
// enumerate all source-to-sink paths
template <class CB> void enumPaths(int n, CB cb) {
    int m = n - 1; int P[MAXN + 1]; P[m] = 0;
    if (m == 0) return;
    function<void(int, u32)> rec = [&](int k, u32 F) {
        if (k == 0) { cb(P, m); return; }
        for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) { P[k] = p; rec(k - 1, F & ~((1u << p) | (1u << (p + k)))); }
    };
    rec(m - 1, ((1u << m) - 1) & ~1u);
}
// all completions (suffixes) of derived placements of size ns, shifted into size nt
bool changed;
int bs_ns, bs_nt;
void back(int i, u32 Fprev, int lo, int hi) {
    int ms = bs_ns - 1, mt = bs_nt - 1;
    if (i > ms - 1) return;
    for (int p = 0; p + i <= ms; p++) {
        int a = p, b = p + i;
        if ((Fprev >> a & 1) || (Fprev >> b & 1)) continue;
        for (int c = 0; c < 2; c++) {
            u32 Fi = Fprev | (1u << (c ? b : a));
            if (!getE(bs_ns, i, Fi, p) || !getR(bs_ns, i, Fi)) continue;
            int nlo = max(lo, -p), nhi = min(hi, mt - i - p);
            for (int s = nlo; s <= nhi; s++) {
                if (bs_ns == bs_nt && s == 0) continue;
                u32 Fs = s >= 0 ? Fi << s : Fi >> (-s);
                if (Fs & 1u || Fs >> mt & 1u) continue;        // labels 0 and m of the target are never free
                if (setE(bs_nt, i, Fs, p + s)) changed = true;
            }
            if (bs_ns == bs_nt && nlo == 0 && nhi == 0) continue;
            back(i + 1, Fi, nlo, nhi);
        }
    }
}
void engine2() {
    for (int n = 1; n <= NMAX; n++) { E[n].assign(1u << 18, 0); R[n].assign(1u << 14, 0); }
    for (int n = 2; n <= NMAX; n++) {
        int m = n - 1;
        if (optT == 2) {             // everything: all valid edges
            for (int k = 1; k <= m - 1; k++) for (u32 F = 0; F < (1u << m); F += 2) if (__builtin_popcount(F) == k)
                for (int p = 0; p + k <= m; p++) if ((F >> p & 1) != (F >> (p + k) & 1)) setE(n, k, F, p);
        } else {
            staircases(m, [&](const int *Q, int mq) { addPlacement(n, Q); });
            // completions from smaller sizes (Rule T with a smaller h); these do not change during the rounds
            for (int ns = 3; ns < n; ns++) { bs_ns = ns; bs_nt = n; back(1, 0, -99, 99); }
            int rounds = 0;
            do {
                changed = false; rounds++;
                computeReach(n);
                bs_ns = bs_nt = n; back(1, 0, -99, 99);
                // Rule C on edges
                for (int k = 1; k <= m - 1; k++) for (u32 F = 0; F < (1u << m); F += 2) for (int p = 0; p + k <= m; p++) if (getE(n, k, F, p)) {
                    u32 Fr = 0; for (int x = 1; x < m; x++) if (F >> x & 1) Fr |= 1u << (m - x);
                    if (setE(n, k, Fr, m - k - p)) changed = true;
                }
                if (optP) {
                    for (int k = 1; k <= m - 1; k++) for (int x = 1; x + k - 1 <= m - 1; x++) {
                        u32 F = ((1u << k) - 1) << x; if (!getR(n, k, F)) continue;
                        for (int pos = 0; pos < 2; pos++) { int base = x - 1 + pos;
                            if (setE(n, k, F, base)) changed = true;        // top bracket of g
                            enumPaths(k + 1, [&](const int *G, int mg) { int Q[MAXN + 1]; u32 FF = ((1u << mg) - 1) & ~1u;
                                for (int i = mg - 1; i >= 1; i--) { if (setE(n, i, FF << base, G[i] + base)) changed = true; FF &= ~((1u << G[i]) | (1u << (G[i] + i))); } (void)Q; });
                        }
                    }
                }
            } while (changed);
            fprintf(stderr, "  n=%d: %d rounds\n", n, rounds);
        }
        computeReach(n);
        // finalise: count, verify, trees, and push products to larger sizes
        long long cnt = 0; unordered_set<u32> trees;
        enumPaths(n, [&](const int *P, int mm) {
            cnt++;
            if (!isGrowth(P, mm)) { fprintf(stderr, "NON-GROWTH PLACEMENT DERIVED\n"); exit(1); }
            trees.insert(canon(P, mm));
            if (optT == 2) return;
            if (optNest >= 1 && n + 1 <= NMAX) ruleL8(P, mm, [&](const int *Q, int mq) { if (!isGrowth(Q, mq)) { fprintf(stderr, "L8 BAD\n"); exit(1); } addPlacement(mq + 1, Q); });
            if (optBlk) ruleB(P, mm, optBlk == 1, [&](const int *Q, int mq) { if (!isGrowth(Q, mq)) { fprintf(stderr, "B BAD\n"); exit(1); } addPlacement(mq + 1, Q); });
        });
        printf("n=%2d  derived placements %10lld   trees reached %6zu of %lld%s\n", n, cnt, trees.size(), NTREES[n], (long long)trees.size() == NTREES[n] ? "  ALL" : "");
        fflush(stdout);
        if (getenv("DUMP")) { string fn = string(getenv("DUMP")) + to_string(n) + ".txt"; FILE *f = fopen(fn.c_str(), "w"); vector<u32> v(trees.begin(), trees.end()); sort(v.begin(), v.end()); for (u32 t : v) fprintf(f, "%s\n", paren(t, n).c_str()); fclose(f); }
    }
}
int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: clos NMAX P NEST BLK T [L6]\n"); return 1; }
    NMAX = atoi(argv[1]); optP = atoi(argv[2]); optNest = atoi(argv[3]); optBlk = atoi(argv[4]); optT = atoi(argv[5]);
    if (argc > 6) optL6 = atoi(argv[6]);
    if (NMAX > MAXN) return 1;
    if (optT == 0 || optT == 3) engine1(); else engine2();
}
