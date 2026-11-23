// anch.cpp -- exhaustive anchor computation, written from the definitions in README sections 1, 2, 8.
// A vertex v of a tree T (n vertices) is an ANCHOR if there is a growth placement with label(v)=1:
// labels 1..n bijective, edge lengths 1..n-1 each once, and brackets n-1,n-2,...,k connected for every k.
// Search: label v=1; for k=n-1..1 attach an unlabelled neighbour w of a labelled u at label(u)+-k.
// Symmetry reduction: among unlabelled children of u (tree rooted at v) with isomorphic subtrees only the first is tried.
// Usage: anch n [part parts] [v]   -> prints one line per non-anchor orbit, and a summary line.
//   line: NA n deg(v) leafflag  branches-of-v (AHU strings, sorted) | edge list | v
#include <bits/stdc++.h>
#include "../../treegen.h"
using namespace std;
int n; vector<int> adj[40]; int par_[40]; vector<int> ch[40]; int cls[40]; int lab[40]; bool used_[80];
long long nodes;
string ahu(int u,int p){ vector<string> s; for(int w:adj[u]) if(w!=p) s.push_back(ahu(w,u)); sort(s.begin(),s.end()); string r="("; for(auto&x:s) r+=x; return r+")"; }
map<string,int> clsid;
string rootAt(int u,int p){ // fills ch, cls
  ch[u].clear(); vector<pair<string,int>> s; for(int w:adj[u]) if(w!=p){ s.push_back({rootAt(w,u),w}); }
  sort(s.begin(),s.end()); string r="("; for(auto&x:s){ r+=x.first; ch[u].push_back(x.second);} r+=")";
  auto it=clsid.find(r); if(it==clsid.end()) it=clsid.insert({r,(int)clsid.size()}).first; cls[u]=it->second; return r; }
vector<int> labelled; // list of labelled vertices
bool dfs(int k){
  if(k==0) return true; nodes++;
  for(size_t i=0;i<labelled.size();i++){ int u=labelled[i];
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used_[x]) continue;
      int prev=-1;
      for(int w:ch[u]) if(!lab[w]){ if(cls[w]==prev) continue; prev=cls[w];
        lab[w]=x; used_[x]=1; labelled.push_back(w); bool ok=dfs(k-1); labelled.pop_back(); lab[w]=0; used_[x]=0; if(ok) return true; } } }
  return false; }
bool anchor(int v){ clsid.clear(); rootAt(v,-1); memset(lab,0,sizeof lab); memset(used_,0,sizeof used_); labelled.clear(); lab[v]=1; used_[1]=1; labelled.push_back(v); return dfs(n-1); }
int main(int argc,char**argv){
  n=atoi(argv[1]); int part=argc>3?atoi(argv[2]):0, parts=argc>3?atoi(argv[3]):1;
  TreeGen g(n); vector<int> par; long idx=0, trees=0, verts=0, na=0, naLeaf=0, naInt=0, allA=0, noA=0, noMaxdeg=0, noLeafA=0, kindsInt=0, kindsLeaf=0; map<int,long> byDeg, kindDeg;
  while(g.next()){ if((idx++)%parts!=part) continue; g.parents(par); for(int i=0;i<n;i++) adj[i].clear(); for(int i=1;i<n;i++){ adj[i].push_back(par[i]); adj[par[i]].push_back(i);} trees++;
    int md=0; for(int i=0;i<n;i++) md=max(md,(int)adj[i].size());
    map<string,int> orb; bool all=true, any=false, mdok=false, leafA=false;
    for(int v=0;v<n;v++){ verts++; string key=ahu(v,-1); int a; auto it=orb.find(key); bool fresh=(it==orb.end());
      if(fresh){ a=anchor(v); orb[key]=a; } else a=it->second;
      int d=adj[v].size();
      if(a){ any=true; if(d==md) mdok=true; if(d==1) leafA=true; }
      else { all=false; na++; byDeg[d]++; if(d==1) naLeaf++; else naInt++;
        if(fresh){ kindDeg[d]++; if(d==1) kindsLeaf++; else kindsInt++;
          vector<string> br; for(int w:adj[v]) br.push_back(ahu(w,v)); sort(br.begin(),br.end(),[](const string&a,const string&b){return a.size()!=b.size()?a.size()>b.size():a<b;});
          printf("NA %d deg%d %s",n,d,d==1?"leaf":"internal"); for(auto&b:br) printf(" %s",b.c_str()); printf(" |"); for(int i=1;i<n;i++) printf(" %d-%d",par[i],i); printf(" | v=%d\n",v); } } }
    if(all) allA++; if(!any) noA++; if(!mdok) { noMaxdeg++; printf("NOMAXDEG %d |",n); for(int i=1;i<n;i++) printf(" %d-%d",par[i],i); printf("\n"); } if(!leafA) noLeafA++;
  }
  printf("SUMMARY n=%d part=%d/%d trees=%ld vertices=%ld nonAnchors=%ld (leaf %ld, internal %ld) kinds(leaf %ld, internal %ld) allAnchorTrees=%ld treesNoAnchor=%ld treesNoMaxDegAnchor=%ld treesNoLeafAnchor=%ld nodes=%lld | nonanchors by degree:",n,part,parts,trees,verts,na,naLeaf,naInt,kindsLeaf,kindsInt,allA,noA,noMaxdeg,noLeafA,nodes);
  for(auto&p:byDeg) printf(" d%d:%ld",p.first,p.second); printf(" | kinds by degree:"); for(auto&p:kindDeg) printf(" d%d:%ld",p.first,p.second); printf("\n");
}
