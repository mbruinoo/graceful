// Candidate induction hypotheses P for clean-leaf insertion (README Lemma 8), tested on ALL growth placements, n<=N.
// For each P:  exist(n) = #tree shapes with some P-placement;   chain(n) = #tree shapes with a placement p such that p has P and
// (n<=3 or some clean leaf of p can be deleted leaving a placement with the same chain property)  [closure of P under the move].
//   P0: no condition (chain = peelable, class K1)
//   P1: every leaf of the tree is clean in p
//   P2: at least two clean leaves
//   P3: every vertex of degree>=3 has a clean cut next to its label (cut l-1 or cut l; the two end cuts count)
//   P4: at least 3 clean interior cuts with pairwise distinct heights
//   P5: at least half of the interior cuts are clean
// Also: tree-level step statistics.  A pair (T'', T') with T'' = T' minus a leaf is "realised" in a class if some placement of T'
// in the class has a clean leaf whose deletion gives a placement of T'' in the class.
// Usage: props N
#include "enum.h"
static bool restrict1(const Pl&p,int L,Pl&q){ int n=p.n; q.n=n-1; if(q.n<2) return false; bool have[20]={0}; int cnt=0;
  for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if(a==L||b==L) continue; int a2=a-(a>L), b2=b-(b>L); int len=b2-a2; if(have[len]) return false; have[len]=1; q.pos[len]=a2; cnt++; }
  return cnt==q.n-1 && isGrowth(q); }
static bool restrict2clean(const Pl&p,int x,int y,Pl&q){ int n=p.n; q.n=n-2; if(q.n<2) return false; int cnt=0,last=0;
  for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if(a==x||b==x||a==y||b==y) continue; int a2=a-(a>x)-(a>y), b2=b-(b>x)-(b>y); int len=b2-a2; if(len<=last) return false; last=len; q.pos[len]=a2; cnt++; }
  return cnt==q.n-1 && isGrowth(q); }
const int NP=6;
int main(int argc,char**argv){ int N=atoi(argv[1]);
  vector<unordered_map<u64,unsigned>> fl(N+1);   // bits 0..NP-1: chain property for P_i ; bit 8: class C2 (clean steps of size<=2)
  for(int n=2;n<=N;n++){ vector<set<string>> ex(NP), ch(NP); set<string> allT, c2T; map<string,Pl> rep;
    set<pair<string,string>> prAll, prK1, prC2; long nP[NP]={0};
    enumGrowth(n,[&](const Pl&p){ string t=canon(p); allT.insert(t); if(!rep.count(t)) rep[t]=p; Pl q;
      int deg[20]={0}; for(int k=1;k<n;k++){ deg[p.pos[k]]++; deg[p.pos[k]+k]++; }
      int h[20]; for(int i=0;i<=n;i++) h[i]=cutHeight(p,i);
      vector<int> cl; int nleaf=0; for(int L=1;L<=n;L++){ if(deg[L]==1) nleaf++; if(restrict1(p,L,q)) cl.push_back(L); }
      bool P[NP]; P[0]=true; P[1]=((int)cl.size()==nleaf); P[2]=cl.size()>=2;
      P[3]=true; for(int L=1;L<=n;L++) if(deg[L]>=3 && h[L-1]<0 && h[L]<0) P[3]=false;
      { set<int> hs; int nc=0; for(int i=1;i<n;i++) if(h[i]>=0){ hs.insert(h[i]); nc++; } P[4]=hs.size()>=3||n<=4; P[5]=2*nc>=n-1; }
      unsigned f=0; 
      if(n<=3){ f=(1u<<NP)-1; f|=256; }
      else { unsigned got=0; for(int L:cl){ restrict1(p,L,q); got|=fl[n-1][enc(q)]; }
        for(int i=0;i<NP;i++) if(P[i] && (got>>i&1)) f|=1u<<i;
        bool c2=got>>8&1; if(!c2) for(int x=1;x<=n&&!c2;x++) for(int y=x+1;y<=n&&!c2;y++) if(restrict2clean(p,x,y,q) && (fl[n-2][enc(q)]>>8&1)) c2=true;
        if(c2) f|=256; }
      fl[n][enc(p)]=f;
      for(int i=0;i<NP;i++){ if(P[i]){ ex[i].insert(t); nP[i]++; } if(f>>i&1) ch[i].insert(t); }
      if(f>>8&1) c2T.insert(t);
      if(n>=3) for(int L:cl){ restrict1(p,L,q); string s=canon(q); unsigned g=fl[n-1][enc(q)]; prAll.insert({s,t}); if((f&1)&&(g&1)) prK1.insert({s,t}); if((f>>8&1)&&(g>>8&1)) prC2.insert({s,t}); } });
    // all structural pairs (T' minus a leaf, T')
    set<pair<string,string>> prStruct;
    for(auto&kv:rep){ const Pl&p=kv.second; auto adj=adjOf(p); for(int L=1;L<=n&&n>=3;L++) if(adj[L].size()==1){ vector<vector<int>> a2(n); 
        for(int v=1;v<=n;v++) if(v!=L) for(int w:adj[v]) if(w!=L) a2[v-(v>L)].push_back(w-(w>L)); prStruct.insert({canonAdj(a2,n-1),kv.first}); } }
    printf("n=%d trees=%zu |",n,allT.size()); for(int i=0;i<NP;i++) printf(" P%d: pl=%ld exist=%zu chain=%zu |",i,nP[i],ex[i].size(),ch[i].size());
    printf(" C2 trees=%zu | (tree minus leaf, tree) pairs: all=%zu, by a clean leaf in some growth pl=%zu, inside K1=%zu, inside C2=%zu\n",c2T.size(),prStruct.size(),prAll.size(),prK1.size(),prC2.size());
    fflush(stdout); }
}
