
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded():
    url = "http://user%40name:p%40ss@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user@name", "p@ss")
