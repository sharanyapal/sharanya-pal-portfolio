"""Detect spikes in request counts using robust median absolute deviation."""
import argparse
import csv
import json
import statistics
from pathlib import Path

def detect(values:list[float],threshold:float=3.5)->list[dict]:
    if len(values)<3: return []
    baseline=statistics.median(values)
    mad=statistics.median(abs(x-baseline) for x in values)
    if mad==0:
        # Use a non-zero absolute guard when observations are mostly identical.
        return [{'index':i,'value':v,'score':None} for i,v in enumerate(values) if abs(v-baseline)>max(1,baseline*.25)]
    return [{'index':i,'value':v,'score':round(.6745*(v-baseline)/mad,3)} for i,v in enumerate(values) if abs(.6745*(v-baseline)/mad)>threshold]

def analyze(path:Path)->dict:
    with path.open(newline='',encoding='utf8') as fh:
        rows=list(csv.DictReader(fh))
    counts=[float(r['requests']) for r in rows]
    out=detect(counts)
    return {'samples':len(rows),'baseline':statistics.median(counts) if counts else None,'anomalies':[{'timestamp':rows[x['index']]['timestamp'],**x} for x in out]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,default=Path(__file__).with_name('traffic.csv'));args=p.parse_args()
    print(json.dumps(analyze(args.csv),indent=2))
if __name__=='__main__':main()
