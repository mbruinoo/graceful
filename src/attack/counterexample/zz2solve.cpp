// Zigzag deal for the spider with k legs of length 2 (centre at label 0, labels 0..2k):
// hand out lengths x = 2k..1; x either opens a leg (inner label x) or closes an open leg a>x (outer label a-x).
// Randomised DFS with restarts.  Prints the legs as "a:o" (inner label, outer label) and re-checks from the definition.
#include <bits/stdc++.h>
using namespace std;
int k,N; bool usedLab[512]; int openLegs[512], nopen; vector<pair<int,int>> legs; long long nodes,lim; mt19937 rng(7);
bool dfs(int x,int toOpen){
  if(x==0) return nopen==0 && toOpen==0;
  if(++nodes>lim) return false;
  if(nopen>x) return false;                        // not enough lengths left to close the open legs
  // candidates: close leg i, or open
  int cand[512], c=0;
  for(int i=0;i<nopen;i++){ int o=openLegs[i]-x; if(o>=1 && !usedLab[o]) cand[c++]=i; }
  shuffle(cand,cand+c,rng);
  bool canOpen = toOpen>0 && !usedLab[x];
  int openPos = canOpen ? (int)(rng()%(c+1)) : -1;
  for(int j=0;j<=c;j++){
    if(j==openPos){ usedLab[x]=1; openLegs[nopen++]=x; if(dfs(x-1,toOpen-1)) return true; nopen--; usedLab[x]=0; }
    if(j<c){ int i=cand[j]; int a=openLegs[i], o=a-x; usedLab[o]=1; openLegs[i]=openLegs[--nopen]; legs.push_back({a,o});
      if(dfs(x-1,toOpen)) return true; legs.pop_back(); openLegs[nopen++]=openLegs[i]; openLegs[i]=a; usedLab[o]=0; }
  }
  return false; }
int main(int c,char**v){ for(int a=1;a<c;a++){ k=atoi(v[a]); N=2*k; bool ok=false; lim=20000;
  for(int r=0;r<200000&&!ok;r++){ memset(usedLab,0,sizeof usedLab); nopen=0; legs.clear(); nodes=0; ok=dfs(N,k); if(r%20==19 && lim<5000000) lim*=2; }
  if(!ok){ printf("k=%d unresolved\n",k); continue; }
  // check from the definition: labels 0..N once each, lengths 1..N once each, lengths decrease outward (a > |a-o|)
  vector<int> L(N+1,0), D(N+1,0); L[0]=1; bool good=legs.size()==(size_t)k;
  for(auto&p:legs){ int a=p.first,o=p.second; if(a<1||a>N||o<1||o>N||L[a]++||L[o]++) good=false; if(D[a]++) good=false; int d=abs(a-o); if(d<1||d>=a||D[d]++) good=false; }
  printf("k=%d n=%d %s legs:",k,N+1,good?"OK":"CHECK-FAILED"); for(auto&p:legs) printf(" %d:%d",p.first,p.second); printf("\n"); fflush(stdout); } }
