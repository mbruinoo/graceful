# sample_summary.py trees.txt results.out [results2.out ...] -- tidy numbers of a sample against the invariants of
# invariants.py.  Several result files for the same trees are merged (largest lb, smallest ub).
import sys, collections, lib
from invariants import invs, spearman
trees=[l for l in open(sys.argv[1]) if l.strip()]
R=[lib.read_results(f) for f in sys.argv[2:]]
for r in R: assert len(r)==len(trees),(len(r),len(trees))
rows=[]
for i,t in enumerate(trees):
    n,E,adj=lib.parse(t); lb=max(r[i]['lb'] for r in R); ubs=[r[i]['ub'] for r in R if r[i]['ub'] is not None]
    if not ubs: continue
    d=invs(n,adj); d.update(n=n,lb=lb,ub=min(ubs)); rows.append(d)
m=len(rows); ex=sum(1 for r in rows if r['lb']==r['ub'])
print(f'{sys.argv[1]}: {m} trees, n = {min(r["n"] for r in rows)}..{max(r["n"] for r in rows)}; exact for {ex}')
print('  best found (ub): mean %.2f  min %d  max %d   distribution %s'%(sum(r['ub'] for r in rows)/m,min(r['ub'] for r in rows),max(r['ub'] for r in rows),dict(sorted(collections.Counter(r['ub'] for r in rows).items()))))
print('  proved lower bound (lb): mean %.2f   distribution %s'%(sum(r['lb'] for r in rows)/m,dict(sorted(collections.Counter(r['lb'] for r in rows).items()))))
print('  share of non-staircase steps: mean ub/(n-2) = %.3f'%(sum(r['ub']/(r['n']-2) for r in rows)/m))
for nm in ('leaves_minus_2','branch_vertices','derived_leaves_minus_2','off_spine','max_branches','derived_branch_vertices'):
    print(f'  {nm:26s} mean {sum(r[nm] for r in rows)/m:6.2f}   Spearman rho with ub = {spearman([r["ub"] for r in rows],[r[nm] for r in rows]):.2f}')
