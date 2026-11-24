// Independent referee solver (written from README definitions only).
// Anchor test: does tree T have a graceful labelling with labels 0..m, root r at 0,
// such that edge lengths strictly decrease along every path away from r (README Thm 7)?
// Search: assign lengths m, m-1, ..., 1 in turn; length k goes to a frontier edge
// (parent labelled, child not), child label = parent label +- k.  Children of one parent
// with isomorphic subtrees are interchangeable, so only one per class is tried.
// Input lines: n r u1 v1 ... u_{n-1} v_{n-1}
// Mode argv[1]: "d" decide (prints ANCHOR+labels / NOT / CAP), "a" enumerate all (prints each labelling).
#include <bits/stdc++.h>
using namespace std;
int n, m, R; vector<vector<int>> ch; vector<int> par, cls, lab; vector<char> used, done;
long long nodes, cap; string mode; long long nsol;
vector<int> order_frontier;
bool rec(int k) {
    if (++nodes > cap) return false;
    if (k == 0) {
        nsol++;
        if (mode == "a") { for (int i = 0; i < n; i++) printf("%d ", lab[i]); printf("\n"); return false; }
        return true;
    }
    // frontier: unlabelled vertices whose parent is labelled
    set<pair<int,int>> tried; // (parent, class)
    for (int x = 0; x < n; x++) {
        if (done[x] || x == R || !done[par[x]]) continue;
        if (!tried.insert({par[x], cls[x]}).second) continue;
        int pl = lab[par[x]];
        for (int s = -1; s <= 1; s += 2) {
            int L = pl + s * k;
            if (L < 0 || L > m || used[L]) continue;
            used[L] = 1; done[x] = 1; lab[x] = L;
            if (rec(k - 1)) return true;
            used[L] = 0; done[x] = 0; lab[x] = -1;
            if (nodes > cap) return false;
        }
    }
    return false;
}
int main(int argc, char** argv) {
    mode = argc > 1 ? argv[1] : "d"; cap = argc > 2 ? atoll(argv[2]) : 4000000000LL;
    while (scanf("%d %d", &n, &R) == 2) {
        m = n - 1; vector<vector<int>> adj(n);
        for (int i = 0; i < n - 1; i++) { int u, v; scanf("%d %d", &u, &v); adj[u].push_back(v); adj[v].push_back(u); }
        ch.assign(n, {}); par.assign(n, -1);
        vector<int> bfs = {R}; vector<char> seen(n, 0); seen[R] = 1;
        for (size_t i = 0; i < bfs.size(); i++) for (int y : adj[bfs[i]]) if (!seen[y]) { seen[y] = 1; par[y] = bfs[i]; ch[bfs[i]].push_back(y); bfs.push_back(y); }
        // canonical classes of rooted subtrees (AHU)
        map<vector<int>, int> canon; cls.assign(n, 0);
        for (int i = n - 1; i >= 0; i--) { int x = bfs[i]; vector<int> c; for (int y : ch[x]) c.push_back(cls[y]); sort(c.begin(), c.end());
            auto it = canon.find(c); if (it == canon.end()) { int id = canon.size(); canon[c] = id; cls[x] = id; } else cls[x] = it->second; }
        lab.assign(n, -1); used.assign(n, 0); done.assign(n, 0);
        lab[R] = 0; used[0] = 1; done[R] = 1; nodes = 0; nsol = 0;
        bool ok = rec(m);
        if (mode == "a") printf("END solutions=%lld nodes=%lld%s\n", nsol, nodes, nodes > cap ? " CAP" : "");
        else if (ok) { // verify from definition
            set<int> L, D; bool good = true;
            for (int i = 0; i < n; i++) L.insert(lab[i]);
            for (int x = 0; x < n; x++) if (x != R) { int d = abs(lab[x] - lab[par[x]]); D.insert(d);
                if (par[x] != R && d >= abs(lab[par[x]] - lab[par[par[x]]])) good = false; }
            good = good && (int)L.size() == n && (int)D.size() == m && *D.begin() == 1 && *D.rbegin() == m && lab[R] == 0;
            printf("%s nodes=%lld", good ? "ANCHOR" : "BADWITNESS", nodes); for (int i = 0; i < n; i++) printf(" %d", lab[i]); printf("\n");
        } else printf("%s nodes=%lld\n", nodes > cap ? "CAP" : "NOT", nodes);
        fflush(stdout);
    }
}
