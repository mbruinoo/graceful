// growcheck: second, independently written counter of growth placements, used to cross-check growfam.
// It uses the heap form (README Theorem 7) instead of the longest-first build:
//   a graceful labeling is a growth placement iff, rooting the tree at the vertex labelled 1, edge
//   lengths strictly decrease along every path away from the root.
// For every root r (label 1) the vertices are labelled in breadth-first order of the TREE (not in order of
// edge length); a label is accepted if it is unused, its edge length is unused and shorter than the
// parent's edge, and not shorter than the number of vertices in the subtree it carries (the edges below it
// are distinct and shorter).  No memo, no symmetry pruning: it counts labelings and divides by |Aut T|, computed
// separately from the centre-rooted canonical form.
// Usage: growcheck < trees      (same line format as growfam; practical for n up to about 20)
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[130]; int lab[130], par[130], plen[130], sub_[130]; bool usedL[130], usedD[130]; vector<int> order_;
unsigned long long cnt;
void rec(size_t i) {
  if (i == order_.size()) { cnt++; return; }
  int w = order_[i], u = par[w], bound = plen[u];
  for (int x = 1; x <= n; x++) { if (usedL[x]) continue; int d = abs(x - lab[u]); if (d >= bound || d < sub_[w] || usedD[d]) continue;
    usedL[x] = usedD[d] = true; lab[w] = x; plen[w] = d; rec(i + 1); usedL[x] = usedD[d] = false; }
}
// automorphisms: product over vertices of factorials of multiplicities of equal child encodings
string enc(int v, int p, double &logaut, unsigned long long &aut) {
  vector<string> ch; for (int u : adj[v]) if (u != p) ch.push_back(enc(u, v, logaut, aut)); sort(ch.begin(), ch.end());
  for (size_t i = 0; i < ch.size();) { size_t j = i; while (j < ch.size() && ch[j] == ch[i]) j++; for (size_t t = 2; t <= j - i; t++) aut *= t; i = j; }
  string s = "("; for (auto &c : ch) s += c; return s + ")"; }
unsigned long long automorphisms() {
  vector<int> deg(n), layer; vector<char> gone(n, 0); int rem = n; for (int i = 0; i < n; i++) { deg[i] = adj[i].size(); if (deg[i] <= 1) layer.push_back(i); }
  while (rem > 2) { vector<int> nx; for (int v : layer) { gone[v] = 1; rem--; for (int u : adj[v]) if (!gone[u] && --deg[u] == 1) nx.push_back(u); } layer = nx; }
  unsigned long long aut = 1; double la = 0;
  if (layer.size() == 1) { enc(layer[0], -1, la, aut); return aut; }
  string a = enc(layer[0], layer[1], la, aut), b = enc(layer[1], layer[0], la, aut); if (a == b) aut *= 2; return aut; }
int main() {
  string line;
  while (getline(cin, line)) { if (line.empty() || line[0] == '#') continue; string name, body = line; size_t c = line.find(':'); if (c != string::npos) { name = line.substr(0, c); body = line.substr(c + 1); }
    istringstream is(body); vector<pair<int, int>> es; int u, v, mx = -1; while (is >> u >> v) { es.push_back({u, v}); mx = max(mx, max(u, v)); } n = mx + 1;
    for (int i = 0; i < n; i++) adj[i].clear(); for (auto e : es) { adj[e.first].push_back(e.second); adj[e.second].push_back(e.first); }
    unsigned long long labelings = 0;
    for (int r = 0; r < n; r++) { order_.clear(); vector<int> q = {r}; par[r] = -1; for (size_t h = 0; h < q.size(); h++) { int x = q[h]; for (int y : adj[x]) if (y != par[x]) { par[y] = x; q.push_back(y); order_.push_back(y); } }
      for (int h = (int)q.size() - 1; h >= 0; h--) { int x = q[h]; sub_[x] = 1; for (int y : adj[x]) if (y != par[x]) sub_[x] += sub_[y]; }
      memset(usedL, 0, sizeof usedL); memset(usedD, 0, sizeof usedD); lab[r] = 1; usedL[1] = true; plen[r] = n; cnt = 0; rec(0); labelings += cnt; }
    unsigned long long aut = automorphisms();
    printf("%s n=%d count=%llu labelings=%llu aut=%llu%s\n", name.c_str(), n, labelings / aut, labelings, aut, labelings % aut ? " NOT DIVISIBLE" : ""); fflush(stdout); }
}
