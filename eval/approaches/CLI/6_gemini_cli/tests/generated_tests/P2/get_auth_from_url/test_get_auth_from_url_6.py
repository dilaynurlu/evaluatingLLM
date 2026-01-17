import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_with_port():
    url = "http://user:pass@example.com:8080"
    auth = get_auth_from_url(url)
    assert auth == ("user", "pass")
