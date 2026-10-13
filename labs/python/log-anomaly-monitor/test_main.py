from pathlib import Path
from main import detect, analyze

def test_spike():
    out=detect([50,51,49,50,52,400,48,50,52])
    assert any(x['value']==400 for x in out)
def test_csv():
    result=analyze(Path(__file__).with_name('traffic.csv'))
    assert result['samples']==10
    assert result['anomalies']
