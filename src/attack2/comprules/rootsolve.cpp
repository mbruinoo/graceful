// Is the root of a rooted tree an anchor?  (README section 7: an anchor is a vertex that can carry the
// end label in a growth placement; by the definition of growth, that is: labels 0..m, root at 0, and,
// placing lengths m, m-1, .., 1, each bracket joins an already labelled vertex to a new one.)
// Written from the definitions only.  Input lines:  n p1 p2 .. p_{n-1}   (parent of vertex i, root = 0,
// parents come before children).  Output per line: 1 (anchor) or 0, exhaustive search.
#include <cstdio>
#include <vector>
#include <cstdlib>
using namespace std;
int n, m, par[32], lab[32], sz[32]; bool usedLab[64];
vector<int> kids[32];
bool rec(int k) {                 // place length k
    if (k == 0) return true;
    for (int v = 1; v < n; v++) {
        if (lab[v] >= 0 || lab[par[v]] < 0) continue;
        if (sz[v] - 1 > k - 1) continue;          // everything below v needs shorter lengths
        // skip v if an earlier unlabelled sibling has an identical situation? (no symmetry breaking: plain search)
        for (int sg = -1; sg <= 1; sg += 2) {
            int x = lab[par[v]] + sg * k;
            if (x < 0 || x > m || usedLab[x]) continue;
            lab[v] = x; usedLab[x] = true;
            if (rec(k - 1)) return true;
            lab[v] = -1; usedLab[x] = false;
        }
    }
    return false;
}
int main() {
    while (scanf("%d", &n) == 1) {
        m = n - 1;
        for (int i = 0; i < n; i++) { kids[i].clear(); lab[i] = -1; sz[i] = 1; }
        for (int i = 0; i <= m; i++) usedLab[i] = false;
        for (int i = 1; i < n; i++) { scanf("%d", &par[i]); kids[par[i]].push_back(i); }
        for (int i = n - 1; i >= 1; i--) sz[par[i]] += sz[i];
        lab[0] = 0; usedLab[0] = true;
        printf("%d\n", rec(m) ? 1 : 0);
    }
}
