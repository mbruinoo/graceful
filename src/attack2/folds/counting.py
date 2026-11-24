# counting.py -- the counting bound of REPORT.txt section 6 (Theorem F4).
# builds(n,K) = sum_{j<=K} C(n-2,j) (2n)^j 2^(n-2-j) bounds the number of growth placements on n cells with at most K
# non-staircase steps (cost A); trees(n) = number of trees on n vertices (computed here from the classical recurrences
# for rooted trees and Otter's formula; checked against 1,1,1,2,3,6,11,23,47,106,235,551,1301,3159).
# Prints, for each n: K_all = least K with builds(n,K) >= trees(n)   (so SOME tree on n vertices has tidy_A >= K_all),
#                     K_half = least K with builds(n,K) >= trees(n)/2 (so at least half of all trees have tidy_A >= K_half).
from math import comb
def tree_counts(N):
    r=[0]*(N+1); r[1]=1
    for n in range(1,N):
        s=0
        for d in range(1,n+1):
            sd=sum(k*r[k] for k in range(1,d+1) if d%k==0)      # sum over divisors k of d of k*r[k]
            s+=sd*r[n-d+1]
        r[n+1]=s//n
    t=[0]*(N+1)
    for n in range(1,N+1):
        # Otter: t_n = r_n - (1/2) sum_{i+j=n} r_i r_j + (1/2) r_{n/2} [n even]
        s2=sum(r[i]*r[n-i] for i in range(1,n))
        t[n]=r[n]-(s2-(r[n//2] if n%2==0 else 0))//2
    return t
t=tree_counts(120)
assert t[1:15]==[1,1,1,2,3,6,11,23,47,106,235,551,1301,3159], t[1:15]
def builds(n,K): return sum(comb(n-2,j)*(2*n)**j*2**(n-2-j) for j in range(K+1))
print(' n   trees(n)          K_all  K_half')
for n in (10,14,16,18,20,25,30,40,50,70,100):
    Ka=next(K for K in range(n) if builds(n,K)>=t[n]); Kh=next(K for K in range(n) if 2*builds(n,K)>=t[n])
    print(f'{n:3d}  {t[n]:<18.6g} {Ka:3d}   {Kh:3d}')
