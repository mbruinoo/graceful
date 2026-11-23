// Referee: all-up comb search (claim 2) in the partition form.  For every diameter-4 tree on n
// vertices (centre with neighbours of leaf counts s_1>=..>=s_k>=0, s_2>0), look for y, hub cells
// h_i, leaf lengths U_i, W with {y-h_i},U_i,W and {h_i},h_i+U_i,W both partitioning [1,y-1],
// |W|<=s_1, U_i within [1,y-1-h_i].  DFS over lengths y-1..1.  Every solution found is re-verified
// from the README section 1 definitions (labels, lengths, growth order, tree shape).
// Usage: comb_search n [n2]
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int y, K; // K = number of non-root nbrs of centre
vector<int> sz; int s1;
int hubAt[64], hubRem[64], hubSz[64], nh;
int typeCnt[64]; // remaining hubs of each size
int lenUse[64]; // 0 = W, 1+i = leaf of hub i, -1 = hub edge
u64 nodes;
bool rec(int L, u64 used, int wrem) {
    if (L == 0) return true;
    nodes++;
    // leaf of a placed hub
    for (int i = 0; i < nh; i++) if (hubRem[i] > 0) {
        int c = hubAt[i] + L; if (c > y - 1 || (used >> c & 1)) continue;
        hubRem[i]--; lenUse[L] = 1 + i;
        if (rec(L - 1, used | 1ull << c, wrem)) return true;
        hubRem[i]++;
    }
    // new hub at cell y-L
    int c = y - L;
    if (!(used >> c & 1)) {
        for (int s = L - 1; s >= 0; s--) if (typeCnt[s] > 0) {
            typeCnt[s]--; hubAt[nh] = c; hubRem[nh] = s; hubSz[nh] = s; nh++; lenUse[L] = -1;
            if (rec(L - 1, used | 1ull << c, wrem)) return true;
            nh--; typeCnt[s]++;
        }
    }
    if (wrem > 0 && !(used >> L & 1)) {
        lenUse[L] = 0;
        if (rec(L - 1, used | 1ull << L, wrem - 1)) return true;
    }
    return false;
}
bool verify(int n) { // rebuild labeling and check from definitions
    int m = n - 1; vector<pair<int,int>> E; E.push_back({0, y});
    vector<int> leafcnt(nh, 0);
    for (int i = 0; i < nh; i++) E.push_back({hubAt[i], y});
    int w = 0;
    for (int L = 1; L < y; L++) { if (lenUse[L] == 0) { E.push_back({0, L}); w++; }
        else if (lenUse[L] > 0) { int i = lenUse[L] - 1; E.push_back({hubAt[i], hubAt[i] + L}); leafcnt[i]++;
            if (!(hubAt[i] + L < y)) return false; } }
    for (int x = y + 1; x <= m; x++) { E.push_back({0, x}); w++; }
    if (w != s1 || (int)E.size() != m) return false;
    vector<int> got; for (int i = 0; i < nh; i++) got.push_back(leafcnt[i]);
    sort(got.rbegin(), got.rend()); if (got != sz) return false;
    vector<int> byLen(m + 1, -1); vector<int> deg(m + 1, 0);
    for (int i = 0; i < m; i++) { int a = E[i].first, b = E[i].second, l = abs(a - b);
        if (l < 1 || l > m || byLen[l] >= 0 || a < 0 || b < 0 || a > m || b > m) return false; byLen[l] = i; deg[a]++; deg[b]++; }
    for (int v = 0; v <= m; v++) if (!deg[v]) return false;
    vector<char> used(m + 1, 0);
    { auto e = E[byLen[m]]; used[e.first] = used[e.second] = 1; }
    for (int l = m - 1; l >= 1; l--) { auto e = E[byLen[l]]; if (used[e.first] == used[e.second]) return false; used[e.first] = used[e.second] = 1; }
    // vertex roles distinct: leaves have degree 1, hubs deg = size+1, centre deg nh+1, root deg s1+1
    if (deg[0] != s1 + 1 || deg[y] != nh + 1) return false;
    for (int i = 0; i < nh; i++) if (deg[hubAt[i]] != leafcnt[i] + 1) return false;
    return true;
}
vector<vector<int>> parts;
void gen(int rem, int mx, vector<int>& cur) {
    if (rem == 0) { parts.push_back(cur); return; }
    for (int s = min(mx, rem - 1); s >= 0; s--) { cur.push_back(s); gen(rem - s - 1, s, cur); cur.pop_back(); }
}
int main(int argc, char** argv) {
    int n1 = atoi(argv[1]), n2 = argc > 2 ? atoi(argv[2]) : n1;
    for (int n = n1; n <= n2; n++) {
        parts.clear(); vector<int> cur; gen(n - 1, n, cur);
        int trees = 0, fail = 0; u64 tot = 0, worst = 0; vector<int> worstT;
        for (auto& s : parts) {
            if (s.size() < 2 || s[1] == 0) continue;
            trees++; s1 = s[0]; sz.assign(s.begin() + 1, s.end()); K = sz.size();
            int m = n - 1; bool ok = false; u64 tn = 0;
            for (int w = 0; w <= s1 && !ok; w++) {
                y = m - (s1 - w);
                memset(typeCnt, 0, sizeof typeCnt); for (int x : sz) typeCnt[x]++;
                nh = 0; nodes = 0;
                ok = rec(y - 1, 0, w);
                tn += nodes;
                if (ok && !verify(n)) { printf("VERIFY FAILED n=%d\n", n); return 1; }
            }
            tot += tn; if (tn > worst) { worst = tn; worstT = s; }
            if (!ok) { fail++; printf("  NO ALL-UP COMB:"); for (int x : s) printf(" %d", x); puts(""); }
        }
        printf("n=%d diameter-4 trees=%d without all-up comb at largest hub=%d nodes=%llu worst=%llu (", n, trees, fail, tot, worst);
        for (int x : worstT) printf("%d ", x); puts(")"); fflush(stdout);
    }
}
