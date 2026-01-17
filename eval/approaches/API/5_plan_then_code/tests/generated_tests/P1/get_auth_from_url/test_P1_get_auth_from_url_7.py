import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_bytes_input():
    """
    Test that the function accepts a bytes URL and returns the auth components
    as decoded strings (utf-8 default).
    """
    url = b"http://user:password@example.com/"
    expected_auth = ("user", "password")
    
    assert get_auth_from_url(url) == expected_auth