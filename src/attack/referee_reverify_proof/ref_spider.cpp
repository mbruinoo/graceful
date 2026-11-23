// Referee's independent spider deal search (README sec 13): centre at label 0, labels 0..m,
// numbers m..1 handed to legs one at a time, each moves that leg's tip up or down, first move up; no label twice.
// usage: ref_spider n MODE   MODE: free zigzag level first.   All spiders with >=3 legs on n vertices.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int m,k; vector<int> L; int tip[64],cnt[64]; string mode; vector<pair<int,int>> hist;
static bool dfs(int w,u64 used){
    if(w==0) return true;
    int mincnt=1e9; bool unstarted=false;
    for(int i=0;i<k;i++) if(cnt[i]<L[i]){ mincnt=min(mincnt,cnt[i]); if(cnt[i]==0) unstarted=true; }
    for(int i=0;i<k;i++){ if(cnt[i]>=L[i]) continue;
        if(cnt[i]==0 && i>0 && L[i-1]==L[i] && cnt[i-1]==0) continue; // identical unstarted legs
        if(mode=="level" && cnt[i]!=mincnt) continue;
        if(mode=="first" && unstarted && cnt[i]!=0) continue;
        for(int s=1;s>=-1;s-=2){
            if(cnt[i]==0 && s<0) continue;
            if(mode=="zigzag" && s!=((cnt[i]%2==0)?1:-1)) continue;
            int b=tip[i]+s*w; if(b<1||b>m||(used>>b&1)) continue;
            int old=tip[i]; tip[i]=b; cnt[i]++;
            if(dfs(w-1,used|(1ULL<<b))){ hist.push_back({i,b}); return true; }
            tip[i]=old; cnt[i]--;
        } }
    return false;
}
static void part(int rem,int mx,vector<int>&cur,vector<vector<int>>&out){
    if(rem==0){ if(cur.size()>=3) out.push_back(cur); return; }
    for(int x=min(rem,mx);x>=1;x--){ cur.push_back(x); part(rem-x,x,cur,out); cur.pop_back(); }
}
int main(int argc,char**argv){
    int n=atoi(argv[1]); mode=argv[2]; m=n-1;
    vector<vector<int>> ps; vector<int> cur; part(m,m,cur,ps);
    int none=0; string fails;
    for(auto&p:ps){ L=p; k=p.size(); for(int i=0;i<k;i++){tip[i]=0;cnt[i]=0;} hist.clear();
        if(!dfs(m,1ULL)){ none++; fails+=" ("; for(int i=0;i<k;i++) fails+=(i?",":"")+to_string(p[i]); fails+=")"; }
        else { // replay check: labels distinct in 1..m, numbers m..1 in order, per-leg edge lengths decreasing outward by construction
            reverse(hist.begin(),hist.end()); vector<int> t(k,0); set<int> seen; int w=m; bool ok=true;
            for(auto&h:hist){ if(abs(h.second-t[h.first])!=w) ok=false; t[h.first]=h.second; if(!seen.insert(h.second).second||h.second<1||h.second>m) ok=false; w--; }
            if(!ok||w!=0){ printf("REPLAY FAILED\n"); return 1; } }
    }
    printf("n=%d mode=%s spiders %zu NONE %d%s\n",n,mode.c_str(),ps.size(),none, none<=6?fails.c_str():"");
}
