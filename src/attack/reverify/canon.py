#!/usr/bin/env python3
"""Canonical codes of trees, matching enumgp.cpp (independent Python implementation).

  canon.py missing treefile shapesfile
      prints how many trees of treefile have their unrooted code in shapesfile, and lists the
      trees that do not (edge lists).
  canon.py anchors treefile rootedfile [gpanchorsfile]
      vertex v of tree T is an anchor iff code(T rooted at v) is in rootedfile.  Prints the row
      of the README section 7 table; if gpanchorsfile (output of gp mode=anchors) is given,
      checks that it agrees vertex by vertex.
"""
import sys

def read_trees(fn):
    for line in open(fn):
        x = list(map(int, line.split()))
        if not x:
            continue
        n = x[0]
        adj = [[] for _ in range(n)]
        for i in range(n - 1):
            u, v = x[1 + 2 * i], x[2 + 2 * i]
            adj[u].append(v); adj[v].append(u)
        yield n, adj, line.strip()

def code(adj, v, p):
    cs = sorted((code(adj, w, v) for w in adj[v] if w != p), reverse=True)  # (len, val) descending
    val, ln = 1, 1
    for l, c in cs:
        val = (val << l) | c
        ln += l
    return (ln + 1, val << 1)

def centres(n, adj):
    deg = [len(a) for a in adj]
    gone = [False] * n
    cur = [v for v in range(n) if deg[v] <= 1]
    alive = n
    while alive > 2:
        nx = []
        for v in cur:
            gone[v] = True; alive -= 1
            for w in adj[v]:
                if not gone[w]:
                    deg[w] -= 1
                    if deg[w] == 1:
                        nx.append(w)
        cur = nx
    return cur

def ucode(n, adj):
    return max(code(adj, c, -1)[1] for c in centres(n, adj))

def main():
    cmd = sys.argv[1]
    if cmd == "missing":
        S = set(int(l) for l in open(sys.argv[3]))
        seen = set(); miss = []; tot = 0
        for n, adj, line in read_trees(sys.argv[2]):
            c = ucode(n, adj)
            assert c not in seen, "two input trees with the same code"
            seen.add(c); tot += 1
            if c not in S:
                miss.append(line)
        assert S <= seen, "enumerated shape not among the input trees"
        print(f"trees {tot}, drawn {tot - len(miss)}, not drawn {len(miss)}")
        for m in miss[:20]:
            print("  not drawn:", m)
    elif cmd == "anchors":
        S = set(int(l) for l in open(sys.argv[3]))
        gp = None
        if len(sys.argv) > 4:
            gp = [list(map(int, l.split()[1:])) for l in open(sys.argv[4]) if l.strip()]
        verts = non = allanch = trees = 0; maxdeg_non = 0; noanch = 0
        for i, (n, adj, line) in enumerate(read_trees(sys.argv[2])):
            bits = [1 if code(adj, v, -1)[1] in S else 0 for v in range(n)]
            if gp is not None:
                assert gp[i] == bits, ("gp.cpp and enumeration disagree", line, gp[i], bits)
            trees += 1; verts += n; non += n - sum(bits)
            allanch += (sum(bits) == n); noanch += (sum(bits) == 0)
            for v in range(n):
                if not bits[v]:
                    maxdeg_non = max(maxdeg_non, len(adj[v]))
        print(f"trees {trees}, vertices {verts}, non-anchors {non}, trees with every vertex an anchor {allanch}, "
              f"trees with no anchor {noanch}, max degree of a non-anchor {maxdeg_non}"
              + (", gp.cpp agrees vertex by vertex" if gp is not None else ""))

if __name__ == "__main__":
    main()
