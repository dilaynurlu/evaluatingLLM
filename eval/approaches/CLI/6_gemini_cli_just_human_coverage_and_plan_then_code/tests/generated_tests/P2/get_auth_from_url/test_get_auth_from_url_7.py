import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_complex():
    url = "http://user:pass@example.com/path?query=1#frag"
    auth = get_auth_from_url(url)
    assert auth == ("user", "pass")
