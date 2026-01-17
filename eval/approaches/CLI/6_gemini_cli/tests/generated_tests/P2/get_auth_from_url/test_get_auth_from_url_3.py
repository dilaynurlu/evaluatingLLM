import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_none():
    url = "http://example.com"
    auth = get_auth_from_url(url)
    # username=None, password=None -> TypeError in unquote -> returns ("", "")
    assert auth == ("", "")
