// greedy.cpp -- randomized longest-first process for RELAXED growth labelings.
//
// Definition (relaxed growth labeling, range N >= n). A tree T on n vertices,
// a root r, an injective f : V -> {1..N} with f(r) = 1, such that
//   (i)  the n-1 edge lengths |f(u)-f(v)| are pairwise distinct, and
//   (ii) lengths strictly decrease along every path away from r.
// For N = n this is exactly a growth placement (README Theorem 7).
//
// Process (no backtracking). Keep the current length bound L (initially N).
// Repeatedly: find the LARGEST l < L for which some placed vertex y with an
// unplaced child has y+l or y-l free and inside [1,N]; among all such
// (parent, free label) pairs pick one by the tie-break policy; place one
// child there; set L = l.  Fail if l would drop below the number of vertices
// still to place (then no completion exists).
//
// Every success is re-verified from the definition (verify()).
//
// usage: greedy TYPE n TRIALS POLICY ROOT SEED  slack1 slack2 ...
//   TYPE   : prufer | recursive | binary | cater | spider<k> | cbin | path |
//            comb<L> | pa | lobster
//   POLICY : 0 uniform random candidate, random child
//            1 child with the largest subtree first (ties random)
//            2 child with the tallest subtree first (ties random)
//            3 child with the smallest subtree first (ties random)
//            4 most urgent parent first: minimise (free labels the parent can
//              still reach with shorter lengths) - (its unplaced children);
//              that parent's largest child is placed
//            5 non-leaf children first, largest subtree first (as 1); among
//              leaf children, most urgent parent first (as 4)
//            6 parents whose margin (as in 4) is <= THETA (env, default 0)
//              first, smallest margin first; otherwise as 1
//   ROOT   : c centroid | r random vertex | l random leaf
//   slack  : N = n + slack.  Each tree is tried at every slack (same tree).
// output: one line per slack: successes / trials, plus mean number of skipped
//         lengths in successful runs.
// With slack list "min": for each tree find by doubling+bisection the least
//   slack at which a single run succeeds (not exactly monotone; reported as is).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
static const int MAXN = 16384, W = MAXN / 64;
struct BS {
    u64 w[W];
    void clear() { memset(w, 0, sizeof w); }
    void set(int i) { w[i >> 6] |= 1ULL << (i & 63); }
    void reset(int i) { w[i >> 6] &= ~(1ULL << (i & 63)); }
    bool get(int i) const { return w[i >> 6] >> (i & 63) & 1; }
};
static int NW;
// out = (a << s) & ~u  (labels y -> y+s), returns any-nonzero
static bool shl_andnot(const BS& a, int s, const BS& u, BS& out) {
    int ws = s >> 6, bs = s & 63; bool any = false;
    for (int i = NW - 1; i >= 0; --i) {
        u64 v = 0;
        if (i - ws >= 0) { v = a.w[i - ws] << bs; if (bs && i - ws - 1 >= 0) v |= a.w[i - ws - 1] >> (64 - bs); }
        v &= ~u.w[i]; out.w[i] = v; any |= v != 0;
    }
    return any;
}
static bool shr_andnot(const BS& a, int s, const BS& u, BS& out) {
    int ws = s >> 6, bs = s & 63; bool any = false;
    for (int i = 0; i < NW; ++i) {
        u64 v = 0;
        if (i + ws < NW) { v = a.w[i + ws] >> bs; if (bs && i + ws + 1 < NW) v |= a.w[i + ws + 1] << (64 - bs); }
        v &= ~u.w[i]; out.w[i] = v; any |= v != 0;
    }
    return any;
}

static mt19937_64 rng;
static int rnd(int m) { return (int)(rng() % (u64)m); }

// ---------- tree generators: return edge list on vertices 0..n-1 ----------
static vector<pair<int,int>> gen(const string& type, int n) {
    vector<pair<int,int>> e;
    if (type == "prufer") {            // uniform random labelled tree
        if (n == 2) { e.push_back({0, 1}); return e; }
        vector<int> p(n - 2), deg(n, 1);
        for (auto& x : p) { x = rnd(n); deg[x]++; }
        set<int> leaves; for (int i = 0; i < n; i++) if (deg[i] == 1) leaves.insert(i);
        for (int x : p) { int l = *leaves.begin(); leaves.erase(leaves.begin()); e.push_back({l, x}); if (--deg[x] == 1) leaves.insert(x); }
        int a = *leaves.begin(), b = *leaves.rbegin(); e.push_back({a, b});
    } else if (type == "recursive") {  // random recursive tree
        for (int i = 1; i < n; i++) e.push_back({rnd(i), i});
    } else if (type == "pa") {         // preferential attachment
        vector<int> ends; e.push_back({0, 1}); ends = {0, 1};
        for (int i = 2; i < n; i++) { int p = ends[rnd(ends.size())]; e.push_back({p, i}); ends.push_back(p); ends.push_back(i); }
    } else if (type == "binary") {     // max degree 3: attach to random vertex of degree < 3
        vector<int> deg(n, 0), avail = {0};
        for (int i = 1; i < n; i++) {
            int k = rnd(avail.size()), p = avail[k]; e.push_back({p, i}); deg[p]++; deg[i]++;
            if (deg[p] == 3) { avail[k] = avail.back(); avail.pop_back(); }
            avail.push_back(i);
        }
    } else if (type == "cater") {      // random caterpillar: spine n/2, rest random legs
        int s = max(2, n / 2); for (int i = 1; i < s; i++) e.push_back({i - 1, i});
        for (int i = s; i < n; i++) e.push_back({rnd(s), i});
    } else if (type == "lobster") {    // spine n/3, n/3 random legs, n/3 random second-level
        int s = max(2, n / 3), m = max(s + 1, 2 * n / 3); for (int i = 1; i < s; i++) e.push_back({i - 1, i});
        for (int i = s; i < m; i++) e.push_back({rnd(s), i});
        for (int i = m; i < n; i++) e.push_back({s + rnd(m - s), i});
    } else if (type.rfind("spider", 0) == 0) {  // k legs, lengths as equal as possible
        int k = atoi(type.c_str() + 6), id = 1;
        for (int j = 0; j < k; j++) { int len = (n - 1) / k + (j < (n - 1) % k), prev = 0; for (int t = 0; t < len; t++) { e.push_back({prev, id}); prev = id++; } }
    } else if (type == "cbin") {       // heap-shaped binary tree
        for (int i = 1; i < n; i++) e.push_back({(i - 1) / 2, i});
    } else if (type == "path") {
        for (int i = 1; i < n; i++) e.push_back({i - 1, i});
    } else if (type.rfind("comb", 0) == 0) {    // spine with a pendant path of length L at every spine vertex
        int L = atoi(type.c_str() + 4), id = 0, prevspine = -1;
        while (id < n) { int sp = id++; if (prevspine >= 0) e.push_back({prevspine, sp}); prevspine = sp; int prev = sp; for (int t = 0; t < L && id < n; t++) { e.push_back({prev, id}); prev = id++; } }
    } else { fprintf(stderr, "unknown type\n"); exit(1); }
    return e;
}

struct Tree { int n, root; vector<vector<int>> ch; vector<int> par, sz, ht; };
static Tree build(int n, const vector<pair<int,int>>& e, char rootmode) {
    vector<vector<int>> adj(n); for (auto& x : e) { adj[x.first].push_back(x.second); adj[x.second].push_back(x.first); }
    Tree T; T.n = n; T.ch.assign(n, {}); T.par.assign(n, -1); T.sz.assign(n, 1); T.ht.assign(n, 0);
    auto rootat = [&](int r) {
        T.root = r; for (auto& c : T.ch) c.clear(); fill(T.sz.begin(), T.sz.end(), 1); fill(T.ht.begin(), T.ht.end(), 0);
        vector<int> order = {r}; T.par[r] = -1;
        for (size_t i = 0; i < order.size(); i++) { int v = order[i]; for (int u : adj[v]) if (u != T.par[v]) { T.par[u] = v; T.ch[v].push_back(u); order.push_back(u); } }
        for (int i = n - 1; i > 0; i--) { int v = order[i], p = T.par[v]; T.sz[p] += T.sz[v]; T.ht[p] = max(T.ht[p], T.ht[v] + 1); }
    };
    rootat(0);
    int r = 0;
    if (rootmode == 'c') { for (;;) { int nx = -1; for (int c : T.ch[r]) if (2 * T.sz[c] > n) nx = c; if (nx < 0) break; r = nx; } }
    else if (rootmode == 'r') r = rnd(n);
    else { vector<int> lv; for (int v = 0; v < n; v++) if (adj[v].size() == 1) lv.push_back(v); r = lv[rnd(lv.size())]; }
    rootat(r);
    return T;
}

// check a labeling against the definition; returns true iff relaxed growth labeling in [1,N]
static bool verify(const Tree& T, const vector<int>& lab, int N) {
    int n = T.n; vector<char> seenL(N + 1, 0), seenE(N + 1, 0);
    if (lab[T.root] != 1) return false;
    for (int v = 0; v < n; v++) { if (lab[v] < 1 || lab[v] > N || seenL[lab[v]]) return false; seenL[lab[v]] = 1; }
    for (int v = 0; v < n; v++) if (v != T.root) {
        int p = T.par[v], d = abs(lab[v] - lab[p]); if (d < 1 || seenE[d]) return false; seenE[d] = 1;
        if (p != T.root) { int dp = abs(lab[p] - lab[T.par[p]]); if (!(d < dp)) return false; }
    }
    return true;
}

static long long g_skips; static int g_minlen; static int g_theta = 0;
static int fen[MAXN + 2], fenN;                 // Fenwick tree over used labels
static void fadd(int i) { for (; i <= fenN; i += i & -i) fen[i]++; }
static int fsum(int i) { int s = 0; if (i > fenN) i = fenN; for (; i > 0; i -= i & -i) s += fen[i]; return s; }
static int freein(int a, int b) { if (a < 1) a = 1; if (b > fenN) b = fenN; if (a > b) return 0; return (b - a + 1) - (fsum(b) - fsum(a - 1)); }
static bool run(const Tree& T, int N, int policy, vector<int>& lab) {
    int n = T.n; NW = (N + 64) / 64 + 1;
    static BS used, front, c1, c2; used.clear(); front.clear();
    static vector<int> at; at.assign(N + 2, -1);
    vector<vector<int>> pend(n);            // pending children, best LAST
    vector<double> key(n);
    fenN = N; memset(fen, 0, sizeof(int) * (N + 2)); fadd(1);
    for (int v = 0; v < n; v++) key[v] = (policy == 1 || policy >= 4 ? T.sz[v] : policy == 2 ? T.ht[v] : policy == 3 ? -T.sz[v] : 0) + (rng() >> 11) * (1.0 / 9007199254740992.0) * 0.5;
    for (int v = 0; v < n; v++) { pend[v] = T.ch[v]; sort(pend[v].begin(), pend[v].end(), [&](int a, int b) { return key[a] < key[b]; }); }
    lab.assign(n, 0); lab[T.root] = 1; used.set(1); at[1] = T.root; if (!pend[T.root].empty()) front.set(1);
    // labels outside [1,N] must never be free: mark them used
    used.set(0); for (int i = N + 1; i < NW * 64; i++) used.set(i);
    int L = N, rem = n - 1; g_skips = 0;
    while (rem > 0) {
        int l = L - 1; bool a1 = false, a2 = false;
        for (; l >= rem; --l) { a1 = shl_andnot(front, l, used, c1); a2 = shr_andnot(front, l, used, c2); if (a1 || a2) break; }
        if (l < rem) return false;
        g_skips += (L - 1) - l;
        // choose candidate
        int bestx = -1, besty = -1; double bestk = -1e300; int cnt = 0;
        for (int pass = 0; pass < 2; pass++) {
            if (!(pass ? a2 : a1)) continue; const BS& c = pass ? c2 : c1;
            for (int i = 0; i < NW; i++) { u64 w = c.w[i]; while (w) { int x = i * 64 + __builtin_ctzll(w); w &= w - 1;
                int y = pass ? x + l : x - l; int v = at[y]; double k;
                if (policy == 0) { cnt++; k = (rnd(cnt) == 0) ? 1e300 : -1e299; if (k > 0) { bestx = x; besty = y; } continue; }
                k = key[pend[v].back()];
                if ((policy == 4 || policy == 5) && !(policy == 5 && k >= 2)) {   // urgency: reachable free labels with lengths in [rem-1, l-1], minus pending children
                    int lo = max(rem - 1, 1), reach = freein(y - l + 1, y - lo) + freein(y + lo, y + l - 1) - 1;
                    k = -(reach - (int)pend[v].size()) * 1e-3 * (policy == 5 ? 1 : 1e6) + (k - floor(k)) * 1e-4 + (policy == 4 ? 0 : 1.0);
                } else if (policy == 5) k += 10;
                if (policy == 6) {   // critical parents first (margin <= THETA), otherwise largest subtree first
                    int lo = max(rem - 1, 1), reach = freein(y - l + 1, y - lo) + freein(y + lo, y + l - 1) - 1, margin = reach - (int)pend[v].size();
                    k = key[pend[v].back()]; if (margin <= g_theta) k += 1e7 - 1e3 * margin;
                }
                if (k > bestk) { bestk = k; bestx = x; besty = y; } } }
        }
        int v = at[besty]; int c;
        if (policy == 0) { int j = rnd(pend[v].size()); c = pend[v][j]; pend[v][j] = pend[v].back(); pend[v].pop_back(); }
        else { c = pend[v].back(); pend[v].pop_back(); }
        if (pend[v].empty()) front.reset(besty);
        lab[c] = bestx; used.set(bestx); fadd(bestx); at[bestx] = c; if (!pend[c].empty()) front.set(bestx);
        L = l; rem--;
    }
    g_minlen = L;
    return true;
}

int main(int argc, char** argv) {
    if (argc < 8) { fprintf(stderr, "usage: greedy TYPE n TRIALS POLICY ROOT SEED slack...|min\n"); return 1; }
    string type = argv[1]; int n = atoi(argv[2]), trials = atoi(argv[3]), policy = atoi(argv[4]); char rootmode = argv[5][0];
    rng.seed(atoll(argv[6])); if (getenv("THETA")) g_theta = atoi(getenv("THETA"));
    bool minmode = string(argv[7]) == "min";
    vector<int> slacks; if (!minmode) for (int i = 7; i < argc; i++) slacks.push_back(atoi(argv[i]));
    vector<int> succ(slacks.size(), 0); vector<double> skipsum(slacks.size(), 0), minlensum(slacks.size(), 0);
    vector<int> mins; vector<int> lab; long long bad = 0;
    for (int t = 0; t < trials; t++) {
        auto e = gen(type, n); Tree T = build(n, e, rootmode);
        if (minmode) {
            auto ok = [&](int s) { bool r = run(T, n + s, policy, lab); if (r && !verify(T, lab, n + s)) { bad++; r = false; } return r; };
            int hi = 0; if (!ok(0)) { hi = 1; while (hi < 8 * n && !ok(hi)) hi *= 2; int lo = hi / 2; while (hi - lo > 1) { int m = (lo + hi) / 2; if (ok(m)) hi = m; else lo = m; } }
            mins.push_back(hi);
        } else for (size_t i = 0; i < slacks.size(); i++) {
            int N = n + slacks[i]; bool r = run(T, N, policy, lab);
            if (r) { if (!verify(T, lab, N)) { bad++; continue; } succ[i]++; skipsum[i] += g_skips; minlensum[i] += g_minlen; }
        }
    }
    if (minmode) {
        sort(mins.begin(), mins.end()); double mean = 0; for (int x : mins) mean += x; mean /= trials;
        printf("%s n=%d policy=%d root=%c trials=%d  least slack: min=%d q25=%d median=%d q75=%d q90=%d max=%d mean=%.1f  verify_failures=%lld\n",
               type.c_str(), n, policy, rootmode, trials, mins[0], mins[trials / 4], mins[trials / 2], mins[3 * trials / 4], mins[9 * trials / 10], mins.back(), mean, bad);
    } else for (size_t i = 0; i < slacks.size(); i++)
        printf("%s n=%d policy=%d root=%c slack=%d eps=%.4f  success %d/%d  mean_skips=%.1f mean_shortest_len=%.1f verify_failures=%lld\n",
               type.c_str(), n, policy, rootmode, slacks[i], slacks[i] / (double)n, succ[i], trials,
               succ[i] ? skipsum[i] / succ[i] : 0.0, succ[i] ? minlensum[i] / succ[i] : 0.0, bad);
    return 0;
}
