// Referee brute force for claim 1: classes C(K), K=1,2,3, backward for n<=NB (every growth
// placement, every label set of size <=3), then forward closure of C(2) for n<=NF.
// Also class V = "delete <=2 labels, any growth placement result" (no order requirement).
// usage: ./ck NB NF        compile: g++ -O2 -fopenmp
#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
typedef unsigned long long u64;
typedef unsigned int u32;

// ---------- placements ----------
bool isGrowth(const int* q, int m) {
    u32 used = 0;
    for (int k = m - 1; k >= 1; k--) {
        int a = q[k], b = q[k] + k;
        if (a < 1 || b > m) return false;
        bool ua = used >> (a - 1) & 1, ub = used >> (b - 1) & 1;
        if (k == m - 1) { if (ua || ub) return false; }
        else if (ua == ub) return false;
        used |= 1u << (a - 1) | 1u << (b - 1);
    }
    return true;
}
u64 key(const int* q, int m) {
    u64 x = 0;
    for (int k = 1; k <= m - 1; k++) x = x * (u64)(m - k) + (u64)(q[k] - 1);
    return x;
}
void unkey(u64 x, int m, int* q) {
    for (int k = m - 1; k >= 1; k--) { q[k] = (int)(x % (u64)(m - k)) + 1; x /= (u64)(m - k); }
}
bool cond1(const int* p, int m, u32 R) {
    int c = 0;
    for (int k = 1; k < m; k++) if ((R >> (p[k] - 1) & 1) || (R >> (p[k] + k - 1) & 1)) c++;
    return c == __builtin_popcount(R);
}
bool cond2(const int* p, int m, u32 R) {
    int shorter = 0;
    for (int k = 1; k < m; k++) {
        int a = p[k], b = p[k] + k;
        if ((R >> (a - 1) & 1) || (R >> (b - 1) & 1)) { shorter++; continue; }
        u32 between = ((1u << (b - 1)) - 1) & ~((1u << a) - 1);   // labels a+1..b-1
        if (__builtin_popcount(R & between) != shorter) return false;
    }
    return true;
}
// delete R; returns true if result is a placement (lengths 1..m'-1 once each); q filled
bool restrictTo(const int* p, int m, u32 R, int* q, int& mm) {
    int rank[41]; int c = 0;
    for (int x = 1; x <= m; x++) { if (!(R >> (x - 1) & 1)) c++; rank[x] = c; }
    mm = c;
    u32 seen = 0; int cnt = 0;
    for (int k = 1; k < m; k++) {
        int a = p[k], b = p[k] + k;
        if ((R >> (a - 1) & 1) || (R >> (b - 1) & 1)) continue;
        int nl = rank[b] - rank[a];
        cnt++;
        if (nl < 1 || nl > c - 1 || (seen >> nl & 1)) return false;
        seen |= 1u << nl; q[nl] = rank[a];
    }
    return cnt == c - 1;
}

// ---------- trees ----------
struct Enc { u64 b; int len; };
static thread_local int T_adj[20][20], T_deg[20];
Enc encRec(int v, int par) {
    Enc ch[20]; int nc = 0;
    for (int i = 0; i < T_deg[v]; i++) { int w = T_adj[v][i]; if (w != par) ch[nc++] = encRec(w, v); }
    for (int i = 1; i < nc; i++) { Enc t = ch[i]; int j = i; while (j > 0 && (ch[j - 1].len < t.len || (ch[j - 1].len == t.len && ch[j - 1].b < t.b))) { ch[j] = ch[j - 1]; j--; } ch[j] = t; }
    Enc r; r.b = 1; r.len = 2;
    for (int i = 0; i < nc; i++) { r.b = r.b << ch[i].len | ch[i].b; r.len += ch[i].len; }
    r.b <<= 1;
    return r;
}
u64 canon(int n, const int* ea, const int* eb) {  // vertices 0..n-1, n-1 edges
    for (int i = 0; i < n; i++) T_deg[i] = 0;
    for (int i = 0; i < n - 1; i++) { T_adj[ea[i]][T_deg[ea[i]]++] = eb[i]; T_adj[eb[i]][T_deg[eb[i]]++] = ea[i]; }
    int d[20], layer[20], nl = 0, rem = n; bool gone[20];
    for (int i = 0; i < n; i++) { d[i] = T_deg[i]; gone[i] = false; }
    for (int i = 0; i < n; i++) if (d[i] <= 1) layer[nl++] = i;
    while (rem > 2) {
        int nx[20], nn = 0;
        for (int i = 0; i < nl; i++) { int v = layer[i]; gone[v] = true; rem--; for (int j = 0; j < T_deg[v]; j++) { int w = T_adj[v][j]; if (!gone[w] && --d[w] == 1) nx[nn++] = w; } }
        nl = nn; for (int i = 0; i < nn; i++) layer[i] = nx[i];
    }
    if (nl == 1) return encRec(layer[0], -1).b;
    Enc a = encRec(layer[0], layer[1]), b = encRec(layer[1], layer[0]);
    if (a.len < b.len || (a.len == b.len && a.b < b.b)) swap(a, b);
    u64 r = 1; r = r << a.len | a.b; r = r << b.len | b.b; r <<= 1;
    return r | (1ull << 62);   // mark bicentral
}
u64 canonPl(const int* p, int m) {
    int ea[40], eb[40];
    for (int k = 1; k < m; k++) { ea[k - 1] = p[k] - 1; eb[k - 1] = p[k] + k - 1; }
    return canon(m, ea, eb);
}
map<u64, vector<pair<int,int>>> treesOf[20];
void genTrees(int N) {
    treesOf[2][canon(2, (const int[]){0}, (const int[]){1})] = {{0, 1}};
    for (int n = 3; n <= N; n++)
        for (auto& kv : treesOf[n - 1]) for (int v = 0; v < n - 1; v++) {
            int ea[20], eb[20]; int i = 0;
            for (auto& e : kv.second) { ea[i] = e.first; eb[i] = e.second; i++; }
            ea[i] = v; eb[i] = n - 1;
            u64 c = canon(n, ea, eb);
            if (!treesOf[n].count(c)) { auto e = kv.second; e.push_back({v, n - 1}); treesOf[n][c] = e; }
        }
}
void printMissing(int n, const set<u64>& got, const char* name) {
    for (auto& kv : treesOf[n]) if (!got.count(kv.first)) {
        printf("   %s misses n=%d tree:", name, n);
        for (auto& e : kv.second) printf(" %d-%d", e.first, e.second);
        vector<int> dg(n, 0); for (auto& e : kv.second) { dg[e.first]++; dg[e.second]++; }
        sort(dg.rbegin(), dg.rend()); printf("   degs:"); for (int x : dg) printf(" %d", x); puts("");
    }
}

// ---------- backward ----------
int n; int P[40];
vector<u64> C[20][4];          // C[n][1..3] sorted keys ; C[n][0] = class V
set<u64> shapes[20][4], shapesAll[20];
bool has(const vector<u64>& v, u64 x) { return binary_search(v.begin(), v.end(), x); }

void visit() {
    const int* p = P;
    int deg[41] = {0}; u32 adj[41] = {0};
    for (int k = 1; k < n; k++) { int a = p[k], b = p[k] + k; deg[a]++; deg[b]++; adj[a] |= 1u << b; adj[b] |= 1u << a; }
    bool in[4] = {false, false, false, false};
    auto tryR = [&](u32 R, int s) {
        int q[40], mm;
        bool pl = restrictTo(p, n, R, q, mm);
        if (!pl) return;
        u64 kq = key(q, mm);
        if (s <= 2 && !in[0] && isGrowth(q, mm) && has(C[mm][0], kq)) in[0] = true;
        if (!cond2(p, n, R)) return;
        if (!isGrowth(q, mm)) { printf("T1 VIOLATION in ck n=%d\n", n); exit(1); }
        for (int K = s; K <= 3; K++) if (!in[K] && has(C[mm][K], kq)) in[K] = true;
    };
    for (int a = 1; a <= n; a++) {
        if (n - 1 >= 2 && deg[a] == 1) tryR(1u << (a - 1), 1);
        for (int b = a + 1; b <= n; b++) {
            int e2 = deg[a] + deg[b] - (adj[a] >> b & 1);
            if (n - 2 >= 2 && e2 == 2) tryR(1u << (a - 1) | 1u << (b - 1), 2);
            if (n - 3 >= 2) for (int c = b + 1; c <= n; c++) {
                int e3 = e2 + deg[c] - (adj[a] >> c & 1) - (adj[b] >> c & 1);
                if (e3 == 3) tryR(1u << (a - 1) | 1u << (b - 1) | 1u << (c - 1), 3);
            }
        }
    }
    u64 me = key(p, n), cf = canonPl(p, n);
    shapesAll[n].insert(cf);
    for (int K = 0; K <= 3; K++) if (in[K]) { C[n][K].push_back(me); shapes[n][K].insert(cf); }
}
u64 ngrowth;
void gen(int k, u32 used) {
    if (k == 0) { ngrowth++; visit(); return; }
    for (int p = 1; p <= n - k; p++) {
        bool ua = used >> (p - 1) & 1, ub = used >> (p + k - 1) & 1;
        if (k == n - 1) { if (ua || ub) continue; }
        else if (ua == ub) continue;
        P[k] = p;
        gen(k - 1, used | 1u << (p - 1) | 1u << (p + k - 1));
    }
}

// ---------- forward: all p on m+s labels with clean R (|R|=s) and p\R = q ----------
template <class F> void children(const int* q, int m, int s, F&& emit) {
    int M = m + s;
    int p[40];
    int Rl[2];
    for (Rl[0] = 1; Rl[0] <= M; Rl[0]++) for (Rl[1] = (s == 2 ? Rl[0] + 1 : 0); Rl[1] <= (s == 2 ? M : 0); Rl[1]++) {
        u32 R = 1u << (Rl[0] - 1); if (s == 2) R |= 1u << (Rl[1] - 1);
        int mp[41]; { int c = 0; for (int x = 1; x <= M; x++) if (!(R >> (x - 1) & 1)) mp[++c] = x; }
        u32 usedLen = 0; int last = 0; bool ok = true;
        for (int l = 1; l < m; l++) {
            int a = mp[q[l]], b = mp[q[l] + l];
            int nl = b - a;
            if (nl <= last) { ok = false; break; }     // kept brackets must keep length order (necessary for (2))
            last = nl; usedLen |= 1u << nl; p[nl] = a;
        }
        if (!ok) continue;
        int miss[2], nm = 0;
        for (int l = 1; l < M; l++) if (!(usedLen >> l & 1)) miss[nm++] = l;
        // candidate positions for each missing length: bracket of that length with a foot in R
        int cand[2][4], nc[2] = {0, 0};
        for (int i = 0; i < s; i++) {
            int j = miss[i];
            for (int t = 0; t < s; t++) {
                int x = Rl[t];
                int c1 = x - j, c2 = x;   // positions (left feet)
                if (c1 >= 1) { bool dup = false; for (int u = 0; u < nc[i]; u++) if (cand[i][u] == c1) dup = true; if (!dup) cand[i][nc[i]++] = c1; }
                if (c2 + j <= M) { bool dup = false; for (int u = 0; u < nc[i]; u++) if (cand[i][u] == c2) dup = true; if (!dup) cand[i][nc[i]++] = c2; }
            }
        }
        if (s == 1) {
            for (int u = 0; u < nc[0]; u++) {
                p[miss[0]] = cand[0][u];
                if (isGrowth(p, M) && cond1(p, M, R) && cond2(p, M, R)) emit(p, M);
            }
        } else {
            for (int u = 0; u < nc[0]; u++) for (int v = 0; v < nc[1]; v++) {
                p[miss[0]] = cand[0][u]; p[miss[1]] = cand[1][v];
                if (isGrowth(p, M) && cond1(p, M, R) && cond2(p, M, R)) emit(p, M);
            }
        }
    }
}

int main(int argc, char** argv) {
    int NB = atoi(argv[1]), NF = argc > 2 ? atoi(argv[2]) : NB;
    genTrees(max(NB, NF));
    for (int K = 0; K <= 3; K++) C[2][K].push_back(0);
    for (n = 3; n <= NB; n++) {
        ngrowth = 0; gen(n - 1, 0);
        for (int K = 0; K <= 3; K++) sort(C[n][K].begin(), C[n][K].end());
        printf("n=%d trees=%zu growth=%llu shapesWithGrowth=%zu | C1 %zu pl %zu trees | C2 %zu pl %zu trees | C3 %zu pl %zu trees | V(no order,<=2) %zu pl %zu trees\n",
               n, treesOf[n].size(), ngrowth, shapesAll[n].size(), C[n][1].size(), shapes[n][1].size(), C[n][2].size(), shapes[n][2].size(),
               C[n][3].size(), shapes[n][3].size(), C[n][0].size(), shapes[n][0].size());
        if (shapes[n][2].size() != treesOf[n].size()) printMissing(n, shapes[n][2], "C2");
        if (shapes[n][3].size() != treesOf[n].size()) printMissing(n, shapes[n][3], "C3");
        if (shapes[n][0].size() != treesOf[n].size() && n <= 13) printMissing(n, shapes[n][0], "V");
        if (n <= 8 && shapes[n][1].size() != treesOf[n].size()) printMissing(n, shapes[n][1], "C1");
        fflush(stdout);
    }
    // forward check of C(2) against backward for n <= NB (independent second method)
    vector<u64> F[20]; F[2].push_back(0);
    for (int M = 3; M <= NF; M++) {
        bool last = (M == NF && M > NB);   // final level: shapes only, no storing
        int nt = omp_get_max_threads();
        vector<vector<u64>> buf(nt); vector<set<u64>> sh(nt); vector<u64> gencount(nt, 0);
        const size_t CS = 1 << 22;
        vector<vector<u64>> cache(nt, vector<u64>(CS, ~0ull));
        for (int s = 1; s <= 2; s++) {
            int m = M - s; if (m < 2) continue;
            const vector<u64>& src = F[m];
            #pragma omp parallel for schedule(dynamic, 4096)
            for (size_t i = 0; i < src.size(); i++) {
                int t = omp_get_thread_num();
                int q[40]; unkey(src[i], m, q);
                children(q, m, s, [&](const int* p, int MM) {
                    gencount[t]++;
                    u64 k = key(p, MM);
                    size_t h = (k * 0x9E3779B97F4A7C15ull) >> 42;
                    if (cache[t][h] == k) return;
                    cache[t][h] = k;
                    if (last) sh[t].insert(canonPl(p, MM));
                    else buf[t].push_back(k);
                });
            }
        }
        u64 g = 0; for (int t = 0; t < nt; t++) g += gencount[t];
        if (!last) {
            vector<u64>& out = F[M];
            for (int t = 0; t < nt; t++) { out.insert(out.end(), buf[t].begin(), buf[t].end()); vector<u64>().swap(buf[t]); }
            sort(out.begin(), out.end()); out.erase(unique(out.begin(), out.end()), out.end());
            set<u64> shp;
            if (M > NB) {
                vector<set<u64>> s2(nt);
                #pragma omp parallel for schedule(dynamic, 4096)
                for (size_t i = 0; i < out.size(); i++) { int q[40]; unkey(out[i], M, q); s2[omp_get_thread_num()].insert(canonPl(q, M)); }
                for (auto& x : s2) shp.insert(x.begin(), x.end());
            }
            printf("forward n=%d: generated=%llu distinct C2 placements=%zu", M, g, out.size());
            if (M <= NB) printf("  backward=%zu  %s\n", C[M][2].size(), out == C[M][2] ? "IDENTICAL SETS" : "MISMATCH");
            else { printf("  trees reached %zu of %zu\n", shp.size(), treesOf[M].size()); printMissing(M, shp, "C2"); }
        } else {
            set<u64> shp; for (auto& x : sh) shp.insert(x.begin(), x.end());
            printf("forward n=%d (shapes only): generated=%llu trees reached %zu of %zu\n", M, g, shp.size(), treesOf[M].size());
            printMissing(M, shp, "C2");
        }
        fflush(stdout);
        if (M >= 4 && M - 2 >= 2) vector<u64>().swap(F[M - 2 < 2 ? 0 : M - 2 - 0 == M - 2 ? 0 : 0]);  // (no-op; keep all levels)
    }
}
