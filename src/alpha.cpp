// Tree shapes having an alpha-placement (all brackets jump over one common point: max left foot < min right foot),
// and shapes having an alpha GROWTH placement.  Writes shape lists.  Usage: alpha n outprefix
#include <bits/stdc++.h>
using namespace std;
int n; int p[32]; set<string> A, AG;
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
int par[32]; int fnd(int x){ while(par[x]!=x) x=par[x]; return x; }
// place brackets longest first; keep maxLeft < minRight; forest check via union-find; track growth (connected) flag
void rec(int k,int maxL,int minR,bool growth,unsigned S){
  if(k==0){ string c=canon(); A.insert(c); if(growth) AG.insert(c); return; }
  for(int q=1;q<=n-k;q++){ int nl=max(maxL,q), nr=min(minR,q+k); if(nl>=nr) continue; int a=fnd(q), b=fnd(q+k); if(a==b) continue;
    bool g=growth && (((S>>q)&1)!=((S>>(q+k))&1)); par[a]=b; p[k]=q; rec(k-1,nl,nr,g,S|1u<<q|1u<<(q+k)); par[a]=a; }
}
int main(int c,char**v){ n=atoi(v[1]); for(int i=1;i<=n;i++) par[i]=i; p[n-1]=1; par[1]=n; rec(n-2,1,n,true,1u<<1|1u<<n);
  printf("n=%d shapes with alpha placement=%zu, with alpha growth placement=%zu\n",n,A.size(),AG.size());
  if(c>2){ FILE*f=fopen((string(v[2])+"a"+v[1]+".txt").c_str(),"w"); for(auto&s:A) fprintf(f,"%s\n",s.c_str()); fclose(f); f=fopen((string(v[2])+"ag"+v[1]+".txt").c_str(),"w"); for(auto&s:AG) fprintf(f,"%s\n",s.c_str()); fclose(f);} }
