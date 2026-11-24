# tables.py -- prints the summary tables of REPORT.txt from the result files in data/ (run from this directory).
import lib, collections, os, re
def merged(treefile,files):
    T=[l for l in open(treefile) if l.strip()]; R=[lib.read_results(f) for f in files if os.path.exists(f)]
    out=[]
    for i in range(len(T)):
        rs=[r[i] for r in R if i<len(r)]
        if not rs: continue
        ubs=[r['ub'] for r in rs if r['ub'] is not None]; out.append((max(r['lb'] for r in rs),min(ubs) if ubs else None,int(lib.parse(T[i])[0])))
    return out
def line(name,rows):
    m=len(rows); f=[r for r in rows if r[1] is not None]; ex=sum(1 for r in f if r[0]==r[1])
    if not f: print(f'  {name}: {m} trees, nothing found'); return
    print(f'  {name:26s} trees {m:4d}  exact {ex:4d}  no build found {m-len(f):2d}   lb mean {sum(r[0] for r in rows)/m:5.2f}   best found: mean {sum(r[1] for r in f)/len(f):5.2f} min {min(r[1] for r in f)} max {max(r[1] for r in f)}'
          f'   mean share of steps {sum(r[1]/(r[2]-2) for r in f)/len(f):.3f}   dist {dict(sorted(collections.Counter(r[1] for r in f).items()))}')
print('RANDOM TREES (uniform labelled, gen.py random n count n):')
for n in (20,25,30,40,70,100):
    line(f'n={n} cost A',merged(f'pop/random_{n}.txt',[f'data/random_A_{n}.txt',f'data/random_A_{n}_beam.txt']))
    line(f'n={n} cost B',merged(f'pop/random_{n}.txt',[f'data/random_B_{n}.txt']))
print('SYMMETRIC TREES:')
line('n<=30 (418) cost A',merged('pop/sym_small.txt',['data/sym_small_A.txt'])); line('n<=30 (418) cost B',merged('pop/sym_small.txt',['data/sym_small_B.txt']))
for s,lab in (('a','n=31..46'),('b','n=53..73'),('c','n=85..100')):
    if os.path.exists(f'data/sym_large_{s}_A.txt'): line(f'{lab} cost A',merged(f'pop/sym_large_{s}.txt',[f'data/sym_large_{s}_A.txt']))
    if os.path.exists(f'data/sym_large_{s}_B.txt'): line(f'{lab} cost B',merged(f'pop/sym_large_{s}.txt',[f'data/sym_large_{s}_B.txt']))
print('RULES on samples (existence of a build obeying the rule; found / proved none / undecided):')
for name,tf,pat in (('sym n<=30','pop/sym_small.txt','data/sym_small_rule%d.txt'),('sym n=31..100','pop/sym_large.txt','data/sym_large_rule%d.txt'),('hubs n=31..70','pop/hubs_31_70.txt','data/hubs_rule%d.txt'),
                    ('random 40','pop/random_40.txt','data/random_40_rule%d.txt'),('random 70','pop/random_70.txt','data/random_70_rule%d.txt'),('random 100','pop/random_100.txt','data/random_100_rule%d.txt'),
                    ('random 40 x300','pop/random_40_x300.txt','data/random_40_x300_rule%d.txt'),('random 70 x300','pop/random_70_x300.txt','data/random_70_x300_rule%d.txt'),('random 100 x300','pop/random_100_x300.txt','data/random_100_x300_rule%d.txt')):
    for R in (1,3,5,17,33,19,35,37,49,51):
        f=pat%R
        if not os.path.exists(f): continue
        res=lib.read_results(f); nT=sum(1 for l in open(tf) if l.strip())
        fo=sum(1 for r in res if r['ub'] is not None); no=sum(1 for r in res if r['ub'] is None and r['exact']); un=sum(1 for r in res if r['ub'] is None and not r['exact'])
        print(f'  {name:16s} RULE={R:2d}: {fo:4d} found / {no:3d} none / {un:3d} undecided   (of {nT}; {len(res)} run)')
