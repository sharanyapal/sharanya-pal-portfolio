#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#define N 12
#define INF 1e20
static const int blocked[N]={0,0,0,0,0,1,1,0,0,0,0,0};
static int parent[N],closed[N];static double score[N];
static int heap[100],count=0;
static void push(int v){int i=++count;while(i>1&&score[heap[i/2]]>score[v]){heap[i]=heap[i/2];i/=2;}heap[i]=v;}
static int pop(void){int top=heap[1],v=heap[count--],i=1,k;while(i*2<=count){k=i*2;if(k<count&&score[heap[k+1]]<score[heap[k]])k++;if(score[v]<=score[heap[k]])break;heap[i]=heap[k];i=k;}heap[i]=v;return top;}
static double h(int a,int b){return abs(a/4-b/4)+abs(a%4-b%4);} /* admissible Manhattan */
int astar(int start,int goal){double g[N];count=0;for(int i=0;i<N;i++){g[i]=INF;score[i]=INF;closed[i]=0;parent[i]=-1;}if(blocked[start]||blocked[goal])return -1;g[start]=0;score[start]=h(start,goal);push(start);while(count){int u=pop();if(closed[u])continue;closed[u]=1;if(u==goal)return (int)g[u];for(int dir=0;dir<4;dir++){int r=u/4,c=u%4,nr=r+(dir==0)-(dir==1),nc=c+(dir==2)-(dir==3);if(nr<0||nr>=3||nc<0||nc>=4)continue;int v=nr*4+nc;if(blocked[v]||closed[v])continue;double next=g[u]+1;if(next<g[v]){g[v]=next;parent[v]=u;score[v]=next+h(v,goal);push(v);}}}return -1;}
int main(void){int distance=astar(0,11);if(distance!=5){fprintf(stderr,"expected route cost 5, got %d\n",distance);return 1;}printf("A* shortest route length=%d\npath: ",distance);int route[N],n=0;for(int v=11;v!=-1;v=parent[v])route[n++]=v;for(int i=n-1;i>=0;i--)printf("%d%s",route[i],i?" -> ":"\n");return 0;}
