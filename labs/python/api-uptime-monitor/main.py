"""Async HTTP uptime probe, with opt-in hosts and defensive timeout settings."""
import argparse
import asyncio
import json
import time
from urllib.parse import urlparse
import httpx

def check_target(url:str)->None:
    parsed=urlparse(url)
    if parsed.scheme not in {'http','https'} or not parsed.hostname: raise ValueError('Expected http(s) URL')
    # Educational client: user controls target. Do not expose as an unrestricted server-side URL fetcher.

async def probe(url:str,timeout=6.0)->dict:
    check_target(url)
    start=time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=timeout,follow_redirects=False) as client:
            response=await client.get(url)
        status=response.status_code
        return {'url':url,'status':status,'healthy':200<=status<400,'latency_ms':round((time.perf_counter()-start)*1000,1)}
    except httpx.RequestError as exc:
        return {'url':url,'status':None,'healthy':False,'error':type(exc).__name__,'latency_ms':round((time.perf_counter()-start)*1000,1)}

async def monitor(urls:list[str])->list[dict]:
    return await asyncio.gather(*(probe(url) for url in urls))

def main():
    p=argparse.ArgumentParser();p.add_argument('urls',nargs='+',help='Sites you are authorized to monitor');args=p.parse_args()
    print(json.dumps(asyncio.run(monitor(args.urls)),indent=2))
if __name__=='__main__':main()
