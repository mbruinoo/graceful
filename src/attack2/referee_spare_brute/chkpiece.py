# verify piece lines "piece(b,j) FOUND nodes=.. : labels" from the definition (one-spare, crossing, tip innermost)
import sys,re
from common import *
from thms import crossing
from gen import path
for l in sys.stdin:
    m=re.match(r"piece\((\d+),(\d+)\) (\S+)",l)
    if not m or m.group(3)!="FOUND": print(l.strip()[:60]); continue
    b,j=int(m.group(1)),int(m.group(2)); n,e=path(b,j); lab=list(map(int,l.split(":")[1].split()))
    ok,why=check(n,0,e,lab,n+1); cr=crossing(n,0,e,lab); y=n-1
    inner = cr and lab[y]==(cr[1] if j%2 else cr[0])
    print("piece(%d,%d) valid=%s crossing=%s tip_innermost=%s unused=%s A=%s B=%s"%(b,j,ok,bool(cr),bool(inner),unused(n,e,lab,n+1),lab[1:b+1],lab[b+1:]))
