// For a spider: enumerate ALL its growth placements and, for each, the smallest clean set (see lemma_check.cpp for the definition).
// Only sets R whose removal leaves a connected subtree can be clean, i.e. R = a union of leg tails (centre kept), or everything
// except a sub-path of one leg (centre removed).  Prints the distribution of the least clean-set size.
// Usage: spider_minstep leg1 leg2 ...
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[40]; int lab[40]; bool used[41]; vector<int> legs; vector<vector<int>> legv; long total=0; map<int,long> dist;
static bool isClean(const vector<int>&pos,unsigned long long R){ int r=__builtin_popcountll(R); if(n-r<2) return false; int rb=0;
  for(int k=1;k<n;k++) if((R>>pos[k]&1)||(R>>(pos[k]+k)&1)) rb++; if(rb!=r) return false;
  int shorter=0; for(int k=1;k<n;k++){ int a=pos[k], b=a+k; if((R>>a&1)||(R>>b&1)){ shorter++; continue; }
    int jump=__builtin_popcountll(R & (((1ULL<<b)-1) & ~((1ULL<<(a+1))-1))); if(jump!=shorter) return false; } return true; }
void leaf(){ total++; vector<int> pos(n); for(int u=0;u<n;u++) for(int w:adj[u]) if(u<w){ int a=min(lab[u],lab[w]), b=max(lab[u],lab[w]); pos[b-a]=a; }
  int best=99; int L=legs.size(); vector<int> t(L,0);
  while(true){ unsigned long long R=0; int r=0; for(int i=0;i<L;i++) for(int j=0;j<t[i];j++){ R|=1ULL<<lab[legv[i][legs[i]-1-j]]; r++; }
    if(r>0 && r<best && isClean(pos,R)) best=r;
    int i=0; while(i<L && t[i]==legs[i]){ t[i]=0; i++; } if(i==L) break; t[i]++; }
  for(int i=0;i<L;i++) for(int a=0;a<legs[i];a++) for(int b=a+1;b<legs[i];b++){ unsigned long long R=0; int r=0; for(int u=0;u<n;u++){ bool keep=false; for(int j=a;j<=b;j++) if(legv[i][j]==u) keep=true; if(!keep){ R|=1ULL<<lab[u]; r++; } } if(r<best && isClean(pos,R)) best=r; }
  dist[best]++; }
void dfs(int k){ if(k==0){ leaf(); return; }
  for(int u=0;u<n;u++) if(lab[u]) for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue; for(int w:adj[u]) if(!lab[w]){ lab[w]=x; used[x]=1; dfs(k-1); lab[w]=0; used[x]=0; } } }
int main(int argc,char**argv){ for(int i=1;i<argc;i++) legs.push_back(atoi(argv[i])); n=1; int v=1; for(int l:legs){ vector<int> lv; int p=0; for(int j=0;j<l;j++){ adj[p].push_back(v); adj[v].push_back(p); lv.push_back(v); p=v; v++; } legv.push_back(lv); n+=l; }
  for(int r=0;r<n;r++) for(int w:adj[r]){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[r]=1; lab[w]=n; used[1]=used[n]=1; dfs(n-2); }
  printf("spider"); for(int l:legs) printf(" %d",l); printf(" n=%d: growth labelings (vertex-labelled, automorphic copies counted separately)=%ld ; least clean-set size -> count:",n,total); for(auto&d:dist) printf(" %d:%ld",d.first,d.second); printf("\n"); }
