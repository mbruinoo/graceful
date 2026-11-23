// Closure of clean leaf insertion (README Lemma 8) from the single edge, vs all growth placements.
// Usage: closure N
#include "enum.h"
int main(int argc,char**argv){ int N=atoi(argv[1]);
  unordered_set<u64> reach; { Pl p; p.n=2; p.pos[1]=1; reach.insert(enc(p)); }
  for(int n=2;n<=N;n++){
    // stats at size n
    set<string> allT, reachT; long total=0, prim=0, primReachable=0; map<string,long> primT;
    long nonconf=0;
    enumGrowth(n,[&](const Pl&p){ total++; string c=canon(p); allT.insert(c); if(reach.count(enc(p))) reachT.insert(c); });
    printf("n=%d growth=%ld trees=%zu peelable_placements=%zu trees_reached=%zu\n",n,total,allT.size(),reach.size(),reachT.size());
    if(n<=10) for(auto&c:allT) if(!reachT.count(c)) printf("   missed %s\n",c.c_str());
    fflush(stdout);
    if(n==N) break;
    unordered_set<u64> nx;
    for(u64 x:reach){ Pl p=dec(x,n),q; for(int i=0;i<=n;i++){ if(cutHeight(p,i)<0) continue; for(int d=-1;d<=1;d+=2) if(insertLeaf(p,i,d,q)) nx.insert(enc(q)); } }
    reach.swap(nx); }
}
