"""Deterministic walk-forward performance and bootstrap Value at Risk diagnostics."""
from __future__ import annotations
from collections import deque
import argparse,csv,json,math,random,statistics

def drawdown(equity:list[float])->float:
    peak=equity[0] if equity else 1
    worst=0.0
    for v in equity:
        peak=max(peak,v)
        worst=max(worst,1-v/peak)
    return worst

def ema(values:list[float],period:int)->list[float]:
    if period<1 or not values:raise ValueError('Invalid EMA period / prices')
    a=2/(period+1);v=values[0];out=[]
    for x in values:v=(1-a)*v+a*x;out.append(v)
    return out

def strategy(prices:list[float],short:int=8,long:int=21,fee:float=.001)->dict:
    """Execute the crossover detected at t-1 on bar t; avoid look-ahead bias."""
    if len(prices)<long+3 or short>=long or short<2 or any(p<=0 for p in prices):raise ValueError('Invalid prices or periods')
    fast=ema(prices,short);slow=ema(prices,long)
    cash=10000.0;shares=0.0;curve=[];trades=[]
    for i,p in enumerate(prices):
        if i>long:
            prev=fast[i-2]>slow[i-2];curr=fast[i-1]>slow[i-1]
            if curr and not prev and shares==0:
                shares=cash*(1-fee)/p;cash=0;trades.append({'day':i,'side':'BUY','price':p})
            elif prev and not curr and shares>0:
                cash=shares*p*(1-fee);shares=0;trades.append({'day':i,'side':'SELL','price':p})
        curve.append(cash+shares*p)
    ret=curve[-1]/curve[0]-1
    returns=[curve[i]/curve[i-1]-1 for i in range(1,len(curve))]
    return {'return':ret,'hold_return':prices[-1]/prices[0]-1,
            'max_drawdown':drawdown(curve),'trade_count':len(trades),'equity':curve,'daily_returns':returns}

def bootstrap_var(returns:list[float],confidence:float=.95,replications:int=3000,seed:int=42)->dict:
    if not returns or not 0<confidence<1:raise ValueError('No returns or invalid confidence')
    rng=random.Random(seed);sim=[rng.choice(returns) for _ in range(replications)]
    sim.sort();tail=max(1,int((1-confidence)*len(sim)))
    return {'var':-sim[tail-1],'expected_shortfall':-statistics.mean(sim[:tail]),
            'confidence':confidence,'bootstrap_samples':len(sim)}

def read_csv(path):
    with open(path,newline='',encoding='utf8') as f:return [float(r['Close']) for r in csv.DictReader(f)]

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--short',type=int,default=8);p.add_argument('--long',type=int,default=21)
    a=p.parse_args();r=strategy(read_csv(a.csv),a.short,a.long)
    print(json.dumps({**{k:v for k,v in r.items() if k not in ('equity','daily_returns')},'risk':bootstrap_var(r['daily_returns'])},indent=2))
