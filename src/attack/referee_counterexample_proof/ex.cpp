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
bool dfs(int k){
  if(k==0) return true;
  for(int u=0;u<n;u++) if(lab[u]) for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
    bool leafTried=false;
    for(int w:adj[u]) if(!lab[w]){ bool leaf=adj[w].size()==1; if(leaf){ if(leafTried) continue; leafTried=true; }
      lab[w]=x; used[x]=true; bool r=dfs(k-1); lab[w]=0; used[x]=false; if(r) return true; } }
  return false; }
bool tryEdge(int a,int b){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[a]=1; lab[b]=n; used[1]=used[n]=true; return dfs(n-2); }
int main(){ string line; while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n; for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u); }
  bool root=false, any=false;
  if(n==1){ root=any=true; }
  else { for(int w:adj[0]) if(tryEdge(0,w)){ root=true; break; }
    any=root; for(int a=0;a<n&&!any;a++) for(int w:adj[a]) if(tryEdge(a,w)){ any=true; break; } }
  printf("%d %d\n",root,any); } }
