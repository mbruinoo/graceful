// For each tree on stdin (edge list, 0-based), search for a GROWTH graceful labeling:
// labels 1..n; edge lengths n-1, n-2, ..., 1 are assigned in this order so that the labeled part
// is always a connected subtree (each new edge hangs one new vertex off the labeled part).
// Usage: growsolve n [nodeLimit] < trees.txt     prints stats and any trees with no solution found.
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[300]; int lab[300]; bool used[301]; long long nodes, limit_;
int order_[300];
mt19937 rng(12345);
// returns 1 found, 0 exhausted, -1 limit hit
int dfs(int k){
  if(k==0) return 1;
  if(++nodes>limit_) return -1;
  // candidates: (u labeled, w unlabeled neighbour, new label)
  int cu[4000], cw[4000], cl[4000], c=0;
  for(int u=0;u<n;u++) if(lab[u]){
    bool hasUn=false; for(int w:adj[u]) if(!lab[w]){ hasUn=true; break; }
    if(!hasUn) continue;
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
      // symmetry: unlabeled leaf-neighbours of u are interchangeable only if isomorphic; just try each
      for(int w:adj[u]) if(!lab[w]){ cu[c]=u; cw[c]=w; cl[c]=x; c++; } }
  }
  // random order
  for(int i=c-1;i>0;i--){ int j=rng()%(i+1); swap(cu[i],cu[j]); swap(cw[i],cw[j]); swap(cl[i],cl[j]); }
  for(int i=0;i<c;i++){ lab[cw[i]]=cl[i]; used[cl[i]]=1; int r=dfs(k-1); if(r==1) return 1; lab[cw[i]]=0; used[cl[i]]=0; if(r<0) return -1; }
  return 0;
}
int solve(long long lim){
  limit_=lim; nodes=0;
  vector<pair<int,int>> es; for(int u=0;u<n;u++) for(int w:adj[u]) es.push_back({u,w}); // both orientations
  shuffle(es.begin(),es.end(),rng);
  bool hit=false;
  for(auto e:es){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[e.first]=1; lab[e.second]=n; used[1]=used[n]=1;
    int r=dfs(n-2); if(r==1) return 1; if(r<0){ hit=true; nodes=0; } }
  return hit?-1:0;
}
int main(int argc,char**argv){
  n=atoi(argv[1]); long long lim= argc>2? atoll(argv[2]) : 20000;
  string line; long long total=0, fail=0, exhausted=0; long long maxnodes=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    total++; int r=-1; long long L=lim;
    for(int attempt=0; attempt<12 && r<0; attempt++){ r=solve(L); L*=3; }
    if(r==0){ exhausted++; printf("NO GROWTH LABELING (exhaustive): %s\n",line.c_str()); }
    else if(r<0){ fail++; printf("UNRESOLVED: %s\n",line.c_str()); }
  }
  printf("n=%d trees=%lld  proven-impossible=%lld unresolved=%lld\n",n,total,exhausted,fail);
}
