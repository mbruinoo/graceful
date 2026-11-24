// brute.cpp -- independent cross-check of tidy.cpp.  Enumerates EVERY growth placement on n cells by the balance rule
// (README Lemma 10: with t cells unused, a fresh cell x joins a used cell x-t or x+t), computes cost A and cost B of
// each (definitions in tidy.cpp, re-implemented here), and prints for every tree shape (canonical centre-rooted
// parenthesis code) the minimum of each cost and the number of growth placements.   Usage: brute n
#include <bits/stdc++.h>
using namespace std;
int n; int used_[40]; vector<pair<int,int>> E; long long total=0;
struct Rec{ int a,b; long long cnt; }; map<string,Rec> best;
vector<int> g[40];
string enc(int v,int p){ vector<string> ch; for(int u:g[v]) if(u!=p) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string r="("; for(auto&c:ch) r+=c; return r+")"; }
string canon(){ for(int i=1;i<=n;i++) g[i].clear(); for(auto&e:E){ g[e.first].push_back(e.second); g[e.second].push_back(e.first); }
  // centre(s) by peeling leaves
  vector<int> deg(n+1), alive(n+1,1); int left=n; vector<int> lv; for(int i=1;i<=n;i++){ deg[i]=g[i].size(); if(deg[i]<=1) lv.push_back(i); }
  while(left>2){ vector<int> nx; for(int v:lv){ alive[v]=0; left--; for(int u:g[v]) if(alive[u] && --deg[u]==1) nx.push_back(u); } lv=nx; }
  vector<int> c; for(int i=1;i<=n;i++) if(alive[i]) c.push_back(i);
  if(c.size()==1) return enc(c[0],0);
  string a=enc(c[0],c[1]), b=enc(c[1],c[0]); if(a>b) swap(a,b); return a+"|"+b; }
void rec(int t,int ca,int cb){
  if(t==0){ total++; string c=canon(); auto it=best.find(c); if(it==best.end()) best[c]={ca,cb,1}; else { it->second.a=min(it->second.a,ca); it->second.b=min(it->second.b,cb); it->second.cnt++; } return; }
  // main run (longest, leftmost)
  int ml=0,mh=-1; { int i=1; while(i<=n){ if(!used_[i]){ int j=i; while(j<n&&!used_[j+1]) j++; if(j-i>mh-ml){ ml=i; mh=j; } i=j+1; } else i++; } }
  for(int x=1;x<=n;x++) if(!used_[x]) for(int s=-1;s<=1;s+=2){ int y=x+s*t; if(y<1||y>n||!used_[y]) continue;
    int lo=x,hi=x; while(lo>1&&!used_[lo-1]) lo--; while(hi<n&&!used_[hi+1]) hi++;
    int r=(y>x)? x-lo : hi-x; int da=(r==0 && lo==ml)?0:1, db=(r==0)?0:1;
    used_[x]=1; E.push_back({x,y}); rec(t-1,ca+da,cb+db); E.pop_back(); used_[x]=0; } }
int main(int argc,char**argv){ n=atoi(argv[1]); used_[1]=used_[n]=1; E.push_back({1,n}); rec(n-2,0,0);
  for(auto&kv:best) printf("%s %d %d %lld\n",kv.first.c_str(),kv.second.a,kv.second.b,kv.second.cnt);
  fprintf(stderr,"n=%d growth placements=%lld shapes=%zu\n",n,total,best.size()); }
