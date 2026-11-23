# paren string -> "n u v u v ..." edge list.  usage: fam.py '<paren>' ...   or import
import sys
def edges(s):
    E=[]; cnt=[0]
    def parse(i,pa):
        v=cnt[0]; cnt[0]+=1
        if pa is not None: E.append((pa,v))
        i+=1
        while s[i]=='(': i=parse(i,v)
        return i+1
    parse(0,None)
    return cnt[0],E
def line(s):
    n,E=edges(s); return str(n)+" "+" ".join("%d %d"%e for e in E)
hub=lambda k:"("+"()"*k+")"
path=lambda k:"("*k+")"*k
if __name__=="__main__":
    for s in sys.argv[1:]: print(line(s))
