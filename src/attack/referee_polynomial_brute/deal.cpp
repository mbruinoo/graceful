// Referee: independent two-leg deal counter.
// Labels 0..m, root labelled 0, leg A has m-b edges, leg B has b edges.
// Numbers m, m-1, ..., 1 handed out in decreasing order; number k moves the tip
// of the receiving leg by +k or -k onto an unused label in [0,m].
// Counts all complete deals (no pruning other than validity).
// usage: deal mlo mhi blo bhi   (b ranges over [blo, min(bhi, m/2)]; bhi<0 means b=m/2 only (m even))
//        prints for each m: counts per b.  For b == m-b the ordered count is halved.
#include <bits/stdc++.h>
using namespace std;
int m; static char used_[4096];
long long cnt; long long nodes;
void rec(int k,int tA,int rA,int tB,int rB){
    nodes++;
    if(k==0){cnt++;return;}
    if(rA>0){
        int x=tA+k; if(x<=m && !used_[x]){used_[x]=1;rec(k-1,x,rA-1,tB,rB);used_[x]=0;}
        x=tA-k; if(x>=0 && !used_[x]){used_[x]=1;rec(k-1,x,rA-1,tB,rB);used_[x]=0;}
    }
    if(rB>0){
        int x=tB+k; if(x<=m && !used_[x]){used_[x]=1;rec(k-1,tA,rA,x,rB-1);used_[x]=0;}
        x=tB-k; if(x>=0 && !used_[x]){used_[x]=1;rec(k-1,tA,rA,x,rB-1);used_[x]=0;}
    }
}
long long deals(int mm,int b){
    m=mm; memset(used_,0,sizeof used_); used_[0]=1; cnt=0;
    rec(m,0,m-b,0,b);
    if(2*b==m) cnt/=2;
    return cnt;
}
int main(int argc,char**argv){
    int mlo=atoi(argv[1]),mhi=atoi(argv[2]),blo=atoi(argv[3]),bhi=atoi(argv[4]);
    for(int mm=mlo;mm<=mhi;mm++){
        printf("%d",mm);
        if(bhi<0){ if(mm%2==0) printf(" %lld",deals(mm,mm/2)); else printf(" -"); }
        else for(int b=blo;b<=min(bhi,mm/2);b++) printf(" %lld",deals(mm,b));
        printf("\n"); fflush(stdout);
    }
    fprintf(stderr,"nodes %lld\n",nodes);
}
