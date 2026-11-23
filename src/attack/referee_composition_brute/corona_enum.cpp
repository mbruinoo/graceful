// Referee: enumerate ALL growth placements on labels 0..2s-1, keep coronas with label 0 on a core
// vertex, collect the rooted cores (AHU form).  Usage: corona_enum s
#include <bits/stdc++.h>
using namespace std;
int s, N; bool used[40]; int deg[40]; int ea[40], eb[40];
long long total = 0, coronas = 0; set<string> cores;
vector<int> adj[40];
string ahu(int x, int p) {
    vector<string> ch;
    for (int y : adj[x]) if (y != p && deg[y] > 1) ch.push_back(ahu(y, x));
    sort(ch.begin(), ch.end());
    string r = "("; for (auto& c : ch) r += c; return r + ")";
}
void leaf() {
    total++;
    if (deg[0] == 1) return;
    int nl = 0; for (int v = 0; v <= N; v++) nl += deg[v] == 1;
    if (nl != s) return;
    int lc[40] = {0};
    for (int c = 1; c <= N; c++) { int a = ea[c], b = eb[c]; if (deg[a] == 1) lc[b]++; if (deg[b] == 1) lc[a]++; }
    for (int v = 0; v <= N; v++) if (deg[v] > 1 && lc[v] != 1) return;
    coronas++;
    for (int v = 0; v <= N; v++) adj[v].clear();
    for (int c = 1; c <= N; c++) { adj[ea[c]].push_back(eb[c]); adj[eb[c]].push_back(ea[c]); }
    cores.insert(ahu(0, -1));
}
void rec(int c) {
    if (c == 0) { leaf(); return; }
    for (int a = 0; a + c <= N; a++) {
        int b = a + c;
        if (used[a] == used[b]) continue;
        int nw = used[a] ? b : a;
        used[nw] = true; deg[a]++; deg[b]++; ea[c] = a; eb[c] = b;
        rec(c - 1);
        used[nw] = false; deg[a]--; deg[b]--;
    }
}
int main(int argc, char** argv) {
    s = atoi(argv[1]); N = 2 * s - 1;
    used[0] = used[N] = true; deg[0] = deg[N] = 1; ea[N] = 0; eb[N] = N;
    rec(N - 1);
    printf("s=%d growth placements on %d labels: %lld, coronas with 0 on core: %lld, distinct rooted cores: %zu\n", s, N + 1, total, coronas, cores.size());
}
