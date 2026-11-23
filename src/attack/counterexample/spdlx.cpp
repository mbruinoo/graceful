// Centre-anchored deal (README section 13) for a spider with n1 legs of length 1, n2 of length 2, n3 of length 3,
// as an exact cover.  Centre label 0, labels 0..N, N = n1+2*n2+3*n3.  Items len_y, lab_y (y=1..N).
// An option is a whole leg: lengths a>b>c from the centre outward and signs; labels a, a+-b, a+-b+-c in 1..N, distinct.
// Search: item with fewest live options, random order, restarts.  With ZIG=1 only alternating legs (a, a-b, a-b+c).
// Output "n1 n2 n3 OK legs: l1,l2,l3 ..." (labels along each leg) after a check from the definition:
// all labels 1..N once, all lengths 1..N once, lengths strictly decreasing outward on every leg.
// usage: spdlx n1 n2 n3 [n1 n2 n3 ...]
#include <bits/stdc++.h>
using namespace std;
struct Opt{ int type; int nit; int it[6]; int lab[3]; };
int N; vector<Opt> opt; vector<vector<int>> byItem; vector<array<int,3>> cnt; vector<char> covered, dead; int quota[3];
long long nodes, lim; mt19937 rng(5); vector<int> chosen; int totalLegs;
bool dfs(int depth){
  if(depth==totalLegs) return true; if(++nodes>lim) return false;
  int best=-1, bc=1<<30; for(int it=0;it<2*N;it++) if(!covered[it]){ int c=0; for(int t=0;t<3;t++) if(quota[t]>0) c+=cnt[it][t]; if(c<bc || (c==bc && (rng()&1))){ bc=c; best=it; } }
  if(bc==0) return false;
  vector<int> cand; for(int o:byItem[best]) if(!dead[o] && quota[opt[o].type]>0) cand.push_back(o); shuffle(cand.begin(),cand.end(),rng);
  for(int o:cand){ vector<int> killed; for(int j=0;j<opt[o].nit;j++){ int it=opt[o].it[j]; covered[it]=1; for(int q:byItem[it]) if(!dead[q]){ dead[q]=1; killed.push_back(q); for(int t=0;t<opt[q].nit;t++) cnt[opt[q].it[t]][opt[q].type]--; } }
    quota[opt[o].type]--; chosen.push_back(o); if(dfs(depth+1)) return true; chosen.pop_back(); quota[opt[o].type]++;
    for(int q:killed){ dead[q]=0; for(int t=0;t<opt[q].nit;t++) cnt[opt[q].it[t]][opt[q].type]++; } for(int j=0;j<opt[o].nit;j++) covered[opt[o].it[j]]=0; if(nodes>lim) return false; }
  return false; }
int main(int c,char**v){ bool ZIG=getenv("ZIG");
  for(int ai=1;ai+2<c;ai+=3){ int n1=atoi(v[ai]), n2=atoi(v[ai+1]), n3=atoi(v[ai+2]); N=n1+2*n2+3*n3; totalLegs=n1+n2+n3; opt.clear();
    auto in=[&](int x){ return x>=1&&x<=N; };
    for(int a=1;a<=N;a++){ if(n1){ Opt o; o.type=0; o.nit=2; o.it[0]=a-1; o.it[1]=N+a-1; o.lab[0]=a; opt.push_back(o); }
      for(int b=1;b<a;b++) for(int s=-1;s<=1;s+=2){ int l2=a+s*b; if(!in(l2)||(ZIG&&s>0)) continue;
        if(n2){ Opt o; o.type=1; o.nit=4; o.it[0]=a-1; o.it[1]=b-1; o.it[2]=N+a-1; o.it[3]=N+l2-1; o.lab[0]=a; o.lab[1]=l2; opt.push_back(o); }
        if(n3) for(int d=1;d<b;d++) for(int s2=-1;s2<=1;s2+=2){ int l3=l2+s2*d; if(!in(l3)||l3==a||(ZIG&&s2<0)) continue;
          Opt o; o.type=2; o.nit=6; o.it[0]=a-1; o.it[1]=b-1; o.it[2]=d-1; o.it[3]=N+a-1; o.it[4]=N+l2-1; o.it[5]=N+l3-1; o.lab[0]=a; o.lab[1]=l2; o.lab[2]=l3; opt.push_back(o); } } }
    byItem.assign(2*N,{}); for(size_t i=0;i<opt.size();i++) for(int j=0;j<opt[i].nit;j++) byItem[opt[i].it[j]].push_back(i);
    bool ok=false; lim=5000; int R=getenv("RESTARTS")?atoi(getenv("RESTARTS")):400;
    for(int r=0;r<R&&!ok;r++){ covered.assign(2*N,0); dead.assign(opt.size(),0); cnt.assign(2*N,{0,0,0}); for(size_t i=0;i<opt.size();i++) for(int j=0;j<opt[i].nit;j++) cnt[opt[i].it[j]][opt[i].type]++;
      quota[0]=n1; quota[1]=n2; quota[2]=n3; chosen.clear(); nodes=0; ok=dfs(0); if(r%20==19 && lim<2000000) lim*=2; }
    if(!ok){ printf("%d %d %d UNRESOLVED\n",n1,n2,n3); fflush(stdout); continue; }
    vector<int> L(N+1,0), D(N+1,0); bool good=true; int k[3]={0,0,0};
    for(int o:chosen){ int len=opt[o].type+1; k[len-1]++; int prev=0, prevd=N+1; for(int j=0;j<len;j++){ int x=opt[o].lab[j]; if(x<1||x>N){ good=false; break; } int d=abs(x-prev); if(d<1||d>=prevd) good=false; L[x]++; D[d]++; prev=x; prevd=d; } }
    for(int y=1;y<=N;y++) if(L[y]!=1||D[y]!=1) good=false; if(k[0]!=n1||k[1]!=n2||k[2]!=n3) good=false;
    printf("%d %d %d %s legs:",n1,n2,n3,good?"OK":"CHECK-FAILED"); for(int o:chosen){ printf(" "); for(int j=0;j<=opt[o].type;j++) printf(j?",%d":"%d",opt[o].lab[j]); } printf("\n"); fflush(stdout); } }
