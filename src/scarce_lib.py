def build(s):
    E=[]; cnt=[0]
    def parse(i,pa):
        v=cnt[0]; cnt[0]+=1
        if pa is not None: E.append((pa,v))
        i+=1
        while s[i]=='(' : i=parse(i,v)
        return i+1
    if '|' in s:
        a,b=s.split('|'); 
        s=a; parse(0,None); r2=cnt[0]; s=b; parse(0,None); E.append((0,r2))
    else: parse(0,None)
    return cnt[0],E
