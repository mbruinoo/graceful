#!/usr/bin/env python3
# summarize.py  -- totals of the ascan runs in this directory (out_<n>_<part>of<parts>.txt), per n.
import glob,re,collections
tot=collections.defaultdict(lambda: collections.Counter()); lines=collections.defaultdict(list)
for f in sorted(glob.glob("out_*_*of*.txt")):
    n=int(f.split("_")[1]); parts=int(f.split("of")[1].split(".")[0])
    for line in open(f):
        if line.startswith("SUMMARY"):
            tot[n]['files']+=1; tot[n]['parts']=parts
            for k in ("trees","orbitsTested","anchors","NOT","CAP","treesNoMaxDegAnchor","treesMaxDegUndecided","nodes"):
                tot[n][k]+=int(re.search(k+r"=(\d+)",line).group(1))
            m=re.search(r"witnesses verified: (\d+)",line)
            if m: tot[n]['verified']+=int(m.group(1))
            m=re.search(r"NOT kinds by degree:(.*?)\|",line)
            for d,c in re.findall(r"d(\d+):(\d+)",m.group(1)): tot[n]['NOTdeg%s'%d]+=int(c)
        elif line.strip(): lines[n].append(line.strip())
for n in sorted(tot):
    t=tot[n]
    print("n=%d: parts %d/%d, trees %d, vertex orbits of degree>=4 tested (plus max-degree tests) %d, anchors %d (witness verified %d), "
          "NOT %d [by degree: %s], CAP %d, trees with no max-degree anchor %d, undecided %d, search nodes %d"%(n,t['files'],t['parts'],t['trees'],t['orbitsTested'],t['anchors'],t['verified'],
          t['NOT']," ".join("d%s:%d"%(k[6:],v) for k,v in sorted(t.items()) if k.startswith("NOTdeg")),t['CAP'],t['treesNoMaxDegAnchor'],t['treesMaxDegUndecided'],t['nodes']))
    for l in lines[n][:20]: print("   ",l)
