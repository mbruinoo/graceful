// Deals for k equal legs of length L with at most B "breaks".  Leg edges e_1>e_2>...; gaps g_j=e_j-e_{j+1}.
// A break is a j with g_j != g_{j-P} (P = env PER, default 2), or a move in the same direction as the previous move of that leg (j>=2).
// usage: persearch k L B [all]
#include <bits/stdc++.h>
using namespace std;
int k,L,m,B,P=2; int cnt_[64],cur[64],ldir[64]; bool used[4096]; vector<int> w[64],lab[64]; long long nodes,found=0; bool ALL=false; long long LIMIT=3000000000LL;
void show(){ for(int i=0;i<k;i++){ printf("  labels:"); for(int x:lab[i]) printf(" %3d",x); printf("   edges:"); for(int x:w[i]) printf(" %3d",x); printf("\n"); } }
int rec(int t,int br){ if(t==0){ found++; if(ALL){ printf("deal %lld breaks=%d\n",found,br); show(); return 0;} show(); return 1; } if(++nodes>LIMIT) return -1;
  for(int i=0;i<k;i++){ if(cnt_[i]==L) continue; int c=cnt_[i]; if(c==0 && i>0 && cnt_[i-1]==0) continue;
    int gb=0; if(c>=P+1){ int g=w[i][c-1]-t, g0=w[i][c-1-P]-w[i][c-P]; if(g!=g0) gb=1; }
    for(int sg=0;sg<2;sg++){ int x,d; if(c==0){ if(sg) continue; x=t; d=1; } else { d= sg==0?-1:1; x=cur[i]+d*t; }
      if(x<1||x>m||used[x]) continue;
      int nb=br+gb+((c>=1 && d==ldir[i])?1:0); if(nb>B) continue;
      int old=cur[i],od=ldir[i]; cur[i]=x; ldir[i]=d; used[x]=1; cnt_[i]++; w[i].push_back(t); lab[i].push_back(x);
      int r=rec(t-1,nb);
      lab[i].pop_back(); w[i].pop_back(); cnt_[i]--; used[x]=0; cur[i]=old; ldir[i]=od; if(r==1) return 1; if(r<0) return -1; } }
  return 0; }
int main(int argc,char**argv){ k=atoi(argv[1]); L=atoi(argv[2]); B=atoi(argv[3]); ALL=argc>4; m=k*L; if(getenv("PER")) P=atoi(getenv("PER"));
  int r=rec(m,0); if(ALL){ printf("k=%d L=%d B=%d total=%lld\n",k,L,B,found); return 0; }
  printf("k=%d L=%d B=%d %s nodes=%lld\n",k,L,B,r==1?"found":r==0?"none":"unresolved",nodes); }
