// ANCHOR-LEVEL COMPOSITION RULES THAT FAIL.  Enumerates every growth placement on n <= N vertices (default 14) from the
// definition, records which rooted trees (T,v) have v as an anchor (v can carry label 0), and then tests, for all pairs
// of anchored trees (T,v), (T',v') with at most S vertices each (default 7):
//   F1  identify v with v'         : is the merged vertex an anchor of the union?
//   F2  join v to v' by an edge    : is v an anchor of the result?  is at least one of v, v' an anchor?
// Prints counts and the smallest failing pairs.      Usage: anchortest [N=14] [S=7]
#include "common.h"
int N=14,S=7; unordered_set<uint32_t> anchor[16]; long long cnt[16];
static void rec(int k,int m,unsigned used,int*pos){ if(k==0){ cnt[m+1]++; anchor[m+1].insert(rooted_pos(pos,m,0)); anchor[m+1].insert(rooted_pos(pos,m,m)); return; }
  for(int a=0;a+k<=m;a++){ bool x=used>>a&1,y=used>>(a+k)&1; if(x==y) continue; pos[k]=a; rec(k-1,m,used|(1u<<a)|(1u<<(a+k)),pos); } }
static uint32_t merge_code(uint32_t c1,int n1,uint32_t c2,int n2,bool edge){ int p1[16],p2[16]; decode(c1,n1,p1); decode(c2,n2,p2); vector<int> adj[32];
  for(int i=1;i<n1;i++){ adj[i].push_back(p1[i]); adj[p1[i]].push_back(i); }
  if(edge){ for(int i=1;i<n2;i++){ adj[n1+i].push_back(n1+p2[i]); adj[n1+p2[i]].push_back(n1+i); } adj[0].push_back(n1); adj[n1].push_back(0); }
  else { for(int i=1;i<n2;i++){ int a=n1+i-1,b= p2[i]==0?0:n1+p2[i]-1; adj[a].push_back(b); adj[b].push_back(a); } }
  return rcode(0,-1,adj).bits; }
int main(int argc,char**argv){ if(argc>1) N=atoi(argv[1]); if(argc>2) S=atoi(argv[2]);
  anchor[1].insert(2); cnt[1]=1;
  for(int n=2;n<=N;n++){ int pos[16]; int m=n-1; pos[m]=0; rec(m-1,m,1u|(1u<<m),pos); printf("n=%d growth placements=%lld anchored rooted trees=%zu\n",n,cnt[n],anchor[n].size()); fflush(stdout); }
  // F1 / F2
  long long pairs1=0,fail1=0,pairs2=0,fail2v=0,fail2both=0; string first1="",first2="",first2b=""; int best1=99,best2=99,best2b=99;
  for(int n1=1;n1<=S;n1++) for(int n2=1;n2<=n1;n2++) for(uint32_t a:anchor[n1]) for(uint32_t b:anchor[n2]){ if(n1==n2 && b>a) continue;
    if(n1+n2-1<=N && n1>1 && n2>1){ pairs1++; uint32_t c=merge_code(a,n1,b,n2,false); if(!anchor[n1+n2-1].count(c)){ fail1++; if(n1+n2-1<best1){ best1=n1+n2-1; first1=paren(a,n1)+" + "+paren(b,n2); } } }
    if(n1+n2<=N){ pairs2++; uint32_t c=merge_code(a,n1,b,n2,true), d=merge_code(b,n2,a,n1,true); bool x=anchor[n1+n2].count(c),y=anchor[n1+n2].count(d);
      if(!x||!y){ fail2v++; if(n1+n2<best2){ best2=n1+n2; first2=paren(a,n1)+" -- "+paren(b,n2)+(x?"  (second root is not an anchor)":"  (first root is not an anchor)"); } }
      if(!x&&!y){ fail2both++; if(n1+n2<best2b){ best2b=n1+n2; first2b=paren(a,n1)+" -- "+paren(b,n2); } } } }
  printf("F1 identify two anchors (each tree 2..%d vertices): %lld unordered pairs, merged vertex NOT an anchor in %lld; smallest: %s (n=%d)\n",S,pairs1,fail1,first1.c_str(),best1);
  printf("F2 join two anchors by an edge (each tree 1..%d vertices): %lld unordered pairs; some end of the new edge is not an anchor in %lld; smallest: %s (n=%d)\n",S,pairs2,fail2v,first2.c_str(),best2);
  printf("F2' neither end of the new edge is an anchor in %lld; smallest: %s (n=%d)\n",fail2both,first2b.c_str(),best2b);
  printf("(rooted trees are written as nested parentheses, root = outermost pair)\n");
}
