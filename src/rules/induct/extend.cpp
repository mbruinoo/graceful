// EXTENSION RELATION between valid deals (exhaustive).
// A deal D' of a spider S' EXTENDS a deal D of a sub-spider S if deleting the extra edges of S' and
// renumbering the surviving numbers by rank (order preserved) gives D, with the same up/down signs
// (for edges inserted at the base of a leg the rest of that leg may keep its signs or have them all flipped;
//  the first surviving edge of a leg is always "up").
// We enumerate ALL valid deals for every spider with m <= M edges, and for every deal D' compute its
// restrictions of the following types; each restriction that is itself a valid deal D marks D as
// "extendable" by that type.
//   TIP1(i)  : leg i longer by one edge at its tip          TIP2(i): by two edges at its tip
//   BASE(i,v): leg i longer by one edge at its base; v=0 rest keeps signs, v=1 rest flipped
//   ALLTIP1 / ALLTIP2 : every leg longer by one / two at the tip
//   ALLBASE  : every leg longer by one at the base (each leg keep or flip), ALLBASEM: all flipped (mirror)
//   NEW(r)   : one new leg of length r (r=1..4)             TWO(r): two new legs of length r (r=1..3)
// Output: per m, number of deals D having at least one extension of each type, and the first deal lacking one.
// Usage: extend M     (M <= 17; deals with m edges are tested for a type adding c edges only if m+c <= M)
#include <bits/stdc++.h>
using namespace std;
typedef vector<vector<int>> Deal;
int M;
vector<vector<Deal>> deals;                 // deals[m]
vector<unordered_map<string,int>> idx;      // key -> id
string keyOf(const Deal&d){ string s; for(auto&l:d){ s.push_back((char)(100+l.size())); for(int x:l) s.push_back((char)(64+x)); } return s; }
// ---- enumeration
int k,m_; int L[32], cnt_[32], cur[32]; bool used[64]; Deal w;
void rec(int t){ if(t==0){ idx[m_][keyOf(w)]=deals[m_].size(); deals[m_].push_back(w); return; }
  for(int i=0;i<k;i++){ if(cnt_[i]==L[i]) continue; if(cnt_[i]==0 && i>0 && L[i-1]==L[i] && cnt_[i-1]==0) continue;
    for(int sg=0; sg<(cnt_[i]>0?2:1); sg++){ int x=(cnt_[i]==0||sg==1)?cur[i]+t:cur[i]-t; if(x<1||x>m_||used[x]) continue;
      int old=cur[i]; cur[i]=x; used[x]=1; cnt_[i]++; w[i].push_back(x>old?t:-t); rec(t-1); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; } } }
vector<int> part;
void gen(int rem,int mx){ if(rem==0){ k=part.size(); w.assign(k,{}); for(int i=0;i<k;i++){ L[i]=part[i]; cnt_[i]=0; cur[i]=0; } memset(used,0,sizeof used); rec(m_); return; }
  for(int x=min(rem,mx);x>=1;x--){ part.push_back(x); gen(rem-x,x); part.pop_back(); } }
// ---- restriction.  nb[i] in {0,1}: drop first edge; nt[i]: drop last nt edges; fl[i]: flip signs after first surviving edge.
// returns id of restricted deal in deals[m2] or -1; perm[j] = index (in D') of the leg that became canonical leg j of D.
int restrict_(const Deal&d,const int*nb,const int*nt,const int*fl,int&m2,vector<int>&perm){
  static int rk[64]; bool keep[64]; memset(keep,0,sizeof keep); int kk=d.size();
  for(int i=0;i<kk;i++) for(int j=nb[i]; j<(int)d[i].size()-nt[i]; j++) keep[abs(d[i][j])]=1;
  int mm=0; for(auto&l:d) mm+=l.size(); m2=0; for(int x=1;x<=mm;x++) if(keep[x]) rk[x]=++m2;
  vector<pair<vector<int>,int>> legs;
  for(int i=0;i<kk;i++){ vector<int> l; for(int j=nb[i]; j<(int)d[i].size()-nt[i]; j++){ int a=rk[abs(d[i][j])]; int s=d[i][j]>0?1:-1; if(fl[i]) s=-s; if(l.empty()) s=1; l.push_back(s*a); } if(!l.empty()) legs.push_back({l,i}); }
  if(m2==0) return -1;
  bool u[64]; memset(u,0,sizeof u); for(auto&pl:legs){ int c=0; for(int x:pl.first){ c+=x; if(c<1||c>m2||u[c]) return -1; u[c]=1; } }
  sort(legs.begin(),legs.end(),[](const pair<vector<int>,int>&a,const pair<vector<int>,int>&b){ if(a.first.size()!=b.first.size()) return a.first.size()>b.first.size(); return a.first[0]>b.first[0]; });
  Deal r; perm.clear(); for(auto&pl:legs){ r.push_back(pl.first); perm.push_back(pl.second); }
  auto it=idx[m2].find(keyOf(r)); if(it==idx[m2].end()){ fprintf(stderr,"BUG: valid restriction not enumerated\n"); exit(1); } return it->second; }
enum { ALLTIP1=0, ALLTIP2, ALLBASE, ALLBASEM, NEW1, NEW2, NEW3, NEW4, TWO1, TWO2, TWO3, NF };
const char* fname[NF]={"ALLTIP1","ALLTIP2","ALLBASE","ALLBASEM","NEW1","NEW2","NEW3","NEW4","TWO1","TWO2","TWO3"};
int fadd(int f,int kS){ switch(f){ case ALLTIP1: return kS; case ALLTIP2: return 2*kS; case ALLBASE: case ALLBASEM: return kS; case NEW1: return 1; case NEW2: return 2; case NEW3: return 3; case NEW4: return 4; case TWO1: return 2; case TWO2: return 4; case TWO3: return 6; } return 0; }
vector<vector<uint32_t>> tip1, tip2, base0, base1, flags;
void printDeal(const Deal&d){ printf("S("); for(size_t i=0;i<d.size();i++) printf("%zu%s",d[i].size(),i+1<d.size()?",":""); printf(") numbers"); for(auto&l:d){ printf(" ["); for(size_t j=0;j<l.size();j++) printf("%s%+d",j?" ":"",l[j]); printf("]"); } }
int main(int argc,char**argv){ M=atoi(argv[1]); deals.resize(M+1); idx.resize(M+1);
  for(m_=1;m_<=M;m_++){ gen(m_,m_); fprintf(stderr,"m=%d deals=%zu\n",m_,deals[m_].size()); }
  tip1.resize(M+1); tip2.resize(M+1); base0.resize(M+1); base1.resize(M+1); flags.resize(M+1);
  for(int m=1;m<=M;m++){ size_t n=deals[m].size(); tip1[m].assign(n,0); tip2[m].assign(n,0); base0[m].assign(n,0); base1[m].assign(n,0); flags[m].assign(n,0); }
  int nb[32],nt[32],fl[32]; vector<int> perm; int m2;
  for(int m=2;m<=M;m++) for(const Deal&d:deals[m]){ int kk=d.size();
    auto zero=[&](){ for(int i=0;i<kk;i++) nb[i]=nt[i]=fl[i]=0; };
    auto legOf=[&](int i){ for(size_t j=0;j<perm.size();j++) if(perm[j]==i) return (int)j; return -1; };
    for(int i=0;i<kk;i++){ int Li=d[i].size();
      if(Li>=2){ zero(); nt[i]=1; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) tip1[m2][id]|=1u<<legOf(i); }
      if(Li>=3){ zero(); nt[i]=2; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) tip2[m2][id]|=1u<<legOf(i); }
      if(Li>=2) for(int v=0;v<2;v++){ zero(); nb[i]=1; fl[i]=v; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) (v?base1:base0)[m2][id]|=1u<<legOf(i); }
      // remove whole leg i
      if(kk>=2 && Li<=4){ zero(); nt[i]=Li; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) flags[m2][id]|=1u<<(NEW1+Li-1); }
      for(int j=i+1;j<kk;j++) if((int)d[j].size()==Li && Li<=3 && kk>=3){ zero(); nt[i]=nt[j]=Li; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) flags[m2][id]|=1u<<(TWO1+Li-1); } }
    int mn=99; for(auto&l:d) mn=min(mn,(int)l.size());
    if(mn>=2){ zero(); for(int i=0;i<kk;i++) nt[i]=1; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) flags[m2][id]|=1u<<ALLTIP1;
      for(int mask=0;mask<(1<<kk);mask++){ zero(); for(int i=0;i<kk;i++){ nb[i]=1; fl[i]=(mask>>i)&1; } int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0){ flags[m2][id]|=1u<<ALLBASE; if(mask==(1<<kk)-1) flags[m2][id]|=1u<<ALLBASEM; } } }
    if(mn>=3){ zero(); for(int i=0;i<kk;i++) nt[i]=2; int id=restrict_(d,nb,nt,fl,m2,perm); if(id>=0) flags[m2][id]|=1u<<ALLTIP2; }
  }
  // ---- report
  printf("columns: m, deals, then for each type: (#deals with at least one extension)/(#deals tested)\n");
  for(int m=1;m<=M;m++){ size_t n=deals[m].size(); printf("m=%d deals=%zu\n",m,n);
    if(m+1<=M){ long a=0,b=0,legsT=0,legsOK=0; for(size_t i=0;i<n;i++){ int kS=deals[m][i].size(); legsT+=kS; legsOK+=__builtin_popcount(tip1[m][i]); if(tip1[m][i]) a++; if(tip1[m][i]==(1u<<kS)-1) b++; }
      printf("   TIP1: some leg %ld/%zu, every leg %ld/%zu, (deal,leg) pairs %ld/%ld\n",a,n,b,n,legsOK,legsT); }
    if(m+2<=M){ long a=0,legsT=0,legsOK=0; for(size_t i=0;i<n;i++){ legsT+=deals[m][i].size(); legsOK+=__builtin_popcount(tip2[m][i]); if(tip2[m][i]) a++; } printf("   TIP2: some leg %ld/%zu, pairs %ld/%ld\n",a,n,legsOK,legsT); }
    if(m+1<=M){ long a=0,b=0,c=0,legsT=0,l0=0,l1=0; for(size_t i=0;i<n;i++){ legsT+=deals[m][i].size(); l0+=__builtin_popcount(base0[m][i]); l1+=__builtin_popcount(base1[m][i]); if(base0[m][i]) a++; if(base1[m][i]) b++; if(base0[m][i]|base1[m][i]) c++; }
      printf("   BASE: some leg keep-signs %ld/%zu, flipped %ld/%zu, either %ld/%zu; pairs keep %ld flipped %ld of %ld\n",a,n,b,n,c,n,l0,l1,legsT); }
    for(int f=0;f<NF;f++){ long tot=0,ok=0; int firstFail=-1; for(size_t i=0;i<n;i++){ int kS=deals[m][i].size(); if(m+fadd(f,kS)>M) continue; tot++; if(flags[m][i]>>f&1) ok++; else if(firstFail<0) firstFail=i; }
      if(tot){ printf("   %-8s %ld/%ld",fname[f],ok,tot); if(firstFail>=0){ printf("   first without: "); printDeal(deals[m][firstFail]); } printf("\n"); } } }
  // ---- per spider: does every / some deal extend, for the leg-adding types
  if(argc>2){ for(int m=1;m<=M;m++){ map<vector<int>,array<long,2*NF+1>> sp; for(size_t i=0;i<deals[m].size();i++){ vector<int> sh; for(auto&l:deals[m][i]) sh.push_back(l.size()); auto&a=sp[sh]; a[2*NF]++; for(int f=0;f<NF;f++){ if(m+fadd(f,sh.size())>M) continue; a[2*f]++; if(flags[m][i]>>f&1) a[2*f+1]++; } }
      for(auto&pr:sp){ printf("SP m=%d S(",m); for(size_t i=0;i<pr.first.size();i++) printf("%d%s",pr.first[i],i+1<pr.first.size()?",":""); printf(") deals=%ld",pr.second[2*NF]); for(int f=0;f<NF;f++) if(pr.second[2*f]) printf(" %s=%ld",fname[f],pr.second[2*f+1]); printf("\n"); } } }
}
