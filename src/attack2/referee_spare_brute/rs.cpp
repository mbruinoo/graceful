// Referee program (independent of src/attack2/spare/spare.cpp).
// Relaxed growth labeling of (T,r) with range N=n+slack: injective f:V->{0..N-1}, f(r)=0,
// distinct edge lengths, lengths strictly decreasing away from r.
// Search: lengths N-1 down to 1; each length is either skipped or hangs an unplaced child on its placed parent.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef long long ll;
static inline u64 mix(u64 x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
struct Solver{
  int n,N,root; vector<int> par; vector<vector<int>> ch; vector<u64> typ;
  vector<int> lab,lo,hi,nun; vector<char> used; vector<int> placed;
  ll nodes,cap; int lastv; int order; mt19937 rng; bool capped;
  void setup(const vector<vector<int>>&adj,int r,int N_){
    n=adj.size();N=N_;root=r;par.assign(n,-1);ch.assign(n,{});
    vector<int> bfs;bfs.push_back(r);par[r]=r;
    for(size_t i=0;i<bfs.size();i++){int u=bfs[i];for(int w:adj[u])if(par[w]<0){par[w]=u;ch[u].push_back(w);bfs.push_back(w);}}
    par[r]=-1; lo.assign(n,0);hi.assign(n,N-1);lastv=-1;order=0;cap=-1;bfsord=bfs;
  }
  vector<int> bfsord;
  void finalize(){ // types (after constraints are set)
    typ.assign(n,0);
    for(int i=n-1;i>=0;i--){int v=bfsord[i];vector<u64> hs;for(int c:ch[v])hs.push_back(typ[c]);sort(hs.begin(),hs.end());
      u64 h=mix(1000003ULL*lo[v]+hi[v]*7919ULL+(v==lastv?123456789ULL:0)+17);for(u64 x:hs)h=mix(h^mix(x)+0x1234567ULL*h);typ[v]=h;}
    for(int v=0;v<n;v++)sort(ch[v].begin(),ch[v].end(),[&](int a,int b){return typ[a]<typ[b];});
  }
  bool rec(int L,int rem){
    if(rem==0)return true;
    if(L<rem)return false;
    if(cap>=0&&nodes>=cap){capped=true;return false;}
    nodes++;
    int P=placed.size();
    int start=0,dir=1;
    if(order==1){start=P-1;dir=-1;}
    else if(order>=2){start=rng()%P;dir=(rng()&1)?1:-1;}
    bool trySkipFirst=(order>=2 && L>rem && (rng()%8==0));
    if(trySkipFirst){ if(rec(L-1,rem))return true; if(capped)return false; }
    for(int k=0;k<P;k++){
      int idx=((start+dir*k)%P+P)%P; int u=placed[idx]; if(!nun[u])continue;
      int s0=(order>=2&&(rng()&1))?1:0;
      for(int si=0;si<2;si++){
        int p=((si^s0)==0)?lab[u]+L:lab[u]-L; if(p<0||p>=N||used[p])continue;
        u64 prev=0;bool hp=false;
        for(int c:ch[u]){ if(lab[c]>=0)continue; if(hp&&typ[c]==prev)continue; hp=true;prev=typ[c];
          if(p<lo[c]||p>hi[c])continue;
          if(lastv>=0){ if((c==lastv)!=(L==1))continue; }
          lab[c]=p;used[p]=1;nun[u]--;placed.push_back(c);
          bool ok=rec(L-1,rem-1);
          if(ok)return true;
          placed.pop_back();nun[u]++;used[p]=0;lab[c]=-1;
          if(capped)return false;
        }
      }
    }
    if(L>rem&&!trySkipFirst){ if(rec(L-1,rem))return true; }
    return false;
  }
  // 1 found, 0 none (exact), 2 cap
  int run(int ord,ll cap_,unsigned seed=1){
    order=ord;cap=cap_;rng.seed(seed);nodes=0;capped=false;
    lab.assign(n,-1);used.assign(N,0);nun.assign(n,0);placed.clear();
    for(int v=0;v<n;v++)nun[v]=ch[v].size();
    if(lo[root]>0)return 0;
    lab[root]=0;used[0]=1;placed.push_back(root);
    bool ok=rec(N-1,n-1);
    if(ok){ if(!verify()){fprintf(stderr,"VERIFYFAIL\n");exit(3);} return 1;}
    return capped?2:0;
  }
  bool verify(){ // from the definition
    vector<char> us(N,0),ul(N,0);
    for(int v=0;v<n;v++){ if(lab[v]<0||lab[v]>=N||us[lab[v]])return false; us[lab[v]]=1; if(lab[v]<lo[v]||lab[v]>hi[v])return false;}
    if(lab[root]!=0)return false;
    for(int v=0;v<n;v++)if(v!=root){int l=abs(lab[v]-lab[par[v]]); if(l<1||ul[l])return false; ul[l]=1;
      int u=par[v]; if(u!=root){int l2=abs(lab[u]-lab[par[u]]); if(!(l<l2))return false;}
      if(lastv>=0 && ((v==lastv)!=(l==1)))return false;}
    return true;
  }
  // portfolio: exact NONE if any complete order exhausts; FOUND if any finds
  int solve(ll cap0,ll bigcap,ll*tot=nullptr){
    int r=run(0,cap0); if(tot)*tot+=nodes; if(r!=2)return r;
    r=run(1,cap0); if(tot)*tot+=nodes; if(r!=2)return r;
    ll c=cap0;
    for(int rd=0;rd<40;rd++){ r=run(2,c,1000+rd); if(tot)*tot+=nodes; if(r==1)return r; if(r==0)return 0; if(rd%8==7&&c<bigcap)c*=4; }
    r=run(0,bigcap); if(tot)*tot+=nodes; return r;
  }
};
string canon(const vector<vector<int>>&adj,int v,int p){vector<string> s;for(int w:adj[v])if(w!=p)s.push_back(canon(adj,w,v));sort(s.begin(),s.end());string r="(";for(auto&x:s)r+=x;return r+")";}
int orbit(const vector<vector<int>>&adj,int r){string c=canon(adj,r,-1);int k=0;for(int v=0;v<(int)adj.size();v++)if(canon(adj,v,-1)==c)k++;return k;}
// Beyer-Hedetniemi rooted trees
struct RT{int n;vector<int>L;bool first=true;
  RT(int n_):n(n_),L(n_+1){for(int i=1;i<=n;i++)L[i]=i;}
  bool next(){ if(first){first=false;return true;} int p=n;while(p>=1&&L[p]<=2)p--; if(p<1)return false; int q=p-1;while(L[q]!=L[p]-1)q--; for(int i=p;i<=n;i++)L[i]=L[i-(p-q)]; return true;}
  vector<vector<int>> adj(){vector<vector<int>>a(n);vector<int> last(n+2,-1);for(int i=1;i<=n;i++){ if(i>1){int pa=last[L[i]-1];a[pa].push_back(i-1);a[i-1].push_back(pa);} last[L[i]]=i-1;}return a;}
};
void printlab(Solver&S){for(int v=0;v<S.n;v++)printf(" %d",S.lab[v]);}
int main(int argc,char**argv){
  string mode=argv[1];
  if(mode=="file"){ // file slack cap0 bigcap [show]
    int slack=atoi(argv[2]);ll cap0=atoll(argv[3]),big=atoll(argv[4]);bool show=argc>5;
    string line;int nf=0,nn=0,nc=0,tot=0;
    while(getline(cin,line)){ if(line.empty())continue; istringstream is(line);string name;int n,r;is>>name>>n>>r;vector<vector<int>>adj(n);int a,b;int m=0;while(is>>a>>b){adj[a].push_back(b);adj[b].push_back(a);m++;}
      if(m!=n-1){fprintf(stderr,"bad tree %s\n",name.c_str());return 2;}
      Solver S;S.setup(adj,r,n+slack);S.finalize();ll t=0;int res=S.solve(cap0,big,&t);tot++;
      if(res==1)nf++;else if(res==0)nn++;else nc++;
      printf("%s n=%d slack=%d %s nodes=%lld",name.c_str(),n,slack,res==1?"FOUND":res==0?"NONE":"CAP",t);
      if(res==1&&show){printf(" lab");printlab(S);}
      printf("\n");fflush(stdout);}
    printf("TOTAL %d FOUND %d NONE %d CAP %d\n",tot,nf,nn,nc);
  } else if(mode=="all"){ // all n slack part mod cap0 bigcap
    int n=atoi(argv[2]),slack=atoi(argv[3]),part=atoi(argv[4]),mod=atoi(argv[5]);ll cap0=atoll(argv[6]),big=atoll(argv[7]);
    RT g(n);ll idx=0,nt=0,nf=0,nn=0,nc=0,pairsNone=0,hard=0;
    while(g.next()){ if((idx++)%mod!=part)continue; auto adj=g.adj();Solver S;S.setup(adj,0,n+slack);S.finalize();
      int res=S.run(0,cap0); if(res==2){hard++;res=S.solve(cap0,big);} nt++;
      if(res==1)nf++;else if(res==0){nn++;int o=orbit(adj,0);pairsNone+=o; if(argc>8){printf("NONE orbit=%d L:",o);for(int i=1;i<=n;i++)printf(" %d",g.L[i]);printf("\n");}}
      else{nc++;printf("CAP L:");for(int i=1;i<=n;i++)printf(" %d",g.L[i]);printf("\n");fflush(stdout);}
    }
    printf("n=%d slack=%d part=%d/%d rootedtrees(total enumerated)=%lld handled=%lld FOUND=%lld NONE=%lld (vertex pairs %lld) CAP=%lld firstpass-capped=%lld\n",n,slack,part,mod,idx,nt,nf,nn,pairsNone,nc,hard);
  } else if(mode=="e1"){ // S1+: non-anchors and one extra leaf
    int n=atoi(argv[2]);RT g(n);ll pairs=0,some=0,atroot=0,nonework=0;
    while(g.next()){auto adj=g.adj();Solver S;S.setup(adj,0,n);S.finalize();int res=S.solve(200000,2000000000LL); if(res==2){printf("CAP\n");return 1;} if(res==1)continue;
      int o=orbit(adj,0);pairs+=o;bool any=false,rt=false;
      for(int w=0;w<n;w++){auto a2=adj;a2.push_back({w});a2[w].push_back(n);Solver S2;S2.setup(a2,0,n+1);S2.finalize();int r2=S2.solve(200000,2000000000LL); if(r2==2){printf("CAP\n");return 1;} if(r2==1){any=true;if(w==0)rt=true;}}
      if(any)some+=o;else nonework+=o; if(rt)atroot+=o;}
    printf("E1 n=%d nonanchor pairs=%lld some-leaf-works=%lld leaf-at-root-works=%lld none-works=%lld\n",n,pairs,some,atroot,nonework);
  } else if(mode=="e2"){ // (tree, leaf) pairs; is there a growth placement whose length-1 bracket hangs the leaf
    int n=atoi(argv[2]);RT g(n);ll pairs=0,can=0,cannot=0;
    while(g.next()){auto adj=g.adj(); if(adj[0].size()!=1)continue; int o=orbit(adj,0);pairs+=o;bool ok=false;
      for(int r=1;r<n&&!ok;r++){Solver S;S.setup(adj,r,n);S.lastv=0;S.finalize();int res=S.solve(1000000,2000000000LL); if(res==2){printf("CAP\n");return 1;} if(res==1)ok=true;}
      if(ok)can+=o;else{cannot+=o; if(n<=7){printf("  fail (orbit %d) L:",o);for(int i=1;i<=n;i++)printf(" %d",g.L[i]);printf("\n");}}}
    printf("E2 n=%d (tree,leaf) pairs=%lld can=%lld cannot=%lld\n",n,pairs,can,cannot);
  } else if(mode=="piece"){ // piece b j cap : crossing one-spare labelings of path arms (b,j), j-tip innermost
    int b=atoi(argv[2]),j=atoi(argv[3]);ll cap=atoll(argv[4]);int n=b+j+1;vector<vector<int>>adj(n);
    // vertices: 0 root; A arm 1..b ; B arm b+1..b+j
    vector<int> dep(n,0);
    for(int i=1;i<=b;i++){int p=i-1;adj[p].push_back(i);adj[i].push_back(p);dep[i]=i;}
    for(int i=1;i<=j;i++){int v=b+i,p=(i==1)?0:v-1;adj[p].push_back(v);adj[v].push_back(p);dep[v]=i;}
    int y=b+j;int E=0;for(int v=0;v<n;v++)if(dep[v]%2==0)E++;
    // cases: (evenmax, oddmin, ylabel)
    vector<array<int,3>> cs; if(dep[y]%2==0){cs.push_back({E-1,E,E-1});cs.push_back({E,E+1,E});} else {cs.push_back({E-1,E,E});cs.push_back({E,E+1,E+1});}
    int anyfound=0,anycap=0;ll tot=0;
    for(auto c:cs){Solver S;S.setup(adj,0,n+1);for(int v=0;v<n;v++){if(dep[v]%2==0){S.lo[v]=0;S.hi[v]=c[0];}else{S.lo[v]=c[1];S.hi[v]=n;}} S.lo[y]=S.hi[y]=c[2];S.finalize();
      int res=S.run(0,cap);tot+=S.nodes; if(res==1){anyfound=1;printf("piece b=%d j=%d FOUND:",b,j);printlab(S);printf("\n");break;} if(res==2)anycap=1;}
    if(!anyfound)printf("piece b=%d j=%d %s nodes=%lld\n",b,j,anycap?"CAP(undecided)":"NONE(exhaustive)",tot);
  }
  return 0;
}
