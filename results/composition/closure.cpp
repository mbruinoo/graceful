// CLOSURE OF THE COMPOSITION RULES (see REPORT.md).  D_n = set of growth placements on n vertices derived from
// staircases by the rules switched on.  Every placement put into D_n is re-checked against the definition.
//
//   closure N [P=1] [NEST=0|1|2] [BLK=0|1|2] [dumpdir]
//     P    : 1 = run filling (Rule P) on.                 (complement, Rule C, is always on)
//     NEST : 0 off, 1 = only single-leaf insertion (README Lemma 8), 2 = full clean-cut nesting (Rule N)
//     (5th argument T: 1 = completion transplant, Rule T, on)
//     BLK  : 0 off, 1 = mirror-window designs only (Rule D, the growth Delta-construction), 2 = all block designs (Rule B)
#include "common.h"
int NMAX; int useP=1,useN=0,useB=0,useT=0;
vector<P> Dl[18]; unordered_set<P> Ds[18];
// provenance (only kept when a derivation is asked for with the environment variable TRACE)
struct Prov { char rule; int n1; P p1; int n2; P p2; int a,b; };
bool tracing=false; unordered_map<P,Prov> prov[18]; Prov cur;
vector<P> TL[18][18];      // TL[j][g]: truncated placements (brackets j..j+g-1 on labels {0} u [j,j+g-1]), packed at index k-j+1
bool TLdone[18][18];

static void add(int n,const int*pos,vector<P>&queue){ int m=n-1;
  if(!is_growth(pos,m)){ fprintf(stderr,"BUG: non-growth output n=%d\n",n); for(int k=m;k>=1;k--) fprintf(stderr,"%d-%d ",pos[k],pos[k]+k); fprintf(stderr,"\n"); exit(1); }
  P x=packp(pos,m); if(Ds[n].insert(x).second){ Dl[n].push_back(x); queue.push_back(x); if(tracing) prov[n][x]=cur; }
  int q[16]; for(int k=1;k<=m;k++) q[k]=m-k-pos[k];            // Rule C: complement
  P y=packp(q,m); if(Ds[n].insert(y).second){ Dl[n].push_back(y); queue.push_back(y); if(tracing) prov[n][y]=Prov{'C',n,x,0,0,0,0}; } }

static void staircases(int n,vector<P>&queue){ int m=n-1; if(m==0){ return; }
  for(unsigned s=0;s<(1u<<(m-1));s++){ int pos[16]; pos[m]=0; for(int k=m-1;k>=1;k--) pos[k]=pos[k+1]+((s>>(k-1))&1); cur=Prov{'S',0,0,0,0,0,0}; add(n,pos,queue); } }

static const vector<P>& getTL(int j,int g){            // from D_{g+j}, which must be final
  if(TLdone[j][g]) return TL[j][g]; TLdone[j][g]=true; int q=g+j,m=q-1; set<P> S;
  for(P x:Dl[q]){ int pos[16]; unpackp(x,m,pos); unsigned used=0; for(int k=m;k>=j;k--) used|=(1u<<pos[k])|(1u<<(pos[k]+k));
    unsigned want=((1u<<q)-1)&~(((1u<<j)-1)&~1u);          // everything except labels 1..j-1
    if(used!=want) continue; P t=0; for(int k=j;k<=m;k++) t|=(P)pos[k]<<(4*(k-j)); S.insert(t); }
  TL[j][g].assign(S.begin(),S.end()); return TL[j][g]; }

static void nest_into(int n,vector<P>&queue){            // Rule N: outputs of size n from f in D_{n'} , n' < n
  for(int n1=2;n1<n;n1++){ int g=n-n1,m1=n1-1; if(useN==1 && g!=1) continue;
    for(size_t idx=0;idx<Dl[n1].size();idx++){ P x=Dl[n1][idx]; int pos[16],par[16],plen[16]; unpackp(x,m1,pos); growth_info(pos,m1,par,plen);
      for(int L=1;L<=m1;L++){ int c=0,mn=99; for(int k=1;k<=m1;k++) if(pos[k]<L && pos[k]+k>=L){ c++; mn=min(mn,k); }
        if(mn!=m1-c+1) continue; int j=n1-c; int u=L-j; if(u<0) continue; if(!(u==0 || plen[u]>=j)) continue;
        int base[16]; for(int k=1;k<=m1;k++){ bool jump=pos[k]<L && pos[k]+k>=L; int nk=jump?k+g:k; base[nk]= pos[k]>=L?pos[k]+g:pos[k]; }
        cur=Prov{'N',n1,x,0,0,L,j};
        if(useN==1){ base[j]=u; add(n,base,queue); continue; }
        const vector<P>&tl=getTL(j,g);
        for(P t:tl){ for(int k=j;k<j+g;k++) base[k]=u+((t>>(4*(k-j)))&15); add(n,base,queue); } } } } }

static void block_into(int n,vector<P>&queue){            // Rule B / D: outputs of size n = (p-1)t+1
  for(int t=2;t<=n-1;t++){ if((n-1)%t) continue; int p=(n-1)/t+1; if(p<2) continue; int mp=p-1;
    for(size_t idx=0;idx<Dl[p].size();idx++){ P x=Dl[p][idx]; int pos[16],par[16],plen[16]; unpackp(x,mp,pos); growth_info(pos,mp,par,plen);
      int vert[16]; // vert[j] = T-label owning block j (blocks 0..p-2)
      auto emit=[&](){ int out[16]; for(int k=1;k<=mp;k++) out[k*t]=pos[k]*t;
        for(int j=0;j<=p-2;j++) for(int d=1;d<t;d++){ int a=j*t+d,b=vert[j]*t; int len=abs(a-b); out[len]=min(a,b); }
        cur=Prov{'B',p,x,0,0,t,0}; for(int j=0;j<=p-2;j++) cur.b=cur.b*10+vert[j];
        add(n,out,queue); };
      if(useB==1){ for(int w=1;w<=p;w++){ bool ok=true; for(int j=0;j<=p-2 && ok;j++){ int k= (j>=w-1)?0:(w-1-j); vert[j]=k;
              int beta= k<=j? j-k : k-j-1; if(k!=0 && beta>=plen[k]) ok=false; }
            if(ok) emit(); } }
      else { bool usedblk[16]={0};
        function<void(int)> rec=[&](int beta){ if(beta<0){ emit(); return; }
          for(int j=0;j<=p-2;j++){ if(usedblk[j]) continue;
            int k=j-beta; if(k>=0 && (k==0 || beta<plen[k])){ usedblk[j]=1; vert[j]=k; rec(beta-1); usedblk[j]=0; }
            k=j+beta+1; if(k<=p-1 && beta<plen[k]){ usedblk[j]=1; vert[j]=k; rec(beta-1); usedblk[j]=0; } } };
        rec(p-2); } } } }

static string show(int n,P x){ int pos[16]; unpackp(x,n-1,pos); string r; for(int k=n-1;k>=1;k--){ r+=to_string(pos[k])+"-"+to_string(pos[k]+k); if(k>1) r+=" "; } return r; }
static void derivation(int n,P x,map<pair<int,P>,int>&id,int depth){ if(id.count({n,x})) return; if(n==1){ return; }
  Prov pr=prov[n][x]; if(pr.n1>1) derivation(pr.n1,pr.p1,id,depth+1); if(pr.n2>1) derivation(pr.n2,pr.p2,id,depth+1);
  int me=id.size()+1; id[{n,x}]=me; auto ref=[&](int nn,P pp){ return "#"+to_string(id[{nn,pp}]); };
  printf("  #%-3d n=%-2d  %-44s ",me,n,show(n,x).c_str());
  switch(pr.rule){ case 'S': printf("staircase"); break; case 'C': printf("C: complement of %s",ref(pr.n1,pr.p1).c_str()); break;
    case 'P': printf("P: brackets >%d of %s, run filled with %s shifted by %d",pr.a,ref(pr.n1,pr.p1).c_str(),pr.n2>1?ref(pr.n2,pr.p2).c_str():"a point",pr.b); break;
    case 'T': printf("T: brackets >%d of %s, brackets <=%d of %s",pr.a,ref(pr.n1,pr.p1).c_str(),pr.a,ref(pr.n2,pr.p2).c_str()); break;
    case 'N': printf("N: gap opened in %s before label %d, free lengths start at %d",ref(pr.n1,pr.p1).c_str(),pr.a,pr.b); break;
    case 'B': printf("B: %s multiplied by t=%d, blocks owned by labels (digits) %d",ref(pr.n1,pr.p1).c_str(),pr.a,pr.b); break; }
  printf("\n"); }
// ---- Rule T (completion transplant) ----
struct Comp { uint64_t touched; signed char rel[15]; signed char nh; P src; };
unordered_map<uint64_t,vector<Comp>> comps;            // key (k, pattern of unused labels) -> completions
unordered_set<string> compSeen; size_t compDone[18];
static void extract_comps(int nh){ int mh=nh-1;
  for(size_t&idx=compDone[nh]; idx<Dl[nh].size(); idx++){ int pos[16]; unpackp(Dl[nh][idx],mh,pos);
    unsigned used=0; for(int k=mh;k>=2;k--){ used|=(1u<<pos[k])|(1u<<(pos[k]+k)); int kk=k-1;
      unsigned un=((1u<<nh)-1)&~used; int lo=__builtin_ctz(un); Comp c; c.touched=0; string key; key.push_back((char)kk);
      for(int i=1;i<=kk;i++){ int a=pos[i],b=a+i; c.rel[i]=a-lo; key.push_back((char)(a-lo+32));
        if(!(un>>a&1)) c.touched|=1ull<<(a-lo+20); if(!(un>>b&1)) c.touched|=1ull<<(b-lo+20); }
      { unsigned pat=un>>lo; key.append((const char*)&pat,4); }      // the same brackets can add different labels: keep the pattern in the key
      if(!compSeen.insert(key).second) continue;
      c.nh=nh; c.src=Dl[nh][idx]; comps[((uint64_t)kk<<32)|(un>>lo)].push_back(c); } } }
unordered_map<P,uint32_t> frameIdx;
static bool transplant_round(int n,vector<P>&queue){ int m=n-1; size_t before=Dl[n].size(); size_t N0=Dl[n].size();
  for(size_t idx=0;idx<N0;idx++){ P x=Dl[n][idx]; int pos[16]; unpackp(x,m,pos);
    unsigned used=0; for(int k=m;k>=2;k--){ used|=(1u<<pos[k])|(1u<<(pos[k]+k)); int kk=k-1;
      unsigned un=((1u<<n)-1)&~used; int lo=__builtin_ctz(un);
      auto it=comps.find(((uint64_t)kk<<32)|(un>>lo)); if(it==comps.end()) continue;
      P frame=(x>>(4*kk))<<(4*kk) | ((P)kk<<60); uint32_t&fi=frameIdx[frame]; const vector<Comp>&v=it->second; if(fi>=v.size()) continue;
      uint64_t usedpat=0; for(int a=0;a<=m;a++) if(used>>a&1) usedpat|=1ull<<(a-lo+20);
      int out[16]; for(int i=kk+1;i<=m;i++) out[i]=pos[i];
      size_t end=v.size();
      for(size_t ci=fi;ci<end;ci++){ const Comp&c=it->second[ci]; if(c.touched&~usedpat) continue; for(int i=1;i<=kk;i++) out[i]=lo+c.rel[i]; cur=Prov{'T',n,x,c.nh,c.src,kk,0}; add(n,out,queue); }
      frameIdx[frame]=end; } }
  return Dl[n].size()>before; }

int main(int argc,char**argv){ NMAX=atoi(argv[1]); if(argc>2) useP=atoi(argv[2]); if(argc>3) useN=atoi(argv[3]); if(argc>4) useB=atoi(argv[4]); if(argc>5) useT=atoi(argv[5]);
  const char*dump= argc>6?argv[6]:nullptr;
  const char*target=getenv("TRACE"); tracing=target!=nullptr;
  auto trees=all_trees(NMAX);
  { int pos[2]={0,0}; (void)pos; Ds[1].insert(0); Dl[1].push_back(0); }
  printf("rules: C%s%s%s%s\n",useP?" P":"",useT?" T":"",useN==2?" N":useN==1?" L8":"",useB==2?" B":useB==1?" D":"");
  printf("%3s %8s %8s %8s %9s %12s  %s\n","n","trees","caterp","reached","fraction","placements","first tree not reached");
  for(int n=2;n<=NMAX;n++){ vector<P> queue; int m=n-1;
    staircases(n,queue); if(useN) nest_into(n,queue); if(useB) block_into(n,queue);
    unordered_set<P> frames; size_t qi=0; frameIdx.clear();
    for(;;){
    for(;qi<queue.size() && useP;qi++){ P x=queue[qi]; int pos[16]; unpackp(x,m,pos);
      unsigned used=0; for(int k=m;k>=2;k--){ used|=(1u<<pos[k])|(1u<<(pos[k]+k));
        int kk=k-1; // brackets > kk placed, kk labels unused
        unsigned un=((1u<<n)-1)&~used; int lo=__builtin_ctz(un); if(un!=(((1u<<kk)-1)<<lo)) continue;
        P frame=(x>>(4*kk))<<(4*kk) | ((P)kk<<60); if(!frames.insert(frame).second) continue;
        int out[16]; for(int i=kk+1;i<=m;i++) out[i]=pos[i];
        for(int off=lo-1;off<=lo;off++){ if(off<0||off+kk>m) continue;
          for(P g:Dl[kk+1]){ for(int i=1;i<=kk;i++) out[i]=off+((g>>(4*(i-1)))&15); cur=Prov{'P',n,x,kk+1,g,kk,off}; add(n,out,queue); } } } }
    if(!useT) break; extract_comps(n); if(!transplant_round(n,queue)) break; if(!useP) qi=queue.size(); }
    set<uint32_t> reached; for(P x:Dl[n]){ int pos[16]; unpackp(x,m,pos); reached.insert(canon_pos(pos,m)); }
    int cat=0; for(uint32_t c:trees[n]) if(is_caterpillar(c,n)) cat++;
    string first="-"; for(uint32_t c:trees[n]) if(!reached.count(c)){ first=paren(c,n); }   // set is increasing; keep the last = largest code
    vector<uint32_t> miss; for(uint32_t c:trees[n]) if(!reached.count(c)) miss.push_back(c);
    printf("%3d %8zu %8d %8zu %8.1f%% %12zu  %s\n",n,trees[n].size(),cat,reached.size(),100.0*reached.size()/trees[n].size(),Dl[n].size(),miss.empty()?"-":paren(miss.back(),n).c_str()); fflush(stdout);
    if(tracing && (int)strlen(target)==2*n){ for(P x:Dl[n]){ int pos[16]; unpackp(x,m,pos); if(paren(canon_pos(pos,m),n)==target){ printf("derivation of %s:\n",target); map<pair<int,P>,int> id; derivation(n,x,id,0); break; } } }
    if(dump){ FILE*f=fopen((string(dump)+"/missed"+to_string(n)+".txt").c_str(),"w"); for(uint32_t c:miss) fprintf(f,"%s\n",paren(c,n).c_str()); fclose(f);
      f=fopen((string(dump)+"/reached"+to_string(n)+".txt").c_str(),"w"); for(uint32_t c:reached) fprintf(f,"%s\n",paren(c,n).c_str()); fclose(f); }
  } }
