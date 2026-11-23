# outer 3-fold stacking of an inner design of size k2 with total inner gap gam (Delta width k2+2gam, Pi width k2+gam)
import itertools,sys
def outer(k2,gam,Gmax):
    wd=k2+2*gam; wp=k2+gam; out=[]
    for G1 in range(Gmax+1):
        for G2 in range(Gmax+1):
            D=(0,wd+2*G1,2*wd+2*G1+2*G2); P=(0,wp+G1,2*wp+G1+G2)
            for a in itertools.permutations(range(3)):
                for b in itertools.permutations(range(3)):
                    s={ i*k2+D[a[i]]+P[b[i]] for i in range(3)}
                    if len(s)==1: out.append((G1,G2,a,b,s.pop()))
    return out
for k2 in eval(sys.argv[1]):
    for gam in (0,1):
        print(k2,gam,[(G1,G2,a,b,K,(K)%3) for G1,G2,a,b,K in outer(k2,gam,3*k2)])
