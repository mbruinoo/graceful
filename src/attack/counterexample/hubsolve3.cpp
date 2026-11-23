// As hubsolve.cpp, but the part handed to the exact cover consists of small pendant BRANCHES, not only leaves:
// rooting the tree at its centre, a branch is a maximal subtree with at most 3 vertices; shapes: leaf, path of 2,
// path of 3, cherry (a vertex with two leaves).  The remaining vertices are the skeleton.
// Stage 1: skeleton labelled longest length first from an anchor (label 1) among skeleton vertices; a length may be
//   deferred to the branches if it fits under a labelled skeleton vertex with spare branch capacity.
// Stage 2: exact cover; items = remaining lengths and labels; option = a heap-ordered labelling of one branch at
//   one skeleton vertex v (all its lengths < length of v's parent edge, decreasing outward); each (v, shape) has a quota.
// Randomised with restarts; a failure proves nothing.  Every placement found is re-checked from the definition.
// usage: hubsolve3 [tries=100000] [stage2 node limit=3000]     env SHOW=1 prints "tree | labels"
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[130]; int lab[130], dpar[130]; bool inBranch[130]; bool usedLab[130], usedLen[130];
vector<int> order_, parentOf, cpar; mt19937 rng(123); long long s2limit, tries, triesDone, cap, nodes1; bool found;
struct Br{ int v,type; vector<int> verts; };  // attached at skeleton vertex v; verts in a fixed order (see embed)
vector<Br> branches; int quota[130][4]; int capTot[130];
struct Opt{ int v,type,ni; int it[6]; int labs[3]; }; vector<Opt> opt; vector<vector<int>> byItem; vector<vector<int>> cnt; vector<char> covered, dead; int q2[130][4]; long long nodes2; int needBr; vector<int> chosen;
bool cover(int depth){
  if(depth==needBr) return true; if(++nodes2>s2limit) return false;
  int NI=2*n; int best=-1, bc=1<<30; for(int it=0;it<NI;it++) if(!covered[it]){ int c=0; for(int v:order_) for(int t=0;t<4;t++) if(q2[v][t]>0) c+=cnt[it][v*4+t]; if(c<bc || (c==bc && (rng()&1))){ bc=c; best=it; } }
  if(bc==0) return false;
  vector<int> cand; for(int o:byItem[best]) if(!dead[o] && q2[opt[o].v][opt[o].type]>0) cand.push_back(o); shuffle(cand.begin(),cand.end(),rng);
  for(int o:cand){ vector<int> killed; for(int j=0;j<opt[o].ni;j++){ int it=opt[o].it[j]; covered[it]=1; for(int q:byItem[it]) if(!dead[q]){ dead[q]=1; killed.push_back(q); for(int t=0;t<opt[q].ni;t++) cnt[opt[q].it[t]][opt[q].v*4+opt[q].type]--; } }
    q2[opt[o].v][opt[o].type]--; chosen.push_back(o); if(cover(depth+1)) return true; chosen.pop_back(); q2[opt[o].v][opt[o].type]++;
    for(int q:killed){ dead[q]=0; for(int t=0;t<opt[q].ni;t++) cnt[opt[q].it[t]][opt[q].v*4+opt[q].type]++; } for(int j=0;j<opt[o].ni;j++) covered[opt[o].it[j]]=0; if(nodes2>s2limit) return false; }
  return false; }
inline bool okL(int x){ return x>=1&&x<=n&&!usedLab[x]; }
void addOpt(int v,int type,int k1,int x1,int k2,int x2,int k3,int x3){ Opt o; o.v=v; o.type=type; o.ni=0; int ks[3]={k1,k2,k3}, xs[3]={x1,x2,x3}; int m= type==0?1: type==1?2:3;
  for(int i=0;i<m;i++) for(int j=i+1;j<m;j++) if(xs[i]==xs[j]) return;
  for(int i=0;i<m;i++){ o.it[o.ni++]=ks[i]-1; o.it[o.ni++]=n-1+xs[i]-1; o.labs[i]=xs[i]; } opt.push_back(o); }
bool stage2(){
  opt.clear();
  for(int v:order_){ int L=lab[v], D=dpar[v];
    for(int a=1;a<D;a++) if(!usedLen[a]) for(int s1=-1;s1<=1;s1+=2){ int x1=L+s1*a; if(!okL(x1)) continue;
      if(quota[v][0]) addOpt(v,0,a,x1,0,0,0,0);
      if(quota[v][1]||quota[v][2]||quota[v][3]) for(int b=1;b<a;b++) if(!usedLen[b]) for(int s2=-1;s2<=1;s2+=2){ int x2=x1+s2*b; if(!okL(x2)) continue;
        if(quota[v][1]) addOpt(v,1,a,x1,b,x2,0,0);
        if(quota[v][2]||quota[v][3]) for(int c=1;c<b;c++) if(!usedLen[c]) for(int s3=-1;s3<=1;s3+=2){
          if(quota[v][2]){ int x3=x2+s3*c; if(okL(x3)) addOpt(v,2,a,x1,b,x2,c,x3); }        // path: v - x1 - x2 - x3
          if(quota[v][3]){ int x3=x1+s3*c; if(okL(x3)) addOpt(v,3,a,x1,b,x2,c,x3); } } } } }  // cherry: v - x1, x1 - x2, x1 - x3 (b > c)
  byItem.assign(2*n,{}); cnt.assign(2*n,vector<int>(4*n,0)); covered.assign(2*n,1); dead.assign(opt.size(),0);
  for(int k=1;k<n;k++) if(!usedLen[k]) covered[k-1]=0; for(int x=1;x<=n;x++) if(!usedLab[x]) covered[n-1+x-1]=0;
  for(size_t i=0;i<opt.size();i++) for(int j=0;j<opt[i].ni;j++){ byItem[opt[i].it[j]].push_back(i); cnt[opt[i].it[j]][opt[i].v*4+opt[i].type]++; }
  for(int v:order_) for(int t=0;t<4;t++) q2[v][t]=quota[v][t]; nodes2=0; chosen.clear(); return cover(0); }
int finalLab[130];
bool verifyAndStore(){ vector<int> L(n,0); for(int v=0;v<n;v++) if(!inBranch[v]) L[v]=lab[v]; vector<char> usedBr(branches.size(),0);
  for(int o:chosen){ int bi=-1; for(size_t i=0;i<branches.size();i++) if(!usedBr[i] && branches[i].v==opt[o].v && branches[i].type==opt[o].type){ bi=i; break; } if(bi<0) return false; usedBr[bi]=1;
    for(size_t j=0;j<branches[bi].verts.size();j++) L[branches[bi].verts[j]]=opt[o].labs[j]; }
  vector<int> seenL(n+1,0), len(n,0); for(int i=0;i<n;i++){ if(L[i]<1||L[i]>n||seenL[L[i]]) return false; seenL[L[i]]=1; }
  vector<pair<int,pair<int,int>>> E; for(int u=0;u<n;u++) for(int w:adj[u]) if(u<w){ int d=abs(L[u]-L[w]); if(d<1||d>n-1||len[d]) return false; len[d]=1; E.push_back({d,{u,w}}); }
  if((int)E.size()!=n-1) return false; sort(E.rbegin(),E.rend()); vector<char> in(n,0); in[E[0].second.first]=in[E[0].second.second]=1;
  for(int i=1;i<n-1;i++){ int a=E[i].second.first,b=E[i].second.second; if(in[a]==in[b]) return false; in[a]=in[b]=1; }
  for(int i=0;i<n;i++) finalLab[i]=L[i]; return true; }
int nSkelLeft; vector<int> deferred;
bool hallOK(){ vector<pair<int,int>> hubs; for(int v:order_) if(lab[v] && capTot[v]) hubs.push_back({dpar[v],capTot[v]}); sort(hubs.rbegin(),hubs.rend());
  size_t j=0; long long cum=0; for(size_t i=0;i<deferred.size();i++){ int k=deferred[i]; while(j<hubs.size() && hubs[j].first>k){ cum+=hubs[j].second; j++; } if((long long)(i+1)>cum) return false; } return true; }
bool stage1(int k){
  if(found) return true;
  if(nSkelLeft==0){ triesDone++; if(stage2()){ found=true; return true; } return false; }
  if(k==0 || triesDone>=cap) return false; if(++nodes1>5000000){ triesDone=cap; return false; }
  vector<pair<int,int>> cand;
  for(int v:order_) if(!lab[v]){ int p=parentOf[v]; if(!lab[p] || dpar[p]<=k) continue; for(int sg=-1;sg<=1;sg+=2){ int x=lab[p]+sg*k; if(x>=1&&x<=n&&!usedLab[x]) cand.push_back({v,x}); } }
  cand.push_back({-1,0}); shuffle(cand.begin(),cand.end(),rng);
  for(auto c:cand){
    if(c.first<0){ deferred.push_back(k); bool ok=hallOK(); if(ok && stage1(k-1)) return true; deferred.pop_back(); }
    else { int v=c.first,x=c.second; lab[v]=x; dpar[v]=k; usedLab[x]=usedLen[k]=1; nSkelLeft--; if(stage1(k-1)) return true; nSkelLeft++; usedLab[x]=usedLen[k]=0; lab[v]=0; }
    if(found) return true; if(triesDone>=cap) return false; }
  return false; }
int szv[130]; int dfsSize(int v,int p){ cpar[v]=p; szv[v]=1; for(int u:adj[v]) if(u!=p) szv[v]+=dfsSize(u,v); return szv[v]; }
int main(int argc,char**argv){ tries=argc>1?atoll(argv[1]):100000; s2limit=argc>2?atoll(argv[2]):3000; bool SHOW=getenv("SHOW"); string line; long long tot=0,nf=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n; for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u); }
    vector<int> deg(n), layer; vector<char> gone(n,0); int rem=n; for(int i=0;i<n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
    while(rem>2){ vector<int> nx; for(int x:layer){ gone[x]=1; rem--; for(int y:adj[x]) if(!gone[y] && --deg[y]==1) nx.push_back(y);} layer=nx; }
    int ctr=layer[0]; cpar.assign(n,-1); dfsSize(ctr,-1); memset(inBranch,0,sizeof inBranch); memset(quota,0,sizeof quota); memset(capTot,0,sizeof capTot); branches.clear();
    for(int w=0;w<n;w++) if(w!=ctr && szv[w]<=3 && szv[cpar[w]]>3){ Br b; b.v=cpar[w]; vector<int> ch; for(int y:adj[w]) if(y!=cpar[w]) ch.push_back(y);
      if(szv[w]==1){ b.type=0; b.verts={w}; } else if(szv[w]==2){ b.type=1; b.verts={w,ch[0]}; } else if(ch.size()==1){ int z=-1; for(int y:adj[ch[0]]) if(y!=w) z=y; b.type=2; b.verts={w,ch[0],z}; } else { b.type=3; b.verts={w,ch[0],ch[1]}; }
      for(int y:b.verts) inBranch[y]=1; quota[b.v][b.type]++; capTot[b.v]+=b.verts.size(); branches.push_back(b); }
    needBr=branches.size(); vector<int> skel; for(int i=0;i<n;i++) if(!inBranch[i]) skel.push_back(i);
    found=false; triesDone=0; tot++; int rounds=100;
    for(int rd=0;rd<rounds && !found;rd++){ int r=skel[rng()%skel.size()];
      order_.clear(); parentOf.assign(n,-1); order_.push_back(r); for(size_t i=0;i<order_.size();i++){ int a=order_[i]; for(int w:adj[a]) if(!inBranch[w] && w!=parentOf[a]){ parentOf[w]=a; order_.push_back(w); } }
      memset(usedLab,0,sizeof usedLab); memset(usedLen,0,sizeof usedLen); memset(lab,0,sizeof lab); lab[r]=1; dpar[r]=n; usedLab[1]=1; cap=triesDone+max(1LL,tries/rounds); nSkelLeft=order_.size()-1; deferred.clear(); nodes1=0; stage1(n-1); }
    if(found){ if(!verifyAndStore()){ printf("VERIFY-FAILED %s\n",line.c_str()); return 1; } nf++; printf("FOUND n=%d tries=%lld",n,triesDone); if(SHOW){ printf(" :: %s |",line.c_str()); for(int i=0;i<n;i++) printf(" %d",finalLab[i]); } printf("\n"); }
    else printf("UNRESOLVED: %s\n",line.c_str());
    fflush(stdout); }
  printf("trees=%lld found=%lld\n",tot,nf); }
