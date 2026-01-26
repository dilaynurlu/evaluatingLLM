import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_bytes_input():
    """
    Test that providing a bytes URL works and returns a tuple of strings.
    
    urlparse handles bytes and returns byte components. 
    unquote handles bytes by decoding them to strings (default utf-8).
    """
    url = b"http://byteuser:bytepass@example.com"
    expected_auth = ("byteuser", "bytepass")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth
    assert isinstance(auth[0], str)
    assert isinstance(auth[1], str)