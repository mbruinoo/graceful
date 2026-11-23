// Referee: for every rooted tree on s vertices (Beyer-Hedetniemi level sequences), search for a growth
// placement of its corona (or of the tree itself, mode "plain") with the root at label 0.
// Search = README Theorem 7 form: lengths N..1 in order, each new bracket hangs a not-yet-labelled child
// on a labelled vertex.  Every answer is re-verified from the definition.
// Usage: corona_solve s [corona|plain] [part nparts]
#include <bits/stdc++.h>
using namespace std;
int V, N; vector<int> par, cls, sz; vector<vector<int>> ch;
int lab[64], vert[64]; int nun[64]; // nun[u] = number of unlabelled children
long long nodes, limitN; bool rnd; mt19937 rng(12345);
string cstr(int x, map<string,int>& ids) {
    vector<string> c; for (int y : ch[x]) c.push_back(cstr(y, ids));
    sort(c.begin(), c.end()); string r = "("; for (auto& t : c) r += t; r += ")";
    if (!ids.count(r)) { int k = ids.size(); ids[r] = k; } cls[x] = ids[r]; return r;
}
int csz(int x) { sz[x] = 1; for (int y : ch[x]) sz[x] += csz(y); return sz[x]; }
struct Cand { int u, v, b; };
int rec(int c) { // 1 found, 0 exhausted, -1 limit
    if (c == 0) return 1;
    if (++nodes > limitN) return -1;
    Cand cs[256]; int nc = 0;
    for (int a = 0; a <= N; a++) {
        int u = vert[a]; if (u < 0 || nun[u] == 0) continue;
        for (int sg = -1; sg <= 1; sg += 2) {
            int b = a + sg * c; if (b < 0 || b > N || vert[b] >= 0) continue;
            int seen[16], ns = 0;
            for (int v : ch[u]) if (lab[v] < 0 && sz[v] <= c) {
                bool dup = false; for (int i = 0; i < ns; i++) if (seen[i] == cls[v]) dup = true;
                if (dup) continue; if (ns < 16) seen[ns++] = cls[v];
                cs[nc++] = {u, v, b};
            }
        }
    }
    if (rnd) shuffle(cs, cs + nc, rng);
    for (int i = 0; i < nc; i++) {
        Cand k = cs[i]; lab[k.v] = k.b; vert[k.b] = k.v; nun[k.u]--;
        int r = rec(c - 1);
        if (r == 1) return 1;
        lab[k.v] = -1; vert[k.b] = -1; nun[k.u]++;
        if (r == -1) return -1;
    }
    return 0;
}
bool verify() { // from the definition
    vector<int> seen(N + 1, 0);
    for (int v = 0; v < V; v++) { if (lab[v] < 0 || lab[v] > N || seen[lab[v]]) return false; seen[lab[v]] = 1; }
    if (lab[0] != 0) return false;
    vector<int> ea(N + 1, -1), eb(N + 1, -1);
    for (int v = 1; v < V; v++) { int l = abs(lab[v] - lab[par[v]]); if (l < 1 || l > N || ea[l] >= 0) return false; ea[l] = lab[v]; eb[l] = lab[par[v]]; }
    vector<int> used(N + 1, 0); used[ea[N]] = used[eb[N]] = 1;
    for (int c = N - 1; c >= 1; c--) { if (used[ea[c]] == used[eb[c]]) return false; used[ea[c]] = used[eb[c]] = 1; }
    return true;
}
int solve() {
    for (long long lim = 2000; lim <= 4000000; lim *= 4) {
        for (int i = 0; i <= N; i++) vert[i] = -1;
        for (int v = 0; v < V; v++) { lab[v] = -1; nun[v] = ch[v].size(); }
        lab[0] = 0; vert[0] = 0; nodes = 0; limitN = lim; rnd = true;
        int r = rec(N); if (r >= 0) return r;
    }
    for (int i = 0; i <= N; i++) vert[i] = -1;
    for (int v = 0; v < V; v++) { lab[v] = -1; nun[v] = ch[v].size(); }
    lab[0] = 0; vert[0] = 0; nodes = 0; limitN = LLONG_MAX; rnd = false;
    return rec(N);
}
int main(int argc, char** argv) {
    int s = atoi(argv[1]); bool corona = argc < 3 || string(argv[2]) == "corona";
    int part = argc > 4 ? atoi(argv[3]) : 0, nparts = argc > 4 ? atoi(argv[4]) : 1;
    vector<int> L(s); for (int i = 0; i < s; i++) L[i] = i;
    long long cnt = 0, fail = 0, bad = 0, idx = 0;
    while (true) {
        if (idx % nparts == part) {
            cnt++;
            V = corona ? 2 * s : s; N = V - 1;
            par.assign(V, -1); ch.assign(V, {}); cls.assign(V, 0); sz.assign(V, 0);
            for (int i = 1; i < s; i++) { int q = i - 1; while (L[q] != L[i] - 1) q--; par[i] = q; ch[q].push_back(i); }
            if (corona) for (int i = 0; i < s; i++) { par[s + i] = i; ch[i].push_back(s + i); }
            map<string,int> ids; cstr(0, ids); csz(0);
            int r = solve();
            if (r == 1) { if (!verify()) { bad++; printf("BAD VERIFY\n"); } }
            else { fail++; printf("NOT ANCHORED: levels"); for (int x : L) printf(" %d", x); printf("\n"); }
        }
        idx++;
        int p = s - 1; while (p > 0 && L[p] <= 1) p--;
        if (p <= 0) break;
        int q = p - 1; while (L[q] != L[p] - 1) q--;
        for (int i = p; i < s; i++) L[i] = L[i - (p - q)];
    }
    printf("s=%d mode=%s part %d/%d: rooted trees seen %lld (of %lld generated), without anchored growth placement %lld, bad verifications %lld\n",
           s, corona ? "corona" : "plain", part, nparts, cnt, idx, fail, bad);
}
