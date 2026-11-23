// Deals for k equal legs of length L in which every leg's edge lengths at positions Q1..L-Q2 form an
// arithmetic progression with difference STEP (default k) (free signs).  usage: apsearch k L Q1 Q2 [limit] [all]
#include <bits/stdc++.h>
using namespace std;
int k,L,m,Q1,Q2,STEP; int cnt_[64],cur[64],last_[64]; bool used[2048]; vector<int> w[64],lab[64]; long long nodes,LIMIT=20000000,found=0; bool ALL=false;
void show(){ for(int i=0;i<k;i++){ printf("  labels:"); for(int x:lab[i]) printf(" %3d",x); printf("   edges:"); for(int x:w[i]) printf(" %3d",x); printf("\n"); } }
int rec(int t){ if(t==0){ found++; if(ALL){ printf("deal %lld\n",found); show(); return 0;} return 1; } if(++nodes>LIMIT) return -1;
  int forced=-1;
  for(int i=0;i<k;i++){ int c=cnt_[i]; if(c>=Q1 && c>=1 && c+1<=L-Q2){ int need=last_[i]-STEP; if(need>t) return 0; if(need==t){ if(forced>=0) return 0; forced=i; } } }
  for(int i=0;i<k;i++){ if(cnt_[i]==L) continue; if(forced>=0 && i!=forced) continue; int c=cnt_[i];
    if(c>=Q1 && c>=1 && c+1<=L-Q2 && last_[i]-STEP!=t) continue;
    if(c==0 && i>0 && cnt_[i-1]==0) continue;
    for(int sg=0;sg<2;sg++){ int x; if(c==0){ if(sg) continue; x=t; } else x= sg==0?cur[i]-t:cur[i]+t;
      if(x<1||x>m||used[x]) continue;
      int old=cur[i],ol=last_[i]; cur[i]=x; last_[i]=t; used[x]=1; cnt_[i]++; w[i].push_back(t); lab[i].push_back(x);
      int r=rec(t-1); 
      lab[i].pop_back(); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; last_[i]=ol; if(r==1) { return 1; } if(r<0) return -1; } }
  return 0; }
int main(int argc,char**argv){ k=atoi(argv[1]); L=atoi(argv[2]); Q1=atoi(argv[3]); Q2=atoi(argv[4]); if(argc>5) LIMIT=atoll(argv[5]); ALL=argc>6; STEP=getenv("STEP")?atoi(getenv("STEP")):k;
  m=k*L; int r=rec(m); if(ALL){ printf("k=%d L=%d Q1=%d Q2=%d total=%lld %s\n",k,L,Q1,Q2,found,r<0?"(limit)":""); return 0; }
  printf("k=%d L=%d Q1=%d Q2=%d %s nodes=%lld\n",k,L,Q1,Q2,r==1?"found":r==0?"none":"unresolved",nodes); }
