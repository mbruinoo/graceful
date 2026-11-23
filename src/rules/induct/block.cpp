// BLOCK DEALS.  A block deal on (m, M] for leg lengths L_1..L_k (sum = M-m): hand the numbers M, M-1, .., m+1
// to the legs (leg i gets L_i numbers, decreasing), tips start at 0, first move up, later moves up or down,
// and the labels visited are exactly the numbers m+1..M, each once.
// Union Lemma: a valid deal on 1..m of a spider S together with a block deal on (m,M] is a valid deal of S + new legs.
// Usage: block m L1 L2 ... Lk   -> prints one block deal or "none"   (ZIG=1: zigzag legs only; LIMIT nodes via ZLIMIT)
//        block scan L mmax kmax -> for each m<=mmax the k<=kmax for which k legs of length L form a block on (m, m+kL]
#include <bits/stdc++.h>
using namespace std;
int k,m,M; int L[64], cnt_[64], cur[64]; bool used[512]; vector<int> w[64]; long long nodes, LIMIT=50000000; bool ZIG=false;
int rec(int t){ if(t==m) return 1; if(++nodes>LIMIT) return -1;
  for(int i=0;i<k;i++){ if(cnt_[i]==L[i]) continue; if(cnt_[i]==0 && i>0 && L[i-1]==L[i] && cnt_[i-1]==0) continue;
    for(int sg=0; sg<(cnt_[i]>0&&!ZIG?2:1); sg++){ int x; if(cnt_[i]==0) x=t; else if(ZIG) x=(cnt_[i]%2==0)?cur[i]+t:cur[i]-t; else x= sg==0?cur[i]-t:cur[i]+t;
      if(x<=m||x>M||used[x]) continue; int old=cur[i]; cur[i]=x; used[x]=1; cnt_[i]++; w[i].push_back(x>old?t:-t);
      int r=rec(t-1); if(r==1) return 1; w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; if(r<0) return -1; } }
  return 0; }
int solve(){ M=m; for(int i=0;i<k;i++){ M+=L[i]; cnt_[i]=0; cur[i]=0; w[i].clear(); } memset(used,0,sizeof used); nodes=0; return rec(M); }
int main(int argc,char**argv){ if(getenv("ZIG")) ZIG=true; if(getenv("ZLIMIT")) LIMIT=atoll(getenv("ZLIMIT"));
  if(!strcmp(argv[1],"scan")){ int LL=atoi(argv[2]), mmax=atoi(argv[3]), kmax=atoi(argv[4]);
    for(m=0;m<=mmax;m++){ printf("L=%d m=%d: k =",LL,m); for(k=1;k<=kmax;k++){ for(int i=0;i<k;i++) L[i]=LL; int r=solve(); if(r==1) printf(" %d",k); else if(r<0) printf(" %d?",k); } printf("\n"); fflush(stdout); } return 0; }
  m=atoi(argv[1]); k=argc-2; for(int i=0;i<k;i++) L[i]=atoi(argv[i+2]); int r=solve(); if(r!=1){ printf(r==0?"none\n":"unresolved\n"); return 0; }
  for(int i=0;i<k;i++){ printf("  ["); int c=0; for(size_t j=0;j<w[i].size();j++) printf("%s%+d",j?" ":"",w[i][j]); printf("]  labels"); for(int x:w[i]){ c+=x; printf(" %d",c); } printf("\n"); } }
