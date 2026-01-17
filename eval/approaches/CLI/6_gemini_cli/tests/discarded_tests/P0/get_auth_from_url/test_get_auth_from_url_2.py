
import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_username_only():
    url = "http://user@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user", None)
