// Growth placements for trees with many leaves ("hub" trees), two-stage search.
// Stage 1 (skeleton): the non-leaf vertices get labels, parent before child from a root labelled 1, edge length
//   smaller than the parent's edge length (heap form, README Theorem 7), all labels/lengths distinct.
// Stage 2 (leaves): an exact cover.  Items: every remaining length and every remaining label.  Option (k, v, +-):
//   a leaf of v with edge length k (k < length of v's parent edge, or v is the root) and label lab(v)+-k.
//   Each skeleton vertex v needs exactly (number of leaf neighbours) options.  Fewest-options-first search.
// Only anchors that are non-leaves are tried, so "no placement found" is NOT a proof of non-existence unless
//   EXH=1 (exhaustive ordered stage 1 and unlimited stage 2) AND the leaf anchors are covered separately.
// Every placement found is re-checked from the definition (labels 1..n once, lengths 1..n-1 once, brackets of
//   length >= k connected for every k).  Input lines "n u v u v ...".  Output FOUND/UNRESOLVED/NONE(non-leaf anchors).
// usage: hubsolve [tries=200000] [stage2 node limit=2000]      env SHOW=1 prints labels, EXH=1 exhaustive
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[130]; int lab[130], dpar[130], quota[130]; bool isLeaf[130]; bool usedLab[130], usedLen[130];
vector<int> order_, parentOf; mt19937 rng(99); bool EXH=false; long long s2limit, tries, triesDone, cap; bool found;
// stage 2
struct Opt{ int k,v,x; }; vector<Opt> opt; vector<vector<int>> byItem; vector<vector<int>> cnt; vector<char> covered, dead; int q2[130]; long long nodes2; int needLeaves;
vector<int> chosen;
bool cover(int depth){
  if(depth==needLeaves) return true; if(s2limit && ++nodes2>s2limit) return false;
  int NI=byItem.size(); int best=-1, bc=1<<30; for(int it=0;it<NI;it++) if(!covered[it]){ int c=0; for(int v:order_) if(q2[v]>0) c+=cnt[it][v]; if(c<bc || (c==bc && !EXH && (rng()&1))){ bc=c; best=it; } }
  if(bc==0) return false;
  vector<int> cand; for(int o:byItem[best]) if(!dead[o] && q2[opt[o].v]>0) cand.push_back(o); if(!EXH) shuffle(cand.begin(),cand.end(),rng);
  for(int o:cand){ vector<int> killed; int its[2]={opt[o].k-1, n-1+opt[o].x-1};
    for(int j=0;j<2;j++){ covered[its[j]]=1; for(int q:byItem[its[j]]) if(!dead[q]){ dead[q]=1; killed.push_back(q); cnt[opt[q].k-1][opt[q].v]--; cnt[n-1+opt[q].x-1][opt[q].v]--; } }
    q2[opt[o].v]--; chosen.push_back(o); if(cover(depth+1)) return true; chosen.pop_back(); q2[opt[o].v]++;
    for(int q:killed){ dead[q]=0; cnt[opt[q].k-1][opt[q].v]++; cnt[n-1+opt[q].x-1][opt[q].v]++; } covered[its[0]]=covered[its[1]]=0; if(s2limit && nodes2>s2limit) return false; }
  return false; }
bool stage2(){
  opt.clear(); for(int v:order_) if(quota[v]) for(int k=1;k<dpar[v];k++) if(!usedLen[k]) for(int s=-1;s<=1;s+=2){ int x=lab[v]+s*k; if(x>=1&&x<=n&&!usedLab[x]) opt.push_back({k,v,x}); }
  byItem.assign(2*n,{}); cnt.assign(2*n,vector<int>(n,0)); covered.assign(2*n,1); dead.assign(opt.size(),0);
  for(int k=1;k<n;k++) if(!usedLen[k]) covered[k-1]=0; for(int x=1;x<=n;x++) if(!usedLab[x]) covered[n-1+x-1]=0;
  for(size_t i=0;i<opt.size();i++){ byItem[opt[i].k-1].push_back(i); byItem[n-1+opt[i].x-1].push_back(i); cnt[opt[i].k-1][opt[i].v]++; cnt[n-1+opt[i].x-1][opt[i].v]++; }
  for(int v:order_) q2[v]=quota[v]; nodes2=0; chosen.clear(); return cover(0); }
int leafLab[130]; vector<pair<int,int>> edgesAll;
bool verifyAndStore(){ // assign leaves from chosen
  vector<int> L(n,0); for(int v=0;v<n;v++) L[v]=isLeaf[v]?0:lab[v]; vector<vector<int>> leavesOf(n); for(int v=0;v<n;v++) if(isLeaf[v]) leavesOf[adj[v][0]].push_back(v);
  for(int o:chosen){ int v=opt[o].v; int w=leavesOf[v].back(); leavesOf[v].pop_back(); L[w]=opt[o].x; }
  vector<int> seenL(n+1,0), len(n,0); for(int i=0;i<n;i++){ if(L[i]<1||L[i]>n||seenL[L[i]]) return false; seenL[L[i]]=1; }
  vector<pair<int,pair<int,int>>> E; for(int u=0;u<n;u++) for(int w:adj[u]) if(u<w){ int d=abs(L[u]-L[w]); if(d<1||d>n-1||len[d]) return false; len[d]=1; E.push_back({d,{u,w}}); }
  if((int)E.size()!=n-1) return false; sort(E.rbegin(),E.rend()); vector<char> in(n,0); in[E[0].second.first]=in[E[0].second.second]=1;
  for(int i=1;i<n-1;i++){ int a=E[i].second.first,b=E[i].second.second; if(in[a]==in[b]) return false; in[a]=in[b]=1; }
  for(int i=0;i<n;i++) leafLab[i]=L[i]; return true; }
// Stage 1, longest length first: length k is either given to a skeleton edge (child gets lab(parent)+-k, parent's own
// edge longer) or deferred to the leaves; a deferred length must fit under some labelled vertex with spare leaves
// (greedy necessary test).  When every skeleton vertex is labelled, stage 2 places the leaves.
int nSkelLeft; vector<int> deferred;
bool hallOK(){ // deferred lengths (descending) versus labelled vertices' leaf capacities under dpar
  vector<pair<int,int>> hubs; for(int v:order_) if(lab[v] && quota[v]) hubs.push_back({dpar[v],quota[v]}); sort(hubs.rbegin(),hubs.rend());
  size_t hi=0; int capLeft=0; multiset<int> dummy; long long avail=0; size_t j=0; vector<int> ds=deferred; // ds is already descending
  // process lengths from smallest to largest: a length k can use any hub with dpar>k; count hubs capacity with dpar>k minus lengths >= k
  long long cum=0; for(size_t i=0;i<ds.size();i++){ int k=ds[i]; while(j<hubs.size() && hubs[j].first>k){ cum+=hubs[j].second; j++; } /* hubs sorted desc: all with dpar>k for current (largest-first) k */
    if((long long)(i+1)>cum) return false; } (void)hi;(void)capLeft;(void)avail; return true; }
bool stage1(int k){
  if(found) return true;
  if(nSkelLeft==0){ triesDone++; if(stage2()){ found=true; return true; } return false; }
  if(k==0) return false;
  if(!EXH && triesDone>=cap) return false;
  if(!EXH && ++nodes2>20000000) { triesDone=cap; return false; }
  vector<pair<int,int>> cand;   // (vertex, label); (-1,0) = defer
  for(int v:order_) if(!lab[v]){ int p=parentOf[v]; if(!lab[p] || dpar[p]<=k) continue; for(int sg=-1;sg<=1;sg+=2){ int x=lab[p]+sg*k; if(x>=1&&x<=n&&!usedLab[x]) cand.push_back({v,x}); } }
  cand.push_back({-1,0}); if(!EXH) shuffle(cand.begin(),cand.end(),rng);
  for(auto c:cand){
    if(c.first<0){ deferred.push_back(k); bool ok=hallOK(); if(ok && stage1(k-1)) return true; deferred.pop_back(); }
    else { int v=c.first,x=c.second; lab[v]=x; dpar[v]=k; usedLab[x]=usedLen[k]=1; nSkelLeft--; if(stage1(k-1)) return true; nSkelLeft++; usedLab[x]=usedLen[k]=0; lab[v]=0; }
    if(found) return true; if(!EXH && triesDone>=cap) return false; }
  return false; }
int main(int argc,char**argv){ tries=argc>1?atoll(argv[1]):200000; s2limit=argc>2?atoll(argv[2]):2000; EXH=getenv("EXH"); if(EXH) s2limit=0; bool SHOW=getenv("SHOW"); string line; long long tot=0,nf=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n; for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u); }
    for(int i=0;i<n;i++){ isLeaf[i]=adj[i].size()==1; } for(int i=0;i<n;i++){ quota[i]=0; if(!isLeaf[i]) for(int w:adj[i]) if(isLeaf[w]) quota[i]++; }
    needLeaves=0; for(int i=0;i<n;i++) if(isLeaf[i]) needLeaves++;
    vector<int> skel; for(int i=0;i<n;i++) if(!isLeaf[i]) skel.push_back(i);
    found=false; triesDone=0; tot++; int rounds = EXH?1:200;
    for(int rd=0;rd<rounds && !found && (EXH || triesDone<tries);rd++) for(size_t ri=0;ri<skel.size()&&!found;ri++){ int r = skel[EXH? ri : rng()%skel.size()];
      order_.clear(); parentOf.assign(n,-1); order_.push_back(r); for(size_t i=0;i<order_.size();i++){ int a=order_[i]; for(int w:adj[a]) if(!isLeaf[w] && w!=parentOf[a]){ parentOf[w]=a; order_.push_back(w); } }
      memset(usedLab,0,sizeof usedLab); memset(usedLen,0,sizeof usedLen); memset(lab,0,sizeof lab); lab[r]=1; dpar[r]=n; usedLab[1]=1; cap=triesDone+max(1LL,tries/rounds); nSkelLeft=order_.size()-1; deferred.clear(); nodes2=0; stage1(n-1); if(!EXH) break; }
    if(found){ if(!verifyAndStore()){ printf("VERIFY-FAILED %s\n",line.c_str()); return 1; } nf++; printf("FOUND n=%d tries=%lld",n,triesDone); if(SHOW){ printf(" | %s |",line.c_str()); for(int i=0;i<n;i++) printf(" %d",leafLab[i]); } printf("\n"); }
    else printf("%s: %s\n",EXH?"NONE(non-leaf anchors)":"UNRESOLVED",line.c_str());
    fflush(stdout); }
  printf("trees=%lld found=%lld\n",tot,nf); }
