// print the canonical form (same AHU form as enum.h) of every tree on n vertices, using the repo's generator src/treegen.h
#include "enum.h"
#include "../../treegen.h"
int main(int argc,char**argv){ int n=atoi(argv[1]); TreeGen g(n); vector<int> par; long c=0; while(g.next()){ g.parents(par); vector<vector<int>> adj(n+1); for(int i=1;i<n;i++){ adj[i+1].push_back(par[i]+1); adj[par[i]+1].push_back(i+1); } printf("%s\n",canonAdj(adj,n).c_str()); c++; } fprintf(stderr,"%ld trees\n",c); }
