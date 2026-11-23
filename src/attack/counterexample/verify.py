# Independent check of certificates, straight from README sections 1-2.
# stdin: alternating lines  "<n u v u v ...>"  and  "labels: l_0 ... l_{n-1}"   (or one line "tree | labels")
# Checks: labels are 1..n once each; the n-1 edge lengths |l_u-l_v| are 1..n-1 once each (a placement drawing the
# tree); for every k the brackets of length >= k form a connected graph (growth placement).
# With argument "root0": additionally vertex 0 has label 1.
import sys
root0 = len(sys.argv)>1 and sys.argv[1]=="root0"
ok=bad=0
for l in sys.stdin:
    if "|" not in l: continue
    t,lab=l.split("|"); t=list(map(int,t.split())); lab=list(map(int,lab.split()))
    n=t[0]; E=list(zip(t[1::2],t[2::2])); good = len(E)==n-1 and sorted(lab)==list(range(1,n+1))
    if good:
        lens=sorted(abs(lab[a]-lab[b]) for a,b in E); good = lens==list(range(1,n))
    if good:
        byl={abs(lab[a]-lab[b]):(lab[a],lab[b]) for a,b in E}
        used=set(byl[n-1])
        for k in range(n-2,0,-1):
            a,b=byl[k]
            if (a in used)==(b in used): good=False; break
            used|={a,b}
    if good and root0 and lab[0]!=1: good=False
    if good: ok+=1
    else: bad+=1; print("BAD",l.strip())
print("certificates checked: ok=%d bad=%d"%(ok,bad))
