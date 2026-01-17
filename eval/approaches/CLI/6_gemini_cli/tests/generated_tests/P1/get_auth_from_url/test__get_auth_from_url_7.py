import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_string():
    url = ""
    auth = get_auth_from_url(url)
    assert auth == ("", "")
