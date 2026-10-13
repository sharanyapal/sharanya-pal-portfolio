"""Build and verify a SHA-256 manifest of relative paths, guarding against path escapes."""
import argparse
import hashlib
import json
from pathlib import Path

CHUNK = 1024*1024

def hash_file(path:Path)->str:
    digest=hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda:handle.read(CHUNK),b''):digest.update(block)
    return digest.hexdigest()

def manifest(root:Path)->dict:
    root=root.resolve()
    records={}
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.is_symlink() or path.name=='manifest.json':continue
        rel=path.relative_to(root).as_posix()
        records[rel]=hash_file(path)
    return {'algorithm':'sha256','files':records}

def verify(root:Path,data:dict)->dict:
    root=root.resolve()
    checked,issues=0,[]
    for rel,expected in data['files'].items():
        path=(root/rel).resolve()
        if not path.is_relative_to(root):
            issues.append(f'{rel}: unsafe path');continue
        if not path.is_file():issues.append(f'{rel}: missing');continue
        checked+=1
        if hash_file(path)!=expected:issues.append(f'{rel}: modified')
    return {'checked':checked,'valid':not issues,'issues':issues}

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['build','verify']);p.add_argument('directory',type=Path);args=p.parse_args()
    path=args.directory/'manifest.json'
    if args.command=='build':
        result=manifest(args.directory);path.write_text(json.dumps(result,indent=2),encoding='utf8');print(f'Manifest saved: {path}')
    else:
        result=verify(args.directory,json.loads(path.read_text(encoding='utf8')));print(json.dumps(result,indent=2));raise SystemExit(0 if result['valid'] else 1)
if __name__=='__main__':main()
