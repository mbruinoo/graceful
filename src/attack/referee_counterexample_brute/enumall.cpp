// Referee brute force. Enumerates EVERY growth placement on n vertices straight from
// README section 1/2: labels 0..m (m=n-1), bracket of length k is {p,p+k}; brackets taken
// longest first, each must have exactly one foot on a used label.
// For each placement: the tree rooted at the vertex labelled 0 (README label 1) is canonised
// (AHU bit code).  Output: one line per rooted code:  code_hex count
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n,m;
int par[40];           // par[label] = parent label
int ordv[40];          // labels in order of addition
unordered_map<u64,u64> tally;
u64 total=0;
struct C{u64 b;int l;};
static inline bool gt(const C&a,const C&b){return a.l!=b.l? a.l>b.l : a.b>b.b;}
void record(){
    static C kids[40][40]; static int nk[40];
    for(int i=0;i<n;i++)nk[i]=0;
    C rootc{0,0};
    for(int i=n-1;i>=0;i--){
        int v=ordv[i];
        // sort kids of v descending
        C*k=kids[v];int c=nk[v];
        for(int a=1;a<c;a++){C x=k[a];int b=a-1;while(b>=0&&gt(x,k[b])){k[b+1]=k[b];b--;}k[b+1]=x;}
        u64 bits=1;int len=1;
        for(int a=0;a<c;a++){bits=(bits<<k[a].l)|k[a].b;len+=k[a].l;}
        bits<<=1;len++;
        if(i==0){rootc={bits,len};}
        else{int p=par[v];kids[p][nk[p]++]={bits,len};}
    }
    tally[rootc.b]++;total++;
}
void rec(int k,unsigned used,int cnt){
    if(k==0){record();return;}
    for(int p=0;p+k<=m;p++){
        bool a=used>>p&1,b=used>>(p+k)&1;
        if(a==b)continue;
        int nw=a?p+k:p, old=a?p:p+k;
        par[nw]=old;ordv[cnt]=nw;
        rec(k-1,used|(1u<<nw),cnt+1);
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]);m=n-1;
    if(n==1){printf("2 1\n");return 0;}
    ordv[0]=0;par[0]=-1;
    // bracket m is {0,m}
    par[m]=0;ordv[1]=m;
    rec(m-1,1u|(1u<<m),2);
    for(auto&kv:tally)printf("%llx %llu\n",kv.first,kv.second);
    fprintf(stderr,"n=%d growth placements=%llu rooted shapes=%zu\n",n,total,tally.size());
}
