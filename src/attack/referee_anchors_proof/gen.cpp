// Referee solver, written from README section 1 only.
// Input lines: n root  a b  a b ... (n-1 edges, vertices 0..n-1).  Output: YES/NO nodes [witness labels]
// Decides whether a growth placement exists with label 0 (README: label 1) on root.
// Brackets m..1 longest first, each with exactly one used foot. Sibling subtrees of equal shape interchangeable.
#include <bits/stdc++.h>
using namespace std;
int n,m,root; vector<vector<int>> adj, ch; vector<int> cls; 
vector<vector<pair<int,vector<int>>>> groups; // per vertex: (class, list of children)
vector<vector<int>> used_in_group; // per vertex per group count assigned
vector<int> lab; // label -> vertex
vector<int> vlab;
long long nodes; long long limit;
map<string,int> canon;
string build(int u,int p){ vector<pair<string,int>> s; for(int w:adj[u]) if(w!=p){ ch[u].push_back(w); s.push_back({build(w,u),w}); }
  sort(s.begin(),s.end()); string r="("; for(auto&x:s) r+=x.first; r+=")";
  if(!canon.count(r)){int id=canon.size(); canon[r]=id;} cls[u]=canon[r];
  // groups
  map<int,vector<int>> g; for(int w:ch[u]) g[cls[w]].push_back(w);
  for(auto&kv:g) groups[u].push_back({kv.first,kv.second});
  used_in_group[u].assign(groups[u].size(),0);
  return r; }
bool rec(int k){
  if(k==0) return true;
  nodes++; if(limit && nodes>limit) throw 1;
  for(int a=0;a+k<=m;a++){
    int ua=lab[a], ub=lab[a+k];
    if((ua<0)==(ub<0)) continue;
    int u = ua>=0?ua:ub; int fresh = ua>=0? a+k : a;
    for(size_t g=0;g<groups[u].size();g++){
      int c=used_in_group[u][g]; if(c>=(int)groups[u][g].second.size()) continue;
      int w=groups[u][g].second[c];
      used_in_group[u][g]++; lab[fresh]=w; vlab[w]=fresh;
      if(rec(k-1)) return true;
      used_in_group[u][g]--; lab[fresh]=-1; vlab[w]=-1;
    }
  }
  return false;
}
int main(int argc,char**argv){ limit = argc>1? atoll(argv[1]):0; string line;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n>>root; m=n-1;
    adj.assign(n,{}); ch.assign(n,{}); cls.assign(n,0); groups.assign(n,{}); used_in_group.assign(n,{}); canon.clear();
    for(int i=0;i<m;i++){int a,b; is>>a>>b; adj[a].push_back(b); adj[b].push_back(a);}
    build(root,-1); lab.assign(n,-1); vlab.assign(n,-1); lab[0]=root; vlab[root]=0; nodes=0;
    try{ bool ok=rec(m); printf("%s %lld",ok?"YES":"NO",nodes); if(ok){ for(int v=0;v<n;v++) printf(" %d",vlab[v]); } printf("\n"); }
    catch(int){ printf("TIMEOUT %lld\n",nodes); }
    fflush(stdout);
  }
}
