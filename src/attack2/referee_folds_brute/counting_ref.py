# referee: recompute Theorem F4 bound table independently
from math import comb, log
N=110
r=[0]*(N+1); r[1]=1   # rooted trees A000081
for m in range(1,N):
    s=0
    for k in range(1,m+1):
        d_sum=sum(d*r[d] for d in range(1,k+1) if k%d==0)
        s+=d_sum*r[m-k+1]
    r[m+1]=s//m
t=[0]*(N+1)
for m in range(1,N+1):
    v=r[m]-sum(r[i]*r[m-i] for i in range(1,m) if 2*i<m)
    if m%2==0: v-=r[m//2]*(r[m//2]-1)//2
    t[m]=v
print("t_n check", [t[m] for m in range(1,19)])
def builds(n,K): return sum(comb(n-2,j)*(2*n)**j*2**(n-2-j) for j in range(0,K+1))
for n in [14,16,18,20,25,30,40,50,70,100]:
    # K_all: smallest K such that builds(n,K) >= t_n ; then some tree has tidy >= K_all... some tree has tidy > K whenever builds(n,K) < t_n
    Kall=0
    while builds(n,Kall) < t[n]: Kall+=1
    # at least half have tidy >= K  iff builds(n,K-1) <= t_n/2 (bound); largest such K
    Kh=0
    while builds(n,Kh) <= t[n]/2: Kh+=1
    print(n, "t_n=%d"%t[n], "K_all(some tree has tidy>=)=",Kall, "K_half=",Kh)
a=2.955765285651994974714817524
print("ln(alpha/2)/2 =", log(a/2)/2, " log2 alpha=", log(a,2))
