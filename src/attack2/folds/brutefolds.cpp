// brutefolds.cpp -- which fold types are needed?  Enumerates EVERY growth placement on n cells (as brute.cpp) and
// records, for every tree shape and every SET of non-staircase fold types, the least cost A of a placement whose
// non-staircase steps all have types in that set.  Fold types (bit), relative to the main run M (longest, leftmost):
//   1  K1  : x one cell in from an end of M, bracket covers the rest of M           (single skip, across)
//   2  K1* : x one cell in from an end of M, bracket covers only the one end cell   (single skip, back)   [M >= 4 cells]
//   4  Kbig: any other split of M (both pieces >= 2 cells)
//   8  B   : x an end cell of M, bracket points away from M (back step)
//  16  F   : x a single-cell run that is not M
//  32  Fbig: x in a run of >= 2 cells that is not M
// (a run of 3 cells split in the middle counts as K1.)   Output: code, then 64 numbers (min cost for each mask, -1 none).
#include <bits/stdc++.h>
using namespace std;
int n; int used_[40]; vector<pair<int,int>> E; map<string,array<int,64>> best; vector<int> g[40];
string enc(int v,int p){ vector<string> ch; for(int u:g[v]) if(u!=p) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string r="("; for(auto&c:ch) r+=c; return r+")"; }
string canon(){ for(int i=1;i<=n;i++) g[i].clear(); for(auto&e:E){ g[e.first].push_back(e.second); g[e.second].push_back(e.first); }
  vector<int> deg(n+1), alive(n+1,1); int left=n; vector<int> lv; for(int i=1;i<=n;i++){ deg[i]=g[i].size(); if(deg[i]<=1) lv.push_back(i); }
  while(left>2){ vector<int> nx; for(int v:lv){ alive[v]=0; left--; for(int u:g[v]) if(alive[u] && --deg[u]==1) nx.push_back(u); } lv=nx; }
  vector<int> c; for(int i=1;i<=n;i++) if(alive[i]) c.push_back(i);
  if(c.size()==1) return enc(c[0],0);
  string a=enc(c[0],c[1]), b=enc(c[1],c[0]); if(a>b) swap(a,b); return a+"|"+b; }
void rec(int t,int cost,int mask){
  if(t==0){ string c=canon(); auto it=best.find(c); if(it==best.end()){ array<int,64> a; a.fill(-1); it=best.insert({c,a}).first; } int &v=it->second[mask]; if(v<0||cost<v) v=cost; return; }
  int ml=0,mh=-1; { int i=1; while(i<=n){ if(!used_[i]){ int j=i; while(j<n&&!used_[j+1]) j++; if(j-i>mh-ml){ ml=i; mh=j; } i=j+1; } else i++; } }
  for(int x=1;x<=n;x++) if(!used_[x]) for(int s=-1;s<=1;s+=2){ int y=x+s*t; if(y<1||y>n||!used_[y]) continue;
    int lo=x,hi=x; while(lo>1&&!used_[lo-1]) lo--; while(hi<n&&!used_[hi+1]) hi++;
    int r=(y>x)? x-lo : hi-x, c=(hi-lo)-r; int ty=0;
    if(lo==ml){ if(r==0) ty=0; else if(c==0) ty=8; else if(r==1) ty=1; else if(c==1) ty=2; else ty=4; }
    else ty=(lo==hi)?16:32;
    used_[x]=1; E.push_back({x,y}); rec(t-1,cost+(ty?1:0),mask|ty); E.pop_back(); used_[x]=0; } }
int main(int argc,char**argv){ n=atoi(argv[1]); used_[1]=used_[n]=1; E.push_back({1,n}); rec(n-2,0,0);
  for(auto&kv:best){ printf("%s",kv.first.c_str()); for(int m=0;m<64;m++) printf(" %d",kv.second[m]); printf("\n"); } }
