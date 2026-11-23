# Abstract reachability for the insertion calculus (see NOTES in rule.py).  State (M,N,Sigma): there is a closed
# structure on the labels M+1..N whose set of split thresholds contains Sigma.
# Usage: calculus.py Nmax
import sys
from collections import defaultdict
Nmax=int(sys.argv[1])
st=defaultdict(set)   # (M,N) -> set of frozenset Sigma
def add(M,N,S):
    if N>Nmax: return False
    S=frozenset(S)
    for S2 in st[(M,N)]:
        if S<=S2: return False
    st[(M,N)]={S2 for S2 in st[(M,N)] if not S2<=S}|{S}
    return True
for M in range(0,Nmax+1):
    add(M,M,{M}); add(M,5*M+2,{5*M+2})
changed=True
while changed:
    changed=False
    for (M,N),sets in list(st.items()):
        for S in list(sets):
            # SL
            if N%2==0 and N//2 in S and N//2>=M: changed|=add(M,3*N+6,{3*N//2+3,3*N+6})
            # BL(t)
            for T in S:
                t=2*T-N
                if t>=0: changed|=add(M,N+4*t+2,{N+4*t+2})
            # insert interval cap at T
            for T in S:
                for (M2,N2),sets2 in list(st.items()):
                    if M2!=T or N2==M2: continue
                    d=N2-M2
                    if N+d>Nmax: continue
                    for S2 in list(sets2):
                        changed|=add(M,N+d,{s+d for s in S if s>=T}|set(S2))
ks=sorted(N//2 for (M,N) in st if M==0 and st[(M,N)])
print("reachable k:",ks)
print("missing valid k:",[k for k in range(1,Nmax//2+1) if k%3!=2 and k not in ks])
