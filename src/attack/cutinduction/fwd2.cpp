// Same closure C(2) as fwd.cpp (clean steps that open one or two gaps), with flat hash sets, for larger n.
//   fwd2 build N DIR            compute C(2) at every size <= N, print counts, dump the sets for sizes N-1 and N to DIR/c2_<n>.bin
//   fwd2 final N DIR part parts read DIR/c2_<N-1>.bin and DIR/c2_<N-2>.bin, generate the size-N members from a slice of the sources,
//                               and write the canonical forms of the tree shapes reached to DIR/trees_<N>_<part>.txt
#include "enum.h"
struct Flat { vector<u64> t; u64 mask; size_t cnt=0; Flat(int bits=10){ t.assign((size_t)1<<bits,0); mask=((u64)1<<bits)-1; }
  static u64 h(u64 x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }
  void grow(){ vector<u64> o; o.swap(t); t.assign(o.size()*2,0); mask=t.size()-1; cnt=0; for(u64 x:o) if(x) ins(x); }
  bool ins(u64 x){ if(cnt*2>t.size()) grow(); u64 i=h(x)&mask; while(t[i]){ if(t[i]==x) return false; i=(i+1)&mask; } t[i]=x; cnt++; return true; } };
template<class F> static void children1(const Pl&p,F f){ Pl q; int n=p.n; for(int i=0;i<=n;i++) for(int d=-1;d<=1;d+=2) if(insertLeaf(p,i,d,q)) f(q); }
template<class F> static void children2(const Pl&p,F f){ Pl q; int n=p.n;
  for(int g1=0;g1<=n;g1++) for(int g2=g1;g2<=n;g2++){ q.n=n+2; int last=0; bool ok=true; bool have[24]={0};
    for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; a+=(a>g1)+(a>g2); b+=(b>g1)+(b>g2); int len=b-a; if(len<=last){ ok=false; break; } last=len; have[len]=1; q.pos[len]=a; }
    if(!ok) continue; int fr[2],nf=0; for(int k=1;k<=n+1;k++) if(!have[k]){ if(nf<2) fr[nf]=k; nf++; } if(nf!=2) continue;
    int L1=g1+1, L2=g2+2; int c1[4]={L1-fr[0],L1,L2-fr[0],L2}, c2[4]={L1-fr[1],L1,L2-fr[1],L2};
    for(int a=0;a<4;a++){ int p1=c1[a]; if(p1<1||p1+fr[0]>n+2) continue; for(int b=0;b<4;b++){ int p2=c2[b]; if(p2<1||p2+fr[1]>n+2) continue;
      q.pos[fr[0]]=p1; q.pos[fr[1]]=p2; if(isGrowth(q)) f(q); } } } }
static void dump(const Flat&s,const string&fn){ FILE*f=fopen(fn.c_str(),"wb"); for(u64 x:s.t) if(x) fwrite(&x,8,1,f); fclose(f); }
static vector<u64> load(const string&fn){ vector<u64> v; FILE*f=fopen(fn.c_str(),"rb"); if(!f){ fprintf(stderr,"missing %s\n",fn.c_str()); exit(1);} u64 x; while(fread(&x,8,1,f)==1) v.push_back(x); fclose(f); sort(v.begin(),v.end()); return v; }
int main(int argc,char**argv){ string mode=argv[1]; int N=atoi(argv[2]); string dir=argv[3];
  if(mode=="build"){ vector<Flat> C(N+3); { Pl p; p.n=2; p.pos[1]=1; C[2].ins(enc(p)); }
    for(int n=2;n<=N;n++){ set<string> T; for(u64 x:C[n].t) if(x) T.insert(canon(dec(x,n))); printf("n=%d C(2) placements=%zu trees=%zu\n",n,C[n].cnt,T.size()); fflush(stdout);
      if(n>=N-1) dump(C[n],dir+"/c2_"+to_string(n)+".bin"); if(n==N) break;
      for(u64 x:C[n].t) if(x){ Pl p=dec(x,n); children1(p,[&](const Pl&q){ C[n+1].ins(enc(q)); }); if(n+2<=N) children2(p,[&](const Pl&q){ C[n+2].ins(enc(q)); }); }
      if(n>=3) { vector<u64>().swap(C[n-1].t); } } }
  else { int part=atoi(argv[4]), parts=atoi(argv[5]); vector<u64> A=load(dir+"/c2_"+to_string(N-1)+".bin"), B=load(dir+"/c2_"+to_string(N-2)+".bin");
    vector<u64> cache((size_t)1<<26,0); set<string> T; long gen=0, can=0;
    auto visit=[&](const Pl&q){ gen++; u64 e=1469598103934665603ULL; for(int k=1;k<q.n;k++) e=(e^(u64)q.pos[k])*1099511628211ULL;   /* 64-bit hash: positions may need 5 bits at n=17; a collision can only lose a placement, never add one */ u64 i=Flat::h(e)&(cache.size()-1); if(cache[i]==e) return; cache[i]=e; can++; T.insert(canon(q)); };
    for(size_t i=part;i<A.size();i+=parts) children1(dec(A[i],N-1),visit);
    for(size_t i=part;i<B.size();i+=parts) children2(dec(B[i],N-2),visit);
    FILE*f=fopen((dir+"/trees_"+to_string(N)+"_"+to_string(part)+".txt").c_str(),"w"); for(auto&s:T) fprintf(f,"%s\n",s.c_str()); fclose(f);
    printf("final n=%d part %d/%d: sources %zu + %zu, generated %ld (canonised %ld), tree shapes reached by this slice: %zu\n",N,part,parts,A.size(),B.size(),gen,can,T.size()); }
}
