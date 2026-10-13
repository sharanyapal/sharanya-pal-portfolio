"""Offline source sanity checks. Python/Java tests run separately."""
from pathlib import Path
import json
import re
import subprocess
ROOT=Path(__file__).parent
projects=json.loads((ROOT/'projects.json').read_text(encoding='utf8'))
assert len(projects)==24 and len(set(x['id'] for x in projects))==24
assert len([x for x in projects if x['live']])==12
for p in projects:
    root=(ROOT/'apps'/p['id']) if p['live'] else ROOT/('sql' if p['language']=='SQL' else p['language'].lower())/p['id']
    assert root.is_dir(),root
    assert (root/'README.md').is_file(),root
    if p['live']:
        assert (root/'index.html').is_file()
        assert (root/'app.js').is_file()
        subprocess.run(['node','--check',str(root/'app.js')],check=True,stdout=subprocess.DEVNULL)
for path in [ROOT/'assets'/'gallery.js',ROOT/'assets'/'app.js']:
    subprocess.run(['node','--check',str(path)],check=True,stdout=subprocess.DEVNULL)
for html in [ROOT/'index.html',*(ROOT/'apps').glob('*/index.html')]:
    contents=html.read_text(encoding='utf8')
    assert '<!doctype html>' in contents.lower()
    for ref in re.findall(r'(?:src|href)="([^"]+)"',contents):
        if ref.startswith(('http:','https:','#','mailto:','data:')):continue
        assert (html.parent/ref).exists(),(html,ref)
print('PASS: 24 project manifests, 12 browser app structures, JavaScript syntax and relative references')
