// Deals for k equal legs of length L with at most R "runs".  A run = maximal stretch of consecutive numbers
// t, t-1, t-2, ... handed to the same leg with alternating directions.   usage: runsearch k L R [all]
#include <bits/stdc++.h>
using namespace std;
int k,L,m,R; int cnt_[64],cur[64],ldir[64]; bool used[2048]; vector<int> w[64],lab[64]; long long nodes,found=0; bool ALL=false; long long LIMIT=2000000000LL;
void show(){ for(int i=0;i<k;i++){ printf("  labels:"); for(int x:lab[i]) printf(" %3d",x); printf("   edges:"); for(int x:w[i]) printf(" %3d",x); printf("\n"); } }
int rec(int t,int prev,int runs){ if(t==0){ found++; if(ALL){ printf("deal %lld runs=%d\n",found,runs); show(); return 0;} show(); return 1; } if(++nodes>LIMIT) return -1;
  for(int i=0;i<k;i++){ if(cnt_[i]==L) continue; int c=cnt_[i]; if(c==0 && i>0 && cnt_[i-1]==0) continue;
    for(int sg=0;sg<2;sg++){ int x,d; if(c==0){ if(sg) continue; x=t; d=1; } else { d= sg==0?-1:1; x=cur[i]+d*t; }
      if(x<1||x>m||used[x]) continue;
      int nr=runs + ((i==prev && d==-ldir[i])?0:1); if(nr>R) continue;
      int old=cur[i],od=ldir[i]; cur[i]=x; ldir[i]=d; used[x]=1; cnt_[i]++; w[i].push_back(t); lab[i].push_back(x);
      int r=rec(t-1,i,nr);
      lab[i].pop_back(); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; ldir[i]=od; if(r==1) return 1; if(r<0) return -1; } }
  return 0; }
int main(int argc,char**argv){ k=atoi(argv[1]); L=atoi(argv[2]); R=atoi(argv[3]); ALL=argc>4; m=k*L;
  int r=rec(m,-1,0); if(ALL){ printf("k=%d L=%d R=%d total=%lld\n",k,L,R,found); return 0; }
  printf("k=%d L=%d R=%d %s nodes=%lld\n",k,L,R,r==1?"found":r==0?"none":"unresolved",nodes); }
