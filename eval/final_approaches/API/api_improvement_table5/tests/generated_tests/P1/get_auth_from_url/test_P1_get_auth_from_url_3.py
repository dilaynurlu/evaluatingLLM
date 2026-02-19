import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that a URL with no authentication components returns a tuple of empty strings.
    
    This scenario triggers the exception handler within get_auth_from_url, 
    as parsed.username and parsed.password are None, causing unquote(None) 
    to raise a TypeError which is caught and handled.
    """
    url = "http://example.com/index.html"
    expected_auth = ("", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth