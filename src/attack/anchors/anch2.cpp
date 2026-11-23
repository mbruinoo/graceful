// anch2.cpp -- anchor decisions with a restart strategy (same definitions as anch.cpp; README sections 1, 2, 8).
// The search tries four branching orders under growing node caps and only then exhausts, so a slow success
// under one order does not dominate.  A vertex is reported as a non-anchor only after an UNCAPPED exhaustive search.
// Modes:
//   anch2 deg n mindeg [part parts]   every tree on n vertices (src/treegen.h), every vertex orbit of degree >= mindeg
//   anch2 pend k l [part parts]       every rooted tree (R,c) on k vertices; T = R + v joined to c + l leaves at v; test v
#include <bits/stdc++.h>
#include "../../treegen.h"
using namespace std;
int n; vector<int> adj[40]; vector<int> ch[40]; int cls[40]; int lab[40]; bool used_[80]; long long nodes, cap_, total; bool capped; int ordA, ordS;
map<string,int> clsid;
string ahu(int u,int p){ vector<string> s; for(int w:adj[u]) if(w!=p) s.push_back(ahu(w,u)); sort(s.begin(),s.end()); string r="("; for(auto&x:s) r+=x; return r+")"; }
string rootAt(int u,int p){ ch[u].clear(); vector<pair<string,int>> s; for(int w:adj[u]) if(w!=p) s.push_back({rootAt(w,u),w});
  sort(s.begin(),s.end()); string r="("; for(auto&x:s){ r+=x.first; ch[u].push_back(x.second);} r+=")";
  auto it=clsid.find(r); if(it==clsid.end()) it=clsid.insert({r,(int)clsid.size()}).first; cls[u]=it->second; return r; }
vector<int> labelled;
bool dfs(int k){ if(k==0) return true; nodes++; if(cap_&&nodes>cap_){ capped=true; return false; }
  int sz=labelled.size();
  for(int ii=0;ii<sz;ii++){ int u=labelled[ordA?sz-1-ii:ii];
    for(int t=0;t<2;t++){ int s=(t==ordS)?-1:1; int x=lab[u]+s*k; if(x<1||x>n||used_[x]) continue; int prev=-1;
      for(int w:ch[u]) if(!lab[w]){ if(cls[w]==prev) continue; prev=cls[w];
        lab[w]=x; used_[x]=1; labelled.push_back(w); bool ok=dfs(k-1); labelled.pop_back(); lab[w]=0; used_[x]=0; if(ok) return true; if(capped) return false; } } }
  return false; }
bool anchor(int v){ clsid.clear(); rootAt(v,-1);
  static const long long caps[]={3000,100000,3000000,0};
  for(int c=0;c<4;c++) for(int o=0;o<4;o++){ if(caps[c]==0&&o>0) break; ordA=o&1; ordS=o>>1; cap_=caps[c]; nodes=0; capped=false;
    memset(lab,0,sizeof lab); memset(used_,0,sizeof used_); labelled.clear(); lab[v]=1; used_[1]=1; labelled.push_back(v);
    bool ok=dfs(n-1); total+=nodes; if(ok) return true; if(!capped) return false; }
  return false; }
int main(int argc,char**argv){ string mode=argv[1];
  if(mode=="deg"){ n=atoi(argv[2]); int mindeg=atoi(argv[3]); int part=argc>5?atoi(argv[4]):0, parts=argc>5?atoi(argv[5]):1;
    TreeGen g(n); vector<int> par; long idx=0,trees=0,tested=0,non=0; map<int,long> byDeg;
    while(g.next()){ if((idx++)%parts!=part) continue; g.parents(par); for(int i=0;i<n;i++) adj[i].clear(); for(int i=1;i<n;i++){ adj[i].push_back(par[i]); adj[par[i]].push_back(i);} trees++;
      set<string> seen;
      for(int v=0;v<n;v++){ if((int)adj[v].size()<mindeg) continue; string key=ahu(v,-1); if(!seen.insert(key).second) continue; tested++;
        if(!anchor(v)){ non++; byDeg[adj[v].size()]++; printf("NONANCHOR n=%d deg=%d |",n,(int)adj[v].size()); for(int i=1;i<n;i++) printf(" %d-%d",par[i],i); printf(" | v=%d\n",v); fflush(stdout); } } }
    printf("SUMMARY deg n=%d mindeg=%d part=%d/%d trees=%ld vertex-orbits tested=%ld non-anchors=%ld nodes=%lld |",n,mindeg,part,parts,trees,tested,non,total); for(auto&p:byDeg) printf(" d%d:%ld",p.first,p.second); printf("\n");
  } else { int k=atoi(argv[2]), l=atoi(argv[3]); int part=argc>5?atoi(argv[4]):0, parts=argc>5?atoi(argv[5]):1;
    n=k+1+l; vector<int> L(k); for(int i=0;i<k;i++) L[i]=i; long idx=0,tested=0,non=0;
    while(true){
      if((idx++)%parts==part){ for(int i=0;i<n;i++) adj[i].clear(); vector<int> st;
        for(int i=0;i<k;i++){ while(!st.empty()&&L[st.back()]>=L[i]) st.pop_back(); if(!st.empty()){ adj[i].push_back(st.back()); adj[st.back()].push_back(i);} st.push_back(i); }
        adj[k].push_back(0); adj[0].push_back(k); for(int j=0;j<l;j++){ adj[k].push_back(k+1+j); adj[k+1+j].push_back(k); }
        tested++; if(!anchor(k)){ non++; printf("NONANCHOR n=%d deg=%d R(level sequence from c):",n,l+1); for(int i=0;i<k;i++) printf(" %d",L[i]); printf("\n"); fflush(stdout); } }
      int p=k-1; while(p>0&&L[p]==1) p--; if(p==0) break; int q=p-1; while(L[q]!=L[p]-1) q--; for(int i=p;i<k;i++) L[i]=L[i-(p-q)]; }
    printf("SUMMARY pend k=%d l=%d n=%d part=%d/%d rooted trees tested=%ld non-anchors=%ld nodes=%lld\n",k,l,n,part,parts,tested,non,total); }
}
