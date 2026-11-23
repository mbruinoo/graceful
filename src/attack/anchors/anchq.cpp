// anchq.cpp -- anchor query for single trees.  stdin lines:  n v  u1 w1 u2 w2 ...   (edges, vertices 0..n-1)
// prints: ANCHOR/NOT, node count, and a witness labelling (labels 1..n, vertex order 0..n-1) if any.
// Same search as anch.cpp (definitions of README sections 1,2).  Optional argv[1] = node cap (0 = none); prints CAP if hit.
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[130]; vector<int> ch[130]; int cls[130]; int lab[130]; bool used_[300]; long long nodes, cap_=0; bool capped;
map<string,int> clsid;
string rootAt(int u,int p){ ch[u].clear(); vector<pair<string,int>> s; for(int w:adj[u]) if(w!=p) s.push_back({rootAt(w,u),w});
  sort(s.begin(),s.end()); string r="("; for(auto&x:s){ r+=x.first; ch[u].push_back(x.second);} r+=")";
  auto it=clsid.find(r); if(it==clsid.end()) it=clsid.insert({r,(int)clsid.size()}).first; cls[u]=it->second; return r; }
vector<int> labelled;
bool dfs(int k){ if(k==0) return true; nodes++; if(cap_&&nodes>cap_){capped=true;return false;}
  for(size_t i=0;i<labelled.size();i++){ int u=labelled[i];
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used_[x]) continue; int prev=-1;
      for(int w:ch[u]) if(!lab[w]){ if(cls[w]==prev) continue; prev=cls[w];
        lab[w]=x; used_[x]=1; labelled.push_back(w); bool ok=dfs(k-1); labelled.pop_back(); if(ok) return true; lab[w]=0; used_[x]=0; if(capped) return false; } } }
  return false; }
int main(int argc,char**argv){ if(argc>1) cap_=atoll(argv[1]); string line;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); int v; is>>n>>v; for(int i=0;i<n;i++) adj[i].clear(); int a,b; while(is>>a>>b){ adj[a].push_back(b); adj[b].push_back(a);} 
    clsid.clear(); rootAt(v,-1); memset(lab,0,sizeof lab); memset(used_,0,sizeof used_); labelled.clear(); lab[v]=1; used_[1]=1; labelled.push_back(v); nodes=0; capped=false;
    bool ok=dfs(n-1); printf("%s nodes=%lld",ok?"ANCHOR":(capped?"CAP":"NOT"),nodes); if(ok){ printf(" labels:"); for(int i=0;i<n;i++) printf(" %d",lab[i]); } printf("\n"); fflush(stdout); } }
