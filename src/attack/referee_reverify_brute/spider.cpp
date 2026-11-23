// Referee: spider deals (README sec 13). Centre at label 0, labels 0..m. Numbers m, m-1, ..., 1 are handed
// to legs one at a time; each moves that leg's tip up or down by that amount (first move of a leg: up from 0).
// Valid if every tip stays in 1..m and no label is visited twice.
// usage: spider n mode      mode: free | zigzag | level | first
//   zigzag: every leg alternates up, down, up, ...
//   level : every leg gets its j-th number before any leg gets its (j+1)-th (directions free)
//   first : every leg gets its first number before any leg gets a second (then free)
// All spiders with >= 3 legs on n vertices (partitions of n-1 into >= 3 parts). Exhaustive DFS with a
// table of failed states (exact keys). Each deal found is replayed by check().
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int m,mode,K; int len[40],tip[40],got[40],dirn[40]; int who[64],sgn[64];
struct Key{u64 a,b,c; bool operator==(const Key&o)const{return a==o.a&&b==o.b&&c==o.c;}};
struct KH{size_t operator()(const Key&k)const{return k.a*0x9E3779B97F4A7C15ULL^(k.b*0xC2B2AE3D27D4EB4FULL)^(k.c*0x165667B19E3779F9ULL);}};
unordered_set<Key,KH> failed; bool usememo;
Key mk(u64 used){ // state: used labels + multiset of (tip,got,dir) for unfinished legs, grouped by leg length
  // exact: sort unfinished legs' (len,got,tip,dir) tuples and pack; fall back to hashing two independent mixes
  u64 t[40]; int c=0; for(int i=0;i<K;i++) if(got[i]<len[i]) t[c++]=((u64)len[i]<<24)|((u64)got[i]<<16)|((u64)tip[i]<<8)|(u64)(dirn[i]+1);
  sort(t,t+c); u64 h1=1469598103934665603ULL,h2=0x9E3779B97F4A7C15ULL; for(int i=0;i<c;i++){h1=(h1^t[i])*1099511628211ULL; h2=(h2+t[i])*0xD6E8FEB86659FD93ULL; h2^=h2>>29;}
  return Key{used,h1,h2}; }
bool dfs(int w,u64 used){
  if(w==0) return true;
  // candidate legs
  int minlvl=1000; if(mode==2||mode==3) for(int i=0;i<K;i++) if(got[i]<len[i]) minlvl=min(minlvl,got[i]);
  Key key; if(usememo){ key=mk(used); if(failed.count(key)) return false; }
  u64 tried[80]; int nt=0;
  for(int i=0;i<K;i++){ if(got[i]>=len[i]) continue;
    if(mode==2 && got[i]!=minlvl) continue;
    if(mode==3 && minlvl==0 && got[i]!=0) continue;
    u64 sig=((u64)len[i]<<24)|((u64)got[i]<<16)|((u64)tip[i]<<8)|(u64)(dirn[i]+1);
    bool dup=false; for(int j=0;j<nt;j++) if(tried[j]==sig){dup=true;break;} if(dup)continue; tried[nt++]=sig;
    for(int s=1;s>=-1;s-=2){
      if(got[i]==0 && s<0) continue;
      if(mode==1 && got[i]>0 && s==dirn[i]) continue;
      int nt2=tip[i]+s*w; if(nt2<1||nt2>m||((used>>nt2)&1)) continue;
      int ot=tip[i],od=dirn[i]; tip[i]=nt2; dirn[i]=s; got[i]++; who[w]=i; sgn[w]=s;
      bool r=dfs(w-1,used|(1ULL<<nt2));
      tip[i]=ot; dirn[i]=od; got[i]--;
      if(r) return true; } }
  if(usememo) failed.insert(key);
  return false;
}
bool check(){ // replay the deal from scratch
  int t[40]={0},g[40]={0},d[40]={0}; u64 used=1; int lvlmin;
  for(int w=m;w>=1;w--){ int i=who[w],s=sgn[w]; if(g[i]>=len[i]) return false;
    if(g[i]==0&&s!=1) return false; if(mode==1&&g[i]>0&&s==d[i]) return false;
    lvlmin=1000; for(int j=0;j<K;j++) if(g[j]<len[j]) lvlmin=min(lvlmin,g[j]);
    if(mode==2&&g[i]!=lvlmin) return false; if(mode==3&&lvlmin==0&&g[i]!=0) return false;
    t[i]+=s*w; if(t[i]<1||t[i]>m||((used>>t[i])&1)) return false; used|=1ULL<<t[i]; g[i]++; d[i]=s; }
  for(int j=0;j<K;j++) if(g[j]!=len[j]) return false;
  return used==((m==63)?~0ULL:((1ULL<<(m+1))-1)); }
long nsp=0,nok=0,nnone=0; string nonelist;
void run(){ for(int i=0;i<K;i++){tip[i]=0;got[i]=0;dirn[i]=0;} failed.clear(); usememo=true;
  nsp++; if(dfs(m,1ULL)){ if(!check()){fprintf(stderr,"CHECK FAILED\n");exit(3);} nok++; }
  else { nnone++; nonelist+=" ("; for(int i=0;i<K;i++){nonelist+=to_string(len[i]); if(i+1<K)nonelist+=",";} nonelist+=")"; } }
void parts(int rem,int mx,int k){ if(rem==0){ if(k>=3){K=k;run();} return; }
  for(int p=min(rem,mx);p>=1;p--){len[k]=p;parts(rem-p,p,k+1);} }
int main(int argc,char**argv){ int n=atoi(argv[1]); m=n-1; string md=argv[2];
  mode= md=="free"?0: md=="zigzag"?1: md=="level"?2:3;
  parts(m,m,0);
  printf("n=%d mode=%s: spiders=%ld deals(found, replayed)=%ld NONE=%ld%s\n",n,md.c_str(),nsp,nok,nnone,nnone<=12?nonelist.c_str():""); }
