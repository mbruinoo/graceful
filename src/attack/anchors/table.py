# table.py -- aggregate the SUMMARY lines of out_<n>_<part>.txt (written by ./anch n part parts) into one row per n
import re,glob,collections
T=collections.defaultdict(lambda: collections.Counter())
for f in glob.glob("out_*_*.txt"):
    for line in open(f):
        if not line.startswith("SUMMARY"): continue
        n=int(re.search(r"n=(\d+)",line).group(1)); c=T[n]
        for k in ["trees","vertices","nonAnchors","allAnchorTrees","treesNoAnchor","treesNoMaxDegAnchor","treesNoLeafAnchor"]:
            c[k]+=int(re.search(k+r"=(\d+)",line).group(1))
        m=re.search(r"nonAnchors=\d+ \(leaf (\d+), internal (\d+)\) kinds\(leaf (\d+), internal (\d+)\)",line)
        c["leaf"]+=int(m.group(1)); c["internal"]+=int(m.group(2)); c["kindsLeaf"]+=int(m.group(3)); c["kindsInternal"]+=int(m.group(4))
        bd=line.split("nonanchors by degree:")[1].split("|")[0]
        for d,x in re.findall(r"d(\d+):(\d+)",bd): c["deg%s"%d]+=int(x)
print("n trees vertices nonAnchors(leaf,internal) kinds(leaf,internal) byDegree(d1,d2,d3,d>=4) treesAllAnchors treesNoAnchor treesNoMaxDegAnchor treesNoLeafAnchor")
for n in sorted(T):
    c=T[n]; hi=sum(v for k,v in c.items() if k.startswith("deg") and int(k[3:])>=4)
    print(n,c["trees"],c["vertices"],"%d(%d,%d)"%(c["nonAnchors"],c["leaf"],c["internal"]),"(%d,%d)"%(c["kindsLeaf"],c["kindsInternal"]),"(%d,%d,%d,%d)"%(c["deg1"],c["deg2"],c["deg3"],hi),c["allAnchorTrees"],c["treesNoAnchor"],c["treesNoMaxDegAnchor"],c["treesNoLeafAnchor"])
