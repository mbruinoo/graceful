// For each tree (edge list on stdin) and each vertex v: is there a growth placement with label(v)=1 ?
// ("v is an anchor".)  Exhaustive DFS.  Prints summary statistics and small non-anchor examples.
// Usage: anchors n [verbose] < trees
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[40]; int lab[40]; bool used[41];
bool dfs(int k){
  if(k==0) return true;
  for(int u=0;u<n;u++) if(lab[u]){
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
      for(int w:adj[u]) if(!lab[w]){ lab[w]=x; used[x]=1; if(dfs(k-1)) return true; lab[w]=0; used[x]=0; } } }
  return false;
}
bool anchor(int v){ for(int w:adj[v]){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[v]=1; lab[w]=n; used[1]=used[n]=1; if(dfs(n-2)) return true; } return false; }
int main(int argc,char**argv){
  n=atoi(argv[1]); bool verbose=argc>2; string line; long trees=0, allAnch=0, nonLeafFail=0, leafFail=0, leafNbrFail=0, maxdegFail=0, noAnchor=0, verts=0, fails=0, centreFail=0;
  map<int,long> failDeg;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    trees++; int md=0; for(int i=0;i<n;i++) md=max(md,(int)adj[i].size());
    bool all=true, any=false, mdOK=false; string bad;
    for(int x=0;x<n;x++){ verts++; bool a=anchor(x); if(a) any=true; else { all=false; fails++; failDeg[adj[x].size()]++; bad+=" "+to_string(x)+"(deg"+to_string(adj[x].size())+")";
        if(adj[x].size()==1) leafFail++; else nonLeafFail++;
        bool ln=false; for(int w:adj[x]) if(adj[w].size()==1) ln=true; if(ln) leafNbrFail++; }
      if(a && (int)adj[x].size()==md) mdOK=true; }
    if(all) allAnch++; if(!any) noAnchor++; if(!mdOK) maxdegFail++;
    if(verbose && !all) printf("%s | non-anchors:%s\n",line.c_str(),bad.c_str());
  }
  printf("n=%d trees=%ld allVerticesAnchor=%ld treesWithNoAnchor=%ld | vertices=%ld nonAnchors=%ld (leaves %ld, internal %ld, with-leaf-neighbour %ld) treesWhereNoMaxDegVertexIsAnchor=%ld | by degree:",n,trees,allAnch,noAnchor,verts,fails,leafFail,nonLeafFail,leafNbrFail,maxdegFail);
  for(auto&p:failDeg) printf(" d%d:%ld",p.first,p.second); printf("\n");
}
