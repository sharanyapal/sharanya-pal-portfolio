"""Reference-first local RAG retrieval with BM25, evidence citations and abstention.
OpenAI inference is optional and isolated behind an environment variable.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
import math
import os
import re
import json
import argparse

WORDS=re.compile(r'[a-z0-9]+',re.I)
def tokens(text: str) -> list[str]: return WORDS.findall(text.lower())
@dataclass(frozen=True)
class Passage:
    source: str
    number: int
    text: str

class Retriever:
    def __init__(self, documents: dict[str,str], chunk_words:int=95, overlap:int=18):
        if chunk_words<=overlap or overlap<0: raise ValueError('chunk_words must exceed overlap')
        self.passages=[]
        for source,text in documents.items():
            terms=text.split()
            for i,start in enumerate(range(0,len(terms),chunk_words-overlap)):
                snippet=' '.join(terms[start:start+chunk_words])
                if snippet: self.passages.append(Passage(source,i+1,snippet))
        self.freq=[Counter(tokens(p.text)) for p in self.passages]
        self.lengths=[sum(c.values()) for c in self.freq]
        self.avglen=sum(self.lengths)/max(1,len(self.lengths))
        self.df=Counter(t for f in self.freq for t in f)

    def search(self,query:str,k:int=4) -> list[tuple[float,Passage]]:
        n=len(self.passages);scores=[]
        for i,freq in enumerate(self.freq):
            score=0.0
            for term in set(tokens(query)):
                if not freq[term]:continue
                idf=math.log(1+(n-self.df[term]+.5)/(self.df[term]+.5))
                tf=freq[term]
                score+=idf*tf*2.2/(tf+1.2*(.25+.75*self.lengths[i]/max(1,self.avglen)))
            if score>0:scores.append((score,self.passages[i]))
        return sorted(scores,key=lambda x:(-x[0],x[1].source,x[1].number))[:k]

    def answer(self,query:str,k:int=3,threshold:float=.05) -> dict:
        hits=self.search(query,k)
        if not hits or hits[0][0]<threshold:
            return {'answer':'Insufficient evidence in indexed documents.', 'citations':[], 'abstained':True}
        citations=[{'source':p.source,'chunk':p.number,'score':round(score,4),'excerpt':p.text}
                   for score,p in hits]
        # The offline answer is EXTRACTIVE, not made up or claimed to be an LLM response.
        summary=' '.join(p.text.split('. ')[0].strip()+'.' for _,p in hits)
        return {'answer':summary,'citations':citations,'abstained':False}

def optional_openai_answer(question:str, evidence:dict) -> str:
    """Requires a server-side API key; never expose keys in client-side JavaScript."""
    key=os.environ.get('OPENAI_API_KEY')
    if not key: raise RuntimeError('Set OPENAI_API_KEY in your server environment to enable model inference.')
    from openai import OpenAI
    client=OpenAI(api_key=key)
    contexts='\n'.join(f"[{x['source']}#{x['chunk']}] {x['excerpt']}" for x in evidence['citations'])
    result=client.responses.create(model=os.environ.get('OPENAI_MODEL','gpt-4.1-mini'),input=(
      'Answer only using these passages. Cite source#chunk. If insufficient, say so.\n'+contexts+'\nQuestion: '+question))
    return result.output_text

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('files',nargs='+');parser.add_argument('--question',required=True)
    args=parser.parse_args();docs={f:open(f,encoding='utf8').read() for f in args.files}
    print(json.dumps(Retriever(docs).answer(args.question),indent=2))
