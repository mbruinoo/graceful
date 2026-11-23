// Zigzag deal of the spider S(2^k) as an exact cover (centre label 0, labels 0..2k):
// items len_y, lab_y (y=1..2k); option (a,b), 1<=b<a<=2k: a leg with inner label a (inner length a), outer length b,
// outer label a-b; it covers len_a, lab_a, len_b, lab_{a-b}.  k options must cover all 4k items.
// Search: choose the item with fewest live options (ties random), options in random order, restarts.
// Result re-checked from the definition and printed as "a:o" pairs.
#include <bits/stdc++.h>
using namespace std;
int k,N; vector<array<int,4>> opt; vector<vector<int>> byItem; vector<int> cntLive; vector<char> covered, dead; vector<int> deadBy;
long long nodes, lim; mt19937 rng(11); vector<int> chosen;
bool dfs(int depth){
  if(depth==k) return true; if(++nodes>lim) return false;
  int best=-1, bc=1<<30; for(int it=0;it<2*N;it++) if(!covered[it]){ int c=cntLive[it]; if(c<bc || (c==bc && (rng()&1))){ bc=c; best=it; } }
  if(bc==0) return false;
  vector<int> cand; for(int o:byItem[best]) if(!dead[o]) cand.push_back(o); shuffle(cand.begin(),cand.end(),rng);
  for(int o:cand){ vector<int> killed; for(int j=0;j<4;j++){ int it=opt[o][j]; covered[it]=1; for(int q:byItem[it]) if(!dead[q]){ dead[q]=1; killed.push_back(q); for(int t=0;t<4;t++) cntLive[opt[q][t]]--; } }
    chosen.push_back(o); if(dfs(depth+1)) return true; chosen.pop_back();
    for(int q:killed){ dead[q]=0; for(int t=0;t<4;t++) cntLive[opt[q][t]]++; } for(int j=0;j<4;j++) covered[opt[o][j]]=0; if(nodes>lim) return false; }
  return false; }
int main(int c,char**v){ for(int ai=1;ai<c;ai++){ k=atoi(v[ai]); N=2*k; opt.clear(); byItem.assign(2*N,{});
  for(int a=2;a<=N;a++) for(int b=1;b<a;b++){ int o=a-b; if(o==a) continue; /* items: len y -> y-1, lab y -> N+y-1 */ if(b==a) continue; opt.push_back({a-1,b-1,N+a-1,N+o-1}); }
  for(size_t i=0;i<opt.size();i++) for(int j=0;j<4;j++) byItem[opt[i][j]].push_back(i);
  bool ok=false; lim=20000; for(int r=0;r<1000000&&!ok;r++){ covered.assign(2*N,0); dead.assign(opt.size(),0); cntLive.assign(2*N,0); for(int it=0;it<2*N;it++) cntLive[it]=byItem[it].size(); chosen.clear(); nodes=0; ok=dfs(0); if(r%10==9 && lim<20000000) lim*=2; if(k*(2*k+1)%3) break; }
  if(!ok){ printf("k=%d none-or-unresolved\n",k); continue; }
  vector<int> L(N+1,0), D(N+1,0); bool good=true; for(int o:chosen){ int a=opt[o][0]+1,b=opt[o][1]+1,out=a-b; if(L[a]++||L[out]++||D[a]++||D[b]++||b>=a) good=false; }
  for(int y=1;y<=N;y++) if(L[y]!=1||D[y]!=1) good=false;
  printf("k=%d n=%d %s legs:",k,N+1,good?"OK":"CHECK-FAILED"); for(int o:chosen) printf(" %d:%d",opt[o][0]+1,opt[o][0]-opt[o][1]); printf("\n"); fflush(stdout); } }
