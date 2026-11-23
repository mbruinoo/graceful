// relaxpattern.cpp -- for every (tree, root) that is NOT an anchor (no slack-0 labeling), enumerate ALL
// slack-1 relaxed growth labelings (root label 1, labels in [1,n+1]) and record which (unused label, unused length)
// pairs occur.  Prints, per n, for each (unused label, unused length) the number of non-anchor pairs that admit it.
// usage: relaxpattern n
// (derived from relaxmin.cpp) -- exhaustive: least slack s such that the rooted tree (T, r)
// has a RELAXED growth labeling with labels in [1, n+s].
//
// Relaxed growth labeling of (T, r) in range N: injective f : V -> {1..N},
// pairwise distinct edge lengths, lengths strictly decreasing along every path
// away from r.  Variant A: f(r) = 1 (for s = 0 this is "r is an anchor",
// README section 7).  Variant B: f(r) arbitrary.
//
// Search: complete backtracking in longest-first order (any relaxed growth
// labeling can be built by placing its edges in decreasing length, each new
// edge hanging a new vertex on a placed one), so "no solution found" is exact.
// Every solution found is re-checked from the definition.
//
// usage: relaxmin n [maxslack=3] [B]     (all free trees on n vertices, all roots)
#include <bits/stdc++.h>
#include "../../treegen.h"
using namespace std;
typedef unsigned long long u64;
static int n, N; static vector<vector<int>> ch; static vector<int> par_, code_;
static int lab[64]; static u64 used; static vector<int> pend[64]; static vector<int> frontier;
static long long nodes;

static bool verify(int root, bool rootAtOne) {
    u64 sl = 0, se = 0; if (rootAtOne && lab[root] != 1) return false;
    for (int v = 0; v < n; v++) { if (lab[v] < 1 || lab[v] > N || (sl >> lab[v] & 1)) return false; sl |= 1ULL << lab[v]; }
    for (int v = 0; v < n; v++) if (v != root) { int p = par_[v], d = abs(lab[v] - lab[p]); if (se >> d & 1) return false; se |= 1ULL << d;
        if (p != root) { int dp = abs(lab[p] - lab[par_[p]]); if (!(d < dp)) return false; } }
    return true;
}
static bool g_all = false; static set<pair<int,int>> g_pat; static u64 g_lens;
static bool dfs(int L, int rem) {
    if (rem == 0) { if (!g_all) return true; int ul = 0, ue = 0; for (int x = 1; x <= N; x++) if (!(used >> x & 1)) ul = x; for (int d = 1; d <= N - 1; d++) if (!(g_lens >> d & 1)) ue = d; g_pat.insert({ul, ue}); return false; } nodes++;
    for (int l = L - 1; l >= rem; --l) {
        for (int v = 0; v < n; v++) if (lab[v] && !pend[v].empty()) {
            int y = lab[v];
            for (int sgn = -1; sgn <= 1; sgn += 2) {
                int x = y + sgn * l; if (x < 1 || x > N || (used >> x & 1)) continue;
                int lastcode = -1;
                for (size_t i = 0; i < pend[v].size(); i++) {
                    int c = pend[v][i]; if (code_[c] == lastcode) continue; lastcode = code_[c];   // pend sorted by code: equivalent children tried once
                    pend[v].erase(pend[v].begin() + i); lab[c] = x; used |= 1ULL << x; g_lens |= 1ULL << l;
                    bool ok = dfs(l, rem - 1);
                    if (ok) return true;
                    used &= ~(1ULL << x); lab[c] = 0; g_lens &= ~(1ULL << l); pend[v].insert(pend[v].begin() + i, c);
                }
            }
        }
    }
    return false;
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); int maxs = argc > 2 ? atoi(argv[2]) : 3; bool varB = argc > 3;
    TreeGen g(n); vector<int> p0; long long trees = 0, pairs = 0, bad = 0;
    vector<long long> hist(maxs + 2, 0), treehist(maxs + 2, 0); long long treeAllRootsAt1 = 0;
    map<vector<int>, int> codes; map<pair<int,int>, long long> patcount; long long nonanch = 0, no_e1 = 0; long long withleaf = 0, withleaf_bad = 0, deghist[10] = {0};
    while (g.next()) {
        trees++; g.parents(p0);
        vector<vector<int>> adj(n); for (int i = 1; i < n; i++) { adj[i].push_back(p0[i]); adj[p0[i]].push_back(i); }
        int best = maxs + 1, worst = 0;
        for (int r = 0; r < n; r++) {
            ch.assign(n, {}); par_.assign(n, -1); code_.assign(n, 0);
            vector<int> order = {r};
            for (size_t i = 0; i < order.size(); i++) { int v = order[i]; for (int u : adj[v]) if (u != par_[v]) { par_[u] = v; ch[v].push_back(u); order.push_back(u); } }
            for (int i = n - 1; i >= 0; i--) { int v = order[i]; vector<int> k; for (int c : ch[v]) k.push_back(code_[c]); sort(k.begin(), k.end());
                auto it = codes.find(k); if (it == codes.end()) it = codes.insert({k, (int)codes.size() + 1}).first; code_[v] = it->second; }
            int s;
            for (s = 0; s <= maxs; s++) {
                N = n + s; bool found = false;
                int rlmax = varB ? (N + 1) / 2 : 1;                 // reflection: root label <= (N+1)/2 suffices
                for (int rl = 1; rl <= rlmax && !found; rl++) {
                    memset(lab, 0, sizeof lab); used = 1ULL << rl; lab[r] = rl;
                    for (int v = 0; v < n; v++) { pend[v] = ch[v]; sort(pend[v].begin(), pend[v].end(), [&](int a, int b) { return code_[a] < code_[b]; }); }
                    if (dfs(N, n - 1)) { found = true; if (!verify(r, !varB)) bad++; }
                }
                if (found) break;
            }
            if (s == 1) { g_all = true; g_pat.clear(); g_lens = 0; N = n + 1; memset(lab, 0, sizeof lab); used = 2; lab[r] = 1;
                for (int v = 0; v < n; v++) { pend[v] = ch[v]; sort(pend[v].begin(), pend[v].end(), [&](int a, int b) { return code_[a] < code_[b]; }); }
                dfs(N, n - 1); g_all = false; nonanch++; for (auto& p : g_pat) patcount[p]++;
                bool e1 = false; for (auto& p : g_pat) if (p.second == 1) e1 = true; if (!e1) no_e1++; }
            pairs++; hist[s]++; best = min(best, s); worst = max(worst, s);
            { bool leafnb = false; for (int u : adj[r]) if (adj[u].size() == 1) leafnb = true; if (leafnb) { withleaf++; if (s > 0) withleaf_bad++; }
              if (s > 0) deghist[min<int>(adj[r].size(), 9)]++; }
        }
        treehist[best]++; if (worst == 0) treeAllRootsAt1++;
    }
    printf("n=%d variant=%s trees=%lld rooted pairs (tree,vertex)=%lld  verify_failures=%lld\n", n, varB ? "B(root label free)" : "A(root label 1)", trees, pairs, bad);
    for (int s = 0; s <= maxs + 1; s++) printf("  least slack %s%d: %lld (tree,root) pairs;  trees whose best root needs it: %lld\n", s > maxs ? ">" : "", s > maxs ? maxs : s, hist[s], treehist[s]);
    printf("  non-anchor pairs: %lld.  (unused label, unused length): number of non-anchor pairs admitting it\n", nonanch);
    for (auto& p : patcount) if (p.second * 2 >= nonanch) printf("   (%d,%d): %lld\n", p.first.first, p.first.second, p.second);
    printf("  roots having a leaf neighbour: %lld, of which need slack > 0: %lld\n", withleaf, withleaf_bad);
    printf("  degree of roots needing slack > 0:"); for (int d = 1; d < 10; d++) printf(" deg%d:%lld", d, deghist[d]); printf("\n");
    return 0;
}
