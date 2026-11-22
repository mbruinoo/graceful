// Slide graph of graceful trees in the "bracket" model.
// Vertices 1..n on a line. Bracket k (k=1..n-1) sits at position p_k in [1,n-k],
// giving edge {p_k, p_k+k}. A configuration is a tree-configuration if the n-1 edges form a tree.
// Unit slide: change one p_k by +-1 (result must again be a tree).
// Usage: slide n
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n;
vector<u64> W;            // mixed radix weights, W[k] for bracket k
vector<u64> cfgs;
int par[32];
int findp(int x){ while(par[x]!=x) x=par[x]; return x; }
int pos[32];
void dfs(int k, u64 idx){          // place brackets from longest (n-1) down to 1
  if(k==0){ cfgs.push_back(idx); return; }
  for(int p=1;p<=n-k;p++){
    int a=findp(p), b=findp(p+k);
    if(a==b) continue;
    par[a]=b; pos[k]=p;            // no path compression => simple undo
    dfs(k-1, idx+(u64)(p-1)*W[k]);
    par[a]=a;
  }
}
void decode(u64 idx,int*p){ for(int k=1;k<=n-1;k++){ p[k]=(idx/W[k])%(n-k)+1; } }
bool isTree(const int*p){
  int q[32]; for(int i=1;i<=n;i++) q[i]=i;
  for(int k=1;k<n;k++){ int a=p[k],b=p[k]+k; while(q[a]!=a)a=q[a]; while(q[b]!=b)b=q[b]; if(a==b) return false; q[a]=b; }
  return true;
}
// canonical form of tree (AHU from centre(s))
string canon(const int*p){
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
vector<int> uf;
int ff(int x){ while(uf[x]!=x){ uf[x]=uf[uf[x]]; x=uf[x]; } return x; }
int main(int argc,char**argv){
  n=atoi(argv[1]); bool iso = argc>2;
  W.assign(n+1,0); u64 w=1; for(int k=1;k<n;k++){ W[k]=w; w*=(n-k); }
  for(int i=1;i<=n;i++) par[i]=i;
  dfs(n-1,0);
  sort(cfgs.begin(),cfgs.end());
  size_t N=cfgs.size();
  auto lookup=[&](u64 x)->long{ auto it=lower_bound(cfgs.begin(),cfgs.end(),x); if(it!=cfgs.end()&&*it==x) return it-cfgs.begin(); return -1; };
  uf.resize(N); iota(uf.begin(),uf.end(),0);
  // stats
  size_t stuckLeft=0, isolated=0; u64 edges=0;
  vector<int> dist(N,-1);
  vector<vector<int>> dummy;
  vector<unsigned char> hasLeft(N,0);
  int p[32];
  for(size_t i=0;i<N;i++){
    decode(cfgs[i],p); int deg=0; bool left=false;
    for(int k=1;k<n;k++){
      if(p[k]>1){ long j=lookup(cfgs[i]-W[k]); if(j>=0){ deg++; left=true; int a=ff(i),b=ff(j); if(a!=b) uf[a]=b; edges++; } }
      if(p[k]<n-k){ long j=lookup(cfgs[i]+W[k]); if(j>=0) deg++; }
    }
    if(!left) stuckLeft++;
    if(deg==0) isolated++;
  }
  map<int,size_t> comp; for(size_t i=0;i<N;i++) comp[ff(i)]++;
  printf("n=%d treeConfigs=%zu slideEdges=%llu components=%zu noLeftSlide=%zu isolated=%zu\n",n,N,edges,comp.size(),stuckLeft,isolated);
  vector<pair<size_t,int>> cs; for(auto&c:comp) cs.push_back({c.second,c.first}); sort(cs.rbegin(),cs.rend());
  printf(" component sizes:"); for(size_t i=0;i<cs.size()&&i<12;i++) printf(" %zu",cs[i].first); printf("%s\n",cs.size()>12?" ...":"");
  // BFS from star at vertex 1 (index 0)
  { vector<int> q; q.push_back(0); dist[0]=0; int maxd=0;
    for(size_t h=0;h<q.size();h++){ int i=q[h]; decode(cfgs[i],p);
      for(int k=1;k<n;k++){ for(int s=-1;s<=1;s+=2){ int np=p[k]+s; if(np<1||np>n-k) continue; long j=lookup(cfgs[i]+(long long)s*(long long)W[k]); if(j>=0&&dist[j]<0){ dist[j]=dist[i]+1; maxd=max(maxd,dist[j]); q.push_back(j);} } } }
    printf(" reachable from star@1: %zu, eccentricity %d\n",q.size(),maxd);
  }
  if(iso){
    map<string,int> id; vector<int> minDist; vector<size_t> cnt; vector<set<int>> compsOf;
    map<int,set<int>> shapesIn;
    for(size_t i=0;i<N;i++){ decode(cfgs[i],p); string c=canon(p); auto it=id.find(c); int t; if(it==id.end()){ t=id.size(); id[c]=t; minDist.push_back(INT_MAX); cnt.push_back(0);} else t=it->second;
      cnt[t]++; if(dist[i]>=0) minDist[t]=min(minDist[t],dist[i]); shapesIn[ff(i)].insert(t); }
    int mx=0, unreach=0; for(size_t t=0;t<minDist.size();t++){ if(minDist[t]==INT_MAX) unreach++; else mx=max(mx,minDist[t]); }
    size_t mn=*min_element(cnt.begin(),cnt.end());
    printf(" tree shapes seen=%zu  shapes not in star component=%d  max over shapes of min slide-distance from star=%d  min #labelings of a shape=%zu\n",id.size(),unreach,mx,mn);
    printf(" shapes per component (largest comps):"); for(size_t i=0;i<cs.size()&&i<12;i++) printf(" %zu",shapesIn[cs[i].second].size()); printf("\n");
  }

  // --- monotone (right-slides only) reachability from star@1, and long-jump components
  { vector<char> seen(N,0); vector<int> q; q.push_back(0); seen[0]=1;
    for(size_t h=0;h<q.size();h++){ int i=q[h]; decode(cfgs[i],p);
      for(int k=1;k<n;k++){ if(p[k]<n-k){ long j=lookup(cfgs[i]+W[k]); if(j>=0&&!seen[j]){ seen[j]=1; q.push_back(j);} } } }
    set<string> sh; if(iso) for(int i:q){ decode(cfgs[i],p); sh.insert(canon(p)); }
    printf(" right-slides-only from star@1 reaches %zu configs, %zu shapes\n",q.size(),sh.size());
    iota(uf.begin(),uf.end(),0);
    for(size_t i=0;i<N;i++){ decode(cfgs[i],p); for(int k=1;k<n;k++) for(int np=p[k]+1;np<=n-k;np++){ long j=lookup(cfgs[i]+(u64)(np-p[k])*W[k]); if(j>=0){ int a=ff(i),b=ff(j); if(a!=b) uf[a]=b; } } }
    set<int> cc; for(size_t i=0;i<N;i++) cc.insert(ff(i));
    printf(" long-jump components=%zu\n",cc.size());
  }
}
