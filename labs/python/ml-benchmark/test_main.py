from main import benchmark

def test_models():
    out=benchmark()
    assert len(out)==3
    assert all(0.0<=v['test_accuracy']<=1.0 for v in out.values())
    assert all(len(v['confusion_matrix'])==3 for v in out.values())
