#!/usr/bin/env python3
"""Anchor (README section 7: label 0 in a growth labeling, i.e. edge lengths decreasing away from
that vertex) versus 0-rotatability (Chung-Hwang 1981 / Van Bussel 2004: label 0 in some graceful
labeling).  Brute force from the definitions for two small examples quoted in REPORT.txt.
Usage: anchor_vs_zero.py
"""
import sys
sys.setrecursionlimit(10000)

def can_zero(adj, root, growth):
    n = len(adj); m = n - 1
    order, par = [root], {root: None}
    for u in order:
        for w in adj[u]:
            if w not in par: par[w] = u; order.append(w)
    lab, usedv, usede, plen = {root: 0}, {0}, set(), {root: m + 1}
    def rec(i):
        if i == n: return True
        v = order[i]; p = par[v]
        for d in range(1, m + 1):
            if d in usede or (growth and d >= plen[p]): continue
            for x in (lab[p] + d, lab[p] - d):
                if 0 <= x <= m and x not in usedv:
                    lab[v] = x; usedv.add(x); usede.add(d); plen[v] = d
                    if rec(i + 1): return True
                    usedv.discard(x); usede.discard(d)
        return False
    return rec(1)

def path(k): return {i: [j for j in (i - 1, i + 1) if 0 <= j < k] for i in range(k)}
def hub(a, b, c):
    adj = {0: []}; nxt = 1
    for k in (a, b, c):
        h = nxt; nxt += 1; adj[0].append(h); adj[h] = [0]
        for _ in range(k):
            adj[h].append(nxt); adj[nxt] = [h]; nxt += 1
    return adj

P7 = path(7)
print("P7, vertex i (0 = end):  0-rotatable / anchor")
for v in range(4):
    print("  v =", v, can_zero(P7, v, False), can_zero(P7, v, True))
for k in (8,):
    H = hub(1, 1, k)
    print(f"H(1,1,{k}) (centre with three neighbours carrying 1,1,{k} leaves), centre: "
          f"0-centred graceful = {can_zero(H, 0, False)}, anchor = {can_zero(H, 0, True)}")
