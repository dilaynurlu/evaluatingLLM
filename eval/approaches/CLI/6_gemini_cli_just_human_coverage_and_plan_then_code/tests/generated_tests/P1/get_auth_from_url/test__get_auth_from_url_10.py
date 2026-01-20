import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_complex_chars():
    # http://user:pass@word@example.com -> user:pass, host: word@example.com? No.
    # @ delimits userinfo. Last @ is the delimiter.
    # http://u:p@host -> u, p
    # http://u:p@ss@host -> u, p@ss
    url = "http://user:p%40ss@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", "p@ss")
