// Machine check of the clean-leaf persistence lemma and the unique-core theorem, from the definitions.
// For every growth placement p on n<=N vertices:
//  (A) for every ordered pair of distinct clean leaves (l1,l2): after deleting l1 and closing the gap, l2 is still a clean leaf.
//  (B) the terminal placement of clean-leaf peeling (stop when no clean leaf, or at n=2) is the same whatever order is used.
//  (C) Lemma-8 form of clean leaf (crossing brackets = the longer ones) agrees with "deleting the label and closing the gap
//      gives a growth placement" (restriction checked by definition).
// Also prints the number of primitive placements (no clean leaf), and the distribution of core sizes.
#include "enum.h"
static bool restrict1(const Pl&p,int L,Pl&q){ int n=p.n; q.n=n-1; if(q.n<2) return false; bool have[20]={0}; int cnt=0;
  for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if(a==L||b==L) continue; int a2=a-(a>L), b2=b-(b>L); int len=b2-a2; if(have[len]) return false; have[len]=1; q.pos[len]=a2; cnt++; }
  return cnt==q.n-1 && isGrowth(q); }
// clean leaf by the README definition: label L is a leaf, hung by a bracket of length j, and the other brackets jumping over L are exactly those longer than j
static bool cleanLeafDef(const Pl&p,int L){ int n=p.n, deg=0, j=0; for(int k=1;k<n;k++) if(p.pos[k]==L||p.pos[k]+k==L){ deg++; j=k; } if(deg!=1) return false;
  for(int k=1;k<n;k++){ if(k==j) continue; bool cr=p.pos[k]<L && L<p.pos[k]+k; if(cr!=(k>j)) return false; } return true; }
int main(int argc,char**argv){ int N=atoi(argv[1]);
  vector<unordered_map<u64,u64>> core(N+1); vector<unordered_map<u64,int>> coren(N+1);   // core placement (encoded) and its size
  long badA=0,badB=0,badC=0;
  for(int n=2;n<=N;n++){ long total=0, prim=0, pairs=0; map<int,long> dist; map<int,set<string>> mincoreT; map<string,int> treeMin;
    enumGrowth(n,[&](const Pl&p){ total++; u64 e=enc(p); Pl q,q2;
      if(n==2){ core[n][e]=e; coren[n][e]=2; dist[2]++; treeMin[canon(p)]=2; return; }
      vector<int> cl; for(int L=1;L<=n;L++){ bool a=cleanLeafDef(p,L), b=restrict1(p,L,q); if(a!=b) badC++; if(a) cl.push_back(L); }
      if(cl.empty()){ prim++; core[n][e]=e; coren[n][e]=n; }
      else { bool first=true; u64 c0=0; int cn=0;
        for(int L:cl){ restrict1(p,L,q); u64 c=core[n-1][enc(q)]; int m=coren[n-1][enc(q)]; if(first){ c0=c; cn=m; first=false; } else if(c!=c0||m!=cn) badB++;
          for(int L2:cl) if(L2!=L && n>=4){ pairs++; int L2n=L2-(L2>L); if(!cleanLeafDef(q,L2n)) badA++; } }
        core[n][e]=c0; coren[n][e]=cn; }
      int cn=coren[n][e]; dist[cn]++; string t=canon(p); auto it=treeMin.find(t); if(it==treeMin.end()||it->second>cn) treeMin[t]=cn; });
    printf("n=%d growth=%ld primitive=%ld pairs_checked=%ld | core size: placements",n,total,prim,pairs); for(auto&d:dist) printf(" %d:%ld",d.first,d.second);
    map<int,int> tm; for(auto&t:treeMin) tm[t.second]++; printf(" | trees by least core size:"); for(auto&d:tm) printf(" %d:%d",d.first,d.second);
    printf(" | violations A=%ld B=%ld C=%ld\n",badA,badB,badC); fflush(stdout); }
}
