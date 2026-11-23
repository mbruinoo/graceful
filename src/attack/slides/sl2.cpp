// Lean version of sl.cpp for larger n: local minima by shape, and components under richer moves.
// usage: sl2 n
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; u64 W[32]; vector<u64> cf;
void rec(int k,int*p){
  if(k==0){ u64 x=0; for(int j=1;j<n;j++) x+=(u64)(p[j]-1)*W[j]; cf.push_back(x); return; }
  for(int pp=1;pp<=n-k;pp++){ p[k]=pp; int q[32]; for(int i=1;i<=n;i++)q[i]=i; bool ok=true;
    for(int j=n-1;j>=k;j--){int a=p[j],b=p[j]+j; while(q[a]!=a)a=q[a]; while(q[b]!=b)b=q[b]; if(a==b){ok=false;break;} q[a]=b;}
    if(ok) rec(k-1,p);} }
void dec(u64 x,int*p){ for(int k=1;k<n;k++) p[k]=(x/W[k])%(n-k)+1; }
long look(u64 x){ auto it=lower_bound(cf.begin(),cf.end(),x); return (it!=cf.end()&&*it==x)?it-cf.begin():-1; }
string canon(const int*p){
  vector<vector<int>> adj(n+1); for(int k=1;k<n;k++){adj[p[k]].push_back(p[k]+k);adj[p[k]+k].push_back(p[k]);}
  vector<int> deg(n+1),layer; int rem=n; for(int i=1;i<=n;i++){deg[i]=adj[i].size(); if(deg[i]<=1)layer.push_back(i);}
  vector<char> gone(n+1,0);
  while(rem>2){vector<int> nx; for(int v:layer){gone[v]=1;rem--; for(int u:adj[v]) if(!gone[u]&&--deg[u]==1) nx.push_back(u);} layer=nx;}
  function<string(int,int)> enc=[&](int v,int pa){vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch)s+=c; return s+")";};
  if(layer.size()==1) return enc(layer[0],0);
  string a=enc(layer[0],layer[1]),b=enc(layer[1],layer[0]); if(a>b)swap(a,b); return a+b;}
vector<int> uf; int ff(int x){while(uf[x]!=x){uf[x]=uf[uf[x]];x=uf[x];}return x;}
void un(long a,long b){a=ff(a);b=ff(b); if(a!=b)uf[a]=b;}
size_t ncomp(){ size_t c=0; for(size_t i=0;i<uf.size();i++) if(ff(i)==(int)i)c++; return c; }
int main(int argc,char**argv){ n=atoi(argv[1]);
  u64 w=1; for(int k=1;k<n;k++){W[k]=w;w*=(n-k);} int p[32]; rec(n-1,p); sort(cf.begin(),cf.end()); size_t N=cf.size();
  map<string,int> id; vector<long> cnt, mincnt; vector<u64> ex;
  uf.resize(N); iota(uf.begin(),uf.end(),0); size_t nmin=0;
  for(size_t i=0;i<N;i++){dec(cf[i],p); string c=canon(p); auto it=id.find(c); int t; if(it==id.end()){t=id.size(); id[c]=t; cnt.push_back(0); mincnt.push_back(0); ex.push_back(cf[i]);} else t=it->second; cnt[t]++;
    bool L=false; for(int k=1;k<n;k++){ if(p[k]>1){long j=look(cf[i]-W[k]); if(j>=0){L=true;un(i,j);}} }
    if(!L){nmin++; mincnt[t]++;} }
  int miss=0; for(size_t t=0;t<cnt.size();t++) if(!mincnt[t]) miss++;
  printf("n=%d placements=%zu shapes=%zu unit_components=%zu localmin=%zu shapes_missing_from_localmin=%d\n",n,N,id.size(),ncomp(),nmin,miss);
  for(size_t t=0;t<cnt.size();t++) if(!mincnt[t]){ dec(ex[t],p); printf("  missing: placements=%ld example edges:",cnt[t]); for(int k=n-1;k>=1;k--) printf(" {%d,%d}",p[k],p[k]+k); printf("\n"); }
  vector<int> unit=uf;
  for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) if(p[k]+2<=n-k){long j=look(cf[i]+2*W[k]); if(j>=0)un(i,j);} }
  printf("unit + slide-by-2: components=%zu\n",ncomp());
  uf=unit; for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) if(p[k]+k<=n-k){long j=look(cf[i]+(u64)k*W[k]); if(j>=0)un(i,j);} }
  printf("unit + reflect-through-foot: components=%zu\n",ncomp());
  uf=unit; for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) for(int l=k+1;l<n;l++) for(int s=-1;s<=1;s+=2) for(int t=-1;t<=1;t+=2){ if(s<0&&t<0)continue; int a=p[k]+s,b=p[l]+t; if(a<1||a>n-k||b<1||b>n-l)continue;
        u64 x=cf[i]+(s>0?W[k]:-W[k])+(t>0?W[l]:-W[l]); long j=look(x); if(j>=0)un(i,j);} }
  printf("unit + two-at-once: components=%zu\n",ncomp());
  // two-at-once restricted to adjacent lengths l=k+1
  uf=unit; for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n-1;k++){int l=k+1; for(int s=-1;s<=1;s+=2) for(int t=-1;t<=1;t+=2){ int a=p[k]+s,b=p[l]+t; if(a<1||a>n-k||b<1||b>n-l)continue;
        u64 x=cf[i]+(s>0?W[k]:-W[k])+(t>0?W[l]:-W[l]); long j=look(x); if(j>=0)un(i,j);} } }
  printf("unit + two-at-once (consecutive lengths only): components=%zu\n",ncomp());
  // two-at-once restricted to same direction
  uf=unit; for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) for(int l=k+1;l<n;l++){ if(p[k]+1>n-k||p[l]+1>n-l)continue; long j=look(cf[i]+W[k]+W[l]); if(j>=0)un(i,j);} }
  printf("unit + two-at-once (same direction only): components=%zu\n",ncomp());
}
