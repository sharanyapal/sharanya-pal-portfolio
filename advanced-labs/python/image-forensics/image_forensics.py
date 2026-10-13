"""Safe image integrity and duplicate analysis. Requires Pillow; no malware analysis."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageOps

def digest(path:str)->str:
    h=hashlib.sha256()
    with open(path,'rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def difference_hash(path:str,size:int=8)->int:
    if size<2:raise ValueError('hash size too small')
    with Image.open(path) as im:
        im=ImageOps.exif_transpose(im).convert('L').resize((size+1,size),Image.Resampling.LANCZOS)
        values=list(im.getdata())
    bits=0
    for row in range(size):
        for col in range(size):
            bits=(bits<<1)|int(values[row*(size+1)+col]>values[row*(size+1)+col+1])
    return bits

def compare(a:str,b:str)->dict:
    x=difference_hash(a);y=difference_hash(b)
    return {'exact_same_sha256':digest(a)==digest(b),'perceptual_distance':(x^y).bit_count(),
            'phash_similarity_label':'very similar' if (x^y).bit_count()<=8 else 'different'}

def strip_metadata(source:str,target:str)->None:
    with Image.open(source) as image:
        im=ImageOps.exif_transpose(image).convert('RGB');im.save(target,format='PNG')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('first');p.add_argument('second');p.add_argument('--clean-output')
    a=p.parse_args();print(json.dumps(compare(a.first,a.second),indent=2))
    if a.clean_output:strip_metadata(a.first,a.clean_output)
