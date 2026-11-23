// Forward closure C(2): start from the single edge; a step opens ONE or TWO gaps in a growth placement and adds one new
// vertex per gap, such that (a) every old bracket keeps its rank among the old brackets ("clean set"), (b) each new bracket
// has a foot on a new label, (c) the result is a growth placement (checked by definition).
// Independent of restrict.cpp (which works backwards by deleting labels).  Usage: fwd N [K=2]
#include "enum.h"
int main(int argc,char**argv){ int N=atoi(argv[1]); int K=argc>2?atoi(argv[2]):2;
  vector<unordered_set<u64>> C(N+3); { Pl p; p.n=2; p.pos[1]=1; C[2].insert(enc(p)); }
  for(int n=2;n<=N;n++){
    { set<string> T; for(u64 x:C[n]) T.insert(canon(dec(x,n))); printf("n=%d C(%d) placements=%zu trees=%zu\n",n,K,C[n].size(),T.size()); fflush(stdout); }
    if(n==N) break;
    for(u64 x:C[n]){ Pl p=dec(x,n),q;
      // one gap
      for(int i=0;i<=n;i++) for(int d=-1;d<=1;d+=2) if(insertLeaf(p,i,d,q)) C[n+1].insert(enc(q));
      if(K<2||n+2>N) continue;
      // two gaps g1<=g2 (cuts 0..n); new labels L1=g1+1, L2=g2+2
      for(int g1=0;g1<=n;g1++) for(int g2=g1;g2<=n;g2++){ q.n=n+2; int last=0; bool ok=true; bool have[24]={0};
        for(int k=1;k<n&&ok;k++){ int a=p.pos[k], b=a+k; a+=(a>g1)+(a>g2); b+=(b>g1)+(b>g2); int len=b-a; if(len<=last){ ok=false; break; } last=len; have[len]=1; q.pos[len]=a; }
        if(!ok) continue; int f[2],nf=0; for(int k=1;k<=n+1;k++) if(!have[k]){ if(nf<2) f[nf]=k; nf++; } if(nf!=2) continue;
        int L1=g1+1, L2=g2+2; int cand1[4]={L1-f[0],L1,L2-f[0],L2}, cand2[4]={L1-f[1],L1,L2-f[1],L2};
        for(int a=0;a<4;a++){ int p1=cand1[a]; if(p1<1||p1+f[0]>n+2) continue; for(int b=0;b<4;b++){ int p2=cand2[b]; if(p2<1||p2+f[1]>n+2) continue;
          q.pos[f[0]]=p1; q.pos[f[1]]=p2; if(isGrowth(q)) C[n+2].insert(enc(q)); } } } } }
}
