// Path anchors.  The path with m edges, rooted at the vertex at distance b from one end
// (legs of a = m-b and b edges).  A growth placement with that vertex labelled 0 (README s.8,
// Theorem 7; labels 0..m) is a "two-leg deal": hand m, m-1, ..., 1 to the two legs; each number
// k moves that leg's tip by +k or -k; labels stay in [0,m] and are never repeated.
// Usage: ./pathanchor M BLO BHI   -> for every m <= M and BLO <= b <= min(BHI, m/2):
//        number of deals (= growth placements of the path with that vertex labelled 0).
// Counts are capped at CAP to keep runs short (prints CAP+ when reached).
#include <bits/stdc++.h>
using namespace std;
static int m; static bool used[1024]; static long long cnt, CAP;
static int tip[2], rem_[2];
static void go(int k){
  if(cnt>=CAP) return;
  if(k==0){cnt++; return;}
  for(int l=0;l<2;l++){ if(!rem_[l]) continue;
    if(l==1 && rem_[0]==rem_[1] && tip[0]==0 && tip[1]==0) continue; // equal legs: same placement
    for(int d=+1;d>=-1;d-=2){ int x=tip[l]+d*k; if(x<0||x>m||used[x]) continue;
      int ot=tip[l]; used[x]=true; tip[l]=x; rem_[l]--;
      go(k-1);
      used[x]=false; tip[l]=ot; rem_[l]++; } }
}
int main(int argc,char**argv){ int M=atoi(argv[1]), BLO=atoi(argv[2]), BHI=atoi(argv[3]);
  CAP = argc>4 ? atoll(argv[4]) : (long long)4e18; int M0 = argc>5 ? atoi(argv[5]) : 2;
  for(m=M0;m<=M;m++){ printf("m=%d:",m);
    for(int b=BLO;b<=BHI && 2*b<=m;b++){ int a=m-b; rem_[0]=a; rem_[1]=b; tip[0]=tip[1]=0;
      memset(used,0,sizeof used); used[0]=true; cnt=0; go(m);
      printf(" (%d,%d):%lld%s",a,b,cnt,cnt>=CAP?"+":"");} puts(""); fflush(stdout); }
}
