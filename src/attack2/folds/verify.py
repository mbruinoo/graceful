# verify.py [--rule R] trees.txt results.out [A|B]  -- independent re-check (Python, shares no code with tidy.cpp).
# For every line with a labeling: (1) it is a growth placement by the definition (lib.replay: labels are a
# permutation of 1..n, lengths 1..n-1 once each, every bracket taken longest first has exactly one used foot);
# (2) its number of non-staircase steps (cost A or B) equals the reported ub;  (3) with --rule R: the build obeys
# the vocabulary RULE=R of tidy.cpp, re-implemented here from the description in REPORT.txt section 5.
import sys, lib
from verify_rule import obeys
args=sys.argv[1:]; R=0
if args[0]=='--rule': R=int(args[1])|1; args=args[2:]
trees=[l for l in open(args[0]) if l.strip()]; res=lib.read_results(args[1]); mode=args[2] if len(args)>2 else 'A'
assert len(trees)==len(res),(len(trees),len(res))
ok=0; none=0; bad=0
for t,r in zip(trees,res):
    if r['labels'] is None:
        none+=1; continue
    n,E,adj=lib.parse(t); steps=lib.replay(n,E,r['labels'])
    if R:
        good,why=obeys(n,steps,R)
        if not good: bad+=1; print('RULE VIOLATION tree',r['idx'],why)
    else:
        c=sum(s['cost'+mode] for s in steps)
        if c!=r['ub']: bad+=1; print('COST MISMATCH tree',r['idx'],c,r['ub'])
    ok+=1
print(f'{args[1]}: {len(res)} lines, {ok} labelings re-checked from the definition'+(f' and against RULE={R}' if R else f' (cost {mode})')+f', {none} without labeling, {bad} problems')
