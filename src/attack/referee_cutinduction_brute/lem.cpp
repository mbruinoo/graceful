// Referee brute force for claim 0 (T1, converse, T2, T3, T4).
// Written from README sections 1-2, 9 definitions only.
// usage: ./lem N CAP      (all growth placements n<=N, all label sets R with |R|<=CAP)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef unsigned int u32;

int n;
int P[40];                    // P[k] = position of bracket k, 1..n-k
vector<vector<int>> all;      // all growth placements for current n

void gen(int k, u32 used) {
    if (k == 0) { all.push_back(vector<int>(P, P + n)); return; }
    for (int p = 1; p <= n - k; p++) {
        bool ua = used >> (p - 1) & 1, ub = used >> (p + k - 1) & 1;
        if (k == n - 1) { if (ua || ub) continue; }      // first bracket: both feet fresh
        else if (ua == ub) continue;                     // exactly one foot already used
        P[k] = p;
        gen(k - 1, used | 1u << (p - 1) | 1u << (p + k - 1));
    }
}
// literal growth test of placement q on m labels
bool isGrowth(const int* q, int m) {
    u32 used = 0;
    for (int k = m - 1; k >= 1; k--) {
        int a = q[k], b = q[k] + k;
        if (a < 1 || b > m) return false;
        bool ua = used >> (a - 1) & 1, ub = used >> (b - 1) & 1;
        if (k == m - 1) { if (ua || ub) return false; }
        else if (ua == ub) return false;
        used |= 1u << (a - 1) | 1u << (b - 1);
    }
    return true;
}
u64 key(const int* q, int m) {  // mixed radix, plus m
    u64 x = 0;
    for (int k = 1; k <= m - 1; k++) x = x * (u64)(m - k) + (u64)(q[k] - 1);
    return x * 64 + m;
}
// conditions (1),(2) literally
bool cond1(const int* p, int m, u32 R) {
    int c = 0;
    for (int k = 1; k < m; k++) if ((R >> (p[k] - 1) & 1) || (R >> (p[k] + k - 1) & 1)) c++;
    return c == __builtin_popcount(R);
}
bool cond2(const int* p, int m, u32 R) {
    int shorter = 0;  // number of R-brackets shorter than current
    for (int k = 1; k < m; k++) {
        bool rb = (R >> (p[k] - 1) & 1) || (R >> (p[k] + k - 1) & 1);
        if (rb) { shorter++; continue; }
        u32 between = 0;
        for (int x = p[k] + 1; x < p[k] + k; x++) between |= 1u << (x - 1);
        if (__builtin_popcount(R & between) != shorter) return false;
    }
    return true;
}
bool clean(const int* p, int m, u32 R) {
    if (m - __builtin_popcount(R) < 2 || R == 0) return false;
    return cond1(p, m, R) && cond2(p, m, R);
}
// delete R (assumes nothing); out: q on m' labels. returns flags
struct Rs { bool isPl, order; int m; int q[40]; };
void restrictTo(const int* p, int m, u32 R, Rs& r) {
    int rank[41]; int c = 0;
    for (int x = 1; x <= m; x++) { if (!(R >> (x - 1) & 1)) c++; rank[x] = c; }
    r.m = c; r.isPl = true; r.order = true;
    int seen[41]; memset(seen, 0, sizeof seen);
    int last = 0, cnt = 0;
    for (int k = 1; k < c; k++) r.q[k] = 0;
    for (int k = 1; k < m; k++) {
        int a = p[k], b = p[k] + k;
        if ((R >> (a - 1) & 1) || (R >> (b - 1) & 1)) continue;
        int nl = rank[b] - rank[a];
        cnt++;
        if (nl <= last) r.order = false;
        last = nl;
        if (nl < 1 || nl > c - 1 || seen[nl]) { r.isPl = false; continue; }
        seen[nl] = 1; r.q[nl] = rank[a];
    }
    if (cnt != c - 1) r.isPl = false;
}
u32 imageMask(int m, u32 R1, u32 R2) {  // image of R2 after deleting R1
    u32 out = 0; int c = 0;
    for (int x = 1; x <= m; x++) {
        if (R1 >> (x - 1) & 1) continue;
        c++;
        if (R2 >> (x - 1) & 1) out |= 1u << (c - 1);
    }
    return out;
}

unordered_map<u64, u64> term;  // T3: key -> unique terminal key (0 = non-unique)
u64 viol[8];

int main(int argc, char** argv) {
    int N = atoi(argv[1]), CAP = atoi(argv[2]);
    int T3N = argc > 3 ? atoi(argv[3]) : N;
    // n = 2 base for T3
    { int q[3] = {0, 1, 0}; term[key(q, 2)] = key(q, 2); }
    for (n = 3; n <= N; n++) {
        all.clear(); gen(n - 1, 0);
        u64 nclean = 0, npairs = 0, nonorder = 0, t1chk = 0, convchk = 0, t4stair = 0, prim = 0;
        map<int, u64> coreSize;
        for (auto& pv : all) {
            const int* p = pv.data();
            if (!isGrowth(p, n)) { printf("BUG enumeration\n"); return 1; }
            vector<u32> cl;
            for (u32 R = 1; R < (1u << n); R++) {
                int sz = __builtin_popcount(R);
                if (sz > CAP || n - sz < 2) continue;
                bool c1 = cond1(p, n, R), c2 = cond2(p, n, R);
                Rs r; restrictTo(p, n, R, r);
                bool gr = r.isPl && isGrowth(r.q, r.m);
                if (c1 && c2) {
                    nclean++; cl.push_back(R); t1chk++;
                    if (!(r.isPl && r.order && gr)) {
                        if (!viol[1]++) { printf("T1 VIOLATION n=%d R=%x p=", n, R); for (int k = 1; k < n; k++) printf("%d ", p[k]); puts(""); }
                    }
                }
                if (c1 && r.isPl && r.order) {
                    convchk++;
                    if (!c2) { if (!viol[2]++) { printf("CONVERSE VIOLATION n=%d R=%x p=", n, R); for (int k = 1; k < n; k++) printf("%d ", p[k]); puts(""); } }
                }
                if (c1 && gr && !r.order) nonorder++;
            }
            // T2
            for (u32 R1 : cl) for (u32 R2 : cl) {
                if (R1 & R2) continue;
                if (n - __builtin_popcount(R1 | R2) < 2) continue;
                npairs++;
                Rs r1; restrictTo(p, n, R1, r1);
                u32 im = imageMask(n, R1, R2);
                bool ok = clean(r1.q, r1.m, im);
                bool uni = clean(p, n, R1 | R2);
                Rs r12; restrictTo(r1.q, r1.m, im, r12);
                Rs ru; restrictTo(p, n, R1 | R2, ru);
                Rs r2; restrictTo(p, n, R2, r2);
                Rs r21; restrictTo(r2.q, r2.m, imageMask(n, R2, R1), r21);
                bool comm = r12.m == ru.m && r21.m == ru.m;
                if (comm) for (int k = 1; k < ru.m; k++) if (r12.q[k] != ru.q[k] || r21.q[k] != ru.q[k]) comm = false;
                if (!(ok && uni && comm)) {
                    if (!viol[3]++) { printf("T2 VIOLATION n=%d R1=%x R2=%x ok=%d uni=%d comm=%d p=", n, R1, R2, ok, uni, comm); for (int k = 1; k < n; k++) printf("%d ", p[k]); puts(""); }
                }
            }
            // T4
            {
                int deg[41] = {0};
                for (int k = 1; k < n; k++) { deg[p[k]]++; deg[p[k] + k]++; }
                bool allc = true; int nl = 0;
                for (int x = 1; x <= n; x++) if (deg[x] == 1) { nl++; if (!clean(p, n, 1u << (x - 1))) allc = false; }
                // leaf end(s) of bracket 1
                int a = p[1], b = p[1] + 1;
                bool leafEndClean;
                if (deg[a] == 1 && deg[b] == 1) { printf("bracket 1 isolated?? n=%d\n", n); return 1; }
                if (deg[a] != 1 && deg[b] != 1) { printf("bracket 1 not pendant?? n=%d\n", n); return 1; }
                leafEndClean = clean(p, n, 1u << ((deg[a] == 1 ? a : b) - 1));
                bool stair = p[n - 1] == 1;
                for (int k = 1; k < n - 1; k++) { int d = p[k] - p[k + 1]; if (d != 0 && d != 1) stair = false; }
                if (stair) t4stair++;
                if (allc != stair || leafEndClean != stair) {
                    if (!viol[4]++) { printf("T4 VIOLATION n=%d allc=%d leafEnd=%d stair=%d p=", n, allc, leafEndClean, stair); for (int k = 1; k < n; k++) printf("%d ", p[k]); puts(""); }
                }
            }
            // T3: unique terminal over all orders
            if (n <= T3N) {
                u64 t = ~0ull; bool uniq = true; int ncl = 0;
                for (int x = 1; x <= n; x++) {
                    u32 R = 1u << (x - 1);
                    if (!clean(p, n, R)) continue;
                    ncl++;
                    Rs r; restrictTo(p, n, R, r);
                    auto it = term.find(key(r.q, r.m));
                    if (it == term.end()) { printf("T3: child missing (not growth?) n=%d\n", n); viol[5]++; continue; }
                    if (it->second == 0) uniq = false;
                    else if (t == ~0ull) t = it->second;
                    else if (t != it->second) uniq = false;
                }
                u64 me = key(p, n);
                if (ncl == 0) { term[me] = me; prim++; coreSize[n]++; }
                else if (!uniq) { term[me] = 0; if (!viol[5]++) { printf("T3 VIOLATION n=%d p=", n); for (int k = 1; k < n; k++) printf("%d ", p[k]); puts(""); } }
                else { term[me] = t; coreSize[(int)(t & 63)]++; }
            }
        }
        printf("n=%d growth=%zu cleansets=%llu disjointpairs(ordered)=%llu t1checks=%llu convchecks=%llu nonorderGrowthRestr=%llu staircases=%llu (2^(n-2)=%d) primitive=%llu core:",
               n, all.size(), nclean, npairs, t1chk, convchk, nonorder, t4stair, 1 << (n - 2), prim);
        for (auto& kv : coreSize) printf(" %d:%llu", kv.first, kv.second);
        puts("");
        fflush(stdout);
    }
    printf("violations T1=%llu conv=%llu T2=%llu T4=%llu T3=%llu\n", viol[1], viol[2], viol[3], viol[4], viol[5]);
}
