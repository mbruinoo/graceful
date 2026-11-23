// print all growth placements on n vertices: peelable flag, edges longest first, clean cut heights, tree
#include "enum.h"
int main(int argc,char**argv){ int N=atoi(argv[1]);
  unordered_set<u64> reach; { Pl p; p.n=2; p.pos[1]=1; reach.insert(enc(p)); }
  for(int n=2;n<N;n++){ unordered_set<u64> nx;
    for(u64 x:reach){ Pl p=dec(x,n),q; for(int i=0;i<=n;i++){ if(cutHeight(p,i)<0) continue; for(int d=-1;d<=1;d+=2) if(insertLeaf(p,i,d,q)) nx.insert(enc(q)); } }
    reach.swap(nx); }
  enumGrowth(N,[&](const Pl&p){ printf("%c ",reach.count(enc(p))?'P':'-'); for(int k=N-1;k>=1;k--) printf("%d-%d ",p.pos[k],p.pos[k]+k);
    printf(" cuts:"); for(int i=1;i<N;i++){ int c=cutHeight(p,i); if(c<0) printf(" ."); else printf(" %d",c);} printf("  %s\n",canon(p).c_str()); });
}
