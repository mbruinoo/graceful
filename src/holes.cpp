// Growth placements in which the unused labels never split into more than R runs (maximal intervals).
// R=1 is the "interval" variant.  Counts placements and the tree shapes drawn.   Usage: holes n R [HS [SIDE]]  (SIDE=1: at most one hole each side of the main run; SIDE=2: holes all on one side)
//   (HS: all runs but the longest have at most HS cells)
#include <bits/stdc++.h>
using namespace std;
int n,R,HS,SIDE=0;  /* HS: every run except the longest may have at most HS cells (0 = no limit) */  int p[32]; unsigned inV; unordered_set<string> shapes; long long cnt=0;
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
int runs(unsigned S){ unsigned un=~S & (((1u<<n)-1)<<1); return __builtin_popcount(un & ~(un<<1)); }   // starts of runs of unused labels
bool holesOK(unsigned S){ if(!HS) return true; int big=0,cur=0,over=0,bigcount=0; vector<int> sz; for(int i=1;i<=n+1;i++){ if(i<=n && !(S>>i&1)) cur++; else { if(cur) sz.push_back(cur); cur=0; } }
  if(sz.empty()) return true; size_t bi=0; for(size_t i=0;i<sz.size();i++) if(sz[i]>sz[bi]) bi=i;       /* sz is in left-to-right order; bi = first longest run */
  for(size_t i=0;i<sz.size();i++) if(i!=bi && sz[i]>HS) return false;
  if(SIDE==1 && (bi>1 || sz.size()-1-bi>1)) return false;        /* at most one hole on each side of the main run */
  if(SIDE==2 && bi>0 && bi+1<sz.size()) return false;            /* all holes on one side of the main run */
  return true; }
void dfs(int k){
  if(k==0){ cnt++; shapes.insert(canon()); return; }
  for(int q=1;q<=n-k;q++){ bool a=inV>>q&1, b=inV>>(q+k)&1; if(a==b) continue; unsigned s=inV; inV|=1u<<q|1u<<(q+k); if(runs(inV)<=R && holesOK(inV)){ p[k]=q; dfs(k-1);} inV=s; }
}
int main(int c,char**v){ n=atoi(v[1]); R=atoi(v[2]); HS=c>3?atoi(v[3]):0; SIDE=c>4?atoi(v[4]):0; p[n-1]=1; inV=1u<<1|1u<<n; dfs(n-2); printf("n=%d runs<=%d holesize<=%d side-rule=%d placements=%lld shapes=%zu\n",n,R,HS,SIDE,cnt,shapes.size()); }
