// spiderdeal.cpp -- independent search for spider deals (README section 13), written in the
// DEAL formulation, not as a tree search: centre at label 0, labels 0..m (m = n-1).  Hand the
// numbers m, m-1, ..., 1 to the legs, each leg receiving as many numbers as its length; each
// number moves that leg's tip up or down by that amount (the first move of a leg is up from 0).
// Valid: every tip position visited is in 1..m and no label is visited twice.
//
// Usage: spiderdeal n [mode] [minlegs]
//   mode = free    any valid deal                                   (Conjecture S)
//          zigzag  every leg alternates up, down, up, ...           (section 12)
//          level   every leg gets its j-th number before any leg gets its (j+1)-th
//          first   every leg gets its first number before any leg gets a second
//   Enumerates all partitions of n-1 into at least minlegs (default 3) parts.
// Output: one line per spider: "legs l1 l2 ... : OK (leg,sign)..." listing for w = m..1 the
//   0-based leg index and sign, or "legs ... : NONE" after an exhaustive search.
// Symmetry: among legs of equal length that have not started, only the first is tried.
#include <bits/stdc++.h>
using namespace std;
static int m, K, mode;
static int len_[64], got[64], tip[64], lastdir[64];
static bool used[128];
static int who[128], sgn[128];

static bool allowed(int i) {
    if (got[i] == len_[i]) return false;
    if (got[i] == 0) { for (int j = 0; j < i; j++) if (got[j] == 0 && len_[j] == len_[i]) return false; }
    if (mode == 2) { for (int j = 0; j < K; j++) if (got[j] < got[i] && got[j] < len_[j]) return false; }
    if (mode == 3 && got[i] >= 1) { for (int j = 0; j < K; j++) if (got[j] == 0) return false; }
    return true;
}
static bool rec(int w) {
    if (w == 0) return true;
    for (int i = 0; i < K; i++) {
        if (!allowed(i)) continue;
        for (int d = +1; d >= -1; d -= 2) {
            if (got[i] == 0 && d < 0) continue;
            if (mode == 1 && got[i] > 0 && d == lastdir[i]) continue;
            int x = tip[i] + d * w;
            if (x < 1 || x > m || used[x]) continue;
            int ot = tip[i], od = lastdir[i];
            used[x] = true; tip[i] = x; lastdir[i] = d; got[i]++; who[w] = i; sgn[w] = d;
            if (rec(w - 1)) return true;
            used[x] = false; tip[i] = ot; lastdir[i] = od; got[i]--;
        }
    }
    return false;
}
static long long cntAll = 0, cntNone = 0;
static void runSpider() {
    for (int i = 0; i < K; i++) { got[i] = 0; tip[i] = 0; lastdir[i] = 0; }
    memset(used, 0, sizeof used); used[0] = true;
    bool ok = rec(m);
    cntAll++;
    printf("legs");
    for (int i = 0; i < K; i++) printf(" %d", len_[i]);
    if (!ok) { printf(" : NONE\n"); cntNone++; return; }
    printf(" : OK");
    for (int w = m; w >= 1; w--) printf(" %d%c", who[w], sgn[w] > 0 ? '+' : '-');
    printf("\n");
}
static int minlegs = 3;
static void parts(int rest, int maxp, int k) {
    if (rest == 0) { if (k >= minlegs) { K = k; runSpider(); } return; }
    for (int p = min(rest, maxp); p >= 1; p--) { len_[k] = p; parts(rest - p, p, k + 1); }
}
int main(int argc, char** argv) {
    int n = atoi(argv[1]); m = n - 1;
    string md = argc > 2 ? argv[2] : "free";
    mode = md == "free" ? 0 : md == "zigzag" ? 1 : md == "level" ? 2 : 3;
    if (argc > 3) minlegs = atoi(argv[3]);
    parts(m, m, 0);
    fprintf(stderr, "n=%d mode=%s spiders=%lld NONE=%lld\n", n, md.c_str(), cntAll, cntNone);
    return 0;
}
