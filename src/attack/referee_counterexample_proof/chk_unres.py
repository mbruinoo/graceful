import sys
from chk import growth
want=set(" ".join(l.split()) for l in open("../counterexample/unresolved_all.txt") if l.strip())
logs=set()
for f in "run_eq.log run_eqp.log run_eq2.log run_sym.log run_spider.log run_comb.log".split():
    for l in open("../counterexample/"+f):
        if l.startswith("UNRESOLVED:"): logs.add(" ".join(l.split()[1:]))
print("unresolved_all.txt distinct=%d ; UNRESOLVED lines in six logs distinct=%d ; same set=%s"%(len(want),len(logs),want==logs))
ok=bad=0; got=set()
for l in sys.stdin:
    if "|" not in l: continue
    t,lab=l.split("::")[-1].split("|"); t=list(map(int,t.split())); lab=list(map(int,lab.split()))
    n=t[0]; E=list(zip(t[1::2],t[2::2]))
    if growth(n,E,lab): ok+=1; got.add(" ".join(map(str,t)))
    else: bad+=1
print("hubsolve3 certificates: ok=%d bad=%d ; unresolved trees covered=%d of %d"%(ok,bad,len(got&want),len(want)))
