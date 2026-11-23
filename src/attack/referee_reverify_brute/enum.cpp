// Referee brute force: enumerate ALL growth placements on labels 1..n (README sec 2 definition:
// brackets longest first, each has exactly one foot on a used label), optionally restricted by
// a rule on the set of unused labels after every bracket (README sec 11).
// usage: enum n R H SIDE [dumpfile] [anchors]
//   R    : max number of runs of unused labels (0 = no limit)
//   H    : -1 off; else: unused = one main run + at most H isolated single cells
//   SIDE : 0 none; 1 = all singles on the same side of the main run; 2 = at most one single on each side
//          (1,2: "exists a choice of main run"); 3 = like 2 but main run := first run of maximal size
// prints: number of placements, number of distinct shapes. dumpfile: shape codes (hex), one per line.
// anchors=1: also the anchor table (vertex v is an anchor if some growth placement gives it label 1).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned int u32;
int n,R,H,SIDE,ANCH=0;
int adjn[40], adj[40][40];
u64 nplace=0;
unordered_set<u64> shapes, rooted1;
// rooted canonical code: '1' + children codes sorted descending + '0'; returns code, sets len
u64 rcode(int v,int par,int &len){
  u64 c[40]; int l[40]; int m=0;
  for(int i=0;i<adjn[v];i++){int w=adj[v][i]; if(w==par)continue; c[m]=rcode(w,v,l[m]); m++;}
  // sort descending by (code aligned) : compare as strings -> compare (len desc?) use numeric of left-aligned
  for(int i=1;i<m;i++){u64 ci=c[i];int li=l[i];int j=i-1;
    while(j>=0 && ( (c[j]<<(62-l[j])) < (ci<<(62-li)) )){c[j+1]=c[j];l[j+1]=l[j];j--;}
    c[j+1]=ci;l[j+1]=li;}
  u64 r=1; int L=1;
  for(int i=0;i<m;i++){r=(r<<l[i])|c[i];L+=l[i];}
  r<<=1;L++; len=L; return r;
}
u64 ucode(){
  // centres by leaf stripping
  int deg[40],q[40],qh=0,qt=0,rem=n,layer[40];
  for(int v=1;v<=n;v++){deg[v]=adjn[v]; layer[v]=0; if(deg[v]<=1){q[qt++]=v;}}
  int last=0;
  while(qh<qt){int v=q[qh++]; last=layer[v];
    for(int i=0;i<adjn[v];i++){int w=adj[v][i]; if(--deg[w]==1){layer[w]=layer[v]+1;q[qt++]=w;}}}
  // centres: vertices with maximal layer
  int c1=q[qt-1],c2=-1; if(qt>=2 && layer[q[qt-2]]==layer[c1]) c2=q[qt-2];
  (void)rem;(void)last;
  int len; u64 a=rcode(c1,0,len);
  if(c2>0){u64 b=rcode(c2,0,len); if(b<a)a=b;}
  return a;
}
inline bool okstate(u32 u){
  if(!u) return true;
  u32 starts=u&~(u<<1); int runs=__builtin_popcount(starts);
  if(R && runs>R) return false;
  if(H<0) return true;
  u32 singles=starts&~(u>>1); int ns=__builtin_popcount(singles); int big=runs-ns;
  if(big>1) return false;
  if(runs-1>H) return false;
  if(SIDE==0) return true;
  // list runs in order: 1 if big, 0 if single
  int kind[8],m=0; u32 s=starts; while(s){int b=__builtin_ctz(s); s&=s-1; kind[m++]=((singles>>b)&1)?0:1;}
  if(SIDE==3){ int mi=0; for(int i=0;i<m;i++) if(kind[i]){mi=i;break;} // first run of maximal size
    return mi<=1 && (m-1-mi)<=1; }
  for(int mi=0;mi<m;mi++){ if(big && !kind[mi]) continue;
    int l=mi, r=m-1-mi;
    if(SIDE==1 && (l==0||r==0)) return true;
    if(SIDE==2 && l<=1 && r<=1) return true; }
  return false;
}
void rec(int k,u32 used,u32 full){
  if(k==0){ nplace++; shapes.insert(ucode()); if(ANCH){int len; rooted1.insert(rcode(1,0,len));} return; }
  for(int p=1;p+k<=n;p++){ int a=p,b=p+k; bool ua=(used>>a)&1, ub=(used>>b)&1;
    if(ua==ub) continue;
    u32 nu=used|(1u<<a)|(1u<<b);
    if(!okstate(full&~nu)) continue;
    adj[a][adjn[a]++]=b; adj[b][adjn[b]++]=a;
    rec(k-1,nu,full);
    adjn[a]--; adjn[b]--; }
}
// decode rooted code into adjacency (labels 1..n) for the anchor table
void decode(u64 code,int len){
  for(int v=1;v<=n;v++)adjn[v]=0; int st[40],sp=0,cnt=0;
  for(int i=len-1;i>=0;i--){ if((code>>i)&1){int v=++cnt; if(sp){int p=st[sp-1]; adj[p][adjn[p]++]=v; adj[v][adjn[v]++]=p;} st[sp++]=v;} else sp--; }
}
int main(int argc,char**argv){
  n=atoi(argv[1]);R=atoi(argv[2]);H=atoi(argv[3]);SIDE=atoi(argv[4]);
  const char*dump=argc>5?argv[5]:"-"; if(argc>6)ANCH=atoi(argv[6]);
  u32 full=0; for(int i=1;i<=n;i++)full|=1u<<i;
  if(n==1){printf("n=1 trivial\n");return 0;}
  adj[1][adjn[1]++]=n; adj[n][adjn[n]++]=1;
  u32 used=(1u<<1)|(1u<<n);
  if(okstate(full&~used)) rec(n-2,used,full);
  printf("n=%d R=%d H=%d SIDE=%d placements=%llu shapes=%zu\n",n,R,H,SIDE,nplace,shapes.size());
  if(strcmp(dump,"-")){FILE*f=fopen(dump,"w"); vector<u64> v(shapes.begin(),shapes.end()); sort(v.begin(),v.end()); for(u64 c:v)fprintf(f,"%llx\n",c); fclose(f);}
  if(ANCH){
    long verts=0,non=0,allanch=0,noanchor=0,noanchorleaf=0; int maxdegnon=0; 
    vector<u64> v(shapes.begin(),shapes.end()); sort(v.begin(),v.end());
    for(u64 c:v){ decode(c,2*n); int bad=0; bool anyleaf=false,any=false;
      for(int x=1;x<=n;x++){int len; u64 rc=rcode(x,0,len); verts++;
        if(rooted1.count(rc)){any=true; if(adjn[x]==1)anyleaf=true;} else {non++;bad++; maxdegnon=max(maxdegnon,adjn[x]);
          if(n<=8||ANCH>1){printf("  non-anchor: tree %llx vertex deg %d rootedcode %llx\n",c,adjn[x],rc);} } }
      if(!bad)allanch++; if(!any)noanchor++; if(!anyleaf){noanchorleaf++; printf("  tree with no anchor leaf: %llx\n",c);} }
    printf("anchors n=%d: vertices=%ld nonanchors=%ld trees_all_anchor=%ld of %zu; trees_with_no_anchor=%ld; trees_with_no_anchor_leaf=%ld; max degree of a non-anchor=%d\n",n,verts,non,allanch,v.size(),noanchor,noanchorleaf,maxdegnon);
  }
}
