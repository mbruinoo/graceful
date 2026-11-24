#!/usr/bin/env python3
# rootcount.py N -- number of rooted trees on n vertices (= pairs (tree, vertex orbit)) by root degree, and the
# same with no leaf child of the root, from the generating function  prod_k (1 - y x^k)^(-r(k))  (r = A000081).
# Used to check, independently of the tree generator and of the orbit reduction, that the scans tested the
# right number of vertex orbits.
import sys
from math import comb
N=int(sys.argv[1])
r=[0,1]                                  # r[n] rooted trees on n vertices (Euler transform)
for n in range(2,N+1):
    s=0
    for k in range(1,n):
        s+=sum(d*r[d] for d in range(1,k+1) if k%d==0)*r[n-k]
    r.append(s//(n-1))
def bydeg(kmin):
    # P[t][d] = number of multisets of d rooted trees with t vertices in total, each tree with >= kmin vertices
    P=[[0]*(N+1) for _ in range(N+1)]; P[0][0]=1
    for k in range(kmin,N):
        Q=[[0]*(N+1) for _ in range(N+1)]
        for t in range(N):
            for d in range(N):
                if P[t][d]:
                    j=0
                    while t+j*k<N and d+j<=N:
                        Q[t+j*k][d+j]+=P[t][d]*comb(r[k]+j-1,j); j+=1
        P=Q
    return P
A=bydeg(1); B=bydeg(2)
for n in range(14,N+1):
    print("n=%d rooted trees %d | root degree 2: %d  3: %d  >=4: %d | no leaf child: degree 2: %d  3: %d  >=4: %d"%(
        n,r[n],A[n-1][2],A[n-1][3],sum(A[n-1][4:]),B[n-1][2],B[n-1][3],sum(B[n-1][4:])))
