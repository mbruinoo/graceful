// INTERVAL growth placements: growth placements in which the unused labels always form one interval (a,b).
// With k = b-a-1 the next bracket has length k and the new vertex is a+1 or b-1; four options:
//   A: new a+1 hangs on b          B: new a+1 hangs on 2a+2-b (mirror of b through a+1)
//   C: new b-1 hangs on a          D: new b-1 hangs on 2b-2-a (mirror of a through b-1)
// Count placements and the tree shapes they draw.  Usage: interval n
#include <bits/stdc++.h>
using namespace std;
int n; int p[32]; unordered_set<string> shapes; long long cnt=0;
string canon(){
  vector<vector<int>> adj(n+1);
  for(int k=1;k<n;k++){ adj[p[k]].push_back(p[k]+k); adj[p[k]+k].push_back(p[k]); }
  vector<int> deg(n+1), layer; int rem=n;
  for(int i=1;i<=n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
  vector<char> gone(n+1,0);
  while(rem>2){ vector<int> nx; for(int v:layer){ gone[v]=1; rem--; for(int u:adj[v]) if(!gone[u] && --deg[u]==1) nx.push_back(u);} layer=nx; }
  function<string(int,int)> enc=[&](int v,int pa){ vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch) s+=c; return s+")"; };
  if(layer.size()==1) return enc(layer[0],0);
  string a=enc(layer[0],layer[1]), b=enc(layer[1],layer[0]); if(a>b) swap(a,b); return a+b;
}
void rec(int a,int b){ int k=b-a-1;
  if(k==0){ cnt++; shapes.insert(canon()); return; }
  p[k]=a+1; rec(a+1,b);                               // A: {a+1,b}
  if(a+1-k>=1){ p[k]=a+1-k; rec(a+1,b); }             // B: {a+1-k,a+1}
  if(k>1 || true){ p[k]=a; if(!(k==0)) { /* C: {a,b-1} */ if(k>=1 && !(a+1==b-1 && false)) rec(a,b-1); } }
  if(b-1+k<=n){ p[k]=b-1; rec(a,b-1); }               // D: {b-1,b-1+k}
}
int main(int c,char**v){ n=atoi(v[1]); p[n-1]=1; rec(1,n); printf("n=%d interval-growth placements(with repeats)=%lld shapes=%zu\n",n,cnt,shapes.size()); if(c>2){ FILE*f=fopen(v[2],"w"); for(auto&s:shapes) fprintf(f,"%s\n",s.c_str()); fclose(f);} }
