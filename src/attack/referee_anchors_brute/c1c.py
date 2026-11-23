# explicit witness families of H3, verified from the growth definition for odd 11<=m<=1501
from lib import check_growth
def tree(m):
    k=m-5; e=[(0,1),(0,2),(0,3),(1,4),(2,5)]+[(3,6+i) for i in range(k)]; return m+1,e   # 1,2 small hubs; 3 big
def wit(m,kind):
    n,e=tree(m); lab=[None]*n; lab[0]=0
    if kind=='4':
        b=(m-1)//2; c=m-1; w1=(b-1)//2; w0=w1+1
        lab[1]=m; lab[4]=m-w0; lab[2]=b; lab[5]=b+w1; lab[3]=c; skip={m,b,c,w0,w1}; big=lambda w:c-w
    elif kind=='3':
        b=(2*m-3)//3; c=m-1; w1=m//3; w0=b+1
        lab[1]=m; lab[4]=m-w0; lab[2]=b; lab[5]=b-w1; lab[3]=c; skip={m,b,c,w0,w1}; big=lambda w:c-w
    else:
        b=2*m//5; c=4*m//5
        lab[3]=m; lab[1]=b; lab[4]=b+m//5; lab[2]=c; lab[5]=c-3*m//5; skip={m,b,c,m//5,3*m//5}; big=lambda w:m-w
    ws=[w for w in range(1,m+1) if w not in skip]
    if len(ws)!=m-5: return False
    for i,w in enumerate(ws): lab[6+i]=big(w)
    if any(x is None or x<0 or x>m for x in lab): return False
    return check_growth(n,0,e,lab)
bad=[];cnt=0
for m in range(11,1502,2):
    for kind,cond in (('4',m%4==3),('3',m%3==0),('5',m%5==0)):
        if cond:
            cnt+=1
            if not wit(m,kind): bad.append((m,kind))
print("witness checks",cnt,"failures",bad[:20])
