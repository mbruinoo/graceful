// referee (brute-force lens) for claim 0 and the window lemma of claim 1.
// Written from the README definitions; does not use the claimant's code.
//
// relaxed growth labeling of (T,r), range N: injective f:V->{1..N}, f(r)=1,
// edge lengths pairwise distinct, strictly decreasing away from r.
//
// usage: relax MODE MAXSLACK < trees
//   MODE = search : longest-first complete backtracking, least slack per (T,r)
//   MODE = brute  : enumerate ALL injective f with f(r)=1 (no pruning), test the
//                   definition on each; also tests the window lemma on every
//                   relaxed growth labeling found, for every slack 0..MAXSLACK.
#include <bits/stdc++.h>
using namespace std;
static int n, N, root;
static vector<int> adj[32];
static int par[32], lab[32], sub[32];
static vector<int> ch[32];
static long long canon[32];
static map<vector<long long>, long long> canonMap;
static void dfs(int v, int p) {
    par[v] = p; ch[v].clear(); sub[v] = 1;
    vector<long long> ks;
    for (int w : adj[v]) if (w != p) { dfs(w, v); ch[v].push_back(w); sub[v] += sub[w]; ks.push_back(canon[w]); }
    sort(ks.begin(), ks.end());
    auto it = canonMap.find(ks);
    if (it == canonMap.end()) it = canonMap.emplace(ks, (long long)canonMap.size()).first;
    canon[v] = it->second;
}
// independent check straight from the definition
static bool verify() {
    set<int> L, S;
    for (int v = 0; v < n; v++) { if (lab[v] < 1 || lab[v] > N) return false; if (!L.insert(lab[v]).second) return false; }
    if (lab[root] != 1) return false;
    for (int v = 0; v < n; v++) if (v != root) {
        int l = abs(lab[v] - lab[par[v]]);
        if (l < 1 || !S.insert(l).second) return false;
        int p = par[v];
        if (p != root && abs(lab[p] - lab[par[p]]) <= l) return false;
    }
    return true;
}
static unsigned used; static bool placed[32];
static long long nodes;
static bool rec(int prevL, int remaining) {
    if (remaining == 0) return true;
    nodes++;
    // prune: every placed vertex with k unplaced children needs k free labels at distance < prevL
    for (int p = 0; p < n; p++) if (placed[p]) {
        int k = 0; for (int c : ch[p]) if (!placed[c]) k++;
        if (!k) continue;
        int f = 0;
        for (int l = 1; l < prevL; l++) {
            if (lab[p] + l <= N && !(used >> (lab[p] + l) & 1)) f++;
            if (lab[p] - l >= 1 && !(used >> (lab[p] - l) & 1)) f++;
        }
        if (f < k) return false;
    }
    for (int l = prevL - 1; l >= remaining; l--) {
        for (int p = 0; p < n; p++) if (placed[p]) {
            for (int s = -1; s <= 1; s += 2) {
                int y = lab[p] + s * l;
                if (y < 1 || y > N || (used >> y & 1)) continue;
                long long seen[32]; int ns = 0;
                for (int c : ch[p]) if (!placed[c]) {
                    bool dup = false; for (int i = 0; i < ns; i++) if (seen[i] == canon[c]) dup = true;
                    if (dup) continue; seen[ns++] = canon[c];
                    placed[c] = true; lab[c] = y; used |= 1u << y;
                    if (rec(l, remaining - 1)) return true;
                    placed[c] = false; used &= ~(1u << y);
                }
            }
        }
    }
    return false;
}
static bool search(int slack) {
    N = n + slack; memset(placed, 0, sizeof placed); used = 2; placed[root] = true; lab[root] = 1;
    return rec(N, n - 1);
}
// ---- brute mode ----
static long long cntLab, winFail;
static vector<int> order_; // vertices other than root
static void windowCheck() {
    // for every pair of edges (length L) and (length l < L, parent label y, child label x): x in (y-L, y+L)
    // and for each edge: min endpoint <= N-l, max endpoint >= l+1
    for (int v = 0; v < n; v++) if (v != root) {
        int l = abs(lab[v] - lab[par[v]]);
        int mn = min(lab[v], lab[par[v]]), mx = max(lab[v], lab[par[v]]);
        if (!(mn <= N - l && mx >= l + 1)) winFail++;
        for (int w = 0; w < n; w++) if (w != root) {
            int L = abs(lab[w] - lab[par[w]]);
            if (l < L) { int y = lab[par[v]], x = lab[v]; if (!(x > y - L && x < y + L)) winFail++; }
        }
    }
}
static bool bruteFound;
static void brute(int i) {
    if (i == (int)order_.size()) { if (verify()) { bruteFound = true; cntLab++; windowCheck(); } return; }
    for (int y = 2; y <= N; y++) if (!(used >> y & 1)) { used |= 1u << y; lab[order_[i]] = y; brute(i + 1); used &= ~(1u << y); }
}
int main(int argc, char** argv) {
    string mode = argv[1]; int maxSlack = atoi(argv[2]);
    string line; long long trees = 0, pairs = 0, verFail = 0;
    map<int, long long> least, leastOrb; long long allAnch = 0, noAnchorTree = 0;
    map<int,long long> degNeed; long long leafNbr = 0, leafNbrNeed = 0;
    long long mismatch = 0;
    while (getline(cin, line)) {
        istringstream is(line); is >> n; for (int i = 0; i < n; i++) adj[i].clear();
        int u, v; int m = 0; while (is >> u >> v) { adj[u].push_back(v); adj[v].push_back(u); m++; }
        if (m != n - 1) { fprintf(stderr, "bad tree\n"); return 1; }
        trees++; int best = 99; bool all0 = true;
        set<long long> orbitsSeen; // rooted canonical form identifies the orbit of the root
        for (root = 0; root < n; root++) {
            dfs(root, -1); pairs++;
            int need = -1;
            if (mode == "search") {
                for (int s = 0; s <= maxSlack; s++) if (search(s)) { need = s; if (!verify()) verFail++; break; }
            } else {
                order_.clear(); for (int x = 0; x < n; x++) if (x != root) order_.push_back(x);
                for (int s = 0; s <= maxSlack; s++) {
                    N = n + s; used = 2; lab[root] = 1; bruteFound = false; brute(0);
                    if (bruteFound && need < 0) need = s;
                    bool sr = search(s); if (sr && !verify()) verFail++;
                    N = n + s;
                    if (sr != bruteFound) mismatch++;
                }
            }
            if (need < 0) need = 99;
            least[need]++; best = min(best, need); if (need) all0 = false;
            if (orbitsSeen.insert(canon[root]).second) leastOrb[need]++;
            bool ln = false; for (int w : adj[root]) if (adj[w].size() == 1) ln = true;
            if (ln) { leafNbr++; if (need) leafNbrNeed++; }
            if (need) { degNeed[adj[root].size()]++;
                if (need >= 2 || n <= 7) { printf("  n=%d need=%d root=%d edges:", n, need, root); for (int a = 0; a < n; a++) for (int b : adj[a]) if (a < b) printf(" %d-%d", a, b); printf("\n"); } }
        }
        if (all0) allAnch++; if (best > 0) noAnchorTree++;
    }
    printf("n=%d mode=%s trees=%lld pairs=%lld verify_failures=%lld", n, mode.c_str(), trees, pairs, verFail);
    if (mode == "brute") printf(" search_vs_brute_mismatch=%lld labelings=%lld window_failures=%lld", mismatch, cntLab, winFail);
    printf("\n  least slack (per vertex):"); for (auto& kv : least) printf(" %d:%lld", kv.first, kv.second);
    printf("\n  least slack (per root orbit):"); for (auto& kv : leastOrb) printf(" %d:%lld", kv.first, kv.second);
    printf("\n  trees all-slack-0=%lld  trees with no slack-0 root=%lld  leaf-neighbour roots=%lld needing slack=%lld\n  degree of roots needing slack:", allAnch, noAnchorTree, leafNbr, leafNbrNeed);
    for (auto& kv : degNeed) printf(" deg%d:%lld", kv.first, kv.second); printf("  search_nodes=%lld\n", nodes);
}
