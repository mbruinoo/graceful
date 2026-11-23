// enumgp.cpp -- PLACEMENT-centric enumeration of all growth placements on n vertices, directly
// from README sections 1-2: for k = n-1, ..., 1 choose p_k in 1..n-k such that exactly one of
// p_k, p_k+k is already a foot of a longer bracket (k = n-1: p = 1).  No tree is given; every
// growth placement is generated and the shape it draws is recorded by a canonical code.
// This is a second method, independent of gp.cpp (which searches tree by tree with symmetry
// pruning): here there is no pruning at all except the optional shape restriction itself.
//
// Usage: enumgp n [R=r] [H=h] [SIDE=s] [rooted=1] [out=prefix]
//   prints the number of placements and the number of distinct shapes;
//   writes prefix.shapes (canonical codes of unrooted shapes, one per line, decimal) and, with
//   rooted=1, prefix.rooted (canonical codes of the shape rooted at the vertex labelled 1).
// Canonical code of a rooted tree: bitstring '1' + (children's codes, sorted by (length,value)
// descending) + '0'.  Unrooted: root at the centre; with two centres take the larger code.
// Compile with -DSLOWCHECK to cross-check the bit-trick run counter against a plain loop.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
static int n, R = 99, H = -1, SIDE = 0, wantRooted = 0;
static int pos[40];
static u64 usedMask, total;
static unordered_set<u64> shapes, rshapes;
static vector<int> g[40];

static bool shapeSlow() {
    vector<pair<int,int>> runs;
    for (int x = 1; x <= n; x++) if (!(usedMask >> x & 1)) {
        if (!runs.empty() && runs.back().second == x - 1) runs.back().second = x; else runs.push_back({x, x});
    }
    if ((int)runs.size() > R) return false;
    if (H >= 0) {
        int big = 0, bi = -1;
        for (size_t i = 0; i < runs.size(); i++) if (runs[i].second > runs[i].first) { big++; bi = i; }
        if (big > 1 || (int)runs.size() > H + 1) return false;
        if (SIDE && big == 1) {
            int nb = bi, na = runs.size() - 1 - bi;
            if (SIDE == 1 && nb && na) return false;
            if (SIDE == 2 && (nb > 1 || na > 1)) return false;
        }
    }
    return true;
}
static bool shapeOK() {
    u64 full = ((1ULL << n) - 1) << 1, U = full & ~usedMask, starts = U & ~(U << 1);
    int runs = __builtin_popcountll(starts);
    bool ok = true;
    if (runs > R) ok = false;
    else if (H >= 0) {
        u64 bs = starts & (U >> 1);
        int big = __builtin_popcountll(bs);
        if (big > 1 || runs > H + 1) ok = false;
        else if (SIDE && big == 1) {
            int s = __builtin_ctzll(bs);
            int nb = __builtin_popcountll(U & ((1ULL << s) - 1)), na = runs - 1 - nb;
            if (SIDE == 1 && nb && na) ok = false;
            if (SIDE == 2 && (nb > 1 || na > 1)) ok = false;
        }
    }
#ifdef SLOWCHECK
    if (ok != shapeSlow()) { fprintf(stderr, "run counter mismatch\n"); exit(1); }
#endif
    return ok;
}

struct Code { int len; u64 val; };
static Code code(int v, int p) {
    Code cs[40]; int m = 0;
    for (int w : g[v]) if (w != p) cs[m++] = code(w, v);
    sort(cs, cs + m, [](const Code& a, const Code& b) { return a.len != b.len ? a.len > b.len : a.val > b.val; });
    Code r; r.len = 1; r.val = 1;
    for (int i = 0; i < m; i++) { r.val = (r.val << cs[i].len) | cs[i].val; r.len += cs[i].len; }
    r.val <<= 1; r.len++;
    return r;
}
static void leaf() {
    total++;
    for (int i = 1; i <= n; i++) g[i].clear();
    for (int k = 1; k < n; k++) { g[pos[k]].push_back(pos[k] + k); g[pos[k] + k].push_back(pos[k]); }
    if (wantRooted) rshapes.insert(code(1, 0).val);
    // centre by peeling leaves
    int deg[40], alive = n; vector<int> cur;
    for (int i = 1; i <= n; i++) { deg[i] = g[i].size(); if (deg[i] <= 1) cur.push_back(i); }
    bool gone[40] = {0};
    while (alive > 2) {
        vector<int> nx;
        for (int v : cur) { gone[v] = 1; alive--; for (int w : g[v]) if (!gone[w] && --deg[w] == 1) nx.push_back(w); }
        cur = nx;
    }
    u64 best = 0;
    for (int v : cur) best = max(best, code(v, 0).val);
    shapes.insert(best);
}
static void rec(int k) {
    if (k == 0) { leaf(); return; }
    for (int p = 1; p + k <= n; p++) {
        int a = usedMask >> p & 1, b = usedMask >> (p + k) & 1;
        if (k == n - 1 ? (a + b != 0) : (a + b != 1)) continue;
        u64 old = usedMask;
        usedMask |= (1ULL << p) | (1ULL << (p + k));
        pos[k] = p;
        if (shapeOK()) rec(k - 1);
        usedMask = old;
    }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); string out;
    for (int i = 2; i < argc; i++) {
        string a = argv[i];
        if (a.rfind("R=", 0) == 0) R = atoi(a.c_str() + 2);
        else if (a.rfind("H=", 0) == 0) H = atoi(a.c_str() + 2);
        else if (a.rfind("SIDE=", 0) == 0) SIDE = atoi(a.c_str() + 5);
        else if (a.rfind("rooted=", 0) == 0) wantRooted = atoi(a.c_str() + 7);
        else if (a.rfind("out=", 0) == 0) out = a.substr(4);
    }
    rec(n - 1);
    printf("n=%d R=%d H=%d SIDE=%d placements=%llu shapes=%zu rooted_shapes=%zu\n", n, R, H, SIDE, total, shapes.size(), rshapes.size());
    if (!out.empty()) {
        FILE* f = fopen((out + ".shapes").c_str(), "w");
        for (u64 s : shapes) fprintf(f, "%llu\n", s);
        fclose(f);
        if (wantRooted) { f = fopen((out + ".rooted").c_str(), "w"); for (u64 s : rshapes) fprintf(f, "%llu\n", s); fclose(f); }
    }
    return 0;
}
