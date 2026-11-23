// Referee tree-by-tree solver. Own tree generator (Beyer-Hedetniemi level sequences of rooted trees,
// keep those rooted at a unique centroid; bicentroid trees = unordered pairs of rooted trees of size n/2),
// counts asserted against A000081/A000055. For each tree an exhaustive DFS for a growth placement
// (README sec 2) obeying the rule (same okstate() semantics as enum.cpp). Every solution found is
// re-verified by verify() straight from the definitions.
// usage: solve n R H SIDE part parts [nodelimit]     or   solve file <treefile> R H SIDE
//   treefile lines: n u1 v1 u2 v2 ...   (0-based vertices)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned int u32;
int n,R,H,SIDE;
static const u64 A55[]={0,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320,48629,123867,317955,823065,2144505,5623756,14828074};
static const u64 A81[]={0,1,1,2,4,9,20,48,115,286,719,1842,4766,12486,32973,87811,235381,634847,1721159,4688676,12826228,35221832,97055181};
inline bool okstate(u32 u){
  if(!u) return true;
  u32 starts=u&~(u<<1); int runs=__builtin_popcount(starts);
  if(R && runs>R) return false;
  if(H<0) return true;
  u32 singles=starts&~(u>>1); int ns=__builtin_popcount(singles); int big=runs-ns;
  if(big>1) return false;
  if(runs-1>H) return false;
  if(SIDE==0) return true;
  int kind[8],m=0; u32 s=starts; while(s){int b=__builtin_ctz(s); s&=s-1; kind[m++]=((singles>>b)&1)?0:1;}
  if(SIDE==3){ int mi=0; for(int i=0;i<m;i++) if(kind[i]){mi=i;break;} return mi<=1 && (m-1-mi)<=1; }
  for(int mi=0;mi<m;mi++){ if(big && !kind[mi]) continue; int l=mi,r=m-1-mi;
    if(SIDE==1 && (l==0||r==0)) return true; if(SIDE==2 && l<=1 && r<=1) return true; }
  return false;
}
// ---- tree
int deg[32], nb[32][32]; u64 dc[32][32]; // dc[v][i] = code of subtree hanging at nb[v][i] away from v
u64 rcode(int v,int par,int &len){
  u64 c[32]; int l[32]; int m=0;
  for(int i=0;i<deg[v];i++){int w=nb[v][i]; if(w==par)continue; c[m]=rcode(w,v,l[m]); m++;}
  for(int i=1;i<m;i++){u64 ci=c[i];int li=l[i];int j=i-1;
    while(j>=0 && ((c[j]<<(62-l[j]))<(ci<<(62-li)))){c[j+1]=c[j];l[j+1]=l[j];j--;} c[j+1]=ci;l[j+1]=li;}
  u64 r=1;int L=1; for(int i=0;i<m;i++){r=(r<<l[i])|c[i];L+=l[i];} r<<=1;L++; len=L; return r;
}
int lab[32], at[40], unl[32]; u64 nodes, nodelimit=0; bool aborted;
u32 FULL;
bool dfs(int k,u32 used){
  if(k==0) return true;
  if(nodelimit && nodes>nodelimit){aborted=true;return false;}
  u32 un=FULL&~used;
  for(u32 s=un;s;s&=s-1){ int x=__builtin_ctz(s);
    u32 nu=used|(1u<<x);
    bool checked=false, ok=false;
    for(int d=0;d<2;d++){ int y=d?x+k:x-k; if(y<1||y>n||!((used>>y)&1)) continue;
      int v=at[y]; if(!unl[v]) continue;
      if(!checked){ok=okstate(FULL&~nu);checked=true;} if(!ok) break;
      u64 tried[32]; int nt=0;
      for(int i=0;i<deg[v];i++){ int w=nb[v][i]; if(lab[w]) continue;
        bool dup=false; for(int j=0;j<nt;j++) if(tried[j]==dc[v][i]){dup=true;break;} if(dup)continue; tried[nt++]=dc[v][i];
        nodes++;
        lab[w]=x; at[x]=w; unl[v]--; for(int j=0;j<deg[w];j++) if(nb[w][j]!=v) ; unl[w]=deg[w]-1;
        if(dfs(k-1,nu)) return true;
        lab[w]=0; unl[v]++; if(aborted) return false; } } }
  return false;
}
bool verify(){ // from the definitions: labels 1..n distinct; bracket lengths n-1..1 each once; growth; rule
  u32 seen=0; for(int v=0;v<n;v++){ if(lab[v]<1||lab[v]>n||((seen>>lab[v])&1)) return false; seen|=1u<<lab[v]; }
  int a[40]={0},b[40]={0};
  for(int v=0;v<n;v++) for(int i=0;i<deg[v];i++){int w=nb[v][i]; if(v<w){int k=abs(lab[v]-lab[w]); if(k<1||k>n-1||a[k]) return false; a[k]=lab[v]; b[k]=lab[w];}}
  u32 used=0;
  for(int k=n-1;k>=1;k--){ if(!a[k]) return false; bool ua=(used>>a[k])&1, ub=(used>>b[k])&1;
    if(k==n-1){ if(ua||ub) return false; } else if(ua==ub) return false;
    used|=(1u<<a[k])|(1u<<b[k]); if(!okstate(FULL&~used)) return false; }
  return true;
}
int solve_tree(){ // 1 found, 0 none (exhaustive), -1 aborted
  for(int v=0;v<n;v++) for(int i=0;i<deg[v];i++){int len; dc[v][i]=rcode(nb[v][i],v,len);}
  FULL=0; for(int i=1;i<=n;i++) FULL|=1u<<i;
  u32 used=(1u<<1)|(1u<<n); if(!okstate(FULL&~used)) return 0;
  vector<pair<u64,u64>> seen; nodes=0; aborted=false;
  for(int u=0;u<n;u++) for(int i=0;i<deg[u];i++){ int v=nb[u][i];
    u64 c1=dc[u][i], c2=0; for(int j=0;j<deg[v];j++) if(nb[v][j]==u) c2=dc[v][j];
    pair<u64,u64> key(c2,c1); // (side of u, side of v): u gets label 1
    if(find(seen.begin(),seen.end(),key)!=seen.end()) continue; seen.push_back(key);
    for(int w=0;w<n;w++){lab[w]=0;unl[w]=deg[w];}
    lab[u]=1;at[1]=u;lab[v]=n;at[n]=v;unl[u]--;unl[v]--;
    if(dfs(n-2,used)){ if(!verify()){fprintf(stderr,"VERIFY FAILED\n");exit(3);} return 1; }
    if(aborted) return -1; }
  return 0;
}
void print_tree(const char*tag){ printf("%s %d",tag,n); for(int v=0;v<n;v++)for(int i=0;i<deg[v];i++)if(v<nb[v][i])printf(" %d %d",v,nb[v][i]); printf("\n"); fflush(stdout);}
u64 total=0,found=0,none=0,ab=0,idx=0; int part=0,parts=1; u64 maxnodes=0;
void handle(){ u64 my=idx++; total++; if((int)(my%parts)!=part) return;
  int r=solve_tree(); if(nodes>maxnodes)maxnodes=nodes;
  if(r==1)found++; else if(r==0){none++; print_tree("NONE");} else {ab++; print_tree("ABORT");} }
void from_levels(const int*L,int m,int off,int*par){ // level sequence -> parents (vertex ids off..off+m-1)
  int st[40]; for(int i=0;i<m;i++){ st[L[i]]=i; par[off+i]= (L[i]==1)?-1:off+st[L[i]-1]; } }
void set_tree(const int*par){ for(int v=0;v<n;v++)deg[v]=0; for(int v=0;v<n;v++) if(par[v]>=0){int p=par[v]; nb[p][deg[p]++]=v; nb[v][deg[v]++]=p;} }
template<class F> u64 gen_rooted(int m,F f){ // Beyer-Hedetniemi
  int L[40]; for(int i=0;i<m;i++)L[i]=i+1; u64 c=0;
  while(true){ f(L); c++; int p=m-1; while(p>=0&&L[p]<=2)p--; if(p<1)break;   // p<1: star reached (or m<=2)
    int q=p-1; while(L[q]!=L[p]-1)q--; for(int i=p;i<m;i++)L[i]=L[i-(p-q)]; }
  return c; }
int main(int argc,char**argv){
  if(!strcmp(argv[1],"file")){ R=atoi(argv[3]);H=atoi(argv[4]);SIDE=atoi(argv[5]);
    FILE*f=fopen(argv[2],"r"); char line[4096];
    while(fgets(line,sizeof line,f)){ istringstream is(line); if(!(is>>n))continue; for(int v=0;v<n;v++)deg[v]=0; int a,b; while(is>>a>>b){nb[a][deg[a]++]=b;nb[b][deg[b]++]=a;}
      int r=solve_tree(); printf("R=%d H=%d SIDE=%d n=%d result=%s nodes=%llu",R,H,SIDE,n,r==1?"FOUND":"NONE(exhaustive)",nodes);
      if(r==1){printf(" labels:");for(int v=0;v<n;v++)printf(" %d",lab[v]);} printf("\n"); }
    return 0; }
  n=atoi(argv[1]);R=atoi(argv[2]);H=atoi(argv[3]);SIDE=atoi(argv[4]); if(argc>6){part=atoi(argv[5]);parts=atoi(argv[6]);} if(argc>7)nodelimit=atoll(argv[7]);
  int par[40];
  u64 rc=gen_rooted(n,[&](const int*L){ int sz=0,mx=0; for(int i=1;i<n;i++){ if(L[i]==2){ if(sz>mx)mx=sz; sz=0;} sz++; } if(sz>mx)mx=sz;
      if(2*mx<n){ from_levels(L,n,0,par); set_tree(par); handle(); } });
  if(rc!=A81[n]){fprintf(stderr,"rooted count mismatch %llu\n",rc);return 2;}
  if(n%2==0){ int h=n/2; vector<vector<int>> half; gen_rooted(h,[&](const int*L){half.push_back(vector<int>(L,L+h));});
    for(size_t i=0;i<half.size();i++)for(size_t j=i;j<half.size();j++){ from_levels(half[i].data(),h,0,par); from_levels(half[j].data(),h,h,par); par[h]=0; set_tree(par); handle(); } }
  if(total!=A55[n]){fprintf(stderr,"free tree count mismatch %llu\n",total);return 2;}
  printf("n=%d R=%d H=%d SIDE=%d part %d/%d: trees generated=%llu (matches A000055), searched here: found(verified)=%llu NONE=%llu aborted=%llu maxnodes=%llu\n",n,R,H,SIDE,part,parts,total,found,none,ab,maxnodes);
}
