// For each tree on stdin: is there a growth placement in which the unused labels never form more than R runs?
// Trees come from the built-in generator (treegen.h); work can be split: only trees with index % parts == part are solved.
// Randomised DFS with restarts, then exhaustive.   Usage: runsolve_gen n R [part parts [HS [SIDE]]]   (HS>0: all runs but the longest have at most HS cells)
#include <bits/stdc++.h>
#include "treegen.h"
using namespace std;
typedef unsigned long long u64;
int n,R; vector<int> adj[64]; int lab[64]; u64 usedm; long long nodes, limit_; mt19937 rng(12345);
int HS=0, SIDE=0;   /* HS>0: every run of unused labels except the longest has at most HS cells; SIDE=1: at most one such run on each side of the longest */
inline bool holesOK(u64 S){ if(!HS) return true; int sz[40], m=0, cur=0; for(int i=1;i<=n+1;i++){ if(i<=n && !(S>>i&1)) cur++; else if(cur){ sz[m++]=cur; cur=0; } }
  if(!m) return true; int bi=0; for(int i=1;i<m;i++) if(sz[i]>sz[bi]) bi=i;
  for(int i=0;i<m;i++) if(i!=bi && sz[i]>HS) return false;
  if(SIDE==1 && (bi>1 || m-1-bi>1)) return false;
  return true; }
inline int runs(u64 S){ u64 all=(n>=63? ~0ull : ((1ull<<n)-1))<<1; u64 un=~S & all; return __builtin_popcountll(un & ~(un<<1)); }
int dfs(int k){
  if(k==0) return 1; if(++nodes>limit_) return -1;
  int cu[256], cw[256], cl[256], c=0;
  for(int u=0;u<n;u++) if(lab[u]){ bool hasUn=false; int firstLeaf=-1; for(int w:adj[u]) if(!lab[w]){hasUn=true;break;} if(!hasUn) continue;
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||(usedm>>x&1)) continue; if(runs(usedm|1ull<<x)>R || !holesOK(usedm|1ull<<x)) continue;
      bool leafDone=false; for(int w:adj[u]) if(!lab[w]){ if(adj[w].size()==1){ if(leafDone) continue; leafDone=true; } cu[c]=u; cw[c]=w; cl[c]=x; c++; } } }
  for(int i=c-1;i>0;i--){ int j=rng()%(i+1); swap(cu[i],cu[j]); swap(cw[i],cw[j]); swap(cl[i],cl[j]); }
  for(int i=0;i<c;i++){ lab[cw[i]]=cl[i]; usedm|=1ull<<cl[i]; int r=dfs(k-1); if(r==1) return 1; lab[cw[i]]=0; usedm&=~(1ull<<cl[i]); if(r<0) return -1; }
  return 0;
}
int solve(long long lim){ limit_=lim; vector<pair<int,int>> es; for(int u=0;u<n;u++) for(int w:adj[u]) es.push_back({u,w}); shuffle(es.begin(),es.end(),rng); bool hit=false;
  for(auto e:es){ memset(lab,0,sizeof lab); lab[e.first]=1; lab[e.second]=n; usedm=(1ull<<1)|(1ull<<n); nodes=0; int r=dfs(n-2); if(r==1) return 1; if(r<0) hit=true; }
  return hit?-1:0; }
int main(int argc,char**argv){ n=atoi(argv[1]); R=atoi(argv[2]); int part=argc>3?atoi(argv[3]):0, parts=argc>4?atoi(argv[4]):1; HS=argc>5?atoi(argv[5]):0; SIDE=argc>6?atoi(argv[6]):0; long long lim=5000;
  TreeGen g(n); vector<int> par; long long idx=0,total=0,fail=0,none=0;
  while(g.next()){ if((idx++)%parts!=part) continue; g.parents(par); for(int i=0;i<n;i++) adj[i].clear(); for(int i=1;i<n;i++){ adj[i].push_back(par[i]); adj[par[i]].push_back(i); }
    total++; int r=-1; long long L=lim; for(int a=0;a<14&&r<0;a++){ r=solve(L); L*=3; }
    if(r<=0){ if(r==0) none++; else fail++; printf("%s:",r==0?"NONE":"UNRESOLVED"); for(int i=1;i<n;i++) printf(" %d %d",par[i],i); printf("\n"); fflush(stdout); } }
  printf("n=%d runs<=%d holesize<=%d side=%d part %d/%d trees=%lld  none=%lld unresolved=%lld\n",n,R,HS,SIDE,part,parts,total,none,fail); }
