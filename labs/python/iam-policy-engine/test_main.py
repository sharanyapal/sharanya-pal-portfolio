from main import Identity, authorize, audit

def test_explicit_access():
    assert authorize(Identity('x', ('analyst',)), 'reports', 'write')['allow']
def test_default_deny():
    assert not authorize(Identity('x', ('viewer',)), 'incidents', 'delete')['allow']
def test_inactive():
    assert not authorize(Identity('x', ('admin',), False), 'reports', 'read')['allow']
def test_sod_conflict():
    report = audit([Identity('x', ('admin','auditor'))])
    assert report['findings'] and not report['passed']
