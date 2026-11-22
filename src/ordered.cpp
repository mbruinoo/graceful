// Growth placements with a prescribed BUILD ORDER.
//   mode d : depth-first  -- the next vertex is a child of the deepest vertex on the current branch that still has an unbuilt child
//   mode b : breadth-first -- the next vertex is a child of the earliest-built vertex that still has an unbuilt child
// For every tree on stdin: does some root (label 1), child order and sign choice give a growth placement?
// Usage: ordered n mode [v] < trees
#include <bits/stdc++.h>
using namespace std;
int n; char mode; vector<int> adj[40]; int lab[40], par[40], ordv[40], seq[40]; bool used[41]; int last_;
bool dfs(int t){            // t vertices already built; next bracket length n-t
  if(t==n) return true; int k=n-t, u=-1;
  if(mode=='d'){ for(int x=seq[t-1]; x>=0; x=par[x]){ bool un=false; for(int w:adj[x]) if(!lab[w]){un=true;break;} if(un){u=x;break;} } }
  else { for(int i=0;i<t;i++){ int x=seq[i]; bool un=false; for(int w:adj[x]) if(!lab[w]){un=true;break;} if(un){u=x;break;} } }
  for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
    for(int w:adj[u]) if(!lab[w]){ lab[w]=x; used[x]=1; par[w]=u; seq[t]=w; if(dfs(t+1)) return true; lab[w]=0; used[x]=0; } }
  return false;
}
bool solve(){ for(int r=0;r<n;r++){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[r]=1; used[1]=1; par[r]=-1; seq[0]=r; if(dfs(1)) return true; } return false; }
int main(int argc,char**argv){ n=atoi(argv[1]); mode=argv[2][0]; bool verbose=argc>3; string line; long trees=0, fail=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    trees++; if(!solve()){ fail++; if(verbose) printf("FAIL %s\n",line.c_str()); } }
  printf("n=%d mode=%c trees=%ld without-such-placement=%ld\n",n,mode,trees,fail); }
