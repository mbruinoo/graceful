// gp.cpp -- independent tree-by-tree search for growth placements (README sections 1, 2, 11).
// Written from scratch for src/attack/reverify; does not share code with src/growsolve.cpp etc.
//
// Style: TREE-centric.  Root the tree at a vertex r, give r label 1 and one neighbour label n
// (the bracket of length n-1 can only be {1,n}).  Then for k = n-2, ..., 1 pick an unlabelled
// vertex v whose parent is labelled and give it label lab[parent] +- k (must be an unused label
// in 1..n).  By README Theorem 7 / the definition in section 2 this enumerates exactly the growth
// placements of the tree with r labelled 1 (each bracket, longest first, has exactly one foot on
// a used vertex).
//
// Optional restrictions on the set U of unused labels after every bracket:
//   R=<r>   U has at most r runs (maximal intervals)                    (README 11, "R-run")
//   H=<h>   U is one run plus at most h isolated single labels, i.e.
//           at most one run of size >1 and at most h+1 runs in total    (README 11, "skips")
//   SIDE=1  (with H) all single labels lie on the same side of the run of size > 1
//   SIDE=2  (with H) at most one single label on each side of the run of size > 1
//           (SIDE only constrains states that still have a run of size > 1)
//   TRACK=1 (with H) "tracked main run" reading of the skip rules: the main run is the gap
//           between two blocks that grow inward from the ends (used cells a < d, main run
//           a+1..d-1, possibly empty).  A move either places the cell a+1+s or d-1-s with
//           s in {0,1} (skipping s cells, which become skipped cells left resp. right of the main
//           run), or fills a skipped cell.  At most H skipped cells outstanding; SIDE=1: never
//           skipped cells on both sides; SIDE=2: at most one on each side.  When a move can be
//           read both ways (main run of size <= 3) both readings are explored.  Without SIDE
//           this accepts exactly the same placements as H alone (checked in run_all.sh).
// Symmetry reduction: among unlabelled children of the same parent whose rooted subtrees are
// isomorphic, only the first is tried (their roles are interchangeable).
//
// Input (stdin): one tree per line: n  u1 v1  u2 v2 ... (n-1 edges, vertices 0..n-1)
// Output: one line per tree:
//   mode=exist :  "OK l0 l1 ... l(n-1)"  (labels 1..n of vertices 0..n-1)  or  "NONE"
//   mode=anchors: "A b0 b1 ... b(n-1)"  with bi = 1 iff vertex i can carry label 1
// "NONE" and bi = 0 are reported only after an exhaustive search.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;

static int n, R = 99, H = -1, SIDE = 0;
static vector<int> adjv[64];
static int par_[64], cls_[64], lab[64];
static vector<int> ch[64];
static u64 usedMask; // bit i (1..n) set = label used
static u64 nodes, cap;
static bool capped;

static bool shapeOK() {
    u64 full = ((1ULL << n) - 1) << 1;      // bits 1..n
    u64 U = full & ~usedMask;                // unused
    u64 starts = U & ~(U << 1);              // first cell of each run
    int runs = __builtin_popcountll(starts);
    if (runs > R) return false;
    if (H >= 0) {
        u64 bigStarts = starts & (U >> 1);   // runs of size >= 2
        int big = __builtin_popcountll(bigStarts);
        if (big > 1) return false;
        if (runs > H + 1) return false;
        if (SIDE && big == 1) {
            int s = __builtin_ctzll(bigStarts);
            u64 below = U & ((1ULL << s) - 1);
            int nb = __builtin_popcountll(below);
            int na = runs - 1 - nb;
            if (SIDE == 1 && nb > 0 && na > 0) return false;
            if (SIDE == 2 && (nb > 1 || na > 1)) return false;
        }
    }
    return true;
}

static void rootAt(int r) {
    // BFS order, parents, children, then isomorphism classes of rooted subtrees
    vector<int> order; order.push_back(r); par_[r] = -1;
    for (int i = 0; i < n; i++) ch[i].clear();
    for (size_t i = 0; i < order.size(); i++) {
        int v = order[i];
        for (int w : adjv[v]) if (w != par_[v]) { par_[w] = v; ch[v].push_back(w); order.push_back(w); }
    }
    map<vector<int>, int> ids;
    for (int i = n - 1; i >= 0; i--) {
        int v = order[i];
        vector<int> key;
        for (int w : ch[v]) key.push_back(cls_[w]);
        sort(key.begin(), key.end());
        auto it = ids.find(key);
        if (it == ids.end()) { int id = ids.size(); ids[key] = id; cls_[v] = id; }
        else cls_[v] = it->second;
    }
}

static bool rec(int k) {
    if (k == 0) return true;
    if (++nodes > cap) { capped = true; return false; }
    for (int v = 0; v < n; v++) {
        if (lab[v]) continue;
        int p = par_[v];
        if (!lab[p]) continue;
        bool dup = false;
        for (int w : ch[p]) { if (w == v) break; if (!lab[w] && cls_[w] == cls_[v]) { dup = true; break; } }
        if (dup) continue;
        for (int s = 0; s < 2; s++) {
            int x = s ? lab[p] - k : lab[p] + k;
            if (x < 1 || x > n) continue;
            if (usedMask >> x & 1) continue;
            usedMask |= 1ULL << x; lab[v] = x;
            if (shapeOK() && rec(k - 1)) return true;
            usedMask &= ~(1ULL << x); lab[v] = 0;
            if (capped) return false;
        }
    }
    return false;
}

static int TRACK = 0;
static bool sideOK(int sl, int sr) {
    if (sl + sr > H) return false;
    if (SIDE == 1 && sl && sr) return false;
    if (SIDE == 2 && (sl > 1 || sr > 1)) return false;
    return true;
}
static bool recT(int k, int a, int d, int sl, int sr) {
    if (k == 0) return true;
    if (++nodes > cap) { capped = true; return false; }
    for (int v = 0; v < n; v++) {
        if (lab[v]) continue;
        int p = par_[v];
        if (!lab[p]) continue;
        bool dup = false;
        for (int w : ch[p]) { if (w == v) break; if (!lab[w] && cls_[w] == cls_[v]) { dup = true; break; } }
        if (dup) continue;
        for (int s = 0; s < 2; s++) {
            int x = s ? lab[p] - k : lab[p] + k;
            if (x < 1 || x > n) continue;
            if (usedMask >> x & 1) continue;
            usedMask |= 1ULL << x; lab[v] = x;
            bool ok = false;
            if (x < a) ok = recT(k - 1, a, d, sl - 1, sr);
            else if (x > d) ok = recT(k - 1, a, d, sl, sr - 1);
            else {
                int s1 = x - a - 1, s2 = d - 1 - x;
                if (s1 <= 1 && sideOK(sl + s1, sr)) ok = recT(k - 1, x, d, sl + s1, sr);
                if (!ok && !capped && s2 <= 1 && sideOK(sl, sr + s2)) ok = recT(k - 1, a, x, sl, sr + s2);
            }
            if (ok) return true;
            usedMask &= ~(1ULL << x); lab[v] = 0;
            if (capped) return false;
        }
    }
    return false;
}

// 1 found, 0 exhausted, -1 capped
static int tryRoot(int r, u64 capv) {
    rootAt(r);
    cap = capv; nodes = 0; capped = false;
    for (int i = 0; i < n; i++) lab[i] = 0;
    if (n == 1) { lab[r] = 1; return 1; }
    lab[r] = 1; usedMask = 1ULL << 1;
    for (size_t i = 0; i < ch[r].size(); i++) {
        int c = ch[r][i];
        bool dup = false;
        for (size_t j = 0; j < i; j++) if (cls_[ch[r][j]] == cls_[c]) dup = true;
        if (dup) continue;
        lab[c] = n; usedMask |= 1ULL << n;
        if (TRACK ? recT(n - 2, 1, n, 0, 0) : (shapeOK() && rec(n - 2))) return 1;
        lab[c] = 0; usedMask &= ~(1ULL << n);
        if (capped) return -1;
    }
    return 0;
}

int main(int argc, char** argv) {
    string mode = "exist";
    for (int i = 1; i < argc; i++) {
        string a = argv[i];
        if (a.rfind("R=", 0) == 0) R = atoi(a.c_str() + 2);
        else if (a.rfind("H=", 0) == 0) H = atoi(a.c_str() + 2);
        else if (a.rfind("SIDE=", 0) == 0) SIDE = atoi(a.c_str() + 5);
        else if (a.rfind("TRACK=", 0) == 0) TRACK = atoi(a.c_str() + 6);
        else if (a.rfind("mode=", 0) == 0) mode = a.substr(5);
    }
    string line;
    long long cnt = 0, none = 0;
    while (getline(cin, line)) {
        istringstream is(line);
        if (!(is >> n)) continue;
        for (int i = 0; i < n; i++) adjv[i].clear();
        for (int i = 0; i < n - 1; i++) { int a, b; is >> a >> b; adjv[a].push_back(b); adjv[b].push_back(a); }
        cnt++;
        if (mode == "anchors") {
            printf("A");
            for (int r = 0; r < n; r++) printf(" %d", tryRoot(r, ~0ULL) == 1 ? 1 : 0);
            printf("\n");
            continue;
        }
        bool found = false;
        static const u64 caps[] = {300, 20000, 2000000, ~0ULL};
        vector<char> dead(n, 0);
        for (int ci = 0; ci < 4 && !found; ci++) {
            bool anyCapped = false;
            for (int r = 0; r < n && !found; r++) {
                if (dead[r]) continue;
                int res = tryRoot(r, caps[ci]);
                if (res == 1) found = true;
                else if (res == 0) dead[r] = 1;
                else anyCapped = true;
            }
            if (!anyCapped) break;
        }
        if (found) { printf("OK"); for (int i = 0; i < n; i++) printf(" %d", lab[i]); printf("\n"); }
        else { printf("NONE\n"); none++; }
    }
    fprintf(stderr, "trees %lld, NONE %lld (R=%d H=%d SIDE=%d)\n", cnt, none, R, H, SIDE);
    return 0;
}
