// growfam: exact NUMBER of growth placements of a given tree, and exhaustive existence search.
//
// A growth placement of a tree T on n vertices is a labeling with 1..n such that the edge lengths are
// n-1, ..., 1 and, taken longest first, every edge hangs one new vertex on the part already labelled.
// The number of growth placements that draw T equals (growth labelings of T) / |Aut T|.
//
// Search: fix the top bracket {1,n} on one oriented edge per orbit, then place lengths n-2, ..., 1.
// Symmetry pruning (as subId in runsolve128.cpp): unbuilt branches of the same shape hanging on the same
// labelled vertex are interchangeable, so only one of them is tried.  This counts every orbit of
// labelings exactly once, i.e. it counts placements.
// Memo: the number of completions depends only on (set of used labels, for every labelled vertex that
// still has unbuilt branches: its label and the multiset of their shapes).  That state is hashed to
// 128 bits and stored in a fixed-size table (a hash collision would give a wrong number; with < 2^32
// states the chance is below 2^-64 and is ignored).  NOMEMO=1 switches the table off.
// Sound dead-end tests: every unused label needs a possible partner; every open vertex needs enough
// unused labels within reach.  NOPRUNE=1 switches them off.
//
// Usage:
//   growfam count [R]            < trees     exact count for each tree (R>0: only placements whose unused
//                                            labels never form more than R runs)
//   growfam exist [R [budget]]   < trees     R given: complete search within <=R runs only.
//                                            R=0 or absent: budgeted attempts with R = 1,2,3, then rounds with
//                                            R = 3, 4, unrestricted in fixed-seed shuffled orders and doubling
//                                            budgets, then the unrestricted complete search in natural order
//                                            (no budget unless FINALBUDGET is set).  Every run is reproducible;
//                                            NONE is only ever reported by a complete unrestricted search.
//                                            Prints a verified labeling, NONE, or UNRESOLVED.
//   growfam all n [show [part parts]]        count for every tree on n vertices (built-in generator);
//                                            prints total, and the `show` scarcest non-caterpillars.
// Tree lines: "name: u v u v ..." or just "u v u v ..." (0-based edge list).
//   The `all` mode also reports anchors (vertices that carry label 1 in some growth placement, README s.7):
//   totals, every tree with no anchor leaf, every tree in which at least half the vertices are non-anchors.
//   ANCHORS=1 in count mode lists, per vertex orbit, the number of placements with that orbit at label 1.
// Env: TABLE=bits (default 22; 48 bytes per entry), NOMEMO, NOPRUNE, FINALBUDGET=nodes, ROUNDS=r, COUNTBUDGET=nodes
//      (count mode gives up on a tree after that many nodes and says so), STOPABORT=k (count mode stops
//      reading after k trees over budget in a row), QUIET.
#include <bits/stdc++.h>
#include "treegen.h"
using namespace std;
typedef unsigned __int128 u128; typedef unsigned long long u64;
const int MAXN = 126;
int n, R = 0;
vector<int> adj[MAXN + 2];
int lab[MAXN + 2], vat[MAXN + 2], rem_[MAXN + 2];
int sid[MAXN + 2][MAXN + 2];
u128 usedm, openm, ALLM, win[MAXN + 2][MAXN + 2];
u64 Z1[MAXN + 2][2 * MAXN + 4], Z2[MAXN + 2][2 * MAXN + 4];
u64 H1, H2, salt = 0x9e3779b97f4a7c15ull;
bool NOMEMO = false, NOPRUNE = false, EXIST = false, found = false, aborted = false;
long long nodes = 0, budget = 0, memohits = 0;
bool SHUFFLE = false; mt19937 ordrng(1);   // exist mode only: fixed-seed shuffled candidate order for the budgeted attempts

static inline u128 bit(int x) { return ((u128)1) << x; }
static inline int pc(u128 x) { return __builtin_popcountll((u64)x) + __builtin_popcountll((u64)(x >> 64)); }
static inline int ctz(u128 x) { u64 lo = (u64)x; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((u64)(x >> 64)); }
static inline int runs(u128 S) { u128 un = ~S & ALLM; return pc(un & ~(un << 1)); }
static inline u64 mix(u64 x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdull; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ull; x ^= x >> 33; return x; }

struct Entry { u64 a, b; u128 cnt; u64 cost; };
Entry *tab = nullptr; u64 tabmask = 0;

string encSub(int v, int pa) { vector<string> ch; for (int u : adj[v]) if (u != pa) ch.push_back(encSub(u, v)); sort(ch.begin(), ch.end()); string r = "("; for (auto &c : ch) r += c; return r + ")"; }
void prepIds() { map<string, int> ids; for (int u = 0; u < n; u++) for (int w : adj[u]) { string e = encSub(w, u); auto it = ids.find(e); int id; if (it == ids.end()) { id = ids.size(); ids[e] = id; } else id = it->second; sid[u][w] = id; } }

static inline void place(int u, int w, int x) {
  lab[w] = x; vat[x] = w; usedm |= bit(x);
  H1 -= Z1[lab[u]][sid[u][w]]; H2 -= Z2[lab[u]][sid[u][w]];
  if (--rem_[u] == 0) openm &= ~bit(lab[u]);
  int r = 0; for (int c : adj[w]) if (c != u) { r++; H1 += Z1[x][sid[w][c]]; H2 += Z2[x][sid[w][c]]; }
  rem_[w] = r; if (r) openm |= bit(x);
}
static inline void unplace(int u, int w, int x) {
  for (int c : adj[w]) if (c != u) { H1 -= Z1[x][sid[w][c]]; H2 -= Z2[x][sid[w][c]]; }
  openm &= ~bit(x); rem_[w] = 0;
  if (rem_[u]++ == 0) openm |= bit(lab[u]);
  H1 += Z1[lab[u]][sid[u][w]]; H2 += Z2[lab[u]][sid[u][w]];
  usedm &= ~bit(x); lab[w] = 0;
}

// number of completions when lengths k, k-1, ..., 1 remain; cost = nodes below (for the table)
u128 dfs(int k, u64 &cost) {
  cost = 1;
  if (k == 0) { if (EXIST) found = true; return 1; }
  nodes++;
  if (budget && nodes > budget) { aborted = true; return 0; }
  u128 un = ~usedm & ALLM;
  if (!NOPRUNE) {
    for (u128 m = un; m; m &= m - 1) { int x = ctz(m); if (!(openm & win[x][k]) && !(un & win[x][k - 1] & ~bit(x))) return 0; }
    for (u128 m = openm; m; m &= m - 1) { int y = ctz(m); if (pc(un & win[y][k]) < rem_[vat[y]]) return 0; }
  }
  u64 ka = 0, kb = 0, idx = 0;
  if (!NOMEMO) {
    ka = mix(H1 ^ mix((u64)usedm + salt)) ^ mix((u64)(usedm >> 64) + 0x1234567ull); kb = H2 + mix((u64)usedm * 3 + 1) + mix((u64)(usedm >> 64) * 5 + salt);
    idx = ka & tabmask & ~1ull;
    for (int t = 0; t < 2; t++) { Entry &e = tab[idx + t]; if (e.a == ka && e.b == kb && e.cost) { memohits++; return e.cnt; } }
  }
  u128 total = 0;
  int cu[2 * MAXN], cw[2 * MAXN], cx[2 * MAXN], nc = 0;
  for (u128 m = openm; m; m &= m - 1) {
    int y = ctz(m), u = vat[y];
    for (int s = -1; s <= 1; s += 2) {
      int x = y + s * k; if (x < 1 || x > n || (usedm >> x & 1)) continue;
      if (R && runs(usedm | bit(x)) > R) continue;
      int seen[MAXN], ns = 0;
      for (int w : adj[u]) if (!lab[w]) {
        int id = sid[u][w]; bool dup = false; for (int i = 0; i < ns; i++) if (seen[i] == id) { dup = true; break; }
        if (dup) continue; seen[ns++] = id; cu[nc] = u; cw[nc] = w; cx[nc] = x; nc++;
      }
    }
  }
  if (SHUFFLE) for (int i = nc - 1; i > 0; i--) { int j = ordrng() % (i + 1); swap(cu[i], cu[j]); swap(cw[i], cw[j]); swap(cx[i], cx[j]); }
  for (int i = 0; i < nc; i++) {
    place(cu[i], cw[i], cx[i]); u64 c; total += dfs(k - 1, c); cost += c;
    if (found) return total;                 // keep lab[] as the solution
    unplace(cu[i], cw[i], cx[i]);
    if (aborted) return 0;
  }
  if (!NOMEMO && cost >= 4) {
    Entry *e = &tab[idx]; if (tab[idx + 1].cost < e->cost) e = &tab[idx + 1];
    if (e->cost <= cost || e->a == 0) { e->a = ka; e->b = kb; e->cnt = total; e->cost = cost; }
  }
  return total;
}

vector<pair<int, int>> rootOrbits() { vector<pair<int, int>> r; set<pair<int, int>> seen; for (int u = 0; u < n; u++) for (int v : adj[u]) { pair<int, int> key(sid[v][u], sid[u][v]); if (seen.insert(key).second) r.push_back({u, v}); } return r; }

void setRoot(int u, int v) {
  memset(lab, 0, sizeof lab); memset(rem_, 0, sizeof rem_); usedm = bit(1) | bit(n); openm = 0; H1 = H2 = 0;
  lab[u] = 1; vat[1] = u; lab[v] = n; vat[n] = v;
  for (int a = 0; a < 2; a++) { int p = a ? v : u, q = a ? u : v; int r = 0; for (int c : adj[p]) if (c != q) { r++; H1 += Z1[lab[p]][sid[p][c]]; H2 += Z2[lab[p]][sid[p][c]]; } rem_[p] = r; if (r) openm |= bit(lab[p]); }
}
void newSalt() { salt = mix(salt + 0x51ed27ull); }   // entries of earlier trees and earlier R no longer match
void newTree() {
  prepIds(); ALLM = 0; for (int i = 1; i <= n; i++) ALLM |= bit(i);
  for (int x = 1; x <= n; x++) for (int d = 0; d <= n; d++) { u128 w = 0; for (int y = max(1, x - d); y <= min(n, x + d); y++) w |= bit(y); win[x][d] = w; }
  newSalt();
}
// anchors: orbitOf[v] = index of v's orbit under Aut T; anchored[o] = placements with a vertex of orbit o at label 1
int orbitOf[MAXN + 2], norb; u128 anchored[MAXN + 2]; int orbSize[MAXN + 2], orbRep[MAXN + 2];
void prepOrbits() { map<string, int> ids; norb = 0; for (int v = 0; v < n; v++) { string e = encSub(v, -1); auto it = ids.find(e); if (it == ids.end()) { ids[e] = norb; orbSize[norb] = 0; orbRep[norb] = v; anchored[norb] = 0; orbitOf[v] = norb++; } else orbitOf[v] = it->second; orbSize[orbitOf[v]]++; } }
u128 countTree() { u128 total = 0; found = aborted = false; prepOrbits(); for (auto e : rootOrbits()) { setRoot(e.first, e.second); u64 c; u128 t = dfs(n - 2, c); total += t; anchored[orbitOf[e.first]] += t; if (aborted) break; } return total; }
// 1 found (lab[] holds it), 0 none (complete), -1 budget hit
int existTree() { found = aborted = false; bool hit = false; for (auto e : rootOrbits()) { setRoot(e.first, e.second); u64 c; aborted = false; dfs(n - 2, c); if (found) return 1; if (aborted) { hit = true; break; } } return hit ? -1 : 0; }

// independent check from the definition: labels are 1..n, and taking lengths n-1..1 each edge has exactly one used foot
bool verify() {
  vector<int> seenL(n + 1, 0); for (int u = 0; u < n; u++) { if (lab[u] < 1 || lab[u] > n || seenL[lab[u]]++) return false; }
  vector<pair<int, int>> byLen(n, {-1, -1});
  for (int u = 0; u < n; u++) for (int w : adj[u]) if (u < w) { int d = abs(lab[u] - lab[w]); if (d < 1 || d > n - 1 || byLen[d].first >= 0) return false; byLen[d] = {u, w}; }
  vector<char> usedV(n, 0); if (byLen[n - 1].first < 0) return false; usedV[byLen[n - 1].first] = usedV[byLen[n - 1].second] = 1;
  for (int d = n - 2; d >= 1; d--) { auto e = byLen[d]; if (e.first < 0) return false; if (usedV[e.first] == usedV[e.second]) return false; usedV[e.first] = usedV[e.second] = 1; }
  return true;
}
string str128(u128 x) { if (!x) return "0"; string s; while (x) { s += char('0' + (int)(x % 10)); x /= 10; } reverse(s.begin(), s.end()); return s; }
bool readTree(const string &line, string &name) {
  string body = line; size_t c = line.find(':'); name = ""; if (c != string::npos) { name = line.substr(0, c); body = line.substr(c + 1); }
  istringstream is(body); vector<pair<int, int>> es; int u, v, mx = -1; while (is >> u >> v) { es.push_back({u, v}); mx = max(mx, max(u, v)); }
  if (es.empty()) return false; n = mx + 1; if (n > MAXN || (int)es.size() != n - 1) { fprintf(stderr, "bad tree line: %s\n", line.c_str()); return false; }
  for (int i = 0; i < n; i++) adj[i].clear(); for (auto e : es) { adj[e.first].push_back(e.second); adj[e.second].push_back(e.first); }
  return true;
}
bool isCaterpillar() { for (int v = 0; v < n; v++) { int c = 0; for (int u : adj[v]) if (adj[u].size() > 1) c++; if (c > 2) return false; } return true; }
double now() { return chrono::duration<double>(chrono::steady_clock::now().time_since_epoch()).count(); }

int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: growfam count [R] | exist [R [budget]] | all n [show [part parts]]\n"); return 1; }
  string mode = argv[1]; NOMEMO = getenv("NOMEMO"); NOPRUNE = getenv("NOPRUNE"); bool quiet = getenv("QUIET");
  int bits = getenv("TABLE") ? atoi(getenv("TABLE")) : 22; if (mode == "all" && !getenv("TABLE")) bits = 16;
  if (!NOMEMO) { tab = (Entry *)calloc((size_t)1 << bits, sizeof(Entry)); tabmask = ((u64)1 << bits) - 1; }
  mt19937_64 rng(20261123); for (int i = 0; i < MAXN + 2; i++) for (int j = 0; j < 2 * MAXN + 4; j++) { Z1[i][j] = rng(); Z2[i][j] = rng(); }
  if (mode == "all") {
    n = atoi(argv[2]); int show = argc > 3 ? atoi(argv[3]) : 8, part = argc > 4 ? atoi(argv[4]) : 0, parts = argc > 5 ? atoi(argv[5]) : 1;
    TreeGen g(n); vector<int> par; long long idx = 0, trees = 0, zero = 0, verts = 0, nonanch = 0, allanch = 0; u128 total = 0; vector<pair<u128, string>> best;   // scarcest non-caterpillars
    while (g.next()) { if ((idx++) % parts != part) continue; g.parents(par); for (int i = 0; i < n; i++) adj[i].clear(); for (int i = 1; i < n; i++) { adj[i].push_back(par[i]); adj[par[i]].push_back(i); }
      newTree(); u128 c = countTree(); trees++; total += c;
      { int na = 0, leaves = 0, aleaves = 0; for (int v = 0; v < n; v++) { bool a = anchored[orbitOf[v]] != 0; if (!a) na++; if (adj[v].size() == 1) { leaves++; if (a) aleaves++; } }
        verts += n; nonanch += na; if (!na) allanch++; if (!aleaves) { printf("NO ANCHOR LEAF (count %s, non-anchors %d of %d):", str128(c).c_str(), na, n); for (int i = 1; i < n; i++) printf(" %d %d", par[i], i); printf("\n"); }
        if (na * 2 >= n) { printf("HALF NON-ANCHORS (count %s, non-anchors %d of %d):", str128(c).c_str(), na, n); for (int i = 1; i < n; i++) printf(" %d %d", par[i], i); printf("\n"); } } if (!c) { zero++; printf("NO GROWTH PLACEMENT:"); for (int i = 1; i < n; i++) printf(" %d %d", par[i], i); printf("\n"); }
      if (show > 0 && !isCaterpillar() && ((int)best.size() < show || c < best.back().first)) { string s; for (int i = 1; i < n; i++) s += " " + to_string(par[i]) + " " + to_string(i); best.push_back({c, s}); sort(best.begin(), best.end()); if ((int)best.size() > show) best.pop_back(); } }
    printf("n=%d part %d/%d trees=%lld total_growth_placements=%s trees_with_none=%lld vertices=%lld non_anchors=%lld trees_all_anchors=%lld\n", n, part, parts, trees, str128(total).c_str(), zero, verts, nonanch, allanch);
    for (auto &b : best) printf("  %s :%s\n", str128(b.first).c_str(), b.second.c_str());
    return 0;
  }
  EXIST = (mode == "exist"); R = argc > 2 ? atoi(argv[2]) : 0; long long userBudget = argc > 3 ? atoll(argv[3]) : 0;
  long long finalBudget = getenv("FINALBUDGET") ? atoll(getenv("FINALBUDGET")) : 0, countBudget = getenv("COUNTBUDGET") ? atoll(getenv("COUNTBUDGET")) : 0;
  string line, name; int abortsInRow = 0, stopAfter = getenv("STOPABORT") ? atoi(getenv("STOPABORT")) : 1 << 30;
  while (getline(cin, line)) {
    if (line.empty() || line[0] == '#') continue; if (!readTree(line, name)) continue; double t0 = now();
    if (!EXIST) { newTree(); nodes = memohits = 0; budget = countBudget; u128 c = countTree();
      if (aborted) { printf("%s n=%d count=ABORTED(budget) nodes=%lld t=%.1fs\n", name.c_str(), n, nodes, now() - t0); if (++abortsInRow >= stopAfter) { printf("# stopped after %d trees over budget in a row\n", abortsInRow); return 0; } }
      else { abortsInRow = 0; printf("%s n=%d count=%s nodes=%lld hits=%lld t=%.1fs", name.c_str(), n, str128(c).c_str(), nodes, memohits, now() - t0);
        if (getenv("ANCHORS")) { int na = 0; for (int v = 0; v < n; v++) if (!anchored[orbitOf[v]]) na++; printf(" non_anchors=%d/%d orbits[deg x size: placements with it at label 1]:", na, n);
          for (int o = 0; o < norb; o++) printf(" [%zu x%d: %s]", adj[orbRep[o]].size(), orbSize[o], str128(anchored[o]).c_str()); }
        printf("\n"); }
      fflush(stdout); continue; }
    // Schedule.  Every attempt is a depth-first search that is complete unless it hits its node budget.
    //  1. R = 1, 2, 3 in natural order, budget b each (b = 2,000,000 nodes unless given).
    //  2. rounds r = 0..ROUNDS-1: R = 3, 4, unrestricted, candidates in a fixed-seed shuffled order, budget 20000*2^r
    //     (ROUNDS defaults to 14).
    //     Failed states stay in the table between rounds of the same R (failure does not depend on order).
    //  3. unrestricted, natural order, budget FINALBUDGET (default: none) -- the only source of a NONE verdict.
    int Rsaved = R, res = -1, usedR = -1; long long totalNodes = 0; string noneIn; newTree();
    auto attempt = [&](int r, long long bud, int seed) { R = r; budget = bud; SHUFFLE = seed != 0; if (seed) ordrng.seed(seed); nodes = 0; res = existTree(); totalNodes += nodes; usedR = r; SHUFFLE = false; return res; };
    if (Rsaved > 0) { attempt(Rsaved, userBudget, 0); }
    else { long long b = userBudget ? userBudget : 2000000; bool done = false; int rounds = getenv("ROUNDS") ? atoi(getenv("ROUNDS")) : 14; long long b0 = 20000;
      for (int r = 1; r <= 3 && !done; r++) { newSalt(); attempt(r, b, 0); if (res == 1) done = true; else if (res == 0) noneIn += to_string(r) + " "; }
      bool none3 = noneIn.find("3") != string::npos, none4 = false; u64 saltR[3]; for (int i = 0; i < 3; i++) { newSalt(); saltR[i] = salt; }
      for (int rd = 0; rd < rounds && !done; rd++) { int Rs[3] = {3, 4, 0};
        for (int i = 0; i < 3 && !done; i++) { if ((i == 0 && none3) || (i == 1 && none4)) continue; salt = saltR[i]; attempt(Rs[i], b0 << rd, 1000 * rd + i + 1);
          if (res == 1 || (res == 0 && Rs[i] == 0)) done = true; else if (res == 0) { (i == 0 ? none3 : none4) = true; noneIn += to_string(Rs[i]) + " "; } } }
      if (!done) { newSalt(); attempt(0, finalBudget, 0); } }
    R = Rsaved;
    if (res == 1) { bool ok = verify(); printf("%s n=%d FOUND runs<=%s verified=%s nodes=%lld t=%.1fs", name.c_str(), n, usedR ? to_string(usedR).c_str() : "inf", ok ? "yes" : "NO", totalNodes, now() - t0);
      if (noneIn.size()) printf(" none_with_runs<=[%s]", noneIn.c_str()); if (!quiet) { printf(" labels:"); for (int u = 0; u < n; u++) printf(" %d", lab[u]); } printf("\n"); }
    else if (res == 0 && usedR == 0) printf("%s n=%d NONE (complete unrestricted search) nodes=%lld t=%.1fs edges:%s\n", name.c_str(), n, totalNodes, now() - t0, line.c_str());
    else if (res == 0) printf("%s n=%d NONE with runs<=%d (complete) nodes=%lld t=%.1fs\n", name.c_str(), n, usedR, totalNodes, now() - t0);
    else printf("%s n=%d UNRESOLVED (budget) none_with_runs<=[%s] nodes=%lld t=%.1fs\n", name.c_str(), n, noneIn.c_str(), totalNodes, now() - t0);
    fflush(stdout);
  }
}
