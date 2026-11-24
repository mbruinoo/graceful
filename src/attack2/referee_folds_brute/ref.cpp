// Referee solver, written from README sections 1-3, 11 and the definitions in the claims.
// Usage: ./ref MODE [PARAM] [NODECAP] < trees     (one tree per line, 0-based edge list)
//   MODE A  : tidy_A exactly (iterative deepening on budget)
//   MODE B  : tidy_B exactly
//   MODE R  : PARAM = rule bitmask; existence of a growth placement obeying the rule
// Output per line: "<idx> <n> <value or NONE or CAP> labels: l0 l1 ..."  (label of vertex i)
// Each found labeling is re-checked from scratch by check() (bijection, lengths, growth, cost/rule).
#include <bits/stdc++.h>
using namespace std;

int MODE; int RULE=0; bool STRICT=false; long long NODECAP=0;
int n; vector<vector<int>> adj;
// shapes
map<vector<int>,int> shapeId; vector<vector<int>> shapeKids;
map<vector<int>,int> forestId; vector<vector<int>> forestList;
int internForest(vector<int> v){ sort(v.begin(),v.end()); auto it=forestId.find(v); if(it!=forestId.end()) return it->second; int id=forestList.size(); forestId[v]=id; forestList.push_back(v); return id;}
int shapeOf(int v,int p, vector<int>& sh){ // fills sh[v] for rooting with parent p
    vector<int> k; for(int w:adj[v]) if(w!=p){ k.push_back(shapeOf(w,v,sh)); } sort(k.begin(),k.end());
    auto it=shapeId.find(k); int id; if(it==shapeId.end()){ id=shapeKids.size(); shapeId[k]=id; shapeKids.push_back(k);} else id=it->second; sh[v]=id; return id; }

// search state
vector<int> par; vector<int> sh; // rooting for current root edge
vector<int> cellV;   // vertex at cell (1..n), -1 unused
vector<char> placed;
vector<int> cellF;   // forest id at cell (-1 unused)
int gapLo,gapHi; vector<int> holes; // rule mode
long long nodes; bool capped;
unordered_map<string,int> failMemo; // key -> largest budget known to fail
int unusedCnt;

string key(){ string s; s.reserve(4*(n+4)+4*holes.size());
    auto put=[&](int x){ s.append((char*)&x,4); };
    for(int c=1;c<=n;c++) put(cellF[c]);
    if(MODE=='R'){ put(gapLo); put(gapHi); vector<int> h=holes; if(!(RULE&(8|16))) sort(h.begin(),h.end()); for(int x:h) put(x);} return s; }

// cost of step x (fresh) -> y, given current used state (before the step)
int stepCost(int x,int y){
    if(MODE=='R') return 0;
    // runs
    int lo=x,hi=x; while(lo-1>=1 && cellV[lo-1]<0) lo--; while(hi+1<=n && cellV[hi+1]<0) hi++;
    int r = (y>x)? (x-lo) : (hi-x);
    if(MODE=='B') return r==0?0:1;
    // main run: longest, leftmost on ties
    int bestL=-1,bestLo=-1; int c=1; while(c<=n){ if(cellV[c]<0){ int a=c; while(c<=n&&cellV[c]<0) c++; int L=c-a; if(L>bestL){bestL=L;bestLo=a;} } else c++; }
    if(bestLo!=lo) return 1; return r==0?0:1;
}

vector<int> kidsUnplaced(int v){ vector<int> k; for(int w:adj[v]) if(w!=par[v] && !placed[w]) k.push_back(w); return k; }

int removeFromForest(int f,int s){ vector<int> v=forestList[f]; auto it=find(v.begin(),v.end(),s); v.erase(it); return internForest(v);}
vector<int> vForest; // forest id of vertex's full child set

bool dfs(int budget);

bool tryMove(int x,int y,int budget, int ngLo,int ngHi, int holeAdd, int holeRemove){
    // place a child of vertex at y on cell x
    if(x<1||x>n||y<1||y>n) return false; if(cellV[x]>=0||cellV[y]<0) return false;
    int v=cellV[y]; vector<int> k=kidsUnplaced(v); if(k.empty()) return false;
    int cst=stepCost(x,y); if(cst>budget) return false;
    set<int> seen;
    for(int w:k){ if(seen.count(sh[w])) continue; seen.insert(sh[w]);
        // apply
        int oldFy=cellF[y]; int oGL=gapLo,oGH=gapHi; vector<int> oH=holes;
        placed[w]=1; cellV[x]=w; cellF[x]=vForest[w]; cellF[y]=removeFromForest(oldFy,sh[w]); unusedCnt--;
        if(MODE=='R'){ gapLo=ngLo; gapHi=ngHi; if(holeRemove>0) holes.erase(find(holes.begin(),holes.end(),holeRemove)); if(holeAdd>0) holes.push_back(holeAdd);}
        bool ok=dfs(budget-cst);
        if(ok) return true;
        placed[w]=0; cellV[x]=-1; cellF[x]=-1; cellF[y]=oldFy; unusedCnt++; gapLo=oGL; gapHi=oGH; holes=oH;
        if(capped) return false;
    }
    return false;
}

bool dfs(int budget){
    if(unusedCnt==0) return true;
    if(NODECAP && ++nodes>NODECAP){ capped=true; return false; }
    if(!NODECAP) nodes++;
    string kk=key(); auto it=failMemo.find(kk); if(it!=failMemo.end() && it->second>=budget) return false;
    int t=unusedCnt; bool ok=false;
    if(MODE!='R'){
        for(int y=1;y<=n && !ok;y++) if(cellV[y]>=0 && !forestList[cellF[y]].empty()){
            if(tryMove(y+t,y,budget,0,0,0,0)) ok=true; else if(capped) return false;
            else if(tryMove(y-t,y,budget,0,0,0,0)) ok=true; if(capped) return false; }
    } else {
        int L=(gapLo<=gapHi)?gapHi-gapLo+1:0;
        // S/B from ends
        if(L>=1){
            int ends[2]={gapLo,gapHi};
            for(int e=0;e<2 && !ok;e++){ if(e==1 && L==1) break; int x=ends[e];
                int nlo= (e==0)? gapLo+1:gapLo, nhi=(e==0)?gapHi:gapHi-1;
                for(int d=-1;d<=1 && !ok;d+=2){
                    bool isS = (L==1) || (e==0 ? d>0 : d<0);
                    if(!isS && (RULE&4)) continue;
                    if(tryMove(x,x+d*t,budget,nlo,nhi,0,0)) ok=true; if(capped) return false; }
            }
        }
        // K1
        if(L>=2 && !ok){
            for(int e=0;e<2 && !ok;e++){
                int x=(e==0)?gapLo+1:gapHi-1; int hole=(e==0)?gapLo:gapHi;
                int nlo=(e==0)?gapLo+2:gapLo, nhi=(e==0)?gapHi:gapHi-2;
                for(int d=-1;d<=1 && !ok;d+=2){
                    bool across = (e==0)? d>0 : d<0;
                    if(!across && (RULE&2)) continue;
                    if(STRICT && across && L<3) continue;   // classify (x,y) uniquely: gap of 2 -> B
                    if(STRICT && !across && L<4) continue;  // gap of 2 -> S, gap of 3 -> across from other end
                    if(tryMove(x,x+d*t,budget,nlo,nhi,hole,0)) ok=true; if(capped) return false; }
            }
        }
        // F
        if(!ok && !holes.empty()){
            vector<int> cand;
            if(RULE&8) cand.push_back(holes.front());
            else if(RULE&16) cand.push_back(holes.back());
            else if(RULE&32){ int mn=*min_element(holes.begin(),holes.end()), mx=*max_element(holes.begin(),holes.end()); cand.push_back(mn); if(mx!=mn) cand.push_back(mx);}
            else cand=holes;
            for(int x:cand){ for(int d=-1;d<=1 && !ok;d+=2){ if(tryMove(x,x+d*t,budget,gapLo,gapHi,0,x)) ok=true; if(capped) return false; } if(ok) break; }
        }
    }
    if(!ok){ int &m=failMemo[kk]; if(failMemo.count(kk)==0 || m<budget) m=budget; failMemo[kk]=max(failMemo[kk],budget); }
    return ok;
}

// ---------- independent check of a labeling ----------
// returns cost (A or B) or -1 if not a growth placement
int checkLabel(const vector<pair<int,int>>& E, const vector<int>& lab, char cm){
    int N=lab.size(); vector<int> seen(N+2,0); for(int l:lab){ if(l<1||l>N||seen[l]) return -1; seen[l]=1; }
    vector<pair<int,int>> br(N); vector<int> got(N,0);
    for(auto&e:E){ int a=lab[e.first],b=lab[e.second]; int L=abs(a-b); if(L<1||L>N-1||got[L]) return -1; got[L]=1; br[L]={min(a,b),max(a,b)}; }
    vector<char> used(N+2,0); if(br[N-1]!=make_pair(1,N)) return -1; used[1]=used[N]=1; int cost=0;
    for(int L=N-2;L>=1;L--){ int a=br[L].first,b=br[L].second; if(used[a]==used[b]) return -1; int x=used[a]?b:a, y=used[a]?a:b;
        int lo=x,hi=x; while(lo-1>=1&&!used[lo-1]) lo--; while(hi+1<=N&&!used[hi+1]) hi++;
        int r=(y>x)?x-lo:hi-x; int unusedTot=0; for(int c=1;c<=N;c++) if(!used[c]) unusedTot++; if(unusedTot!=L+1-1+0 && unusedTot!=L) return -1; // t = #unused
        bool stair=(r==0);
        if(cm=='A'){ int bestL=-1,bestLo=-1,c=1; while(c<=N){ if(!used[c]){int s=c; while(c<=N&&!used[c]) c++; if(c-s>bestL){bestL=c-s;bestLo=s;}} else c++; } if(bestLo!=lo) stair=false; }
        if(!stair) cost++; used[x]=1; }
    return cost;
}

int main(int argc,char**argv){
    MODE=argv[1][0]; STRICT=getenv("STRICT")!=nullptr; if(MODE=='R') RULE=atoi(argv[2]); if(argc>3) NODECAP=atoll(argv[3]);
    string line; int idx=0;
    while(getline(cin,line)){
        istringstream is(line); vector<int> a; int z; while(is>>z) a.push_back(z); if(a.empty()) continue;
        n=a.size()/2+1; adj.assign(n,{}); vector<pair<int,int>> E;
        for(size_t i=0;i+1<a.size();i+=2){ adj[a[i]].push_back(a[i+1]); adj[a[i+1]].push_back(a[i]); E.push_back({a[i],a[i+1]}); }
        int maxB = (MODE=='R')?0:n; int found=-1; vector<int> bestLab; bool anyCap=false;
        // root edges, deduped by shape pair
        vector<pair<int,int>> roots; set<pair<int,int>> rs;
        for(auto&e:E) for(int o=0;o<2;o++){ int u=o?e.second:e.first, v=o?e.first:e.second; vector<int> s1(n),s2(n); int A=shapeOf(u,v,s1), B=shapeOf(v,u,s2); if(rs.insert({A,B}).second) roots.push_back({u,v}); }
        for(int bud=0; bud<=maxB && found<0; bud++){
            for(auto rt:roots){
                int u=rt.first,v=rt.second;
                par.assign(n,-1); sh.assign(n,0);
                // root: u with parent v, v with parent u
                vector<int> s1(n),s2(n); shapeOf(u,v,s1); shapeOf(v,u,s2);
                // set par via BFS
                function<void(int,int)> setp=[&](int x,int p){ par[x]=p; sh[x]=s1[x]; for(int w:adj[x]) if(w!=p) setp(w,x); };
                function<void(int,int)> setq=[&](int x,int p){ par[x]=p; sh[x]=s2[x]; for(int w:adj[x]) if(w!=p) setq(w,x); };
                setp(u,v); setq(v,u);
                vForest.assign(n,0); for(int x=0;x<n;x++){ vector<int> k; for(int w:adj[x]) if(w!=par[x]) k.push_back(sh[w]); vForest[x]=internForest(k); }
                cellV.assign(n+1,-1); cellF.assign(n+1,-1); placed.assign(n,0);
                cellV[1]=u; cellV[n]=v; placed[u]=placed[v]=1; cellF[1]=vForest[u]; cellF[n]=vForest[v];
                unusedCnt=n-2; gapLo=2; gapHi=n-1; holes.clear(); if(n==2){gapLo=1;gapHi=0;}
                failMemo.clear(); nodes=0; capped=false;
                bool ok=dfs(bud);
                if(capped) anyCap=true;
                if(ok){ found=bud; bestLab.assign(n,0); for(int c=1;c<=n;c++) bestLab[cellV[c]]=c; break; }
            }
            if(MODE=='R') break;
            if(anyCap) break;
        }
        cout<<idx<<" "<<n<<" ";
        if(found<0) cout<<(anyCap?"CAP":"NONE"); else {
            cout<<found; if(MODE!='R'){ int c=checkLabel(E,bestLab,MODE); if(c!=found){ cout<<" CHECKFAIL "<<c; } }
            else { int c=checkLabel(E,bestLab,'B'); if(c<0) cout<<" CHECKFAIL"; }
            cout<<" labels:"; for(int l:bestLab) cout<<" "<<l; }
        cout<<"\n"; cout.flush(); idx++;
    }
}
