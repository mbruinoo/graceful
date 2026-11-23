import sys
d={}
for line in open(sys.argv[1]):
    a=line.split(); d[int(a[0])]=int(a[1])
f=lambda m:(m%3==2)+(m%9==5)+(m%5==4)+(m%7==3)
bad=[(m,d[m],f(m)) for m in d if m>=21 and d[m]!=f(m)]
print("m range",min(d),max(d),"formula mismatches for m>=21:",bad)
crit=lambda m:(m%3==2) or (m%5==4) or (m%7==3)
print("anchor-criterion mismatches m>=15:",[m for m in d if m>=15 and (d[m]>0)!=crit(m)])
print("small m (4..20) count vs formula:",[(m,d[m],f(m)) for m in range(4,21)])
print("anchor-criterion mismatches m<15:",[(m,d[m]) for m in d if m<15 and (d[m]>0)!=crit(m)])
print("max",max(d.values()),[m for m in d if d[m]==max(d.values())])
print("zero check:",[(m,d[m]) for m in (15,16,18,21,22,25,27,28,30)])
# theorem families
print("family members with zero count:",[m for m in d if m>=5 and crit(m) and d[m]==0])
nz=sum(1 for m in d if m>=15 and d[m]==0); print("non-anchor fraction m>=15:",nz/sum(1 for m in d if m>=15), 48/105)
