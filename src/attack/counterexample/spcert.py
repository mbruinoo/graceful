# spdlx output -> certificates "tree | labels" (labels 1..n, centre = vertex 0 with label 1) for verify.py root0
import sys
for l in sys.stdin:
    if " OK legs:" not in l: 
        print("NOT-OK",l.strip(),file=sys.stderr); continue
    legs=[list(map(int,p.split(","))) for p in l.split("legs:")[1].split()]
    E=[]; lab=[1]; v=1
    for leg in legs:
        prev=0
        for x in leg: E.append((prev,v)); lab.append(x+1); prev=v; v+=1
    print(v," ".join("%d %d"%e for e in E),"|"," ".join(map(str,lab)))
