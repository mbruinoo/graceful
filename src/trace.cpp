// Find a growth placement of each tree on stdin and print how the set of unused labels evolves:
// for each step (length k): new label, its parent's label, and the unused labels shown as a strip ('.'=unused, '#'=used).
// Usage: trace n < trees
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[300]; int lab[300]; bool used[301]; long long nodes, limit_; mt19937 rng(7);
vector<array<int,3>> hist;
int dfs(int k){
  if(k==0) return 1; if(++nodes>limit_) return -1;
  vector<array<int,3>> c;
  for(int u=0;u<n;u++) if(lab[u]) for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue; for(int w:adj[u]) if(!lab[w]) c.push_back({u,w,x}); }
  shuffle(c.begin(),c.end(),rng);
  for(auto&e:c){ lab[e[1]]=e[2]; used[e[2]]=1; hist.push_back({k,e[2],lab[e[0]]}); int r=dfs(k-1); if(r==1) return 1; hist.pop_back(); lab[e[1]]=0; used[e[2]]=0; if(r<0) return -1; }
  return 0;
}
int main(int argc,char**argv){ n=atoi(argv[1]); string line;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    for(int tries=0;tries<100000;tries++){ int r0=rng()%n; int w=adj[r0][rng()%adj[r0].size()]; memset(lab,0,sizeof lab); memset(used,0,sizeof used); hist.clear(); lab[r0]=1; lab[w]=n; used[1]=used[n]=1; nodes=0; limit_=20000;
      if(dfs(n-2)==1){ string strip(n,'.'); strip[0]='#'; strip[n-1]='#'; int maxgaps=0, cross=0; double c=(n+1)/2.0;
        printf("k=%3d                 %s\n",n-1,strip.c_str());
        for(auto&h:hist){ strip[h[1]-1]='#'; int gaps=0; for(int i=0;i<n;i++) if(strip[i]=='.'&&(i==0||strip[i-1]!='.')) gaps++; maxgaps=max(maxgaps,gaps);
          bool same=(h[1]<c)==(h[2]<c); printf("k=%3d new %3d on %3d %s %s\n",h[0],h[1],h[2],same?"same":"    ",strip.c_str()); }
        printf("max number of unused runs: %d\n\n",maxgaps); break; } } } }
