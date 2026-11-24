# cross.py trees.txt tidyA.out tidyB.out brute.out -- compare tidy.cpp (tree by tree) with brute.cpp (all placements),
# and re-verify every labeling and its cost in Python from the definition.
import sys, lib
trees=[l for l in open(sys.argv[1]) if l.strip()]
A=lib.read_results(sys.argv[2]); B=lib.read_results(sys.argv[3])
br={}
for l in open(sys.argv[4]):
    c,a,b,cnt=l.split(); br[c]=(int(a),int(b))
assert len(trees)==len(A)==len(B)==len(br),(len(trees),len(A),len(B),len(br))
bad=0
for t,ra,rb in zip(trees,A,B):
    n,E,adj=lib.parse(t); c=lib.canon(adj)
    assert ra['exact'] and rb['exact']
    sa=lib.replay(n,E,ra['labels']); sb=lib.replay(n,E,rb['labels'])
    assert sum(s['costA'] for s in sa)==ra['ub'] and sum(s['costB'] for s in sb)==rb['ub']
    if br[c]!=(ra['ub'],rb['ub']): bad+=1; print('MISMATCH',c,br[c],ra['ub'],rb['ub'])
print(sys.argv[1],'trees',len(trees),'mismatches',bad)
