// Referee brute force: is vertex `root` an anchor of tree T?
// Straight from README section 1: labels 0..m (shifted by 1), root at 0,
// place brackets m, m-1, ..., 1; each must have exactly one used foot (at a
// placed tree vertex u) and its other foot an unused label, which is given to
// a not-yet-placed tree neighbour of u.  Symmetry: unplaced neighbours of u
// whose hanging subtrees are isomorphic are interchangeable.
// Sound prunes: (a) a vertex whose hanging subtree has s vertices needs
// length >= s (all lengths in the subtree are smaller and distinct -- this
// follows from the growth order itself: everything below is placed later);
// (b) when all unplaced vertices are leaves of placed vertices, each unused
// label must be within reach (< k) of some open parent and each remaining
// length must have a free foot.  PRUNE=0 env disables (b); PRUNE=-1 disables both.
// input lines: n root a1 b1 ... a_{n-1} b_{n-1}
// output: "1 nodes label0 ... label_{n-1}" or "0 nodes" or "? nodes" (limit)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n,m,root; vector<int> adj[80]; int par[80], cls[80], sz[80], lab[80]; bool placed[80], isleaf[80];
vector<int> kids[80];
u64 used; long long nodes, limitN; int pruneLevel=1;
int nonleafUnplaced;
map<vector<int>,int> canon;
int build(int u,int p){ par[u]=p; sz[u]=1; vector<int> c; for(int w:adj[u]) if(w!=p){ kids[u].push_back(w); c.push_back(build(w,u)); sz[u]+=sz[w]; }
  sort(c.begin(),c.end()); auto it=canon.find(c); if(it==canon.end()) it=canon.insert({c,(int)canon.size()}).first; cls[u]=it->second; isleaf[u]=kids[u].empty(); return cls[u]; }
vector<int> act; // placed vertices (all); we scan kids
int remk[80]; // number of unplaced kids
bool feasible(int k){ // lengths 1..k remain; all unplaced are leaves
  // lengths
  for(int w=1;w<=k;w++){ bool ok=false; for(int u:act){ if(!remk[u]) continue; int a=lab[u]; if(a+w<=m && !((used>>(a+w))&1)){ok=true;break;} if(a-w>=0 && !((used>>(a-w))&1)){ok=true;break;} } if(!ok) return false; }
  for(int x=0;x<=m;x++){ if((used>>x)&1) continue; bool ok=false; for(int u:act){ if(!remk[u]) continue; int d=abs(x-lab[u]); if(d>=1&&d<=k){ok=true;break;} } if(!ok) return false; }
  return true; }
int dfs(int k){ // returns 1 found, 0 none, -1 limit
  if(k==0) return 1;
  if(++nodes>limitN) return -1;
  if(pruneLevel>=1 && nonleafUnplaced==0 && !feasible(k)) return 0;
  // forced: any frontier vertex with sz==k must be placed now
  int forced=-1;
  if(pruneLevel>=0){ for(int u:act){ if(!remk[u]) continue; for(int c:kids[u]) if(!placed[c]){ if(sz[c]>k) return 0; if(sz[c]==k){ if(forced>=0 && forced!=c) return 0; forced=c; } } } }
  size_t na=act.size();
  for(size_t i=0;i<na;i++){ int u=act[i]; if(!remk[u]) continue; int a=lab[u];
    int seen[80]; int ns=0;
    for(int c:kids[u]){ if(placed[c]) continue; if(forced>=0 && c!=forced) continue; if(pruneLevel>=0 && sz[c]>k) continue;
      bool dup=false; for(int j=0;j<ns;j++) if(seen[j]==cls[c]){dup=true;break;} if(dup) continue; seen[ns++]=cls[c];
      for(int s=0;s<2;s++){ int x= s? a-k : a+k; if(x<0||x>m) continue; if((used>>x)&1) continue;
        placed[c]=true; lab[c]=x; used|=1ULL<<x; remk[u]--; act.push_back(c); if(!isleaf[c]) nonleafUnplaced--;
        int r=dfs(k-1);
        if(r!=0) return r; // keep labels for the witness; main() re-initialises
        if(!isleaf[c]) nonleafUnplaced++; act.pop_back(); remk[u]++; used&=~(1ULL<<x); placed[c]=false;
        if(r!=0) return r; } } }
  return 0; }
int main(int argc,char**argv){ limitN = argc>1? atoll(argv[1]) : (long long)4e18; if(getenv("PRUNE")) pruneLevel=atoi(getenv("PRUNE"));
  string line; while(getline(cin,line)){ istringstream is(line); if(!(is>>n>>root)) continue; m=n-1; for(int i=0;i<n;i++){adj[i].clear();kids[i].clear();placed[i]=false;}
    for(int i=0;i<m;i++){int a,b; is>>a>>b; adj[a].push_back(b); adj[b].push_back(a);} canon.clear(); build(root,-1);
    nonleafUnplaced=0; for(int i=0;i<n;i++){ remk[i]=kids[i].size(); if(i!=root && !isleaf[i]) nonleafUnplaced++; }
    act.clear(); act.push_back(root); placed[root]=true; lab[root]=0; used=1; nodes=0;
    // dfs leaves lab[] intact on success since we return before undoing? we undo; so record
    int r=dfs(m);
    if(r==1){ printf("1 %lld",nodes); for(int i=0;i<n;i++) printf(" %d",lab[i]); printf("\n"); } else if(r==0) printf("0 %lld\n",nodes); else printf("? %lld\n",nodes); }
}
