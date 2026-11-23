// Enumerate ALL valid deals (definition: centre label 0, numbers m..1 dealt to legs, first move up,
// later moves up or down, all labels distinct in 1..m) of ALL spiders with m edges (every partition of m,
// including 1 and 2 legs).  Legs of equal length are interchangeable: canonical form lists legs by
// (length descending, first number descending).
// Output, one deal per line:   L1 L2 .. Lk | w11 w12 .. ; w21 .. ; ...   with signed numbers (negative = down move).
// Usage: enum_deals m [count]     ("count" prints only per-spider counts)
#include <bits/stdc++.h>
using namespace std;
int k,m; int L[32], cnt_[32], cur[32], firstw[32]; bool used[64]; vector<int> w[32]; long long ndeals; bool COUNT=false;
void emit(){ ndeals++; if(COUNT) return; for(int i=0;i<k;i++) printf("%d ",L[i]); printf("|"); for(int i=0;i<k;i++){ for(int x:w[i]) printf(" %d",x); if(i<k-1) printf(" ;"); } printf("\n"); }
void rec(int t){
  if(t==0){ emit(); return; }
  for(int i=0;i<k;i++){ if(cnt_[i]==L[i]) continue;
    // canonical: among equal-length legs, leg i may start only if previous equal-length leg has started (first numbers descending)
    if(cnt_[i]==0 && i>0 && L[i-1]==L[i] && cnt_[i-1]==0) continue;
    for(int sg=0; sg<(cnt_[i]>0?2:1); sg++){
      int x = (cnt_[i]==0||sg==1) ? cur[i]+t : cur[i]-t;
      if(x<1||x>m||used[x]) continue;
      int old=cur[i]; cur[i]=x; used[x]=1; cnt_[i]++; w[i].push_back(x>old?t:-t);
      rec(t-1);
      w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; } } }
vector<int> part;
void gen(int rem,int mx){ if(rem==0){ k=part.size(); for(int i=0;i<k;i++){ L[i]=part[i]; cnt_[i]=0; cur[i]=0; w[i].clear(); } memset(used,0,sizeof used); long long b=ndeals; rec(m);
    if(COUNT){ printf("S("); for(int i=0;i<k;i++) printf("%d%s",L[i],i<k-1?",":""); printf(") %lld\n",ndeals-b); } return; }
  for(int x=min(rem,mx);x>=1;x--){ part.push_back(x); gen(rem-x,x); part.pop_back(); } }
int main(int argc,char**argv){ m=atoi(argv[1]); COUNT=argc>2; gen(m,m); fprintf(stderr,"m=%d deals=%lld\n",m,ndeals); }
