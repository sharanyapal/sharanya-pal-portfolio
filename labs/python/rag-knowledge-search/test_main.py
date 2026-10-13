from pathlib import Path
from main import tokens,chunks,retrieve

def test_search():
    docs=chunks(Path(__file__).with_name('docs'))
    hits=retrieve('least privilege access',docs)
    assert hits and 'iam-guide' in hits[0]['id']
def test_abstain():
    docs=chunks(Path(__file__).with_name('docs'))
    assert not retrieve('quasars neutron uranium',docs)
def test_tokenize():
    assert tokens('What is least privilege?')==['least','privilege']
