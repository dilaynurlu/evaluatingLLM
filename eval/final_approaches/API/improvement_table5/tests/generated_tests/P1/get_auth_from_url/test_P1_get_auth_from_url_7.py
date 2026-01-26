import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_bytes_input():
    """
    Test that the function handles bytes URL input correctly.
    
    The internal usage of urlparse handles bytes, and requests.utils.unquote 
    decodes bytes to string. Thus, the returned authentication tuple should 
    contain strings (unicode), not bytes.
    """
    url = b"http://byteuser:bytepass@example.com/"
    expected_auth = ("byteuser", "bytepass")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth
    assert isinstance(auth[0], str)
    assert isinstance(auth[1], str)