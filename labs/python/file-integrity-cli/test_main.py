from main import manifest,verify

def test_verify_detects_tampering(tmp_path):
    (tmp_path/'sample.txt').write_text('hello')
    m=manifest(tmp_path)
    assert verify(tmp_path,m)['valid']
    (tmp_path/'sample.txt').write_text('changed')
    assert not verify(tmp_path,m)['valid']
def test_prevent_escape(tmp_path):
    r=verify(tmp_path,{'files':{'../outside':'abc'}})
    assert not r['valid']
