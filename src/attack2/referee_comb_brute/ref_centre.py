#!/usr/bin/env python3
"""Referee: count growth placements (README s2) of the diameter-4 tree with hub sizes Sigma in which the
CENTRE has label 1 (label n is the mirror image).  DFS longest bracket first; the subtree always contains
the centre, so a new vertex is a hub (hung on the centre) or a leaf (hung on a hub)."""
import sys
def count(Sigma, limit=None):
    Sigma = sorted(Sigma, reverse=True); H = len(Sigma); n = 1 + H + sum(Sigma)
    role = [None] * (n + 2)      # 'c', or hub index
    leaves = []                  # leaf count per hub
    isleaf = [False] * (n + 2)
    used = [False] * (n + 2)
    used[1] = True; role[1] = 'c'; used[n] = True; role[n] = 0; leaves.append(0)
    res = [0]
    def feasible():
        cur = sorted(leaves, reverse=True)
        return len(cur) <= H and all(cur[i] <= Sigma[i] for i in range(len(cur)))
    def rec(d):
        if limit and res[0] >= limit: return
        if d == 0:
            if sorted(leaves, reverse=True) == Sigma: res[0] += 1
            return
        for p in range(1, n - d + 1):
            a, b = p, p + d
            if used[a] == used[b]: continue
            o, v = (a, b) if used[a] else (b, a)
            if isleaf[o]: continue
            if role[o] == 'c':
                if len(leaves) == H: continue
                used[v] = True; role[v] = len(leaves); leaves.append(0)
                rec(d - 1)
                leaves.pop(); role[v] = None; used[v] = False
            else:
                h = role[o]; leaves[h] += 1
                if feasible():
                    used[v] = True; isleaf[v] = True
                    rec(d - 1)
                    used[v] = False; isleaf[v] = False
                leaves[h] -= 1
    rec(n - 2)
    return res[0]
if __name__ == "__main__":
    for Sg in ([2, 1], [4, 1], [3, 2], [3, 3, 3], [1, 1], [2, 2], [1, 1, 1], [8, 1, 1], [12, 1, 1]):
        print("hub sizes", Sg, "n =", 1 + len(Sg) + sum(Sg), ": growth placements with centre at label 1:", count(Sg), flush=True)
