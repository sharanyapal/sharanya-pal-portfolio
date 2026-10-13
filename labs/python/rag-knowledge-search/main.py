"""Citation-grounded local retrieval with optional OpenAI-compatible LLM answers.
No API key is required for document search. Explicitly abstains when relevance is poor.
"""
from __future__ import annotations
import argparse
import json
import math
import os
import re
import urllib.request
from collections import Counter
from pathlib import Path

STOP = {'the','a','an','and','to','in','of','are','is','at','on','for','with','how','what','does','our','from'}

def tokens(text: str) -> list[str]:
    return [x for x in re.findall(r"[a-z0-9]+", text.lower()) if x not in STOP]

def chunks(directory: Path) -> list[dict]:
    docs = []
    for path in sorted(directory.glob('*.md')):
        content = path.read_text(encoding='utf8')
        for i, block in enumerate(re.split(r'\n\s*\n', content)):
            if block.strip(): docs.append({'id': f'{path.name}#{i+1}', 'text': block.strip()})
    return docs

def retrieve(question: str, documents: list[dict], top_k: int=3, min_score: float=.11) -> list[dict]:
    if not documents: return []
    q = Counter(tokens(question))
    counts = [Counter(tokens(d['text'])) for d in documents]
    df = Counter(word for row in counts for word in row)
    def vec(c): return {word: (1+math.log(cnt))*math.log(1+(len(counts)+1)/(df[word]+1)) for word,cnt in c.items()}
    def cosine(a,b):
        dot=sum(v*b.get(k,0) for k,v in a.items())
        return dot/(math.sqrt(sum(v*v for v in a.values()))*math.sqrt(sum(v*v for v in b.values())) or 1)
    qv=vec(q)
    scored=[dict(d,score=round(cosine(qv,vec(c)),4)) for d,c in zip(documents,counts)]
    return [x for x in sorted(scored,key=lambda x:x['score'],reverse=True)[:top_k] if x['score']>=min_score]

def optional_llm(question:str, passages:list[dict]) -> str:
    """Calls a configured OpenAI-compatible /chat/completions endpoint; NEVER prints secrets."""
    api_key=os.getenv('LLM_API_KEY')
    if not api_key: return 'LLM disabled (set LLM_API_KEY and LLM_API_URL). Retrieval results are available above.'
    url=os.getenv('LLM_API_URL')
    if not url or not url.startswith('https://'): raise ValueError('LLM_API_URL must be a trusted HTTPS endpoint')
    prompt='\n\n'.join(f"[{p['id']}] {p['text']}" for p in passages)
    data=json.dumps({'model':os.getenv('LLM_MODEL','gpt-4o-mini'), 'messages':[{'role':'system','content':'Use only the provided passages. Cite [document#section]. If evidence is insufficient, say so.'},{'role':'user','content':f'Question: {question}\n\nPassages:\n{prompt}'}], 'temperature':0}).encode()
    req=urllib.request.Request(url,data=data,headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=20) as response:
        answer=json.load(response)
    return answer['choices'][0]['message']['content']

def main():
    parser=argparse.ArgumentParser(description='Local citation-grounded retrieval')
    parser.add_argument('question',nargs='?',default='How do least privilege and access reviews work?')
    parser.add_argument('--docs',type=Path,default=Path(__file__).with_name('docs'))
    parser.add_argument('--llm',action='store_true',help='Use optional configured LLM API')
    args=parser.parse_args()
    found=retrieve(args.question,chunks(args.docs))
    if not found:
        print('No sufficiently relevant local evidence found.');return
    for p in found: print(f"[{p['id']}] confidence={p['score']:.3f}\n{p['text']}\n")
    if args.llm: print('Grounded answer:\n'+optional_llm(args.question,found))

if __name__=='__main__': main()
