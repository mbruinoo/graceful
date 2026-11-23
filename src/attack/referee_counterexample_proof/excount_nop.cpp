// Referee tool, written from README sections 1-2 only.
// stdin: "n u v u v ..." per line.  For each tree prints "<rootAnchor> <any>":
//   rootAnchor = 1 iff some growth placement labels vertex 0 with 1 (exhaustive)
//   any        = 1 iff some growth placement exists (exhaustive; by reflection i->n+1-i we may take any
//                oriented edge (a,b) with a labelled 1, b labelled n)
// Search: longest bracket first; bracket k must join a labelled vertex u to an unlabelled neighbour w with
// label lab[u]+-k free.  Only pruning: unlabelled LEAF neighbours of the same vertex are interchangeable, so
// only the lowest-index unlabelled leaf neighbour of u is tried.
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[64]; int lab[64]; bool used[80];
long long CNT=0; bool dfs(int k){
  if(k==0){ CNT++; return false; }
  for(int u=0;u<n;u++) if(lab[u]) for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
    bool leafTried=false;
    for(int w:adj[u]) if(!lab[w]){ bool leaf=adj[w].size()==1; (void)leaf;
      lab[w]=x; used[x]=true; bool r=dfs(k-1); lab[w]=0; used[x]=false; if(r) return true; } }
  return false; }
bool tryEdge(int a,int b){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[a]=1; lab[b]=n; used[1]=used[n]=true; return dfs(n-2); }
int main(){ string line; while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n; for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u); }
  CNT=0; for(int a=0;a<n;a++){ bool leafTried=false; for(int w:adj[a]){ tryEdge(a,w); } }
  printf("%lld\n",CNT); } }
// Count variant of ex.cpp WITHOUT the leaf rule: prints the number of vertex labelings of the tree that are growth placements (= placements drawing the tree x automorphisms).
//  leaf-sibling rule, summed over all oriented top edges (a labelled 1, b labelled n).)
