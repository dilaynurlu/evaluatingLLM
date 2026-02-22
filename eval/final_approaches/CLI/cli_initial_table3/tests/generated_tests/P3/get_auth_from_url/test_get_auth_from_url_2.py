import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_2():
    # Percent encoded
    url = "http://user%40mail:p%40ss@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user@mail", "p@ss")
