// Generalised deal G_t(k,L): centre 0, k legs of length L, labels AND edge lengths are both exactly the set [t+1, t+kL];
// edge lengths strictly decreasing outward, first move up from 0, later moves up or down.  (t=0 is the ordinary deal.)
// env ZIG=1 forces alternation.  usage: gt k L t [show]
#include <bits/stdc++.h>
using namespace std;
int k,L,m,T; int cnt_[64],cur[64]; bool used[4096]; vector<int> w[64],lab[64]; long long nodes,LIMIT=30000000; bool ZIG;
int rec(int e){ if(e==T) return 1; if(++nodes>LIMIT) return -1;
  for(int i=0;i<k;i++){ if(cnt_[i]==L) continue; if(cnt_[i]==0 && i>0 && cnt_[i-1]==0) continue;
    for(int sg=0;sg<2;sg++){ int x; if(cnt_[i]==0){ if(sg) continue; x=e; } else if(ZIG){ if(sg) continue; x=(cnt_[i]%2==0)?cur[i]+e:cur[i]-e; } else x= sg==0?cur[i]-e:cur[i]+e;
      if(x<T+1||x>T+m||used[x]) continue;
      int old=cur[i]; cur[i]=x; used[x]=1; cnt_[i]++; w[i].push_back(e); lab[i].push_back(x);
      int r=rec(e-1); if(r==1) return 1;
      lab[i].pop_back(); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; if(r<0) return -1; } }
  return 0; }
int main(int argc,char**argv){ k=atoi(argv[1]); L=atoi(argv[2]); T=atoi(argv[3]); ZIG=getenv("ZIG"); m=k*L; int r=rec(T+m);
  printf("%s",r==1?"f":r==0?".":"?"); if(argc>4 && r==1){ printf("\n"); for(int i=0;i<k;i++){ printf("  labels:"); for(int x:lab[i]) printf(" %d",x); printf("   edges:"); for(int x:w[i]) printf(" %d",x); printf("\n"); } } }
