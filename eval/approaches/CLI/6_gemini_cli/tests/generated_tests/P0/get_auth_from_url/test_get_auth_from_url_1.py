
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic():
    url = "http://user:pass@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "pass")
