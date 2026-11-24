// lred.cpp -- the REDUCED problem behind L(l;h1,h2) (REPORT.txt section 2).
// Numbers 1..N, N = hP+hQ+2+d, a = N+1 (c at the top label).  Hub P at gP with edge a-gP and hP leaves,
// hub Q at gQ with edge a-gQ and hQ leaves; d numbers are "gaps" (root leaves: label = length).
// A leaf of a hub at g with length w (w < a-g) has label g+w or g-w.  Every number in 1..N is used once as a
// label and once as a length.  Usage: lred hP hQ d  -> prints every (gP,gQ) for which a solution exists.
#include <bits/stdc++.h>
using namespace std;
int hP,hQ,d,N,a,g[2],x[2],cap[3]; bool usedL[200]; long long nodes;
bool rec(int w){ // lengths descending
  while(w>=1&&(w==x[0]||w==x[1])) w--;
  if(w==0) return true; nodes++;
  if(cap[2]&&!usedL[w]){ cap[2]--; usedL[w]=1; if(rec(w-1)) return true; usedL[w]=0; cap[2]++; }
  for(int k=0;k<2;k++) if(cap[k]&&w<x[k]) for(int s=1;s>=-1;s-=2){ int L=g[k]+s*w; if(L<1||L>N||usedL[L]) continue;
    cap[k]--; usedL[L]=1; if(rec(w-1)) return true; usedL[L]=0; cap[k]++; }
  return false; }
int main(int argc,char**argv){ hP=atoi(argv[1]); hQ=atoi(argv[2]); d=atoi(argv[3]); N=hP+hQ+2+d; a=N+1; int cnt=0;
  printf("hP=%d hQ=%d d=%d N=%d feasible (gP,gQ):",hP,hQ,d,N);
  for(g[0]=1;g[0]<=N;g[0]++) for(g[1]=1;g[1]<=N;g[1]++){ if(g[0]==g[1]) continue; x[0]=a-g[0]; x[1]=a-g[1];
    memset(usedL,0,sizeof usedL); usedL[g[0]]=usedL[g[1]]=1; cap[0]=hP; cap[1]=hQ; cap[2]=d;
    if(rec(N)){ printf(" (%d,%d)",g[0],g[1]); cnt++; } }
  printf(" | count=%d nodes=%lld\n",cnt,nodes); }
