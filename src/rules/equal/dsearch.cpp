// Deal searcher for k equal legs of length L, straight from the definition.
// env ZIG=1: zigzag only.  ALPHA=1: zigzag and every odd-position label > lam >= every even-position label, lam = k*floor(L/2).
// usage: dsearch k L [limit]
#include <bits/stdc++.h>
using namespace std;
int k,L,m,lam; int cnt_[64],cur[64]; bool used[1024]; vector<int> w[64],lab[64]; long long nodes,LIMIT=50000000; bool ZIG,ALPHA;
int rec(int t){ if(t==0) return 1; if(++nodes>LIMIT) return -1;
  for(int i=0;i<k;i++){ if(cnt_[i]==L) continue; if(cnt_[i]==0 && i>0 && cnt_[i-1]==0) continue;
    for(int sg=0;sg<2;sg++){ int x;
      if(cnt_[i]==0){ if(sg) continue; x=t; }
      else if(ZIG||ALPHA){ if(sg) continue; x=(cnt_[i]%2==0)?cur[i]+t:cur[i]-t; }
      else x= sg==0?cur[i]-t:cur[i]+t;
      if(x<1||x>m||used[x]) continue;
      if(ALPHA){ if(cnt_[i]%2==0 && x<=lam) continue; if(cnt_[i]%2==1 && x>lam) continue; }
      int old=cur[i]; cur[i]=x; used[x]=1; cnt_[i]++; w[i].push_back(t); lab[i].push_back(x);
      int r=rec(t-1); if(r==1) return 1;
      lab[i].pop_back(); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; if(r<0) return -1; } }
  return 0; }
int main(int argc,char**argv){ k=atoi(argv[1]); L=atoi(argv[2]); if(argc>3) LIMIT=atoll(argv[3]); ZIG=getenv("ZIG"); ALPHA=getenv("ALPHA");
  m=k*L; lam=k*(L/2); int r=rec(m); printf("k=%d L=%d %s nodes=%lld\n",k,L,r==1?"found":r==0?"none":"unresolved",nodes);
  if(r==1) for(int i=0;i<k;i++){ printf("  labels:"); for(int x:lab[i]) printf(" %d",x); printf("   edges:"); for(int x:w[i]) printf(" %d",x); printf("\n"); } }
