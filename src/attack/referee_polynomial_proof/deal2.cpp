// Referee: independent two-leg deal counter. Labels 0..m, root 0, legs of lenA=m-b and lenB=b edges.
// Numbers m..1 in decreasing order; each moves a leg tip by +-k to an unused label in [0,m].
// usage: deal2 mlo mhi blo bhi   (b = -1 means b=m/2 ; counts printed per (m,b)); optional node cap
#include <bits/stdc++.h>
using namespace std;
int m; vector<char> used; long long cnt, nodes, cap;
void rec(int k,int ta,int ra,int tb,int rb){
    if(k==0){cnt++;return;}
    if(cap && nodes>cap) return;
    nodes++;
    if(ra){
        for(int s=-1;s<=1;s+=2){int x=ta+s*k; if(x<0||x>m||used[x])continue; used[x]=1; rec(k-1,x,ra-1,tb,rb); used[x]=0;}
    }
    if(rb){
        if(ta==tb && ra) return; // both tips at root: symmetric only if equal lengths; handled by caller (never equal here unless b=m-b)
        for(int s=-1;s<=1;s+=2){int x=tb+s*k; if(x<0||x>m||used[x])continue; used[x]=1; rec(k-1,ta,ra,x,rb-1); used[x]=0;}
    }
}
int main(int c,char**v){
    int mlo=atoi(v[1]),mhi=atoi(v[2]),blo=atoi(v[3]),bhi=atoi(v[4]); cap=c>5?atoll(v[5]):0;
    for(m=mlo;m<=mhi;m++){
        for(int b=blo;b<=bhi;b++){
            int bb= b<0? m/2 : b; if(b<0 && m%2) continue;
            if(bb>m-bb) continue;
            used.assign(m+1,0); used[0]=1; cnt=0; nodes=0;
            // legs A (m-bb) and B (bb). If bb==0 single leg. If both tips at root initially and lengths differ, both orders distinct.
            if(bb==0) { rec(m,0,m,0,0); }
            else if(bb==m-bb){ // equal legs: fix that A receives m (unordered legs)
                used[m]=1; rec(m-1,m,m-bb-1,0,bb); 
            } else {
                // can't use the ta==tb shortcut: explore both
                used[m]=1; rec(m-1,m,m-bb-1,0,bb); long long c1=cnt; 
                rec(m-1,0,m-bb,m,bb-1); used[m]=0; (void)c1;
            }
            printf("%d %d %lld%s\n",m,bb,cnt,(cap&&nodes>cap)?" CAPPED":"");
        }
        fflush(stdout);
    }
}
