import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_bytes_input():
    """
    Test that the function accepts bytes input and returns string tuples
    (unquote handles decoding).
    """
    url = b"http://byteuser:bytepass@example.com"
    expected_auth = ("byteuser", "bytepass")
    
    assert get_auth_from_url(url) == expected_auth