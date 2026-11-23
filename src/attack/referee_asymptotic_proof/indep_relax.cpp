// Referee check of claim 0 (independent of relaxmin.cpp).
// Search order differs on purpose: vertices are labelled in BFS (parent-first) order,
// NOT longest-edge-first.  For vertex v with parent p (label y, parent-edge length Lp)
// try every unused length l < Lp (l >= height of v's subtree) and both signs.
// Reads trees from emit_trees.py on stdin.  For each (T,r): least slack s in 0..2 (3 = none).
// Also: for each pair needing slack >= 1, is r an anchor (slack 0) of T + new leaf at r ?
#include <bits/stdc++.h>
using namespace std;
static int n, N; static vector<vector<int>> adj; static vector<int> order_, par, ht; static int lab[40], elen[40]; static bool usedL[80], usedE[80];
static bool rec(int i) {
    if (i == (int)order_.size()) return true;
    int v = order_[i], p = par[v], y = lab[p], Lp = elen[p];
    for (int l = Lp - 1; l >= ht[v] + 1; --l) { if (usedE[l]) continue;
        for (int sg = -1; sg <= 1; sg += 2) { int x = y + sg * l; if (x < 1 || x > N || usedL[x]) continue;
            usedE[l] = usedL[x] = true; lab[v] = x; elen[v] = l;
            if (rec(i + 1)) return true;
            usedE[l] = usedL[x] = false; } }
    return false;
}
static bool check(int r) { // definition check of lab[]
    set<int> L, E; if (lab[r] != 1) return false;
    for (int v = 0; v < (int)adj.size(); v++) { if (lab[v] < 1 || lab[v] > N || !L.insert(lab[v]).second) return false; }
    for (int v : order_) if (v != r) { int d = abs(lab[v] - lab[par[v]]); if (d < 1 || !E.insert(d).second) return false;
        if (par[v] != r && !(d < abs(lab[par[v]] - lab[par[par[v]]]))) return false; }
    return true;
}
static long long bad = 0;
static bool solve(int r, int range) {
    int m = adj.size(); N = range; par.assign(m, -1); ht.assign(m, 0); order_ = {r};
    for (size_t i = 0; i < order_.size(); i++) { int v = order_[i]; for (int u : adj[v]) if (u != par[v]) { par[u] = v; order_.push_back(u); } }
    for (int i = m - 1; i > 0; i--) { int v = order_[i]; ht[par[v]] = max(ht[par[v]], ht[v] + 1); }
    memset(usedL, 0, sizeof usedL); memset(usedE, 0, sizeof usedE); lab[r] = 1; usedL[1] = true; elen[r] = N;
    bool ok = rec(1); if (ok && !check(r)) { bad++; } return ok;
}
int main() {
    long long trees = 0, pairs = 0, hist[4] = {0}, leafnb_bad = 0, deg[10] = {0}, treeNoAnchor = 0, routeOK = 0, routeFail = 0;
    while (scanf("%d", &n) == 1) { adj.assign(n, {}); for (int i = 0; i < n - 1; i++) { int a, b; scanf("%d %d", &a, &b); adj[a].push_back(b); adj[b].push_back(a); }
        trees++; bool any0 = false;
        for (int r = 0; r < n; r++) { int s = 0; while (s < 3 && !solve(r, n + s)) s++;
            pairs++; hist[s]++; if (s == 0) any0 = true;
            if (s > 0) { deg[min<int>(adj[r].size(), 9)]++; bool ln = false; for (int u : adj[r]) if (adj[u].size() == 1) ln = true; if (ln) leafnb_bad++;
                // route of the claimant's sketch: is r an anchor of T + leaf at r ?
                adj.push_back({r}); adj[r].push_back(n); bool a = solve(r, n + 1); adj[r].pop_back(); adj.pop_back(); (a ? routeOK : routeFail)++;
                if (!a) { printf("  route fails: n=%d root=%d deg=%zu leafnb=%d edges:", n, r, adj[r].size(), (int)ln); for (int v = 0; v < n; v++) for (int u : adj[v]) if (u > v) printf(" %d-%d", v, u); printf("\n"); } }
        }
        if (!any0) treeNoAnchor++;
    }
    printf("n=%d trees=%lld pairs=%lld slack0=%lld slack1=%lld slack2=%lld slack>2=%lld  verify_failures=%lld\n", n, trees, pairs, hist[0], hist[1], hist[2], hist[3], bad);
    printf("  trees with no slack-0 root: %lld; non-anchors with a leaf neighbour: %lld; degrees of non-anchors:", treeNoAnchor, leafnb_bad); for (int d = 1; d < 10; d++) printf(" %lld", deg[d]); printf("\n");
    printf("  of the slack>=1 pairs: r is an anchor of T+leaf(r): %lld, is not: %lld\n", routeOK, routeFail);
}
