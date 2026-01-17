import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_password():
    url = "http://user:pa%24s@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "pa$s")
