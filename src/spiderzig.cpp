// ZIGZAG SPIDERS.  Spider with leg lengths L_1..L_k, m = sum L_i edges, centre labelled 0, labels 0..m.
// Give leg i a strictly decreasing list of edge lengths w_1 > w_2 > ... (all lengths 1..m used once in total);
// the j-th vertex of the leg gets the alternating sum w_1 - w_2 + w_3 - ... (j terms).  The labeling is graceful
// (and a growth placement with the centre as anchor) iff all these alternating sums are different.
// With FREE=1 in the environment the legs need not alternate: any growth placement with the centre at label 0.
// For every spider on n vertices: does such a split exist?   Usage: spiderzig n [show]   or   spiderzig 0 L1 L2 ...
#include <bits/stdc++.h>
using namespace std;
int k,m; int L[64], cnt_[64], cur[64]; bool used[256]; vector<int> w[64], lab[64]; long long nodes, LIMIT; bool FREE=false; int LEVEL=0;   // LEVEL=1: deal level by level (every unfinished leg gets its j-th number before any gets its (j+1)-th); LEVEL=2: only the first level first   // FREE: any signs (centre at label 0, lengths still decreasing outward)
int rec(int t){           // t = next edge length to hand out (from m down to 1)
  if(t==0) return 1; if(++nodes>LIMIT) return -1;
  int minc=1<<30; if(LEVEL) for(int i=0;i<k;i++) if(cnt_[i]<L[i]) minc=min(minc,cnt_[i]);
  for(int i=0;i<k;i++){ if(cnt_[i]==L[i]) continue; if(LEVEL==1 && cnt_[i]!=minc) continue; if(LEVEL==2 && minc==0 && cnt_[i]!=0) continue;
    bool dup=false; for(int j=0;j<i;j++) if(L[j]==L[i] && cnt_[j]==cnt_[i] && cur[j]==cur[i] && (cnt_[i]==0)) { dup=true; break; }   // untouched equal legs are interchangeable
    if(dup) continue;
    for(int sg=0; sg<(FREE&&cnt_[i]>0?2:1); sg++){
      int x = FREE ? (cnt_[i]==0 ? cur[i]+t : (sg==0? cur[i]-t : cur[i]+t)) : ((cnt_[i]%2==0) ? cur[i]+t : cur[i]-t);
      if(x<1||x>m||used[x]) continue;
      int old=cur[i]; cur[i]=x; used[x]=1; cnt_[i]++; w[i].push_back(t); lab[i].push_back(x);
      int r=rec(t-1); if(r==1) return 1;
      lab[i].pop_back(); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; if(r<0) return -1; } }
  return 0; }
int solve(){ m=0; for(int i=0;i<k;i++){ m+=L[i]; cnt_[i]=0; cur[i]=0; w[i].clear(); lab[i].clear(); } memset(used,0,sizeof used); nodes=0; return rec(m); }
void show(){ for(int i=0;i<k;i++){ printf("   leg %d lengths:",L[i]); for(int x:w[i]) printf(" %d",x); printf("   labels:"); for(int x:lab[i]) printf(" %d",x); printf("\n"); } }
vector<int> part; long long total=0, none=0, unres=0; bool SHOW=false;
void gen(int rem,int mx){ if(rem==0){ if(part.size()<3) return; k=part.size(); for(int i=0;i<k;i++) L[i]=part[i]; total++; int r=solve();
    if(r==0){ none++; printf("NONE:"); for(int x:part) printf(" %d",x); printf("\n"); } else if(r<0){ unres++; printf("UNRESOLVED:"); for(int x:part) printf(" %d",x); printf("\n"); } else if(SHOW){ printf("spider"); for(int x:part) printf(" %d",x); printf("\n"); show(); } return; }
  for(int x=min(rem,mx);x>=1;x--){ part.push_back(x); gen(rem-x,x); part.pop_back(); } }
int main(int argc,char**argv){ if(getenv("FREE")) FREE=true; if(getenv("LEVEL")) LEVEL=atoi(getenv("LEVEL")); int n=atoi(argv[1]); LIMIT= getenv("ZLIMIT")? atoll(getenv("ZLIMIT")) : 200000000LL;
  if(n==0){ k=argc-2; for(int i=0;i<k;i++) L[i]=atoi(argv[i+2]); int r=solve(); printf(r==1?"found\n":r==0?"none\n":"unresolved\n"); if(r==1) show(); return 0; }
  SHOW=argc>2; gen(n-1,n-1); printf("n=%d spiders=%lld  no zigzag split=%lld  unresolved=%lld\n",n,total,none,unres); }
