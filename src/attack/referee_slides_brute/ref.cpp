// Referee brute force, written from README section 1 only.
// usage: ./ref n
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64; typedef uint32_t u32;
int n; u64 W[20]; // W[k] weight of bracket k
vector<u32> codes; vector<u64> bm; vector<u32> pre;
void dfs(int k,u64 code,const unsigned char*comp){
  if(k==0){codes.push_back((u32)code);return;}
  for(int p=1;p<=n-k;p++){int a=comp[p],b=comp[p+k];if(a==b)continue;
    unsigned char c2[20];for(int i=1;i<=n;i++)c2[i]=comp[i]==b?a:comp[i];
    dfs(k-1,code+(u64)(p-1)*W[k],c2);}
}
inline bool isT(u64 c){return bm[c>>6]>>(c&63)&1;}
inline u32 rk(u64 c){return pre[c>>6]+__builtin_popcountll(bm[c>>6]&((1ULL<<(c&63))-1));}
struct UF{vector<u32> p;void init(size_t m){p.resize(m);iota(p.begin(),p.end(),0);}
  u32 f(u32 x){while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;}
  void u(u32 a,u32 b){a=f(a);b=f(b);if(a!=b)p[a]=b;}
  size_t cnt(){size_t c=0;for(u32 i=0;i<p.size();i++)if(p[i]==i)c++;return c;}};
void dec(u32 c,int*p){for(int k=1;k<=n-1;k++){p[k]=c%(n-k)+1;c/=(n-k);}}
u64 enc(const int*p){u64 c=0;for(int k=1;k<=n-1;k++)c+=(u64)(p[k]-1)*W[k];return c;}
int adj[20][20],dg[20];
u64 rooted(int v,int par){u64 ch[20];int m=0;for(int i=0;i<dg[v];i++)if(adj[v][i]!=par)ch[m++]=rooted(adj[v][i],v);
  sort(ch,ch+m);u64 r=1;for(int i=0;i<m;i++){int len=64-__builtin_clzll(ch[i]);r=(r<<len)|ch[i];}return r<<1;}
u64 canon(const int*p){for(int i=1;i<=n;i++)dg[i]=0;
  for(int k=1;k<n;k++){int a=p[k],b=p[k]+k;adj[a][dg[a]++]=b;adj[b][dg[b]++]=a;}
  int d[20],rem=n;bool gone[20]={0};for(int i=1;i<=n;i++)d[i]=dg[i];
  while(rem>2){int lv[20],m=0;for(int i=1;i<=n;i++)if(!gone[i]&&d[i]<=1)lv[m++]=i;
    for(int i=0;i<m;i++){gone[lv[i]]=1;rem--;for(int j=0;j<dg[lv[i]];j++)d[adj[lv[i]][j]]--;}}
  int c[2],m=0;for(int i=1;i<=n;i++)if(!gone[i])c[m++]=i;
  if(m==1)return rooted(c[0],0);
  u64 a=rooted(c[0],c[1]),b=rooted(c[1],c[0]);if(a>b)swap(a,b);return (1ULL<<62)|(a<<30)|b;}
int main(int argc,char**argv){n=atoi(argv[1]);W[1]=1;for(int k=2;k<=n-1;k++)W[k]=W[k-1]*(n-(k-1));
  u64 tot=W[n-1];
  unsigned char comp[20];for(int i=1;i<=n;i++)comp[i]=i;dfs(n-1,0,comp);
  size_t T=codes.size();bm.assign(tot/64+2,0);for(u32 c:codes)bm[c>>6]|=1ULL<<(c&63);
  pre.resize(bm.size());{u32 s=0;for(size_t i=0;i<bm.size();i++){pre[i]=s;s+=__builtin_popcountll(bm[i]);}}
  for(size_t i=1;i<T;i++)assert(codes[i]>codes[i-1]);
  printf("n=%d tree placements=%zu\n",n,T);
  UF U1,U2,UR,UT,US,UC;U1.init(T);U2.init(T);UR.init(T);UT.init(T);US.init(T);UC.init(T);
  vector<char> reach(T,0);vector<u64> cn(T);
  size_t nmin=0;long long lemF_viol=0,lemF_tested=0;int p[20];
  set<u64> shapes,minshapes,rshapes;size_t nreach=0;
  for(size_t id=0;id<T;id++){u64 c=codes[id];dec(c,p);cn[id]=canon(p);shapes.insert(cn[id]);
    bool leftslide=false,r=(c==0);
    for(int k=1;k<n;k++){
      if(p[k]>1&&isT(c-W[k])){leftslide=true;if(reach[rk(c-W[k])])r=true;}
      if(p[k]<n-k&&isT(c+W[k])){u32 j=rk(c+W[k]);U1.u(id,j);U2.u(id,j);UR.u(id,j);UT.u(id,j);US.u(id,j);UC.u(id,j);}
      if(p[k]+2<=n-k&&isT(c+2*W[k]))U2.u(id,rk(c+2*W[k]));
      if(p[k]+k<=n-k&&isT(c+k*W[k]))UR.u(id,rk(c+k*W[k]));
    }
    reach[id]=r;if(r){nreach++;rshapes.insert(cn[id]);}
    if(!leftslide){nmin++;minshapes.insert(cn[id]);}
    // two at once
    for(int j=1;j<n;j++){if(p[j]>=n-j)continue;
      for(int k=1;k<n;k++){if(k==j)continue;
        if(k>j&&p[k]<n-k){u64 d=c+W[j]+W[k];if(isT(d)){u32 q=rk(d);UT.u(id,q);US.u(id,q);if(k==j+1)UC.u(id,q);}}
        if(p[k]>1){u64 d=c+W[j]-W[k];if(isT(d)){u32 q=rk(d);UT.u(id,q);if(k==j+1||j==k+1)UC.u(id,q);}}
      }}
    // Lemma F
    int deg[20]={0};for(int k=1;k<n;k++){deg[p[k]]++;deg[p[k]+k]++;}
    for(int k=1;k<n;k++){int a=p[k],b=a+k;if(deg[a]!=1&&deg[b]!=1)continue;lemF_tested++;
      bool L=p[k]>1&&isT(c-W[k]),R=p[k]<n-k&&isT(c+W[k]);
      if(k>=2){if(L||R)lemF_viol++;}
      else{ // k==1
        bool expL,expR; // expected
        if(deg[a]==1&&deg[b]==1){lemF_viol++;continue;}
        if(deg[a]==1){expL=p[k]>1;expR=false;}else{expR=p[k]<n-k;expL=false;}
        if(L!=expL||R!=expR)lemF_viol++;}
    }
  }
  printf("unit components=%zu star comp size=",U1.cnt());{u32 r0=U1.f(0);size_t s=0;for(u32 i=0;i<T;i++)if(U1.f(i)==r0)s++;printf("%zu\n",s);}
  printf("shapes=%zu right-reach placements=%zu shapes=%zu\n",shapes.size(),nreach,rshapes.size());
  printf("local minima=%zu shapes among minima=%zu missing=%zu\n",nmin,minshapes.size(),shapes.size()-minshapes.size());
  for(u64 s:shapes)if(!minshapes.count(s)){for(size_t id=0;id<T;id++)if(cn[id]==s){dec(codes[id],p);printf("  missing shape, e.g. edges:");for(int k=1;k<n;k++)printf(" {%d,%d}",p[k],p[k]+k);
      int deg[20]={0};for(int k=1;k<n;k++){deg[p[k]]++;deg[p[k]+k]++;}sort(deg+1,deg+n+1);printf("  degs:");for(int i=n;i>=1;i--)printf(" %d",deg[i]);
      size_t cntl=0;for(size_t j=0;j<T;j++)if(cn[j]==s)cntl++;printf("  #placements of shape=%zu\n",cntl);break;}}
  printf("components: unit+slide2=%zu unit+reflect=%zu unit+two=%zu two-samedir=%zu two-consec=%zu\n",U2.cnt(),UR.cnt(),UT.cnt(),US.cnt(),UC.cnt());
  printf("LemmaF: leaf-footed (placement,bracket) pairs tested=%lld violations=%lld\n",lemF_tested,lemF_viol);
  // Theorem I
  if(n>=7){int P[20];for(int k=1;k<n;k++)P[k]=1;P[1]=2;P[2]=n-3;P[n-2]=2;u64 c1=enc(P);P[1]=3;u64 c2=enc(P);
    if(!isT(c1)||!isT(c2))printf("ThmI: P or P' NOT a tree\n");else{u32 r1=U1.f(rk(c1));size_t s=0;for(u32 i=0;i<T;i++)if(U1.f(i)==r1)s++;
      printf("ThmI: comp size of P=%zu, P' in same comp=%d\n",s,(int)(U1.f(rk(c2))==r1));}
    // size-2 islands count
    map<u32,u32> cs;for(u32 i=0;i<T;i++)cs[U1.f(i)]++;size_t s2=0,tot2=0;u32 r0=U1.f(0);for(auto&x:cs){if(x.second==2)s2++;if(x.first!=r0)tot2+=x.second;}
    printf("islands(non-star comps)=%zu holding %zu placements; size-2 islands=%zu\n",cs.size()-1,tot2,s2);}
  // Theorem S2
  for(int a=2;2*a+1<=n;a++){int b=n-2*a-1;int F[20];for(int k=1;k<=n-2;k++)F[k]=2;F[n-1]=1;for(int j=1;j<=a-1;j++)F[2*j-1]=a+2-j;
    u64 c=enc(F);bool tr=isT(c);bool sp=false,rr=false;
    if(tr){u32 id=rk(c);rr=reach[id];int deg[20]={0};for(int k=1;k<n;k++){deg[F[k]]++;deg[F[k]+k]++;}
      // spider S(2^a,1^b): compare canonical form with explicitly built spider
      int Q[20];// build spider edges as adjacency directly
      for(int i=1;i<=n;i++)dg[i]=0;auto ae=[&](int x,int y){adj[x][dg[x]++]=y;adj[y][dg[y]++]=x;};
      int v=2;for(int i=0;i<a;i++){ae(1,v);ae(v,v+1);v+=2;}for(int i=0;i<b;i++){ae(1,v);v++;}
      // canonical of this graph: reuse canon internals by duplicating code
      {int d[20],rem=n;bool gone[20]={0};for(int i=1;i<=n;i++)d[i]=dg[i];
       while(rem>2){int lv[20],m=0;for(int i=1;i<=n;i++)if(!gone[i]&&d[i]<=1)lv[m++]=i;for(int i=0;i<m;i++){gone[lv[i]]=1;rem--;for(int j=0;j<dg[lv[i]];j++)d[adj[lv[i]][j]]--;}}
       int cc[2],m=0;for(int i=1;i<=n;i++)if(!gone[i])cc[m++]=i;u64 s;
       if(m==1)s=rooted(cc[0],0);else{u64 x=rooted(cc[0],cc[1]),y=rooted(cc[1],cc[0]);if(x>y)swap(x,y);s=(1ULL<<62)|(x<<30)|y;}
       sp=(s==cn[id]);} (void)Q;(void)deg;}
    printf("S2: a=%d b=%d tree=%d spider=%d right-reachable=%d\n",a,b,tr,sp,rr);}
  return 0;}
