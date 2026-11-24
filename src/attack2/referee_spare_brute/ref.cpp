// referee search: relaxed growth labeling, written from the definition.
// input lines: name n root a b a b ...   args: slack cap mode seed
// mode 0: find one; mode 1: count all (no symmetry reduction); mode 2: piece mode (args b j follow): path arms, crossing, tip innermost
#include <bits/stdc++.h>
using namespace std;
int n,N,root; vector<vector<int>> adj,ch; vector<int> par,dep,code,lab; vector<char> used; vector<int> placed;
long long nodes,cap,sols; int mode; unsigned seed; mt19937 rng;
int maxEven,minOdd; int tipY; bool capped; vector<int> sol;
map<vector<int>,int> codes;
int getcode(int v){ vector<int> c; for(int w:ch[v]) c.push_back(getcode(w)); sort(c.begin(),c.end()); auto it=codes.find(c); if(it==codes.end()) it=codes.emplace(c,(int)codes.size()).first; return code[v]=it->second; }
bool leafOK(){ // piece final check
  // crossing already enforced; innermost: tip is min odd label or max even label
  if(dep[tipY]&1) return lab[tipY]==minOdd; else return lab[tipY]==maxEven; }
bool rec(int L,int cnt){
  if(cnt==n){ if(mode==2){ if(!leafOK()) return false; } sols++; if(sols==1) sol=lab; return mode==0|| (mode==2); }
  if(n-cnt>L) return false;
  if(++nodes>cap){capped=true;return true;}
  struct C{int u,c,p;}; vector<C> cs;
  for(int u:placed){ int last=-1;
    for(int c:ch[u]) if(lab[c]<0){ if(mode!=1 && code[c]==last) continue; last=code[c];
      for(int sg=-1;sg<=1;sg+=2){ int p=lab[u]+sg*L; if(p<0||p>=N||used[p]) continue;
        if(mode==2){ if(dep[c]&1){ if(p<maxEven) continue;} else { if(p>minOdd) continue; } }
        cs.push_back({u,c,p}); } } }
  if(seed) shuffle(cs.begin(),cs.end(),rng);
  bool canskip = (n-cnt<=L-1);
  bool skipfirst = seed && canskip && (rng()%4==0);
  if(skipfirst){ if(rec(L-1,cnt)) return true; }
  for(auto&x:cs){ int sme=maxEven,smo=minOdd; lab[x.c]=x.p; used[x.p]=1; placed.push_back(x.c);
    if(dep[x.c]&1) minOdd=min(minOdd,x.p); else maxEven=max(maxEven,x.p);
    bool r=rec(L-1,cnt+1);
    placed.pop_back(); used[x.p]=0; lab[x.c]=-1; maxEven=sme; minOdd=smo; if(r) return true; }
  if(canskip && !skipfirst){ if(rec(L-1,cnt)) return true; }
  return false; }
int main(int argc,char**argv){ int slack=atoi(argv[1]); cap=atoll(argv[2]); mode=atoi(argv[3]); seed=argc>4?atoi(argv[4]):0; int restarts=argc>5?atoi(argv[5]):1;
  string line; long long found=0,none=0,capc=0,tot=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); string name; is>>name>>n>>root; adj.assign(n,{}); int a,b; while(is>>a>>b){adj[a].push_back(b);adj[b].push_back(a);}
    N=n+slack; par.assign(n,-1); dep.assign(n,0); ch.assign(n,{}); code.assign(n,0); codes.clear();
    vector<int> st={root}; vector<char> seen(n,0); seen[root]=1; while(!st.empty()){int v=st.back();st.pop_back(); for(int w:adj[v]) if(!seen[w]){seen[w]=1;par[w]=v;dep[w]=dep[v]+1;ch[v].push_back(w);st.push_back(w);} }
    getcode(root); for(int v=0;v<n;v++) sort(ch[v].begin(),ch[v].end(),[&](int x,int y){return code[x]<code[y];});
    tipY=n-1; string status="NONE"; 
    for(int t=0;t<restarts;t++){ rng.seed(seed+t*7919); lab.assign(n,-1); used.assign(N,0); placed={root}; lab[root]=0; used[0]=1; nodes=0; sols=0; capped=false; maxEven=0; minOdd=INT_MAX;
      rec(N-1,1);
      if(sols>0 && (mode!=1)){status="FOUND";break;} if(mode==1){ status=capped?"CAP":"COUNT"; break;} if(capped) status="CAP"; else {status="NONE";break;} }
    tot++; if(status=="FOUND")found++; else if(status=="NONE")none++; else if(status=="CAP")capc++;
    cout<<name<<" "<<status; if(mode==1) cout<<" "<<sols; cout<<" nodes="<<nodes; if(status=="FOUND"){ cout<<" :"; for(int v=0;v<n;v++) cout<<" "<<sol[v]; } cout<<"\n"; }
  cerr<<"total="<<tot<<" found="<<found<<" none="<<none<<" cap="<<capc<<"\n"; }
