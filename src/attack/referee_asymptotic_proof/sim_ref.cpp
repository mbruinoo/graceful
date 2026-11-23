// Referee re-implementation of the one-pass longest-first process of claim 1 (written from the
// statement, plain arrays, no bitset tricks).  Policies: 0 = uniform random candidate + random child,
// 1 = candidate whose parent has the pending child with the largest subtree (ties random).
// Prufer trees, centroid root.  Also records, for failed runs, where stalled parents / free labels sit.
// usage: sim_ref n trials policy seed slack...
#include <bits/stdc++.h>
using namespace std;
static mt19937_64 rng;
int main(int argc, char** argv) {
    int n = atoi(argv[1]), trials = atoi(argv[2]), pol = atoi(argv[3]); rng.seed(atoll(argv[4]));
    vector<int> slacks; for (int i = 5; i < argc; i++) slacks.push_back(atoi(argv[i]));
    vector<int> succ(slacks.size(), 0); long long bad = 0;
    vector<long long> stP(slacks.size(), 0), stP10(slacks.size(), 0), stP20(slacks.size(), 0), fr(slacks.size(), 0), fr10(slacks.size(), 0), fr20(slacks.size(), 0); vector<vector<int>> remv(slacks.size());
    for (int t = 0; t < trials; t++) {
        vector<int> p(n - 2), deg(n, 1); for (auto& x : p) { x = rng() % n; deg[x]++; }
        vector<vector<int>> adj(n); set<int> lv; for (int i = 0; i < n; i++) if (deg[i] == 1) lv.insert(i);
        for (int x : p) { int l = *lv.begin(); lv.erase(lv.begin()); adj[l].push_back(x); adj[x].push_back(l); if (--deg[x] == 1) lv.insert(x); }
        { int a = *lv.begin(), b = *lv.rbegin(); adj[a].push_back(b); adj[b].push_back(a); }
        vector<int> par(n), sz(n), ord; vector<vector<int>> ch(n);
        auto rootat = [&](int r) { ord = {r}; par.assign(n, -1); sz.assign(n, 1); for (auto& c : ch) c.clear();
            for (size_t i = 0; i < ord.size(); i++) { int v = ord[i]; for (int u : adj[v]) if (u != par[v]) { par[u] = v; ch[v].push_back(u); ord.push_back(u); } }
            for (int i = n - 1; i > 0; i--) sz[par[ord[i]]] += sz[ord[i]]; };
        rootat(0); int r = 0; for (;;) { int nx = -1; for (int c : ch[r]) if (2 * sz[c] > n) nx = c; if (nx < 0) break; r = nx; } rootat(r);
        for (size_t si = 0; si < slacks.size(); si++) {
            int N = n + slacks[si]; vector<int> lab(n, 0), at(N + 2, -1); vector<vector<int>> pend = ch; vector<int> front;
            vector<double> key(n); for (int v = 0; v < n; v++) key[v] = sz[v] + (rng() % 1000000) / 2000001.0;
            lab[r] = 1; at[1] = r; front.push_back(r); int L = N, rem = n - 1; bool ok = true;
            while (rem > 0) {
                int l; vector<pair<int,int>> cand;   // (parent, label)
                for (l = L - 1; l >= rem; --l) { for (int v : front) if (!pend[v].empty()) for (int sg = -1; sg <= 1; sg += 2) { int x = lab[v] + sg * l; if (x >= 1 && x <= N && at[x] < 0) cand.push_back({v, x}); } if (!cand.empty()) break; }
                if (cand.empty()) { ok = false; break; }
                int v, x, c;
                if (pol == 0) { auto pr = cand[rng() % cand.size()]; v = pr.first; x = pr.second; int j = rng() % pend[v].size(); c = pend[v][j]; pend[v].erase(pend[v].begin() + j); }
                else { double bk = -1; int bi = 0, bj = 0; for (size_t i = 0; i < cand.size(); i++) { int u = cand[i].first; for (size_t j = 0; j < pend[u].size(); j++) if (key[pend[u][j]] > bk) { bk = key[pend[u][j]]; bi = i; bj = j; } }
                    v = cand[bi].first; x = cand[bi].second; c = pend[v][bj]; pend[v].erase(pend[v].begin() + bj); }
                lab[c] = x; at[x] = c; if (!pend[c].empty()) front.push_back(c); L = l; rem--;
            }
            if (ok) { // verify from the definition
                set<int> Ls, Es; bool g = lab[r] == 1; for (int v = 0; v < n; v++) g = g && lab[v] >= 1 && lab[v] <= N && Ls.insert(lab[v]).second;
                for (int v = 0; v < n; v++) if (v != r) { int d = abs(lab[v] - lab[par[v]]); g = g && d >= 1 && Es.insert(d).second; if (par[v] != r) g = g && d < abs(lab[par[v]] - lab[par[par[v]]]); }
                if (g) succ[si]++; else bad++;
            } else { remv[si].push_back(rem);
                for (int v : front) if (!pend[v].empty()) { stP[si]++; int d = min(lab[v] - 1, N - lab[v]); if (d < 0.1 * N) stP10[si]++; if (d < 0.2 * N) stP20[si]++; }
                for (int x = 1; x <= N; x++) if (at[x] < 0) { fr[si]++; int d = min(x - 1, N - x); if (d < 0.1 * N) fr10[si]++; if (d < 0.2 * N) fr20[si]++; } }
        }
    }
    for (size_t si = 0; si < slacks.size(); si++) { printf("prufer n=%d policy=%d slack=%d success %d/%d verify_failures=%lld", n, pol, slacks[si], succ[si], trials, bad);
        if (!remv[si].empty()) { sort(remv[si].begin(), remv[si].end()); printf(" | failed runs %zu: stalled parents %lld (outer10%% %.1f%%, outer20%% %.1f%%), free labels %lld (outer10%% %.2f%%, outer20%% %.1f%%), median unplaced %d", remv[si].size(), stP[si], 100.0 * stP10[si] / max(1LL, stP[si]), 100.0 * stP20[si] / max(1LL, stP[si]), fr[si], 100.0 * fr10[si] / max(1LL, fr[si]), 100.0 * fr20[si] / max(1LL, fr[si]), remv[si][remv[si].size() / 2]); }
        printf("\n"); }
}
