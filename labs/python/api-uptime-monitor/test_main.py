import pytest
from main import check_target

def test_http_urls():
    check_target('https://example.org/health')
def test_reject_file_protocol():
    with pytest.raises(ValueError): check_target('file:///etc/passwd')
