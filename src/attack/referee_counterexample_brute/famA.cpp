// Referee: exact number of growth placements of README family A on n vertices
// (centre c; hub h adjacent to c with m=n-6 leaves; two legs c-x1-y1, c-x2-y2), by direct enumeration of the
// labels of the 6 non-leaf... vertices h,c,x1,y1,x2,y2 (labels 0..n-1); the hub leaves take all other labels.
// Graceful: all n-1 edge lengths distinct.  Growth: Theorem 7 heap form is NOT assumed blindly -- the final
// labeling is checked by the definition (longest first, each bracket exactly one used foot).
// count = labelings / (2 * m!) ; we enumerate labelings up to leaf permutation and divide by 2 (leg swap).
#include <bits/stdc++.h>
using namespace std;
int n;int cnt[200];int a;long long total;
int core[6];bool isCore[200];
bool growthCheck(){ // definition check
    // edges: (a,c),(c,x1),(x1,y1),(c,x2),(x2,y2), and (a,l) for every non-core l
    static int ea[200],eb[200];
    for(int L=0;L<n;L++)ea[L]=-1;
    auto add=[&](int u,int v)->bool{int L=abs(u-v);if(L<1||ea[L]>=0)return false;ea[L]=u;eb[L]=v;return true;};
    int c=core[1],x1=core[2],y1=core[3],x2=core[4],y2=core[5];
    if(!add(a,c)||!add(c,x1)||!add(x1,y1)||!add(c,x2)||!add(x2,y2))return false;
    for(int l=0;l<n;l++)if(!isCore[l])if(!add(a,l))return false;
    static bool used[200];for(int i=0;i<n;i++)used[i]=false;
    for(int L=n-1;L>=1;L--){
        if(ea[L]<0)return false;
        if(L==n-1){used[ea[L]]=used[eb[L]]=true;continue;}
        if(used[ea[L]]==used[eb[L]])return false;
        used[ea[L]]=used[eb[L]]=true;
    }
    return true;
}
void rec(int depth,int bad){
    if(depth==6){
        if(bad)return;
        if(growthCheck())total++;
        return;
    }
    int rem=6-depth;
    for(int l=0;l<n;l++){
        if(isCore[l])continue;
        int j=abs(l-a);
        int nb=bad-(cnt[j]==2);
        if(nb>rem-1)continue;
        cnt[j]--;isCore[l]=true;core[depth]=l;
        // prune: lengths of core edges fixed so far must end with cnt==0 (no leaf may use them), and be distinct
        int e[5];int ne=0;bool ok=true;
        if(depth>=1)e[ne++]=abs(core[1]-a);
        if(depth>=2)e[ne++]=abs(core[2]-core[1]);
        if(depth>=3)e[ne++]=abs(core[3]-core[2]);
        if(depth>=4)e[ne++]=abs(core[4]-core[1]);
        if(depth>=5)e[ne++]=abs(core[5]-core[4]);
        int need=0;
        for(int i=0;i<ne&&ok;i++){for(int k=0;k<i;k++)if(e[k]==e[i])ok=false;need+=cnt[e[i]];}
        if(ok&&need<=rem-1)rec(depth+1,nb);
        cnt[j]++;isCore[l]=false;
    }
}
int main(int argc,char**argv){
    int lo=atoi(argv[1]),hi=atoi(argv[2]);
    for(n=lo;n<=hi;n++){
        total=0;
        for(a=0;a<n;a++){
            int bad=0;
            for(int j=1;j<n;j++){cnt[j]=(a-j>=0)+(a+j<n);if(cnt[j]==2)bad++;}
            if(bad>5)continue;
            for(int i=0;i<n;i++)isCore[i]=false;
            isCore[a]=true;core[0]=a;
            rec(1,bad);
        }
        printf("n=%d count=%lld%s\n",n,total/2,total%2?" ODD!":"");fflush(stdout);
    }
}
