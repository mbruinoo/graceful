// Referee brute force for claims 1 (n=17 exceptions) and 2 (step number kappa).
// Top-down: enumerate every growth labeling of a given tree, then
//   kappa(p) = min over clean sets R of max(|R|, kappa(p\R)),  kappa(single edge) = 0.
// Clean sets are found by enumerating every connected vertex set S (|S|>=2) of the tree drawn
// by p and testing condition (2) on R = complement; condition (1) holds iff S is connected
// (|S|-1 kept edges <=> exactly |R| brackets touch R), and that is double-checked literally.
// usage: ./kap S l1 l2 l3 ...      spider with given leg lengths
//        ./kap E a-b c-d ...       tree by edge list (0-based)
//        ./kap scan nmin nmax      all 3-legged spiders, report those with kappa >= 3
#include <bits/stdc++.h>
using namespace std;
typedef unsigned int u32;
typedef unsigned long long u64;
const int INF = 99;

unordered_map<string, int> memo;
u64 literalChecks = 0;

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
        u32 between = ((1u << (b - 1)) - 1) & ~((1u << a) - 1);
        if (__builtin_popcount(R & between) != shorter) return false;
    }
    return true;
}
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
void connSets(const u32* adj, int m, u32 S, u32 X, u32 nb, vector<u32>& out) {
    u32 cand = nb & ~S & ~X;
    if (!cand) { if (__builtin_popcount(S) >= 2 && __builtin_popcount(S) < m) out.push_back(S); return; }
    int v = __builtin_ctz(cand);
    connSets(adj, m, S | 1u << v, X, nb | adj[v], out);
    connSets(adj, m, S, X | 1u << v, nb, out);
}
int kappa(const int* p, int m) {
    if (m == 2) return 0;
    string key((size_t)(m - 1), 0);
    for (int k = 1; k < m; k++) key[k - 1] = (char)p[k];
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;
    u32 adj[32] = {0};
    for (int k = 1; k < m; k++) { int a = p[k] - 1, b = p[k] + k - 1; adj[a] |= 1u << b; adj[b] |= 1u << a; }
    vector<u32> sets;
    u32 full = (m == 32) ? ~0u : ((1u << m) - 1);
    for (int r = 0; r < m; r++) connSets(adj, m, 1u << r, (1u << r) - 1, adj[r], sets);
    vector<pair<int, u32>> cl;
    for (u32 S : sets) {
        u32 R = full & ~S;
        if (!cond2(p, m, R)) continue;
        literalChecks++;
        if (!cond1(p, m, R)) { printf("BUG: cond1 fails for connected complement\n"); exit(1); }
        cl.push_back({__builtin_popcount(R), R});
    }
    sort(cl.begin(), cl.end());
    int best = INF;
    for (auto& c : cl) {
        if (c.first >= best) break;
        int q[40], mm;
        if (!restrictTo(p, m, c.second, q, mm) || !isGrowth(q, mm)) { printf("T1 VIOLATION (kap) m=%d R=%x\n", m, c.second); exit(1); }
        int v = max(c.first, kappa(q, mm));
        if (v < best) best = v;
    }
    memo[key] = best;
    return best;
}

// ---- tree and its growth labelings ----
int n; vector<int> g[40]; int lab[40]; bool usedLab[41];
u64 nlab; map<int, u64> dist; int minK; int stopAt = -1; bool stopped;
set<vector<int>> placements;
void search(int k) {
    if (stopped) return;
    if (k == 0) {
        int p[40];
        for (int v = 0; v < n; v++) for (int w : g[v]) if (lab[v] < lab[w]) p[lab[w] - lab[v]] = lab[v];
        if (!isGrowth(p, n)) { printf("BUG: labeling not growth\n"); exit(1); }
        nlab++;
        placements.insert(vector<int>(p + 1, p + n));
        int kp = kappa(p, n);
        dist[kp]++; minK = min(minK, kp);
        if (kp <= stopAt) stopped = true;
        return;
    }
    for (int u = 0; u < n; u++) if (lab[u]) for (int v : g[u]) if (!lab[v]) {
        for (int sgn = -1; sgn <= 1; sgn += 2) {
            int x = lab[u] + sgn * k;
            if (x < 1 || x > n || usedLab[x]) continue;
            lab[v] = x; usedLab[x] = true;
            search(k - 1);
            lab[v] = 0; usedLab[x] = false;
        }
    }
}
void run() {
    nlab = 0; dist.clear(); minK = INF; stopped = false; placements.clear();
    memset(lab, 0, sizeof lab); memset(usedLab, 0, sizeof usedLab);
    for (int v = 0; v < n && !stopped; v++) for (int w : g[v]) {
        lab[v] = 1; lab[w] = n; usedLab[1] = usedLab[n] = true;
        search(n - 2);
        lab[v] = lab[w] = 0; usedLab[1] = usedLab[n] = false;
    }
}
void spider(const vector<int>& legs) {
    n = 1; for (int l : legs) n += l;
    for (int i = 0; i < n; i++) g[i].clear();
    int c = 1;
    for (int l : legs) { int prev = 0; for (int i = 0; i < l; i++) { g[prev].push_back(c); g[c].push_back(prev); prev = c++; } }
}
int main(int argc, char** argv) {
    string mode = argv[1];
    if (mode == "scan") {
        int a0 = atoi(argv[2]), a1 = atoi(argv[3]);
        stopAt = 2;
        for (int N = a0; N <= a1; N++) {
            int cnt = 0;
            for (int a = N - 1; a >= 1; a--) for (int b = a; b >= 1; b--) { int c = N - 1 - a - b; if (c < 1 || c > b) continue;
                spider({a, b, c}); run(); cnt++;
                if (minK >= 3) printf("n=%d S(%d,%d,%d) kappa=%d  labelings=%llu placements=%zu\n", N, a, b, c, minK, nlab, placements.size());
                fflush(stdout);
            }
            printf("n=%d: %d three-legged spiders scanned (memo %zu)\n", N, cnt, memo.size()); fflush(stdout);
        }
        return 0;
    }
    if (mode == "S") { vector<int> legs; for (int i = 2; i < argc; i++) legs.push_back(atoi(argv[i])); spider(legs); }
    else {
        n = 0;
        for (int i = 2; i < argc; i++) { int a, b; sscanf(argv[i], "%d-%d", &a, &b); g[a].push_back(b); g[b].push_back(a); n = max(n, max(a, b) + 1); }
    }
    run();
    printf("n=%d labelings=%llu distinct placements=%zu  min kappa=%d  kappa distribution (per labeling):", n, nlab, placements.size(), minK);
    for (auto& kv : dist) printf(" %d:%llu", kv.first, kv.second);
    printf("   [memo %zu, clean sets seen %llu]\n", memo.size(), literalChecks);
}
