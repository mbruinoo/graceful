"""Tree generator independent of src/treegen.h: networkx.nonisomorphic_trees.
usage: python3 gen.py N [check]   -> one tree per line: 'N a-b a-b ...' (vertices 0..N-1)
With 'check', also verifies on stderr that all trees are pairwise non-isomorphic (canonical codes)."""
import sys
import networkx as nx
from common import canon
KNOWN = {1:1,2:1,3:1,4:2,5:3,6:6,7:11,8:23,9:47,10:106,11:235,12:551,13:1301,14:3159,15:7741,
         16:19320,17:48629,18:123867,19:317955,20:823065,21:2144505,22:5623756,23:14828074,
         24:39299897,25:104636890}   # OEIS A000055
def trees(n):
    for T in nx.nonisomorphic_trees(n):
        yield list(T.edges())
if __name__ == "__main__":
    n = int(sys.argv[1])
    check = len(sys.argv) > 2
    seen = set()
    cnt = 0
    out = sys.stdout
    for e in trees(n):
        cnt += 1
        if check:
            seen.add(canon(n, [(a + 1, b + 1) for a, b in e]))
        out.write(str(n) + " " + " ".join(f"{a}-{b}" for a, b in e) + "\n")
    ok = (cnt == KNOWN[n]) and (not check or len(seen) == cnt)
    sys.stderr.write(f"gen n={n}: {cnt} trees, known {KNOWN[n]}, distinct codes {len(seen) if check else 'n/a'}: {'OK' if ok else 'MISMATCH'}\n")
    if not ok:
        sys.exit(1)
