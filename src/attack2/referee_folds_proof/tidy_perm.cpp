// tidy.cpp -- TIDIEST growth placement of a tree: fewest non-staircase steps.   (line "folds", see REPORT.txt)
//
// Cells 1..n.  A growth placement is built longest bracket first; with t cells unused the next bracket has length t
// and joins a fresh (unused) cell x to a used cell y, |x-y| = t (README Lemma 10).  The first bracket {1,n} is not a step.
// A "run" is a maximal interval of unused cells; the MAIN run is the longest one (leftmost on ties, as src/fold_stats.py).
// Let R be the run containing x and let r = number of cells of R that are NOT under the bracket x..y  ("left behind").
//   cost A (default): the step is a STAIRCASE step iff R is the main run and r = 0
//                     (x is an end cell of the main run and y lies beyond its other end).
//   cost B (MODE=B) : the step is a staircase step iff r = 0 (the same for any run; no tie-break is involved).
// cost of a placement = number of steps that are not staircase steps.  tidy(T) = minimum over growth placements of T.
//
// Search: iterative deepening on the budget K = 0,1,2,...; for each K a complete depth-first search over
// longest-first builds (every root edge up to symmetry, interchangeable pending branches tried once), with a
// transposition table of failed states.  A state is (set of used cells, multiset of (cell, shape of pending branch)).
// "exhausted" at K: no placement of cost <= K exists.  "limit": the node cap was hit (undecided).
// Output per tree:  lb ub  (exact iff lb == ub)  and a labeling of cost ub, re-verified from the definition by
// verifyCost() (which shares no code with the search) and again by verify.py.
//
// Usage: tidy [nodeLimit=2000000] [timePerTreeSec=60] < trees      (one tree per line: "u v u v ..." 0-based)
//   nodeLimit is per budget K, shared equally among the root edges (but at least MINROOT=20000 nodes per root edge).
// Env:   MODE=A|B     SEED=..   TT=log2 table size (default 21)   KMAX=..   QUIET=1 (no labels)
//        HEUR=1  large-n mode: prove the lower bound only while cheap, then look for upper bounds with restarts.
//        BEAM=W  beam mode for upper bounds (KB = largest cost kept, default 24; T0 = cells left when the exact tail
//                search takes over, default 0 = beam to the end, TAILCAP nodes per state; RO = free-run cap, default 40); see beamSolve().
//        RULE=<bitmask>  restrict the vocabulary of steps (see allowedRule());  FREE=1  ignore cost, only ask whether a
//        placement obeying RULE exists ('ub=NONE exact=1' means: exhaustively none).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 M;
typedef unsigned long long u64;
static inline u64 mix(u64 x){ x+=0x9e3779b97f4a7c15ULL; x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL; x=(x^(x>>27))*0x94d049bb133111ebULL; return x^(x>>31); }
u64 treeSalt=0; bool FREE=false; int n; vector<int> adj[128], sid[128]; int lab[128], pend[128]; M U; int MODE=0, RULE=0; mt19937_64 rng(12345);
long long nodes, lim, attemptNodes; int KMAX=120; u64 hF1, hF2; long long MINROOT=20000; bool NOPRUNE=false;
struct Ent{ u64 a,b; signed char v; }; vector<Ent> TT; u64 TTmask;
map<string,int> shapeIds;
string encSub(int v,int pa){ vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(encSub(u,v)); sort(ch.begin(),ch.end()); string r="("; for(auto&c:ch) r+=c; return r+")"; }
void prepIds(){ shapeIds.clear(); for(int u=0;u<n;u++){ sid[u].clear(); for(int w:adj[u]){ string e=encSub(w,u); auto it=shapeIds.find(e); int id; if(it==shapeIds.end()){ id=shapeIds.size()+1; shapeIds[e]=id; } else id=it->second; sid[u].push_back(id); } } }
static inline u64 pk1(int cell,int shape){ return mix((u64)cell*100003ULL+shape); }
static inline u64 pk2(int cell,int shape){ return mix((u64)cell*7919ULL+shape*1000003ULL+12345); }
// ---- step classification -------------------------------------------------------------------------------------
int rlo[130], rhi[130], mlo, mhi;
void scanRuns(){ mlo=0; mhi=-1; int i=1;
  while(i<=n){ if(!((U>>i)&1)){ int j=i; while(j<n && !((U>>(j+1))&1)) j++; for(int k=i;k<=j;k++){ rlo[k]=i; rhi[k]=j; } if(j-i>mhi-mlo){ mlo=i; mhi=j; } i=j+1; } else i++; } }
static inline void rc(int x,int y,int&r,int&c){ if(y>x){ r=x-rlo[x]; c=rhi[x]-x; } else { r=rhi[x]-x; c=x-rlo[x]; } }
static inline int stepCost(int x,int y){ if(FREE) return 0; int r,c; rc(x,y,r,c); bool inM=(rlo[x]==mlo); return (r==0 && (MODE==1 || inM))?0:1; }
// ---- RULE: restricted vocabularies ("single-cell hole" normal forms) ---------------------------------------------
// With RULE != 0 the unused cells are: the GAP (one run, the remnant of the original interval 2..n-1; age 0) and
// HOLES (isolated single cells, each created by a skip; age = time of creation).  Steps:
//   S  staircase : x an end cell of the gap, y beyond the other end of the gap
//   K  skip      : x one cell in from an end of the gap; the end cell it jumps over becomes a hole.
//                  "across" if y lies beyond the far end of the gap (r = 1), "back" otherwise (c = 1, r > 1)
//   B  back      : x an end cell of the gap, y on x's own side (gap of >= 2 cells)
//   F  fill      : x a hole
// bit 0 (1)  : always set when RULE != 0 (holes are single cells)
// bit 1 (2)  : skips must be across
// bit 2 (4)  : no back step B
// bit 3 (8)  : FIFO  - only the oldest hole may be filled
// bit 4 (16) : LIFO  - only the newest hole may be filled
// bit 5 (32) : ENDS  - only the leftmost or the rightmost hole may be filled
// bit 6 (64) : at most MAXH holes open at any time (env MAXH)
int age[130]; int MAXH=1000, nh=0;
// returns -1 if not allowed, 0 if allowed with no new hole, else the cell that becomes a hole
int allowedRule(int x,int y){ int r,c; rc(x,y,r,c);
  if(age[x]==0){
    if(r>=1 && c>=1){ int hole; if(r==1) hole=(y>x)? x-1 : x+1; else if(c==1){ if(RULE&2) return -1; hole=(y>x)? x+1 : x-1; } else return -1;
      if((RULE&64) && nh>=MAXH) return -1; return hole; }
    if(c==0 && r>=1 && (RULE&4)){ if(getenv("PERM") && r==1){ if((RULE&64) && nh>=MAXH) return -1; return (y>x)? x-1 : x+1; } return -1; }  // referee: PERM=1 reads a 2-cell-gap back step as an across K1
    return 0; }
  if(RULE&8){ for(int z=1;z<=n;z++) if(!((U>>z)&1) && age[z] && age[z]<age[x]) return -1; }
  if(RULE&16){ for(int z=1;z<=n;z++) if(!((U>>z)&1) && age[z]>age[x]) return -1; }
  if(RULE&32){ bool l=false,rr=false; for(int z=1;z<x;z++) if(!((U>>z)&1) && age[z]) l=true; for(int z=x+1;z<=n;z++) if(!((U>>z)&1) && age[z]) rr=true; if(l&&rr) return -1; }
  return 0; }
struct Mv{ int c; u64 rk; int u,w,x,hole; };
int dfs(int t,int budget){
  if(t==0) return 1;
  if(++nodes>lim) return -1;
  u64 ka=mix((u64)U ^ hF1) ^ mix((u64)(U>>64)+0x1234567ULL) ^ treeSalt, kb=mix((u64)(U>>64) ^ hF2 ^ 0xabcdefULL) + mix((u64)U*3+1);
  if(RULE){ u64 h=0; for(int z=1;z<=n;z++) if(!((U>>z)&1)){ int a=age[z]; if(!(RULE&24)) a=a?1:0; h=mix(h+a*131+z); } ka^=h; kb+=mix(h); }
  Ent &e=TT[ka&TTmask]; if(e.a==ka && e.b==kb && e.v>=budget) return 0;
  scanRuns();
  if(!NOPRUNE){ // sound dead-state tests (REPORT.txt section 1)
    // (P1) a pending vertex at cell y gets each remaining child on an unused cell within distance t of y
    // (P2) cost A, budget 0, no RULE: only staircase steps remain.  While the main run stays the main run they hit
    //      the cells mhi-t, mhi-t+1, ... on the left and mlo+t, mlo+t-1, ... on the right, so a pending vertex
    //      outside [mhi-t, mlo+t] must wait until another run can become the main run, i.e. until at most
    //      T2 = t - (mainlen - m2) cells are unused (m2 = longest other run); same count with radius T2.
    int T2=t; bool p2=(budget==0 && MODE==0 && !RULE && !FREE);
    if(p2){ int m2=0; int i=1; while(i<=n){ if(!((U>>i)&1)){ int j=rhi[i]; if(i!=mlo) m2=max(m2,j-i+1); i=j+1; } else i++; } int ml=mhi-mlo+1; if(ml>m2) T2=t-(ml-m2); }
    M un=~U & ((((M)1)<<(n+1))-2);
    for(int u=0;u<n;u++) if(lab[u] && pend[u]){ int y=lab[u]; int rad=t; if(p2 && (y<mhi-t || y>mlo+t)) rad=T2;
      int a=max(1,y-rad), b=min(n,y+rad); M w=un & ((((M)1)<<(b+1))-(((M)1)<<a)); int cnt=__builtin_popcountll((u64)w)+__builtin_popcountll((u64)(w>>64));
      if(cnt<pend[u]){ if(!(e.a==ka && e.b==kb) || e.v<budget){ e.a=ka; e.b=kb; e.v=(signed char)min(budget,120); } return 0; } } }
  Mv mv[512]; int c=0;
  for(int u=0;u<n;u++) if(lab[u] && pend[u]){
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*t; if(x<1||x>n||((U>>x)&1)) continue; int cst=stepCost(x,lab[u]); if(cst>budget) continue; int hole=0; if(RULE){ hole=allowedRule(x,lab[u]); if(hole<0) continue; }
      int seen[128], ns=0; for(size_t i=0;i<adj[u].size();i++){ int w=adj[u][i]; if(lab[w]) continue; int id=sid[u][i]; bool dup=false; for(int k=0;k<ns;k++) if(seen[k]==id){dup=true;break;} if(dup) continue; seen[ns++]=id;
        if(c<512){ mv[c].c=cst; mv[c].rk=rng(); mv[c].u=u; mv[c].w=w; mv[c].x=x; mv[c].hole=hole; c++; } } } }
  sort(mv,mv+c,[](const Mv&a,const Mv&b){ return a.c!=b.c? a.c<b.c : a.rk<b.rk; });
  int res=0;
  for(int i=0;i<c;i++){ int u=mv[i].u,w=mv[i].w,x=mv[i].x; u64 s1=hF1,s2=hF2;
    lab[w]=x; U|=((M)1)<<x; pend[u]--; int pw=0; int sav=age[x]; if(mv[i].hole){ age[mv[i].hole]=n-t; nh++; } if(sav) nh--;
    for(size_t k=0;k<adj[u].size();k++) if(adj[u][k]==w){ hF1-=pk1(lab[u],sid[u][k]); hF2-=pk2(lab[u],sid[u][k]); break; }
    for(size_t k=0;k<adj[w].size();k++) if(adj[w][k]!=u){ pw++; hF1+=pk1(x,sid[w][k]); hF2+=pk2(x,sid[w][k]); }
    pend[w]=pw;
    int r = dfs(t-1,budget-mv[i].c);
    if(r==1) return 1;
    lab[w]=0; U&=~(((M)1)<<x); pend[u]++; pend[w]=0; hF1=s1; hF2=s2; if(mv[i].hole){ age[mv[i].hole]=0; nh--; } if(sav) nh++; age[x]=sav;
    if(r<0){ res=-1; break; } }
  if(res==0){ if(!(e.a==ka && e.b==kb) || e.v<budget){ e.a=ka; e.b=kb; e.v=(signed char)min(budget,120); } }
  return res; }
vector<pair<int,int>> roots;
void prepRoots(){ roots.clear(); set<pair<int,int>> seenRoot;
  for(int u=0;u<n;u++) for(size_t i=0;i<adj[u].size();i++){ int w=adj[u][i]; int a=sid[u][i], b=0; for(size_t k=0;k<adj[w].size();k++) if(adj[w][k]==u) b=sid[w][k]; if(seenRoot.insert({a,b}).second) roots.push_back({u,w}); } }
int runRoot(pair<int,int> ed,int K,long long L){ lim=L; memset(lab,0,sizeof lab); memset(pend,0,sizeof pend); memset(age,0,sizeof age); nh=0; int u=ed.first,w=ed.second; lab[u]=1; lab[w]=n; U=(((M)1)<<1)|(((M)1)<<n); hF1=hF2=0;
    for(int z:{u,w}){ int o=(z==u?w:u); for(size_t k=0;k<adj[z].size();k++) if(adj[z][k]!=o){ pend[z]++; hF1+=pk1(lab[z],sid[z][k]); hF2+=pk2(lab[z],sid[z][k]); } }
    nodes=0; int r=dfs(n-2,K); attemptNodes+=nodes; return r; }
// one attempt at budget K over all root edges; 1 found, 0 exhausted, -1 limit hit somewhere
int attempt(int K,long long L){ vector<pair<int,int>> es=roots; shuffle(es.begin(),es.end(),rng); bool hit=false; attemptNodes=0; long long per=max(MINROOT,L/(long long)es.size());
  for(auto ed:es){ int r=runRoot(ed,K,per); if(r==1) return 1; if(r<0) hit=true; }
  return hit?-1:0; }
// ---- independent verification from the definition, and cost by replay -------------------------------------------
int verifyCost(const vector<int>&f,const vector<pair<int,int>>&edges,int mode){ // returns cost, or -1 if not a growth placement
  int N=f.size(); vector<int> seen(N+2,0); for(int v=0;v<N;v++){ if(f[v]<1||f[v]>N||seen[f[v]]) return -1; seen[f[v]]=1; }
  if((int)edges.size()!=N-1) return -1; vector<pair<int,int>> byLen(N,{0,0}); for(auto&e:edges){ int a=f[e.first],b=f[e.second]; int d=abs(a-b); if(d<1||d>N-1||byLen[d].first) return -1; byLen[d]={min(a,b),max(a,b)}; }
  if(byLen[N-1]!=make_pair(1,N)) return -1; vector<int> used(N+2,0); used[1]=used[N]=1; int cost=0;
  for(int t=N-2;t>=1;t--){ int a=byLen[t].first,b=byLen[t].second; if(used[a]==used[b]) return -1; int x=used[a]?b:a, y=used[a]?a:b;
    int cnt=0; for(int i=1;i<=N;i++) if(!used[i]) cnt++; if(cnt!=t) return -1;
    int bl=0,bh=-1; int i=1; while(i<=N){ if(!used[i]){ int j=i; while(j<N&&!used[j+1]) j++; if(j-i>bh-bl){ bl=i; bh=j; } i=j+1; } else i++; }
    int lo=x,hi=x; while(lo>1&&!used[lo-1]) lo--; while(hi<N&&!used[hi+1]) hi++;
    int r = (y>x)? x-lo : hi-x; bool stair = (r==0) && (mode==1 || lo==bl); if(!stair) cost++; used[x]=1; }
  return cost; }
// ---- BEAM mode (upper bounds for large n) --------------------------------------------------------------------------
// Layer by layer (one bracket per layer) keep, for every number g <= KB of non-staircase steps made so far, the BW
// partial builds of cost g that look best; "best" = (i) longest FREE RUN: the smallest number of unused cells that
// staircase steps alone can reach from the state (depth-first, at most RO nodes), then (ii) fewest pending children
// on vertices that staircase steps in the current main run can no longer reach, then at random.  All root edges
// With VOC=1 the non-staircase steps of the beam are restricted to single-cell skips (K1, K1*), back steps B and fills
// of single-cell holes (VOC=2: K1, B, F only); this narrows the beam's branching, the bound stays a valid upper bound.
// start in layer 0.  When T0 cells are left the beam stops and every kept state is COMPLETED by the complete search
// dfs() above, budget by budget (total budget B = 0,1,2,...; a state of cost g gets budget B-g), so the tail of the
// build is optimal for the prefixes kept (up to the node cap per state).  A free run that reaches the end is itself
// a complete build.  The result is an UPPER bound only.
struct St{ unsigned char lab[104]; M U; u64 hF; int g; int h; u64 rk; };
int VOC=0; int BW=0, KB=24, T0=0; long long RO=40, TAILCAP=3000;
int frLab[130]; M frU; long long frNodes, frCap; int frBest; bool frDone; int frSol[130];
static inline int costOf(M Ux,int x,int y,int ml){ int lo=x,hi=x; while(lo>1&&!((Ux>>(lo-1))&1)) lo--; while(hi<n&&!((Ux>>(hi+1))&1)) hi++; int r=(y>x)? x-lo : hi-x; return (r==0 && (MODE==1 || lo==ml))?0:1; }
static inline void mainRun(M Ux,int&ml,int&mh){ ml=0; mh=-1; int i=1; while(i<=n){ if(!((Ux>>i)&1)){ int j=i; while(j<n && !((Ux>>(j+1))&1)) j++; if(j-i>mh-ml){ ml=i; mh=j; } i=j+1; } else i++; } }
void freeRun(int t){ if(t<frBest) frBest=t; if(t==0){ frDone=true; memcpy(frSol,frLab,sizeof(int)*n); return; } if(++frNodes>frCap) return;
  int ml,mh; mainRun(frU,ml,mh);
  for(int u=0;u<n && !frDone;u++) if(frLab[u]){ int y=frLab[u]; for(int sg=-1;sg<=1;sg+=2){ int x=y+sg*t; if(x<1||x>n||((frU>>x)&1)) continue; if(costOf(frU,x,y,ml)) continue;
      int seenS[128], ns=0; for(size_t i=0;i<adj[u].size();i++){ int w=adj[u][i]; if(frLab[w]) continue; int id=sid[u][i]; bool dup=false; for(int q=0;q<ns;q++) if(seenS[q]==id){dup=true;break;} if(dup) continue; seenS[ns++]=id;
        frLab[w]=x; frU|=((M)1)<<x; freeRun(t-1); if(frDone) return; frLab[w]=0; frU&=~(((M)1)<<x); if(frNodes>frCap) return; } } } }
// returns ub (or -1) and fills best
int beamSolve(vector<int>&best,double tl,long long tailCap,const function<double()>&el){ int ub=-1, kmax=KB;
  vector<St> cur; for(auto ed:roots){ int u=ed.first,w=ed.second; St s; memset(&s,0,sizeof s); s.lab[u]=1; s.lab[w]=n; s.U=(((M)1)<<1)|(((M)1)<<n); for(int z:{u,w}){ int o=(z==u?w:u); for(size_t k=0;k<adj[z].size();k++) if(adj[z][k]!=o) s.hF+=pk1(s.lab[z],sid[z][k]); } cur.push_back(s); }
  int t=n-2;
  for(;t>=1 && t>T0 && !cur.empty();t--){ vector<St> nxt; unordered_map<u64,int> seen;
    for(const St&s:cur){ int ml,mh; mainRun(s.U,ml,mh);
      for(int u=0;u<n;u++) if(s.lab[u]){ int np=0; for(int w:adj[u]) if(!s.lab[w]) np++; if(!np) continue; int y=s.lab[u];
        for(int sg=-1;sg<=1;sg+=2){ int x=y+sg*t; if(x<1||x>n||((s.U>>x)&1)) continue; int cst=costOf(s.U,x,y,ml); if(s.g+cst>kmax) continue;
          if(VOC && cst){ int lo=x,hi=x; while(lo>1&&!((s.U>>(lo-1))&1)) lo--; while(hi<n&&!((s.U>>(hi+1))&1)) hi++; int r=(y>x)? x-lo : hi-x, c2=(hi-lo)-r;
            if(lo==ml){ if(!(c2==0 || r==1 || (c2==1 && VOC==1))) continue; } else if(lo!=hi) continue; }
          int seenS[128], ns=0; for(size_t i=0;i<adj[u].size();i++){ int w=adj[u][i]; if(s.lab[w]) continue; int id=sid[u][i]; bool dup=false; for(int k=0;k<ns;k++) if(seenS[k]==id){dup=true;break;} if(dup) continue; seenS[ns++]=id;
            St c=s; c.lab[w]=x; c.U|=((M)1)<<x; c.g=s.g+cst; c.hF-=pk1(y,id); for(size_t k=0;k<adj[w].size();k++) if(adj[w][k]!=u) c.hF+=pk1(x,sid[w][k]);
            u64 key=mix((u64)c.U ^ c.hF) ^ mix((u64)(c.U>>64)+77);
            auto it=seen.find(key); if(it!=seen.end()){ if(nxt[it->second].g>c.g){ c.h=nxt[it->second].h; c.rk=nxt[it->second].rk; nxt[it->second]=c; } continue; }
            int t1=t-1; int cml,cmh; mainRun(c.U,cml,cmh); M un1=~c.U & ((((M)1)<<(n+1))-2); bool dead=false; int h=0;
            for(int q=0;q<n && !dead;q++) if(c.lab[q]){ int pq=0; for(int w2:adj[q]) if(!c.lab[w2]) pq++; if(!pq) continue; int yy=c.lab[q];
              int a=max(1,yy-t1), b=min(n,yy+t1); M wd=un1 & ((((M)1)<<(b+1))-(((M)1)<<a)); int cnt=__builtin_popcountll((u64)wd)+__builtin_popcountll((u64)(wd>>64)); if(cnt<pq) dead=true;
              if(t1>0 && (yy<cmh-t1 || yy>cml+t1)) h+=pq; }
            if(dead) continue; c.h=h; c.rk=rng();
            if(RO>0 && t1>0){ for(int q=0;q<n;q++) frLab[q]=c.lab[q]; frU=c.U; frNodes=0; frCap=RO; frBest=t1; frDone=false; freeRun(t1);
              if(frDone && (ub<0 || c.g<ub)){ ub=c.g; best.assign(frSol,frSol+n); kmax=ub-1; }
              c.h = frBest*1000 + c.h; }
            seen[key]=nxt.size(); nxt.push_back(c); } } } }
    if(kmax<0) return ub;
    sort(nxt.begin(),nxt.end(),[](const St&a,const St&b){ if(a.g!=b.g) return a.g<b.g; if(a.h!=b.h) return a.h<b.h; return a.rk<b.rk; });
    cur.clear(); int cg=-1, cnt=0; for(const St&s:nxt){ if(s.g>kmax) break; if(s.g!=cg){ cg=s.g; cnt=0; } if(cnt<BW){ cur.push_back(s); cnt++; } } }
  // exact completion of the kept states
  for(int B=0; (ub<0 || B<ub) && B<=kmax+T0 && el()<tl; B++){
    for(const St&s:cur){ if(s.g>B) break; if(el()>tl) break;
      memset(lab,0,sizeof lab); memset(pend,0,sizeof pend); memset(age,0,sizeof age); nh=0; for(int q=0;q<n;q++) lab[q]=s.lab[q]; U=s.U; hF1=hF2=0;
      for(int q=0;q<n;q++) if(lab[q]) for(size_t k=0;k<adj[q].size();k++) if(!lab[adj[q][k]]){ pend[q]++; hF1+=pk1(lab[q],sid[q][k]); hF2+=pk2(lab[q],sid[q][k]); }
      lim=tailCap; nodes=0; int r=dfs(t,B-s.g); if(r==1){ ub=B; best.assign(lab,lab+n); break; } } }
  return ub; }
int main(int argc,char**argv){ long long L0= argc>1? atoll(argv[1]) : 2000000; double tl= argc>2? atof(argv[2]) : 60;
  if(getenv("MODE")&&getenv("MODE")[0]=='B') MODE=1; if(getenv("FREE")) FREE=true; if(getenv("SEED")) rng.seed(atoll(getenv("SEED")));
  if(getenv("RULE")){ RULE=atoi(getenv("RULE")); if(RULE) RULE|=1; } if(getenv("MAXH")){ MAXH=atoi(getenv("MAXH")); RULE|=65; } if(getenv("NOPRUNE")) NOPRUNE=true; if(getenv("BEAM")) BW=atoi(getenv("BEAM")); if(getenv("KB")) KB=atoi(getenv("KB")); if(getenv("T0")) T0=atoi(getenv("T0")); if(getenv("RO")) RO=atoll(getenv("RO")); if(getenv("VOC")) VOC=atoi(getenv("VOC")); if(getenv("TAILCAP")) TAILCAP=atoll(getenv("TAILCAP")); if(getenv("MINROOT")) MINROOT=atoll(getenv("MINROOT"));
  int ttb= getenv("TT")? atoi(getenv("TT")) : 21; TT.assign((size_t)1<<ttb,Ent{0,0,-1}); TTmask=((u64)1<<ttb)-1; KMAX= getenv("KMAX")? atoi(getenv("KMAX")) : 120; if(FREE) KMAX=0; bool quiet=getenv("QUIET"), heur=getenv("HEUR");
  string line; long long idx=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); vector<pair<int,int>> edges; int u,v,mx=0; while(is>>u>>v){ edges.push_back({u,v}); mx=max(mx,max(u,v)); }
    n=mx+1; for(int i=0;i<n;i++) adj[i].clear(); for(auto&e:edges){ adj[e.first].push_back(e.second); adj[e.second].push_back(e.first); }
    prepIds(); prepRoots(); treeSalt=mix(idx*2654435761ULL+17);
    auto t0=chrono::steady_clock::now(); auto el=[&]{ return chrono::duration<double>(chrono::steady_clock::now()-t0).count(); };
    int lb=0, ub=-1; bool chain=true; vector<int> best; long long totnodes=0;
    if(BW){ // BEAM mode: lower bound while cheap (as HEUR), then beam + exact tails; the rest of the time: restarts with new seeds
      for(int K=0;K<=KMAX;K++){ int r=attempt(K,L0); totnodes+=attemptNodes; if(r==1){ ub=K; best.assign(lab,lab+n); break; } if(r==0) lb=K+1; else break; }
      function<double()> elf=el; int rs=0;
      while(ub!=lb && (rs==0 || el()<tl)){ vector<int> b2; int savK=KB; if(ub>=0) KB=min(KB,ub-1); int r=beamSolve(b2,tl,TAILCAP,elf); KB=savK; rs++; if(r>=0 && (ub<0 || r<ub)){ ub=r; best=b2; } if(getenv("ONEPASS")) break; }
    } else if(!heur){
      // phase 1: climb K with the base limit
      for(int K=0;K<=KMAX && ub<0;K++){ int r=attempt(K,L0); totnodes+=attemptNodes; if(r==1){ ub=K; best.assign(lab,lab+n); } else if(r==0){ if(chain) lb=K+1; } else chain=false; }
      // phase 2: growing limits on the undecided budgets
      long long L=L0;
      while(ub>lb && el()<tl){ L*=4;
        { int r=attempt(lb,L); totnodes+=attemptNodes; if(r==1){ ub=lb; best.assign(lab,lab+n); break; } else if(r==0){ lb++; L=max(L0,L/4); continue; } }
        if(ub>lb && el()<tl){ int r=attempt(ub-1,L); totnodes+=attemptNodes; if(r==1){ ub--; best.assign(lab,lab+n); } else if(r==0){ lb=ub; } } }
      while(ub<0 && !(FREE&&chain&&lb>0) && el()<tl){ L*=4; int K=FREE?0:n; int r=attempt(K,L); totnodes+=attemptNodes; if(r==1){ ub=K; best.assign(lab,lab+n); if(!FREE) ub=verifyCost(best,edges,MODE); } else if(r==0){ lb=K+1; chain=true; break; } }
    } else {
      // HEUR: (a) lower bound while cheap: budget K exhausted over all roots within L0 nodes in total
      for(int K=0;K<=KMAX;K++){ int r=attempt(K,L0); totnodes+=attemptNodes; if(r==1){ ub=K; best.assign(lab,lab+n); break; } if(r==0) lb=K+1; else break; }
      // (b) upper bound: rounds of restarts; in round j every budget K >= lb gets `per` nodes on each of a few random roots
      long long per=max(MINROOT,L0/50); int K=lb; double tlb=tl;
      while(ub<0 && el()<tlb){ // climbing: several short tries at K, then K+1 ...
        bool found=false; for(int rep=0;rep<12 && !found;rep++){ attemptNodes=0; int r=runRoot(roots[rng()%roots.size()],K,per); totnodes+=attemptNodes; if(r==1){ found=true; ub=K; best.assign(lab,lab+n); } }
        if(!found){ K++; if(K>n){ K=lb; per*=2; } } }
      // (c) descend: try to beat ub with the rest of the time, restarts of growing size
      long long p2=per;
      while(ub>lb && el()<tl){ bool found=false; for(int rep=0;rep<12 && !found && el()<tl;rep++){ attemptNodes=0; int r=runRoot(roots[rng()%roots.size()],ub-1,p2); totnodes+=attemptNodes; if(r==1){ found=true; ub--; best.assign(lab,lab+n); } }
        if(!found) p2*=2; }
    }
    if(ub<0){ printf("T %lld n=%d lb=%d ub=NONE exact=%d nodes=%lld time=%.1f\n",idx,n,lb,(int)(FREE&&chain&&lb>0),totnodes,el()); idx++; fflush(stdout); continue; }
    int vc=verifyCost(best,edges,MODE); if(vc<0 || (!FREE && vc>ub)){ printf("VERIFY-FAIL tree %lld (vc=%d ub=%d)\n",idx,vc,ub); return 1; }
    if(!FREE && vc<ub){ if(lb==ub){ printf("VERIFY-FAIL tree %lld: cost %d below a proved lower bound %d\n",idx,vc,lb); return 1; } ub=vc; } // a build found with budget K may cost less than K when smaller budgets were not exhausted
    printf("T %lld n=%d lb=%d ub=%d exact=%d nodes=%lld time=%.1f",idx,n,lb,ub,(int)(lb==ub),totnodes,el()); if(!quiet){ printf(" labels:"); for(int i=0;i<n;i++) printf(" %d",best[i]); } printf("\n"); fflush(stdout); idx++; }
  return 0; }
