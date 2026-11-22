# Turn nested-paren rooted trees (one per line, optional '|' joining two roots by an edge) into edge lists; prints "n: edges".
import sys
from scarce_lib import build
for s in sys.stdin:
    s=s.strip()
    if s: n,E=build(s); print(' '.join(f"{a} {b}" for a,b in E))
