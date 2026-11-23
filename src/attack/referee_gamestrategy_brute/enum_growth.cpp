// Referee: enumerate ALL growth placements on n vertices straight from README section 1
// (brackets n-1..1, each with exactly one foot already used).  For every placement whose tree
// has diameter 4 and whose label-1 vertex is a hub (non-centre, non-leaf vertex... or a
// centre-neighbour with >=1 leaves), record shape (s_root | sorted other sizes) and whether
// the placement is an "all-up comb" (claim 2).  Then list every diameter-4 shape on n vertices
// and report: is a LARGEST hub an anchor?  is there an all-up comb at a largest hub?
// Usage: enum_growth n
#include <bits/stdc++.h>
using namespace std;
int n, m;
int posOf[32]; // posOf[k] = lower foot (labels 0..m) of bracket k
map<vector<int>, int> seen; // key: s_root, then sorted desc others ; value bit0 anchor, bit1 allup
long long total = 0;
void analyze() {
    total++;
    static vector<int> adj[32];
    for (int v = 0; v <= m; v++) adj[v].clear();
    for (int k = 1; k <= m; k++) { int a = posOf[k], b = a + k; adj[a].push_back(b); adj[b].push_back(a); }
    // root = label 0
    int c = -1, rl = 0;
    for (int v : adj[0]) { if (adj[v].size() > 1) { if (c >= 0) return; c = v; } else rl++; }
    if (c < 0 || rl == 0) return; // root must be a hub with >=1 leaf and one non-leaf nbr
    vector<int> others; bool allup = true; int pos = 0;
    for (int h : adj[c]) {
        if (h == 0) continue;
        int s = 0;
        for (int x : adj[h]) { if (x == c) continue; if (adj[x].size() != 1) return; s++;
            if (!(x > h && x < c)) allup = false; }
        if (h > c) allup = false;
        if (s > 0) pos++;
        others.push_back(s);
    }
    if (pos == 0) return; // diameter < 4
    sort(others.rbegin(), others.rend());
    vector<int> key; key.push_back(rl); for (int s : others) key.push_back(s);
    seen[key] |= 1 | (allup ? 2 : 0);
}
void rec(int k, unsigned used) {
    if (k == 0) { analyze(); return; }
    for (int a = 0; a + k <= m; a++) {
        bool ua = used >> a & 1, ub = used >> (a + k) & 1;
        if (ua == ub) continue;
        posOf[k] = a;
        rec(k - 1, used | 1u << a | 1u << (a + k));
    }
}
vector<vector<int>> parts;
void gen(int rem, int mx, int cnt, vector<int>& cur) { // partitions into parts s+1, i.e. k parts s_i>=0 with sum(s_i+1)=rem
    if (rem == 0) { parts.push_back(cur); return; }
    for (int s = min(mx, rem - 1); s >= 0; s--) { cur.push_back(s); gen(rem - s - 1, s, cnt + 1, cur); cur.pop_back(); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); m = n - 1;
    posOf[m] = 0;
    rec(m - 1, 1u | 1u << m);
    vector<int> cur; gen(n - 1, n, 0, cur);
    int trees = 0, noAnchor = 0, noAllup = 0;
    for (auto& s : parts) {
        if (s.size() < 2 || s[1] == 0) continue; // need two hubs with leaves
        trees++;
        vector<int> key(s); // s[0] is a largest; root = largest
        auto it = seen.find(key);
        int f = it == seen.end() ? 0 : it->second;
        if (!(f & 1)) { noAnchor++; printf("  NO ANCHOR at largest hub:"); for (int x : s) printf(" %d", x); puts(""); }
        if (!(f & 2)) { noAllup++; printf("  NO ALL-UP COMB at largest hub:"); for (int x : s) printf(" %d", x); puts(""); }
    }
    printf("n=%d growth placements=%lld diameter-4 trees=%d largest-hub-not-anchor=%d no-all-up-comb=%d\n", n, total, trees, noAnchor, noAllup);
}
