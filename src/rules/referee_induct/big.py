import sys, random
exec(open('/home/user/graceful/src/rules/referee_induct/ref.py').read().split("def check(")[0])
random.seed(7)
deals = {m: enum_deals(m) for m in range(0, 14)}
print({m: len(d) for m, d in deals.items()})
# exhaustive pairs m,n <= 9 beyond claimed (either index 9)
c = 0
for m in range(0, 10):
    for n in range(0, 10):
        if m < 9 and n < 9: continue
        for DS in deals[m]:
            for DT in deals[n]:
                o = fatten(DS, DT); ok, why = valid(o, m + (2*m+1)*n)
                if not ok: print("FAIL", DS, DT, why); sys.exit(1)
                c += 1
print("exhaustive pairs with max(m,n)=9:", c)
c = 0
for _ in range(20000):
    m = random.randint(0, 13); n = random.randint(0, 13)
    DS = random.choice(deals[m]); DT = random.choice(deals[n])
    o = fatten(DS, DT); ok, why = valid(o, m + (2*m+1)*n)
    if not ok: print("FAIL", DS, DT, why); sys.exit(1)
    c += 1
print("random pairs m,n<=13:", c, "ok")
