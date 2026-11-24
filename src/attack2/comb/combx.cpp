// combx.cpp -- exact-cover style search for all-up combs of diameter-4 trees.
//
// Setting (labels 0..m).  S = multiset of sizes of the non-root hubs (entries >= 0; a 0 is a leaf of the
// centre).  An all-up comb with w inside fillers is: y = |S| + sum(S) + w + 1, distinct hub labels h_i in
// [1,y-1], sets U_i of [1,y-1-h_i], |U_i| = s_i, and W of size w such that
//   (L) {y-h_i}, U_i, W partition [1,y-1]      (edge lengths)
//   (C) {h_i}, h_i+U_i, W partition [1,y-1]    (vertex labels)
// (Comb Lemma, src/attack/gamestrategy/REPORT.txt).  It gives a growth placement of D(a1; S) with the
// a1-hub at label 0 for EVERY a1 >= w (root leaves at W and at y+1..m).
// So "every diameter-4 tree with n <= N has an all-up comb rooted at a largest hub" is equivalent to:
//   for every S with |S| + sum(S) + max(S) + 2 <= N there is a comb with w <= max(S).
//
// Search: items are the lengths 1..y-1 and the cells 1..y-1; at each node the item with the fewest
// candidates is branched on (hub / inside filler / leaf of a placed hub / leaf of a new hub).
//
// Usage: combx N [lo] [mode] [part] [nparts]
//        combx S s1 s2 ..    one multiset, randomised tie-breaking with restarts (never returns if no comb)
//   mode 0: find any w <= max(S) (escalating node limits);  mode 1: exact least w (no node limit, w = 0,1,..)
//   env MAXLIM=L: mode 0 gives up on S after node limit L and prints 'HARD n=.. S ..' (not a counterexample:
//                 the search was cut off; such S are settled by symx or hard.py)
//   env FROM=n0: resume a run (same lo, part, nparts) at n0 without redoing smaller n
//   prints one certificate line per S:  S | w y | h:u,u,.. ; ... | W
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
static int Y;
struct St{ u64 hub,capm,unk,fc,fl,flr; int nh,nhpos,wild; signed char cap[64]; signed char cnt[64]; signed char who[64]; };
// who[len] = hub label that owns leaf length len, 0 for W, -1 hub length/unassigned
static long long nodes, limitN; static int maxSize; static St sol;
static unsigned long long rs=0; static bool rnd=false; static inline unsigned rnext(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (unsigned)(rs>>11); }
static inline u64 below(int z){ return (z>=64)?~0ull:((1ull<<z)-1); }
static inline void makeHub(St&s,int h,int sz){ u64 b=1ull<<h; s.hub|=b; s.unk&=~b; s.fc&=~b; int l=Y-h; s.fl&=~(1ull<<l); s.flr&=~(1ull<<(63-l));
  s.cap[h]=sz; if(sz>0){ s.capm|=b; s.nhpos--; } s.cnt[sz]--; s.nh--; }
static inline void assign(St&s,int l,int z,int h){ s.fl&=~(1ull<<l); s.flr&=~(1ull<<(63-l)); s.fc&=~(1ull<<z); s.unk&=~(1ull<<z); s.unk&=~(1ull<<(Y-l));
  s.who[l]=h; if(h){ if(--s.cap[h]==0) s.capm&=~(1ull<<h); } else s.wild--; }
static bool rec(const St&s){
  if(++nodes>limitN) return false;
  if(!s.fc){ sol=s; return true; }
  if(__builtin_popcountll(s.unk)<s.nh) return false;
  int best=1000, bz=-1, bkind=0; // kind 0 = cell, 1 = length
  u64 hubsrc = s.capm | (s.nhpos>0? s.unk:0);
  for(u64 t=s.fc;t;t&=t-1){ int z=__builtin_ctzll(t);
    int c=((s.unk>>z&1)&&s.nh>0) + (s.wild>0&&(s.fl>>z&1)) + __builtin_popcountll(hubsrc & (s.flr>>(63-z)) & below(z));
    if(c<best || (rnd && c==best && (rnext()&3)==0)){ best=c; bz=z; bkind=0; if(c==0) return false; } }
  for(u64 t=s.fl;t;t&=t-1){ int u=__builtin_ctzll(t);
    int c=((s.unk>>(Y-u)&1)&&s.nh>0) + (s.wild>0&&(s.fc>>u&1)) + __builtin_popcountll((hubsrc<<u) & s.fc & below(Y));
    if(c<best || (rnd && c==best && (rnext()&3)==0)){ best=c; bz=u; bkind=1; if(c==0) return false; } }
  St n;
  if(bkind==0){ int z=bz;
    u64 P=s.capm & (s.flr>>(63-z)) & below(z);
    for(u64 t=P;t;t&=t-1){ int h=__builtin_ctzll(t); n=s; assign(n,z-h,z,h); if(rec(n)) return true; if(nodes>limitN) return false; }
    if(s.wild>0&&(s.fl>>z&1)){ n=s; assign(n,z,z,0); if(rec(n)) return true; if(nodes>limitN) return false; }
    if(s.nhpos>0){ u64 Q=s.unk & (s.flr>>(63-z)) & below(z);
      for(u64 t=Q;t;t&=t-1){ int h=__builtin_ctzll(t); for(int sz=maxSize;sz>=1;sz--) if(s.cnt[sz]>0){ n=s; makeHub(n,h,sz); assign(n,z-h,z,h); if(rec(n)) return true; if(nodes>limitN) return false; } } }
    if((s.unk>>z&1)&&s.nh>0){ for(int sz=maxSize;sz>=0;sz--) if(s.cnt[sz]>0){ n=s; makeHub(n,z,sz); if(rec(n)) return true; if(nodes>limitN) return false; } }
  } else { int u=bz;
    u64 P=(s.capm<<u) & s.fc & below(Y);
    for(u64 t=P;t;t&=t-1){ int z=__builtin_ctzll(t); n=s; assign(n,u,z,z-u); if(rec(n)) return true; if(nodes>limitN) return false; }
    if(s.wild>0&&(s.fc>>u&1)){ n=s; assign(n,u,u,0); if(rec(n)) return true; if(nodes>limitN) return false; }
    if(s.nhpos>0){ u64 Q=(s.unk<<u) & s.fc & below(Y);
      for(u64 t=Q;t;t&=t-1){ int z=__builtin_ctzll(t); int h=z-u; for(int sz=maxSize;sz>=1;sz--) if(s.cnt[sz]>0){ n=s; makeHub(n,h,sz); assign(n,u,z,h); if(rec(n)) return true; if(nodes>limitN) return false; } } }
    if((s.unk>>(Y-u)&1)&&s.nh>0){ for(int sz=maxSize;sz>=0;sz--) if(s.cnt[sz]>0){ n=s; makeHub(n,Y-u,sz); if(rec(n)) return true; if(nodes>limitN) return false; } }
  }
  return false;
}
// 1 found, 0 proved none, -1 limit
static int solve(const vector<int>&S,int w,long long lim){
  int k=S.size(), sum=0; for(int x:S) sum+=x; Y=k+sum+w+1;
  { int g=0; for(int x:S) g=__gcd(g,x+2); nodes=0; limitN=lim; if((k*Y)%g) return 0; } // necessary: sum (s_i+2) h_i = k*y if(Y>62){ fprintf(stderr,"too big\n"); exit(1); }
  St s; memset(&s,0,sizeof s); memset(s.who,-1,sizeof s.who);
  u64 all=below(Y)&~1ull; s.unk=all; s.fc=all; s.fl=all; for(int l=1;l<Y;l++) s.flr|=1ull<<(63-l);
  s.nh=k; s.wild=w; maxSize=0; for(int x:S){ s.cnt[x]++; if(x>0) s.nhpos++; maxSize=max(maxSize,x); }
  nodes=0; limitN=lim; bool ok=rec(s); if(ok) return 1; return nodes>limitN? -1:0;
}
static void printSol(const vector<int>&S,int w){
  printf("S"); for(int x:S) printf(" %d",x); printf(" | w %d y %d |",w,Y);
  for(int h=1;h<Y;h++) if(sol.hub>>h&1){ printf(" %d:",h); bool f=true; for(int l=1;l<Y;l++) if(sol.who[l]==h){ printf(f?"%d":",%d",l); f=false; } }
  printf(" | W"); for(int l=1;l<Y;l++) if(sol.who[l]==0) printf(" %d",l); printf("\n");
}
static void gen(int total,int k,int maxv,vector<int>&cur,vector<vector<int>>&out){
  if(k==0){ if(total==0) out.push_back(cur); return; }
  for(int f=min(total,maxv); f>=0; f--){ cur.push_back(f); gen(total-f,k-1,f,cur,out); cur.pop_back(); }
}
int main(int argc,char**argv){
  if(argc>1 && argv[1][0]=='S'){ // single instance with random restarts: combx S s1 s2 ...  (env SEED, WMAX)
    vector<int> S; for(int i=2;i<argc;i++) S.push_back(atoi(argv[i])); sort(S.rbegin(),S.rend()); int mx=S[0];
    int wmax=getenv("WMAX")?atoi(getenv("WMAX")):mx; rs=getenv("SEED")?atoll(getenv("SEED"))*2654435761ULL+88172645463325252ULL:88172645463325252ULL; rnd=true;
    int wmin=getenv("WMIN")?atoi(getenv("WMIN")):0; for(long long lim=300000;;lim+=lim/16) for(int w=wmin;w<=wmax;w++){ int r=solve(S,w,lim); if(r==1){ printSol(S,w); return 0; } }
  }
  int N=atoi(argv[1]); int lo=argc>2?atoi(argv[2]):5; int mode=argc>3?atoi(argv[3]):0;
  int part=argc>4?atoi(argv[4]):0, nparts=argc>5?atoi(argv[5]):1; long long idx=0; long long maxlim=getenv("MAXLIM")?atoll(getenv("MAXLIM")):200000000000LL; int from=getenv("FROM")?atoi(getenv("FROM")):0; // FROM=n0: keep the part numbering of a run started at lo but only solve n >= n0
  for(int n=lo;n<=N;n++){ long long cntS=0, fails=0, tot=0; int maxw=0;
    // S with |S| + sum + max + 2 = n
    for(int k=1;k<n;k++) for(int mx=1; k+mx+mx+2<=n; mx++){ int rest=n-2-k-mx-mx; // sum of the other k-1 entries
        vector<vector<int>> ps; vector<int> cur; gen(rest,k-1,mx,cur,ps);
        for(auto&p:ps){ vector<int> S; S.push_back(mx); for(int x:p) S.push_back(x);
          if((idx++)%nparts!=part) continue; if(n<from) continue; cntS++;
          int found=-1;
          if(mode==1){ for(int w=0;w<=mx;w++){ int r=solve(S,w,LLONG_MAX); tot+=nodes; if(r==1){ found=w; break; } } }
          else { for(long long lim=20000; found<0 && lim<=maxlim; lim*=8){ bool allno=true;
                   for(int w=0;w<=mx;w++){ int r=solve(S,w,lim); tot+=min(nodes,lim); if(r==1){ found=w; break; } if(r==-1) allno=false; }
                   if(allno) break; } }
          if(found<0){ fails++; printf(mode==1?"FAIL n=%d S":"HARD n=%d S",n); for(int x:S) printf(" %d",x); printf("\n"); }
          else { maxw=max(maxw,found); printSol(S,found); }
          fflush(stdout); } }
    printf("# n=%d part %d/%d: multisets S with |S|+sum+max+2=n: %lld  comb with w<=max(S) found: %lld  failures: %lld  largest w used: %d  nodes %lld\n",n,part,nparts,cntS,cntS-fails,fails,maxw,tot); fflush(stdout); }
}
