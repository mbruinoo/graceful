// Number of growth placements of each tree shape; report the scarcest shapes.  Usage: growcount n [howmany]
#include <bits/stdc++.h>
using namespace std;
int n; int p[32]; unsigned inV; unordered_map<string,long long> cnt;
string canon(){
  vector<vector<int>> adj(n+1);
  for(int k=1;k<n;k++){ adj[p[k]].push_back(p[k]+k); adj[p[k]+k].push_back(p[k]); }
  vector<int> deg(n+1), layer; int rem=n;
  for(int i=1;i<=n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
  vector<char> gone(n+1,0);
  while(rem>2){ vector<int> nx; for(int v:layer){ gone[v]=1; rem--; for(int u:adj[v]) if(!gone[u] && --deg[u]==1) nx.push_back(u);} layer=nx; }
  function<string(int,int)> enc=[&](int v,int pa){ vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch) s+=c; return s+")"; };
  if(layer.size()==1) return enc(layer[0],0);
  string a=enc(layer[0],layer[1]), b=enc(layer[1],layer[0]); if(a>b) swap(a,b); return a+"|"+b;
}
void dfs(int k){
  if(k==0){ cnt[canon()]++; return; }
  for(int q=1;q<=n-k;q++){ bool a=inV>>q&1, b=inV>>(q+k)&1; if(a==b) continue; unsigned s=inV; inV|=1u<<q|1u<<(q+k); p[k]=q; dfs(k-1); inV=s; }
}
int main(int c,char**v){ n=atoi(v[1]); int show=c>2?atoi(v[2]):8; p[n-1]=1; inV=1u<<1|1u<<n; dfs(n-2);
  vector<pair<long long,string>> L; long long tot=0; for(auto&e:cnt){ L.push_back({e.second,e.first}); tot+=e.second; } sort(L.begin(),L.end());
  printf("n=%d shapes=%zu total=%lld median=%lld\n",n,L.size(),tot,L[L.size()/2].first);
  for(int i=0;i<show&&i<(int)L.size();i++) printf("  %6lld  %s\n",L[i].first,L[i].second.c_str()); }
