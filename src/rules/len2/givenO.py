# Given the outer set O (python expression in n on the command line), find bijections d by DFS and print a few.
# Usage: givenO.py n "expr for O as list" N_expr [count]
import sys
sys.setrecursionlimit(10000)
n=int(sys.argv[1]); O=sorted(set(eval(sys.argv[2]))); N=eval(sys.argv[3]); cnt=int(sys.argv[4]) if len(sys.argv)>4 else 3
I=sorted(set(range(1,N+1))-set(O)); assert len(I)==len(O), (len(I),len(O))
print("O=",O,"sumO",sum(O),"sumI",sum(I))
Oset=set(O); d={}; used=set(); found=0
def rec(i):
    global found
    if i<0:
        found+=1; print(" d:",[(o,d[o]) for o in O]); 
        if found>=cnt: sys.exit()
        return
    s=I[i]
    for o in O:
        if o>=s: break
        x=s-o
        if o in d or x in used or x not in Oset: continue
        d[o]=x; used.add(x); rec(i-1); del d[o]; used.discard(x)
rec(len(I)-1)
print("found",found)
