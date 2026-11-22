// Count growth labelings (vertex assignments) of one tree, exhaustively.  Tree edges on stdin line(s).
// Usage: famcount n < trees   -> prints one count per tree
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[64]; int lab[64]; bool used[65]; long long cnt, nodes;
void dfs(int k){
  if(k==0){ cnt++; return; } nodes++;
  for(int u=0;u<n;u++) if(lab[u]){
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
      for(int w:adj[u]) if(!lab[w]){ lab[w]=x; used[x]=1; dfs(k-1); lab[w]=0; used[x]=0; } } }
}
int main(int argc,char**argv){ n=atoi(argv[1]); string line;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    cnt=0; nodes=0;
    for(int r=0;r<n;r++) for(int w:adj[r]){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[r]=1; lab[w]=n; used[1]=used[n]=1; dfs(n-2); }
    printf("n=%d labelings=%lld searchnodes=%lld\n",n,cnt,nodes); fflush(stdout); } }
