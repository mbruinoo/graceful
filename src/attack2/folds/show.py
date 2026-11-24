# show.py trees.txt results.out [idx ...] -- draw builds on the number line.  One row per step:
#   tape before the step ('#' used, '.' unused), the bracket (x fresh, y used), step type, cost.
# Step types (names in REPORT.txt section 3):  S staircase | K skip (split of the main run) | B back | F fill of a hole
import sys, lib
def stype(s):
    if s['inM']:
        if s['r']==0: return 'S'
        if s['c']==0: return 'B'
        return 'K%d'%min(s['r'],s['c']) + ('' if s['r']<=s['c'] else '*')
    own=s['own']; m=own[1]-own[0]+1
    if m==1: return 'F'
    if s['r']==0: return 'Fs'      # staircase step inside a hole of size > 1
    if s['c']==0: return 'Fb'
    return 'Fk'
if __name__=='__main__':
    trees=[l for l in open(sys.argv[1]) if l.strip()]; res=lib.read_results(sys.argv[2])
    for i in map(int,sys.argv[3:]):
        n,E,adj=lib.parse(trees[i]); r=res[i]; f=r['labels']; steps=lib.replay(n,E,f)
        print('tree',i,'n',n,'cost',r['ub'],'exact' if r['exact'] else 'lb=%d'%r['lb'],' code',lib.canon(adj))
        used=[False]*(n+2); used[1]=used[n]=True
        for s in steps:
            tape=''.join('#' if used[i] else '.' for i in range(1,n+1))
            row=list(tape); row[s['x']-1]='x'; row[s['y']-1]='Y'
            print('  t=%3d  %s   x=%3d y=%3d  H=%d  %-4s deg(parent)=%d'%(s['t'],''.join(row),s['x'],s['y'],s['H'],stype(s),len(adj[s['parent']])))
            used[s['x']]=True
