// Exhaustive test of the all-up comb form for diameter-4 trees.
// Tree: centre with k>=2 neighbours ("hubs") carrying s_1>=...>=s_k>=0 leaves, at least two s_i>0  (n = 1+k+sum s_i).
// All-up comb rooted at hub r (labels 0..m, m=n-1): hub r at 0, centre at y, every other hub i at h_i<y,
// every leaf of hub i at h_i+u (above its hub, below the centre), leaves of r anywhere.
// By Theorem 7 of the README this is a growth placement iff labels are 0..m once and edge lengths 1..m once;
// the search below places lengths y-1, y-2, ..., 1 in turn (lengths > y are leaves of r at cells > y).
// Usage: au_scan N [lo]   -- all diameter-4 trees with lo <= n <= N
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int y; vector<int> hubLab, hubCap; int cnt[64]; int wild; u64 usedc; long long nodes;
vector<int> sizesDistinct;
bool rec(int u){
  nodes++;
  if(u==0){ for(int c:hubCap) if(c) return false; for(int s:sizesDistinct) if(cnt[s]) return false; return wild==0; }
  // leaf of a placed hub
  for(size_t i=0;i<hubLab.size();i++) if(hubCap[i]>0){ int z=hubLab[i]+u; if(z<y && !(usedc>>z&1)){ hubCap[i]--; usedc|=1ull<<z; if(rec(u-1)) return true; hubCap[i]++; usedc&=~(1ull<<z); } }
  // wildcard: leaf of the root hub at cell u
  if(wild>0 && !(usedc>>u&1)){ wild--; usedc|=1ull<<u; if(rec(u-1)) return true; wild++; usedc&=~(1ull<<u); }
  // new hub at label y-u (its edge to the centre has length u)
  int h=y-u; if(!(usedc>>h&1)) for(int s:sizesDistinct) if(cnt[s]>0){ cnt[s]--; usedc|=1ull<<h; hubLab.push_back(h); hubCap.push_back(s);
      bool ok=rec(u-1); if(ok) return true; hubLab.pop_back(); hubCap.pop_back(); usedc&=~(1ull<<h); cnt[s]++; }
  return false;
}
// returns true if an all-up comb exists with root hub of size a1 and the other hubs 'others'
bool allup(int a1, const vector<int>&others, bool show){
  int m=1+others.size()+a1; for(int s:others) m+=s;
  set<int> ds(others.begin(),others.end()); sizesDistinct.assign(ds.rbegin(),ds.rend());
  for(y=m; y>=m-a1; y--){
    memset(cnt,0,sizeof cnt); for(int s:others) cnt[s]++; wild=a1-(m-y); usedc=1ull; hubLab.clear(); hubCap.clear();
    if(rec(y-1)){ if(show){ printf("   y=%d hubs:",y); for(size_t i=0;i<hubLab.size();i++) printf(" %d",hubLab[i]); printf("\n"); } return true; }
  }
  return false;
}
void gen(int total,int k,int maxv,vector<int>&cur,vector<vector<int>>&out){
  if(k==0){ if(total==0) out.push_back(cur); return; }
  for(int f=min(total,maxv); f>=0; f--){ cur.push_back(f); gen(total-f,k-1,f,cur,out); cur.pop_back(); }
}
int main(int argc,char**argv){ int N=atoi(argv[1]); int lo=argc>2?atoi(argv[2]):5;
  for(int n=lo;n<=N;n++){ long long trees=0, okLargest=0, okSome=0, cat=0; nodes=0;
    for(int k=2;k<n;k++){ vector<vector<int>> ps; vector<int> cur; gen(n-1-k,k,n,cur,ps);
      for(auto&s:ps){ int pos=0; for(int x:s) if(x>0) pos++; if(pos<2) continue; trees++; if(pos==2) cat++;
        vector<int> others(s.begin()+1,s.end());
        if(allup(s[0],others,false)){ okLargest++; okSome++; continue; }
        bool some=false; for(size_t i=1;i<s.size()&&!some;i++){ if(s[i]==s[i-1]||s[i]==0) continue; vector<int> o; for(size_t j=0;j<s.size();j++) if(j!=i) o.push_back(s[j]); some=allup(s[i],o,false); }
        printf("  n=%d sizes",n); for(int x:s) printf(" %d",x); printf(" : no all-up comb rooted at the largest hub; rooted at another nontrivial hub: %s\n", some?"yes":"NO");
        if(some) okSome++; } }
    printf("n=%d diameter-4 trees=%lld (of which caterpillars=%lld)  all-up comb at largest hub: %lld  at some hub: %lld  [search nodes %lld]\n",n,trees,cat,okLargest,okSome,nodes); fflush(stdout); }
}
