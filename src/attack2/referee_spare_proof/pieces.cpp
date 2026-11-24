// pieces.cpp (referee, independent of armpieces.py/armfast.py)
// Count crossing one-spare "pieces" for a rooted path with arms (b, j):
//   labels injective in 0..R, R=b+j+1, root 0; all edge lengths distinct; lengths strictly decreasing along each arm;
//   crossing: every even-depth label < every odd-depth label; tip of j-arm innermost on its side.
// Method: longest-first: for l = R..1 give length l to the next edge of arm A, of arm B, or to nobody (at most one skip).
// Threshold a is fixed in advance: #low-1 or #low (one spare cell is low or high).
#include <bits/stdc++.h>
using namespace std;
int b,j,R,a; bool used[512]; int A[512],B[512]; int la,lb; long long cnt, nodes; int shown;
bool okcell(int z,int depth){ if(z<0||z>R||used[z]) return false; return (depth%2==0)? (z<=a):(z>a); }
void fin(){
    // check innermost
    int y=B[j]; bool inner=true;
    if(j%2==1){ for(int z=a+1;z<y;z++) if(used[z]) inner=false; }
    else { for(int z=y+1;z<=a;z++) if(used[z]) inner=false; }
    if(!inner) return;
    cnt++;
    if(shown<3){ shown++; printf("  piece a=%d A:",a); for(int i=0;i<=b;i++) printf(" %d",A[i]); printf("  B:"); for(int i=0;i<=j;i++) printf(" %d",B[i]); printf("\n"); }
}
void rec(int l,int skips){
    nodes++;
    if(la==b && lb==j){ fin(); return; }
    if(l<1) return;
    int rem=(b-la)+(j-lb); if(l<rem) return;
    if(la<b) for(int s=-1;s<=1;s+=2){ int z=A[la]+s*l; if(okcell(z,la+1)){ used[z]=true; A[++la]=z; rec(l-1,skips); la--; used[z]=false; } }
    if(lb<j) for(int s=-1;s<=1;s+=2){ int z=B[lb]+s*l; if(okcell(z,lb+1)){ used[z]=true; B[++lb]=z; rec(l-1,skips); lb--; used[z]=false; } }
    if(skips<1) rec(l-1,skips+1);
}
int main(int c,char**v){ b=atoi(v[1]); j=atoi(v[2]); R=b+j+1; int nlow=1+b/2+j/2; cnt=0; nodes=0; shown=0;
    for(a=nlow-1;a<=nlow;a++){ memset(used,0,sizeof used); used[0]=true; A[0]=B[0]=0; la=lb=0; rec(R,0); }
    // note: a piece whose spare cell is the top cell R or cell between blocks could be counted under both thresholds only if
    // the unused cell is exactly a (for a=nlow) = also valid for a=nlow-1?  For a=nlow-1 lows fill 0..a exactly; for a=nlow lows
    // occupy 0..nlow minus one cell.  If that missing cell is nlow itself the labeling was already counted with a=nlow-1.
    printf("b=%d j=%d pieces(counted with multiplicity over thresholds)=%lld nodes=%lld\n",b,j,cnt,nodes); }
