from main import model, predict

def test_pipeline():
    pipeline, X, y=model()
    assert len(X)==len(y)==24
    assert len(pipeline.classes_)==4
def test_prediction():
    result=predict('VPN connection drops intermittently')
    assert result['category'] in {'network','identity','application','hardware'}
    assert 0<=result['confidence']<=1
