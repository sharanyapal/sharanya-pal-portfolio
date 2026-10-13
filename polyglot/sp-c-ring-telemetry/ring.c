#include <stdio.h>
#include <assert.h>
#include <stdint.h>
#include <string.h>
#define CAP 128
typedef struct{uint64_t timestamp_ms;double latency_ms;int status;char service[24];} Event;
typedef struct{Event events[CAP];size_t head,len;uint64_t lost;} Ring;
void ingest(Ring*r,Event e){if(r->len==CAP)r->lost++;else r->len++;r->events[r->head]=e;r->head=(r->head+1)%CAP;}
Event get(const Ring*r,size_t offset){assert(offset<r->len);size_t start=(r->head+CAP-r->len)%CAP;return r->events[(start+offset)%CAP];}
double avg(const Ring*r){if(r->len==0)return 0;double sum=0;for(size_t i=0;i<r->len;i++)sum+=get(r,i).latency_ms;return sum/r->len;}
int count_5xx(const Ring*r){int c=0;for(size_t i=0;i<r->len;i++)if(get(r,i).status>=500)c++;return c;}
int main(void){Ring r={0};for(int i=0;i<200;i++){Event e={(uint64_t)i*100,100.0+i,(i%9==0)?503:200,"service-api"};ingest(&r,e);}assert(r.len==CAP);assert(r.lost==72);assert(get(&r,0).timestamp_ms==7200);assert(get(&r,127).timestamp_ms==19900);printf("ring len=%zu dropped=%llu avg=%.2f 5xx=%d\n",r.len,(unsigned long long)r.lost,avg(&r),count_5xx(&r));return 0;}
