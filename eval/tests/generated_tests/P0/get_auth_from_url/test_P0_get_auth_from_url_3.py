import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that URLs without authentication components return a tuple of empty strings.
    This scenario triggers the TypeError exception path internally because
    parsed.username and parsed.password are None, causing unquote(None) to fail.
    """
    url = "http://example.com/index.html"
    expected_auth = ("", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth