// symx.cpp -- search for SYMMETRIC all-up combs ("mirror combs").
// A mirror comb for S with w inside fillers: y = |S|+sum(S)+w+1, distinct heads t_i in [1,y-1] (hub i has
// label y-t_i), sets U_i of [1,t_i-1] with |U_i| = s_i and t_i - U_i = U_i, W with y - W = W, |W| = w,
// all of these partitioning [1,y-1].  (Each hub's leaves are mirror pairs about the midpoint of hub and
// centre, plus the midpoint itself when s_i is odd; see REPORT.txt, Lemma M.)
// Usage: symx N [lo] [exact]   : for every S with |S|+sum+max+2 = n, lo<=n<=N, least w<=max(S) (or -1).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
static int Y; static u64 used; static int cnt[64], maxSize; static vector<int> hT, hCap; static signed char who[64]; static long long nodes;
static bool rec(int x){
  while(x>=1 && (used>>x&1)) x--;
  if(x<1){ for(int c:hCap) if(c) return false; for(int s=0;s<=maxSize;s++) if(cnt[s]) return false; for(int t:hT) if(t<64) who[t]=-1; return true; }
  nodes++;
  for(size_t i=0;i<hT.size();i++) if(hCap[i]>=2){ int p=hT[i]-x; if(p>=1 && p<x && !(used>>p&1)){
      used|=1ull<<x|1ull<<p; hCap[i]-=2; who[x]=who[p]=i; if(rec(x-1)) return true; hCap[i]+=2; used&=~(1ull<<x|1ull<<p); } }
  for(int s=maxSize;s>=0;s--) if(cnt[s]>0){ int mid=0;
      if(s&1){ if(x&1) continue; mid=x/2; if(used>>mid&1) continue; }
      cnt[s]--; used|=1ull<<x; if(mid){ used|=1ull<<mid; who[mid]=hT.size(); } hT.push_back(x); hCap.push_back(s-(s&1));
      if(rec(x-1)) return true;
      hT.pop_back(); hCap.pop_back(); used&=~(1ull<<x); if(mid) used&=~(1ull<<mid); cnt[s]++; }
  return false;
}
static bool solve(const vector<int>&S,int w){
  int k=S.size(), sum=0; for(int x:S) sum+=x; Y=k+sum+w+1; memset(cnt,0,sizeof cnt); maxSize=0; for(int x:S){ cnt[x]++; maxSize=max(maxSize,x); }
  hT.clear(); hCap.clear(); used=1; memset(who,-1,sizeof who);
  hT.push_back(Y); hCap.push_back(w-(w&1)); if(w&1){ if(Y&1) return false; used|=1ull<<(Y/2); who[Y/2]=0; }
  return rec(Y-1);
}
static void gen(int total,int k,int maxv,vector<int>&cur,vector<vector<int>>&out){
  if(k==0){ if(total==0) out.push_back(cur); return; }
  for(int f=min(total,maxv); f>=0; f--){ cur.push_back(f); gen(total-f,k-1,f,cur,out); cur.pop_back(); }
}
int main(int argc,char**argv){
  if(argc>1 && argv[1][0]=='S'){ // single instance: symx S s1 s2 ...   (sizes in any order)
    vector<int> S; for(int i=2;i<argc;i++) S.push_back(atoi(argv[i])); sort(S.rbegin(),S.rend()); int mx=S[0];
    int found=-1; for(int w=0;w<=mx && found<0;w++) if(solve(S,w)) found=w;
    if(found<0){ printf("NOSYM S"); for(int x:S) printf(" %d",x); printf("\n"); return 0; }
    printf("S"); for(int x:S) printf(" %d",x); printf(" | w %d y %d |",found,Y);
    for(size_t i=1;i<hT.size();i++){ printf(" %d:",Y-hT[i]); bool f=true; for(int l=1;l<Y;l++) if(who[l]==(int)i){ printf(f?"%d":",%d",l); f=false; } }
    printf(" | W"); for(int l=1;l<Y;l++) if(who[l]==0) printf(" %d",l); printf("\n"); return 0; }
  int N=atoi(argv[1]); int lo=argc>2?atoi(argv[2]):5;
  for(int n=lo;n<=N;n++){ long long cntS=0, fails=0; nodes=0;
    for(int k=1;k<n;k++) for(int mx=1; k+mx+mx+2<=n; mx++){ int rest=n-2-k-mx-mx;
        vector<vector<int>> ps; vector<int> cur; gen(rest,k-1,mx,cur,ps);
        for(auto&p:ps){ vector<int> S; S.push_back(mx); for(int x:p) S.push_back(x); cntS++;
          int found=-1; for(int w=0;w<=mx && found<0;w++) if(solve(S,w)) found=w;
          if(found<0){ fails++; printf("NOSYM n=%d S",n); for(int x:S) printf(" %d",x); printf("\n"); }
          else { printf("S"); for(int x:S) printf(" %d",x); printf(" | w %d y %d |",found,Y);
            for(size_t i=1;i<hT.size();i++){ printf(" %d:",Y-hT[i]); bool f=true; for(int l=1;l<Y;l++) if(who[l]==(int)i){ printf(f?"%d":",%d",l); f=false; } }
            printf(" | W"); for(int l=1;l<Y;l++) if(who[l]==0) printf(" %d",l); printf("\n"); }
          fflush(stdout); } }
    printf("# n=%d: multisets S: %lld  mirror comb with w<=max(S): %lld  none: %lld  nodes %lld\n",n,cntS,cntS-fails,fails,nodes); fflush(stdout); }
}
