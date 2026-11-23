// Slide-graph explorer, written from README section 1 definitions.
// usage: sl n [dump]
// Enumerates all tree placements; computes
//  - right-slide reach from the star, growth placements inside/outside it
//  - local minima (no legal left slide), shapes among them
//  - components under unit slides, and under richer move sets
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; u64 W[32]; vector<u64> cf;
bool isTree(const int*p){ int q[32]; for(int i=1;i<=n;i++)q[i]=i;
  for(int k=1;k<n;k++){int a=p[k],b=p[k]+k; while(q[a]!=a)a=q[a]; while(q[b]!=b)b=q[b]; if(a==b)return false; q[a]=b;} return true;}
void rec(int k,int*p){ // brute force with pruning by acyclicity (union-find rebuilt each level: simple, from definitions)
  if(k==0){ u64 x=0; for(int j=1;j<n;j++) x+=(u64)(p[j]-1)*W[j]; cf.push_back(x); return; }
  for(int pp=1;pp<=n-k;pp++){ p[k]=pp; int q[32]; for(int i=1;i<=n;i++)q[i]=i; bool ok=true;
    for(int j=n-1;j>=k;j--){int a=p[j],b=p[j]+j; while(q[a]!=a)a=q[a]; while(q[b]!=b)b=q[b]; if(a==b){ok=false;break;} q[a]=b;}
    if(ok) rec(k-1,p);} }
void dec(u64 x,int*p){ for(int k=1;k<n;k++) p[k]=(x/W[k])%(n-k)+1; }
long look(u64 x){ auto it=lower_bound(cf.begin(),cf.end(),x); return (it!=cf.end()&&*it==x)?it-cf.begin():-1; }
bool growth(const int*p){ vector<char> used(n+1,0); used[p[n-1]]=used[p[n-1]+n-1]=1;
  for(int k=n-2;k>=1;k--){int a=p[k],b=p[k]+k; if(used[a]==used[b])return false; used[a]=used[b]=1;} return true;}
string canon(const int*p){
  vector<vector<int>> adj(n+1); for(int k=1;k<n;k++){adj[p[k]].push_back(p[k]+k);adj[p[k]+k].push_back(p[k]);}
  vector<int> deg(n+1),layer; int rem=n; for(int i=1;i<=n;i++){deg[i]=adj[i].size(); if(deg[i]<=1)layer.push_back(i);}
  vector<char> gone(n+1,0);
  while(rem>2){vector<int> nx; for(int v:layer){gone[v]=1;rem--; for(int u:adj[v]) if(!gone[u]&&--deg[u]==1) nx.push_back(u);} layer=nx;}
  function<string(int,int)> enc=[&](int v,int pa){vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch)s+=c; return s+")";};
  if(layer.size()==1) return enc(layer[0],0);
  string a=enc(layer[0],layer[1]),b=enc(layer[1],layer[0]); if(a>b)swap(a,b); return a+b;}
vector<int> uf; int ff(int x){while(uf[x]!=x){uf[x]=uf[uf[x]];x=uf[x];}return x;}
void un(long a,long b){a=ff(a);b=ff(b); if(a!=b)uf[a]=b;}
size_t ncomp(){ size_t c=0; for(size_t i=0;i<uf.size();i++) if(ff(i)==(int)i)c++; return c; }
int main(int argc,char**argv){ n=atoi(argv[1]); bool dump=argc>2;
  u64 w=1; for(int k=1;k<n;k++){W[k]=w;w*=(n-k);} int p[32]; rec(n-1,p); sort(cf.begin(),cf.end()); size_t N=cf.size();
  vector<string> shape(N); set<string> all; vector<char> gr(N);
  for(size_t i=0;i<N;i++){dec(cf[i],p); shape[i]=canon(p); all.insert(shape[i]); gr[i]=growth(p);}
  printf("n=%d placements=%zu shapes=%zu\n",n,N,all.size());
  // right reach
  vector<char> R(N,0); {vector<int> q; q.push_back(0); R[0]=1; for(size_t h=0;h<q.size();h++){int i=q[h]; dec(cf[i],p); for(int k=1;k<n;k++) if(p[k]<n-k){long j=look(cf[i]+W[k]); if(j>=0&&!R[j]){R[j]=1;q.push_back(j);}}}
    size_t g=0,gin=0; set<string> s; for(size_t i=0;i<N;i++){ if(gr[i]){g++; if(R[i])gin++;} if(R[i])s.insert(shape[i]); }
    printf("rightreach=%zu shapes=%zu growth=%zu growth_in_reach=%zu\n",q.size(),s.size(),g,gin);
    set<string> sg; for(size_t i=0;i<N;i++) if(gr[i]&&R[i]) sg.insert(shape[i]); printf("shapes with a right-reachable growth placement=%zu\n",sg.size()); }
  // local minima / maxima and unit components
  uf.resize(N); iota(uf.begin(),uf.end(),0);
  size_t nmin=0, nboth=0; set<string> smin; vector<char> isMin(N,0);
  for(size_t i=0;i<N;i++){dec(cf[i],p); bool L=false,Rr=false; for(int k=1;k<n;k++){ if(p[k]>1){long j=look(cf[i]-W[k]); if(j>=0){L=true;un(i,j);}} if(p[k]<n-k){ if(look(cf[i]+W[k])>=0)Rr=true; } }
    if(!L){nmin++; isMin[i]=1; smin.insert(shape[i]);} if(!L&&!Rr)nboth++; }
  printf("localmin(no left slide)=%zu shapes_among_localmin=%zu isolated=%zu unit_components=%zu\n",nmin,smin.size(),nboth,ncomp());
  { size_t c=0; set<string> s; for(size_t i=0;i<N;i++) if(isMin[i]&&gr[i]){c++; s.insert(shape[i]);} printf("localmin&growth=%zu shapes=%zu\n",c,s.size()); }
  { map<int,vector<int>> comp; for(size_t i=0;i<N;i++) comp[ff(i)].push_back(i); map<size_t,int> hist; int star=ff(0); set<string> sstar; for(int i:comp[star]) sstar.insert(shape[i]);
    for(auto&c:comp) hist[c.second.size()]++; printf("component size histogram:"); for(auto&h:hist) printf(" %zu:%d",h.first,h.second); printf("\nstar comp shapes=%zu\n",sstar.size());
    if(dump){ FILE*f=fopen((string("islands_")+argv[1]+".txt").c_str(),"w"); for(auto&c:comp) if(c.first!=star){ fprintf(f,"I %zu\n",c.second.size()); for(int i:c.second){dec(cf[i],p); for(int k=1;k<n;k++)fprintf(f,"%d ",p[k]); fprintf(f,"\n");} } fclose(f);} }
  vector<int> unit=uf;
  // richer moves, each added to unit slides
  auto base=[&](){uf=unit;};
  // (a) slide by 2 (endpoints trees, middle arbitrary)
  base(); for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) if(p[k]+2<=n-k){long j=look(cf[i]+2*W[k]); if(j>=0)un(i,j);} }
  printf("unit + slide-by-2: components=%zu\n",ncomp());
  // (b) reflect through a foot = slide by k
  base(); for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) if(p[k]+k<=n-k){long j=look(cf[i]+(u64)k*W[k]); if(j>=0)un(i,j);} }
  printf("unit + reflect-through-foot: components=%zu\n",ncomp());
  { uf.assign(N,0); iota(uf.begin(),uf.end(),0); for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) if(p[k]+k<=n-k){long j=look(cf[i]+(u64)k*W[k]); if(j>=0)un(i,j);} } printf("reflect-through-foot alone: components=%zu\n",ncomp()); }
  // (c) two brackets at once, each by +-1
  base(); for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) for(int l=k+1;l<n;l++) for(int s=-1;s<=1;s+=2) for(int t=-1;t<=1;t+=2){ int a=p[k]+s,b=p[l]+t; if(a<1||a>n-k||b<1||b>n-l)continue; if(s<0&&t<0)continue; // symmetric: handle pairs once via ordering of result
        u64 x=cf[i]+(s>0?W[k]:-W[k])+(t>0?W[l]:-W[l]); if(s>0&&t>0){long j=look(x); if(j>=0)un(i,j);} else {long j=look(x); if(j>=0)un(i,j);} } }
  printf("unit + two-at-once: components=%zu\n",ncomp());
  // (d) all three
  for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++){ if(p[k]+2<=n-k){long j=look(cf[i]+2*W[k]); if(j>=0)un(i,j);} if(p[k]+k<=n-k){long j=look(cf[i]+(u64)k*W[k]); if(j>=0)un(i,j);} } }
  printf("unit + two-at-once + by-2 + reflect: components=%zu\n",ncomp());
  // (e) long jump (README Observation D) for reference
  base(); for(size_t i=0;i<N;i++){dec(cf[i],p); for(int k=1;k<n;k++) for(int np=p[k]+2;np<=n-k;np++){long j=look(cf[i]+(u64)(np-p[k])*W[k]); if(j>=0)un(i,j);} }
  printf("long-jump: components=%zu\n",ncomp());
}
