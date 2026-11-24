// spare.cpp -- relaxed growth labelings with a given slack, for one rooted tree per input line.
//
// Definition (README section 16 / src/attack/asymptotic): a relaxed growth labeling of (T,r) with range N is an
// injective f: V -> {1..N}, f(r)=1, pairwise distinct edge lengths, lengths strictly decreasing along every
// path away from r.  Here labels are written 0..N-1 with f(r)=0 (subtract 1).  slack s means N = n+s.
//
// Search: complete longest-first backtracking.  Any relaxed growth labeling can be built by taking its edges in
// decreasing length, each new edge hanging a new vertex on a placed one; conversely anything built that way is
// one.  So at length l we either hang a pending child on a placed vertex at distance l, or leave l unused
// (allowed while #lengths left >= #edges left).  Children with the same rooted-subtree code are interchangeable.
// Forward check (sound, see dead()): applied only when every unplaced vertex is a leaf; then the set of possible
// parents is final, so a length no parent can use now must stay unused, and a free cell no parent can reach is lost.
// "no solution" (NONE) is exact when the node cap is not hit; CAP means undecided.
//
// input line:  n root a1 b1 a2 b2 ... (n-1 edges, vertices 0..n-1)      [optional leading name token "#name"]
// usage: spare slack [nodecap=0 (none)] [order=0] [last]
//   order 0: try place before skip; 1: skip first; >= 2: place first, parents tried in random order (seed = order)
//   4th argument present: each input line ends with a vertex that must be the one hung by the length-1 bracket
//        spare all n slack part mod [cap] : every free tree on n vertices (src/treegen.h), every root
// output per line: name, n, root, slack, FOUND labels... | NONE | CAP, nodes
#include <bits/stdc++.h>
#include "../../treegen.h"
using namespace std;
static int n, N, root; static vector<vector<int>> ch; static vector<int> par_, code_, isleafonly;
static int lab[400]; static bool used[800]; static vector<vector<int>> pend; static long long nodes, cap; static int order_;
static int LASTV_ = -1;
static mt19937 rng_(12345);
static int unplacedInternal;   // number of unplaced vertices that have children
static vector<int> act;        // placed vertices with pending children

// sound prune, used only when every unplaced vertex is a leaf (then the set of parents is final):
// each remaining length l' < L must be skipped or used by some parent v with lab[v]+-l' free; count lengths with
// no such option; they must all be skipped.  Likewise count free labels reachable; need >= rem.
static bool dead(int L, int rem) {
    if (unplacedInternal) return false;
    int skips = (L - 1) - rem, bad = 0;
    for (int l = L - 1; l >= 1; --l) {
        bool ok = false;
        for (int v : act) { int y = lab[v]; if ((y + l < N && !used[y + l]) || (y - l >= 0 && !used[y - l])) { ok = true; break; } }
        if (!ok && ++bad > skips) return true;
    }
    int reach = 0;
    for (int x = 0; x < N; x++) if (!used[x]) { for (int v : act) { int d = abs(x - lab[v]); if (d >= 1 && d < L) { reach++; break; } } }
    return reach < rem;
}
static bool dfs(int L, int rem) {       // lengths < L are available; rem edges still to place
    if (rem == 0) return true;
    if (L - 1 < rem) return false;
    if (cap && nodes > cap) return false;
    nodes++;
    if (dead(L, rem)) return false;
    int l = L - 1;
    for (int pass = 0; pass < 2; pass++) {
        bool doskip = (pass == 0) == (order_ == 1);
        if (doskip) { if (l - 1 >= rem && dfs(l, rem)) return true; if (cap && nodes > cap) return false; continue; }
        vector<int> snapshot = act;
        if (order_ >= 2) shuffle(snapshot.begin(), snapshot.end(), rng_);   // randomised parent order (restarts)
        for (int v : snapshot) {
            int y = lab[v];
            for (int sgn = -1; sgn <= 1; sgn += 2) {
                int x = y + sgn * l; if (x < 0 || x >= N || used[x]) continue;
                int lastcode = -1;
                for (size_t i = 0; i < pend[v].size(); i++) {
                    int c = pend[v][i]; if (code_[c] == lastcode) continue; lastcode = code_[c];
                    if (LASTV_ >= 0 && ((c == LASTV_) != (l == 1))) continue;
                    pend[v].erase(pend[v].begin() + i); lab[c] = x; used[x] = true;
                    bool vgone = pend[v].empty(); if (vgone) act.erase(find(act.begin(), act.end(), v));
                    bool cin = !ch[c].empty(); if (cin) { act.push_back(c); unplacedInternal--; }
                    bool ok = dfs(l, rem - 1);
                    if (ok) return true;
                    if (cin) unplacedInternal++;
                    act = snapshot;                 // restore exactly (deeper calls may have reordered it)
                    used[x] = false; lab[c] = -1; pend[v].insert(pend[v].begin() + i, c);
                    if (cap && nodes > cap) return false;
                }
            }
        }
    }
    return false;
}
static bool verify() {   // from the definition
    vector<char> sl(N, 0), se(N, 0); if (lab[root] != 0) return false;
    for (int v = 0; v < n; v++) { if (lab[v] < 0 || lab[v] >= N || sl[lab[v]]) return false; sl[lab[v]] = 1; }
    for (int v = 0; v < n; v++) if (v != root) { int p = par_[v], d = abs(lab[v] - lab[p]); if (d < 1 || se[d]) return false; se[d] = 1;
        if (p != root) { int dp = abs(lab[p] - lab[par_[p]]); if (!(d < dp)) return false; } }
    return true;
}

static map<vector<int>, int> codes;
#define LASTV LASTV_
//   // if >= 0: this vertex must be the one hung with length 1 (and nothing else may use length 1)
// returns 1 found (verified), 0 none (exact), -1 cap hit, -2 verify failure
static int solve_tree(const vector<vector<int>>& adj, int s) {
    ch.assign(n, {}); par_.assign(n, -1); code_.assign(n, 0); codes.clear();   // codes are only compared inside one rooted tree
    vector<int> ordv = {root};
    for (size_t i = 0; i < ordv.size(); i++) { int v = ordv[i]; for (int u : adj[v]) if (u != par_[v]) { par_[u] = v; ch[v].push_back(u); ordv.push_back(u); } }
    for (int i = n - 1; i >= 0; i--) { int v = ordv[i]; vector<int> k; for (int c : ch[v]) k.push_back(code_[c]); sort(k.begin(), k.end());
        if (v == LASTV) k.push_back(-7);
        auto it = codes.find(k); if (it == codes.end()) it = codes.insert({k, (int)codes.size() + 1}).first; code_[v] = it->second; }
    N = n + s; for (int v = 0; v < n; v++) lab[v] = -1; memset(used, 0, sizeof used); lab[root] = 0; used[0] = true;
    pend.assign(n, {}); for (int v = 0; v < n; v++) { pend[v] = ch[v]; sort(pend[v].begin(), pend[v].end(), [&](int a, int b) { return code_[a] < code_[b]; }); }
    act.clear(); if (!ch[root].empty()) act.push_back(root);
    unplacedInternal = 0; for (int v = 0; v < n; v++) if (v != root && !ch[v].empty()) unplacedInternal++;
    nodes = 0; bool ok = dfs(N, n - 1);
    if (ok) return verify() ? 1 : -2;
    return (cap && nodes > cap) ? -1 : 0;
}
int main(int argc, char** argv) {
    if (string(argv[1]) == "all") {          // spare all n slack part mod [cap]: every free tree on n vertices (src/treegen.h), every root
        n = atoi(argv[2]); int s = atoi(argv[3]), part = atoi(argv[4]), mod = atoi(argv[5]); cap = argc > 6 ? atoll(argv[6]) : 0; order_ = 0;
        TreeGen g(n); vector<int> p0; long long trees = 0, pairs = 0, cnt[4] = {0, 0, 0, 0}, maxnodes = 0, idx = 0;
        while (g.next()) {
            if ((idx++) % mod != part) continue;
            trees++; g.parents(p0);
            vector<vector<int>> adj(n); for (int i = 1; i < n; i++) { adj[i].push_back(p0[i]); adj[p0[i]].push_back(i); }
            for (root = 0; root < n; root++) {
                int r = solve_tree(adj, s); pairs++; cnt[r == 1 ? 0 : r == 0 ? 1 : r == -1 ? 2 : 3]++; maxnodes = max(maxnodes, nodes);
                if (r != 1) { printf("%s tree#%lld root=%d parents:", r == 0 ? "NONE" : r == -1 ? "CAP" : "VERIFYFAIL", idx - 1, root); for (int i = 1; i < n; i++) printf(" %d", p0[i]); printf("\n"); fflush(stdout); }
            }
        }
        printf("n=%d slack=%d part %d/%d: trees=%lld (tree,root) pairs=%lld found(verified)=%lld none=%lld cap=%lld verifyfail=%lld maxnodes=%lld\n", n, s, part, mod, trees, pairs, cnt[0], cnt[1], cnt[2], cnt[3], maxnodes);
        return 0;
    }
    int s = atoi(argv[1]); cap = argc > 2 ? atoll(argv[2]) : 0; order_ = argc > 3 ? atoi(argv[3]) : 0; rng_.seed(order_);
    bool wantlast = argc > 4;    // 4th argument present: input lines carry an extra final token = the vertex that must get length 1
    string line;
    while (getline(cin, line)) {
        istringstream is(line); string name = "-"; if (line.size() && line[0] == '#') is >> name;
        if (!(is >> n >> root)) continue;
        vector<vector<int>> adj(n); for (int i = 0; i < n - 1; i++) { int a, b; is >> a >> b; adj[a].push_back(b); adj[b].push_back(a); }
        LASTV = -1; if (wantlast) is >> LASTV;
        int r = solve_tree(adj, s);
        if (r == 1) { printf("%s n=%d root=%d slack=%d FOUND nodes=%lld labels:", name.c_str(), n, root, s, nodes); for (int v = 0; v < n; v++) printf(" %d", lab[v]); printf("\n"); }
        else printf("%s n=%d root=%d slack=%d %s nodes=%lld\n", name.c_str(), n, root, s, r == 0 ? "NONE" : r == -1 ? "CAP" : "VERIFYFAIL", nodes);
        fflush(stdout);
    }
}
