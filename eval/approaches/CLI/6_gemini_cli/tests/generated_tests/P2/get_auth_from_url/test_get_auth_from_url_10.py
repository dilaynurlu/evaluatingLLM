import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username_with_password():
    # :password@host
    url = "http://:password@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("", "password")
