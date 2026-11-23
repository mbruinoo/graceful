// referee re-implementation of the one-pass longest-first process (claim 1).
// Plain arrays, no bitset tricks; written from the process description.
// usage: proc TYPE n TRIALS POLICY ROOT SEED MODE args...
//   MODE grid s1 s2 ...  : success counts at slack s_i (same tree per trial)
//   MODE min             : least slack by doubling + bisection
//   MODE stall s         : diagnose failed runs at slack s
//   POLICY 0 uniform candidate/random child, 1 largest subtree, 6 critical parents first (THETA env)
#include <bits/stdc++.h>
using namespace std;
static mt19937_64 rng;
static int rnd(int m) { return (int)(rng() % (unsigned long long)m); }
static int n, root, theta = 0;
static vector<vector<int>> adj, ch;
static vector<int> par, sz;
static void gen(const string& t) {
    adj.assign(n, {});
    auto E = [&](int a, int b) { adj[a].push_back(b); adj[b].push_back(a); };
    if (t == "prufer") {
        if (n == 2) { E(0, 1); return; }
        vector<int> p(n - 2), deg(n, 1); for (auto& x : p) { x = rnd(n); deg[x]++; }
        priority_queue<int, vector<int>, greater<int>> lv; for (int i = 0; i < n; i++) if (deg[i] == 1) lv.push(i);
        for (int x : p) { int l = lv.top(); lv.pop(); E(l, x); if (--deg[x] == 1) lv.push(x); }
        int a = lv.top(); lv.pop(); E(a, lv.top());
    } else if (t == "recursive") { for (int v = 1; v < n; v++) E(v, rnd(v)); }
    else if (t == "path") { for (int v = 1; v < n; v++) E(v, v - 1); }
    else if (t == "star") { for (int v = 1; v < n; v++) E(v, 0); }
    else if (t == "cbin") { for (int v = 1; v < n; v++) E(v, (v - 1) / 2); }
    else if (t == "cater") { int s = n / 2; for (int v = 1; v < s; v++) E(v, v - 1); for (int v = s; v < n; v++) E(v, rnd(s)); }
    else if (t.rfind("spider", 0) == 0) { int k = atoi(t.c_str() + 6); for (int v = 1; v < n; v++) E(v, v <= k ? 0 : v - k); }
    else if (t.rfind("comb", 0) == 0) { int L = atoi(t.c_str() + 4); int s = n / (L + 1); if (s < 1) s = 1; for (int v = 1; v < s; v++) E(v, v - 1); for (int v = s; v < n; v++) { int j = v - s; E(v, j < s ? j : v - s); } }
    else { fprintf(stderr, "type?\n"); exit(1); }
}
static void rootat(int r) {
    root = r; ch.assign(n, {}); par.assign(n, -1); sz.assign(n, 1);
    vector<int> o = {r};
    for (size_t i = 0; i < o.size(); i++) { int v = o[i]; for (int u : adj[v]) if (u != par[v]) { par[u] = v; ch[v].push_back(u); o.push_back(u); } }
    for (int i = n - 1; i > 0; i--) sz[par[o[i]]] += sz[o[i]];
}
static void chooseRoot(char m) {
    rootat(0);
    if (m == 'c') { int r = 0; for (;;) { int nx = -1; for (int c : ch[r]) if (2 * sz[c] > n) nx = c; if (nx < 0) break; r = nx; } rootat(r); }
    else if (m == 'r') rootat(rnd(n));
    else if (m == 'l') { vector<int> lv; for (int v = 0; v < n; v++) if (adj[v].size() == 1) lv.push_back(v); rootat(lv[rnd(lv.size())]); }
}
static vector<int> lab; static int N;
static bool verify() {
    vector<char> sl(N + 1, 0), se(N + 1, 0);
    if (lab[root] != 1) return false;
    for (int v = 0; v < n; v++) { if (lab[v] < 1 || lab[v] > N || sl[lab[v]]) return false; sl[lab[v]] = 1; }
    for (int v = 0; v < n; v++) if (v != root) { int d = abs(lab[v] - lab[par[v]]); if (d < 1 || se[d]) return false; se[d] = 1;
        if (par[v] != root && d >= abs(lab[par[v]] - lab[par[par[v]]])) return false; }
    return true;
}
// stall info
static vector<int> stallParents, stallFree; static int stallRem;
static bool run(int policy) {
    vector<char> used(N + 2, 0); lab.assign(n, 0);
    vector<vector<int>> pend = ch; vector<double> jit(n);
    for (int v = 0; v < n; v++) jit[v] = (rng() >> 11) * (1.0 / 9007199254740992.0) * 0.5;
    vector<int> front; vector<int> pref; // prefix count of used labels for policy 6 (recomputed lazily)
    lab[root] = 1; used[1] = 1; if (!pend[root].empty()) front.push_back(root);
    int L = N, rem = n - 1;
    auto fail = [&]() { stallParents.clear(); stallFree.clear(); stallRem = rem; for (int v : front) stallParents.push_back(lab[v]); for (int y = 1; y <= N; y++) if (!used[y]) stallFree.push_back(y); return false; };
    while (rem > 0) {
        int l; vector<pair<int,int>> cand; // (parent, new label)
        for (l = L - 1; l >= rem; l--) {
            for (int v : front) { int y = lab[v]; if (y + l <= N && !used[y + l]) cand.push_back({v, y + l}); if (y - l >= 1 && !used[y - l]) cand.push_back({v, y - l}); }
            if (!cand.empty()) break;
        }
        if (cand.empty()) return fail();
        int bv = -1, bx = -1, bc = -1;
        if (policy == 0) { auto c = cand[rnd(cand.size())]; bv = c.first; bx = c.second; bc = rnd(pend[bv].size()); }
        else {
            if (policy == 6) { pref.assign(N + 1, 0); for (int y = 1; y <= N; y++) pref[y] = pref[y - 1] + (used[y] ? 0 : 1); }
            auto freein = [&](int a, int b) { if (a < 1) a = 1; if (b > N) b = N; return a > b ? 0 : pref[b] - pref[a - 1]; };
            double bk = -1e300;
            for (auto& c : cand) { int v = c.first; int ci = 0; double k = -1;
                for (int i = 0; i < (int)pend[v].size(); i++) { double kk = sz[pend[v][i]] + jit[pend[v][i]]; if (kk > k) { k = kk; ci = i; } }
                if (policy == 6) { int y = lab[v], lo = max(rem - 1, 1); int reach = freein(y - l + 1, y - lo) + freein(y + lo, y + l - 1) - 1; int margin = reach - (int)pend[v].size(); if (margin <= theta) k += 1e7 - 1e3 * margin; }
                k += 1e-9 * (rng() % 1000);   // random side when both free
                if (k > bk) { bk = k; bv = v; bx = c.second; bc = ci; } }
        }
        int c = pend[bv][bc]; pend[bv][bc] = pend[bv].back(); pend[bv].pop_back();
        if (pend[bv].empty()) front.erase(find(front.begin(), front.end(), bv));
        lab[c] = bx; used[bx] = 1; if (!pend[c].empty()) front.push_back(c);
        L = l; rem--;
    }
    return true;
}
int main(int argc, char** argv) {
    string type = argv[1]; n = atoi(argv[2]); int trials = atoi(argv[3]), policy = atoi(argv[4]); char rm = argv[5][0];
    rng.seed(atoll(argv[6])); string mode = argv[7]; if (getenv("THETA")) theta = atoi(getenv("THETA"));
    long long bad = 0;
    auto tryS = [&](int s) { N = n + s; bool r = run(policy); if (r && !verify()) { bad++; r = false; } return r; };
    if (mode == "grid") {
        vector<int> sl; for (int i = 8; i < argc; i++) sl.push_back(atoi(argv[i])); vector<int> succ(sl.size(), 0);
        for (int t = 0; t < trials; t++) { gen(type); chooseRoot(rm); for (size_t i = 0; i < sl.size(); i++) succ[i] += tryS(sl[i]); }
        printf("%s n=%d policy=%d root=%c:", type.c_str(), n, policy, rm);
        for (size_t i = 0; i < sl.size(); i++) printf("  slack %d: %d/%d", sl[i], succ[i], trials); printf("  verify_failures=%lld\n", bad);
    } else if (mode == "min") {
        vector<int> mins;
        for (int t = 0; t < trials; t++) { gen(type); chooseRoot(rm);
            int res; if (tryS(0)) res = 0; else { int hi = 1; while (!tryS(hi)) hi *= 2; int lo = hi / 2; while (hi - lo > 1) { int m = (lo + hi) / 2; if (tryS(m)) hi = m; else lo = m; } res = hi; }
            mins.push_back(res); }
        sort(mins.begin(), mins.end()); double mean = accumulate(mins.begin(), mins.end(), 0.0) / trials;
        printf("%s n=%d policy=%d root=%c trials=%d least slack: min=%d median=%d max=%d mean=%.1f mean/n=%.4f median/n=%.4f verify_failures=%lld\n", type.c_str(), n, policy, rm, trials, mins[0], mins[trials / 2], mins.back(), mean, mean / n, mins[trials / 2] / (double)n, bad);
    } else if (mode == "stall") {
        int s = atoi(argv[8]); long long P = 0, P10 = 0, P20 = 0, F = 0, F10 = 0, F20 = 0; vector<int> rems; int fails = 0, runs = 0;
        while (fails < trials) { gen(type); chooseRoot(rm); runs++; if (tryS(s)) continue; fails++; rems.push_back(stallRem);
            for (int y : stallParents) { P++; double q = (y - 0.5) / N; if (q < .1 || q > .9) P10++; if (q < .2 || q > .8) P20++; }
            for (int y : stallFree) { F++; double q = (y - 0.5) / N; if (q < .1 || q > .9) F10++; if (q < .2 || q > .8) F20++; } }
        sort(rems.begin(), rems.end());
        printf("%s n=%d policy=%d slack=%d: %d failed of %d runs; stalled parents %lld: outer10%%=%.1f%% outer20%%=%.1f%%; free labels %lld: outer10%%=%.2f%% outer20%%=%.1f%%; median unplaced=%d\n",
               type.c_str(), n, policy, s, fails, runs, P, 100.0 * P10 / P, 100.0 * P20 / P, F, 100.0 * F10 / F, 100.0 * F20 / F, rems[fails / 2]);
    }
}
